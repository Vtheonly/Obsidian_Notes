---
tags: [attention, multi-head, transformer]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Multi-Head Attention, MHA]
---

# Multi-Head Attention

> [!info] TL;DR
> Multi-Head Attention (MHA) runs $h$ parallel attention "heads", each with its own learned Q/K/V projections, and concatenates the results. Heads can specialize in different relations (syntax, coreference, induction, copy, etc.). MHA is the default attention in Transformers; modern variants include MQA, GQA, and MLA.

## Why Multiple Heads?

A single attention head computes **one** weighted average of value vectors. This is a limited operation — it can capture only one "kind" of relation at a time.

**Multi-Head Attention** runs $h$ parallel heads, each with its own Q/K/V projections:

$$
\text{head}_i = \text{Attention}(Q \mathbf{W}_Q^{(i)}, K \mathbf{W}_K^{(i)}, V \mathbf{W}_V^{(i)})
$$

$$
\text{MHA}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) \mathbf{W}_O
$$

Each head can learn to attend to a different aspect of the sequence — one head might attend to syntactic dependents, another to coreference, another to the previous token, etc. The output projection $\mathbf{W}_O$ mixes the heads back together.

## Dimensionality

To keep compute roughly constant when varying $h$, the per-head dimension is $d_k = d_{\text{model}} / h$. The original Transformer has $d_{\text{model}} = 512$, $h = 8$, $d_k = 64$.

- Each head's projections: $\mathbf{W}_Q^{(i)}, \mathbf{W}_K^{(i)} \in \mathbb{R}^{d_{\text{model}} \times d_k}$, $\mathbf{W}_V^{(i)} \in \mathbb{R}^{d_{\text{model}} \times d_v}$.
- Each head's output: $\mathbb{R}^{n \times d_v}$.
- Concatenated output: $\mathbb{R}^{n \times (h \cdot d_v)} = \mathbb{R}^{n \times d_{\text{model}}}$ (when $d_v = d_k = d_{\text{model}}/h$).
- Output projection: $\mathbf{W}_O \in \mathbb{R}^{d_{\text{model}} \times d_{\text{model}}}$.

In practice, all heads are computed in a single batched matmul — there's no per-head Python loop. The trick: project to a larger matrix and `reshape` to (batch, h, n, d_k).

## Implementation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_o   = nn.Linear(d_model, d_model, bias=False)
    
    def forward(self, x, mask=None):
        B, N, D = x.shape
        # Project to Q, K, V in one matmul, then reshape to (B, h, N, d_k)
        qkv = self.W_qkv(x)  # (B, N, 3*D)
        q, k, v = qkv.split(D, dim=-1)
        q = q.view(B, N, self.n_heads, self.d_k).transpose(1, 2)  # (B, h, N, d_k)
        k = k.view(B, N, self.n_heads, self.d_k).transpose(1, 2)
        v = v.view(B, N, self.n_heads, self.d_k).transpose(1, 2)
        
        # Scaled dot-product attention (per head, batched)
        scores = (q @ k.transpose(-2, -1)) * (self.d_k ** -0.5)  # (B, h, N, N)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        out = attn @ v  # (B, h, N, d_k)
        
        # Concat heads and project
        out = out.transpose(1, 2).contiguous().view(B, N, D)
        return self.W_o(out), attn
```

The single matmul for QKV projection and the batched per-head attention are crucial for GPU efficiency.

## Head Specialization

Empirical studies (see [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|mechanistic interpretability]]) show that heads specialize:

- **Previous-token heads** — always attend to position $t-1$.
- **Induction heads** — find previous occurrences of the current token, then attend to the token after. Critical for in-context learning.
- **Syntactic heads** — attend to syntactic heads (subject → verb).
- **Coreference heads** — attend to antecedents of pronouns.
- **Copy heads** — attend to a token to copy it verbatim.
- **Noise heads** — attend broadly and uniformly; seem to do "averaging".

Not all heads are useful — many can be pruned with minimal performance impact (see Voita et al., 2019). This observation motivates the modern variants below.

## Modern Variants

### MQA (Multi-Query Attention)

**Multi-Query Attention** (Shazeer, 2019) shares K and V across all heads; only Q is per-head. This dramatically reduces the size of the KV cache (the main memory cost at inference) at a small quality cost.

- KV cache size: $\frac{1}{h}$ of MHA.
- Used by: PaLM, Falcon, StarCoder.

### GQA (Grouped-Query Attention)

**Grouped-Query Attention** (Ainslie et al., 2023) is the intermediate point: $g$ groups of heads share K and V. $g=1$ is MQA; $g=h$ is MHA.

- KV cache size: $\frac{g}{h}$ of MHA.
- Best quality/speed tradeoff in practice.
- Used by: **Llama 2 (70B), Llama 3, Mistral 7B, Gemma, Qwen 2/3**, most modern LLMs.

### MLA (Multi-head Latent Attention)

**Multi-head Latent Attention** (DeepSeek, 2024) is more aggressive: it compresses K and V into a low-rank latent vector, then decompresses per-head. This can achieve KV cache sizes even smaller than MQA while maintaining MHA-like quality.

- Used by: **DeepSeek-V2, DeepSeek-V3**.
- See [[10 - Model Architecture Research/Open Source/DeepSeek|DeepSeek architecture]] (planned).

### Summary table

| Variant  | Q heads | K/V heads | KV cache (relative to MHA) | Quality | Used by                       |
|----------|---------|-----------|----------------------------|---------|-------------------------------|
| MHA      | h       | h         | 1.0                        | Best    | GPT-2/3, BERT, T5             |
| MQA      | h       | 1         | 1/h                        | Slightly worse | PaLM, Falcon, StarCoder |
| GQA      | h       | g         | g/h                        | Near-MHA | Llama 2/3, Mistral, Gemma   |
| MLA      | h       | (latent)  | << 1/h                     | MHA-like | DeepSeek-V2/V3               |

For a deep treatment of these variants, see planned [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA]] note.

## Why This Matters for AI

- MHA is the **default attention** in every Transformer since 2017. If you read any architecture paper, you need to understand it.
- The choice of MHA / MQA / GQA / MLA is one of the most consequential architectural decisions for **inference cost** (KV cache size). Llama 2/3 use GQA specifically to make consumer-GPU inference feasible.
- Head specialization is the basis of [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|mechanistic interpretability]] — understanding what individual heads do gives us insight into what the model has learned.
- Head pruning is a real production technique — you can prune 30–50% of heads with minimal quality loss, giving a free inference speedup.

## Production Implications

- **Always use FlashAttention** for MHA — it's 5–10x faster than naive attention.
- **GQA over MHA** for new model designs — the inference speedup is substantial and the quality loss is small.
- **Head pruning** can be applied post-hoc to existing models. Tools: `torch-pruning`, HuggingFace's `prune_heads`.
- **Quantize the KV cache** to INT8 or FP8 to halve memory. Critical for long-context inference.

## Common Pitfalls

- **Forgetting to reshape Q, K, V to (B, h, N, d_k)** — without the head dimension, you compute a single big attention instead of $h$ parallel ones.
- **Wrong concatenation order** — must be consistent with the head dimension split.
- **Treating all heads as equal** — they're not. Some are critical, some are noise. Don't prune blindly.
- **Forgetting the output projection** — concatenating heads without $\mathbf{W}_O$ loses information.

## Further Reading

- Vaswani et al. (2017), *Attention Is All You Need* — introduced MHA.
- Shazeer (2019), *Fast Transformer Decoding with One Write-Head* — MQA.
- Ainslie et al. (2023), *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*.
- Voita et al. (2019), *Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned*.
- DeepSeek-AI (2024), *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model* — MLA.

## See Also

- [[Self-Attention]]
- [[Transformer Block]]
- [[KV Cache Mechanics]]
- [[06 - Attention Mechanisms/MOC|Attention Mechanisms MOC]]
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] (planned)

## Why $d_k = d_{\text{model}} / h$ Keeps Compute Constant

The original Transformer has $d_{\text{model}} = 512$, $h = 8$ heads, $d_k = 64$. The total compute for MHA vs single-head attention with the same $d_{\text{model}}$:

- **Single-head** ($d_k = d_{\text{model}} = 512$): $Q K^T$ is $(N, 512) \times (512, N) = O(N^2 \cdot 512)$.
- **Multi-head** ($h = 8, d_k = 64$): 8 heads, each $Q_i K_i^T$ is $(N, 64) \times (64, N) = O(N^2 \cdot 64)$. Total: $8 \times O(N^2 \cdot 64) = O(N^2 \cdot 512)$. Same!

The trick: total dimension is preserved ($h \cdot d_k = d_{\text{model}}$), so compute is constant. But you get $h$ parallel attention patterns instead of one. The cost is slightly more parameters (the Q/K/V projections are $3 \times d_{\text{model}}^2$ regardless of $h$, but the output projection adds $d_{\text{model}}^2$).

## Head Specialization — What Heads Actually Learn

Empirical studies (Voita et al. 2019, Olsson et al. 2022) have identified specific head types in trained Transformers:

| Head type         | What it does                                          | Example                                          |
|-------------------|-------------------------------------------------------|--------------------------------------------------|
| Previous-token    | Always attends to position $t-1$                      | Helps with local context                         |
| Induction         | Finds previous occurrences of current token, attends to next token | Critical for in-context learning            |
| Syntactic         | Attends to syntactic heads (subject → verb)            | Parsing                                          |
| Coreference       | Attends to antecedents of pronouns                     | "it" → the noun it refers to                    |
| Copy              | Attends to a token to copy it verbatim                 | Repetition, quoting                              |
| Noise / redundant | Attends broadly and uniformly; seems to do averaging   | Can be pruned                                    |

### The induction head — key for in-context learning

An **induction head** (Olsson et al. 2022) is a two-head circuit that enables in-context learning:
1. Head 1 (previous-token): at position $t$, attends to $t-1$, copying its token ID into the residual stream.
2. Head 2 (induction): at position $t$, looks for previous occurrences of the token at $t-1$, then attends to the token *after* that occurrence.

This allows the model to complete patterns like "A B C ... A B → C" — it sees "A B" earlier, recognizes the pattern, and predicts "C". Induction heads emerge suddenly during training and are strongly correlated with in-context learning ability. See [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]].

### Head pruning

Many heads are redundant or noise. Voita et al. (2019) showed that 30-50% of heads can be pruned with minimal quality loss. The critical heads (induction, syntactic) must be kept; the rest are disposable. Head pruning is a real production technique for inference speedup. Tools: `torch-pruning`, HuggingFace's `prune_heads`.

## The Output Projection — Why It's Needed

After concatenating $h$ heads, you have a tensor of shape $(B, N, h \cdot d_k) = (B, N, d_{\text{model}})$. Naively, this is the output. But the concatenated heads haven't been mixed — each head's output is independent. The output projection $\mathbf{W}_O \in \mathbb{R}^{d_{\text{model}} \times d_{\text{model}}}$ mixes the heads:

$$
\text{MHA}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) \mathbf{W}_O
$$

Without $\mathbf{W}_O$, the heads can't share information. With it, the model can learn to combine head outputs in arbitrary ways. The output projection is essential — don't forget it.

## Worked Example: MHA with Causal Masking

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, max_seq_len=2048):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        # Fused QKV projection (more efficient than separate)
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.o = nn.Linear(d_model, d_model, bias=False)

        # Causal mask buffer (registered once)
        mask = torch.tril(torch.ones(max_seq_len, max_seq_len)).bool()
        self.register_buffer('causal_mask', mask.view(1, 1, max_seq_len, max_seq_len))

    def forward(self, x):
        B, N, D = x.shape
        # Fused QKV: (B, N, 3D) -> 3 × (B, N, D)
        qkv = self.qkv(x)
        q, k, v = qkv.split(D, dim=-1)

        # Reshape to (B, h, N, d_k)
        q = q.view(B, N, self.n_heads, self.d_k).transpose(1, 2)
        k = k.view(B, N, self.n_heads, self.d_k).transpose(1, 2)
        v = v.view(B, N, self.n_heads, self.d_k).transpose(1, 2)

        # Use PyTorch's SDPA (dispatches to FlashAttention when available)
        mask = self.causal_mask[:, :, :N, :N]
        out = F.scaled_dot_product_attention(q, k, v, attn_mask=mask, is_causal=True)

        # Concat heads and project
        out = out.transpose(1, 2).contiguous().view(B, N, D)
        return self.o(out)

# Test
mha = MultiHeadAttention(d_model=512, n_heads=8)
x = torch.randn(2, 128, 512)  # Batch 2, seq_len 128
out = mha(x)
print(f"Input: {x.shape}, Output: {out.shape}")  # Both (2, 128, 512)
print(f"Parameters: {sum(p.numel() for p in mha.parameters()):,}")  # ~1.05M (4 × 512²)
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Wrong output shape | Forgot to transpose head dim back before reshape | Ensure `(B, h, N, d_k)` → `(B, N, h, d_k)` via `.transpose(1, 2)` before `.view` |
| NaN in attention | Softmax over masked positions | Set masked positions to `-inf` before softmax; ensure at least one valid position |
| Slow attention (no FlashAttention) | Not using SDPA or `attn_implementation="flash_attention_2"` | Use `F.scaled_dot_product_attention` or set `attn_implementation` in HuggingFace |
| Head dim not multiple of 8 | Tensor Core underutilization | Choose `d_model` and `n_heads` so `d_k` is a multiple of 8 (or 16 for fp8) |
| All heads attend similarly | Insufficient training; or heads collapsed | Train longer; check init; reduce LR |

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] — the single-head version.
- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA / MQA / MLA]] — memory-efficient variants.
- [[07 - Transformers/Architecture/01 - Transformer Block|Transformer Block]] — where MHA lives.
- [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics|KV Cache Mechanics]] — MHA's memory cost at inference.
- [[13 - Inference/KV Cache/02 - PagedAttention|PagedAttention]] — efficient KV cache management.
- [[13 - Inference/Serving/06 - Continuous Batching Deep Dive|Continuous Batching]] — batching MHA across sequences.
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] — studying head specialization.
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017|Vaswani 2017]] — introduced MHA.
- [[26 - Papers/Efficient Attention/29 - GQA 2024|GQA 2024]] — the modern variant.

## Interview Questions

1. **Q: Why does MHA set $d_k = d_{\text{model}} / h$?**
   A: To keep compute constant when varying $h$. Single-head with $d_k = 512$: $O(N^2 \cdot 512)$. Multi-head with $h = 8, d_k = 64$: 8 heads × $O(N^2 \cdot 64) = O(N^2 \cdot 512)$. Same total compute, but 8 parallel attention patterns instead of 1. The trick: total dimension is preserved ($h \cdot d_k = d_{\text{model}}$). The cost is slightly more parameters (output projection adds $d_{\text{model}}^2$).

2. **Q: What is an induction head and why is it important?**
   A: An induction head (Olsson et al. 2022) is a two-head circuit that enables in-context learning. Head 1 (previous-token) copies the token ID from position $t-1$ into the residual stream. Head 2 (induction) looks for previous occurrences of the token at $t-1$, then attends to the token *after* that occurrence. This allows pattern completion: "A B C ... A B → C". Induction heads emerge suddenly during training and are strongly correlated with in-context learning ability. They're one of the best-understood circuits in Transformers.

3. **Q: Why is the output projection $\mathbf{W}_O$ needed?**
   A: After concatenating $h$ heads, you have $(B, N, h \cdot d_k) = (B, N, d_{\text{model}})$, but the heads haven't been mixed — each head's output is independent. $\mathbf{W}_O$ mixes the heads, letting the model learn to combine head outputs in arbitrary ways. Without it, heads can't share information, and the model loses expressive power. The output projection is essential — don't forget it.

4. **Q: How much can you prune heads without quality loss?**
   A: 30-50% of heads can be pruned with minimal quality loss (Voita et al. 2019). Critical heads (induction, syntactic, coreference) must be kept; noise/redundant heads can be removed. Head pruning is a real production technique for inference speedup. The approach: measure each head's importance (e.g., via L0 regularization or sensitivity analysis), prune the least important, fine-tune briefly to recover. Tools: `torch-pruning`, HuggingFace's `prune_heads`.

5. **Q: What's the difference between MHA, MQA, GQA, and MLA?**
   A: **MHA**: $h$ query heads, $h$ K/V heads. Best quality, most memory. Used by GPT-2/3, BERT, T5. **MQA** (Shazeer 2019): $h$ query heads, 1 K/V head. KV cache is $1/h$ of MHA. Slight quality loss. Used by PaLM, Falcon, StarCoder. **GQA** (Ainslie 2023): $h$ query heads, $g$ K/V heads (between MHA and MQA). Best quality/speed tradeoff. Used by Llama 2/3, Mistral, Gemma, Qwen. **MLA** (DeepSeek 2024): compresses K/V into a low-rank latent vector, then decompresses per-head. KV cache smaller than MQA, MHA-like quality. Used by DeepSeek-V2/V3.

6. **Q: How would you implement MHA efficiently in PyTorch?**
   A: Three key optimizations: (1) **Fused QKV projection** — one `nn.Linear(d_model, 3*d_model)` instead of three separate linears. Saves kernel launches. (2) **Single reshape + transpose** — `q.view(B, N, h, d_k).transpose(1, 2)` produces `(B, h, N, d_k)` in one operation. (3) **Use `F.scaled_dot_product_attention`** (SDPA) — dispatches to FlashAttention when available, handling masking, scaling, and the softmax in a fused kernel. Never write `softmax(Q @ K.T / sqrt(d)) @ V` manually in production.

## See Also

- [[Self-Attention]]
- [[Transformer Block]]
- [[KV Cache Mechanics]]
- [[06 - Attention Mechanisms/MOC|Attention Mechanisms MOC]]
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] (planned)
