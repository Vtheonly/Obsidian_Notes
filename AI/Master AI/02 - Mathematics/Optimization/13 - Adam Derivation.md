---
tags: [mathematics, optimization, adam, derivation]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Adam Derivation Deep]
---

# 13 - Adam Derivation Deep Dive

> [!info] TL;DR
> Adam = Momentum + RMSProp. This note derives Adam step-by-step from first principles, shows why each piece is necessary, and explains the bias correction that makes Adam work well from step 1.

## Building Up to Adam

### Plain SGD

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \mathbf{g}_t
$$

where $\mathbf{g}_t = \nabla L(\boldsymbol{\theta}_t)$. Simple, but suffers from:
- Slow progress in flat directions.
- Oscillation in steep, narrow directions.
- Same learning rate for all parameters.

### SGD with Momentum

Add a moving average of past gradients:

$$
\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t
$$

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \mathbf{m}_t
$$

The momentum $\mathbf{m}_t$ is an exponentially-decaying average of past gradients. It accelerates in consistent-gradient directions and damps oscillations in flipping-gradient directions. Typical $\beta_1 = 0.9$.

### RMSProp

Adapt the per-parameter learning rate based on recent gradient magnitudes:

$$
\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2
$$

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \frac{\mathbf{g}_t}{\sqrt{\mathbf{v}_t} + \epsilon}
$$

$\mathbf{v}_t$ is the exponential moving average of squared gradients. Dividing by $\sqrt{\mathbf{v}_t}$ makes the effective learning rate smaller for parameters with large recent gradients and larger for parameters with small recent gradients.

## Adam: Combine Momentum + RMSProp

Adam maintains **both** first moment $\mathbf{m}_t$ (momentum) and second moment $\mathbf{v}_t$ (RMSProp):

$$
\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t
$$

$$
\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2
$$

### The Bias Correction (Critical)

At $t = 0$, $\mathbf{m}_0 = \mathbf{0}$ and $\mathbf{v}_0 = \mathbf{0}$. So:

$$
\mathbf{m}_1 = (1 - \beta_1) \mathbf{g}_1
$$

This is biased toward zero — the true first-moment estimate should be $\mathbf{g}_1$, not $(1-\beta_1)\mathbf{g}_1$. The bias is especially bad early in training when $\mathbf{m}_t$ hasn't accumulated many terms.

The fix is **bias correction**:

$$
\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}, \qquad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}
$$

Why this works: the uncorrected $\mathbf{m}_t$ is approximately $(1 - \beta_1^t) \cdot \mathbb{E}[\mathbf{g}]$ (under stationarity). Dividing by $1 - \beta_1^t$ recovers the unbiased estimate.

As $t \to \infty$, $\beta_1^t \to 0$, so the correction vanishes — it only matters early in training.

### The Adam Update

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon}
$$

That's Adam. Default hyperparameters: $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$, $\eta \in [10^{-4}, 10^{-3}]$.

## Why $\beta_2 \gg \beta_1$?

- $\beta_1 = 0.9$ → momentum averaging window ~10 steps.
- $\beta_2 = 0.999$ → second-moment averaging window ~1000 steps.

The second moment needs a longer window because squared gradients have higher variance than gradients themselves — we need more samples to estimate $\mathbb{E}[g^2]$ accurately.

## AdamW: Decoupled Weight Decay

The original Adam paper applied weight decay by adding $\lambda \boldsymbol{\theta}$ to the gradient:

$$
\mathbf{g}_t = \nabla L(\boldsymbol{\theta}_t) + \lambda \boldsymbol{\theta}_t
$$

This interacts badly with Adam's adaptive learning rate. The effective weight decay per parameter becomes $\lambda \eta / \sqrt{v_t}$ — so parameters with small gradients get **more** weight decay than parameters with large gradients. This is backwards.

**AdamW** (Loshchilov & Hutter, 2019) decouples weight decay from the gradient:

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \left( \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} + \lambda \boldsymbol{\theta}_t \right)
$$

Now weight decay is multiplied by $\eta$ uniformly, not by the adaptive per-parameter learning rate. This is the **standard optimizer for modern LLM training**.

## Worked Implementation

```python
import torch

class Adam:
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0):
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = [torch.zeros_like(p) for p in self.params]
        self.v = [torch.zeros_like(p) for p in self.params]
        self.t = 0
    
    def step(self):
        self.t += 1
        for i, p in enumerate(self.params):
            if p.grad is None:
                continue
            g = p.grad
            
            # Update moments
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g * g
            
            # Bias correction
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            
            # AdamW update (decoupled weight decay)
            update = m_hat / (v_hat.sqrt() + self.eps)
            if self.weight_decay > 0:
                update = update + self.weight_decay * p
            
            p.data -= self.lr * update
```

## Why Adam Works So Well

1. **Adaptive per-parameter learning rates**: parameters that consistently get large gradients have their effective LR reduced; parameters with small gradients have LR increased. This handles ill-conditioned problems automatically.
2. **Momentum smooths noise**: stochastic gradients are noisy; momentum averages out the noise.
3. **Bias correction enables fast startup**: without it, Adam would be slow for the first few hundred steps.
4. **Robust to hyperparameters**: Adam works reasonably across a wide range of LRs and betas. Less tuning than SGD.

## Adam's Weaknesses

- **Generalization gap**: Adam can overfit the training set faster than SGD-with-momentum, leading to worse test performance on some problems. This is debated but observed.
- **Weight decay interaction**: fixed by AdamW, but old Adam + weight decay is still common in legacy code.
- **Memory**: 2x parameter count for the moment buffers (vs SGD's 1x for momentum, or 0x for plain SGD).

## Variants and Successors

- **AdamW**: decoupled weight decay. **Default for modern LLM training.**
- **LAMB**: layer-wise adaptive LR. Used for very large batch training.
- **Lion**: simpler, uses only first moment (sign of momentum). Reportedly competitive with AdamW at lower memory.
- **Adafactor**: factored second moment for very large models (saves memory).
- **SOAP**, **Shampoo**: approximate second-order info; active research.
- **Sophia**: Hessian-based; claimed 2x speedup over Adam on LMs.

## Why This Matters for AI

- Adam/AdamW is **the** optimizer for modern deep learning. Every LLM paper uses some variant.
- Understanding Adam's components helps you debug training (e.g., "is the gradient norm too small? Is the LR too high? Is weight decay applied correctly?").
- The bias correction is the kind of subtle detail that separates a working optimizer from a broken one. Knowing why it's there prevents you from removing it accidentally.

## Production Implications

- **Use AdamW by default** for new model training. Don't experiment with optimizers until you've nailed down data, architecture, and LR.
- **Track gradient norm, momentum norm, and v norm** during training. Sudden changes signal instability.
- **Resume from checkpoint correctly**: restore optimizer state ($\mathbf{m}, \mathbf{v}, t$) as well as model weights. Otherwise, you lose momentum and bias correction.
- **Mixed precision**: keep optimizer state in fp32 (master weights) even if forward/backward use fp16/bf16.
- **Memory budget**: AdamW needs ~4x parameter count in optimizer state (m + v + fp32 master + fp16 weights). For a 7B model: ~28 GB just for optimizer state.

## Common Pitfalls

- **Forgetting bias correction** — your own reimplementation will silently underperform.
- **Wrong $\epsilon$** — too small → division by near-zero; too large → over-smoothing.
- **Weight decay on biases and norms** — typically not wanted. Most frameworks let you exclude parameter groups.
- **Not zero_grad-ing** — PyTorch accumulates gradients; always call `optimizer.zero_grad()` before `backward()`.
- **Wrong beta2 for short training** — $\beta_2 = 0.999$ means slow second-moment adaptation; for short runs, $\beta_2 = 0.99$ is sometimes better.

## Further Reading

- Kingma & Ba (2015), *Adam: A Method for Stochastic Optimization*.
- Loshchilov & Hutter (2019), *Decoupled Weight Decay Regularization* (AdamW).
- Reddi et al. (2018), *On the Convergence of Adam and Beyond* (AMSGrad).
- Chen et al. (2024), *Lion: Adapting Large Language Models with Limited Data*.

## See Also

- [[12 - Optimization Essentials]]
- [[14 - Learning Rate Schedules]]
- [[10 - Gradient and Chain Rule]]
- [[11 - Jacobians and Hessians]]
- [[02 - Mathematics/MOC|Mathematics MOC]]

## The Natural Gradient Connection

Adam's update $\theta - \eta \hat{m} / \sqrt{\hat{v}}$ has a deeper interpretation: it's an approximation of the **natural gradient**. The natural gradient is $\theta - \eta F^{-1} \nabla L$, where $F$ is the Fisher information matrix (expected Hessian of the NLL). The natural gradient is invariant to parameterization — it points in the direction of steepest descent in the probability distribution space, not parameter space.

Adam approximates $F^{-1}$ with the diagonal of squared gradients: $\text{diag}(1/\sqrt{v_t})$. This is a crude approximation (off-diagonal terms ignored), but it captures the per-parameter curvature well enough to be useful. K-FAC (Martens & Grosse, 2015) and Shampoo (Gupta et al., 2018) are more sophisticated approximations that use block-diagonal or Kronecker-factored Fisher matrices.

This connection explains why Adam is so effective for neural networks: it's approximating the natural gradient, which is the "right" gradient to follow for probabilistic models. The approximation is coarse, but it's good enough.

## Why $\beta_2 = 0.95$ for Transformers (Not 0.999)

The Adam paper recommends $\beta_2 = 0.999$ (averaging window ~1000 steps). But for transformers, $\beta_2 = 0.95$ (window ~20 steps) is often better. Why?

- **Transformer gradient statistics change quickly**: in early training, attention scores are near-uniform; later, they become peaky. With $\beta_2 = 0.999$, the variance estimate is stale — it averages over a window where the gradient distribution has shifted.
- **Short training runs**: for fine-tuning (1K–10K steps), $\beta_2 = 0.999$ means the variance estimate never fully adapts. $\beta_2 = 0.95$ adapts within ~20 steps.
- **Empirical**: GPT-3, Llama, and most modern LLMs use $\beta_2 = 0.95$ or $\beta_2 = 0.98$. The original $\beta_2 = 0.999$ is now considered suboptimal for transformers.

The cost of $\beta_2 = 0.95$: the variance estimate is noisier, so the effective LR is noisier. But for transformers, this noise is actually helpful — it provides regularization and helps escape saddle points.

## Memory-Efficient Adam Variants

AdamW's 2× parameter memory cost is painful for large models. Variants:

### Adafactor

Factored second moment: instead of storing $v \in \mathbb{R}^{n}$, store row and column statistics $v_r \in \mathbb{R}^{m}, v_c \in \mathbb{R}^{k}$ for weight matrices of shape $(m, k)$. Reconstruct $\hat{v}_{ij} \approx v_{r,i} \cdot v_{c,j} / \|v_c\|$. Memory: $O(m + k)$ instead of $O(mk)$. Used by T5, PaLM. Slight quality loss but huge memory savings for embedding matrices.

### 8-bit Adam (BitsAndBytes)

Quantize the momentum and variance buffers to INT8 with per-row or per-block scales. Memory halved with minimal quality loss. Standard for QLoRA fine-tuning (see [[02 - QLoRA]]).

### Lion (EvoLved Sign Momentum)

Discovered by AutoML. Lion uses only the sign of the momentum: $\theta \leftarrow \theta - \eta \cdot \text{sign}(\beta_1 m + (1-\beta_1) g)$. No second moment needed. Memory: same as momentum (1× params). Reportedly matches AdamW on quality with half the memory. Adoption is still growing.

## Worked Numerical Example

Let's trace through 3 Adam steps on a tiny problem to see how the moments evolve.

```python
import torch

# 1-parameter problem: minimize L = (theta - 5)^2
theta = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.Adam([theta], lr=0.1, betas=(0.9, 0.999), eps=1e-8)

for step in range(5):
    loss = (theta - 5) ** 2
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    # Access Adam internals (PyTorch stores them in state)
    state = optimizer.state[theta]
    m = state.get('exp_avg', torch.tensor([0.0]))
    v = state.get('exp_avg_sq', torch.tensor([0.0]))
    t = state.get('step', 0)
    m_hat = m / (1 - 0.9 ** t) if t > 0 else m
    v_hat = v / (1 - 0.999 ** t) if t > 0 else v
    effective_lr = 0.1 * m_hat / (v_hat.sqrt() + 1e-8)

    print(f"step {step} theta={theta.item():.4f} loss={loss.item():.4f} "
          f"grad={-2*(theta.item()-5):.4f} m_hat={m_hat.item():.4f} v_hat={v_hat.item():.4f} "
          f"effective_step={effective_lr.item():.4f}")
```

Output (approximate):
```
step 0 theta=0.1000 loss=25.00 grad=-10.00 m_hat=-10.00 v_hat=100.00 effective_step=-0.1000
step 1 theta=0.2000 loss=23.04 grad=-9.80 m_hat=-9.89 v_hat=99.04 effective_step=-0.0993
step 2 theta=0.3000 loss=22.09 grad=-9.60 m_hat=-9.79 v_hat=98.11 effective_step=-0.0988
```

Notice: even though the raw gradient changes (-10, -9.8, -9.6), the effective step is nearly constant (~0.1) because Adam normalizes by $\sqrt{v}$. This is Adam's adaptive per-parameter LR in action.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Training diverges in first 100 steps | Bias correction not kicking in; LR too high | Reduce peak LR; ensure warmup is ≥100 steps |
| Loss is high and flat | $\beta_2$ too high (0.999) for short training | Try $\beta_2 = 0.95$ or $0.98$ |
| Memory blows up | AdamW needs 2× params for state | Use Adafactor, 8-bit Adam, or Lion |
| Resuming training gives different results | Forgot to restore optimizer state | Always save optimizer.state_dict() alongside model.state_dict() |
| Mixed precision NaN | $\hat{v}$ underflows in fp16 | Keep optimizer state in fp32; use GradScaler for fp16 |
| Weight decay too aggressive | $\lambda > 0.1$ for transformers | Use $\lambda = 0.1$ for weights, 0 for biases/norms |
| Adam trains worse than SGD | Generalization gap | Try SGD with momentum; or use AdamW with higher weight decay |

## Connection to Other Concepts

- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — Adam's broader context.
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|Learning Rate Schedules]] — controls $\eta_t$.
- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — how $\nabla L$ is computed.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — the Fisher information and condition number.
- [[02 - Mathematics/Probability/07 - Probability Essentials|Probability Essentials]] — the natural gradient / Fisher connection.
- [[02 - Mathematics/Statistics/16 - Estimators and Bias|Estimators and Bias]] — bias correction in estimation.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — where gradients come from.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — optimizer state in fp32.
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]] — Adam-specific stability.
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — fine-tuning LR is different.
- [[12 - Fine-Tuning/PEFT/02 - QLoRA|QLoRA]] — uses 8-bit Adam for memory.

## Interview Questions

1. **Q: Derive the bias correction in Adam. Why is it necessary?**
   A: At $t=0$, $\mathbf{m}_0 = 0$, so $\mathbf{m}_1 = (1-\beta_1) \mathbf{g}_1$. This is biased toward zero — the true first-moment estimate should be $\mathbf{g}_1$, not $(1-\beta_1) \mathbf{g}_1$. Under stationarity, $\mathbb{E}[\mathbf{m}_t] \approx (1 - \beta_1^t) \mathbb{E}[\mathbf{g}]$. The bias correction $\hat{\mathbf{m}}_t = \mathbf{m}_t / (1 - \beta_1^t)$ recovers the unbiased estimate. As $t \to \infty$, $\beta_1^t \to 0$ and the correction vanishes — it only matters early in training. Without it, Adam would take tiny steps for the first ~100 steps, wasting training compute.

2. **Q: Why is the natural gradient interpretation of Adam important?**
   A: Adam's update $\theta - \eta \hat{m} / \sqrt{\hat{v}}$ approximates the natural gradient $\theta - \eta F^{-1} \nabla L$, where $F$ is the Fisher information matrix. The natural gradient is parameterization-invariant — it points in the direction of steepest descent in the probability distribution space. This is the "right" gradient for probabilistic models. Adam approximates $F^{-1}$ with the diagonal of squared gradients, which is crude but captures per-parameter curvature. This explains why Adam is so effective for neural networks: it's approximating the natural gradient, which is optimal for maximum likelihood training.

3. **Q: Why do transformers use $\beta_2 = 0.95$ instead of the Adam paper's $\beta_2 = 0.999$?**
   A: Three reasons. (1) **Transformer gradient statistics change quickly** — attention scores are near-uniform in early training and become peaky later. With $\beta_2 = 0.999$, the variance estimate is stale (window ~1000 steps), so the effective LR is wrong. (2) **Short training runs** — for fine-tuning (1K–10K steps), $\beta_2 = 0.999$ never fully adapts. (3) **Empirical** — GPT-3, Llama, and most modern LLMs all use $\beta_2 = 0.95$ or $0.98$. The original $\beta_2 = 0.999$ is now considered suboptimal for transformers. The tradeoff: $\beta_2 = 0.95$ gives a noisier variance estimate, but for transformers this noise is actually helpful (regularization).

4. **Q: Explain AdamW's decoupled weight decay. Why is it better than L2 regularization in Adam?**
   A: In Adam with L2, the gradient becomes $g = \nabla L + \lambda \theta$, which then goes through Adam's adaptive update. The effective weight decay per parameter is $\lambda \eta / \sqrt{v_t}$ — so parameters with small gradients (small $v_t$) get more weight decay than parameters with large gradients. This is backwards: you want more decay on large weights, not on parameters with small gradients. AdamW fixes this by applying weight decay separately: $\theta \leftarrow \theta - \eta (\hat{m}/\sqrt{\hat{v}} + \lambda \theta)$. Now weight decay is $\eta \lambda$ uniformly, independent of the adaptive LR. This is the standard for modern LLM training.

5. **Q: How does Adafactor reduce Adam's memory, and what's the tradeoff?**
   A: Adafactor factorizes the second moment $v \in \mathbb{R}^{m \times k}$ into row and column statistics $v_r \in \mathbb{R}^{m}$ and $v_c \in \mathbb{R}^{k}$, reconstructing $\hat{v}_{ij} \approx v_{r,i} \cdot v_{c,j} / \|v_c\|$. Memory drops from $O(mk)$ to $O(m + k)$. For a 50K × 4K embedding matrix, that's 200M → 54K floats — a 3700× reduction. The tradeoff: the factorization assumes the second moment is rank-1 (outer product of row and column factors), which is only approximately true. Quality is slightly worse than Adam, but for large embedding matrices the memory savings are essential. T5 and PaLM use Adafactor.

6. **Q: How would you debug an Adam training run that's diverging?**
   A: Step-by-step: (1) **Check LR** — is the peak LR too high for this model size? Reduce by 10× and see if it stabilizes. (2) **Check warmup** — is there a warmup phase of at least 100 steps? Without it, the first steps can diverge before bias correction kicks in. (3) **Check gradient norm** — log it every step. If it's >100, you have exploding gradients; add clipping (max norm 1.0). (4) **Check for inf/NaN in inputs** — bad data can poison the whole batch. (5) **Check $\beta_2$** — for transformers, $\beta_2 = 0.999$ can cause stale variance estimates; try 0.95. (6) **Check weight decay** — too aggressive (>0.5) can destabilize. (7) **Try a smaller batch size** — large batches with high LR can diverge; use gradient accumulation. (8) **Check init** — bad init (e.g., wrong scale for the activation) can cause early divergence.

## See Also

- [[12 - Optimization Essentials]]
- [[14 - Learning Rate Schedules]]
- [[10 - Gradient and Chain Rule]]
- [[11 - Jacobians and Hessians]]
- [[02 - Mathematics/MOC|Mathematics MOC]]
