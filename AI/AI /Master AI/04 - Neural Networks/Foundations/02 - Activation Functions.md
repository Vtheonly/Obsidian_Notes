---
tags: [neural-networks, activations, relu, gelu, swiglu]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Activation Functions]
---

# Activation Functions

> [!info] TL;DR
> Activation functions introduce nonlinearity into neural networks. Without them, deep networks collapse to linear models. This note covers the major activations: sigmoid, tanh, ReLU, GELU, and the gated variants SwiGLU and GEGLU that dominate modern Transformers.

## Why Nonlinearity?

A linear composition of linear functions is still linear:

$$
\mathbf{W}_2 (\mathbf{W}_1 \mathbf{x}) = (\mathbf{W}_2 \mathbf{W}_1) \mathbf{x} = \mathbf{W} \mathbf{x}
$$

So no matter how deep a stack of linear layers is, it's equivalent to a single linear layer. **Nonlinear activations break this collapse** and give neural networks their expressive power. See [[Perceptrons and MLPs]].

## Classical Activations

### Sigmoid

$$
\sigma(x) = \frac{1}{1 + e^{-x}} \in (0, 1)
$$

- **Use**: historically popular; now mostly used as a final layer for binary classification (output a probability).
- **Problems**: saturates (gradients vanish for large |x|), not zero-centered, prone to "dead" neurons.
- Rarely used in hidden layers today.

### Tanh

$$
\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} \in (-1, 1)
$$

- **Use**: historically popular in RNNs (LSTM, GRU).
- **Problems**: still saturates, but zero-centered.
- Largely replaced by ReLU family in modern architectures.

## The ReLU Family

### ReLU (Rectified Linear Unit)

$$
\text{ReLU}(x) = \max(0, x)
$$

- **Cheap** to compute (no exp).
- **Non-saturating** for positive inputs (no vanishing gradient).
- **Sparse** activations (negative inputs produce 0).
- Introduced to deep learning by Nair & Hinton (2010); popularized by AlexNet (2012).

**Problem: "dead ReLU"** — a neuron that always outputs 0 will have gradient 0 forever and never recover. Variants address this:

### Leaky ReLU, PReLU

$$
\text{LeakyReLU}(x) = \begin{cases} x & x \geq 0 \\ \alpha x & x < 0 \end{cases}
$$

with small $\alpha$ (e.g., 0.01). PReLU learns $\alpha$ as a parameter. Avoids dead units but adds a hyperparameter.

### GELU (Gaussian Error Linear Unit)

$$
\text{GELU}(x) = x \cdot \Phi(x)
$$

where $\Phi$ is the standard normal CDF. Approximation:

$$
\text{GELU}(x) \approx 0.5 x \left[ 1 + \tanh\left(\sqrt{2/\pi} (x + 0.044715 x^3)\right) \right]
$$

- Smooth (differentiable everywhere).
- Stochastically motivated: multiplies input by a probability derived from its own value.
- **Standard in BERT, GPT-2/3, most Transformer variants.**

## Gated Linear Units (GLU) and Variants

**GLU** (Dauphin et al., 2017) introduces a multiplicative gate:

$$
\text{GLU}(\mathbf{x}) = (\mathbf{W}\mathbf{x} + \mathbf{b}) \otimes \sigma(\mathbf{V}\mathbf{x} + \mathbf{c})
$$

where $\sigma$ is a sigmoid and $\otimes$ is element-wise. The first linear transformation is "gated" by the second.

### SwiGLU

**SwiGLU** (Shazeer, 2020) replaces the sigmoid with Swish (= SiLU = $x \cdot \sigma(x)$):

$$
\text{SwiGLU}(\mathbf{x}) = \text{Swish}(\mathbf{W}\mathbf{x}) \otimes (\mathbf{V}\mathbf{x})
$$

- Used in **Llama, Mistral, PaLM, Gemma, Qwen, and most modern LLMs**.
- Empirically outperforms GELU in large-scale Transformer training.
- **Cost**: requires an extra linear layer (3 weight matrices instead of 2). To keep parameter count comparable, the hidden dimension is reduced by a factor of 2/3.

### GEGLU

Same idea but with GELU as the gate:

$$
\text{GEGLU}(\mathbf{x}) = \text{GELU}(\mathbf{W}\mathbf{x}) \otimes (\mathbf{V}\mathbf{x})
$$

Used in some models; comparable performance to SwiGLU.

## Worked Example

```python
import torch
import torch.nn.functional as F

x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])

F.relu(x)       # tensor([0., 0., 0., 1., 2.])
F.gelu(x)       # tensor([-0.0454, -0.1588, 0.0000, 0.8412, 1.9546])
F.silu(x)       # tensor([-0.2384, -0.2689, 0.0000, 0.7311, 1.7616]) — Swish

# SwiGLU as a feed-forward layer
class SwiGLUFFN(nn.Module):
    def __init__(self, dim, hidden_dim):
        super().__init__()
        self.w_gate = nn.Linear(dim, hidden_dim)
        self.w_up   = nn.Linear(dim, hidden_dim)
        self.w_down = nn.Linear(hidden_dim, dim)
    def forward(self, x):
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))
```

## Choosing an Activation

| Layer type            | Default choice                | Notes                                            |
|-----------------------|-------------------------------|--------------------------------------------------|
| Hidden layer (CNN/MLP)| ReLU or GELU                  | ReLU if you need speed; GELU for smoother grads. |
| Transformer FFN       | SwiGLU or GELU                | SwiGLU is the modern default for LLMs.           |
| Output (classification)| Softmax (multiclass) / Sigmoid (multilabel) | Always paired with cross-entropy.     |
| Output (regression)   | Linear (no activation)        |                                                  |
| RNN/LSTM gates        | Sigmoid / tanh                | Tradition; gating requires (0, 1) range.         |

## Why This Matters for AI

- The choice of activation function in the FFN is a **visible architectural choice** that distinguishes model generations. GPT-2 used GELU; Llama uses SwiGLU.
- Activations interact with initialization, normalization, and learning rate. A bad combination leads to training instability.
- **Quantization** can change the effective activation. INT8 quantization of GELU requires careful implementation; SwiGLU's element-wise multiply can amplify quantization noise.

## Common Pitfalls

- **Using sigmoid in hidden layers** — causes vanishing gradients in deep networks.
- **Forgetting that softmax is for outputs** — softmax in hidden layers saturates and kills gradients.
- **Mixing activations carelessly** — different activations have different scales; mixing can destabilize training.
- **Not scaling hidden dimension for GLU variants** — SwiGLU has 3 weight matrices, so the standard 4x expansion becomes 8/3 x to keep parameter count comparable.

## Production Implications

- SwiGLU and GELU require **fused kernels** for performance. PyTorch's eager mode is slow; use `torch.compile` or library-provided fused ops.
- For **inference at low precision** (INT8/INT4), activation functions need lookup tables or polynomial approximations. Most serving frameworks (vLLM, TensorRT-LLM) handle this; custom implementations may not.
- **Activation checkpointing** trades compute for memory by recomputing activations during the backward pass. Independent of activation function choice.

## Further Reading

- Nair & Hinton (2010), *Rectified Linear Units Improve Restricted Boltzmann Machines*.
- Hendrycks & Gimpel (2016), *Gaussian Error Linear Units (GELUs)*.
- Shazeer (2020), *GLU Variants Improve Transformer*.
- Ramachandran et al. (2017), *Searching for Activation Functions* (Swish).

## See Also

- [[Perceptrons and MLPs]]
- [[Backpropagation]]
- [[Transformer Block]]
- [[Normalization Layers]]
- [[04 - Neural Networks/MOC|Neural Networks MOC]]

## Mathematical Properties of Activations

### Continuity and differentiability

Backpropagation requires the activation to be differentiable (or sub-differentiable) almost everywhere. Properties:

- **ReLU**: continuous everywhere, differentiable except at $x = 0$ (where the derivative is undefined). Sub-gradient at $x = 0$ is conventionally taken as 0. This works in practice — the probability of hitting exactly $x = 0$ is measure zero for continuous inputs.
- **GELU**: smooth (infinitely differentiable), which gives smoother gradients than ReLU. This is part of why GELU trains slightly better in some settings.
- **Swish/SiLU**: smooth, with a small negative region for $x < 0$ (unlike ReLU which is exactly 0). This allows the network to learn "mostly linear with occasional negative" patterns.
- **Sigmoid/tanh**: smooth but saturating — gradients vanish for large $|x|$.

### Boundedness

- **Sigmoid**: bounded in $(0, 1)$. Outputs are interpretable as probabilities.
- **Tanh**: bounded in $(-1, 1)$. Zero-centered, which helps optimization.
- **ReLU/GELU/SwiGLU**: unbounded above. Allows the network to produce large activations when needed.
- **Softmax**: bounded (each output in $(0, 1)$, sums to 1). Used for output, not hidden layers.

Bounded activations prevent activation explosion but can cause vanishing gradients. Modern LLMs use unbounded activations (ReLU, GELU, SwiGLU) and rely on normalization (LayerNorm/RMSNorm) to keep activations in check.

### Sparsity

- **ReLU**: produces exact zeros for $x < 0$, creating sparse activations. This is computationally beneficial (sparse matrix ops) and may have regularization effects.
- **GELU**: produces near-zero but not exact zero for $x < 0$. Less sparse than ReLU.
- **SwiGLU**: the gating mechanism produces sparse-like behavior (gate near 0 suppresses the output) but without exact zeros.

## The GELU Probabilistic Interpretation

GELU is $x \cdot \Phi(x)$ where $\Phi$ is the standard normal CDF. This has a clean probabilistic interpretation: GELU multiplies the input by the probability that a Gaussian random variable is less than the input. Equivalently, GELU is the expected value of $x \cdot \mathbb{1}[X \leq x]$ where $X \sim \mathcal{N}(0, 1)$.

This is a smoother version of ReLU's "pass through if positive, zero if negative" — GELU passes through with probability $\Phi(x)$, which is smooth around $x = 0$. For large positive $x$, $\Phi(x) \to 1$ (full pass-through). For large negative $x$, $\Phi(x) \to 0$ (full suppression). Near $x = 0$, there's a smooth transition.

The probabilistic motivation comes from **dropout** thinking: ReLU deterministically masks, while GELU stochastic-masks with a probability depending on the input value. This connects to the Bayesian interpretation of dropout as approximate variational inference.

## Worked Example: Comparing Activations

```python
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

x = torch.linspace(-5, 5, 200)

# Activation values
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(x, F.relu(x), label='ReLU')
plt.plot(x, F.gelu(x), label='GELU')
plt.plot(x, F.silu(x), label='Swish/SiLU')
plt.plot(x, torch.tanh(x), label='tanh')
plt.plot(x, torch.sigmoid(x), label='sigmoid')
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
plt.legend(); plt.title('Activation functions')

# Derivatives
plt.subplot(1, 3, 2)
plt.plot(x[1:], torch.diff(F.relu(x)) / (x[1] - x[0]).item(), label='ReLU')
plt.plot(x[1:], torch.diff(F.gelu(x)) / (x[1] - x[0]).item(), label='GELU')
plt.plot(x[1:], torch.diff(F.silu(x)) / (x[1] - x[0]).item(), label='Swish')
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.legend(); plt.title('Derivatives')

# Sparsity: fraction of near-zero outputs for Gaussian inputs
gaussian_input = torch.randn(10000)
plt.subplot(1, 3, 3)
activations = {
    'ReLU': F.relu(gaussian_input),
    'GELU': F.gelu(gaussian_input),
    'Swish': F.silu(gaussian_input),
}
sparsity = {name: (act.abs() < 0.01).float().mean().item() for name, act in activations.items()}
plt.bar(sparsity.keys(), sparsity.values())
plt.ylabel('Fraction near zero')
plt.title('Sparsity (Gaussian input)')
```

## Modern Activations in Production LLMs

| Model            | FFN Activation | Notes                                          |
|------------------|----------------|------------------------------------------------|
| GPT-2/3          | GELU           | Original Transformer default                   |
| BERT             | GELU           | Same                                           |
| Llama 1/2/3      | SwiGLU         | $\text{Swish}(xW_1) \otimes (xW_2)$, 3 matrices |
| Mistral 7B       | SwiGLU         | Same as Llama                                  |
| Qwen 2/2.5       | SwiGLU         | Same                                           |
| Gemma            | GELU           | Uses approximate GELU for speed                |
| DeepSeek-V3      | SwiGLU         | Same                                           |
| T5               | GELU           | Original                                       |
| Claude (inferred)| GELU or SwiGLU | Not publicly disclosed                         |

The shift from GELU (GPT-2/3 era) to SwiGLU (Llama era) reflects the empirical finding that gated activations train better at scale. The cost (extra weight matrix) is offset by reducing the hidden dimension by 2/3.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Dead ReLUs (neurons always output 0) | Bad init; or LR too high | Lower LR; use He init; switch to LeakyReLU or GELU |
| Activations explode (NaN) | No normalization; unbounded activation | Add LayerNorm; use bounded activation; gradient clipping |
| Activations vanish (all near 0) | Sigmoid/tanh saturation; deep net | Use ReLU/GELU; add residual connections; proper init |
| SwiGLU dimension mismatch | Forgot to scale hidden dim by 2/3 | Use `hidden_dim = (2/3) * 4 * d_model` |
| INT8 quantization breaks SwiGLU | Element-wise multiply amplifies noise | Use per-channel quantization; or keep activation in fp16 |
| Model is too sparse (low activation density) | Too much ReLU; or high sparsity init | Switch to GELU/SwiGLU; check init scale |

## Connection to Other Concepts

- [[04 - Neural Networks/Foundations/01 - Perceptrons and MLPs|Perceptrons and MLPs]] — why nonlinearity is needed.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — gradients flow through activations.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — He init is paired with ReLU.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — activation choice affects this.
- [[07 - Transformers/Architecture/01 - Transformer Block|Transformer Block]] — where SwiGLU lives.
- [[07 - Transformers/Components/05 - Feed-Forward Network Deep|Feed-Forward Network Deep]] — the FFN that uses these activations.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — INT8/INT4 interaction with activations.
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] — studying activation patterns.
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017|Vaswani 2017]] — original Transformer used ReLU.

## Interview Questions

1. **Q: Why does SwiGLU outperform GELU in modern LLMs?**
   A: Three reasons. (1) **Gating mechanism** — the element-wise multiply with a sigmoid/Swish gate lets the model selectively suppress information, which is more expressive than a simple nonlinearity. (2) **Empirical at scale** — Shazeer (2020) showed SwiGLU beats GELU on large-scale Transformer training. The advantage grows with model size. (3) **Compatibility with normalization** — SwiGLU works well with RMSNorm (used in Llama), while GELU was paired with LayerNorm. The cost: SwiGLU uses 3 weight matrices instead of 2, so the hidden dim is reduced by 2/3 to keep parameter count comparable.

2. **Q: What is the GELU probabilistic interpretation?**
   A: GELU is $x \cdot \Phi(x)$ where $\Phi$ is the standard normal CDF. This multiplies the input by the probability that a Gaussian random variable is less than the input. Equivalently, GELU is the expected value of $x \cdot \mathbb{1}[X \leq x]$ where $X \sim \mathcal{N}(0, 1)$. This is a smoother version of ReLU's "pass through if positive, zero if negative" — GELU passes through with probability $\Phi(x)$, which is smooth around $x = 0$. The probabilistic motivation comes from dropout thinking: ReLU deterministically masks, while GELU stochastic-masks with a probability depending on the input value.

3. **Q: Why don't we use sigmoid in hidden layers anymore?**
   A: Three problems. (1) **Saturation** — for large $|x|$, the gradient is near zero, so deep networks can't learn (vanishing gradients). (2) **Not zero-centered** — the output is in $(0, 1)$, so gradients are always positive, causing zigzag optimization. (3) **No sparsity** — every neuron produces a non-zero output, wasting capacity. ReLU/GELU/SwiGLU solve all three: non-saturating for positive inputs, zero-centered (mostly), and sparse. Sigmoid is still used for output (binary classification) and gating (LSTM gates) where the $(0, 1)$ range is desired.

4. **Q: How does the choice of activation interact with initialization?**
   A: The activation's derivative at init determines the right scale. For ReLU (derivative 0 or 1, expected 0.5 for symmetric inputs), He init uses variance $2/n$ to compensate for the 50% zeroing. For GELU (similar to ReLU but smoother), He init works. For tanh (derivative $\leq 1$), Xavier init uses variance $1/n$. Mismatching activation and init causes activation explosion or vanishing at init, which destabilizes training. Modern LLMs use SwiGLU with He init scaled by $\sqrt{2/n}$ — the gating adds variance, so the scale is adjusted.

5. **Q: Why is SwiGLU's hidden dimension $\frac{8}{3} d$ instead of $4d$?**
   A: SwiGLU has 3 weight matrices (gate, up, down) instead of GELU's 2 (up, down). To keep the parameter count comparable, the hidden dimension is reduced by a factor of $2/3$: $4d \times 2/3 = 8d/3$. Without this reduction, SwiGLU would have 1.5× the parameters of GELU for the same $d_{model}$, which would be an unfair comparison. The $8/3$ factor is empirical; some models use slightly different values (e.g., Llama uses $\lfloor 8d/3 / 256 \rfloor \times 256$ to align with Tensor Core sizes).

6. **Q: How does activation choice affect quantization?**
   A: Two issues. (1) **Range** — unbounded activations (ReLU, GELU, SwiGLU) can produce large values that exceed INT8's range. Per-channel quantization handles this by giving each channel its own scale. (2) **Element-wise multiply** — SwiGLU's gate multiply amplifies quantization noise. The product of two INT8 values has higher relative error than the inputs. Mitigations: keep SwiGLU in fp16 (quantize only the linear layers), or use INT8 with careful per-channel scales. Most production INT8 LLMs (vLLM, TensorRT-LLM) handle this automatically, but custom implementations need care.

## See Also

- [[Perceptrons and MLPs]]
- [[Backpropagation]]
- [[Transformer Block]]
- [[Normalization Layers]]
- [[04 - Neural Networks/MOC|Neural Networks MOC]]
