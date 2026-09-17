---
tags: [paper, longformer, sparse-attention, long-context]
iteration: 4
created: 2026-08-08
aliases: [Longformer 2020, Beltagy 2020, Sliding Window Attention]
---

# 18 — Longformer (Beltagy et al., 2020)

> [!info] TL;DR
> Longformer combined **sliding-window attention** (each token attends to a local window of neighbors) with **global attention** (a few selected tokens attend to everything) to achieve O(N) attention cost while preserving the ability to integrate information across the full sequence. Longformer was designed for long-document NLP tasks (long-context QA, summarization) and became the standard pattern for sparse attention. Sliding-window attention remains a key technique in modern LLMs (Mistral, Gemma).

## Citation

Beltagy, I., Peters, M. E., & Cohan, A. (2020). *Longformer: The Long-Document Transformer*. arXiv:2004.05150.

## The Problem Being Solved

BERT and RoBERTa (2018–2019) achieved SOTA on most NLP benchmarks but were limited to 512-token contexts. Many important tasks — long-document QA, document classification, scientific paper summarization — naturally involve 5K–20K tokens. With vanilla attention, processing 16K tokens requires 256× more attention memory than 512 tokens — completely impractical.

[[17 - Reformer 2020|Reformer]] (2020) tried to solve this with LSH attention, but the quality sacrifices and implementation complexity made it unattractive. Longformer took a different approach: keep the attention mechanism simple and predictable, but restrict which tokens attend to which.

The key insight: in most long-document tasks, attention is *local* — a token cares most about its neighbors. A small amount of *global* attention (for task-critical tokens like the [CLS] token or question tokens) is sufficient to integrate information across the document.

## The Key Idea: Sliding Window + Global Attention

### Sliding Window Attention
Each token attends to `w` tokens on each side (window size `2w + 1`). For a sequence of length N, this gives O(N · w) attention cost — linear in N for fixed w.

With stacked layers, the effective receptive field grows: each layer can attend to tokens `w` positions away, so `L` layers give an effective receptive field of `L · w`. A 12-layer model with `w=512` can integrate information from ~6K tokens — enough for most long-document tasks.

### Global Attention
A few tokens (selected by task design) attend to *every* token in the sequence, and every token attends to them. These "global tokens" act as information hubs, aggregating context from the full document.

For different tasks, different tokens are global:
- **Classification**: the [CLS] token is global. It aggregates document-level information for the classification head.
- **QA**: the question tokens are global. The model needs to attend from the question to all parts of the document, and from the document back to the question.
- **Extractive QA**: the [CLS] and question tokens are global.

Global attention adds O(N · g) cost where g is the number of global tokens (typically small — 5 to 50). The total cost is O(N · w + N · g) = O(N) for fixed w and g.

```mermaid
graph TD
  subgraph Standard Attention O(N²)
    T1[Token 1] --> All1[All N tokens]
    T2[Token 2] --> All2[All N tokens]
    TN[Token N] --> AllN[All N tokens]
  end
  subgraph Longformer Attention O(N)
    L1[Token i-w] --> W1[Token i window]
    L2[Token i] --> W2[Window: i-w to i+w]
    L3[Token i+w] --> W3[Token i window]
    G1[Global token: CLS] --> All3[All N tokens]
    G2[Global token: Q1] --> All4[All N tokens]
  end
```

### Implementation: Dilated Sliding Window
To increase the effective receptive field without increasing the window size, Longformer uses *dilated* windows: tokens at offsets `0, d, 2d, ...` within the window. This is similar to dilated convolutions in CNNs. With dilation `d`, the effective receptive field per layer becomes `d · w` instead of `w`.

Different layers use different dilation patterns (lower layers: small dilation for local patterns; higher layers: large dilation for long-range patterns).

## Key Results

Longformer achieved SOTA on several long-document benchmarks:

| Task                                  | Previous SOTA | Longformer |
|---------------------------------------|---------------|------------|
| WikiHop (multi-hop QA)                | 74.1          | 74.6       |
| TriviaQA (long-context QA)            | 66.4          | 72.0       |
| arXiv summarization (ROUGE-L)         | 33.2          | 36.5       |

The most striking result was on TriviaQA: Longformer improved by 5.6 points, demonstrating that long-context attention was genuinely useful for retrieval-style QA. The arXiv summarization result showed similar gains for generation tasks.

Importantly, Longformer matched full-attention BERT on short-context tasks (with the same parameter count). This meant you could use Longformer as a drop-in replacement for BERT without quality loss on short inputs, while gaining long-context capability for free.

## Why It Worked

### Local + Global Matches Task Structure
Most long-document tasks have a natural structure where most information is local (a paragraph, a section) but a few task-critical tokens need global context (the question, the [CLS]). Longformer's attention pattern matches this structure exactly.

### Stacked Layers Give Long Receptive Fields
A 12-layer model with window size 512 has a receptive field of ~6K tokens — enough for most documents. With dilation, the effective receptive field grows further. This "local attention with stacked layers" pattern is more parameter-efficient than trying to attend globally from every token.

### Linear Complexity Enables Long Contexts
O(N) complexity means Longformer can process 16K-token documents on a single GPU — practical for the first time. This opened up long-document NLP as a research area.

### Drop-in Compatibility with BERT
Longformer was initialized from RoBERTa weights, with only the attention pattern changed. This meant most of the model's capability was inherited from pretraining, and only the long-context attention needed to be fine-tuned. This pattern — initialize from a pretrained model, modify attention — became standard for long-context variants.

## Limitations

### Fixed Window Size
The window size is a hyperparameter that must be chosen in advance. Too small, and the model misses long-range dependencies; too large, and the O(N · w) cost grows. Modern sliding-window models (Mistral) use ~4K windows.

### Global Tokens Must Be Chosen
The choice of global tokens is task-specific. For general-purpose LLMs (chat, code generation), it's not clear which tokens should be global. This limits Longformer's applicability to task-specific fine-tuning.

### Receptive Field Grows Slowly
With L layers and window w, the receptive field is L · w. For very long contexts (100K+ tokens), you need either very deep models or very large windows. Modern long-context models use additional techniques (Ring Attention, sparse global patterns) to extend further.

### Superseded by FlashAttention for Most Use Cases
[[08 - FlashAttention 2022|FlashAttention]] (2022) made full attention fast enough for most practical sequence lengths (up to ~32K). Longformer's complexity advantage matters only for very long contexts (>32K), where the quality trade-offs of sparse attention become worthwhile.

## Impact and Legacy

Longformer's influence extends well beyond the original paper:

1. **Sliding window as a standard pattern**. Mistral 7B (2023), Gemma (2024), and other modern LLMs use sliding-window attention as one of their attention patterns. The exact formulation differs (Mistral uses pure sliding window; Longformer used sliding + global), but the core idea is the same.

2. **Hybrid attention patterns**. Longformer's combination of local + global attention inspired many variants: BigBird (random + local + global), Sparse Transformer (strided + fixed patterns), Mistral (sliding + global for specific layers). The general lesson — combine cheap local attention with expensive global attention for a few tokens — is now standard.

3. **Long-document NLP as a research area**. Longformer demonstrated that long-context models could meaningfully outperform short-context models on long-document tasks. This motivated a wave of long-context benchmarks (LongBench, SCROLLS, L-Eval) and models.

4. **Foundation for modern long-context LLMs**. The techniques Longformer pioneered — sparse attention, hybrid patterns, dilated windows — appear in modified form in modern long-context models. Llama 3's 128K context, Claude's 200K context, and Gemini's 1M context all build on ideas first explored in Longformer and its contemporaries.

For AI engineers, Longformer is the canonical reference for sliding-window attention. If you're working with Mistral, Gemma, or any model that uses local attention, understanding Longformer clarifies the design space and trade-offs.

## Further Reading

- Original paper: arXiv:2004.05150
- [[15 - Sliding Window Attention]] — modern usage in Mistral.
- [[12 - Sparse Attention]] — broader survey of sparse patterns.

## See Also

- [[12 - Sparse Attention]]
- [[15 - Sliding Window Attention]]
- [[17 - Reformer 2020]]
- [[20 - BigBird 2020]]
- [[08 - FlashAttention 2022]]
- [[26 - Papers/MOC|Papers MOC]]
