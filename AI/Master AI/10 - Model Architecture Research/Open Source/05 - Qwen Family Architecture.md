---
tags: [model-architecture, qwen, multilingual, open-source]
iteration: 5
created: 2026-08-08
aliases: [Qwen Architecture, Qwen Family, Qwen 2 2.5 3 Architecture]
---

# 05 — Qwen Family Architecture

> [!info] TL;DR
> Qwen (Alibaba) is the leading Chinese open-weights LLM family, notable for strong multilingual capability (especially Chinese), large vocabulary (151K+), and early adoption of MoE. Architecturally similar to Llama (GQA, RoPE, SwiGLU, RMSNorm), Qwen differentiates through multilingual data, larger vocabularies, and MoE variants (Qwen 2.5 MoE, Qwen 3). All architectural details are **Officially Confirmed** in Alibaba's technical reports and model cards.

> [!info] Source Status
> All claims are **Officially Confirmed** — documented in Alibaba's Qwen technical reports (Qwen, Qwen 1.5, Qwen 2, Qwen 2.5) and model cards on HuggingFace.

## The Qwen Lineage

| Version   | Release       | Key Architectural Features                          |
|-----------|---------------|-----------------------------------------------------|
| Qwen 1    | 2023          | MHA, 32K vocab, RoPE, SwiGLU                       |
| Qwen 1.5  | Early 2024    | GQA, 151K vocab, larger context                     |
| Qwen 2    | Mid 2024      | GQA, 151K vocab, up to 128K context                 |
| Qwen 2.5  | Late 2024     | GQA, 151K vocab, MoE variants, up to 128K context   |
| Qwen 3    | 2025          | MoE, hybrid attention, larger sizes                 |

## Qwen 2 / 2.5 Architecture

### Standard (Dense) Variants

| Property            | Qwen 2.5 7B   | Qwen 2.5 14B  | Qwen 2.5 32B  | Qwen 2.5 72B  |
|---------------------|---------------|---------------|---------------|---------------|
| Parameters          | 7.6B          | 14.7B         | 32.8B         | 72.7B         |
| Layers              | 28            | 40            | 64            | 80            |
| d_model             | 3584          | 5120          | 5120          | 8192          |
| Heads               | 28            | 40            | 40            | 64            |
| KV heads            | 4 (GQA)       | 8 (GQA)       | 8 (GQA)       | 8 (GQA)       |
| Context             | 128K          | 128K          | 128K          | 128K          |
| Vocab               | 151K          | 151K          | 151K          | 151K          |
| RoPE base           | 1000000       | 1000000       | 1000000       | 1000000       |

### Key Architectural Choices

#### Large Vocabulary (151K)
Qwen uses a 151K vocabulary (vs Llama's 32K–128K). The larger vocabulary:
- Better supports Chinese (each character can be a token, vs being split into multiple bytes).
- Better supports other non-Latin scripts (Arabic, Korean, Japanese).
- Reduces sequence length for non-English text (fewer tokens per sentence).

The trade-off: larger embedding matrix (151K × d_model), which adds parameters and memory.

#### Aggressive GQA
Qwen uses very few KV heads (4 for the 7B model — only 1/7 of query heads). This is more aggressive than Llama 3 (8 KV heads) and gives larger KV cache reduction, at some quality cost. The trade-off works for Qwen's use cases (high-volume serving).

#### High RoPE Base
Qwen uses RoPE base 1,000,000 (vs Llama's 10,000–500,000). The higher base gives better length extrapolation — Qwen can handle 128K context from a model trained on shorter sequences.

#### SwiGLU and RMSNorm
Standard choices, same as Llama/Mistral.

### Qwen 2.5 MoE Variants

| Property            | Qwen 2.5 MoE-A14B | Qwen 2.5 MoE-A3B |
|---------------------|--------------------|-------------------|
| Total parameters    | 57B (A14B)         | 36B (A3B)         |
| Active per token    | 14B                | 3B                |
| Experts             | 60+                | 16                |
| Active experts      | 4-8                | 2-4               |
| Context             | 128K               | 128K              |

Qwen's MoE variants use more experts than Mixtral (60+ vs 8), with fewer active per token. This gives finer-grained specialization but more complex routing.

## Qwen 3 (2025)

> [!info] Source Status
> Qwen 3 architecture details are **Officially Confirmed** in Alibaba's announcements, but full technical details may not be completely published. This note reflects publicly available information as of mid-2025.

### Key Changes from Qwen 2.5
- **MoE as default** (not just a variant).
- **Hybrid attention** (linear + full attention, similar to Kimi Linear).
- **Larger sizes** (up to 480B+ total parameters).
- **Native multimodal** (vision-language).

Qwen 3 aligns with the 2025 trend toward MoE + hybrid architectures for long context and efficiency.

## Multilingual Capability

Qwen's standout feature is multilingual quality, especially for Chinese:

### Why Qwen Excels at Chinese
- **Training data**: Qwen is trained on a large Chinese corpus (Alibaba has access to Chinese web data, books, and proprietary content).
- **Tokenizer**: the 151K vocabulary includes many Chinese characters as single tokens, reducing sequence length and improving Chinese understanding.
- **Fine-tuning**: Qwen chat models are fine-tuned with Chinese instruction data.

### Multilingual Benchmarks
Qwen consistently outperforms Llama and Mistral on Chinese benchmarks (C-Eval, CMMLU) and is competitive on multilingual benchmarks (MGSM, FLORES). For Chinese-language applications, Qwen is often the best open-weights choice.

## Qwen Variants

### Qwen-VL (Vision-Language)
- Visual encoder (ViT) + Qwen LLM.
- Pretrained on image-text pairs.
- Strong on document understanding, chart reading, multilingual OCR.
- See [[03 - LLaVA]] for the general VLM pattern.

### Qwen-Coder
- Fine-tuned on code data (Starcoder-style).
- Strong on code generation, completion, and understanding.
- Supports many programming languages.

### Qwen-Math
- Fine-tuned on mathematical reasoning data.
- Strong on math benchmarks (MATH, GSM8K).
- Uses chain-of-thought reasoning.

### Qwen-Long
- Optimized for long-context applications.
- 10M+ token context (with file-based retrieval).
- Targets document analysis use cases.

## Why Qwen Matters

### Chinese AI Sovereignty
Qwen is China's leading open-weights LLM. It demonstrates that frontier-quality LLMs can be developed in China, despite US export controls on advanced GPUs. This has geopolitical implications — China's AI capability is a strategic concern, and Qwen shows that capability is real.

### Multilingual Representation
Most LLM research is English-centric. Qwen's strong Chinese (and other language) capability provides an alternative for non-English applications, reducing dependence on English-centric models.

### MoE Innovation
Qwen's MoE variants (especially Qwen 3) push MoE design — more experts, finer-grained routing, hybrid attention. This contributes to the broader MoE research community.

### Open Weights Despite Geopolitics
Alibaba releases Qwen weights openly (Apache 2.0 for most variants), even as US-China tech tensions escalate. This makes Qwen accessible globally, not just in China.

## Comparison to Other Families

| Family    | Vocab  | Chinese Quality | MoE? | Notable Feature            |
|-----------|--------|-----------------|------|-----------------------------|
| Llama     | 32-128K| Moderate        | Llama 4 | Conservative baseline   |
| Mistral   | 32K    | Weak            | Mixtral | SWA + MoE                |
| Qwen      | 151K   | Excellent       | Qwen 2.5+ | Multilingual + MoE     |
| DeepSeek  | 100K   | Excellent       | V2+  | MLA, auxiliary-loss-free   |
| Gemma     | 256K   | Moderate        | No   | Large vocab, GQA           |

Qwen and DeepSeek are the top choices for Chinese-language applications.

## Impact and Legacy

Qwen's architectural influence:

1. **Multilingual LLM design**. Qwen's large vocabulary and multilingual training data showed how to build LLMs that genuinely work across languages, not just English.

2. **Chinese open-weights ecosystem**. Qwen enabled a Chinese open-source LLM ecosystem parallel to the Western one. Chinese developers have access to frontier-quality open weights.

3. **MoE variety**. Qwen's MoE variants (many experts, fine routing) expanded the MoE design space beyond Mixtral's 8-expert approach.

4. **Competitive pressure**. Qwen's quality (especially Qwen 2.5 72B matching Llama 3.1 70B) pushed other labs to improve, accelerating the entire field.

For AI engineers, Qwen is the top choice for Chinese-language applications and a strong alternative to Llama/Mistral for multilingual use cases. Understanding Qwen's architecture clarifies how to build multilingual LLMs and how MoE design is evolving.

## Further Reading

- Qwen technical report: arXiv:2309.16609 (Qwen 1)
- Qwen 2: qwenlm.github.io/blog/qwen2/
- Qwen 2.5: qwenlm.github.io/blog/qwen2.5/
- [[02 - Llama Mistral Qwen Comparison]] — comparison note.

## See Also

- [[03 - Llama Family Architecture]]
- [[04 - Mistral and Mixtral Architecture]]
- [[02 - Llama Mistral Qwen Comparison]]
- [[14 - GQA MQA MLA]]
- [[15 - Mixture of Experts Transformer]]
- [[08 - RoPE]]
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]
