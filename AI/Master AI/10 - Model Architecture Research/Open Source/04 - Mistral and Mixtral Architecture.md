---
tags: [model-architecture, mistral, mixtral, sliding-window, moe]
iteration: 5
created: 2026-08-08
aliases: [Mistral Architecture, Mixtral Architecture]
---

# 04 — Mistral and Mixtral Architecture

> [!info] TL;DR
> Mistral AI's models (Mistral 7B, Mixtral 8x7B, Mixtral 8x22B, Mistral Large) build on the Llama architecture with two key innovations: **Sliding Window Attention (SWA)** for efficient long context, and **Mixture-of-Experts (MoE)** for sparse compute. Mixtral 8x7B was the first open-weights MoE to match Llama 2 70B quality at 4× faster inference. All architectural details are **Officially Confirmed** in Mistral's blog posts and model cards.

> [!info] Source Status
> All claims are **Officially Confirmed** — documented in Mistral AI's blog posts (mistral.ai), model cards, and the Mistral 7B paper.

## Mistral 7B (September 2023)

### Architecture
Mistral 7B introduced Sliding Window Attention and GQA to the Llama baseline:

| Property            | Llama 2 7B   | Mistral 7B   |
|---------------------|--------------|--------------|
| Parameters          | 6.7B         | 7.2B         |
| Layers              | 32           | 32           |
| d_model             | 4096         | 4096         |
| Heads               | 32           | 32           |
| KV heads            | 32 (MHA)     | 8 (GQA)      |
| Context             | 4096         | 8192         |
| Attention           | Full         | Sliding Window (4096) |
| Vocab               | 32K          | 32K          |

### Key Innovations

#### Sliding Window Attention (SWA)
Each token attends to the previous 4096 tokens, not all previous tokens. With 32 layers, the effective receptive field is 32 × 4096 = 131K tokens — far more than the 8K context window.

See [[15 - Sliding Window Attention]] and [[26 - Mistral 7B 2023]] for details.

#### GQA (Grouped-Query Attention)
8 KV head groups shared across 32 query heads. Reduces KV cache by 4×, enabling larger batch sizes and longer contexts. See [[14 - GQA MQA MLA]].

#### Rolling Buffer KV Cache
The KV cache is stored as a circular buffer of size `window_size`. Position `i` is stored at `i mod window_size`. This keeps the cache fixed-size regardless of sequence length.

### Why Mistral 7B Mattered
Mistral 7B outperformed Llama 2 13B on all benchmarks despite being 2× smaller. This proved that architectural improvements (SWA + GQA) could substitute for scale. It established 7B as the practical sweet spot for open-weights models.

## Mixtral 8x7B (December 2023)

### Architecture
Mixtral 8x7B is Mistral 7B with Mixture-of-Experts:

| Property            | Mixtral 8x7B     |
|---------------------|------------------|
| Total parameters    | 46.7B            |
| Active per token    | 12.9B            |
| Layers              | 32               |
| d_model             | 4096             |
| Experts per layer   | 8                |
| Active experts      | 2                |
| Attention           | SWA (4096) + GQA |
| Context             | 32K              |
| Vocab               | 32K              |

### How MoE Works in Mixtral
Each layer's FFN is replaced by 8 parallel FFNs ("experts"). For each token, a router selects the top-2 experts (by learned affinity score). Only those 2 experts compute; the other 6 are idle for that token.

```
# For each token:
router_scores = softmax(router(token))  # 8 scores
top_2_experts = argsort(router_scores)[-2:]  # pick top 2
output = sum(router_scores[i] * expert[i](token) for i in top_2_experts)
```

This gives 12.9B active parameters (2 experts × ~6.5B each + attention) out of 46.7B total. The model has the capacity of a 47B model but the inference cost of a 13B model.

### Load Balancing
Mixtral uses an auxiliary loss to balance expert usage — if some experts are overused and others idle, the loss penalizes the imbalance. This ensures all experts learn and contribute. (DeepSeek-V3 would later eliminate this auxiliary loss — see [[28 - DeepSeek-V2 and V3 2024]].)

### Key Results
Mixtral 8x7B matched or exceeded Llama 2 70B on most benchmarks while being 4× faster at inference (12.9B active vs 70B active). This established MoE as practical for open-weights, not just closed-source models.

## Mixtral 8x22B (April 2024)

### Architecture
Scaled-up Mixtral:

| Property            | Mixtral 8x22B    |
|---------------------|------------------|
| Total parameters    | 141B             |
| Active per token    | 39B              |
| Experts per layer   | 8                |
| Active experts      | 2                |
| Context             | 64K              |
| Vocab               | 32K              |

### Key Results
Mixtral 8x22B approached GPT-4 quality on some benchmarks, making it the strongest open-weights MoE as of mid-2024 (before DeepSeek-V3).

## Mistral Large (2024)

### Architecture
Unlike Mixtral, Mistral Large is a **dense** model (not MoE):

| Property            | Mistral Large    |
|---------------------|------------------|
| Parameters          | 123B             |
| Architecture        | Dense (no MoE)   |
| Attention           | GQA              |
| Context             | 128K             |
| Vocab               | 32K → 128K (v2)  |

### Why Dense?
Mistral Large is closed-weights (API only). For closed models, the inference cost advantage of MoE is less critical (you're charging per token anyway), and dense models are simpler to serve. The dense architecture may also be easier to align.

## Mistral Nemo (2024)

### Architecture
Developed with NVIDIA, designed as a drop-in upgrade for Mistral 7B:

| Property            | Mistral Nemo     |
|---------------------|------------------|
| Parameters          | 12B              |
| Attention           | GQA              |
| Context             | 128K             |
| Vocab               | 128K (Tekken tokenizer) |

### Key Features
- **128K context** (vs Mistral 7B's 8K).
- **Tekken tokenizer** (128K vocab, better multilingual).
- **Trained with NVIDIA** on their infrastructure.

Mistral Nemo is positioned as the "best 12B model" — small enough to run on consumer hardware, large enough for serious applications.

## Architectural Patterns Across the Family

### Consistent Choices
- **Pre-norm, RMSNorm, SwiGLU, no bias** — inherited from Llama.
- **GQA** — used by all Mistral models (Mistral 7B was an early GQA adopter).
- **RoPE** — standard positional encoding.

### Variable Choices
- **SWA**: used by Mistral 7B and Mixtral; not always used by Mistral Large/Nemo.
- **MoE**: used by Mixtral variants; not by Mistral 7B/Large/Nemo.
- **Context length**: 8K (Mistral 7B) → 32K (Mixtral 8x7B) → 64K (Mixtral 8x22B) → 128K (Large, Nemo).

## Why Mistral's Architecture Matters

### SWA as a Standard Technique
Mistral 7B popularized sliding window attention. While not universally adopted (Llama 3 uses full attention), SWA is now a standard option for efficient long-context models.

### MoE for Open Weights
Mixtral proved that MoE works for open-weights. Before Mixtral, MoE was primarily a closed-source technique (GShard, Switch Transformer were research; GPT-4's rumored MoE was closed). Mixtral's open weights let the community study and build on MoE.

### The 7B Sweet Spot
Mistral 7B's success established 7B as the practical size for open-weights models. Llama 3 8B, Qwen 2.5 7B, Gemma 2 9B all target this tier — small enough for consumer hardware, large enough for serious applications.

### European AI Sovereignty
Mistral AI (French) demonstrated that frontier-quality open-weights LLMs could be developed outside the US. This had geopolitical implications — the EU's AI sovereignty depends on having competitive models, and Mistral provides that.

## Comparison to Other Families

| Family    | MoE? | SWA? | Notable Innovation                  |
|-----------|------|------|-------------------------------------|
| Llama     | Llama 4 only | No  | Conservative baseline              |
| Mistral   | Mixtral | Yes (7B, Mixtral) | SWA + MoE for open weights |
| Qwen      | Qwen 2.5 MoE | Some variants | Multilingual, large vocab  |
| DeepSeek  | V2+  | No   | MLA, auxiliary-loss-free MoE        |
| Gemma     | No   | No   | GQA, large vocab                    |

Mistral's contribution is SWA + MoE, both adopted by the broader community.

## Impact and Legacy

Mistral's architectural influence:

1. **Popularized SWA and GQA**. Both became standard techniques after Mistral 7B's success.

2. **Validated MoE for open-weights**. Mixtral proved MoE was practical and competitive, paving the way for DeepSeek-V3, Qwen MoE, and Llama 4.

3. **Established the 7B tier**. Mistral 7B's quality at 7B parameters made this the default size for cost-effective open-weights models.

4. **European AI presence**. Mistral AI became the leading European AI lab, demonstrating that frontier-quality LLMs could be developed outside the US.

For AI engineers, Mistral models are strong choices for cost-sensitive deployments. The architectural lessons (SWA, GQA, MoE) are now standard across the open-weights ecosystem.

## Further Reading

- Mistral 7B paper: arXiv:2310.06825 — see [[26 - Mistral 7B 2023]]
- Mixtral: arXiv:2401.04088
- Mistral blog: mistral.ai/news/
- [[02 - Llama Mistral Qwen Comparison]] — comparison note.

## See Also

- [[26 - Mistral 7B 2023]]
- [[03 - Llama Family Architecture]]
- [[05 - Qwen Family Architecture]]
- [[02 - Llama Mistral Qwen Comparison]]
- [[15 - Sliding Window Attention]]
- [[14 - GQA MQA MLA]]
- [[15 - Mixture of Experts Transformer]]
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]
