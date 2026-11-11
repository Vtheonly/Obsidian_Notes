---
tags: [model-architecture, claude, anthropic, closed-source, inferred]
iteration: 5
created: 2026-08-08
aliases: [Claude Architecture, Claude 3 3.5 4 Architecture]
---

# 08 — Claude Architecture

> [!info] TL;DR
> Anthropic has not officially disclosed Claude's architecture. Public statements indicate Claude uses a Transformer-based architecture with Constitutional AI (RLAIF) alignment. Specific details — parameter count, dense vs MoE, attention variants — are **not publicly disclosed**. This note summarizes what's known, what's inferred, and what's speculative, per ADR-006 source-labelling.

> [!warning] Source Status
> **Most architectural claims about Claude are Strongly Inferred or Speculative.** Anthropic has published the Constitutional AI method (see [[31 - Constitutional AI 2022]]) and general capabilities, but not Claude's specific architecture. Treat all architectural details as unverified.

## What's Officially Confirmed

Anthropic has publicly stated:
- Claude is a Transformer-based LLM (no specific architecture details).
- Claude is trained with **Constitutional AI** (RLAIF) — Anthropic's alignment method. See [[31 - Constitutional AI 2022]].
- Claude supports long context (200K tokens for Claude 3, 3.5; longer for some variants).
- Claude 3.7+ has an "extended thinking" mode (controllable reasoning length).
- Claude is multimodal (vision-language) starting from Claude 3.

The Constitutional AI paper describes the alignment method but not the base model architecture.

## What's Strongly Inferred

### Transformer-Based, Likely Decoder-Only
**Evidence**:
- All major LLMs since 2018 are Transformer-based.
- Decoder-only is the dominant architecture (GPT, Llama, Mistral, Qwen all use it).
- Claude's generation quality and style are consistent with decoder-only models.

**Inference**: Claude is a decoder-only Transformer, likely with components similar to other frontier LLMs (pre-norm, RMSNorm, RoPE or similar, SwiGLU, GQA).

### Parameter Scale (Hundreds of Billions)
**Evidence**:
- Claude 3 Opus's capability is comparable to GPT-4 (which is inferred to be ~1.7T MoE).
- Claude 3 Opus's pricing is similar to GPT-4's, suggesting similar compute per token.
- Claude 3 Sonnet and Haiku are smaller (cheaper, faster), suggesting a family of sizes.

**Inference**: Claude 3 Opus is likely in the 500B–1T+ parameter range (either dense or MoE). Sonnet and Haiku are smaller. Specific numbers are not confirmed.

### Possible Mixture-of-Experts
**Evidence**:
- Claude 3 Opus's cost is higher than a typical dense model of similar capability, similar to GPT-4.
- MoE has become standard for frontier-scale models (GPT-4 inferred, DeepSeek-V3 confirmed).
- The capability-per-cost ratio suggests sparse computation.

**Inference**: Claude 3 Opus may use MoE, but this is more speculative than for GPT-4. Anthropic has not indicated this.

### Constitutional AI as the Alignment Method
**Evidence**:
- Anthropic published the Constitutional AI paper (see [[31 - Constitutional AI 2022]]).
- Anthropic's public statements emphasize the constitutional approach.
- Claude's behavior (thoughtful, harm-averse) is consistent with constitutional alignment.

**Inference**: Claude is aligned using Constitutional AI (RLAIF), possibly combined with traditional RLHF. The specific constitution (set of principles) is partially public but may have evolved.

### Long Context via Efficient Attention
**Evidence**:
- Claude 3 supports 200K context, comparable to GPT-4 Turbo (128K) and Gemini 1.5 (1M).
- This requires efficient attention techniques (sliding window, sparse attention, Ring Attention, or similar).

**Inference**: Claude uses some form of efficient or distributed attention for long contexts. The specific technique is not disclosed.

## What's Speculative

### Specific Parameter Counts
Any specific number (e.g., "Claude 3 Opus is 820B parameters") is speculative. Anthropic has not disclosed any parameter counts.

### Specific Architecture Components
Whether Claude uses GQA, MLA, sliding window, or other specific techniques is not known. Inferences based on capability patterns are speculative.

### Training Data
Claude's training data is not disclosed. Anthropic has stated it uses web data, books, and code, but specific datasets and proportions are not public.

### "Extended Thinking" Mechanism
Claude 3.7's extended thinking mode (similar to o1's reasoning) is not architecturally described. It could be:
- RL-trained extended chain-of-thought (like o1/R1).
- A prompting technique that elicits longer reasoning.
- A separate reasoning model combined with Claude.

The mechanism is not officially disclosed.

## The Claude Family

### Claude 1 (March 2023)
- Anthropic's first public model.
- 9K context.
- Trained with Constitutional AI.
- Architecture not disclosed.

### Claude 2 (July 2023)
- 100K context (significant jump).
- Improved capability.
- Architecture not disclosed.

### Claude 3 (March 2024)
- Three sizes: Haiku (small/fast), Sonnet (medium), Opus (large/frontier).
- 200K context.
- Multimodal (vision).
- Architecture not disclosed.

### Claude 3.5 (October 2024)
- Improved Sonnet and Haiku.
- Computer use capability (can interact with desktops).
- Architecture not disclosed.

### Claude 3.7 (February 2025)
- "Extended thinking" mode (controllable reasoning length).
- Hybrid reasoning: standard or extended thinking, selectable per request.
- Architecture not disclosed.

### Claude 4 (2025)
- Latest generation.
- Improved capability and reasoning.
- Architecture not disclosed.

## Why Anthropic Doesn't Disclose Architecture

Anthropic's stated reasons:
1. **Safety**: Anthropic is a safety-focused company and believes architecture disclosure could enable misuse.
2. **Competitive**: disclosure helps competitors.
3. **Research focus**: Anthropic publishes research (Constitutional AI, interpretability) but keeps product architecture private.

Anthropic is more transparent than OpenAI about research (publishing the Constitutional AI paper, interpretability research) but equally opaque about product architecture.

## Comparison to Other Closed Models

| Model     | Architecture Disclosure | Alignment Method         |
|-----------|-------------------------|--------------------------|
| GPT-4     | None                    | RLHF (outcome + process?)|
| Claude    | None                    | Constitutional AI (RLAIF)|
| Gemini    | Partial (papers)        | RLHF + other             |

Claude's distinctive feature is Constitutional AI — the alignment method is public even though the architecture isn't.

## Implications for AI Engineers

### You Don't Need Claude's Architecture
For most applications, Claude's API contract (input → output) is what matters, not the internal architecture. You can build production applications without knowing the architecture.

### Constitutional AI Is the Key Differentiator
Claude's behavior (thoughtful, harm-averse, honest) is largely due to Constitutional AI, not the base architecture. Understanding Constitutional AI (see [[31 - Constitutional AI 2022]]) tells you more about Claude's behavior than architecture details would.

### Open Models for Architecture Research
If you need architectural transparency (interpretability, custom training, architecture research), use open models. Claude is unsuitable for these purposes.

### Claude's Strengths Are Behavioral
Claude is known for:
- Long, thoughtful responses.
- Strong harm avoidance.
- Good instruction following.
- Excellent coding and reasoning.

These are behavioral properties, not architectural ones. You can evaluate them through the API without knowing the architecture.

## Future Disclosure

Anthropic is unlikely to disclose Claude's architecture in the near future. However:
- Anthropic publishes research on interpretability and alignment, which may eventually reveal architectural details.
- As open models catch up, the competitive sensitivity of disclosure decreases.
- Regulatory pressure (e.g., EU AI Act) may eventually require more transparency.

## See Also

- [[31 - Constitutional AI 2022]] — Claude's alignment method.
- [[07 - GPT-4 Inferred Architecture]] — comparison to GPT-4.
- [[09 - Gemini Architecture]] — comparison to Gemini.
- [[03 - Llama Family Architecture]] — open-weights alternative.
- [[00 - Vault Management/Research Queue|Research Queue]] — open questions.
- [[10 - Model Architecture Research/MOC|10 Model Architecture MOC]]
