---
tags: [attention, positional-encoding, rope, sinusoidal]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Positional Encoding Overview]
---

# Positional Encoding Overview

> [!info] TL;DR
> Self-attention is **permutation-invariant** — it doesn't know the order of tokens. Positional encoding injects order information. This note surveys the family: sinusoidal, learned, relative (Shaw, Transformer-XL), RoPE, ALiBi, YaRN. Deep dive on RoPE in [[RoPE]].

## The Problem

Self-attention computes:

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V
$$

If you permute the input tokens, you just permute the output rows — the attention weights are unchanged. This is **permutation invariance**: attention has no notion of order.

But language (and most sequence data) is order-dependent. "Dog bites man" and "Man bites dog" mean different things. We need to inject position information.

## Two Families of Solutions

### Absolute positional encoding

Add a position-dependent vector to each token's embedding:

$$
\mathbf{x}_i = \mathbf{e}_{\text{token}_i} + \mathbf{p}_i
$$

where $\mathbf{p}_i$ encodes position $i$. The model learns to use this signal.

### Relative positional encoding

Modify the attention computation to depend on the **relative offset** $i - j$ between query position $i$ and key position $j$. The model knows "key $j$ is 3 positions to the right of query $i$" rather than "key $j$ is at absolute position 5".

Relative encodings generalize better to longer sequences and are dominant in modern LLMs.

## The Major Variants

### 1. Sinusoidal (Vaswani et al., 2017)

The original Transformer uses fixed sinusoidal encoding:

$$
\mathbf{p}_{i, 2k} = \sin\left(\frac{i}{10000^{2k/d}}\right)
$$

$$
\mathbf{p}_{i, 2k+1} = \cos\left(\frac{i}{10000^{2k/d}}\right)
$$

Each dimension is a sine/cosine at a different frequency. The hope was that the model could learn to attend by relative position because $\sin(i + \delta)$ is a linear function of $\sin(i), \cos(i)$.

**Pros**: no learned parameters, theoretically extrapolates to longer sequences.
**Cons**: in practice, doesn't extrapolate well past training length.

### 2. Learned absolute positional embeddings (GPT-2, BERT)

Each position $i \in [0, L)$ has a learned embedding vector $\mathbf{p}_i \in \mathbb{R}^d$.

$$
\mathbf{x}_i = \mathbf{e}_{\text{token}_i} + \mathbf{p}_i
$$

**Pros**: simple, flexible.
**Cons**: hard limit on context length — position $i \geq L$ is undefined. Cannot extrapolate.

### 3. Shaw relative positional encoding (Shaw et al., 2018)

Instead of adding to the input, add a learned relative embedding to the keys (and sometimes values):

$$
\text{Attention}(Q, K + \mathbf{R}^{rel}, V)
$$

where $\mathbf{R}^{rel}$ depends on relative positions $i - j$. Clipped to a maximum relative distance (e.g., $|i - j| \leq 50$).

**Pros**: better generalization; the same embedding for relative distance 5 regardless of absolute position.
**Cons**: needs to be added at every attention layer (not just input); more memory.

### 4. Transformer-XL relative positional encoding (Dai et al., 2019)

Decomposes the attention score into four terms, each with a different relative-position component:

$$
e_{ij} = \underbrace{\mathbf{q}_i \cdot \mathbf{k}_j}_{\text{content-content}} + \underbrace{\mathbf{q}_i \cdot \mathbf{r}_{i-j}^K}_{\text{content-position}} + \underbrace{\mathbf{u} \cdot \mathbf{k}_j}_{\text{global content bias}} + \underbrace{\mathbf{v} \cdot \mathbf{r}_{i-j}^K}_{\text{global position bias}}
$$

where $\mathbf{r}_{i-j}^K$ is a learned relative embedding and $\mathbf{u}, \mathbf{v}$ are global parameters.

**Pros**: state-of-the-art for long-context LMs at the time; foundation for later work.
**Cons**: complex; many moving parts.

### 5. RoPE (Rotary Position Embedding) — Su et al., 2021

Rotates the query and key vectors in 2D subspaces by an angle proportional to position. The dot product then depends only on **relative** position (because rotating $\mathbf{q}$ by $\theta_i$ and $\mathbf{k}$ by $\theta_j$ is equivalent to rotating their dot product by $\theta_i - \theta_j$).

**Pros**: relative encoding that's also computationally free (just multiplies Q and K by rotation matrices). Generalizes to longer sequences with scaling tricks.
**Cons**: requires careful handling of the rotation; context extension needs YaRN or NTK-aware scaling.

**Used by**: Llama, Mistral, Gemma, Qwen, DeepSeek, GLM, and essentially all modern decoder LLMs.

See [[RoPE]] for the full treatment.

### 6. ALiBi (Attention with Linear Biases) — Press et al., 2022

Adds a fixed (non-learned) bias to attention scores that depends linearly on relative distance:

$$
e_{ij} = \mathbf{q}_i \cdot \mathbf{k}_j + m \cdot (j - i)
$$

where $m$ is a head-specific slope (geometrically spaced, e.g., $1/2, 1/4, 1/8, \ldots$).

**Pros**: no positional parameters at all; true extrapolation (trained on 1024 tokens, works on 2048+).
**Cons**: quality slightly below RoPE in practice; less adopted.

### 7. YaRN, NTK-aware scaling, LongRoPE

Methods to **extend** a RoPE-trained model to longer contexts without retraining. They modify the rotation frequencies so that the model can effectively "interpolate" to longer positions.

- **NTK-aware scaling**: scales the rotation frequencies so the highest-frequency rotations stay roughly the same.
- **YaRN** (Peng et al., 2023): a more sophisticated interpolation that segments the frequency range and applies different scaling per segment.
- **LongRoPE** (Microsoft, 2024): searches for non-uniform frequency scaling, achieving 2M-token context.

See planned [[YaRN]] note.

## Comparison Table

| Method              | Family    | Extrapolates? | Used by                          | Notes                          |
|---------------------|-----------|---------------|----------------------------------|--------------------------------|
| Sinusoidal          | Absolute  | Theoretically | Original Transformer             | Rarely used today              |
| Learned absolute    | Absolute  | No            | GPT-2, BERT                      | Hard context limit             |
| Shaw relative       | Relative  | To a limit    | Some early NMT                   | Clipped max distance           |
| Transformer-XL      | Relative  | Better        | Transformer-XL, some long-context| Complex                        |
| **RoPE**            | Relative  | With scaling  | **Llama, Mistral, Gemma, Qwen**  | Modern default                 |
| ALiBi               | Relative  | Yes (linear)  | MPT, BLOOM                       | Slightly lower quality         |
| YaRN                | RoPE ext  | Yes           | Used to extend RoPE models       | Training-free extension        |
| LongRoPE            | RoPE ext  | Yes (2M+)     | Microsoft models                 | Search-based                   |

## Why This Matters for AI

- Positional encoding is **the** mechanism that makes attention work for sequences. Without it, attention is just a set operation.
- The shift from absolute (GPT-2, BERT) to relative (RoPE) was one of the key architectural changes that enabled modern long-context LLMs.
- **Context extension** (YaRN, LongRoPE) is one of the most active research areas because users want longer contexts but retraining is expensive.
- The choice of positional encoding affects **what the model can do at inference**: a model trained with absolute embeddings genuinely cannot process positions past its training length; RoPE + scaling can extend 4–32x.

## Production Implications

- **For new model training**: use RoPE. It's the de-facto standard and has the best tooling.
- **For extending an existing model's context**: use YaRN or NTK-aware scaling. Both are training-free (or fine-tune-light) and well-supported in vLLM, TGI, etc.
- **For very long context (1M+)**: LongRoPE or progressive extension during fine-tuning. Production maturity is still developing.
- **Position embedding bugs** are subtle: a model with the wrong RoPE configuration will look fine on short sequences but degrade sharply on long ones. Always test on the maximum intended context length.

## Common Pitfalls

- **Mixing positional encodings** — never combine absolute embeddings with RoPE. They conflict.
- **Wrong RoPE base or scaling factor** — the model will produce plausible-looking but subtly wrong outputs.
- **Forgetting to apply causal mask AND positional encoding** — both are needed.
- **Truncating positions past training length** — for absolute encodings, you must train at the maximum intended length. For RoPE, you can extend with YaRN.

## Further Reading

- Vaswani et al. (2017), *Attention Is All You Need* — sinusoidal.
- Shaw et al. (2018), *Self-Attention with Relative Position Representations*.
- Dai et al. (2019), *Transformer-XL*.
- Su et al. (2021), *RoFormer: Enhanced Transformer with Rotary Position Embedding*.
- Press et al. (2022), *Train Short, Test Long: Attention with Linear Biases* (ALiBi).
- Peng et al. (2023), *YaRN: Efficient Context Window Extension of Large Language Models*.

## See Also

- [[RoPE]] — deep treatment of the modern default
- [[Self-Attention]]
- [[Transformer Block]]
- [[06 - Attention Mechanisms/MOC|Attention Mechanisms MOC]]
- [[ALiBi]] (planned)
- [[YaRN]] (planned)

## Absolute vs Relative — The Core Distinction

Positional encodings fall into two families with fundamentally different properties:

### Absolute positional encoding

Adds a position-dependent vector to each token: $\mathbf{x}_i = \mathbf{e}_{\text{token}_i} + \mathbf{p}_i$. The model learns to use $\mathbf{p}_i$ to infer position. Examples: sinusoidal, learned absolute.

- **Pros**: simple, works for short sequences.
- **Cons**: can't extrapolate beyond training length (learned) or extrapolates unreliably (sinusoidal). No explicit relative position.

### Relative positional encoding

Modifies the attention computation to depend on relative offset $i - j$. Examples: Shaw, Transformer-XL, RoPE, ALiBi.

- **Pros**: generalizes to longer sequences; relative position is what matters for most tasks.
- **Cons**: more complex; may need per-layer modification (Shaw, Transformer-XL).

Modern LLMs (Llama, Mistral, Qwen, DeepSeek) all use RoPE — a relative encoding that requires no learned parameters and no extra compute. This is the consensus after years of experimentation.

## The Evolution: Why Each Method Replaced the Previous

| Generation | Method | Year | Limitation that motivated the next |
|------------|--------|------|-------------------------------------|
| 1st | Sinusoidal | 2017 | Didn't extrapolate in practice |
| 2nd | Learned absolute | 2018 | Hard context limit; can't extrapolate |
| 3rd | Shaw relative | 2018 | Clipped max distance; per-layer cost |
| 4th | Transformer-XL | 2019 | Complex; many moving parts |
| 5th | RoPE | 2021 | Extrapolation needs YaRN/NTK |
| 5th | ALiBi | 2022 | Locality penalty hurts long-range |
| 6th | YaRN / LongRoPE | 2023-24 | Extends RoPE to 128K-2M |

Each generation addressed the limitation of the previous. The current state (2024-2026): RoPE + YaRN is the default for long context; ALiBi is niche; learned absolute is only for BERT-family (fixed 512 context).

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Mixing positional encodings | Combining absolute + RoPE | Pick one; they conflict |
| Wrong RoPE config | Wrong `rope_theta` or scaling | Check model card; pass correct config |
| Forgetting causal mask AND positional encoding | Both needed | Apply both; positional encoding alone isn't enough |
| Truncating past training length | Absolute embeddings | Use RoPE + YaRN for extension |

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Positional Information/07 - Sinusoidal and Learned Positional|Sinusoidal and Learned]] — generations 1-2.
- [[06 - Attention Mechanisms/Positional Information/08 - RoPE|RoPE]] — generation 5 (modern default).
- [[06 - Attention Mechanisms/Positional Information/09 - ALiBi|ALiBi]] — generation 5 (alternative).
- [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling|YaRN]] — generation 6 (context extension).
- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] — why positional encoding is needed.
- [[07 - Transformers/Architecture/01 - Transformer Block|Transformer Block]] — where positional encoding lives.
- [[24 - Research Frontiers/Long-Context/07 - Long-Context Architectures|Long-Context Architectures]].
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017|Vaswani 2017]] — sinusoidal.
- [[26 - Papers/Efficient Attention/16 - Transformer-XL 2019|Transformer-XL 2019]].

## Interview Questions

1. **Q: What's the difference between absolute and relative positional encoding?**
   A: Absolute adds a position-dependent vector to each token: $\mathbf{x}_i = \mathbf{e}_i + \mathbf{p}_i$. The model infers position from $\mathbf{p}_i$. Relative modifies the attention computation to depend on relative offset $i - j$. Absolute is simpler but can't extrapolate (learned) or extrapolates unreliably (sinusoidal). Relative generalizes to longer sequences and is what matters for most tasks. Modern LLMs use RoPE — a relative encoding with no learned parameters and no extra compute.

2. **Q: Why did relative encodings replace absolute encodings?**
   A: Three reasons. (1) **Extrapolation** — relative encodings generalize to sequences longer than training; absolute can't (learned) or does so unreliably (sinusoidal). (2) **What matters is relative** — for most tasks (translation, Q&A, code), the relative position of tokens matters more than absolute. (3) **Long context** — modern LLMs need 128K+ context; absolute embeddings would require training at that length, which is expensive. Relative encodings (RoPE + YaRN) can extend post-hoc.

3. **Q: Which positional encoding would you use for a new model?**
   A: RoPE. It's the de-facto standard (Llama, Mistral, Qwen, DeepSeek, Gemma all use it). No learned parameters, no extra compute, relative encoding, extensible with YaRN/NTK. For BERT-family (fixed 512 context), learned absolute is fine. For new modalities (audio, video), consider learned 2D/3D positional embeddings. But for text LLMs, RoPE is the answer.

4. **Q: How does positional encoding interact with context extension?**
   A: Absolute (learned): can't extend — positions past training length are undefined. Sinusoidal: theoretically extrapolates, but quality degrades. RoPE: extrapolates with YaRN/NTK scaling (4× zero-shot, 8-16× with fine-tuning, 2M+ with LongRoPE). ALiBi: native extrapolation (train on 1024, test on 2048+), but locality penalty. The choice of positional encoding determines how easily you can extend context post-hoc — this is why RoPE won.

5. **Q: What is the multi-scale property of positional encodings?**
   A: Both RoPE and ALiBi use multi-scale design — different frequencies/slopes capture different distance scales. RoPE: each dimension pair rotates at a different frequency ($\theta_k = 10000^{-2k/d}$); high frequencies capture local position, low frequencies capture long-range. ALiBi: each head has a different slope ($m_h = 1/2^h$); steep slopes attend locally, gentle slopes attend globally. This multi-scale property lets the model attend at multiple distance scales simultaneously, similar to wavelet transforms.

6. **Q: Why can't you combine absolute embeddings with RoPE?**
   A: They conflict. Absolute embeddings add position info to the input; RoPE rotates Q and K. Combining gives two positional signals that can interfere — the model receives conflicting information about position. Pick one. If you need both extrapolation (RoPE's strength via YaRN) and long-range attention (absolute's strength), use RoPE + YaRN — it gives extrapolation without the locality penalty. Mixing positional encodings is an implementation bug, not a design choice.

## See Also

- [[RoPE]] — deep treatment of the modern default
- [[Self-Attention]]
- [[Transformer Block]]
- [[06 - Attention Mechanisms/MOC|Attention Mechanisms MOC]]
- [[ALiBi]] (planned)
- [[YaRN]] (planned)
