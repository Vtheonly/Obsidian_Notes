---
tags: [transformer, components, normalization, layernorm, rmsnorm]
iteration: 1
created: 2026-08-07
---

# Normalization Layers

> [!info] TL;DR
> Normalization keeps activations well-scaled during training. The original Transformer used LayerNorm; modern LLMs (Llama, Mistral, Gemma, Qwen, DeepSeek) use **RMSNorm** — a simpler, faster variant that drops the mean-centering. ScaleNorm is a third rare variant.

## Why Normalize?

Deep networks suffer from **internal covariate shift** — the distribution of each layer's inputs changes during training as the previous layers' weights update. This makes training slow and unstable. Normalization stabilizes the inputs to each layer.

Even though the "internal covariate shift" explanation is now disputed (the real benefit seems to be **smoother loss landscape** and **better conditioning**), normalization is empirically essential for training deep Transformers.

## BatchNorm vs LayerNorm

### BatchNorm (Ioffe & Szegedy, 2015)
Normalizes across the **batch dimension** for each feature:

$$
\hat{x}_{ij} = \frac{x_{ij} - \mu_j}{\sqrt{\sigma_j^2 + \epsilon}}
$$

where $\mu_j, \sigma_j$ are computed across the batch for feature $j$.

- Great for CNNs (where batch is large and features are spatial).
- Bad for RNNs/Transformers (batch statistics vary across timesteps; bad at inference with batch size 1).

### LayerNorm (Lei Ba et al., 2016)
Normalizes across the **feature dimension** for each example:

$$
\hat{\mathbf{x}} = \frac{\mathbf{x} - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

where $\mu, \sigma$ are computed across the features of a single example.

- Independent of batch size — works at batch size 1.
- The standard for Transformers.

### The "across which dimension?" intuition

- BatchNorm: normalize each feature across the batch.
- LayerNorm: normalize each example across its features.

## LayerNorm in Full

$$
\text{LN}(\mathbf{x}) = \boldsymbol{\gamma} \odot \frac{\mathbf{x} - \mu}{\sqrt{\sigma^2 + \epsilon}} + \boldsymbol{\beta}
$$

- $\mu = \frac{1}{d} \sum_i x_i$ (mean across features)
- $\sigma^2 = \frac{1}{d} \sum_i (x_i - \mu)^2$ (variance across features)
- $\boldsymbol{\gamma}, \boldsymbol{\beta}$ are learned per-feature scale and shift
- $\epsilon$ is a small constant for numerical stability

LayerNorm has $2d$ parameters per layer (the $\gamma$ and $\beta$).

## RMSNorm (Zhang & Sennrich, 2019)

**Root Mean Square Normalization** drops the mean-centering — only normalizes by the RMS (root mean square):

$$
\text{RMSNorm}(\mathbf{x}) = \boldsymbol{\gamma} \odot \frac{\mathbf{x}}{\sqrt{\frac{1}{d} \sum_i x_i^2 + \epsilon}}
$$

Differences from LayerNorm:
- No mean subtraction.
- No $\beta$ (no shift) — only $\gamma$ (scale).
- Fewer parameters (just $d$ vs $2d$).
- **Faster** — one less reduction.

Empirically, RMSNorm matches LayerNorm quality at lower compute. Used by **all modern decoder LLMs**: Llama, Mistral, Gemma, Qwen, DeepSeek.

### Why does dropping the mean work?

The mean-centering in LayerNorm is theoretically useful (zero-mean inputs are nicer for many operations) but in practice, the scale normalization is the important part. The mean subtraction adds compute and parameters without much benefit.

## ScaleNorm (rare)

A simpler variant that normalizes by a single learned scalar:

$$
\text{ScaleNorm}(\mathbf{x}) = \frac{\alpha}{\|\mathbf{x}\|} \mathbf{x}
$$

where $\alpha$ is a single learned scalar (shared across all dimensions and layers). Very few parameters; not commonly used.

## Where Norm Goes in a Transformer Block

See [[Pre-Norm vs Post-Norm]]. Modern Transformers use **pre-norm**: the norm is applied to the sublayer's input, not its output.

```python
# Pre-norm Transformer block (Llama-style)
x = x + attn(rmsnorm1(x))
x = x + ffn(rmsnorm2(x))
```

There's also a **final norm** after the last block — most modern Transformers have one (because the last block's residual output is unnormalized).

## Worked Implementation

```python
import torch
import torch.nn as nn

class LayerNorm(nn.Module):
    def __init__(self, d, eps=1e-5):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(d))
        self.beta  = nn.Parameter(torch.zeros(d))
        self.eps = eps
    
    def forward(self, x):
        mu = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        x_norm = (x - mu) / torch.sqrt(var + self.eps)
        return self.gamma * x_norm + self.beta

class RMSNorm(nn.Module):
    def __init__(self, d, eps=1e-6):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(d))
        self.eps = eps
    
    def forward(self, x):
        rms = torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return self.gamma * x * rms
```

PyTorch's `nn.LayerNorm` is well-optimized; for RMSNorm, use the model's reference implementation or `nn.RMSNorm` (PyTorch 2.4+).

## Why This Matters for AI

- Norm is **essential** for training deep Transformers. Without it, training is unstable past a few layers.
- The shift from LayerNorm to RMSNorm is one of the small but consistent improvements in modern LLMs.
- Norm interacts with:
  - **Initialization** — norms reduce sensitivity to initialization scale.
  - **Learning rate** — norms let you use higher learning rates.
  - **Mixed precision** — norms help with fp16/bf16 stability.
  - **Quantization** — at low precision, norm's $\gamma$ scale must be handled carefully (SmoothQuant, etc.).

## Production Implications

- **Use RMSNorm** for new model designs. It's faster and matches LayerNorm quality.
- **Fused kernels** — LayerNorm and RMSNorm are well-fused in PyTorch 2+, FlashAttention-2, and vLLM. Always use fused versions.
- **Quantization** — the norm's $\gamma$ parameter is sensitive to quantization. Most INT8/INT4 quantization schemes keep norms in fp16/fp32.
- **Norm placement bugs** are subtle. A model with the wrong norm placement will look fine on small inputs but degrade on larger ones.

## Common Pitfalls

- **Using BatchNorm in Transformers** — doesn't work; batch statistics are unreliable for sequence data.
- **Forgetting the final norm** — most Transformers need a norm after the last block.
- **Wrong eps** — too small → division by near-zero; too large → over-smoothing. 1e-5 to 1e-6 is standard.
- **Applying norm in the wrong place** — pre-norm and post-norm are different architectures. Pick one and be consistent.
- **Weight decay on norm parameters** — don't apply weight decay to $\gamma$ (and $\beta$ if using LayerNorm). They're scale parameters, not weights; weight decay doesn't have a regularization interpretation here.

## Further Reading

- Ioffe & Szegedy (2015), *Batch Normalization*.
- Lei Ba et al. (2016), *Layer Normalization*.
- Zhang & Sennrich (2019), *Root Mean Square Layer Normalization*.
- Xu et al. (2019), *Understanding and Improving Layer Normalization*.

## See Also

- [[Transformer Block]]
- [[Pre-Norm vs Post-Norm]]
- [[Residual Connections]]
- [[Activation Functions]]
- [[07 - Transformers/MOC|Transformers MOC]]
