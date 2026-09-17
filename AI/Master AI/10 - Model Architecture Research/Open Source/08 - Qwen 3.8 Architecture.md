---
tags: [model-architecture, qwen, alibaba, open-source, moe, 2026]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Qwen 3.8 Architecture, Qwen3.8, Alibaba Qwen 3.8]
---

# 08 — Qwen 3.8 Architecture

> [!info] TL;DR
> Qwen 3.8 continues Alibaba's Qwen family lineage (Qwen → 1.5 → 2 → 2.5 → 3 → 3.5 → 3.8). Qwen 3 (2025) introduced MoE as default and hybrid attention; Qwen 3.8 is the 2026 mid-cycle update. **Source status: partially confirmed.** Alibaba has released Qwen 3 with technical reports, but no Qwen 3.8-specific technical report was found as of the iteration-13 audit (August 2026). Architectural claims here are extrapolated from the Qwen 3 trajectory.

> [!info] Source Status
> - Qwen 1, 1.5, 2, 2.5: **Officially Confirmed** — Alibaba technical reports and model cards.
> - Qwen 3 (2025): **Officially Confirmed** — Alibaba announcements and partial technical report; MoE as default, hybrid attention.
> - Qwen 3.5 / 3.8 (2026): **Strong inference** — extrapolated from Qwen 3. No public Qwen 3.8 technical report found.

## The Qwen Lineage

| Version   | Release       | Key Architectural Feature                                | Source Status             |
|-----------|---------------|---------------------------------------------------------|---------------------------|
| Qwen 1    | 2023          | MHA, 32K vocab, RoPE, SwiGLU                           | Officially Confirmed      |
| Qwen 1.5  | Early 2024    | GQA, 151K vocab, larger context                        | Officially Confirmed      |
| Qwen 2    | Mid 2024      | GQA, 151K vocab, up to 128K context                    | Officially Confirmed      |
| Qwen 2.5  | Late 2024     | GQA, MoE variants, up to 128K context                  | Officially Confirmed      |
| Qwen 3    | 2025          | MoE default, hybrid attention, larger sizes             | Officially Confirmed      |
| Qwen 3.5  | Early 2026    | Mid-cycle update                                        | Strong inference          |
| Qwen 3.8  | 2026          | Mid-cycle update (named in master prompt §5)            | Strong inference          |

## What Is Known About Qwen 3 (Verified Generation)

These are **Officially Confirmed** from Alibaba's Qwen 3 announcements and model cards:

### MoE as Default
Qwen 3 made MoE the default architecture (not just a variant, as in Qwen 2.5). All flagship Qwen 3 models are MoE; only smaller models (e.g., Qwen 3 4B) are dense.

### Hybrid Attention
Qwen 3 introduced hybrid attention: most layers use a linear/sparse attention variant, with periodic full-attention layers for retrieval and in-context learning. This is the same pattern as Kimi Linear, MiniMax-01, and GLM-4.5.

### Reasoning Variant (Qwen3-Thinking)
Qwen 3 released a "thinking" variant trained with RL on verifiable rewards — Qwen's answer to R1 and o1.

### Multimodal Variants
Qwen 3 has separate vision-language (Qwen3-VL), audio (Qwen3-Audio), and code (Qwen3-Coder) variants.

## Architectural Expectations for Qwen 3.8

> [!warning] The following are strong inferences, not confirmed facts.

### Refinement of Qwen 3 Architecture (Strong Inference)
Qwen 3.8 is expected to be a refinement of Qwen 3, not a fundamentally new architecture. Mid-cycle updates typically:
- Adjust expert counts and active-expert ratios.
- Refine the hybrid attention schedule (more or fewer full-attention layers).
- Extend context length.
- Improve the reasoning training recipe.

### Reasoning Capability (Strong Inference)
Qwen 3-Thinking will likely be carried forward into Qwen 3.8-Thinking (or thinking mode built into the base Qwen 3.8). The reasoning recipe (GRPO on verifiable rewards) is by now standard across Chinese open-weights labs (DeepSeek-R1, Kimi K1.5, Qwen-Thinking).

### Multimodal Consolidation (Speculative)
Qwen 3 has separate VL, audio, and code variants. Qwen 3.8 may consolidate these into the base model — making it natively multimodal. This is the 2026 frontier pattern.

### Longer Context (Strong Inference)
Qwen 3 supports 128K–256K context. Qwen 3.8 is expected to extend this to 512K–1M tokens, matching Gemini 1.5/2.0 and Kimi Linear.

## The Qwen 3 Architecture (Reference for 3.8)

### MoE Configuration

| Property            | Qwen 3 30B-A3B (MoE) | Qwen 3 235B-A22B (MoE flagship) |
|---------------------|----------------------|----------------------------------|
| Total parameters    | 30B                  | 235B                             |
| Active per token    | 3B                   | 22B                              |
| Experts             | 128                  | 94                               |
| Active experts      | 8                    | 8                                |
| Shared experts      | 0                    | 4                                |
| Context             | 128K                 | 128K                             |
| Vocab               | 151K                 | 151K                             |
| RoPE base           | 1000000              | 1000000                          |

### Hybrid Attention Schedule
Qwen 3 uses a periodic full-attention schedule: roughly 1 in every 4 layers uses full attention; the other 3 use sparse/linear attention. The exact pattern is documented in the Qwen 3 technical report.

## Why Qwen 3.8 Matters Architecturally

1. **Chinese open-weights frontier** — Qwen is Alibaba's flagship, alongside DeepSeek (DeepSeek-V3/R1) and Zhipu (GLM-4.5). Qwen 3.8 represents another data point in the Chinese open-weights MoE+hybrid landscape.

2. **Aggressive MoE sparsity** — Qwen 3 30B-A3B has a 10:1 sparsity ratio; the flagship 235B-A22B has ~11:1. This approaches DeepSeek-V3's 18:1 and is much more aggressive than Mixtral 8x22B's 3.25:1.

3. **Hybrid attention at scale** — Qwen 3's hybrid attention schedule is the most aggressive among major open-weights models. Qwen 3.8's specific recipe — if disclosed — would be a major reference for the 2026 hybrid-attention landscape.

4. **Multilingual strength** — Qwen's 151K vocabulary supports Chinese, Arabic, Korean, Japanese, and other non-Latin scripts natively. Qwen 3.8 is expected to retain this strength.

## Verification Checklist

- [ ] Locate Qwen 3.8 technical report (Alibaba DAMO blog or arXiv).
- [ ] Confirm MoE configuration (experts, active experts, shared experts).
- [ ] Confirm hybrid attention schedule.
- [ ] Confirm context length.
- [ ] Confirm reasoning variant (Qwen 3.8-Thinking?).
- [ ] Confirm multimodal consolidation (if any).
- [ ] Compare benchmarks to Qwen 3 on standard evals (MMLU, GPQA, AIME, SWE-bench).

## Production Implications (Speculative)

- **Serving**: Qwen 3 is supported in vLLM and SGLang with MoE + hybrid attention kernels. Qwen 3.8 serving should follow the same pattern.
- **Cost**: Qwen 3 30B-A3B is extremely cost-effective (only 3B active per token). Qwen 3.8's small variant should retain this advantage.
- **Multilingual**: Qwen 3.8 should remain the strongest open-weights model for Chinese-language applications.
- **Open weights**: Alibaba has consistently released Qwen weights openly. Qwen 3.8 should follow this pattern.

## Common Pitfalls

- **Confusing Qwen 3.8 with Qwen 3** — they may have different MoE configurations or hybrid attention schedules. Verify before assuming continuity.
- **Assuming "Qwen 3.8" is the official name** — Alibaba may release under a different name (e.g., "Qwen 4" or "Qwen 3.5"). The "3.8" label comes from the master prompt §5.
- **Assuming multimodal is consolidated** — Qwen 3 has separate VL/audio/code variants. Qwen 3.8 may or may not consolidate.

## Connection to Other Concepts

- [[10 - Model Architecture Research/Open Source/05 - Qwen Family Architecture]] — Qwen family overview.
- [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture]] — comparable Chinese open-weights MoE.
- [[10 - Model Architecture Research/Open Source/07 - GLM 5.2 Architecture]] — comparable Chinese open-weights MoE.
- [[26 - Papers/2024-2026/30 - Kimi Linear 2025]] — comparable hybrid attention.
- [[26 - Papers/2024-2026/43 - MiniMax-01 2025]] — comparable hybrid attention at frontier scale.
- [[10 - Model Architecture Research/MOC]] — parent chapter.

## See Also

- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
- [[00 - Vault Management/Research Queue]]
