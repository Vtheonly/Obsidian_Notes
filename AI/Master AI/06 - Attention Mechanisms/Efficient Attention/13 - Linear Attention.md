---
tags: [attention, efficient-attention, linear, performer, linformer]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Linear Attention, Performer, Linformer]
---

# 13 - Linear Attention (Performer, Linformer)

> [!info] TL;DR
> Linear attention approximates the $O(n^2)$ attention with $O(n)$ or $O(n \cdot k)$ compute by replacing the softmax kernel with a decomposable one or by low-rank projection. Performer (2020) and Linformer (2020) are the main variants. Largely superseded by FlashAttention in practice, but the ideas influence modern SSMs.

## The Idea

Standard attention:

$$
\text{Attn}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V
$$

The $Q K^T$ and the softmax-weighted $V$ multiplication are both $O(n^2 d)$. If we could **decompose** the softmax into a feature map $\phi$ such that $\text{softmax}(QK^T) \approx \phi(Q) \phi(K)^T$, we could rearrange:

$$
\text{softmax}(QK^T) V \approx \phi(Q) \big(\phi(K)^T V\big)
$$

Now $\phi(K)^T V$ is $d \times d$ — independent of $n$. Multiplying by $\phi(Q)$ gives $O(n \cdot d^2)$ — **linear in $n$**.

## Performer (Choromanski et al. 2020)

Performer uses **random Fourier features** (RFF) to approximate the softmax kernel:

$$
\phi(\mathbf{x}) = \frac{1}{\sqrt{m}} \exp\left(-\frac{\|\mathbf{x}\|^2}{2}\right) \left[\exp(\mathbf{\omega}_1 \cdot \mathbf{x}), \ldots, \exp(\mathbf{\omega}_m \cdot \mathbf{x})\right]
$$

where $\mathbf{\omega}_i$ are random Gaussian vectors. As $m \to \infty$, $\phi(Q) \phi(K)^T$ converges to the true softmax kernel.

### Pros
- $O(n \cdot m \cdot d)$ compute, $m$ is the feature dimension.
- Unbiased approximation.
- Works for any softmax-based attention.

### Cons
- Approximation error — quality is slightly worse than full attention.
- The $m$ needed for good approximation grows with $d$.
- In practice, FlashAttention often beats Performer because the constants are smaller.

## Linformer (Wang et al. 2020)

Linformer takes a different approach: project $K$ and $V$ along the **sequence dimension** to a fixed low rank:

$$
\tilde{K} = E K \quad \text{where } E \in \mathbb{R}^{k \times n}
$$
$$
\tilde{V} = F V \quad \text{where } F \in \mathbb{R}^{k \times n}
$$

Now $Q \tilde{K}^T$ is $n \times k$ instead of $n \times n$. For $k \ll n$, this is $O(n \cdot k \cdot d)$ — linear in $n$.

### Pros
- Simple and fast.
- The projections $E, F$ can be learned or fixed (random).

### Cons
- **Loses position-dependent structure** — the projection mixes positions, breaking the model's ability to attend to specific positions.
- Quality is worse than full attention for tasks needing precise position information.
- Not extrapolatable — fixed $k$ means the model can't handle sequences longer than $n$.

## Why Linear Attention Lost to FlashAttention

In 2020, linear attention was the most promising path to long context. By 2022, FlashAttention changed the calculus:

- FlashAttention is **exact** — no approximation, no quality loss.
- FlashAttention's constants are small — for typical $n$ (4k–128k), it's faster than linear attention.
- Linear attention requires choosing $m$ or $k$ — for high enough quality, you need $m, k \approx n$, defeating the purpose.

So linear attention is now mostly of **historical / theoretical interest**. The ideas survive in modified forms:

## Linear Attention's Legacy: SSMs and Mamba

The "decompose the kernel, rearrange the multiplication" idea reappears in **state space models** (S4, Mamba):

- Mamba computes a linear-attention-like recurrence but with **selective** gating (input-dependent), which fixes the quality issues.
- The state-space formulation enables $O(n)$ training (parallel scan) and $O(1)$ inference per token (vs $O(n)$ for attention's KV cache).

So linear attention is the conceptual ancestor of modern SSMs. See [[24 - Research Frontiers/State Space Models/Mamba|Mamba]] (planned).

## Worked Example (Conceptual Performer)

```python
def performer_attention(Q, K, V, n_features=256):
    """Simplified Performer with random Fourier features."""
    d = Q.size(-1)
    omega = torch.randn(n_features, d) / math.sqrt(d)
    
    # Feature map
    def phi(x):
        # (B, n, d) → (B, n, m)
        return F.softmax(torch.exp(x @ omega.T / math.sqrt(d)) - 0.5 * (x ** 2).sum(-1, keepdim=True), dim=-1)
    
    phi_Q = phi(Q)
    phi_K = phi(K)
    
    # Linear attention: phi(Q) @ (phi(K)^T @ V)
    K_V = phi_K.transpose(-2, -1) @ V  # (B, m, d)
    return phi_Q @ K_V  # (B, n, d)
```

## Why This Matters for AI

- Linear attention is the **conceptual bridge** between Transformers and SSMs. Understanding it helps you understand why Mamba works.
- For **streaming applications** where $n$ grows indefinitely (online ASR, real-time transcription), linear attention's $O(n)$ is genuinely valuable — full attention can't keep up.
- For most production use cases in 2026, **FlashAttention with full attention is the right choice**. Linear attention is niche.

## Production Implications

- Don't use Performer or Linformer in production — FlashAttention is better in almost all cases.
- Watch for **Mamba / hybrid models** if you need linear-time sequence modeling — they're the modern successors.
- For extreme long-context (>10M tokens), linear attention or hybrid attention may be necessary.

## Common Pitfalls

- **Treating linear attention as equivalent to full attention** — quality differences matter for some tasks.
- **Forgetting that Linformer's projection breaks position info** — bad for tasks needing precise position.
- **Using too-small feature dimension** — quality degrades silently.
- **Comparing FLOPs without measuring wall-clock** — linear attention's smaller FLOPs often don't translate to wall-clock wins because of constants.

## Further Reading

- Choromanski et al. (2020), *Rethinking Attention with Performers*.
- Wang et al. (2020), *Linformer: Self-Attention with Linear Complexity*.
- Katharopoulos et al. (2020), *Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention*.

## See Also

- [[11 - FlashAttention]]
- [[12 - Sparse Attention]]
- [[24 - Research Frontiers/State Space Models/Mamba|Mamba]] (planned)
- [[06 - Attention Mechanisms/MOC|Attention MOC]]

## The Kernel Trick — Mathematical Detail

Standard attention: $\text{Attn}(Q, K, V) = \text{softmax}(QK^T / \sqrt{d}) V$. The softmax makes this $O(n^2)$ — you need the full $n \times n$ matrix before normalization.

Linear attention replaces softmax with a **decomposable kernel** $\phi$:

$$\text{Attn}(Q, K, V) = \phi(Q) (\phi(K)^T V)$$

Now $\phi(K)^T V$ is $d \times d$ — independent of $n$. Multiplying by $\phi(Q)$ gives $O(n \cdot d^2)$ — **linear in $n$** for $d \ll n$.

### The catch: approximation quality

The kernel $\phi$ must approximate the softmax kernel $\exp(q \cdot k)$. Performer uses random Fourier features (RFF):

$$\phi(x) = \frac{1}{\sqrt{m}} \exp\left(-\frac{\|x\|^2}{2}\right) [\exp(\omega_1 \cdot x), \ldots, \exp(\omega_m \cdot x)]$$

where $\omega_i$ are random Gaussian vectors. As $m \to \infty$, $\phi(Q)\phi(K)^T \to \exp(QK^T)$. But for finite $m$, there's approximation error. The $m$ needed for good quality grows with $d$ — so for typical LLM dims ($d = 4096$), you need $m \approx 4096$, which means the linear attention is $O(n \cdot d^2) = O(n \cdot 16M)$ — not better than full attention $O(n^2 \cdot d) = O(n^2 \cdot 4096)$ until $n > 4000$. And FlashAttention's constants are smaller. This is why linear attention lost.

## Linformer's Low-Rank Projection — Different Approach

Linformer takes a different approach: project $K$ and $V$ along the **sequence dimension** to a fixed low rank:

$$\tilde{K} = E K, \quad \tilde{V} = F V$$

where $E, F \in \mathbb{R}^{k \times n}$. Now $Q \tilde{K}^T$ is $n \times k$ instead of $n \times n$. For $k \ll n$, this is $O(n \cdot k \cdot d)$ — linear in $n$.

### The problem: position information loss

The projections $E, F$ mix positions — the model loses the ability to attend to specific positions. For tasks needing precise position information (e.g., "attend to the 5th token"), Linformer is worse than full attention. For tasks where global patterns suffice (e.g., document classification), Linformer is fine.

### Non-extrapolatable

$k$ is fixed at training time. At inference with $n > n_{\text{train}}$, the projection matrices $E, F$ are undefined. This is worse than RoPE (which extrapolates with YaRN) and limits Linformer's applicability.

## Linear Attention's Legacy: Mamba and SSMs

The "decompose the kernel, rearrange the multiplication" idea reappears in **state space models** (S4, Mamba):

- Mamba computes a linear-attention-like recurrence but with **selective** gating (input-dependent), which fixes the quality issues.
- The state-space formulation enables $O(n)$ training (parallel scan) and $O(1)$ inference per token (vs $O(n)$ for attention's KV cache).

So linear attention is the conceptual ancestor of modern SSMs. The key insight — decompose the kernel to avoid the $n^2$ cost — is preserved; the difference is that Mamba adds selectivity (input-dependent gating) which linear attention lacks. See [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs Mamba and Frontiers]].

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Quality worse than full attention | Approximation error in $\phi$; or $k$ too small | Increase $m$ (Performer) or $k$ (Linformer); or use full attention + FA |
| Position information lost | Linformer's projection mixes positions | Use Performer (preserves position); or use full attention |
| Can't extrapolate | Linformer's fixed $k$ | Use RoPE + YaRN for extrapolation |
| Slower than expected | Constants are large; FA is faster | Benchmark against FA; don't assume linear is faster |

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Efficient Attention/11 - FlashAttention|FlashAttention]] — what replaced linear attention.
- [[06 - Attention Mechanisms/Efficient Attention/12 - Sparse Attention|Sparse Attention]] — alternative efficiency approach.
- [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs Mamba and Frontiers]] — the modern successor.
- [[24 - Research Frontiers/Hybrid Architectures/03 - RWKV and RetNet|RWKV and RetNet]] — linear-attention-like modern architectures.
- [[26 - Papers/2024-2026/43 - MiniMax-01 2025|MiniMax-01 2025]] — linear attention in production.
- [[26 - Papers/2024-2026/41 - Jamba 2024|Jamba 2024]] — hybrid with linear-time component.

## Interview Questions

1. **Q: How does linear attention reduce the $O(n^2)$ cost to $O(n)$?**
   A: Standard attention computes $\text{softmax}(QK^T)V$ — the softmax requires the full $n \times n$ matrix. Linear attention replaces softmax with a decomposable kernel $\phi$: $\text{Attn} = \phi(Q)(\phi(K)^T V)$. Now $\phi(K)^T V$ is $d \times d$ (independent of $n$), and multiplying by $\phi(Q)$ gives $O(n \cdot d^2)$ — linear in $n$ for $d \ll n$. The catch: the kernel $\phi$ must approximate softmax, and for good quality you need $m \approx d$, so the speedup only kicks in for $n > d^2 / d = d$. For typical LLM dims ($d = 4096$), that's $n > 4096$.

2. **Q: Why did linear attention lose to FlashAttention?**
   A: Three reasons. (1) **Approximation error** — linear attention approximates softmax; quality is slightly worse. (2) **Constants matter** — for the $m$ needed for good quality, linear attention's $O(n \cdot m \cdot d)$ isn't faster than FA's $O(n^2 \cdot d)$ until $n > m$, which is often $n > 4096$. (3) **FA is exact** — no approximation, no quality loss. FA made full attention cheap enough that the linear approximation wasn't worth the quality loss. Linear attention survives in Mamba/SSMs (which add selectivity) and in MiniMax-01 (hybrid linear + softmax).

3. **Q: How does linear attention relate to Mamba and state space models?**
   A: Mamba is the modern successor of linear attention. The key idea — decompose the kernel to avoid $n^2$ — is preserved. The difference: Mamba adds **selective gating** (input-dependent $B, C$ matrices), which linear attention lacks. This selectivity is what makes Mamba match Transformer quality — linear attention without selectivity is too weak. Mamba also uses a parallel scan for $O(n)$ training and $O(1)$ inference per token. Conceptually, Mamba is "linear attention + selectivity + hardware-efficient scan". See [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs Mamba and Frontiers]].

## See Also

- [[11 - FlashAttention]]
- [[12 - Sparse Attention]]
- [[24 - Research Frontiers/State Space Models/Mamba|Mamba]] (planned)
- [[06 - Attention Mechanisms/MOC|Attention MOC]]
