---
tags: [attention, efficient-attention, sparse, longformer, bigbird]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Sparse Attention, Longformer, BigBird]
---

# 12 - Sparse Attention (Longformer, BigBird)

> [!info] TL;DR
> Sparse attention reduces the $O(n^2)$ cost of full attention by attending only to a subset of positions — typically local windows plus a few global tokens. Longformer (2020) and BigBird (2020) are the canonical variants. Enables $O(n \sqrt{n})$ or $O(n)$ attention for long documents.

## The Problem: $O(n^2)$ Doesn't Scale

Full attention: every token attends to every other token. For seq_len = 16k, that's 256M attention scores per head per layer. For 128k, it's 16B. Memory and compute grow quadratically.

For long-document tasks (books, codebases, legal contracts), full attention is infeasible. **Sparse attention** reduces this by attending only to a structured subset of positions.

## The Local + Global Pattern

The most common sparse pattern:

```
Position:  0 1 2 3 4 5 6 7 8 9 ...
Token 0:   [global] X X X X X X X X X    ← attends to everything
Token 1:   X X X . . . . . . .          ← attends to local window
Token 2:   X X X X . . . . . .
Token 3:   . X X X X . . . . .
Token 4:   . . X X X X . . . .
...
Token 9:   . . . . . . . X X X
```

- **Local window**: each token attends to its $w$ neighbors on each side. Captures local context efficiently.
- **Global tokens**: a few designated tokens (e.g., `[CLS]`, the first token, or task-specific tokens) attend to everything and are attended to by everything. Provides long-range information flow.

This pattern gives $O(n \cdot w + n \cdot g)$ cost, where $w$ is window size and $g$ is global count — linear in $n$ for fixed $w, g$.

## Longformer (Beltagy et al. 2020)

Longformer uses **sliding window** attention plus **dilated sliding window** (skip positions, like dilated CNNs) plus optional global tokens.

- Window size: typically 512.
- Dilated windows in higher layers (larger receptive field).
- Global tokens for tasks like classification (`[CLS]`) or QA (question tokens).
- Achieves SOTA on long-document tasks at the time.

## BigBird (Zaheer et al. 2020)

BigBird's pattern: **local window + global tokens + random connections**.

```
Pattern:   local window  +  global  +  random
```

The **random** connections are critical for theoretical reasons — they ensure the attention graph is a "random graph" with good spectral properties, which BigBird proves approximates full attention in theoretical limits.

BigBird is also theoretically a universal approximator and Turing-complete (like full Transformer), unlike some sparser patterns.

## Block Sparse Attention (Mesh Transformer, etc.)

Block-sparse patterns divide the sequence into blocks and attend at block granularity. Some blocks are fully attended; others are skipped. The pattern can be fixed or learned.

Used in some long-context models (e.g., GPT-3 variants, some MoE models).

## Sparse Transformers (Child et al. 2019)

An earlier pattern that uses a combination of:
- Local windows.
- Strided patterns (attend every $k$-th token).
- Fixed column/row patterns.

Designed for image and audio generation (where long sequences are common).

## Why Sparse Attention Lost to FlashAttention + Long Context

In 2020, sparse attention was the only way to handle 16k+ context. By 2023, two things changed:

1. **FlashAttention** made full attention 4–10x cheaper. $O(n^2)$ became feasible for $n = 32k$ or even 128k.
2. **YaRN / NTK scaling** allowed RoPE models to extend context cheaply.

So modern LLMs (Llama 3 128k, Gemini 1.5 1M) use **full attention** with FlashAttention, not sparse attention. The $O(n^2)$ is manageable up to ~1M tokens with FlashAttention-3 and careful memory management.

## When Sparse Attention Still Wins

- **Extreme long context** (10M+ tokens): FlashAttention can't make $n^2$ tractable here.
- **Memory-constrained inference**: if you can't fit the KV cache, sparse patterns reduce it.
- **Specific structured data** (e.g., DNA sequences, where locality is strong).

For most 2026 use cases, **full attention + FlashAttention is preferred**. Sparse attention is a research area, not the default.

## Worked Example (Longformer-style)

```python
import torch.nn.functional as F

def sliding_window_attention(Q, K, V, window_size, is_causal=True):
    """Simplified sliding window attention. Real implementations use custom CUDA kernels."""
    B, H, N, D = Q.shape
    # Create a mask: token i attends to j if |i - j| <= window_size
    positions = torch.arange(N, device=Q.device)
    mask = (positions[None, :] - positions[:, None]).abs() <= window_size
    if is_causal:
        mask = mask & (positions[None, :] <= positions[:, None])
    mask = mask.unsqueeze(0).unsqueeze(0)  # (1, 1, N, N)
    
    scores = Q @ K.transpose(-2, -1) / math.sqrt(D)
    scores = scores.masked_fill(~mask, float('-inf'))
    attn = F.softmax(scores, dim=-1)
    return attn @ V
```

In practice, use Longformer / BigBird implementations from HuggingFace or the dedicated libraries.

## Why This Matters for AI

- Sparse attention is the **historical answer** to long context. Understanding it helps you read 2020-era papers and understand why modern LLMs do what they do.
- The **local + global pattern** recurs in modern forms: sliding window attention (Mistral), local + sink tokens (StreamingLLM), block-sparse patterns (Mamba hybrids).
- For **streaming / online applications**, sparse attention is still relevant — you can't attend to future tokens you haven't seen.

## Production Implications

- For most long-context use cases, **use a full-attention model** (Llama 3, Qwen, etc.) with FlashAttention. Don't use sparse-attention models unless you have a specific reason.
- For extreme long context (>1M), watch for sparse-attention models or hybrid architectures.
- For **streaming / online ASR**, sparse attention with a sliding window is appropriate.

## Common Pitfalls

- **Treating sparse attention as equivalent to full attention** — it's an approximation; quality can differ.
- **Wrong window size** — too small misses long-range deps; too large loses the efficiency benefit.
- **Forgetting the global tokens** — without them, information can't flow across the full sequence.
- **Incompatible with FlashAttention** — most sparse patterns can't use FlashAttention's tiled kernel (the pattern doesn't fit the tile structure). Some libraries have specialized sparse FlashAttention kernels.

## Further Reading

- Beltagy, Peters, Cohan (2020), *Longformer: The Long-Document Transformer*.
- Zaheer et al. (2020), *Big Bird: Transformers for Longer Sequences*.
- Child et al. (2019), *Generating Long Sequences with Sparse Transformers*.

## See Also

- [[11 - FlashAttention]]
- [[13 - Linear Attention]]
- [[15 - Sliding Window Attention]]
- [[06 - Attention Mechanisms/MOC|Attention MOC]]

## BigBird's Theoretical Guarantee — Why Random Connections Matter

BigBird's pattern is **local window + global tokens + random connections**. The random connections aren't just for empirical quality — they provide a theoretical guarantee. BigBird proves that this pattern is:

1. **A universal approximator**: can approximate any sequence-to-sequence function to arbitrary precision (like full Transformer).
2. **Turing complete**: can simulate any Turing machine (like full Transformer).
3. **A random graph with good spectral properties**: the random connections ensure the attention graph's eigenvalues are well-behaved, which is what makes it approximate full attention.

Without the random connections, local+global patterns (like Longformer without random) are NOT universal approximators — there exist functions they can't approximate. The random connections are theoretically essential, not just an empirical trick.

### Why this matters less in practice

In practice, BigBird's theoretical advantage doesn't translate to better quality than Longformer (which lacks random connections). The theoretical guarantee is about worst-case functions, not real-world text. This is why FlashAttention (which is exact, not approximate) replaced both — it gives full attention quality without the $O(n^2)$ cost.

## Why Sparse Attention Lost to FlashAttention

In 2020, sparse attention was the only way to handle 16K+ context. By 2022, two things changed:

1. **FlashAttention made full attention 4-10× cheaper**. $O(n^2)$ became feasible for $n = 32k$ or even 128k.
2. **YaRN/NTK scaling allowed RoPE models to extend context cheaply** without retraining.

Modern LLMs (Llama 3 128k, Gemini 1.5 1M) use **full attention + FlashAttention**, not sparse attention. The $O(n^2)$ is manageable up to ~1M tokens with FA3 and careful memory management.

### When sparse attention still wins

- **Extreme long context (10M+ tokens)**: FlashAttention can't make $n^2$ tractable here.
- **Memory-constrained inference**: if you can't fit the KV cache, sparse patterns reduce it.
- **Structured data** (DNA, where locality is strong).

For most 2026 use cases, **full attention + FlashAttention is preferred**. Sparse attention is a research area, not the default.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Quality worse than full attention | Sparse pattern too restrictive | Add more global tokens; or use full attention + FA |
| No long-range information flow | Missing global tokens | Always include a few global tokens (e.g., [CLS]) |
| Incompatible with FlashAttention | Sparse pattern doesn't fit tile structure | Use specialized sparse-FA kernels; or switch to full attention |

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Efficient Attention/11 - FlashAttention|FlashAttention]] — what replaced sparse attention.
- [[06 - Attention Mechanisms/Efficient Attention/13 - Linear Attention|Linear Attention]] — alternative efficiency approach.
- [[06 - Attention Mechanisms/Modern Attention/15 - Sliding Window Attention|Sliding Window Attention]] — modern local attention.
- [[24 - Research Frontiers/Long-Context/07 - Long-Context Architectures|Long-Context Architectures]].
- [[26 - Papers/Efficient Attention/18 - Longformer 2020|Longformer 2020]].
- [[26 - Papers/Efficient Attention/20 - BigBird 2020|BigBird 2020]].

## Interview Questions

1. **Q: Why does BigBird include random connections?**
   A: Theoretical guarantee. BigBird proves that local + global + random is a universal approximator and Turing complete. Without random connections, local+global patterns can't approximate all functions. The random connections ensure the attention graph has good spectral properties. In practice, this theoretical advantage doesn't translate to better quality than Longformer (which lacks random), which is why FlashAttention (exact) replaced both.

2. **Q: Why did sparse attention lose to FlashAttention?**
   A: Two changes in 2022. (1) FlashAttention made full attention 4-10× cheaper — $O(n^2)$ became feasible for 128K+. (2) YaRN/NTK scaling allowed RoPE models to extend context without retraining. Modern LLMs use full attention + FA, not sparse. Sparse still wins for extreme long context (10M+), memory-constrained inference, and structured data.

3. **Q: When would you use sparse attention in 2026?**
   A: Three cases. (1) **Extreme long context (10M+)** — FlashAttention can't make $n^2$ tractable. (2) **Memory-constrained inference** — sparse patterns reduce KV cache. (3) **Structured data** (DNA, where locality is strong). For most use cases (up to 1M tokens), full attention + FlashAttention is preferred.

## See Also

- [[11 - FlashAttention]]
- [[13 - Linear Attention]]
- [[15 - Sliding Window Attention]]
- [[06 - Attention Mechanisms/MOC|Attention MOC]]
