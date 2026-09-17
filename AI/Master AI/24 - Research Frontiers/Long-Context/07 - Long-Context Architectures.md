---
tags: [research, long-context, ring-attention, infini-attention, longrope]
iteration: 5
created: 2026-08-08
aliases: [Long-Context Architectures, Ring Attention, Infini-Attention, LongRoPE]
---

# 07 — Long-Context Architectures

> [!info] TL;DR
> Long-context architectures extend LLMs to 1M+ token contexts. The four main approaches are: **Ring Attention** (distribute attention across GPUs in a ring), **Infini-Attention** (compress old context into a fixed-size state), **LongRoPE** (extrapolate positional encodings to extreme lengths), and **hybrid SSM/attention** (use linear layers for long context). Each makes different trade-offs between quality, cost, and maximum context length. Together, they enabled the 2024–2025 era of million-token LLMs.

## The Problem Being Solved

Standard LLMs have context limits (4K–128K tokens). Many applications need more:
- **Full-codebase analysis**: a large codebase can be 1M+ tokens.
- **Long-document research**: scientific papers, legal cases, books.
- **Multi-hour video**: transcripts + frames can be 1M+ tokens.
- **Long conversations**: a year of chat history.

Extending context is hard because attention is O(N²). For 1M tokens, the attention matrix has 10^12 entries — completely infeasible. Long-context architectures solve this through various forms of sparsity, compression, or distribution.

## The Four Approaches

### 1. Ring Attention (Distributed)
Ring Attention (Liu et al., 2023) distributes the attention computation across multiple GPUs arranged in a ring. Each GPU holds a chunk of the sequence; attention is computed by passing KV blocks around the ring.

#### How It Works
1. **Split the sequence**: each of P GPUs holds N/P tokens.
2. **Each GPU computes attention for its queries** against all keys/values.
3. **KV blocks are passed around the ring**: GPU 0 sends its KV to GPU 1, GPU 1 sends to GPU 2, etc.
4. **After P steps**, each GPU has seen all KV blocks and computed full attention.

The key insight: the communication (passing KV around the ring) overlaps with the computation (attention for the current KV block). This hides the communication latency.

#### Trade-offs
- **Pro**: exact attention (no approximation), scales to any context length by adding GPUs.
- **Con**: requires many GPUs (P GPUs for N tokens, with each GPU holding N/P). For 1M tokens on 8 GPUs, each holds 125K — feasible but expensive.
- **Con**: communication overhead; if GPUs are slow to communicate, the ring stalls.

#### Adoption
Ring Attention (or similar distributed attention) is used by frontier models for long contexts. Gemini 1.5's 1M context likely uses a variant.

### 2. Infini-Attention (Compressive)
Infini-Attention (Google, 2024) compresses old context into a fixed-size state, similar to an SSM. Recent context uses standard attention; old context is retrieved from the compressed state.

#### How It Works
1. **Recent context** (last N tokens): standard attention.
2. **Old context** (beyond N): compressed into a fixed-size state via linear attention.
3. **The model attends to both**: recent tokens via attention, old tokens via the compressed state.

The compression is lossy — the state can't store all information from old context. But it's O(1) per token (the state is fixed-size), so context length is unbounded.

#### Trade-offs
- **Pro**: unbounded context length, O(N) compute.
- **Con**: lossy compression — old information is degraded.
- **Con**: retrieval from the compressed state is weaker than from explicit KV.

#### Adoption
Infini-Attention is a Google research contribution. It influenced the design of models with "infinite" context, though production adoption is limited.

### 3. LongRoPE (Positional Extrapolation)
LongRoPE (Microsoft, 2024) extends RoPE (Rotary Position Embedding) to very long contexts (up to 2M tokens) by carefully scaling the positional frequencies.

#### The Problem with RoPE
RoPE encodes positions as rotations. Trained on N tokens, RoPE doesn't extrapolate well to >N tokens — the rotation angles become larger than seen in training, and the model behaves unpredictably.

#### LongRoPE's Solution
LongRoPE searches for the optimal scaling of RoPE frequencies for long contexts. Instead of a single scaling factor (like YaRN), it uses different scaling for different frequency bands:
- **Low frequencies** (long-range patterns): scale less aggressively.
- **High frequencies** (short-range patterns): scale more aggressively.

This non-uniform scaling allows extrapolation to 2M tokens from a model trained on 8K.

#### Trade-offs
- **Pro**: no architecture change, just a positional encoding tweak. Easy to adopt.
- **Pro**: works with existing models (just change the RoPE implementation).
- **Con**: extrapolation quality degrades at extreme lengths — the model hasn't seen such long contexts during training.
- **Con**: requires careful tuning of the scaling per model.

#### Adoption
LongRoPE (and similar techniques like YaRN, NTK-aware scaling) are widely used to extend context for existing models. Llama 3's 128K context, Qwen 2.5's 128K context, and many community models use RoPE scaling.

### 4. Hybrid SSM/Attention
Hybrid architectures (Jamba, Kimi Linear, MiniMax-01) use SSM layers for most of the sequence mixing and attention layers for retrieval. See [[30 - Kimi Linear 2025]] and [[02 - Mamba-2 and Structured Attention]].

#### How It Works
- Most layers: SSM (linear time, handles general context).
- A few layers: full attention (handles precise retrieval).
- The SSM layers make long context cheap; the attention layers maintain retrieval quality.

#### Trade-offs
- **Pro**: O(N) cost for most layers, enabling million-token contexts.
- **Pro**: attention layers preserve retrieval quality.
- **Con**: more complex architecture (two kernel types).
- **Con**: still some retrieval quality loss vs. full attention.

#### Adoption
Hybrid architectures are the 2025 trend for long-context models. Jamba, Zamba, MiniMax-01, and Kimi Linear all use this approach.

## Comparison

| Approach           | Max Context | Quality     | Cost        | Complexity |
|--------------------|-------------|-------------|-------------|------------|
| Ring Attention     | Scales w/ GPUs | Exact    | O(N²) but distributed | High (distributed) |
| Infini-Attention   | Unbounded   | Lossy (old context) | O(N) | Medium |
| LongRoPE           | ~2M         | Degrades at extremes | O(N²) but practical | Low (just RoPE tweak) |
| Hybrid SSM/Attn    | 1M+         | Near-attention | O(N) | Medium |

## Why These Matter

### Enabling New Applications
Million-token contexts enable applications that were previously impossible:
- **Full-codebase AI assistants**: read the entire codebase, answer questions about any part.
- **Long-document research**: upload 1000 papers, ask cross-document questions.
- **Video understanding**: process multi-hour videos with full context.
- **Long-term agents**: agents that maintain context across days/weeks of operation.

### Reducing RAG Dependence
With long enough context, you can put all relevant documents directly in the context, bypassing RAG retrieval. This is simpler (no retrieval pipeline) and often higher quality (no retrieval misses). The trade-off: long-context inference is expensive, so RAG remains cost-effective for high-volume applications.

### Changing Model Design
Long-context requirements drive architectural innovation. The 2024–2025 trend toward hybrid SSM/attention models is largely motivated by long-context needs. Models designed for short contexts (standard Transformers) are being supplemented by long-context variants.

## Production Considerations

### Cost of Long Context
Long context is expensive. A 1M-token prompt costs 1000× more than a 1K-token prompt (for input tokens). For closed-model APIs, this can be $10+ per query. For self-hosted models, it requires significant GPU memory.

### When to Use Long Context vs. RAG
- **Long context**: when quality matters more than cost, when retrieval is hard (unstructured data), when the task requires cross-document reasoning.
- **RAG**: when cost matters, when the corpus is huge (can't fit in context), when retrieval is reliable (structured data).

Many production systems use both: RAG to find relevant chunks, long context to process them in detail.

### Latency
Long contexts have high latency — prefilling 1M tokens takes seconds to minutes. Streaming responses help perceived latency, but the first token is still slow. This makes long-context models unsuitable for real-time chat.

### Quality Degradation
Models degrade at very long contexts, even when technically supported. "Lost in the middle" — information in the middle of a long context is recalled worse than information at the beginning or end. This is an active research area.

## Impact and Legacy

Long-context architectures transformed the LLM landscape in 2024–2025:

1. **Million-token context as a product feature**. Gemini 1.5 (1M), Claude (200K), GPT-4 (128K), Llama 3.1 (128K) — long context is now a standard capability.

2. **Enabled new application categories**. Code assistants (Cursor, Continue), research tools (Perplexity Pro), video understanding (Twelvelabs) all rely on long context.

3. **Drove architectural innovation**. The long-context requirement motivated hybrid SSM/attention models, Ring Attention, and positional extrapolation techniques.

4. **Shifted the RAG vs. long-context trade-off**. With long enough context, RAG becomes optional for some applications. This simplified architectures but increased costs.

5. **Highlighted "lost in the middle"**. The discovery that models recall middle-of-context information poorly motivated research on attention patterns and training strategies.

For AI engineers, long-context architectures matter when:
- Designing applications with large inputs (codebases, documents, video).
- Choosing between long context and RAG.
- Reasoning about cost and latency for long-context queries.
- Understanding why 2025 models handle long context differently.

## Further Reading

- Ring Attention: arXiv:2310.01889
- Infini-Attention: arXiv:2404.07143
- LongRoPE: arXiv:2402.13753
- YaRN: arXiv:2309.00071
- [[30 - Kimi Linear 2025]] — hybrid approach.
- [[10 - YaRN and NTK-aware Scaling]] — positional extrapolation.

## See Also

- [[30 - Kimi Linear 2025]]
- [[02 - Mamba-2 and Structured Attention]]
- [[10 - YaRN and NTK-aware Scaling]]
- [[08 - RoPE]]
- [[12 - Sparse Attention]]
- [[15 - Sliding Window Attention]]
- [[01 - RAG Pipeline Overview]] — the alternative to long context
- [[24 - Research Frontiers/MOC|24 Research Frontiers MOC]]
