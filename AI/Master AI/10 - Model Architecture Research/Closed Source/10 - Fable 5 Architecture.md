---
tags: [model-architecture, fable, closed-source, speculative, 2026]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Fable 5 Architecture, Fable-5]
---

# 10 — Fable 5 Architecture

> [!info] TL;DR
> "Fable 5" is named in the master prompt §5 as one of the architecturally interesting 2026 models. **No public technical report exists.** No model card, paper, or official blog post has been published under the name "Fable 5" by any recognized AI lab. This note exists to document the source-verification status, the technical landscape in which such a model would sit, and what an architecture labelled "Fable 5" would need to disclose before this note can be filled in with real claims. Per the vault's no-fabrication policy (§22 of `What to do.md`), every architectural claim below is labeled **Speculative** until verified.

> [!warning] Source Status
> **Insufficient public evidence.** No official technical report, paper, model card, or credible leak has been found as of the iteration-13 audit (August 2026). The name appears only in the master prompt. Do **not** treat any architectural detail in this note as confirmed — every section is conditional on what such a model *would* look like if it followed the 2026 architectural landscape.

## What This Note Covers

This note exists for three reasons:
1. **Coverage completeness** — the master prompt §5 explicitly lists "Fable 5" alongside Opus 5, Mythos, GLM 5.2, Qwen 3.8, MiniMax 3, Kimi K3. Each must have a note so the vault's project-state files can record what has and hasn't been verified.
2. **Research-queue pointer** — every section ends with an explicit verification checklist that future iterations should resolve.
3. **Architectural template** — even without confirmed details, we can sketch what a 2026 frontier model in the "Fable 5" class would *plausibly* look like based on the convergent architectural trends documented across chapters 10 and 24.

## The 2026 Frontier Architectural Landscape

If a model called "Fable 5" is a 2026 frontier-class LLM, it almost certainly uses some combination of the following — all of which are documented in this vault:

| Component                | 2026 Default                                  | Source Note                                                    |
|--------------------------|-----------------------------------------------|----------------------------------------------------------------|
| Attention                | GQA, MLA, or hybrid linear/attention          | [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA]] |
| Positional encoding      | RoPE with YaRN or NTK-aware scaling            | [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling]] |
| Normalization            | RMSNorm (pre-norm)                            | [[07 - Transformers/Components/04 - Normalization Layers]]     |
| Activation               | SwiGLU                                        | [[07 - Transformers/Components/05 - Feed-Forward Network Deep]]|
| Sparse capacity          | MoE with aux-loss-free routing (DeepSeek-V3)  | [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture]] |
| Long context             | 1M+ tokens via Ring Attention or hybrid SSM   | [[24 - Research Frontiers/Long-Context/07 - Long-Context Architectures]] |
| Multimodal fusion        | Early-fusion native multimodal                 | [[23 - Multimodal AI/Vision-Language/01 - Multimodal AI Overview]] |
| Reasoning                | RL on verifiable rewards (R1-style)            | [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025]]                  |
| Inference acceleration   | EAGLE-3 spec decoding, FP8                    | [[26 - Papers/Efficient Attention/49 - Medusa and EAGLE 2024]]  |

A 2026 model that diverges from this recipe in a major way (e.g., pure attention without any sparse-capacity MoE, or pure SSM without any attention layers) would itself be the architectural novelty worth documenting. Without verified information, we cannot say which path "Fable 5" takes.

## Verification Checklist (for Future Iterations)

Before this note can carry any confirmed architectural claim, the following must be resolved:

- [ ] Locate the official developer (lab) publishing "Fable 5".
- [ ] Locate the technical report or model card.
- [ ] Confirm the architecture family: dense, MoE, hybrid SSM-Transformer, or other.
- [ ] Confirm parameter count and (if MoE) active-parameter count.
- [ ] Confirm attention mechanism: GQA, MLA, hybrid, or other.
- [ ] Confirm positional encoding and any long-context extension method.
- [ ] Confirm training compute (FLOPs) and dataset size.
- [ ] Confirm modalities supported: text-only, text+vision, native multimodal, or other.
- [ ] Confirm reasoning capability: base, SFT-only, or RL-on-verifiable-rewards.

If no public source can confirm any of the above, this note must remain in **Insufficient public evidence** status. The note will not be deleted — it stays as a marker that the gap was identified but unresolved.

## What "Fable 5" Might Be (Strongly Speculative)

The name "Fable" is not associated with any major lab's product line as of mid-2026. Possible interpretations:

1. **A research-internal codename at a frontier lab** that has not yet been publicly released. Several labs use storyteller names ("Minstrel", "Bard", "Scribe") internally. "Fable" fits this convention.
2. **A model from a smaller lab** whose release was missed by this audit. If so, the model would need to be verified through arXiv, HuggingFace, or a lab blog post.
3. **A future/hypothetical model** that the master prompt anticipates will exist by the iteration's date but has not yet been publicly announced.

In all three cases, this note cannot make factual architectural claims. Future iterations should re-check the [[00 - Vault Management/Research Queue|Research Queue]] entry for "Fable 5" and update this note when a public source appears.

## Why This Note Exists Despite Insufficient Evidence

Per `What to do.md` §22 (No Fabrication) and §23 (Avoid Destructive Changes), the vault must:
1. **Document the gap** — knowing that "Fable 5" was listed but unverifiable is itself useful state.
2. **Not invent architectural details** to fill the gap.
3. **Provide a verification target** so future iterations know what to look for.

This note is therefore mostly a research-queue entry dressed as a stub note. When verifiable sources emerge, this note will be expanded with the same depth as the other chapter-10 architecture notes.

## Connection to Other Concepts

- [[10 - Model Architecture Research/MOC]] — parent chapter.
- [[10 - Model Architecture Research/Closed Source/07 - GPT-4 Inferred Architecture]] — comparable closed-source treatment.
- [[10 - Model Architecture Research/Closed Source/08 - Claude Architecture]] — comparable closed-source treatment.
- [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture]] — the 2026 reference open-weights frontier.
- [[00 - Vault Management/Research Queue]] — research-queue entry for "Fable 5".
- [[00 - Vault Management/Architecture Decisions]] — ADR-006 (source-labelling convention).

## See Also

- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
- [[00 - Vault Management/Research Queue]]
