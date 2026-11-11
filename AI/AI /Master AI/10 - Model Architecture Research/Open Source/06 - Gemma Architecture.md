---
tags: [model-architecture, gemma, google, open-source]
iteration: 5
created: 2026-08-08
aliases: [Gemma Architecture, Gemma 2 3, Google Open Weights]
---

# 06 — Gemma Architecture

> [!info] TL;DR
> Gemma is Google's open-weights LLM family (2B, 7B, 9B, 27B), derived from the research and technology used for Gemini. Architecturally similar to Llama (decoder-only, GQA, RoPE, RMSNorm) but with distinctive choices: very large vocabulary (256K), local attention with global periodic attention (Gemma 2), and logit soft-capping for training stability. Gemma 2 (2024) achieved strong quality for its size, making it competitive with Llama 3 and Mistral.

> [!info] Source Status
> All claims are **Officially Confirmed** — documented in Google DeepMind's Gemma and Gemma 2 technical reports and model cards.

## The Gemma Lineage

| Version   | Release       | Sizes              | Key Features                              |
|-----------|---------------|--------------------|---------------------------------------------|
| Gemma 1   | Feb 2024      | 2B, 7B             | GQA, RoPE, 256K vocab                       |
| Gemma 2   | June 2024     | 2B, 9B, 27B        | Local + global attention, logit soft-capping|
| CodeGemma | April 2024    | 2B, 7B             | Code-specialized                            |
| RecurrentGemma | 2024     | 2B, 9B             | Griffin architecture (RNN + attention)     |
| Gemma 3   | 2025          | Multiple           | Multimodal, larger context                  |

## Gemma 1 (February 2024)

### Architecture
Gemma 1 is architecturally similar to Llama 2, with a few key differences:

| Property            | Gemma 2B  | Gemma 7B  |
|---------------------|-----------|-----------|
| Parameters          | 2.5B      | 8.5B      |
| Layers              | 18        | 28        |
| d_model             | 2048      | 3072      |
| Heads               | 8         | 16        |
| KV heads            | 1 (MQA)   | 8 (GQA)   |
| Context             | 8K        | 8K        |
| Vocab               | 256K      | 256K      |
| RoPE base           | 10000     | 10000     |

### Key Architectural Choices

#### Large Vocabulary (256K)
Gemma uses a 256K vocabulary — the largest among major open-weights LLMs at the time. The large vocab:
- Better supports multilingual text (SentencePiece-based tokenizer).
- Better supports code (many tokens per language).
- Reduces sequence length for non-English text.
- Trade-off: large embedding matrix (256K × d_model), adding ~500M parameters for the 7B model.

#### MQA for the 2B Model
Gemma 2B uses Multi-Query Attention (1 KV head) — the most aggressive KV cache reduction. This makes the 2B model very efficient to serve, at some quality cost. The 7B model uses GQA (8 KV heads) — a more balanced choice.

#### GeGLU Activation
Gemma 1 uses GeGLU (GELU-based gated linear unit) instead of SwiGLU. The difference is the activation function inside the gating: GeGLU uses GELU, SwiGLU uses Swish. Both are gated; the choice is largely empirical.

### Training
- 6T tokens of primarily English web data, code, and mathematical text.
- Trained with TPUs (Google's hardware).
- Knowledge distillation from larger Gemini models for the 2B variant.

## Gemma 2 (June 2024)

### Architecture
Gemma 2 introduced several innovations beyond Gemma 1:

| Property            | Gemma 2 2B | Gemma 2 9B | Gemma 2 27B |
|---------------------|------------|------------|-------------|
| Parameters          | 2.6B       | 9B         | 27B         |
| Layers              | 26         | 42         | 46          |
| d_model             | 2304       | 3584       | 4608        |
| Heads               | 8          | 16         | 32          |
| KV heads            | 4 (GQA)    | 8 (GQA)    | 16 (GQA)    |
| Context             | 8K         | 8K         | 8K          |
| Vocab               | 256K       | 256K       | 256K        |

### Key Innovations

#### Local + Global Attention Pattern
Gemma 2 alternates between:
- **Local attention** (sliding window, 1024 tokens): each token attends to a local window. Cheap, captures local patterns.
- **Global attention**: every 6th layer uses full attention. Captures long-range dependencies.

This pattern gives most of the efficiency of sliding window attention while preserving some global context. It's a hybrid approach, similar in spirit to Longformer but with a different pattern.

#### Logit Soft-Capping
Gemma 2 caps attention logits and final logits to a maximum value:
```
logits = tanh(logits / cap) * cap
```

This prevents logits from growing unboundedly during training, which can cause instability. Soft-capping is a simple, effective stabilizer that became more common in 2024+ models.

#### Knowledge Distillation
Gemma 2 9B and 27B were trained with knowledge distillation from a larger (undisclosed) teacher model. The teacher's logits were used as a soft target, in addition to the standard next-token prediction loss. This improved quality significantly — Gemma 2 9B outperforms Gemma 1 7B despite being similar size.

#### Larger Sliding Window
For the local attention layers, Gemma 2 uses a sliding window of 4096 (vs Longformer's 512). The larger window captures more local context per layer.

### Key Results
Gemma 2 achieved strong quality:
- Gemma 2 9B: competitive with Llama 3 8B and Mistral 7B.
- Gemma 2 27B: competitive with Llama 3 70B on some benchmarks (despite being 2.5× smaller).

The quality-per-parameter efficiency was notable — Gemma 2 models punch above their weight class, partly due to knowledge distillation.

## CodeGemma (April 2024)

### Architecture
CodeGemma is Gemma fine-tuned for code:
- 2B and 7B variants.
- Trained on a code-heavy corpus (500B+ tokens of code).
- Supports code completion, generation, and understanding.
- Strong on HumanEval, MBPP, and other code benchmarks.

CodeGemma competes with CodeLlama, DeepSeek-Coder, and StarCoder2.

## RecurrentGemma (2024)

### Architecture
RecurrentGemma uses Google's **Griffin** architecture — a hybrid of RNN and attention:
- Most layers: **Recurrent gated attention** (an RNN-like mechanism with attention-like expressivity).
- Some layers: standard local attention.

The goal: O(1) memory per token (like an RNN) with attention-like quality. RecurrentGemma is Google's answer to Mamba and the linear-time architecture trend.

### Why RecurrentGemma?
- **Efficient inference**: O(1) memory per token, no KV cache growth.
- **Long context**: can handle arbitrarily long sequences (memory doesn't grow).
- **Quality**: competitive with standard Gemma on many tasks.

RecurrentGemma is less popular than standard Gemma but represents Google's exploration of alternative architectures.

## Gemma 3 (2025)

> [!info] Source Status
> Gemma 3 architecture details are **Officially Confirmed** in Google's announcements, but full technical details may not be completely published. This note reflects publicly available information as of mid-2025.

### Key Changes from Gemma 2
- **Multimodal**: native vision-language capability.
- **Larger context**: up to 128K.
- **Improved efficiency**: better attention implementation.
- **Multiple sizes**: including larger variants.

Gemma 3 aligns with the 2025 trend toward multimodal, long-context open-weights models.

## Why Gemma Matters

### Google's Open-Weights Presence
Before Gemma, Google's LLMs (LaMDA, PaLM, Gemini) were closed. Gemma gave Google an open-weights presence, competing with Meta (Llama) and Mistral. This matters for the open-source ecosystem — more competition means better models for everyone.

### Architectural Diversity
Gemma's choices (256K vocab, local+global attention, logit soft-capping, knowledge distillation) add diversity to the open-weights landscape. Not every model needs to follow the Llama template exactly; Gemma shows that variations can work.

### Knowledge Distillation as a Technique
Gemma 2's use of knowledge distillation (from a larger teacher) demonstrated that distillation can significantly improve small models. This technique is now widely used — distill a large model's knowledge into a smaller, deployable model.

### TPU Ecosystem
Gemma is trained on TPUs, not just GPUs. This provides an alternative to the NVIDIA-dominated GPU ecosystem and gives Google independence from GPU supply constraints.

## Comparison to Other Families

| Family    | Vocab  | Distillation? | Attention Pattern         |
|-----------|--------|---------------|---------------------------|
| Llama     | 32-128K| No            | Full (GQA)                |
| Mistral   | 32K    | No            | Sliding window + GQA      |
| Qwen      | 151K   | No            | Full (GQA)                |
| DeepSeek  | 100K   | No            | Full (MLA)                |
| Gemma 2   | 256K   | Yes           | Local + global alternating|

Gemma's distinctive features: largest vocab, knowledge distillation, alternating local/global attention.

## Impact and Legacy

Gemma's architectural influence:

1. **Validated knowledge distillation for open weights**. Gemma 2's quality (punching above its weight) showed that distillation is practical for open-weights, not just closed models.

2. **Popularized logit soft-capping**. The technique became more common after Gemma 2's success.

3. **Added architectural diversity**. The local+global attention pattern and large vocabulary provided alternatives to the Llama template.

4. **Google's open-weights commitment**. Gemma signaled that Google would participate in open-weights, not just closed APIs. This benefits the entire ecosystem.

For AI engineers, Gemma is a strong alternative to Llama/Mistral, especially for multilingual applications (large vocab) and cost-sensitive deployments (Gemma 2's efficiency). Understanding Gemma's architecture clarifies the design space beyond the Llama template.

## Further Reading

- Gemma 1 technical report: arXiv:2403.08295
- Gemma 2 technical report: arXiv:2408.00118
- RecurrentGemma: arXiv:2404.18402
- Google DeepMind blog: deepmind.google/technologies/gemma/

## See Also

- [[03 - Llama Family Architecture]]
- [[04 - Mistral and Mixtral Architecture]]
- [[05 - Qwen Family Architecture]]
- [[02 - Llama Mistral Qwen Comparison]]
- [[14 - GQA MQA MLA]]
- [[15 - Sliding Window Attention]]
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]
