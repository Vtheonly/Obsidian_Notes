---
tags: [model-architecture, minimax, hybrid, long-context, open-source, 2026]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [MiniMax 3 Architecture, MiniMax-3, MiniMax 03]
---

# 09 — MiniMax 3 Architecture

> [!info] TL;DR
> MiniMax 3 continues MiniMax's lineage (MiniMax-01, MiniMax-Text-01, MiniMax-3). MiniMax-01 (2025) was the first open-weights model to demonstrate million-token context using a hybrid lightning-attention + softmax-attention architecture. MiniMax 3 is the 2026 successor. **Source status: partially confirmed.** MiniMax published a MiniMax-01 technical report (Jan 2025), but no MiniMax 3 technical report was found as of the iteration-13 audit (August 2026). Architectural claims here are extrapolated from the MiniMax-01 trajectory.

> [!info] Source Status
> - MiniMax-Text-01 (2025): **Officially Confirmed** in MiniMax technical report (456B total, 45.9B active, 1M context, hybrid lightning+softmax attention).
> - MiniMax-M1 (2025): **Officially Confirmed** — reasoning variant, MoE + lightning attention.
> - MiniMax 3 (2026): **Strong inference** — extrapolated from MiniMax-01/M1. No public MiniMax 3 technical report found.

## The MiniMax Lineage

| Version         | Release       | Key Architectural Feature                                | Source Status             |
|-----------------|---------------|---------------------------------------------------------|---------------------------|
| abab-6          | 2023          | Standard Transformer; MoE                                | Officially Confirmed      |
| abab-6.5        | 2024          | Larger MoE                                              | Officially Confirmed      |
| MiniMax-Text-01 | Jan 2025      | Hybrid lightning+softmax attention; 1M context; 456B MoE | Officially Confirmed      |
| MiniMax-M1      | Mid 2025      | Reasoning variant; hybrid attention + test-time scaling   | Officially Confirmed      |
| MiniMax 3       | 2026          | Next generation; details not fully public                | Strong inference          |

## What Is Known About MiniMax-01 (Verified Generation)

These are **Officially Confirmed** from the MiniMax-01 technical report (January 2025):

### Hybrid Lightning + Softmax Attention
MiniMax-01 introduced a hybrid attention pattern: most layers use **lightning attention** (a linear-attention variant with a specific kernel-friendly formulation), with periodic **softmax attention** layers for retrieval. The ratio is roughly 7:1 (lightning:softmax), similar to Jamba's SSM:attention ratio.

### MoE Architecture
- 456B total parameters.
- 45.9B active per token.
- 32 experts, 2 active per token (plus shared experts).
- Auxiliary-loss-free load balancing (same innovation as DeepSeek-V3).

### 1M Token Context
MiniMax-01 was the first open-weights model to support 1M token context natively. This is enabled by the hybrid attention: lightning attention is O(n) so context grows linearly; softmax attention is O(n²) but used sparingly.

### Open Weights
MiniMax-01 weights are released under a permissive license (MiniMax's own license, similar to Llama's). This makes MiniMax-01 the first open-weights frontier hybrid-attention model.

## Architectural Expectations for MiniMax 3

> [!warning] The following are strong inferences, not confirmed facts.

### Refinement of Hybrid Attention (Strong Inference)
MiniMax 3 is expected to retain the hybrid lightning+softmax attention backbone. Possible refinements:
- Different ratio of lightning to softmax layers (e.g., 9:1 if 7:1 was too attention-heavy).
- Improved lightning attention formulation.
- Dynamic scheduling (use softmax attention only when needed).

### Larger MoE (Strong Inference)
MiniMax-01 was 456B/45.9B; MiniMax 3 is expected to grow this — potentially to 600B+ total parameters with similar activation sparsity.

### Reasoning Training (Strong Inference)
MiniMax-M1 already demonstrated reasoning capability (via RL on verifiable rewards, similar to DeepSeek-R1). MiniMax 3 is expected to inherit this — possibly as a unified base model with thinking mode rather than a separate "M" variant.

### Native Multimodal (Speculative)
MiniMax-Text-01 was text-only; MiniMax has separate vision models (MiniMax-VL). MiniMax 3 may consolidate vision into the base model — making it natively multimodal like Gemini.

## Why MiniMax 3 Matters Architecturally

1. **Open-weights frontier hybrid** — MiniMax-01 was the first open-weights model to demonstrate million-token context via hybrid attention. MiniMax 3 represents the next iteration.

2. **Lightning attention specifically** — MiniMax's lightning attention is a distinct linear-attention formulation, different from Mamba-2's SSD and from Kimi Linear's hybrid. MiniMax 3's specific attention recipe is a unique architectural data point.

3. **Chinese open-weights frontier** — MiniMax is one of the leading Chinese AI labs (alongside DeepSeek, Qwen/Alibaba, Moonshot/Kimi, Zhipu/GLM). MiniMax 3 represents another open-weights alternative in the Chinese ecosystem.

4. **Reasoning + hybrid + long-context** — MiniMax-M1 already demonstrated reasoning on a hybrid backbone. MiniMax 3 is the next data point on whether hybrid-attention backbones can match pure-Transformer backbones for reasoning quality.

## The MiniMax-01 Architecture (Reference for MiniMax 3)

### MoE Configuration

| Property            | MiniMax-Text-01 |
|---------------------|------------------|
| Total parameters    | 456B             |
| Active per token    | 45.9B            |
| Experts             | 32               |
| Active experts      | 2                |
| Shared experts      | 0                |
| Context             | 1M (4M extended)  |
| Attention            | Hybrid (lightning + softmax, 7:1 ratio) |
| Positional           | RoPE             |
| Norm                 | RMSNorm (pre-norm)|
| Activation          | SwiGLU           |

### Hybrid Attention Schedule
MiniMax-01 uses a periodic full-attention schedule: roughly 1 in every 8 layers uses full softmax attention; the other 7 use lightning attention. The exact pattern is documented in the MiniMax-01 technical report.

## Verification Checklist

- [ ] Locate MiniMax 3 technical report (MiniMax blog or arXiv).
- [ ] Confirm architecture: hybrid attention retained? MoE config?
- [ ] Confirm total and active parameter counts.
- [ ] Confirm lightning attention formulation (same as MiniMax-01?).
- [ ] Confirm context length (1M, 4M, longer?).
- [ ] Confirm reasoning capability and training method.
- [ ] Confirm multimodal support (text-only or native multimodal?).
- [ ] Compare benchmarks to MiniMax-01 and MiniMax-M1.

## Production Implications (Speculative)

- **Serving**: MiniMax-01 is supported in vLLM and SGLang with hybrid attention kernels. MiniMax 3 serving should follow the same pattern.
- **Cost**: MiniMax-01's 45.9B active parameters per token is competitive with DeepSeek-V3's 37B and Qwen 3 235B-A22B's 22B. MiniMax 3 should remain cost-competitive.
- **Long context**: MiniMax-01 was the first open-weights model with 1M context. MiniMax 3 may push this further — potentially to 4M+ tokens.
- **Open weights**: if MiniMax 3 retains the open-weights pattern, it provides another open-weights alternative alongside DeepSeek-V3/R1, Qwen 3, and GLM 4.5/5.

## Common Pitfalls

- **Confusing MiniMax-01 with MiniMax 3** — they may have different architectures or hybrid ratios. Verify before assuming continuity.
- **Assuming "MiniMax 3" is the official name** — MiniMax may release under a different name (e.g., "MiniMax-02" or "MiniMax-Text-02"). The "3" label comes from the master prompt §5.
- **Assuming lightning attention = standard linear attention** — lightning attention is a specific MiniMax formulation with custom kernels; it differs from Mamba-2's SSD and from generic linear attention.

## Connection to Other Concepts

- [[26 - Papers/2024-2026/43 - MiniMax-01 2025]] — the MiniMax-01 paper.
- [[26 - Papers/2024-2026/30 - Kimi Linear 2025]] — comparable hybrid attention model.
- [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture]] — comparable open-weights MoE.
- [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers]] — context for linear/hybrid attention.
- [[24 - Research Frontiers/Long-Context/07 - Long-Context Architectures]] — long-context architectures.
- [[10 - Model Architecture Research/MOC]] — parent chapter.

## See Also

- [[10 - Model Architecture Research/MOC|Model Architecture Research MOC]]
- [[00 - Vault Management/Research Queue]]
