---
tags: [research, moc]
iteration: 13
created: 2026-08-07
last_updated: 2026-08-08
---

# 24 — Research Frontiers MOC

> [!info] The 2024–2026 research frontier. Iteration 5 expanded this chapter with notes on Mamba-2, RWKV/RetNet, Hyena, DeltaNet/Titans, test-time compute, and long-context architectures. Iteration 13 added a 2026 Research Frontier Update note that synthesizes the chapter's notes against the 2026 state of the field, identifying what's still current, what's been superseded, and what the open research questions are.

## Reading Order

| #   | Note                                              | Sub-domain        | Purpose                                            |
|-----|---------------------------------------------------|-------------------|----------------------------------------------------|
| 01  | [[01 - SSMs Mamba and Frontiers]]                 | State Space Models| Mamba, hybrids, reasoning, long-context overview.  |
| 02  | [[02 - Mamba-2 and Structured Attention]]         | State Space Models| SSD unification with attention; larger state.      |
| 03  | [[03 - RWKV and RetNet]]                          | Hybrid Architectures | Linear-time predecessors of Mamba.              |
| 04  | [[04 - Hyena and Long Convolutions]]              | Hybrid Architectures | FFT-based long convolutions for sequence mixing.|
| 05  | [[05 - DeltaNet and Titans]]                      | State Space Models | Delta rule update; neural memory at test time.   |
| 06  | [[06 - Test-Time Compute Scaling]]                | Reasoning         | o1/R1 paradigm; inference-time reasoning.          |
| 07  | [[07 - Long-Context Architectures]]               | Long-Context      | Ring Attention, Infini-Attention, LongRoPE, hybrid.|
| 08  | [[08 - 2026 Research Frontier Update]]             | Synthesis         | 2026 verification of all chapter notes; identifies what's still current and what's been superseded. |

## Sub-Domains

- [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|State Space Models]] — notes 01, 02, 05
- [[24 - Research Frontiers/Hybrid Architectures/03 - RWKV and RetNet|Hybrid Architectures]] — notes 03, 04
- [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling|Reasoning]] — note 06
- [[24 - Research Frontiers/Long-Context/07 - Long-Context Architectures|Long-Context]] — note 07
- [[24 - Research Frontiers/08 - 2026 Research Frontier Update|2026 Synthesis]] — note 08
- [[24 - Research Frontiers/Memory|Memory]] — covered in note 05 (Titans)
- [[24 - Research Frontiers/MOC|Emerging 2026]] — (track via [[00 - Vault Management/Research Queue|Research Queue]])

## The Research Landscape (2024–2026)

```mermaid
graph TD
  Attention[Full Attention<br/>O(N²), exact retrieval]
  SSM[SSMs<br/>Mamba, Mamba-2<br/>O(N), weaker retrieval]
  Linear[Linear Attention<br/>Performer, RWKV, RetNet<br/>O(N), fixed decay]
  Conv[Convolutions<br/>Hyena<br/>O(N log N), position-based]
  Hybrid[Hybrid Architectures<br/>Jamba, Kimi Linear, MiniMax-01, GLM-4.5, Qwen 3<br/>SSM + attention - 2026 frontier default]
  Memory[Memory-Augmented<br/>Titans, DeltaNet<br/>neural memory, test-time learning - research only]
  Reasoning[Reasoning Models<br/>o1, R1, Qwen3-Thinking, Kimi K1.5<br/>test-time compute scaling - 2026 commodity]

  Attention --> Hybrid
  SSM --> Hybrid
  Linear --> SSM
  Conv --> SSM
  SSM --> Memory
  Attention --> Reasoning
  Hybrid --> Reasoning
```

## Why This Matters for AI

- The pure-attention era is ending. 2024–2026 frontier models use hybrids (SSM + attention) or memory-augmented architectures.
- Test-time compute scaling (o1, R1) opened a new dimension — models can "think longer" at inference to improve quality.
- Long-context architectures (Ring Attention, LongRoPE) enabled million-token contexts, opening new application categories.
- Understanding these frontiers clarifies where the field is heading and what to evaluate when choosing a model.
- Iteration 13's 2026 Research Frontier Update note confirms what's still current and what's been superseded.

## Production Implications

- **For long context (>256K)**: consider hybrid models (Jamba, Kimi Linear, MiniMax-01, GLM-4.5, Qwen 3) or models with efficient attention.
- **For reasoning-heavy tasks**: use reasoning models (o1, R1, Qwen3-Thinking, Kimi K1.5, Claude Thinking) — they dramatically outperform standard models on math/code.
- **For efficiency-critical serving**: MoE + hybrid attention + EAGLE-3 spec decoding is the 2026 efficiency stack.
- **For research**: watch Titans — it represents the next direction in memory-augmented architectures, but has not yet reached production at frontier scale.

## Open Research Questions for 2026–2027

See [[24 - Research Frontiers/08 - 2026 Research Frontier Update]] § Open Research Questions for:
- Can test-time learning scale to frontier?
- What's the theoretical limit of spec decoding?
- Will MoE granularity keep increasing?
- Can reasoning be combined with multimodal?
- What's beyond MoE + hybrid attention?
- How to evaluate 1M+ context reliably?
- Can RLVR extend to non-verifiable domains?

## See Also

- [[06 - Attention Mechanisms/MOC|06 Attention]] — what's being challenged
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]]
- [[10 - Model Architecture Research/MOC|10 Model Architecture Research]]
- [[10 - Model Architecture Research/2026 Frontier Model Synthesis|2026 Frontier Model Synthesis]]
- [[12 - DeepSeek-R1 2025]] — reasoning model paper
- [[11 - Mamba 2023]] — the foundational SSM paper
- [[30 - Kimi Linear 2025]] — hybrid architecture paper
- [[00 - Vault Management/Research Queue|Research Queue]]
