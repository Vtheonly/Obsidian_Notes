---
tags: [model-architecture, llama, open-source, officially-confirmed]
iteration: 5
created: 2026-08-08
aliases: [Llama Architecture, Llama 1 2 3 4 Architecture]
---

# 03 — Llama Family Architecture

> [!info] TL;DR
> The Llama family (1, 2, 3, 4) is the most influential open-weights LLM lineage. Architecturally conservative — decoder-only Transformer with pre-norm, RMSNorm, RoPE, SwiGLU, no bias — Llama's design became the template for nearly all open-weights LLMs. Evolution across versions: larger context (2K → 128K), better tokenizer (32K → 128K vocab), GQA adoption (Llama 2+), and MoE + multimodal (Llama 4). All architectural details are **Officially Confirmed** in Meta's model cards and papers.

> [!info] Source Status
> All claims in this note are **Officially Confirmed** — documented in Meta's Llama papers (Llama 1, Llama 2), model cards (Llama 3, 3.1, 4), and technical blog posts.

## The Llama Design Philosophy

Llama's architecture is deliberately conservative. Rather than inventing new components, Meta combined the community's best-practice consensus into a single clean design:
- **Decoder-only** (not encoder-decoder) — simpler, supports generation.
- **Pre-norm** (not post-norm) — more stable training.
- **RMSNorm** (not LayerNorm) — slightly faster, same quality.
- **RoPE** (not sinusoidal or learned absolute) — better length generalization.
- **SwiGLU** (not GELU or ReLU) — better FFN quality.
- **No bias terms** — simpler, slightly faster.

This "best practices" approach made Llama a reference implementation. Most subsequent open-weights models (Mistral, Qwen, Gemma, DeepSeek) use variations of the same recipe.

## Llama 1 (February 2023)

### Architecture
| Property            | 7B    | 13B   | 33B   | 65B   |
|---------------------|-------|-------|-------|-------|
| Layers              | 32    | 40    | 60    | 80    |
| d_model             | 4096  | 5120  | 6656  | 8192  |
| Heads               | 32    | 40    | 52    | 64    |
| d_head              | 128   | 128   | 128   | 128   |
| Context             | 2048  | 2048  | 2048  | 2048  |
| Vocab               | 32K   | 32K   | 32K   | 32K   |
| Attention           | MHA   | MHA   | MHA   | MHA   |
| Positional encoding | RoPE  | RoPE  | RoPE  | RoPE  |
| Norm                | RMSNorm | RMSNorm | RMSNorm | RMSNorm |
| Activation          | SwiGLU | SwiGLU | SwiGLU | SwiGLU |

### Training Data
- 4.7T tokens of public data (CommonCrawl, C4, GitHub, Wikipedia, Books, ArXiv, StackExchange).
- Trained with 2K context, no instruction tuning (base model).

### Key Architectural Choices
- **RoPE** with base 10000.
- **No bias** in any projection.
- **Pre-norm** with RMSNorm.
- **Efficient attention** via `xformers`.

See [[25 - LLaMA 2023]] for the full paper note.

## Llama 2 (July 2023)

### Architecture Changes from Llama 1
- **Context**: 2K → 4K (Llama 2) → 16K (Llama 2 long, some variants).
- **GQA** for the 70B model (8 KV head groups, reducing KV cache by 8×).
- **Larger context** for chat variants (16K).
- **RLHF** for chat variants (Llama-2-Chat).

| Property            | 7B    | 13B   | 70B        |
|---------------------|-------|-------|------------|
| Layers              | 32    | 40    | 80         |
| d_model             | 4096  | 5120  | 8192       |
| Heads               | 32    | 40    | 64         |
| KV heads            | 32 (MHA) | 40 (MHA) | 8 (GQA) |
| Context             | 4096  | 4096  | 4096       |
| Vocab               | 32K   | 32K   | 32K        |

### Training Data
- 2.0T tokens (less than Llama 1's 4.7T — Meta found diminishing returns beyond this for the architecture).
- Added instruction-following data for chat variants.
- RLHF with safety and helpfulness rewards.

### Key Results
Llama 2 70B Chat was the first open-weights model to approach GPT-3.5 quality, making it the default for open-source chatbot deployment in 2023.

## Llama 3 (April 2024) and Llama 3.1 (July 2024)

### Architecture Changes from Llama 2
- **Context**: 4K → 8K (Llama 3) → 128K (Llama 3.1).
- **GQA** for all sizes (not just 70B).
- **New tokenizer**: 128K vocabulary (up from 32K), BPE-based. Better multilingual and code support.
- **Much more training data**: 15T tokens (up from 2T).
- **RoPE base** increased to 500000 (for better long-context extrapolation).

| Property            | 8B    | 70B   | 405B       |
|---------------------|-------|-------|------------|
| Layers              | 32    | 80    | 126        |
| d_model             | 4096  | 8192  | 16384      |
| Heads               | 32    | 64    | 128        |
| KV heads            | 8 (GQA) | 8 (GQA) | 8 (GQA) |
| Context             | 128K  | 128K  | 128K       |
| Vocab               | 128K  | 128K  | 128K       |

### Training Data
- 15T tokens of curated data (significantly more and better filtered than Llama 2).
- Multilingual coverage (50+ languages with significant data).
- Code data from GitHub.
- Mathematical and scientific content.

### Key Results
Llama 3.1 405B was the first open-weights model to match GPT-4 on many benchmarks. This was a watershed moment — it proved that open-source could match closed-source at the frontier.

### The 128K Context Extension
Llama 3.1 extended context from 8K to 128K via:
- **RoPE scaling** (YaRN-style, with carefully tuned parameters).
- **Continued pretraining** on long-context data.
- **Attention implementation** that handles 128K efficiently (FlashAttention-2/3).

## Llama 4 (2025)

> [!info] Source Status
> Llama 4 architecture details are **Officially Confirmed** in Meta's announcements, but full technical details may not be completely published. This note reflects publicly available information as of mid-2025.

### Architecture Changes from Llama 3
- **Mixture-of-Experts** (first Llama to use MoE).
- **Multimodal** (vision-language capability, native).
- **Early-fusion architecture** (vision and text processed together from the start).

Llama 4 represents Meta's shift from the conservative dense architecture to MoE + multimodal, aligning with the broader 2025 trend toward MoE + hybrid architectures.

## Why the Llama Architecture Became Standard

### Best-Practices Consensus
Llama's components (pre-norm, RMSNorm, RoPE, SwiGLU, no bias) were each the community's best-practice choice by 2023. Combining them gave a clean, well-understood design.

### Open Weights Enabled Adoption
Because the weights were open, researchers could study, modify, and build on Llama. This drove adoption of the architectural choices — fine-tunes and derivatives inherited the architecture.

### Simplicity
The architecture is simple — no exotic components, no complex routing, no special training tricks. This makes it easy to implement, debug, and serve.

### Proven at Scale
Llama 1, 2, 3, and 4 demonstrated that the architecture scales predictably from 7B to 405B+. The scaling laws are well-understood, giving confidence in the design.

## Comparison to Other Families

| Family    | Architecture Highlights                                  |
|-----------|----------------------------------------------------------|
| Llama     | Conservative: MHA/GQA, RoPE, SwiGLU, RMSNorm            |
| Mistral   | + Sliding Window Attention (Mistral 7B)                  |
| Qwen      | + GQA, larger vocab, multilingual focus                  |
| DeepSeek  | + MLA (V2+), MoE (V2+), auxiliary-loss-free balancing (V3)|
| Gemma     | + GQA, larger vocab, RoPE with longer base              |

Llama is the most conservative; other families add innovations on top of the Llama baseline.

## Impact and Legacy

Llama's architectural influence:

1. **Standardized open-weights LLM design**. Nearly every open-weights LLM uses Llama's architectural choices (with minor variations).

2. **Proved Chinchilla scaling works**. Llama's "train smaller models on more data" strategy validated Chinchilla's predictions and became standard.

3. **Enabled the open-source ecosystem**. Without Llama's open weights, the fine-tune, quantization, and serving ecosystems wouldn't exist.

4. **Pushed closed-source labs**. Llama 3.1 405B matching GPT-4 put competitive pressure on OpenAI and Anthropic, accelerating their development.

For AI engineers, Llama is the reference architecture. If you're building a custom LLM or understanding how open-weights models work, Llama's design is the starting point.

## Further Reading

- Llama 1 paper: arXiv:2302.13971 — see [[25 - LLaMA 2023]]
- Llama 2 paper: arXiv:2307.09288
- Llama 3 model card: huggingface.co/meta-llama/Meta-Llama-3-8B
- [[02 - Llama Mistral Qwen Comparison]] — comparison note.

## See Also

- [[25 - LLaMA 2023]]
- [[02 - Llama Mistral Qwen Comparison]]
- [[04 - Mistral and Mixtral Architecture]]
- [[05 - Qwen Family Architecture]]
- [[08 - RoPE]]
- [[14 - GQA MQA MLA]]
- [[04 - Normalization Layers]]
- [[05 - Feed-Forward Network Deep]]
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]
