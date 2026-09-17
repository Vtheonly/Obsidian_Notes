---
tags: [model-architecture, claude, opus, anthropic, closed-source, 2026]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Opus 5 Architecture, Claude Opus 5, Claude 5 Opus]
---

# 12 — Opus 5 Architecture (Anthropic)

> [!info] TL;DR
> Opus 5 is the next-generation frontier model in Anthropic's Claude lineage (Claude 1 → 2 → 3 → 3.5 → 3.7 → 4 → 5 Opus). Anthropic has consistently published less architectural detail than competitors; even Claude 3's parameter count and expert configuration are undisclosed. Opus 5 is **expected** to continue Anthropic's pattern of constitutional-AI alignment + frontier-scale reasoning capability, but **no official technical report exists** as of the iteration-13 audit (August 2026). This note documents the trajectory, the verification status, and what is known vs inferred.

> [!warning] Source Status
> - Claude 1/2/3/3.5/3.7: **Strongly inferred** — Anthropic disclosed capability and high-level training recipe (constitutional AI, RLHF) but never architecture (parameter count, MoE config, attention variant).
> - Claude 4 (2025): **Strongly inferred** — Anthropic released Claude 4 with extended thinking capability; architectural details remain undisclosed.
> - Opus 5 (2026): **Insufficient public evidence** — no model card, no technical report, no credible leak with verifiable architectural detail. Treat every architectural claim in this note as speculative.

## The Claude Lineage

| Version      | Release       | Notable Capability                                            | Architectural Disclosure |
|--------------|---------------|--------------------------------------------------------------|---------------------------|
| Claude 1     | Early 2023    | First Claude; 9K context                                      | None                      |
| Claude 2     | Mid 2023      | 100K context; document Q&A                                    | None                      |
| Claude 2.1   | Late 2023     | Reduced hallucination; improved long-context                  | None                      |
| Claude 3     | Early 2024    | Haiku/Sonnet/Opus tier; 200K context; vision                  | None                      |
| Claude 3.5   | Mid 2024      | Sonnet (and later Haiku); improved coding                     | None                      |
| Claude 3.7   | Early 2025    | "Extended thinking" mode (visible CoT)                       | None                      |
| Claude 4    | Mid 2025      | Opus 4 / Sonnet 4; tool use; agentic                          | None                      |
| Opus 5       | 2026 (expected)| Next generation                                              | None                      |

Anthropic's pattern is clear: they release capabilities (long context, extended thinking, tool use, agentic systems) but never disclose architecture (parameter count, MoE, attention mechanism). This is the opposite of Google (partial disclosure via papers) and DeepSeek (full disclosure via technical reports).

## What Is Known (Anthropic's Public Statements)

These are **Officially Confirmed** because Anthropic has stated them publicly:

### Constitutional AI Training
Anthropic's published Constitutional AI paper (2022, [[26 - Papers/Alignment/31 - Constitutional AI 2022]]) describes using AI feedback (against a written constitution) instead of pure human feedback. This remains Anthropic's stated alignment method.

### Multimodal Capability
Claude 3+ supports vision input (images, documents). Anthropic has stated this is integrated rather than bolted-on, but the integration mechanism (early fusion vs cross-attention vs projector) is undisclosed.

### Long Context
Claude 2.1 introduced 200K context. The mechanism (sparse attention, sliding window, hybrid, or other) is not disclosed.

### Extended Thinking (3.7+)
Claude 3.7 introduced "extended thinking" — a visible chain-of-thought mode similar to o1's reasoning. The training method (RL on verifiable rewards? Self-distillation? Other?) is not disclosed. Anthropic has stated only that the model "thinks before answering" and the thinking is visible to the user.

## What Is Strongly Inferred

### Decoder-Only Transformer Base
**Evidence**: Anthropic has described Claude as Transformer-based; the dominant pattern for frontier LLMs is decoder-only. The Claude 3 model card describes a Transformer architecture consistent with the GPT/Llama lineage.

**Inference**: Claude uses a decoder-only Transformer backbone (like GPT-4, Gemini, Llama), not an encoder-decoder (like T5 or the original Transformer).

### Likely MoE at Opus Scale
**Evidence**: frontier models at GPT-4 / Claude 3 Opus / Gemini Ultra scale are almost certainly MoE — a dense model at trillion-parameter scale would be uneconomical to serve. Mixtral 8x22B, DeepSeek-V3, and Gemini 1.5 are all confirmed MoE. Claude's "Opus" tier (most expensive, most capable) is consistent with MoE.

**Inference**: Opus 5 is likely MoE, with hundreds of billions of total parameters and tens of billions of active parameters per token. Specific expert count, active-expert count, and routing mechanism are not known.

### Pre-Norm + RMSNorm + RoPE + SwiGLU
**Evidence**: these are the standard 2023–2026 LLM components. The Claude 3 model card and Anthropic papers describe a "modern Transformer architecture" without specifying the details. Pre-norm + RMSNorm + RoPE + SwiGLU is what every open-weights frontier model uses (Llama, Mistral, Qwen, DeepSeek, Gemma).

**Inference**: Opus 5 uses variations of this standard recipe. The exact RoPE base, normalization placement, and SwiGLU variant are not known.

### Hybrid SSM-Transformer (Speculative)
**Evidence**: Anthropic has not announced any hybrid SSM-Transformer work. However, given the 2025–2026 trend (Jamba, Kimi Linear, MiniMax-01, Mamba-2), a frontier-scale hybrid model is plausible. If Opus 5 uses hybrid, it would be the first Anthropic model to do so.

**Status**: Speculative. No evidence either way.

## What Is Not Disclosed

- Parameter count (total or active).
- Expert count or routing mechanism.
- Attention variant (MHA, GQA, MQA, MLA).
- Positional encoding (RoPE, ALiBi, or other).
- Long-context mechanism.
- Training compute (FLOPs) or dataset.
- Whether the base model is dense, MoE, or hybrid SSM-Transformer.

## Verification Checklist

- [ ] Anthropic technical report for Opus 5 (will likely **not** appear — Anthropic does not publish them).
- [ ] Anthropic blog post announcing Opus 5 (likely the only public source).
- [ ] Capability benchmarks (MMLU, GPQA, SWE-bench, AIME) — published via the announcement.
- [ ] API release (Anthropic API + Amazon Bedrock + Google Vertex).
- [ ] Pricing (input/output per million tokens).
- [ ] Context window size.

## Why This Note Matters

Even without architectural disclosure, the Claude lineage is architecturally significant because:

1. **Constitutional AI** — Anthropic pioneered the AI-feedback alignment recipe (an alternative to OpenAI's RLHF-on-human-feedback). Whether Opus 5 still uses Constitutional AI or has moved to verifiable-reward RL is an open question.

2. **Extended thinking** — Claude 3.7 was one of the first models to make the reasoning trace visible to the user (vs o1's hidden CoT). If Opus 5 extends this with deeper reasoning capability, it represents the open-CoT branch of reasoning model design.

3. **Agentic capability** — Anthropic's Computer Use (Claude 3.5+) was a frontier demonstration of agentic capability (controlling a computer via screenshots). Opus 5 is expected to push this further.

## Production Implications (Speculative)

- **API-only access**: Opus 5 will likely be API-only (no open weights). Production deployments pay per-token.
- **Pricing**: expect $15–$75 per million input tokens (Claude 3 Opus was $15; if Opus 5 introduces a higher tier for reasoning, it could approach o1's $60+ rate).
- **Tool use**: Claude's tool use is among the best-documented in production. Opus 5 should continue this pattern.
- **Multimodal**: vision input is standard for Claude 3+; Opus 5 should support images and documents natively.

## Common Pitfalls

- **Assuming Opus 5 uses the same architecture as Claude 3** — Anthropic may have changed attention mechanism, MoE config, or training recipe between generations.
- **Assuming Opus 5's reasoning is GRPO-based** — Anthropic has not disclosed their reasoning training method; it could be PPO, GRPO, or something proprietary.
- **Confusing "Claude 5 Opus" with "Claude 5 Sonnet"** — Anthropic releases multiple tiers per generation. Opus 5 (largest, most expensive) is different from Sonnet 5 (medium) and Haiku 5 (smallest).

## Connection to Other Concepts

- [[10 - Model Architecture Research/Closed Source/08 - Claude Architecture]] — Claude family architecture overview.
- [[26 - Papers/Alignment/31 - Constitutional AI 2022]] — Anthropic's alignment method.
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]] — reasoning model category.
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling]] — extended thinking context.
- [[22 - Production AI/Security/01 - LLM Security and Prompt Injection]] — Claude-specific security considerations.
- [[10 - Model Architecture Research/MOC]] — parent chapter.

## See Also

- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
- [[00 - Vault Management/Research Queue]]
