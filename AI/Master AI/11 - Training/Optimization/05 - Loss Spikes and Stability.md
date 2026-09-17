---
tags: [training, stability, loss-spikes, gradient-clipping, debugging]
iteration: 12
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Loss Spikes, Training Stability, Loss Divergence, NaN Loss]
---

# 05 — Loss Spikes and Stability

> [!info] TL;DR
> Loss spikes — sudden, large increases in training loss during otherwise stable training — are a notorious problem in large-scale LLM training. They can be caused by bad data batches, numerical instability in mixed precision, optimizer state corruption, learning rate issues, or genuine model instability at scale. Without intervention, a single spike can cascade into divergence (loss → NaN), wasting millions of dollars of compute. The standard toolkit for handling spikes: **gradient clipping** (prevent extreme updates), **loss scaling** (for FP16), **selective skip-on-spike** (skip the bad batch), **learning rate warmup** (avoid early instability), and **checkpoint rollback** (rewind to a pre-spike checkpoint). Production training runs instrument these aggressively.

## Why Loss Spikes Happen

A loss spike is a sudden increase in training loss — typically 10× or more — that occurs during otherwise stable training. The fundamental causes fall into five categories:

### 1. Bad Data Batches

A single batch with anomalous data can produce a large loss. Common culprits:

- **Highly repetitive text**: the model fits the repetition pattern, then a non-repetitive batch produces high loss.
- **Out-of-distribution text**: a batch of code when the model expected natural language.
- **Corrupted text**: encoding errors, binary blobs misclassified as text.
- **Long-tail rare tokens**: batches with unusual tokens cause large gradients.

Even one bad batch in a million can cause a spike. The challenge is identifying it among millions of batches.

### 2. Numerical Instability

Mixed precision training (FP16, BF16, FP8) introduces numerical noise. Most of the time this noise is harmless, but occasionally it accumulates:

- **Gradient underflow**: small gradients become zero in FP16, then accumulate in the optimizer state, eventually causing a large update when they resurface.
- **Activation overflow**: large activations become inf, propagating through the network.
- **Softmax saturation**: extreme logits cause softmax to produce one-hot outputs, which then produce extreme gradients.

### 3. Optimizer State Issues

Adam's running statistics (m and v) can become corrupted:

- **v (variance) estimate becomes too small**: the next gradient appears larger than expected, producing a huge update.
- **v estimate becomes too large**: updates become tiny, training stalls (this isn't a spike but is a related failure).
- **Beta values mismatch**: if beta1/beta2 are too high, the optimizer reacts slowly to distribution shifts, then overreacts.

### 4. Learning Rate Issues

- **Warmup too fast**: the learning rate ramps up too quickly in the first few hundred steps, before the optimizer state has stabilized.
- **Decay too slow**: late in training, a high learning rate produces instability because the model is near a local minimum.
- **Schedule restarts**: cosine restarts or step decays can cause temporary spikes as the optimizer re-stabilizes.

### 5. Genuine Model Instability at Scale

Large models (70B+) can exhibit spontaneous spikes without an obvious cause. The Chinchilla and GPT-3 papers both report unexplained spikes during training. These may be related to:

- Sharp minima: the model finds a region of the loss landscape with high curvature, where small updates produce large loss changes.
- Attention pattern collapse: attention heads suddenly concentrate on a single token, producing high loss.
- MoE routing instability: in mixture-of-experts models, the router can suddenly route all tokens to one expert, producing a spike.

## Detecting Spikes

### Loss Monitoring

The most direct signal: monitor the training loss closely. A spike is typically defined as:

- **Spike threshold**: loss > 2× the moving average (or 3× the previous step).
- **NaN/Inf detection**: loss is `nan` or `inf`.

Production training runs log loss every step and alert on these conditions. A simple moving average over the last 100 steps is the baseline; exponential weighted moving averages respond faster.

### Gradient Norm Monitoring

Even when loss looks stable, gradient norms can signal trouble:

- **Gradient norm spike**: a 10× increase in the L2 norm of gradients signals an extreme update is coming.
- **Gradient norm collapse**: a 10× decrease suggests the optimizer is becoming unstable in a different way (vanishing gradients).

Log the gradient norm before clipping; the pre-clip norm is the signal.

### Weight Norm Monitoring

Track the L2 norm of each layer's weights. If a layer's weights suddenly grow or shrink, that's a sign of instability in that layer. Some training runs use weight clipping (rare) or per-layer learning rate scaling (also rare) based on these norms.

### Activation Statistics

Track mean, std, and max of activations at each layer. Spikes in activation max (especially to inf) signal numerical issues. This is more useful for debugging than for online detection (the overhead of computing these statistics is non-trivial).

## Preventing Spikes

### Gradient Clipping

The single most effective preventive measure. Clip the global gradient norm to a threshold (typically 1.0):

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

This ensures no single update can move the weights by more than `lr * 1.0` in L2 norm. It doesn't prevent the cause of the spike, but it prevents the spike from causing a catastrophic update.

Gradient clipping is so standard that essentially all production LLM training runs use it. The threshold (1.0) is a hyperparameter; lower values (0.5) are more conservative, higher values (5.0) are more permissive.

### Learning Rate Warmup

Linear warmup over the first N steps (typically 2000-10000) gradually increases the learning rate from 0 to the target. This gives the optimizer state time to stabilize before updates become large:

```python
from torch.optim.lr_scheduler import LambdaLR
import math

def get_warmup_cosine_schedule(optimizer, warmup_steps, total_steps):
    def lr_lambda(step):
        if step < warmup_steps:
            return step / warmup_steps
        progress = (step - warmup_steps) / (total_steps - warmup_steps)
        return 0.5 * (1 + math.cos(math.pi * progress))
    return LambdaLR(optimizer, lr_lambda)
```

Without warmup, training a model from random init can spike immediately — the gradients are large and the optimizer hasn't built up its variance estimate yet.

### Loss Scaling (FP16 Only)

In FP16 training, loss scaling (see [[04 - Mixed Precision Training]]) prevents gradient underflow. If you see spikes specifically in FP16 training, check the loss scaler — it may be skipping too many steps or scaling incorrectly.

### Weight Decay

Weight decay (L2 regularization) keeps weights bounded, preventing the runaway weight growth that can cause spikes:

```python
optimizer = AdamW(model.parameters(), lr=1e-4, weight_decay=0.1)
```

A weight decay of 0.1 is standard for LLM training. Too high (1.0+) slows learning; too low (0.0) risks instability.

### Stable Initialization

Initialization that produces reasonable activation magnitudes from the start reduces early-training instability:

- **He initialization** for ReLU-based networks.
- **Xavier initialization** for tanh/sigmoid.
- **Truncated normal** with small std (0.02) for Transformers (the BERT/GPT standard).

Bad initialization can cause spikes in the first few hundred steps before the optimizer stabilizes.

## Handling Spikes When They Happen

### Skip the Bad Batch

If a single batch produces a spike, skip it without updating:

```python
loss = model(batch)
if loss > spike_threshold:
    print(f"Spike detected: loss={loss.item()}")
    continue  # skip this batch
loss.backward()
optimizer.step()
```

This is effective for data-caused spikes. The bad batch is logged for later inspection.

### Checkpoint Rollback

If the spike caused a bad update (the loss doesn't recover after a few steps), roll back to the last good checkpoint:

```python
if loss.isnan() or loss > 10 * moving_average:
    # Restore from checkpoint
    model.load_state_dict(torch.load(last_good_checkpoint))
    optimizer.load_state_dict(torch.load(last_good_optimizer))
    # Skip the bad batch, continue training
    continue
```

This is the production standard for large training runs. Without checkpoint rollback, a single NaN can waste weeks of compute.

### Reduce Learning Rate

If spikes recur, reduce the learning rate by 2-10×. This is a sign that the model is near a sharp minimum where the current learning rate is too aggressive.

### Switch to BF16 (if using FP16)

If you're using FP16 and seeing frequent spikes, switch to BF16. The wider range eliminates most FP16-specific numerical issues.

### Inspect the Data

When a spike occurs, save the offending batch. Inspect it manually:

- Are there unusual tokens?
- Is the text unusually long or short?
- Is it from a different distribution than the rest?
- Is it duplicated many times across the dataset?

Patterns in the bad batches often reveal data pipeline bugs.

## Debugging Chronic Spikes

If spikes happen frequently (more than once per billion tokens), something is systematically wrong. Debugging approach:

1. **Switch to FP32**: temporarily disable mixed precision. If spikes disappear, the cause is numerical.
2. **Reduce learning rate by 10×**: if spikes disappear, the learning rate is too high.
3. **Disable optimizer state**: use plain SGD instead of Adam. If spikes disappear, the optimizer state is the problem.
4. **Reduce batch size**: if spikes disappear, large-batch instability is the cause.
5. **Inspect data**: manually examine a sample of batches. Look for anomalies.
6. **Check model init**: verify that initial activations have reasonable magnitudes (mean ≈ 0, std ≈ 1).
7. **Profile gradient flow**: check that gradients at each layer have reasonable magnitudes. Vanishing or exploding gradients at specific layers indicate architectural issues.

## Production Practices

### Frequent Checkpointing

Save a checkpoint every 1000-5000 steps. Keep the last 3-5 checkpoints so you can roll back further if needed. Storage is cheap; retraining is not.

### Spike Logging

When a spike occurs, log:

- The step number.
- The loss value before and after.
- The gradient norm before clipping.
- The batch's source and content hash (for later inspection).
- The optimizer state's beta1, beta2, and v statistics.

This data is invaluable for diagnosing chronic issues.

### Automated Recovery

Production training systems automatically detect spikes, roll back, and skip the offending batch:

```python
def train_step(model, batch, optimizer, moving_avg_loss, spike_threshold=5.0):
    loss = model(batch)
    
    # Check for spike
    if loss.isnan() or (moving_avg_loss > 0 and loss > spike_threshold * moving_avg_loss):
        log_spike(loss, batch)
        rollback_checkpoint(model, optimizer)
        return None  # signal: skip this step
    
    loss.backward()
    clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    return loss.item()
```

This is the standard pattern for production training runs at scale.

### Periodic FP32 Validation

Every N steps (e.g., 10K), run a few batches in FP32 to validate that mixed precision isn't degrading quality. If FP32 loss diverges from BF16 loss, something is wrong with the mixed precision setup.

## See Also

- [[04 - Mixed Precision Training]] — the source of many numerical spikes
- [[03 - Data Pipelines and Deduplication]] — bad data is a common spike cause
- [[02 - Distributed Training]] — distributed training adds spike complexity
- [[12 - Optimization Essentials]] — optimizer choices that affect stability
- [[14 - Learning Rate Schedules]] — LR schedule's role in stability
- [[01 - Pretraining Objectives and Scaling Laws]] — what you're optimizing
- [[11 - Training/MOC|11 Training MOC]]


## Interview Questions

1. **Q: What are the main causes of loss spikes in LLM training?**
   A: Five categories: (1) bad data batches (repetitive, OOD, corrupted text); (2) numerical instability (FP16 underflow, activation overflow, softmax saturation); (3) optimizer state issues (Adam's v estimate too small → huge update); (4) learning rate issues (warmup too fast, decay too slow); (5) genuine model instability at scale (sharp minima, attention collapse, MoE routing instability).

2. **Q: How do you detect and handle a loss spike in production?**
   A: Detection: monitor loss every step; alert if loss > 2x moving average or is NaN/Inf. Also monitor gradient norm (10x increase signals extreme update). Handling: (1) skip the bad batch without updating; (2) if loss doesn't recover, checkpoint rollback to last good state; (3) reduce LR by 2-10x; (4) switch from FP16 to BF16; (5) inspect the offending batch for anomalies.

3. **Q: Why is gradient clipping essential for Transformer training?**
   A: Gradient clipping caps the global gradient L2 norm to a threshold (typically 1.0). This prevents extreme updates from spikes. It doesn't prevent the cause of the spike, but it prevents the spike from causing a catastrophic weight update that leads to divergence. Every production LLM training run uses it.

4. **Q: How does checkpoint rollback work for spike recovery?**
   A: Save checkpoints every 1000-5000 steps. When a spike causes a bad update (loss doesn't recover), restore model + optimizer state from the last good checkpoint, skip the offending batch, and continue. Without this, a single NaN can waste weeks of compute. Production systems automate this: detect spike → rollback → skip batch → continue.

5. **Q: What is the relationship between learning rate warmup and training stability?**
   A: Without warmup, the first steps have large gradients (random init → high loss) and Adam's bias correction hasn't stabilized. A high LR amplifies these, causing divergence. Warmup linearly ramps LR from 0 to peak over 2000-10000 steps, giving the optimizer time to build up its variance estimate. This is essential for Transformers.

6. **Q: How do you debug chronic loss spikes?**
   A: Systematic approach: (1) switch to FP32 — if spikes disappear, cause is numerical; (2) reduce LR by 10x — if spikes disappear, LR too high; (3) use plain SGD instead of Adam — if spikes disappear, optimizer state is the problem; (4) reduce batch size — if spikes disappear, large-batch instability; (5) inspect data for anomalies; (6) check init scale; (7) profile gradient flow per layer.

## Connection to Other Concepts

- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — source of many numerical spikes.
- [[11 - Training/Data/03 - Data Pipelines and Deduplication|Data Pipelines]] — bad data is a common spike cause.
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — gradient clipping and LR.
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|Learning Rate Schedules]] — warmup prevents early spikes.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — the gradient pathologies.
- [[27 - Projects/Capstones/11 - Build a Distributed Training Pipeline|Distributed Training Pipeline]] — checkpointing and recovery.
