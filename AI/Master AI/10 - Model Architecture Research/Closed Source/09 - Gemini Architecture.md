---
tags: [model-architecture, gemini, google, closed-source, partial-disclosure]
iteration: 5
created: 2026-08-08
aliases: [Gemini Architecture, Gemini 1 1.5 2 Architecture]
---

# 09 — Gemini Architecture

> [!info] TL;DR
> Google's Gemini is the most architecturally transparent of the closed-source frontier models — Google has published a paper (Gemini 1) and technical reports with partial architecture details. Gemini is **Officially Confirmed** to be multimodal-native (trained on text, images, audio, video from the start), MoE in some versions, and capable of 1M+ token context (Gemini 1.5). This note summarizes what Google has disclosed and what remains private.

> [!info] Source Status
> Some claims are **Officially Confirmed** (from the Gemini 1 paper and Gemini 1.5 technical report). Others are **Strongly Inferred** (capability-based inferences not in the papers). The note distinguishes these.

## What's Officially Confirmed

Google published the Gemini 1 paper (December 2023) and the Gemini 1.5 technical report (February 2024), which disclosed:

### Multimodal-Native Training
**Officially Confirmed**: Gemini is trained from the start on multiple modalities — text, images, audio, video — not fine-tuned for multimodality after text training. The model processes all modalities in a single architecture, not separate encoders combined.

This is a key architectural distinction. GPT-4 (inferred) and Claude (inferred) may have added vision capability through fine-tuning or a separate vision encoder. Gemini was designed for multimodality from the start.

### Model Family (Ultra, Pro, Flash, Nano)
**Officially Confirmed**: Gemini comes in multiple sizes:
- **Gemini Ultra**: largest, frontier-quality, for complex reasoning.
- **Gemini Pro**: medium, balanced quality and cost.
- **Gemini Flash**: optimized for speed and cost.
- **Gemini Nano**: small, on-device (Pixel phones).

### Long Context (1M+ Tokens for Gemini 1.5)
**Officially Confirmed**: Gemini 1.5 Pro supports 1M+ token context, the longest of any frontier model. The technical report describes this as enabled by efficient attention (likely Ring Attention or similar distributed approach) and mixture-of-Experts architecture.

### Mixture-of-Experts (Gemini 1.5)
**Officially Confirmed**: Gemini 1.5 Pro uses a Mixture-of-Experts architecture. The technical report describes this as enabling "efficient inference" at the 1M+ context scale. Specific expert count and routing are not disclosed.

## What's Strongly Inferred

### Decoder-Only Transformer Base
**Evidence**: Gemini is described as Transformer-based, and the dominant architecture for frontier LLMs is decoder-only. The Gemini paper's description of "Transformer-based architecture" is consistent with decoder-only.

**Inference**: Gemini is a decoder-only Transformer (like GPT-4, Claude, Llama), not an encoder-decoder (like the original Transformer or T5).

### Specific Architectural Components
**Evidence**: Gemini likely uses the standard 2023–2024 LLM components — pre-norm, RMSNorm, RoPE, SwiGLU, GQA — based on what was standard when Gemini was developed.

**Inference**: Gemini uses variations of the standard Llama-era architecture, with multimodal extensions for vision/audio input. Specific choices are not confirmed.

### Training Compute
**Evidence**: Gemini Ultra is described as competitive with GPT-4, suggesting similar training compute (~10²⁵ FLOPs).

**Inference**: Gemini Ultra was trained with ~10²⁵ FLOPs, comparable to GPT-4. Not officially confirmed.

### Vision Encoder Integration
**Evidence**: Gemini's vision capability is fluent (not bolted-on), suggesting deep integration of vision into the Transformer.

**Inference**: Gemini likely uses early fusion (vision tokens concatenated with text tokens, processed by the same Transformer) rather than cross-attention (separate vision encoder, attended to by the text decoder). See [[06 - Cross-Modal Attention]] for the fusion patterns.

## What's Not Disclosed

### Exact Parameter Counts
Google has not disclosed parameter counts for any Gemini model. Estimates based on capability and cost suggest Gemini Ultra is in the 500B–1T+ range, but this is speculative.

### Specific MoE Configuration
The Gemini 1.5 paper confirms MoE but doesn't specify expert count, active experts, or routing mechanism. DeepSeek-V3 uses 256 experts with 8 active; Gemini 1.5's configuration is unknown.

### Specific Attention Mechanism for Long Context
The 1M+ context requires efficient attention, but the specific technique (Ring Attention, sparse attention, sliding window, hybrid) is not disclosed.

### Training Data
Google has stated Gemini is trained on web data, books, code, and multimodal data, but specific datasets and proportions are not public.

## The Gemini Family Evolution

### Gemini 1 (December 2023)
- Three sizes: Ultra, Pro, Nano.
- Multimodal-native (text, image, audio, video).
- Trained on Google's TPUs.
- Architecture partially disclosed in the paper.

### Gemini 1.5 (February 2024)
- Pro and Flash variants.
- 1M+ token context (Pro).
- **Officially Confirmed MoE** architecture.
- Improved efficiency over Gemini 1.

### Gemini 2.0 (December 2024)
- Improved multimodal capability.
- Native multimodal output (can generate images, audio).
- Agentic capabilities (tool use, multi-step planning).
- Architecture not detailed beyond what was disclosed for Gemini 1.5.

### Gemini 2.5 (2025)
- "Thinking" mode (extended reasoning, similar to o1/Claude 3.7).
- Improved coding and math capability.
- Architecture not detailed.

## Why Gemini Is More Transparent Than GPT-4/Claude

Google's relative transparency reflects:
1. **Research culture**: Google DeepMind publishes research papers (the Gemini 1 paper, the Gemini 1.5 report). This is standard academic practice.
2. **Different competitive position**: Google competes on ecosystem (Google Cloud, Vertex AI), not just on model capability. Transparency supports the ecosystem.
3. **Regulatory comfort**: Google is more comfortable with regulatory scrutiny (decades of experience with search, ads) than newer AI labs.

However, Google still withholds key details (parameter counts, specific architectures) — the transparency is partial, not complete.

## Comparison to Other Closed Models

| Model     | Architecture Disclosure | Multimodal-Native? | MoE? | Long Context |
|-----------|-------------------------|--------------------|------|--------------|
| GPT-4     | None                    | Likely added       | Inferred | 128K        |
| Claude    | None                    | Likely added       | Unknown | 200K         |
| Gemini    | Partial (papers)        | Yes (confirmed)    | Yes (1.5+) | 1M+ (1.5 Pro)|

Gemini is the most transparent and the only one with officially confirmed multimodal-native training and MoE.

## Implications for AI Engineers

### Gemini's Multimodal Advantage
Because Gemini is multimodal-native, it may handle multimodal tasks (video understanding, audio analysis) more naturally than models that added vision later. For multimodal-heavy applications, Gemini is worth evaluating.

### Long Context Leadership
Gemini 1.5 Pro's 1M+ context is the longest officially available. For applications requiring extreme context (full codebases, long videos, large document sets), Gemini may be the best choice.

### Open-Weights Alternatives
For architectural transparency, open models (Llama 3.1, DeepSeek-V3, Qwen 2.5) are alternatives. They don't match Gemini's multimodal capability or 1M+ context, but they have known architectures and can be self-hosted.

### Google Cloud Integration
Gemini is deeply integrated with Google Cloud (Vertex AI). If you're already on Google Cloud, Gemini is the natural choice. If you're on AWS or Azure, GPT-4 (Azure) or Claude (AWS Bedrock) may be more convenient.

## Future Disclosure

Google may continue to disclose architecture details over time:
- The Gemini 1 paper was a significant disclosure; subsequent versions may follow.
- Open model progress (Llama, DeepSeek) reduces the competitive sensitivity of disclosure.
- Regulatory pressure may require more transparency.

For now, Gemini is the most transparent closed-source frontier model, but still not fully open.

## See Also

- [[07 - GPT-4 Inferred Architecture]] — comparison to GPT-4.
- [[08 - Claude Architecture]] — comparison to Claude.
- [[03 - Llama Family Architecture]] — open-weights alternative.
- [[28 - DeepSeek-V2 and V3 2024]] — open MoE comparison.
- [[06 - Cross-Modal Attention]] — multimodal fusion.
- [[15 - Mixture of Experts Transformer]] — MoE concept.
- [[00 - Vault Management/Research Queue|Research Queue]] — open questions.
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]
