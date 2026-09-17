---
tags: [neural-networks, training, gradient-stability]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Vanishing and Exploding Gradients]
---

# 08 - Vanishing and Exploding Gradients

> [!info] TL;DR
> Deep networks multiply many gradient factors during backprop. If each factor is < 1, the product → 0 (vanishing). If > 1, the product → ∞ (exploding). Both prevent learning in deep layers. Solutions: ReLU, residual connections, LayerNorm, gradient clipping, careful init.

## The Mechanism

Backpropagation through a deep network multiplies many Jacobians:

$$
\frac{\partial L}{\partial \mathbf{x}_0} = \frac{\partial L}{\partial \mathbf{x}_N} \prod_{l=1}^{N} \frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}}
$$

Each factor $\frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}}$ is a Jacobian. Its norm depends on:
- The weights of layer $l$.
- The activation function's derivative.
- The architecture (residual? normalization?).

If most factors have norm < 1, the product decays exponentially with depth — gradients reaching early layers are near zero, so those layers don't learn. **Vanishing gradient.**

If most factors have norm > 1, the product grows exponentially — gradients reach early layers as huge values, weights explode, training diverges. **Exploding gradient.**

## Where Each Happens

### Vanishing gradient
- **Sigmoid / tanh**: derivatives are ≤ 0.25 (sigmoid) or ≤ 1 (tanh), and saturate to 0 away from the origin. Multiplying many small derivatives → 0.
- **RNNs**: same weights applied at each timestep, so backprop through time multiplies the same Jacobian $T$ times. After 100 timesteps, even a small per-step factor becomes negligible.
- **Deep plain networks** (no residuals): each layer's contribution to the gradient shrinks geometrically.

### Exploding gradient
- **RNNs**: if the recurrent weight matrix has eigenvalues > 1, gradients explode.
- **Large learning rates**: each step overshoots, weights grow, next step's gradients grow more — positive feedback.
- **Bad init**: weights too large at start.

## Diagnosing

- **Vanishing**: early layers don't change during training (their gradient norms are near zero). Loss decreases slowly or plateaus.
- **Exploding**: loss becomes NaN or spikes wildly. Gradient norms are huge.

To diagnose: log gradient norms per layer per step. A healthy training run has roughly constant gradient norms across layers.

## Solutions

### 1. ReLU family activations

ReLU's derivative is 0 or 1 — no saturation for positive inputs. This largely eliminates vanishing gradients from the activation side. See [[02 - Activation Functions]].

### 2. Residual connections

$$
\mathbf{y} = \mathbf{x} + F(\mathbf{x})
$$

The gradient through the residual highway is 1 (identity). So even if $F$'s gradient is tiny, the total gradient is at least 1 — early layers still receive gradient.

This is the single biggest fix for vanishing gradients in deep networks. ResNet enabled 100+ layer CNNs; Transformers rely on residuals for the same reason. See [[07 - Transformers/Architecture/Residual Connections|Residual Connections]].

### 3. LayerNorm / RMSNorm

Normalizing activations keeps them at a stable scale, preventing the multiplicative blow-up or shrinkage. See [[07 - Transformers/Components/Normalization Layers|Normalization Layers]].

### 4. Proper initialization

Xavier (for tanh) and He (for ReLU) inits are designed to keep activation and gradient variances roughly constant across layers. See [[07 - Initialization Schemes]].

### 5. Gradient clipping

Cap the gradient norm:

$$
\text{if } \|\nabla L\| > c: \nabla L \leftarrow c \cdot \frac{\nabla L}{\|\nabla L\|}
$$

Essential for transformer training. Typical $c = 1.0$. Doesn't fix the underlying cause but prevents training divergence.

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### 6. Gated architectures (LSTM/GRU)

LSTM's cell state provides an additive gradient highway (the forget gate controls flow, but it's a multiplication by ≤ 1, not a tanh derivative). This is why LSTMs could learn longer dependencies than vanilla RNNs. See [[04 - RNN LSTM GRU]].

### 7. Attention (the Transformer solution)

Attention provides direct, non-sequential paths between any two positions. The gradient between distant tokens doesn't have to flow through many intermediate layers — it flows directly through attention. This is part of why Transformers handle long sequences better than RNNs.

## Worked Example: Visualizing Vanishing Gradient

Train a 20-layer plain MLP (no residuals, sigmoid activations) on MNIST. Log the gradient norm at each layer:

| Layer | Gradient norm (epoch 1) |
|-------|--------------------------|
| 20    | 1.0                      |
| 15    | 0.1                      |
| 10    | 0.001                    |
| 5     | 1e-5                     |
| 1     | 1e-8                     |

Layer 1's gradients are 8 orders of magnitude smaller than layer 20's — it's effectively not learning.

Same network with ReLU + residuals + LayerNorm: gradient norms stay within 1 order of magnitude across layers. Healthy training.

## Why This Matters for AI

- Every Transformer architecture choice — residuals, LayerNorm, ReLU/SwiGLU, init scheme — is partly motivated by avoiding vanishing/exploding gradients. Understanding this makes the architecture make sense.
- **Training stability** is the #1 practical challenge in LLM training. Loss spikes, divergence, "the model just stopped learning" — these are gradient issues.
- For **fine-tuning**, vanishing gradients are less of a concern (network is shallower in effect), but gradient clipping is still standard practice.
- For **inference**, gradient issues don't apply directly — but understanding them explains architectural choices.

## Production Implications

- **Always use gradient clipping** for transformer training. Max norm 1.0 is standard.
- **Monitor gradient norms** per layer. Sudden spikes → instability. Steady decline → vanishing.
- **Use a known-good architecture** (Transformer with residuals + RMSNorm + SwiGLU) rather than inventing your own. The vanishing/exploding gradient issues have been engineered out.
- **For RNNs**, use LSTM/GRU, not vanilla RNN. Even better, use a Transformer or SSM.
- **Loss spikes** during training are often gradient explosions. Investigate before continuing.

## Common Pitfalls

- **No gradient clipping** in transformer training → almost guaranteed to diverge.
- **Wrong activation + init combo** (sigmoid + He, ReLU + Xavier) → vanishing gradients.
- **Removing residuals** as an "optimization" → kills deep networks.
- **Ignoring loss spikes** as "training noise" → often a sign of impending divergence.
- **No gradient logging** → can't diagnose issues when they appear.

## Further Reading

- Hochreiter (1991), *Untersuchungen zu dynamischen neuronalen Netzen* (original thesis on vanishing gradients, in German).
- Pascanu et al. (2013), *On the Difficulty of Training Recurrent Neural Networks* (mathematical analysis).
- He et al. (2015), *Delving Deep into Rectifiers* (He init, with analysis of gradient flow).

## Mathematical Analysis (Detailed)

For a deep network with $L$ layers, the gradient of the loss w.r.t. early-layer weights involves a product of Jacobians:

$$
\frac{\partial L}{\partial \mathbf{W}_1} = \frac{\partial L}{\partial \mathbf{x}_L} \prod_{l=2}^{L} \frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}} \cdot \frac{\partial \mathbf{x}_2}{\partial \mathbf{W}_1}
$$

Each Jacobian $\frac{\partial \mathbf{x}_l}{\partial \mathbf{x}_{l-1}}$ has a spectral radius (largest eigenvalue magnitude) $\rho_l$. The product's norm is bounded by $\prod_l \rho_l$.

### Vanishing case
If $\rho_l < 1$ for most layers (typical for sigmoid/tanh in saturation, or bad init), the product $\prod \rho_l \to 0$ exponentially. The gradient at early layers is exponentially small — they don't learn.

### Exploding case
If $\rho_l > 1$ (typical for RNNs with large weights, or bad init), the product $\prod \rho_l \to \infty$ exponentially. The gradient at early layers is exponentially large — training diverges.

### RNNs are especially vulnerable
In RNNs, the **same** weight matrix is applied at every timestep: $\mathbf{h}_t = f(\mathbf{W}\mathbf{h}_{t-1})$. The Jacobian product is $\prod_t \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_{t-1}} = \prod_t \mathbf{W}^T \text{diag}(f')$. The spectral radius of $\mathbf{W}$ determines everything:
- $\rho(\mathbf{W}) < 1$: vanishing — can't learn long-range dependencies.
- $\rho(\mathbf{W}) > 1$: exploding — training diverges.
- $\rho(\mathbf{W}) = 1$: stable — but hard to achieve in practice.

This is why RNNs can't remember dependencies > 20-50 timesteps. LSTMs and GRUs mitigate (gates control the effective Jacobian) but don't fully solve. Transformers (with attention) bypass this entirely — no sequential Jacobian product.

## Solutions (Detailed Comparison)

| Solution | Mechanism | Vanishing? | Exploding? | Cost |
|----------|-----------|------------|------------|------|
| ReLU family | Derivative = 1 in active regime | ✅ Fixes | ❌ | Free |
| Residual connections | Additive skip (gradient flows directly) | ✅ Fixes | Partial | +Memory |
| LayerNorm / BatchNorm | Normalize activations (control scale) | ✅ Helps | ✅ Helps | +Compute |
| He / Xavier init | Control initial spectral radius | ✅ Prevents | ✅ Prevents | Free |
| Gradient clipping | Cap gradient norm | ❌ | ✅ Fixes | Free |
| LSTM / GRU gates | Control information flow | ✅ Mitigates | ❌ | +Complexity |
| Attention (no recurrence) | No sequential Jacobian product | ✅ Bypasses | ✅ Bypasses | +$O(n^2)$ |

### Why ReLU fixes vanishing (but not exploding)
ReLU's derivative is 1 for $x > 0$ and 0 for $x < 0$. The Jacobian product through ReLU is a product of 1s (for active neurons) — no exponential decay. But if too many neurons are inactive ("dead ReLUs"), the gradient is 0 — a different problem. Leaky ReLU (derivative = 0.01 for $x < 0$) avoids dead neurons.

### Why residual connections fix vanishing
The residual connection $\mathbf{y} = \mathbf{x} + F(\mathbf{x})$ has Jacobian $\frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \mathbf{I} + \frac{\partial F}{\partial \mathbf{x}}$. The identity term $\mathbf{I}$ ensures the gradient can flow directly, even if $\frac{\partial F}{\partial \mathbf{x}}$ vanishes. This is why 100+ layer networks are trainable with residuals.

### Why gradient clipping fixes exploding (but not vanishing)
Gradient clipping caps $\|\nabla\|$ at a threshold $c$. This prevents the explosion from causing divergence, but doesn't help with vanishing (you can't clip a 0 gradient to be larger). Standard for Transformers (typical $c = 1.0$).

## Modern Context (Transformers)

Transformers are less susceptible to vanishing/exploding than RNNs, but not immune:

### Vanishing in Transformers
- **Deep Transformers (50+ layers)**: without residual connections, gradients vanish. Residuals are essential.
- **Attention saturation**: if $QK^T / \sqrt{d_k}$ has very large entries, softmax saturates (one entry → 1, others → 0). The gradient through saturated softmax is ~0. This is why we scale by $1/\sqrt{d_k}$.

### Exploding in Transformers
- **Large attention scores**: without scaling, $QK^T$ can have very large entries, causing softmax to output near-one-hot, and gradients to explode. Scaling fixes this.
- **Bad init**: too-large init causes activation explosion. He/Xavier init prevents this.
- **Long sequences**: attention over very long sequences can produce large gradients. Gradient clipping is essential.

### Why Transformers still need gradient clipping
Even with good init and scaling, Transformers can have occasional large gradients from:
- Rare but high-loss training examples.
- Numerical instability in attention (especially with FP16).
- Bad mini-batches (outlier data).

Gradient clipping (norm 1.0) is standard in all Transformer training recipes (GPT, Llama, Mistral).

## Worked Example: Diagnosing Gradient Issues

```python
import torch
import torch.nn as nn

def diagnose_gradients(model, input_batch, target_batch):
    """Diagnose vanishing/exploding gradients."""
    loss = model(input_batch).loss(target_batch)
    loss.backward()

    print("Gradient norms per layer:")
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm().item()
            print(f"  {name}: {grad_norm:.6f}")

    # Check for vanishing (early layers << late layers)
    grad_norms = [param.grad.norm().item() for param in model.parameters()
                  if param.grad is not None and param.dim() > 1]
    if grad_norms:
        ratio = max(grad_norms) / (min(grad_norms) + 1e-10)
        print(f"\nMax/min gradient ratio: {ratio:.2f}")
        if ratio > 1000:
            print("⚠️  Likely vanishing or exploding gradients!")
        elif ratio > 100:
            print("🟡 Gradient imbalance — monitor training.")

# Symptoms:
# - All grad norms ~0: vanishing (check init, activations, residual connections)
# - Some grad norms >> 1: exploding (add gradient clipping)
# - Large ratio between layers: gradient imbalance (add LayerNorm)
```

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Early layers don't learn (grad ~0) | Vanishing gradients | Add residual connections; use ReLU; check init |
| Training diverges (loss → NaN) | Exploding gradients | Add gradient clipping; reduce LR; check init |
| Loss plateaus quickly | Vanishing in deep layers | Add LayerNorm; reduce depth; use residual connections |
| RNN can't learn long dependencies | Vanishing through time | Use LSTM/GRU; use attention; use Transformer |
| Different runs give very different results | Init variance; no seed | Set seed; use He/Xavier init |
| FP16 training NaNs | Gradient overflow in FP16 | Use BF16; add gradient scaling |

## Connection to Other Concepts

- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — the chain rule causes vanishing/exploding.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — spectral radius of Jacobians.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Condition Number]] — high condition number = vanishing/exploding.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — the algorithm where gradients flow.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — He/Xavier init prevents vanishing/exploding.
- [[04 - Neural Networks/Foundations/02 - Activation Functions|Activation Functions]] — ReLU vs. sigmoid affects gradient flow.
- [[07 - Transformers/Architecture/03 - Residual Connections|Residual Connections]] — the main fix for vanishing in deep networks.
- [[07 - Transformers/Components/04 - Normalization Layers|Normalization Layers]] — LayerNorm controls activation scale.
- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] — scaling fixes attention saturation.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — FP16 overflow/underflow.
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]] — gradient clipping prevents spikes.

## Interview Questions

1. **Q: Why do vanishing gradients happen in deep networks?**
   A: Backpropagation multiplies many Jacobians: $\nabla = \prod_l J_l$. If each Jacobian has spectral radius < 1 (typical for sigmoid/tanh in saturation, or bad init), the product $\to 0$ exponentially. The gradient at early layers is exponentially small — they don't learn. The chain rule, which makes deep learning possible, also causes this fundamental problem.

2. **Q: How do residual connections fix vanishing gradients?**
   A: The residual connection $\mathbf{y} = \mathbf{x} + F(\mathbf{x})$ has Jacobian $\frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \mathbf{I} + \frac{\partial F}{\partial \mathbf{x}}$. The identity term $\mathbf{I}$ ensures the gradient can flow directly through the network, even if $\frac{\partial F}{\partial \mathbf{x}}$ vanishes. Without residuals, 50+ layer networks are untrainable; with residuals, 1000+ layer networks work.

3. **Q: Why are RNNs especially vulnerable to vanishing gradients?**
   A: RNNs apply the **same** weight matrix at every timestep: $\mathbf{h}_t = f(\mathbf{W}\mathbf{h}_{t-1})$. The Jacobian product is $\prod_t \mathbf{W}^T \text{diag}(f')$. If $\rho(\mathbf{W}) < 1$ (vanishing) or > 1 (exploding), the product diverges exponentially. This is why RNNs can't remember dependencies > 20-50 timesteps. LSTMs mitigate (gates control the Jacobian) but don't fully solve; Transformers bypass entirely (no sequential product).

4. **Q: Why does self-attention scale by $1/\sqrt{d_k}$?**
   A: Without scaling, $QK^T$ has variance $\propto d_k$. For large $d_k$, softmax saturates (one entry → 1, others → 0). In saturation, softmax's gradient is ~0 — vanishing gradient. Scaling by $1/\sqrt{d_k}$ brings variance back to 1, keeping softmax in its non-saturated regime where gradients flow. This is a gradient-stability fix, not just a numerical stability fix.

5. **Q: How does gradient clipping work, and when should you use it?**
   A: Gradient clipping caps $\|\nabla\|$ at a threshold $c$: $\nabla \leftarrow \nabla \cdot \min(1, c / \|\nabla\|)$. This prevents exploding gradients from causing divergence. Use it always for Transformers (typical $c = 1.0$). It doesn't fix vanishing (you can't clip a 0 gradient to be larger). Norm clipping preserves gradient direction; value clipping (per-element) can distort direction.

6. **Q: Why don't Transformers have vanishing gradients like RNNs?**
   A: Three reasons: (1) attention has no sequential Jacobian product — each position attends directly to all others, no chain of multiplications; (2) residual connections provide a direct gradient path; (3) LayerNorm controls activation scale. But Transformers still need gradient clipping for occasional large gradients (rare high-loss examples, numerical instability, long sequences).

## See Also

- [[06 - Backpropagation]]
- [[07 - Initialization Schemes]]
- [[02 - Activation Functions]]
- [[07 - Transformers/Architecture/Residual Connections|Residual Connections]]
- [[07 - Transformers/Components/Normalization Layers|Normalization Layers]]
- [[04 - Neural Networks/MOC|Neural Networks MOC]]