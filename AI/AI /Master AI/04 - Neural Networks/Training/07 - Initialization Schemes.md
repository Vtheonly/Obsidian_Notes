---
tags: [neural-networks, training, initialization]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Initialization Schemes]
---

# 07 - Initialization Schemes

> [!info] TL;DR
> How you initialize neural network weights matters — bad init causes vanishing/exploding gradients from step 1. The two main schemes: **Xavier (Glorot)** for tanh/sigmoid, **He (Kaiming)** for ReLU. Modern Transformers typically use a scaled variant of He init.

## Why Initialization Matters

At step 0, before any training, the network does a forward pass with random weights. The init determines:

- **Activation magnitudes**: do they stay roughly constant across layers, or grow/shrink exponentially?
- **Gradient magnitudes**: same question, but for backward pass.
- **Symmetry breaking**: if all weights are equal, all neurons in a layer compute the same thing — wasted capacity.

Bad init = training never converges, or converges to a bad solution.

## The Goal of Good Init

For a layer $\mathbf{y} = \mathbf{W} \mathbf{x}$ with $\mathbf{x} \in \mathbb{R}^{n_{\text{in}}}$:

$$
\text{Var}(\mathbf{y}) = n_{\text{in}} \cdot \text{Var}(W_{ij}) \cdot \text{Var}(\mathbf{x})
$$

We want $\text{Var}(\mathbf{y}) \approx \text{Var}(\mathbf{x})$ (activations don't blow up or vanish). This gives:

$$
\text{Var}(W_{ij}) = \frac{1}{n_{\text{in}}}
$$

For the backward pass, gradients flow through $\mathbf{W}^T$, and the analogous condition gives $\text{Var}(W_{ij}) = \frac{1}{n_{\text{out}}}$.

## Xavier / Glorot Initialization (tanh, sigmoid)

Glorot & Bengio (2010) proposed averaging the forward and backward conditions:

$$
\text{Var}(W_{ij}) = \frac{2}{n_{\text{in}} + n_{\text{out}}}
$$

Sample from $\mathcal{N}\left(0, \frac{2}{n_{\text{in}} + n_{\text{out}}}\right)$ or $\mathcal{U}\left(-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}, \sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right)$.

Designed for **symmetric activations** (tanh, sigmoid) where the activation is roughly linear near 0 and saturates away from 0. Xavier keeps activations in the linear regime.

## He / Kaiming Initialization (ReLU family)

He et al. (2015) observed that ReLU zeros out half its inputs, so the variance is halved. The fix: double the init variance.

$$
\text{Var}(W_{ij}) = \frac{2}{n_{\text{in}}}
$$

Sample from $\mathcal{N}\left(0, \frac{2}{n_{\text{in}}}\right)$ or $\mathcal{U}\left(-\sqrt{\frac{6}{n_{\text{in}}}}, \sqrt{\frac{6}{n_{\text{in}}}}\right)$.

**The default for ReLU-based networks.** Also used for GELU, SiLU/Swish (which are ReLU-like in their effective behavior).

## For Transformers

Modern Transformers (GPT-2, Llama, etc.) use modified He init:

- **Embedding init**: usually $\mathcal{N}(0, d_{\text{model}}^{-1/2})$ or $\mathcal{N}(0, d_{\text{model}}^{-1})$.
- **Linear layer init**: typically $\mathcal{N}(0, 0.02)$ (GPT-2 style, fixed small std) or $\mathcal{N}(0, \frac{2}{n_{\text{in}} \cdot \text{depth}})$ (residual scaling).
- **Residual layer scaling**: some models scale init by $1/\sqrt{N}$ where $N$ is the depth — to keep residual contributions roughly constant across layers.
- **Output projection init**: often zeros (so the initial output is uniform over vocabulary).

These choices are subtle and matter. Most public models document their init in the config or paper.

## Bias Initialization

- **Standard**: zeros. Simple, works fine.
- **LSTM forget gate bias**: initialized to 1.0 (so the forget gate starts "open" — gradient flows easily early in training). Critical for LSTM training.
- **Output layer bias**: sometimes initialized to the inverse frequency of classes (helps with class imbalance).
- **Final unembedding bias**: usually zeros.

## Worked Example

```python
import torch
import torch.nn as nn

# Xavier (for tanh)
linear = nn.Linear(100, 50)
nn.init.xavier_normal_(linear.weight)

# He (for ReLU)
conv = nn.Conv2d(3, 64, 3)
nn.init.kaiming_normal_(conv.weight, mode='fan_in', nonlinearity='relu')

# Transformer-style
embedding = nn.Linear(768, 768)
nn.init.normal_(embedding.weight, mean=0, std=0.02)
nn.init.zeros_(embedding.bias)
```

## Why This Matters for AI

- Bad init is a silent killer — training "works" but converges to poor solutions, and it's hard to diagnose without comparing to good init.
- Init choice depends on activation function. Mixing them up (Xavier with ReLU, He with tanh) leads to slow or unstable training.
- For **fine-tuning**, init is the pretrained weights — you don't re-init. But you do init the **new** parameters (LoRA's B matrix starts at zero, for example). See [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]].
- The **residual stream** in Transformers is especially sensitive — bad init causes the residual to grow or shrink across layers.

## Production Implications

- **Use the default inits from PyTorch/HuggingFace** — they're well-chosen for the standard architectures.
- **For custom architectures**, think carefully about init. Test that activation magnitudes are roughly constant across layers at initialization (forward a random input, log per-layer norms).
- **For Transformer training from scratch**, follow a published recipe (e.g., GPT-2's `std=0.02` for linear layers, scaled by $1/\sqrt{N}$ for residuals).
- **Don't re-init when fine-tuning** — start from pretrained weights.
- **For LoRA**: init A with Kaiming, B with zero. So $\Delta \mathbf{W} = \mathbf{B}\mathbf{A} = 0$ at start (the model behaves like the base model initially).

## Common Pitfalls

- **Using Xavier for ReLU** — works "okay" but He is strictly better.
- **Zero init for all weights** — every neuron computes the same thing (symmetric), no learning. Always use random init for weights.
- **Forgetting to init biases** — usually fine (zeros), but be intentional.
- **Init too large** — activations explode; gradients explode; training diverges.
- **Init too small** — activations vanish; gradients vanish; training stalls.
- **Not scaling residual branches** — in deep networks, the residual highway can dominate or be dominated by the sublayer outputs.

## Further Reading

- Glorot & Bengio (2010), *Understanding the Difficulty of Training Deep Feedforward Neural Networks*.
- He et al. (2015), *Delving Deep into Rectifiers* (Kaiming init).
- GPT-2 paper (Radford et al. 2019) — Transformer init recipe.

## Derivation of Xavier/He Init (Detailed)

The math behind initialization schemes:

### Forward pass analysis
For a linear layer $\mathbf{y} = \mathbf{W}\mathbf{x}$ where $\mathbf{x} \in \mathbb{R}^{n_{\text{in}}}$, $\mathbf{W} \in \mathbb{R}^{n_{\text{out}} \times n_{\text{in}}}$, with $W_{ij} \sim \mathcal{N}(0, \sigma_W^2)$ i.i.d. and $\mathbb{E}[x_i] = 0$, $\text{Var}(x_i) = \sigma_x^2$:

$$
\text{Var}(y_j) = \sum_{i=1}^{n_{\text{in}}} \text{Var}(W_{ji} x_i) = n_{\text{in}} \sigma_W^2 \sigma_x^2
$$

To keep $\text{Var}(y) = \text{Var}(x)$ (activations don't grow/shrink), we need $\sigma_W^2 = 1/n_{\text{in}}$.

### Backward pass analysis
Gradients flow through $\mathbf{W}^T$: $\frac{\partial L}{\partial \mathbf{x}} = \mathbf{W}^T \frac{\partial L}{\partial \mathbf{y}}$. By analogous analysis, to keep gradient variance constant, we need $\sigma_W^2 = 1/n_{\text{out}}$.

### Xavier's compromise
Glorot & Bengio (2010) averaged the two: $\sigma_W^2 = 2/(n_{\text{in}} + n_{\text{out}})$. This balances forward and backward stability — neither perfect, but both acceptable.

### He's correction for ReLU
He et al. (2015) observed that ReLU zeros out ~half the inputs: $y_j = \text{ReLU}(\sum_i W_{ji} x_i)$. The variance of the active (non-zero) outputs is halved. To compensate, double the init variance: $\sigma_W^2 = 2/n_{\text{in}}$.

### Why this matters
Without these schemes, deep networks (10+ layers) were untrainable — activations exploded or vanished. Xavier/He init was a prerequisite for the deep learning revolution. Modern Transformers use modified He init with additional scaling for residual streams.

## Transformer Initialization (Detailed Recipe)

Modern Transformers (GPT-2, Llama, Mistral) use a specific init recipe:

### Embedding initialization
- Token embedding: $\mathcal{N}(0, d_{\text{model}}^{-1/2})$ — scaled so the embedding norm is ~1.
- Positional embedding: usually learned, initialized $\mathcal{N}(0, d_{\text{model}}^{-1/2})$ or sinusoidal (no learning).

### Linear layer initialization
- QKV projections: $\mathcal{N}(0, 0.02)$ (GPT-2) or $\mathcal{N}(0, (2/n_{\text{in}})^{1/2})$ (He-style).
- Output projection: $\mathcal{N}(0, 0.02)$.
- FFN layers: $\mathcal{N}(0, 0.02)$ or He init.

### Residual stream scaling
The residual stream accumulates contributions from all layers. To keep the residual magnitude stable across depth:
- Scale each residual branch by $1/\sqrt{2 N}$ where $N$ is the number of residual layers (GPT-2 style).
- Or use LayerNorm before each residual addition (pre-norm) — the modern default.

### Output projection
- Final unembedding: often initialized to zeros, so the initial output is uniform over vocabulary. This ensures the initial loss is $\log(\text{vocab})$ (the entropy of uniform distribution), not some random value.

### Why this matters
Transformer init is subtle — small mistakes cause training to never converge or converge to bad solutions. Following a published recipe (GPT-2, Llama) is much safer than designing your own.

## LoRA Initialization (Special Case)

LoRA has a unique init: A is Kaiming-initialized, B is zero. So $\Delta \mathbf{W} = \mathbf{B}\mathbf{A} = 0$ at start — the model behaves exactly like the base model initially.

```python
class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, rank=8):
        super().__init__()
        self.A = nn.Parameter(torch.randn(rank, in_features) * (1.0 / in_features) ** 0.5)
        self.B = nn.Parameter(torch.zeros(out_features, rank))

    def forward(self, x):
        return self.B @ self.A @ x  # = 0 at init
```

This is critical — if both A and B were random, the initial output would be a random perturbation of the base model, causing unstable early training. The zero-init ensures a smooth start: the LoRA contribution grows gradually as B learns.

## Modern Initialization Research (2020-2026)

### MuP (Model Parameterization)
Yang et al. (2021) introduced **MuP** — a parameterization that makes hyperparameters (learning rate, init scale) transferable across model sizes. With MuP, you can tune hyperparameters on a small model and transfer them to a large model. This addresses a major pain point: tuning LRs on 100B-parameter models is prohibitively expensive.

### Tensor Programs
Tensor Programs (Yang et al. 2022-2024) generalize MuP to broader architectural choices. The key insight: with the right parameterization, the Maximum Update Parameterization ($\mu$P) ensures that as model width grows, the update size stays stable. This enables principled scaling without re-tuning init.

### Fixup
Fixup (Zhang et al. 2019) is an init scheme for residual networks without normalization layers. It scales residual branches to compensate for the absence of LayerNorm. Useful for understanding why LayerNorm matters, even if rarely used in practice.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Loss doesn't decrease from initial value | Init too large (activations explode) or too small (gradients vanish) | Use He init for ReLU; check activation norms per layer |
| Loss starts high and stays flat | Output layer init wrong (e.g., not zero for unembedding) | Init final projection to zeros; check initial loss = log(vocab) |
| Training unstable (loss spikes) | Init variance too high | Reduce init std; use residual scaling |
| Different runs give very different results | Init seed not fixed | Set torch.manual_seed; document seed in config |
| Fine-tune degrades base model | LoRA B not zero-initialized | Ensure B is zero-init so ΔW = 0 at start |
| Deep network (50+ layers) won't train | No residual scaling; bad init | Use pre-norm + residual scaling; follow published recipe |

## Connection to Other Concepts

- [[02 - Mathematics/Probability/09 - Gaussian Distribution|Gaussian Distribution]] — init uses Gaussians.
- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — init affects gradient flow.
- [[02 - Mathematics/Linear Algebra/05 - Matrix Decomposition|Matrix Decomposition]] — init affects singular values of weight matrices.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — gradients depend on init.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — bad init causes these.
- [[04 - Neural Networks/Foundations/02 - Activation Functions|Activation Functions]] — init depends on activation (Xavier for tanh, He for ReLU).
- [[07 - Transformers/Architecture/02 - Pre-Norm vs Post-Norm|Pre-Norm vs Post-Norm]] — affects init requirements.
- [[07 - Transformers/Architecture/03 - Residual Connections|Residual Connections]] — residual stream init scaling.
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — special init (B=0).
- [[11 - Training/Optimization/05 - Loss Spikes and Stability|Loss Spikes and Stability]] — bad init causes spikes.

## Interview Questions

1. **Q: Derive He initialization for ReLU networks.**
   A: For $\mathbf{y} = \mathbf{W}\mathbf{x}$ with $W_{ij} \sim \mathcal{N}(0, \sigma_W^2)$, $\text{Var}(y_j) = n_{\text{in}} \sigma_W^2 \sigma_x^2$. To keep $\text{Var}(y) = \text{Var}(x)$, need $\sigma_W^2 = 1/n_{\text{in}}$. But ReLU zeros out ~half the inputs, halving the effective variance. Compensate by doubling: $\sigma_W^2 = 2/n_{\text{in}}$. This is He init.

2. **Q: Why is the final unembedding often initialized to zeros?**
   A: So the initial output is uniform over the vocabulary — the initial loss is exactly $\log(\text{vocab})$, the entropy of the uniform distribution. This gives a clean starting point: any reduction in loss is real learning, not artifact of random init. If the unembedding were random, the initial loss would be a random value, making it harder to detect training issues.

3. **Q: Why does LoRA initialize B to zero and A to random?**
   A: So $\Delta \mathbf{W} = \mathbf{B}\mathbf{A} = 0$ at start — the model behaves exactly like the base model initially. This ensures a smooth start: the LoRA contribution grows gradually as B learns. If both were random, the initial output would be a random perturbation, causing unstable early training. The asymmetry (A random, B zero) is essential.

4. **Q: What is MuP, and why does it matter?**
   A: MuP (Maximum Update Parameterization, Yang et al. 2021) is a parameterization that makes hyperparameters (LR, init scale) transferable across model sizes. With MuP, you can tune hyperparameters on a small model (cheap) and transfer them to a large model (expensive). Without MuP, optimal LR changes with model width, requiring expensive re-tuning at each scale.

5. **Q: Why do Transformers scale residual branches by $1/\sqrt{2N}$?**
   A: The residual stream accumulates contributions from $N$ layers. Without scaling, the variance of the residual grows linearly with $N$ (variance of sum of $N$ i.i.d. terms). Scaling by $1/\sqrt{2N}$ keeps the residual variance constant across depth ($2N$ because each layer has attention + FFN contributions). This stabilizes training of deep Transformers.

6. **Q: What happens if you use Xavier init for a ReLU network?**
   A: It "works" but suboptimally. Xavier assumes symmetric activations (tanh/sigmoid) where the derivative is ~1 near 0. ReLU zeros out half its inputs, so the effective variance is halved — Xavier's $\sigma_W^2 = 2/(n_{\text{in}} + n_{\text{out}})$ is too small by ~2×. The network trains but slower and may converge to worse solutions. He init ($\sigma_W^2 = 2/n_{\text{in}}$) is the correct choice for ReLU.

## See Also

- [[06 - Backpropagation]]
- [[08 - Vanishing and Exploding Gradients]]
- [[02 - Mathematics/Probability/09 - Gaussian Distribution|Gaussian Distribution]]
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] (initialization for LoRA)
- [[04 - Neural Networks/MOC|Neural Networks MOC]]