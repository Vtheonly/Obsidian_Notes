---
tags: [paper, performer, efficient-attention, kernel, random-features]
iteration: 4
created: 2026-08-08
aliases: [Performer 2021, Choromanski 2021, Linearized Attention]
---

# 22 — Performer (Choromanski et al., 2021)

> [!info] TL;DR
> Performer ("Permutation-Invariant Transformer") linearized attention using **random Fourier features** (specifically, the FAVOR+ algorithm). Instead of computing the N×N attention matrix, Performer approximates the softmax kernel with random projections, enabling O(N · r) attention where r is the number of random features. The approximation is unbiased and comes with formal error bounds. Performer is the canonical "kernel method" approach to linear attention.

## Citation

Choromanski, K., Likhosherstov, V., Dohan, D., Song, X., Gane, A., Sarlós, T., Hawkins, P., Davis, J., Mohiuddin, A., Kaiser, L., Belanger, D., Colwell, L. J., & Weller, A. (2021). *Rethinking Attention with Performers*. ICLR 2021. arXiv:2009.14794.

## The Problem Being Solved

Standard attention computes `softmax(Q K^T) V`, which requires materializing the N×N matrix `Q K^T`. For long sequences, this is the bottleneck.

The mathematical structure is: `Attention(Q, K, V) = D^{-1} (exp(Q K^T) V)` where `D` is the normalizing diagonal. The `exp(Q K^T)` is the softmax kernel — it's a function of `Q K^T`, not a linear operation.

**Key observation**: if we could decompose `exp(q · k)` into a product of functions of `q` and `k` separately — i.e., `exp(q · k) ≈ φ(q)^T φ(k)` for some feature map `φ` — then we could rearrange the computation:

```
Standard:    softmax(Q K^T) V = (exp(Q K^T) / D) V           # O(N²)
Linearized:  (Q' (K'^T V)) / (Q' (K'^T 1))                   # O(N·r)
             where Q' = φ(Q), K' = φ(K)
```

The rearrangement exploits associativity: instead of computing `exp(Q K^T) V` (which needs the N×N matrix), compute `K'^T V` first (an r×d matrix, cheap), then multiply by `Q'`. This is O(N · r · d) instead of O(N² · d).

The challenge: finding a `φ` that approximates the softmax kernel well with small r. This is where random features come in.

## The Key Idea: FAVOR+ (Fast Attention via Positive Orthogonal Random Features)

### Random Fourier Features
The softmax kernel `exp(q · k)` can be approximated using random projections. The technique (from Rahimi & Recht, 2007) works as follows:

1. Sample random vectors `ω_1, ..., ω_r` from a Gaussian distribution.
2. Define `φ(x) = [exp(i ω_1 · x), ..., exp(i ω_r · x)]` (complex exponentials).
3. By the Fourier transform, `E[φ(q) · φ(k)^*] = exp(q · k)` (up to constants).

So `φ(q)^T φ(k)` is an unbiased estimator of `exp(q · k)`, with variance that decreases as r increases. With r ≈ 100–1000, the approximation is good enough for practical use.

### Positive Random Features
The original random Fourier features are complex-valued, which is awkward for neural networks. Performer uses a clever trick (based on a change of variables) to make the features non-negative and real-valued, while preserving the unbiasedness:

```
φ(x) = [exp(-||x||²/2) · exp(ω_1 · x), ..., exp(-||ω_r · x||²/2) · exp(ω_r · x)]
```

with `ω_i` sampled from a specific distribution. This gives non-negative features and the kernel `φ(q)^T φ(k)` approximates `exp(q · k)`.

### Orthogonal Random Features
To reduce variance, Performer orthogonalizes the random vectors (using Gram-Schmidt or Householder transforms). Orthogonal features give lower-variance estimates than independent features for the same r.

### Permutation Invariance
The "Performer" name comes from the property that the approximation is invariant to the order of queries and keys — you get the same result regardless of how you permute the input. This is essential for attention (the result shouldn't depend on token order in the batch).

```mermaid
graph TD
  subgraph Standard Attention O(N²)
    Q1[Q: N×d] --> M1[exp Q·K^T: N×N]
    K1[K: N×d] --> M1
    M1 --> V1[× V: N×d]
  end
  subgraph Performer Attention O(N·r)
    Q2[Q: N×d] --> PhiQ[φ Q: N×r]
    K2[K: N×d] --> PhiK[φ K: N×r]
    PhiK --> KtV[K^T V: r×d]
    V2[V: N×d] --> KtV
    PhiQ --> QKtV[Q × K^T V: N×d]
    KtV --> QKtV
  end
```

## Key Results

Performer achieved competitive quality with vanilla Transformers while being faster for long sequences:

| Sequence Length | Vanilla Transformer | Performer (r=256) | Speedup |
|-----------------|---------------------|-------------------|---------|
| 512             | 1.0×                | 0.85×             | (slower — overhead) |
| 1024            | 1.0×                | 1.1×              |         |
| 4096            | OOM                 | 1.0×              | ∞       |
| 8192            | OOM                 | 1.0×              | ∞       |

On protein sequence modeling (a key application — protein sequences are very long), Performer matched full-attention Transformers with 4× less memory. On image classification (ViT), Performer slightly underperformed vanilla ViT but trained faster.

The paper also showed that Performer could be used as a drop-in replacement for attention in pretrained models — you could take a pretrained vanilla Transformer and fine-tune it with Performer attention, with minimal quality loss. This made adoption easier.

## Why It Worked

### Unbiased Approximation
Unlike [[19 - Linformer 2020|Linformer]] (which uses learned, biased projections), Performer's random features are unbiased. The expected approximation is exact; only the variance matters. This gives more predictable quality.

### Formal Error Bounds
The paper provided formal bounds on the approximation error as a function of r. Practitioners could choose r based on their quality tolerance, with theoretical guarantees.

### No Training-Time Modification Needed
Performer's random features are not learned — they're sampled once and fixed. This means you can swap standard attention for Performer attention without retraining the model (though fine-tuning helps). This made Performer attractive as a drop-in efficiency improvement.

### Works with Any Kernel
The FAVOR+ algorithm works for any kernel, not just softmax. Performer can approximate ReLU, polynomial, or other kernels. This generality made it a useful tool for kernel methods in deep learning.

## Limitations

### Variance at High Precision
For applications requiring high-precision attention (e.g., retrieval tasks where the exact attention weight matters), Performer's variance is too high. The approximation is unbiased but noisy, which hurts on tasks sensitive to small attention differences.

### Constant Factor Overhead
For short sequences (where N² < N · r), Performer is slower than vanilla attention due to the feature computation overhead. Performer only wins at long sequences (N > r, typically N > 1000).

### Quality Gap on Hard Tasks
On simple tasks (classification), Performer matches vanilla Transformers. On hard tasks (long-range retrieval, precise copy operations), the approximation loses information and quality drops.

### Superseded by FlashAttention
[[08 - FlashAttention 2022|FlashAttention]] (2022) made exact attention fast enough for most practical sequence lengths, removing the main motivation for linearized attention. For very long contexts, sparse attention (Longformer-style) is generally preferred over kernel methods.

## Impact and Legacy

Performer's direct influence on production systems is limited, but its conceptual contributions were significant:

1. **Established the kernel method approach to linear attention**. Performer is the canonical reference for "linearize attention via kernel approximation". Subsequent linear attention variants (Linear Attention, Cosformer, RWKV) build on the same mathematical framework.

2. **Random features for neural networks**. The use of random features (a classical technique from kernel methods) in deep learning influenced other applications. Random projections appear in efficient MLPs, large-scale retrieval, and model compression.

3. **Theoretical framework for attention approximation**. Performer's formal error bounds provided a template for analyzing other efficient attention variants. Subsequent papers could ask "what's the approximation error of this method?" and use Performer's tools.

4. **Foundation for modern linear attention**. Linear attention variants (used in some 2024–2025 efficient LLMs) are direct descendants of Performer's approach. The math is the same; the difference is in the choice of feature map and the application context.

For AI engineers, Performer is mostly of historical interest. Modern long-context models use FlashAttention (for exact attention at moderate scale) or sparse/hybrid attention (for very long contexts). But understanding Performer clarifies the kernel method approach to linear attention, which is relevant for understanding modern efficient attention variants and the theoretical foundations of attention approximation.

## Further Reading

- Original paper: arXiv:2009.14794
- Rahimi & Recht (2007), *Random Features for Large-Scale Kernel Machines* — the foundation.
- [[13 - Linear Attention]] — broader survey of linear attention variants.

## See Also

- [[12 - Sparse Attention]]
- [[13 - Linear Attention]]
- [[17 - Reformer 2020]]
- [[18 - Longformer 2020]]
- [[19 - Linformer 2020]]
- [[20 - BigBird 2020]]
- [[08 - FlashAttention 2022]]
- [[26 - Papers/MOC|Papers MOC]]
