---
tags: [mathematics, optimization, gradient-descent, adam, learning-rate]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Optimization Essentials]
---

# Optimization Essentials

> [!info] TL;DR
> Training a neural network = minimizing a loss function by following the (negative) gradient. This note covers gradient descent, SGD with momentum, Adam/AdamW, learning-rate schedules, and the practical choices that dominate modern LLM training.

## Gradient Descent

To minimize a loss $L(\boldsymbol{\theta})$, repeatedly step in the direction of steepest descent:

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \nabla L(\boldsymbol{\theta}_t)
$$

where $\eta$ is the **learning rate** (step size).

### Stochastic Gradient Descent (SGD)

In practice, $L$ is a sum over a dataset:

$$
L(\boldsymbol{\theta}) = \frac{1}{N} \sum_{i=1}^{N} \ell_i(\boldsymbol{\theta})
$$

Computing the full gradient is expensive. **SGD** approximates it with a mini-batch of size $B \ll N$:

$$
\nabla L(\boldsymbol{\theta}) \approx \frac{1}{B} \sum_{i \in \text{batch}} \nabla \ell_i(\boldsymbol{\theta})
$$

This is **stochastic** — different batches give different gradient estimates — but unbiased on average. The noise is actually helpful: it provides regularization and helps escape saddle points.

### Why mini-batches?

- **Too small (B=1)**: high variance, poor GPU utilization.
- **Too large (B=N)**: low variance, but only one update per epoch and huge memory.
- **Sweet spot (B=32–4096)**: good GPU utilization, reasonable variance, frequent updates.

Modern LLM training uses very large batch sizes (millions of tokens) enabled by gradient accumulation and distributed training.

## SGD with Momentum

Plain SGD oscillates in ravines (high-curvature directions). **Momentum** smooths the trajectory by accumulating an exponentially-decaying moving average of past gradients:

$$
\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \nabla L(\boldsymbol{\theta}_t)
$$

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \mathbf{v}_{t+1}
$$

Typical $\beta = 0.9$. Momentum accelerates in consistent-gradient directions and damps oscillations in flipping-gradient directions.

### Nesterov momentum

A variant that "looks ahead" — computes the gradient at the anticipated next position. Slightly better convergence in theory; minor differences in practice.

## AdaGrad, RMSProp

**AdaGrad** scales each parameter's learning rate by the inverse square root of the sum of squared gradients. Problem: the scaling monotonically decreases, eventually stopping learning.

**RMSProp** fixes this with an exponential moving average instead of a sum:

$$
\mathbf{s}_{t+1} = \beta \mathbf{s}_t + (1 - \beta) (\nabla L)^2
$$

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \frac{\nabla L}{\sqrt{\mathbf{s}_{t+1}} + \epsilon}
$$

RMSProp adapts the per-parameter learning rate based on recent gradient magnitudes.

## Adam

**Adam** (Adaptive Moment Estimation) combines momentum (first moment) and RMSProp (second moment):

$$
\mathbf{m}_{t+1} = \beta_1 \mathbf{m}_t + (1 - \beta_1) \nabla L \quad \text{(first moment)}
$$

$$
\mathbf{v}_{t+1} = \beta_2 \mathbf{v}_t + (1 - \beta_2) (\nabla L)^2 \quad \text{(second moment)}
$$

Bias-corrected (because $\mathbf{m}, \mathbf{v}$ start at zero and are biased toward zero early):

$$
\hat{\mathbf{m}} = \frac{\mathbf{m}_{t+1}}{1 - \beta_1^{t+1}}, \quad \hat{\mathbf{v}} = \frac{\mathbf{v}_{t+1}}{1 - \beta_2^{t+1}}
$$

Update:

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \frac{\hat{\mathbf{m}}}{\sqrt{\hat{\mathbf{v}}} + \epsilon}
$$

Typical hyperparameters: $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$.

### Why Adam dominates

- Per-parameter adaptive learning rates (like RMSProp).
- Momentum (like SGD-momentum).
- Bias correction makes it work well from step 1.
- Robust to hyperparameter choice.
- Works well out-of-the-box for most problems.

### Adam's weakness: weight decay

Naive weight decay in Adam (just adding $\lambda \boldsymbol{\theta}$ to the gradient) interacts badly with the adaptive learning rate. **AdamW** fixes this by decoupling weight decay from the gradient-based update:

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \left( \frac{\hat{\mathbf{m}}}{\sqrt{\hat{\mathbf{v}}} + \epsilon} + \lambda \boldsymbol{\theta}_t \right)
$$

**AdamW is the default optimizer for almost all modern LLM training.**

## Other Optimizers (briefly)

- **LAMB** — layer-wise adaptive learning rates. Used for very large batch training.
- **Lion** — uses the first moment only; simpler and reportedly matches/beats AdamW on some benchmarks. Still being validated.
- **Shampoo** — uses second-order information; expensive but theoretically better.
- **SOAP** — recent (2024) improvement that approximates second-order info efficiently.

## Learning-Rate Schedules

The learning rate is the **single most important hyperparameter**. A good schedule typically:

1. **Warmup**: linearly increase $\eta$ from 0 (or a small value) to a peak over $T_{\text{warmup}}$ steps. Helps with early-training instability (especially for transformers, where early gradients are large and noisy).
2. **Decay**: gradually decrease $\eta$ after the peak. Common decay schedules:
   - **Cosine decay** — $\eta_t = \eta_{\text{peak}} \cdot \frac{1}{2}(1 + \cos(\pi t / T))$. Smooth, widely used.
   - **Linear decay** — $\eta_t = \eta_{\text{peak}} \cdot (1 - t/T)$. Simple, effective.
   - **Step decay** — multiply $\eta$ by 0.1 every $N$ epochs. Older, less common now.
3. **Cooldown** (optional): a short final phase with very low $\eta$ to fine-tune.

```python
# A canonical transformer training schedule
import math
def lr_lambda(step):
    if step < warmup_steps:
        return step / warmup_steps
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    return 0.5 * (1 + math.cos(math.pi * progress))
```

### Rule of thumb: scale LR with batch size

The "linear scaling rule": when you multiply batch size by $k$, multiply the learning rate by $k$ (with warmup). This works well up to a point; for very large batches, more sophisticated rules (LARS, LAMB) are needed.

## Gradient Clipping

To prevent exploding gradients, clip the gradient's L2 norm to a threshold:

$$
\text{if } \|\nabla L\| > c: \quad \nabla L \leftarrow c \cdot \frac{\nabla L}{\|\nabla L\|}
$$

Essential for transformer training. Typical $c = 1.0$.

## Worked Example

Training a tiny model on a toy loss:

```python
import torch
model = torch.nn.Linear(10, 1)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

for step in range(1000):
    x = torch.randn(32, 10)
    y = torch.randn(32, 1)
    loss = ((model(x) - y) ** 2).mean()
    
    opt.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
```

## Why This Matters for AI

- **Optimizer choice** can swing training stability and final quality by 10%+.
- **AdamW + cosine decay + warmup + gradient clipping** is the standard transformer training recipe. Almost every public LLM (Llama, Mistral, Qwen, DeepSeek, Gemma) uses some variant of this.
- **Fine-tuning** often uses higher LR than pretraining (e.g., 1e-5 → 1e-4 for full fine-tuning, 1e-4 → 1e-3 for LoRA). See [[LoRA]].
- **Inference** doesn't need optimizers — but understanding optimization is essential for choosing checkpoints and monitoring training health.

## Common Pitfalls

- **LR too high**: loss diverges (NaN). Reduce LR, increase warmup, check for gradient explosion.
- **LR too low**: loss barely decreases. Increase LR or train longer.
- **Forgetting warmup** for transformers: training will often diverge in the first few hundred steps.
- **Weight decay on biases and norms**: don't apply weight decay to bias terms or LayerNorm parameters — they don't have a regularization interpretation. Most modern frameworks handle this via parameter groups.
- **Forgetting `zero_grad()`**: PyTorch accumulates gradients by default. Always call `opt.zero_grad()` before `backward()`.

## Production Implications

- **Training stability monitoring**: track gradient norm, loss, and LR. A loss spike usually means gradient explosion — clip harder or reduce LR.
- **Checkpoint selection**: save checkpoints periodically and validate. The best checkpoint is rarely the final one.
- **Resume training**: when resuming, restore optimizer state (momentum buffers, Adam moments) in addition to model weights. Forgetting this loses significant training progress.
- **Distributed training**: optimizers must be wrapped (e.g., FSDP, DeepSpeed ZeRO) to shard state across GPUs. Adam's state is ~4x parameter size in fp32 (momentum + variance + fp32 master copy).

## Further Reading

- Kingma & Ba, *Adam: A Method for Stochastic Optimization* (2015).
- Loshchilov & Hutter, *Decoupled Weight Decay Regularization* (AdamW, 2019).
- Goodfellow et al., *Deep Learning* — Chapter 8 (Optimization for Training Deep Models).
- Karpathy's "A Recipe for Training Neural Networks" — practical advice.

## See Also

- [[Gradient and Chain Rule]]
- [[Probability Essentials]] — MLE/MAP connections
- [[Entropy Cross-Entropy KL]] — the loss function being optimized
- [[02 - Mathematics/MOC|Mathematics MOC]]
- [[11 - Training/MOC|Training MOC]] — practical training recipes

## The Convex vs. Non-Convex Landscape

A function is **convex** if its epigraph is a convex set — equivalently, $f(\lambda x + (1-\lambda) y) \leq \lambda f(x) + (1-\lambda) f(y)$ for all $x, y, \lambda \in [0, 1]$. For convex functions, every local minimum is a global minimum, and gradient descent with a small enough LR is guaranteed to converge. **Strong convexity** (the Hessian has minimum eigenvalue $\mu > 0$) gives a convergence rate of $O(1/\mu t)$ for GD and $O(1/\mu^2 t^2)$ for Nesterov accelerated gradient.

Neural network losses are **non-convex** — there are many local minima, saddle points (more common than minima in high dimensions), and flat regions. There's no global convergence guarantee. In practice, this matters less than you'd think: large nets have so many minima that finding a "good enough" one is easy; the real challenges are ill-conditioning (gradient directions don't point toward the minimum) and training instability (loss spikes, divergence).

### Why neural nets train anyway

Despite non-convexity, neural networks train reliably because:
1. **Overparameterization**: large nets have many minima of similar quality, so finding one is easy.
2. **Stochasticity**: SGD noise helps escape saddle points and shallow minima.
3. **Initialization matters more than algorithm**: good initialization (Xavier, He) puts you in a region where gradients are well-behaved.
4. **Architectural choices**: residual connections, normalization, and skip connections smooth the loss landscape.

## Convergence Rates and Condition Number

The **condition number** $\kappa = L / \mu$ (ratio of largest to smallest Hessian eigenvalue) determines optimization difficulty. For GD on a $\mu$-strongly-convex, $L$-smooth function:

$$
\| \theta_t - \theta^* \|^2 \leq \left( 1 - \frac{1}{\kappa} \right)^t \| \theta_0 - \theta^* \|^2
$$

High $\kappa$ (ill-conditioned) means slow convergence — gradients point in the wrong direction. This is why Adam (which approximates the Hessian diagonal via squared gradients) helps: it effectively rescales the problem to reduce $\kappa$. For LLMs, $\kappa$ can be $10^4$–$10^6$ in early layers, which is why naive GD fails catastrophically and adaptive methods are essential.

| Optimizer              | Convergence rate (strongly convex) | Convergence rate (non-convex) | Per-step cost |
|------------------------|------------------------------------|-------------------------------|---------------|
| Gradient descent       | $O(\kappa / t)$                    | $O(1/\sqrt{t})$               | $O(n)$        |
| SGD with momentum      | $O(\sqrt{\kappa} / t)$             | $O(1/\sqrt{t})$               | $O(n)$        |
| Nesterov AG            | $O(\sqrt{\kappa} / t)$ (optimal)   | $O(1/\sqrt{t})$               | $O(n)$        |
| AdaGrad                | $O(1/t)$ (improves with sparse grads) | $O(1/\sqrt{t})$             | $O(n)$        |
| RMSProp                | similar to SGD with momentum       | $O(1/\sqrt{t})$               | $O(n)$        |
| Adam                   | similar to RMSProp + momentum      | $O(1/\sqrt{t})$ (in practice) | $O(n)$        |
| Newton's method        | $O(\log \log 1/\epsilon)$ (quadratic) | — (needs PD Hessian)      | $O(n^3)$      |
| L-BFGS (quasi-Newton)  | superlinear                        | — (rarely used for NN)        | $O(nm)$       |

The $O(1/\sqrt{t})$ rate for non-convex is a theoretical bound; in practice, neural networks often converge much faster because of the factors listed above.

## Why Adam Is Universal Despite Its Theoretical Weakness

Adam has a known theoretical weakness: Reddi et al. (2018, AMSGrad) showed that Adam can fail to converge in some convex settings because of how the bias-corrected second moment $\hat{v}_t$ is updated. The fix (AMSGrad) keeps a running max of $v_t$, but in practice AMSGrad ≈ Adam for neural networks. So why does Adam dominate?

1. **Robustness to hyperparameters**: Adam works across a wide range of $\beta_1, \beta_2, \eta$ with minimal tuning. SGD with momentum requires careful LR schedule tuning per architecture.
2. **Per-parameter adaptation**: parameters with consistently large gradients get smaller effective LR; parameters with small gradients get larger effective LR. This handles the ill-conditioning problem automatically.
3. **Bias correction**: the early-step correction means Adam trains well from step 1, unlike naive momentum.
4. **Inertia**: the deep learning community has converged on Adam. Code, recipes, and intuitions all assume Adam. Switching optimizers means re-tuning everything.

## Distributed Optimization: Synchronous vs. Asynchronous SGD

For multi-GPU training, gradient computation can be parallelized. Two flavors:

**Synchronous SGD**: all workers compute gradients on their mini-batch, then average. Mathematically equivalent to a larger batch size. Simple, deterministic, but bottlenecked by the slowest worker.

**Asynchronous SGD**: workers update parameters independently without waiting. Hogwild! (Recht et al. 2011) showed this works for sparse problems. The cost: "stale gradients" — a worker's gradient is computed for parameters that have since been updated. For dense problems (LLMs), staleness kills convergence; synchronous is preferred. See [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]].

For LLM pretraining at scale (1000+ GPUs), the practical choice is **synchronous with overlap**: compute gradients on the backward pass while simultaneously all-reducing the previous layer's gradients. This hides most of the communication latency.

## Second-Order Methods: Why They Don't Scale

Newton's method uses the Hessian $H$ to take the optimal step: $\theta \leftarrow \theta - H^{-1} \nabla L$. This converges quadratically near a minimum, vs GD's linear convergence. So why don't we use it?

- **Memory**: $H$ is $n \times n$ for $n$ parameters. For a 1B-parameter model, $H$ is $10^9 \times 10^9 = 10^{18}$ entries — ~4 exabytes in fp32. Impossible.
- **Compute**: inverting $H$ is $O(n^3)$. For 1B params, $10^{27}$ FLOPs per step. Impractical.
- **Non-convexity**: Newton's method can converge to saddle points (where $\nabla L = 0$ but $H$ has negative eigenvalues). Needs modification (e.g., trust regions, damping).

**Quasi-Newton methods** (BFGS, L-BFGS) approximate $H^{-1}$ without computing it. L-BFGS stores the last $m$ gradient/parameter differences and uses them to construct a low-rank approximation. Works for small models (traditional ML) but doesn't scale to deep nets — the approximation quality degrades in high dimensions.

**K-FAC, Shampoo, SOAP** are deep-learning-specific approximations that exploit the layer-wise block structure of the Hessian. They show promise (SOAP reportedly 2× faster than AdamW on some tasks) but are still research-stage.

## Optimizer State Memory Budget

The memory cost of optimizers matters for large models:

| Optimizer | State per parameter | For 7B model | For 70B model |
|-----------|---------------------|--------------|---------------|
| SGD       | 0                   | 14 GB (fp16) | 140 GB        |
| Momentum  | 1 (momentum buffer) | 28 GB        | 280 GB        |
| Adam/AdamW | 2 (momentum + variance) | 42 GB   | 420 GB        |
| AdamW + fp32 master | 3 (m + v + master) | 56 GB | 560 GB   |

For 70B AdamW + fp32 master, you need 560 GB just for optimizer state — multiple H100s. This is why memory-efficient optimizers (Adafactor, factored Adam, 8-bit Adam) are popular. They factorize or quantize the second moment to reduce memory.

## Worked Example: Training a Tiny Transformer

```python
import torch
import torch.nn as nn
import math

class TinyTransformerConfig:
    vocab_size = 32000
    d_model = 256
    n_heads = 4
    d_ff = 1024
    n_layers = 4
    max_seq_len = 512
    dropout = 0.1

class TinyTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.embed = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_embed = nn.Embedding(config.max_seq_len, config.d_model)
        layer = nn.TransformerEncoderLayer(
            d_model=config.d_model, nhead=config.n_heads,
            dim_feedforward=config.d_ff, dropout=config.dropout,
            batch_first=True, norm_first=True,  # Pre-norm for stability
            activation=nn.SiLU()  # SwiGLU-like
        )
        self.transformer = nn.TransformerEncoder(layer, config.n_layers)
        self.norm = nn.RMSNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        # Tie embeddings
        self.lm_head.weight = self.embed.weight

    def forward(self, x):
        B, T = x.shape
        pos = torch.arange(T, device=x.device)
        h = self.embed(x) + self.pos_embed(pos)
        h = self.transformer(h)
        h = self.norm(h)
        return self.lm_head(h)

# Training loop with the standard recipe
def train(model, dataloader, total_steps=10000):
    # Standard transformer training recipe
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=3e-4,           # Peak LR for a small model
        betas=(0.9, 0.95), # Beta2 = 0.95 (not 0.999) — better for transformers
        weight_decay=0.1,  # Decoupled weight decay
        eps=1e-8,
    )
    # Exclude biases and norms from weight decay
    decay_params = [p for n, p in model.named_parameters()
                    if p.dim() > 1 and 'embed' not in n]
    nodecay_params = [p for n, p in model.named_parameters()
                      if p.dim() <= 1 or 'embed' in n]
    optimizer = torch.optim.AdamW([
        {'params': decay_params, 'weight_decay': 0.1},
        {'params': nodecay_params, 'weight_decay': 0.0},
    ], lr=3e-4, betas=(0.9, 0.95))

    # Cosine LR schedule with warmup
    warmup_steps = 200
    def lr_lambda(step):
        if step < warmup_steps:
            return step / warmup_steps
        progress = (step - warmup_steps) / (total_steps - warmup_steps)
        return 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * progress))  # Decay to 10%
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    model.train()
    for step, batch in enumerate(dataloader):
        if step >= total_steps: break
        logits = model(batch['input_ids'])
        loss = nn.functional.cross_entropy(
            logits[:, :-1].reshape(-1, logits.size(-1)),
            batch['input_ids'][:, 1:].reshape(-1),
            ignore_index=-100
        )
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

        if step % 100 == 0:
            print(f"step {step} loss {loss.item():.4f} lr {scheduler.get_last_lr()[0]:.6f}")
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Loss is NaN after a few steps | LR too high; or gradient explosion | Reduce LR by 10×; add gradient clipping; check for inf in inputs |
| Loss plateaus quickly | LR too low; or stuck in saddle point | Increase LR; add momentum; try different initialization |
| Loss spikes intermittently | Bad mini-batch (outliers); or LR too high | Reduce LR; filter outliers; use gradient clipping |
| Loss decreases then increases | LR schedule too aggressive; or overfitting | Lower peak LR; add regularization; shorter training |
| Gradient norm is huge | Exploding gradients; or bad init | Gradient clipping; check init scale; check for numerical issues |
| Gradient norm is tiny | Vanishing gradients; or LR too low | Higher LR; check init; remove unnecessary depth; add residual connections |
| Training loss < validation loss (huge gap) | Overfitting | Add dropout, weight decay, data augmentation; use a smaller model |
| Training and validation loss both high | Underfitting | Train longer; bigger model; better data; check for bugs |
| Adam trains slower than SGD | Wrong beta2 (0.999 too slow for short runs) | Use beta2 = 0.95 or 0.99 for short training runs |
| Memory blows up after backward | Optimizer state not freed | Use gradient checkpointing; reduce batch size; use Adafactor |

## Connection to Other Concepts

- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — the gradient that's being followed.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — second-order info and condition number.
- [[02 - Mathematics/Probability/07 - Probability Essentials|Probability Essentials]] — MLE/MAP and the loss function.
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] — the full Adam derivation.
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|Learning Rate Schedules]] — the schedule that controls $\eta_t$.
- [[02 - Mathematics/Statistics/16 - Estimators and Bias|Estimators and Bias]] — MLE/MAP as estimators.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — how gradients are computed.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — starting point matters.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — gradient pathologies.
- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining Objectives]] — what's being optimized.
- [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]] — scaling SGD across GPUs.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — bf16/fp16 interaction with optimizer state.
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]] — training instability.
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — fine-tuning with different LR.
- [[12 - Fine-Tuning/PEFT/02 - QLoRA|QLoRA]] — quantized optimizer state.

## Interview Questions

1. **Q: Why does Adam dominate deep learning despite its theoretical convergence issues?**
   A: Four reasons. (1) **Robustness to hyperparameters** — Adam works across a wide range of $\beta_1, \beta_2, \eta$ with minimal tuning, unlike SGD-momentum which needs careful per-architecture schedules. (2) **Per-parameter adaptation** — Adam automatically rescales gradients per-parameter based on their recent magnitude, which handles ill-conditioned problems (high condition number $\kappa$). (3) **Bias correction** — Adam works well from step 1, unlike naive momentum which is biased toward zero early. (4) **Inertia** — the community has converged on Adam; code, recipes, and intuitions all assume it. The theoretical issues (AMSGrad) mainly affect convex settings that don't arise in deep learning.

2. **Q: When would you use SGD with momentum instead of Adam?**
   A: Three cases. (1) **Generalization matters more than training speed** — SGD-momentum often generalizes slightly better than Adam (smaller train-test gap), which is why it's still used for image classification (ResNet, ViT). (2) **Memory-constrained training** — SGD-momentum needs 1 buffer vs Adam's 2. (3) **Very large batch training** — for batch sizes >32K, SGD with LARS/LAMB often outperforms Adam. For most other cases (LLMs, fine-tuning, RL), Adam/AdamW is the default.

3. **Q: Explain the condition number and why it matters for optimization.**
   A: The condition number $\kappa = L / \mu$ is the ratio of the largest to smallest Hessian eigenvalue. It measures how "elongated" the loss landscape is. High $\kappa$ (ill-conditioned) means the gradient points mostly along the high-curvature direction, which is rarely toward the minimum — so GD zigzags and converges slowly. The convergence rate for GD on a strongly-convex function is $O(\kappa / t)$. This is why Adam (which approximates the Hessian diagonal via squared gradients) helps: it effectively rescales the problem to reduce $\kappa$. For LLMs, $\kappa$ can be $10^4$–$10^6$ in early layers, which is why naive GD fails catastrophically.

4. **Q: Why doesn't Newton's method work for neural networks?**
   A: Three reasons. (1) **Memory** — the Hessian is $n \times n$ for $n$ parameters. For a 1B-parameter model, that's $10^{18}$ entries — ~4 exabytes. Impossible to store. (2) **Compute** — inverting the Hessian is $O(n^3) = 10^{27}$ FLOPs per step for 1B params. Impractical. (3) **Non-convexity** — Newton's method can converge to saddle points (where $\nabla L = 0$ but the Hessian has negative eigenvalues). Quasi-Newton methods (L-BFGS, K-FAC, Shampoo, SOAP) approximate the Hessian to address memory/compute, but they're still research-stage for deep learning.

5. **Q: How do you choose the learning rate for a new model?**
   A: Start with the canonical values: pretraining $\eta = 3 \times 10^{-4}$ for 7B–70B; full fine-tuning $\eta = 10^{-5}$ to $10^{-4}$; LoRA $\eta = 10^{-4}$ to $10^{-3}$ (higher because LoRA params start from zero). Then sweep: run a few short (1K steps) trials at $\eta / 10$, $\eta$, $10 \eta$ and watch for divergence vs slow progress. Pick the highest LR that doesn't diverge in the first 1K steps. Always use warmup (1–5% of total steps) for transformers — without it, training often diverges in the first 1000 steps due to large early gradients and Adam's bias correction not yet kicked in.

6. **Q: What is the difference between decoupled weight decay (AdamW) and L2 regularization (Adam)?**
   A: In Adam, L2 regularization adds $\lambda \theta$ to the gradient before the adaptive update: $g = \nabla L + \lambda \theta$. This interacts badly with Adam's per-parameter adaptive LR — parameters with small gradients get more weight decay (because $\lambda \theta / \sqrt{v}$ is larger when $v$ is small). AdamW decouples weight decay from the gradient: $\theta \leftarrow \theta - \eta (\hat{m} / \sqrt{\hat{v}} + \lambda \theta)$. Now weight decay is multiplied by $\eta$ uniformly, not by the adaptive per-parameter LR. This is the standard for modern LLM training.

## See Also

- [[Gradient and Chain Rule]]
- [[Probability Essentials]] — MLE/MAP connections
- [[Entropy Cross-Entropy KL]] — the loss function being optimized
- [[Adam Derivation]]
- [[Learning Rate Schedules]]
- [[02 - Mathematics/MOC|Mathematics MOC]]
- [[11 - Training/MOC|Training MOC]] — practical training recipes
