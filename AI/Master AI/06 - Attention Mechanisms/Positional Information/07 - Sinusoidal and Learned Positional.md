---
tags: [attention, positional-encoding, sinusoidal, learned]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Sinusoidal and Learned Positional Encoding]
---

# 07 - Sinusoidal and Learned Positional Encoding

> [!info] TL;DR
> The two earliest positional encodings: **sinusoidal** (Vaswani et al. 2017, fixed sines/cosines) and **learned absolute** (GPT-2, BERT, learned per-position embeddings). Both largely superseded by RoPE for modern LLMs, but still appear in encoder models and historical code.

## Why Both Exist

Self-attention is permutation-invariant (see [[06 - Positional Encoding Overview]]). The original Transformer (Vaswani et al. 2017) added **sinusoidal** positional encodings to inject order. GPT-2 and BERT instead used **learned** positional embeddings — one trainable vector per position. Both work; both have limitations that RoPE later addressed.

## Sinusoidal Encoding (Vaswani et al. 2017)

For position $i$ and dimension $k$ (with $d$ total dimensions):

$$
\text{PE}(i, 2k) = \sin\left(\frac{i}{10000^{2k/d}}\right)
$$

$$
\text{PE}(i, 2k+1) = \cos\left(\frac{i}{10000^{2k/d}}\right)
$$

Each dimension is a sinusoid at a different frequency. Low dimensions have high frequency (capture fine position); high dimensions have low frequency (capture coarse position).

### The hope (that didn't quite pan out)

The authors hoped sinusoidal encoding would **extrapolate** to longer sequences than seen in training, because $\sin(i + \delta)$ is a linear function of $\sin(i)$ and $\cos(i)$:

$$
\sin(i + \delta) = \sin(i) \cos(\delta) + \cos(i) \sin(\delta)
$$

So in principle, the model could learn to attend by relative position. In practice, this extrapolation didn't work well — models trained with sinusoidal encoding on length 512 degrade past length 512.

### Pros
- No parameters (fixed).
- Deterministic.
- Theoretically motivated.

### Cons
- Extrapolation in practice is poor.
- The encoding is added to the input embedding only — it doesn't directly inform the attention computation (unlike RoPE, which rotates Q/K).
- Used in the original Transformer; rarely in modern LLMs.

## Learned Absolute Positional Embeddings (GPT-2, BERT)

Each position $i \in [0, L_{\max})$ has a learned embedding $\mathbf{p}_i \in \mathbb{R}^d$:

$$
\mathbf{x}_i = \mathbf{e}_{\text{token}_i} + \mathbf{p}_i
$$

The embeddings $\mathbf{p}_0, \ldots, \mathbf{p}_{L_{\max}-1}$ are trained alongside the model.

### Pros
- Simple: just a learned embedding table.
- Flexible: the model learns whatever positional information is useful.
- Worked well for BERT and GPT-2.

### Cons
- **Hard context limit**: position $i \geq L_{\max}$ is undefined. The model literally cannot process contexts longer than its training length.
- No notion of relative position (the model must implicitly learn it).
- Embeddings can be wasted capacity if some positions are rarely used.

### Where it's still used
- BERT and BERT-family models (since they're 512-token models anyway, extrapolation isn't a concern).
- Some vision Transformers (ViT) — images have fixed grid positions.
- Original GPT and GPT-2.

Modern decoder LLMs (Llama, Mistral, Gemma, Qwen, DeepSeek) all use RoPE instead.

## Worked Example (Sinusoidal)

```python
import torch
import math

def sinusoidal_pe(max_len, d_model):
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe

pe = sinusoidal_pe(512, 768)
# x = token_embeddings + pe[:seq_len]
```

## Worked Example (Learned)

```python
import torch.nn as nn

class LearnedPositionalEmbedding(nn.Module):
    def __init__(self, max_len, d_model):
        super().__init__()
        self.pe = nn.Embedding(max_len, d_model)
    
    def forward(self, x):
        # x: (B, T, D)
        positions = torch.arange(x.size(1), device=x.device)
        return x + self.pe(positions)
```

## Why Both Were Replaced

Sinusoidal and learned absolute encodings share a common limitation: **they don't generalize well to longer sequences than training**. Modern LLMs need to support long contexts (32k, 128k, 1M+ tokens), which means:

- Can't use learned absolute embeddings (positions past training length are undefined).
- Sinusoidal extrapolation in practice is unreliable.
- Relative encodings (RoPE, ALiBi) handle this much better.

RoPE ([[08 - RoPE]]) rotates Q and K by position, making attention depend on relative offset. This is the modern default. ALiBi ([[09 - ALiBi]]) adds a linear bias based on relative distance.

## Why This Matters for AI

- BERT-family models still use learned absolute embeddings. If you work with BERT, you'll see `position_ids` in the model output.
- Understanding sinusoidal encoding helps you read the original Transformer paper and understand why relative encodings were invented.
- For **vision Transformers**, learned 2D positional embeddings are still standard (images have fixed grid positions, so extrapolation isn't a concern).

## Production Implications

- For BERT-family models, max sequence length is fixed at 512 (or 1024 for some variants). Plan for this.
- For ViT, image size at training time determines the positional embedding grid. Resizing images requires interpolating the positional embeddings.
- For decoder LLMs (Llama, etc.), use RoPE — never sinusoidal or learned absolute.

## Common Pitfalls

- **Mixing positional encoding types** — don't combine absolute + RoPE; pick one.
- **Forgetting to handle position 0** — some implementations start at position 1; others at 0. Match the model's training convention.
- **Truncating positions past training length** for absolute embeddings — the model produces garbage. Use a model with RoPE if you need long context.

## Further Reading

- Vaswani et al. (2017), *Attention Is All You Need* — sinusoidal.
- Devlin et al. (2019), *BERT* — learned absolute.
- Radford et al. (2019), *GPT-2* — learned absolute.

## See Also

- [[06 - Positional Encoding Overview]]
- [[08 - RoPE]]
- [[09 - ALiBi]]
- [[10 - YaRN and NTK-aware Scaling]]
- [[06 - Attention Mechanisms/MOC|Attention MOC]]

## Why Sinusoidal Extrapolation Failed in Practice

The original Transformer paper hypothesized that sinusoidal encoding would extrapolate because $\sin(i + \delta)$ is a linear function of $\sin(i)$ and $\cos(i)$:

$$\sin(i + \delta) = \sin(i)\cos(\delta) + \cos(i)\sin(\delta)$$

The hope: the model could learn to attend by relative position. In practice, this didn't work — models trained on length 512 degrade past length 512. Why?

1. **The model learns absolute patterns**: during training, positions 0-511 always appear. The model learns position-specific patterns (e.g., "attend to position 0 for the [CLS] token"). At position 512+, these patterns break.
2. **Attention scores depend on the full $Q K^T$ product**, not just the positional part. The content-content interaction dominates, and the positional signal is a small perturbation that the model doesn't learn to extract robustly.
3. **High-frequency dimensions alias**: for positions beyond training, high-frequency sinusoids wrap around, creating aliasing — two different positions look identical to that frequency.

This is why RoPE (which makes the dot product explicitly depend on relative position) and ALiBi (which adds a relative bias) work better — they don't rely on the model learning to extract relative position from absolute encoding.

## Learned Absolute in ViT — Why It Still Works

Vision Transformers (ViT) use learned 2D positional embeddings. Why does this work when it fails for text?

1. **Fixed image size**: ViT is trained and evaluated at the same resolution (e.g., 224×224). No extrapolation needed.
2. **Grid structure**: images have a fixed grid; positions are 2D coordinates, not 1D sequence positions.
3. **Limited positions**: a 224×224 image with 16×16 patches has only 14×14 = 196 positions. The embedding table is small.

For variable-resolution ViT (e.g., NaViT), learned absolute doesn't work — you need interpolatable positional embeddings (bicubic interpolation of the learned grid) or relative encodings. This is why NaViT uses RoPE-like relative position encoding.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Quality drops past training length | Absolute encoding can't extrapolate | Use RoPE + YaRN for long context |
| ViT fails on resized images | Learned positional grid doesn't match | Interpolate positional embeddings (bicubic) |
| Mixing encoding types | Combining absolute + RoPE | Pick one; they conflict |

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Positional Information/06 - Positional Encoding Overview|Positional Encoding Overview]].
- [[06 - Attention Mechanisms/Positional Information/08 - RoPE|RoPE]] — the successor.
- [[06 - Attention Mechanisms/Positional Information/09 - ALiBi|ALiBi]] — the alternative.
- [[07 - Transformers/Architecture/01 - Transformer Block|Transformer Block]].
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017|Vaswani 2017]] — sinusoidal.
- [[26 - Papers/Transformers/03 - BERT 2018|BERT 2018]] — learned absolute.
- [[26 - Papers/Transformers/21 - Vision Transformer ViT 2020|ViT 2020]] — 2D learned.

## Interview Questions

1. **Q: Why did sinusoidal encoding fail to extrapolate despite the theoretical argument?**
   A: The theory says $\sin(i+\delta)$ is linear in $\sin(i), \cos(i)$, so the model could learn relative attention. In practice: (1) the model learns absolute position-specific patterns during training; (2) attention scores are dominated by content-content interaction, not the positional perturbation; (3) high-frequency dimensions alias past training length. RoPE and ALiBi work better because they make relative position explicit in the attention computation, not relying on the model to extract it.

2. **Q: When is learned absolute positional encoding still used?**
   A: For BERT-family models (fixed 512 context — extrapolation isn't a concern) and ViT (fixed image size — grid structure, limited positions). For any model that needs variable-length or long-context, use RoPE. NaViT (variable-resolution ViT) uses RoPE-like relative encoding because learned absolute can't handle variable resolution.

3. **Q: How do you handle resized images in ViT?**
   A: Bicubic interpolation of the learned positional embeddings. The original grid (e.g., 14×14 for 224px) is interpolated to the new grid size (e.g., 16×16 for 256px). This works for small resizes but degrades for large ones. For variable-resolution ViT, use relative positional encoding (RoPE-like) instead of learned absolute.

## See Also

- [[06 - Positional Encoding Overview]]
- [[08 - RoPE]]
- [[09 - ALiBi]]
- [[10 - YaRN and NTK-aware Scaling]]
- [[06 - Attention Mechanisms/MOC|Attention MOC]]
