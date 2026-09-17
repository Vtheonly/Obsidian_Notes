---
tags: [attention, self-attention, scaled-dot-product, transformer]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Self-Attention, Scaled Dot-product Attention, QKV Attention]
---

# Self-Attention

> [!info] TL;DR
> Self-attention is the heart of the Transformer. Each token's representation is recomputed as a weighted average of all tokens' value vectors, where the weights come from the dot-product similarity between its query and each key. This note derives the formula, explains every term, shows why scaling by √d_k is essential, provides full implementation, discusses what attention learns, complexity analysis, comparisons to alternatives, and the role across the AI stack.

## The Formula

For an input sequence $\mathbf{X} \in \mathbb{R}^{n \times d}$ (n tokens, d dimensions), self-attention computes:

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V
$$

where:
- $Q = \mathbf{X} \mathbf{W}_Q \in \mathbb{R}^{n \times d_k}$ — **queries**
- $K = \mathbf{X} \mathbf{W}_K \in \mathbb{R}^{n \times d_k}$ — **keys**
- $V = \mathbf{X} \mathbf{W}_V \in \mathbb{R}^{n \times d_v}$ — **values**

$\mathbf{W}_Q, \mathbf{W}_K, \mathbf{W}_V$ are learned projection matrices. In most Transformers $d_k = d_v = d / h$ where $h$ is the number of heads; see [[05 - Multi-Head Attention]].

The output has shape $\mathbb{R}^{n \times d_v}$ — same number of tokens as input, but each token's representation is now a mixture of all tokens' value vectors.

## Intuition

Think of self-attention as **soft database lookup**:

- **Query** ($Q$): "what am I looking for?"
- **Keys** ($K$): "what do I have?"
- **Values** ($V$): "what do I return if matched?"

Each token issues a query. Every token (including itself) has a key. The dot product $Q K^T$ measures how much each token's key matches each token's query. Softmax normalizes these into weights. The weighted sum of values becomes the new representation of each token.

The crucial difference from a real database: it's **soft** — every value contributes, just with different weights. This makes it differentiable and learnable.

### Why Three Different Projections?

Why not just use $\mathbf{X}$ directly as Q, K, V? Because the three projections let the model learn different "views" of the same input:

- $Q = \mathbf{X} \mathbf{W}_Q$: what this token is *looking for* in other tokens.
- $K = \mathbf{X} \mathbf{W}_K$: what this token is *advertising* to other tokens.
- $V = \mathbf{X} \mathbf{W}_V$: what this token *contributes* when attended to.

Without these projections, attention would be a fixed function of $\mathbf{X}$ — no learned parameters, no adaptability. The projections give the model 3$d^2$ learnable parameters per attention layer, which is where most of the attention's expressivity comes from.

### The "Self" in Self-Attention

In **self-attention**, $Q$, $K$, and $V$ all come from the **same** sequence $\mathbf{X}$. The tokens attend to each other. This is the standard attention in encoder layers and decoder layers.

In **cross-attention** (encoder-decoder attention), $Q$ comes from one sequence (e.g., the decoder) and $K, V$ from another (e.g., the encoder). Used in encoder-decoder models like T5 and BART, and in multimodal models (LLaVA: decoder queries attend to vision encoder's K, V).

In **masked self-attention** (causal self-attention), $Q$, $K$, $V$ come from the same sequence, but a causal mask prevents token $i$ from attending to tokens $j > i$. Used in decoder-only LLMs (GPT, Llama, Mistral).

## Step-by-Step Derivation

### Step 1: Project to Q, K, V

Given input $\mathbf{X} \in \mathbb{R}^{n \times d}$, project to three matrices:

$$
Q = \mathbf{X} \mathbf{W}_Q, \quad K = \mathbf{X} \mathbf{W}_K, \quad V = \mathbf{X} \mathbf{W}_V
$$

These projections let the model learn different "views" of the same input — what to look for (Q), what to advertise (K), and what to return (V).

Each projection is a linear layer (matrix multiplication). In PyTorch: `nn.Linear(d, d_k, bias=False)`.

### Step 2: Compute similarities

$Q K^T \in \mathbb{R}^{n \times n}$ is a matrix of dot products. Entry $(i, j)$ is the similarity between token $i$'s query and token $j$'s key.

$$
(Q K^T)_{ij} = \sum_{k=1}^{d_k} Q_{ik} K_{jk} = \mathbf{q}_i \cdot \mathbf{k}_j
$$

This is the "compatibility matrix" — how much each query wants to attend to each key. The diagonal entries ($i = j$) are self-similarity (a token attending to itself).

### Step 3: Scale

Divide by $\sqrt{d_k}$:

$$
S = \frac{Q K^T}{\sqrt{d_k}}
$$

**Why scale?** See the dedicated section below — this is the most important detail in self-attention.

### Step 4: (Optional) Apply Mask

For causal attention (decoder), apply a lower-triangular mask:

$$
S_{ij} = \begin{cases} S_{ij} & \text{if } j \leq i \\ -\infty & \text{if } j > i \end{cases}
$$

This prevents token $i$ from attending to future tokens. For padding, mask positions where the input is a `<PAD>` token.

### Step 5: Softmax

Apply softmax row-wise (each row of $S$ becomes a probability distribution over tokens):

$$
A = \text{softmax}(S) \quad \text{where} \quad A_{ij} = \frac{\exp(S_{ij})}{\sum_k \exp(S_{ik})}
$$

$A$ is the **attention weight matrix**. Each row sums to 1. Entry $A_{ij}$ is the probability that token $i$ attends to token $j$.

### Step 6: Weighted average of values

$$
\text{Output} = A V
$$

The output is $\mathbb{R}^{n \times d_v}$ — same shape as $V$. Each output token is a convex combination of all value vectors, weighted by attention:

$$
\text{Output}_i = \sum_{j=1}^{n} A_{ij} \mathbf{v}_j
$$

Token $i$'s new representation is a weighted average of all tokens' value vectors, with weights from the attention matrix.

### Why Convex Combination?

Because softmax outputs are non-negative and sum to 1, the output is a **convex combination** of value vectors. This has nice properties:

- The output stays in the convex hull of the value vectors (no extrapolation).
- The output magnitude is bounded by the max value magnitude.
- The gradient flows cleanly through the softmax weights.

## Why Scale by √d_k?

This is the most important detail in self-attention. Without it, training is unstable for any non-trivial $d_k$.

### The problem

For random $\mathbf{q}, \mathbf{k} \in \mathbb{R}^{d_k}$ with mean 0, variance 1, the dot product $\mathbf{q} \cdot \mathbf{k} = \sum_{i=1}^{d_k} q_i k_i$ has:

- Mean 0
- **Variance $d_k$** (sum of $d_k$ terms, each with variance 1; assuming independence)

So the **standard deviation of the dot product grows as $\sqrt{d_k}$**.

### The consequence

For large $d_k$ (e.g., 64 or 128), the dot products can be large in magnitude. Softmax then saturates: one entry becomes ≈1, all others ≈0. This creates:

1. **Vanishing gradients** — softmax's gradient is $\approx 0$ when saturated.
2. **Sharp attention** — the model can't learn soft patterns; it's forced into argmax-like behavior.
3. **Training instability** — small changes in input produce large changes in attention weights.

### The fix

Divide by $\sqrt{d_k}$ to bring the standard deviation back to 1:

$$
\text{Var}\left(\frac{\mathbf{q} \cdot \mathbf{k}}{\sqrt{d_k}}\right) = \frac{d_k}{d_k} = 1
$$

This keeps softmax in its "nice" regime (non-saturated, well-conditioned gradients) regardless of dimension.

### Worked example

For $d_k = 64$:
- Without scaling: typical dot product magnitude $\approx \sqrt{64} = 8$.
- With $\sqrt{d_k}$ scaling: typical dot product magnitude $\approx 1$.
- After softmax on logits $\sim (8, 4, -2, ...)$ vs $(1, 0.5, -0.25, ...)$ — the unscaled version saturates much more.

For $d_k = 128$ (typical for Llama 3): dot products can reach ~11 without scaling. After softmax of `(11, 5, 2, ...)`: the top entry gets $\exp(11) / (\exp(11) + \exp(5) + ...) \approx 1.0$. The model can't distinguish between moderately-relevant and irrelevant tokens.

### Derivation: Why Variance Grows as d_k

Each term $q_i k_i$ is the product of two independent standard normal random variables. The variance of the product of two independent standard normals is 1 (since $\mathbb{E}[q_i^2 k_i^2] = \mathbb{E}[q_i^2] \mathbb{E}[k_i^2] = 1$). Summing $d_k$ independent such terms gives variance $d_k$ (variance of sum of independent random variables is the sum of variances).

So the standard deviation is $\sqrt{d_k}$. Dividing by $\sqrt{d_k}$ gives standard deviation 1.

## Computational Complexity

For sequence length $n$ and head dimension $d_k$:

| Step                | FLOPs               | Memory                |
|---------------------|---------------------|-----------------------|
| $Q, K, V$ projection| $3 \cdot n \cdot d \cdot d_k$ | $3 \cdot n \cdot d_k$ |
| $Q K^T$             | $n^2 \cdot d_k$     | $n^2$                 |
| Softmax             | $O(n^2)$            | $n^2$                 |
| $A V$               | $n^2 \cdot d_v$     | $n \cdot d_v$         |

The **$O(n^2)$ terms** are the bottleneck — both compute and memory scale quadratically with sequence length. This is why long-context is hard. See [[06 - Attention Mechanisms/MOC|Efficient Attention]] for the family of solutions.

### Concrete Numbers

For Llama 3 8B at sequence length 8192, head dim 128, 32 heads, 32 layers:
- Per head, per layer: $8192^2 = 67M$ attention scores.
- Per layer (32 heads): $32 \times 67M = 2.1B$ scores.
- All layers (32): $32 \times 2.1B = 68B$ scores.
- At 4 bytes (FP32): 272 GB of attention scores per forward pass.

Without FlashAttention (which avoids materializing this matrix), this would OOM any GPU. FlashAttention fuses the computation, keeping memory at $O(n)$ instead of $O(n^2)$.

### The Quadratic Bottleneck

The $O(n^2)$ scaling is the fundamental limitation of standard attention. Doubling the context length quadruples the attention cost. This is why:

- **Pre-2022 LLMs** had 2K-4K context: $O(n^2)$ at 4K = 16M scores per head per layer.
- **2023 LLMs** (Llama 2, GPT-4) extended to 32K-128K via FlashAttention and RoPE scaling.
- **2024-2026 LLMs** (Gemini 1.5 Pro, Claude 3.5) reach 200K-2M context via Ring Attention, hybrid architectures, and aggressive optimization.
- **Long-context research** (Mamba, Hyena, linear attention) aims to break $O(n^2)$ entirely.

## Implementation (PyTorch)

### Basic Implementation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, d_model, d_k=None):
        super().__init__()
        d_k = d_k or d_model
        self.W_q = nn.Linear(d_model, d_k, bias=False)
        self.W_k = nn.Linear(d_model, d_k, bias=False)
        self.W_v = nn.Linear(d_model, d_k, bias=False)
        self.scale = d_k ** -0.5
    
    def forward(self, x, mask=None):
        Q = self.W_q(x)  # (batch, n, d_k)
        K = self.W_k(x)
        V = self.W_v(x)
        
        # (batch, n, d_k) @ (batch, d_k, n) -> (batch, n, n)
        scores = Q @ K.transpose(-2, -1) * self.scale
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        attn = F.softmax(scores, dim=-1)
        out = attn @ V  # (batch, n, d_k)
        return out, attn
```

### Causal Masking (for decoder-only LLMs)

To prevent token $i$ from attending to tokens $j > i$ (i.e., enforce autoregressive generation), apply a causal mask:

```python
n = x.size(1)
mask = torch.tril(torch.ones(n, n, device=x.device, dtype=torch.bool))  # lower triangle = True
scores = scores.masked_fill(~mask, float('-inf'))
```

After softmax, masked positions have weight 0 — token $i$ only attends to tokens $\leq i$.

### With GQA (Grouped-Query Attention)

Modern LLMs use GQA, where multiple query heads share a single K, V pair. This reduces KV cache size:

```python
class GQASelfAttention(nn.Module):
    def __init__(self, d_model, n_heads, n_kv_heads):
        super().__init__()
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.n_rep = n_heads // n_kv_heads  # how many query heads per KV head
        self.head_dim = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, n_heads * self.head_dim, bias=False)
        self.W_k = nn.Linear(d_model, n_kv_heads * self.head_dim, bias=False)
        self.W_v = nn.Linear(d_model, n_kv_heads * self.head_dim, bias=False)
        self.W_o = nn.Linear(n_heads * self.head_dim, d_model, bias=False)
    
    def forward(self, x):
        B, T, D = x.shape
        Q = self.W_q(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        K = self.W_k(x).view(B, T, self.n_kv_heads, self.head_dim).transpose(1, 2)
        V = self.W_v(x).view(B, T, self.n_kv_heads, self.head_dim).transpose(1, 2)
        
        # Repeat K, V to match Q's head count
        K = K.repeat_interleave(self.n_rep, dim=1)  # (B, n_heads, T, head_dim)
        V = V.repeat_interleave(self.n_rep, dim=1)
        
        scale = self.head_dim ** -0.5
        scores = (Q @ K.transpose(-2, -1)) * scale  # (B, n_heads, T, T)
        attn = F.softmax(scores, dim=-1)
        out = attn @ V  # (B, n_heads, T, head_dim)
        
        out = out.transpose(1, 2).contiguous().view(B, T, -1)
        return self.W_o(out)
```

### Using FlashAttention (Production)

For production, always use FlashAttention (or a similar fused implementation):

```python
# Using PyTorch's built-in scaled_dot_product_attention (uses FlashAttention-2)
out = F.scaled_dot_product_attention(
    Q, K, V,
    attn_mask=causal_mask,
    dropout_p=0.0,
    is_causal=True,  # for causal masking
)
```

This is 5-10× faster than the naive implementation and uses 5-10× less memory (no $n \times n$ matrix materialized).

## What Attention Actually Learns

Empirical studies (especially [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|mechanistic interpretability]]) have found attention heads specializing in:

- **Previous-token attention** — attend to the immediately preceding token. Common in early layers; helps with local context.
- **Induction heads** — attend to the previous occurrence of the current token, then to the token after it. Critical for in-context learning. Example: if the model has seen "Alice Bob Charlie Alice", an induction head helps it predict "Bob" after the second "Alice" by attending to the "Bob" that followed the first "Alice".
- **Syntactic heads** — attend to syntactic dependents (subject → verb, etc.). Found in middle layers.
- **Copy heads** — attend to a token to copy it verbatim to the output. Common in early layers of decoder models.
- **Long-range dependency heads** — attend across long distances (e.g., pronoun to antecedent).
- **Rare token heads** — attend to rare tokens, possibly for lookup.

These patterns emerge naturally during pretraining and are not explicitly supervised. See [[14 - Interpretability/MOC|Interpretability MOC]].

### Attention Pattern Visualization

Attention patterns can be visualized as heatmaps. Common patterns:

- **Diagonal**: token attends to itself (identity).
- **Sub-diagonal**: token attends to previous token (local context).
- **Off-diagonal bands**: token attends to tokens N positions back.
- **Vertical lines**: token attends to specific "anchor" tokens (e.g., punctuation, BOS).
- **Block structure**: tokens within a syntactic unit (clause, sentence) attend to each other.

These patterns are studied in mechanistic interpretability to understand what models actually compute.

## Comparison to Other Sequence Mixers

Self-attention isn't the only way to mix information across sequence positions. Alternatives:

| Sequence Mixer | Complexity | Strengths | Weaknesses |
|----------------|------------|-----------|------------|
| Self-attention | $O(n^2)$ | Content-based routing; flexible; interpretable | Quadratic cost; long-context hard |
| RNN/LSTM | $O(n)$ | Linear cost; recurrent state | Sequential (no parallelism); vanishing gradients |
| Convolution | $O(n \cdot k)$ | Local patterns; parallel | Fixed receptive field; not content-based |
| Mamba/SSM | $O(n)$ | Linear; selective; hardware-efficient | Less interpretable; newer (less mature) |
| Hyena (long conv) | $O(n \log n)$ | Sub-quadratic; FFT-efficient | Less flexible than attention |
| Linear attention | $O(n)$ | Linear; kernelized | Lower expressivity; quality drops |

Self-attention won because:

1. **Content-based routing**: attention weights depend on content, not just position. This is more flexible than convolution or RNN.
2. **Parallelism**: all positions can be computed in parallel (during training). RNNs are inherently sequential.
3. **Long-range dependencies**: any token can attend to any other in one step. RNNs need many steps.
4. **Empirical quality**: at scale, attention-based models consistently outperform alternatives.

The 2024-2026 trend is toward **hybrid architectures** (Mamba + attention, Jamba) that combine attention's flexibility with SSM's efficiency.

## Why This Matters for AI

Self-attention is the **single most important operation in modern AI**. Every LLM forward pass is dominated by self-attention + FFN computations. Understanding self-attention is non-negotiable for:

- Reading any Transformer paper.
- Debugging training or inference issues.
- Understanding modern architectural innovations (GQA, MLA, MoE, FlashAttention).
- Choosing inference optimizations (KV cache, PagedAttention, spec decoding).
- Understanding interpretability research (attention patterns, induction heads).

## Production Implications

- **The $O(n^2)$ cost is the dominant scaling concern**. At sequence length 8192, attention is ~67M scores per head per layer; at 128k, it's ~16B. This is what makes long-context expensive.
- **KV cache** is the inference optimization that makes autoregressive generation tractable. See [[02 - KV Cache Mechanics]].
- **FlashAttention** fuses the $Q K^T \rightarrow$ softmax $\rightarrow \times V$ computation into a single IO-aware kernel, avoiding materializing the $n \times n$ attention matrix in HBM. Critical for any modern LLM. See [[11 - FlashAttention]].
- **Causal masking** in production: precompute the mask once per sequence length; don't recompute per forward pass.
- **Attention quantization**: FP8 attention (Hopper+) doubles throughput. Needs careful scaling to avoid numerical issues.
- **Sliding window attention** (Mistral): for long contexts, attend only to a window of W previous tokens. $O(n \cdot W)$ instead of $O(n^2)$. Combined with global attention for full coverage.
- **Sparse attention**: attend to a subset of positions (Longformer, BigBird). Reduces cost but loses some expressivity.

## Common Pitfalls

- **Forgetting the scaling** — causes training instability, especially for larger $d_k$. Symptom: loss spikes early in training, then diverges.
- **Applying softmax over the wrong axis** — should be over the last axis (key dimension) so each query row sums to 1. Wrong axis = each key column sums to 1, which is meaningless.
- **Masking with 0 instead of -inf** — softmax of 0 still gives non-zero weight. Use `-inf` (or a very large negative number like -1e9 for fp16 safety).
- **Forgetting to apply the mask before softmax** — masking after softmax does nothing (the weights are already normalized).
- **Not using a fused implementation** — naive PyTorch is 5–10× slower than FlashAttention. Always use FlashAttention in production.
- **Wrong head dimension** — $d_k$ must divide $d_{model}$. For $d_{model} = 4096$ and 32 heads, $d_k = 128$. Off-by-one gives shape mismatch.
- **Numerical issues with FP16** — for large $d_k$, even scaled scores can overflow FP16. Use FP32 accumulation or BF16.
- **Attention sink** — early LLMs found that attention concentrates on the first token (BOS), even when it's irrelevant. This is the "attention sink" phenomenon. Fix: include dummy tokens that attention can "dump" into.
- **Forgetting the output projection** — after attention, multiply by $\mathbf{W}_O$ to mix heads. Forgetting this loses head combination.

## Worked Example: Attention on a Short Sequence

Consider the sentence "The cat sat on the mat" with 5 tokens. Suppose after embedding, each token is a 4-d vector:

```
Token embeddings (5 × 4):
The:  [1.0, 0.0, 0.5, 0.2]
cat:  [0.0, 1.0, 0.3, 0.1]
sat:  [0.2, 0.3, 1.0, 0.4]
on:   [0.1, 0.1, 0.2, 0.8]
the:  [1.0, 0.1, 0.4, 0.3]
mat:  [0.0, 0.8, 0.2, 0.5]
```

After Q, K, V projections (with learned weights), suppose:

```
Q (queries):
The:  [0.5, 0.1]   — "looking for noun-like context"
cat:  [0.8, 0.2]   — "looking for verb context"
...

K (keys):
The:  [0.3, 0.7]   — "I'm a determiner"
cat:  [0.9, 0.1]   — "I'm a noun"
...

V (values):
The:  [0.1, 0.0, 0.5, 0.0]
cat:  [0.0, 0.9, 0.0, 0.1]
...
```

For token "cat" (position 1), the attention scores (before softmax) are:

```
score(cat, The) = q_cat · k_The = 0.8*0.3 + 0.2*0.7 = 0.38
score(cat, cat) = q_cat · k_cat = 0.8*0.9 + 0.2*0.1 = 0.74
score(cat, sat) = q_cat · k_sat = ...
score(cat, on)  = ...
score(cat, the) = ...
score(cat, mat) = ...
```

After scaling by $\sqrt{d_k} = \sqrt{2}$, softmax, and weighted sum of V, "cat"'s new representation mixes its own value with the values of related tokens (likely "The" and "sat"). The output reflects the context "The cat sat" rather than just "cat" in isolation.

## Interview Questions

- **Q: Why do we scale by $\sqrt{d_k}$ and not $d_k$?**  
  A: The dot product of two random unit-variance vectors has standard deviation $\sqrt{d_k}$. Dividing by $\sqrt{d_k}$ brings the standard deviation back to 1, keeping softmax in its non-saturated regime. Dividing by $d_k$ would over-suppress, making attention too uniform.

- **Q: What happens if you forget the causal mask in a decoder-only model?**  
  A: The model can "see" future tokens during training, learning to copy them rather than predict. Training loss drops to near zero, but the model produces gibberish at inference (when future tokens aren't available).

- **Q: Why does attention have $O(n^2)$ complexity?**  
  A: The $Q K^T$ matrix has shape $n \times n$ — every query must be compared to every key. This is the fundamental cost. Reducing it requires approximations (sparse attention, linear attention, FlashAttention's memory optimization).

- **Q: What's the difference between self-attention and cross-attention?**  
  A: In self-attention, Q, K, V all come from the same sequence. In cross-attention, Q comes from one sequence (e.g., decoder) and K, V from another (e.g., encoder). Cross-attention is used in encoder-decoder models and multimodal models.

- **Q: Why does GQA reduce KV cache size?**  
  A: With MHA, each of $h$ heads has its own K, V. With GQA, $n_{kv} < h$ heads share K, V. The KV cache is proportional to $n_{kv}$, so for $n_{kv} = h/4$ (Llama 3), the cache is 4× smaller.

- **Q: What is an induction head?**  
  A: An attention head that attends to the previous occurrence of the current token, then to the token after it. This enables in-context learning: if the model sees "A B C A", an induction head helps predict "B" after the second "A". Induction heads are critical for few-shot learning.

## Further Reading

- Vaswani et al. (2017), *Attention Is All You Need* — the original Transformer paper, introduced scaled dot-product self-attention. See [[02 - Vaswani Attention Is All You Need 2017]].
- The Annotated Transformer (Harvard NLP) — line-by-line implementation.
- Karpathy's "Let's build GPT from scratch" video — best pedagogical treatment.
- Olsson et al. (2022), *In-context Learning and Induction Heads* — mechanistic interpretability of attention.
- Dao et al. (2022), *FlashAttention: Fast and Memory-Efficient Exact Attention* — the production implementation. See [[08 - FlashAttention 2022]].

## See Also

- [[01 - Origins of Attention]]
- [[02 - Bahdanau Attention]]
- [[03 - Luong Attention]]
- [[05 - Multi-Head Attention]]
- [[14 - GQA MQA MLA]] — modern attention variants
- [[06 - Positional Encoding Overview]]
- [[08 - RoPE]] — positional encoding for modern LLMs
- [[01 - Transformer Block]] — where self-attention lives
- [[02 - KV Cache Mechanics]] — inference optimization
- [[11 - FlashAttention]] — fast attention kernel
- [[02 - Dot Product]] · [[04 - Matrix Multiplication]] · [[15 - Entropy Cross-Entropy KL]] — the math
- [[06 - Attention Mechanisms/MOC|Attention Mechanisms MOC]]
