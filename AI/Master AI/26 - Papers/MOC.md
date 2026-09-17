---
tags: [moc, papers]
iteration: 13
created: 2026-08-07
last_updated: 2026-08-08
---

# 26 — Papers MOC

> [!info] Landmark papers in AI engineering. Each paper gets its own note with summary, key contributions, architecture, impact, and links to related concepts. Iteration 5 added 8 more paper notes (25–32). Iteration 6 added 5 more paper notes (33–37): Self-Refine, Tree of Thoughts, RAG (the original 2020 paper), Perceiver, and Flamingo. Iteration 10 added 6 more paper notes (38–43): Self-Consistency, Graph of Thoughts, BLIP-2, Jamba, Scaling Laws (Kaplan + Chinchilla), and MiniMax-01. Iteration 12 added 7 more paper notes (44–50): H3, Mamba-2, Titans, Based, ColPali, Medusa/EAGLE, Process Reward Models. Iteration 13 added 5 more paper notes (51–55): EAGLE-3, MTP, Verifiable Rewards vs PRMs, DeiT v2, SigLIP-2. Total: 55 landmark papers covering 2014–2025.

## Reading Order (Numbered Notes)

| #   | Note                                              | Year | Sub-domain        | Why It Matters                                      |
|-----|---------------------------------------------------|------|-------------------|-----------------------------------------------------|
| 01  | [[01 - Bahdanau Attention 2014]]                  | 2014 | Attention Origins | Birth of attention; fixed seq2seq bottleneck.       |
| 02  | [[02 - Vaswani Attention Is All You Need 2017]]   | 2017 | Transformers      | The Transformer; foundation of all modern LLMs.     |
| 03  | [[03 - BERT 2018]]                                | 2018 | Transformers      | Pretrain-finetune paradigm; bidirectional encoder.  |
| 04  | [[04 - GPT-3 2020]]                               | 2020 | LLMs              | Scale → in-context learning; foundation of LLM era. |
| 05  | [[05 - T5 2019]]                                  | 2019 | Transformers      | Text-to-text framing; span corruption; C4.         |
| 06  | [[06 - LoRA 2021]]                                | 2021 | Alignment         | Low-rank adaptation; default PEFT method.           |
| 07  | [[07 - InstructGPT 2022]]                         | 2022 | Alignment         | RLHF recipe; SFT → RM → PPO.                        |
| 08  | [[08 - FlashAttention 2022]]                      | 2022 | Efficient Attention| IO-aware exact attention; enabled long context.    |
| 09  | [[09 - DPO 2023]]                                 | 2023 | Alignment         | Direct preference optimization; replaced PPO.       |
| 10  | [[10 - PagedAttention vLLM 2023]]                 | 2023 | Efficient Attention| Paging for KV cache; 2–4× throughput.              |
| 11  | [[11 - Mamba 2023]]                               | 2023 | 2024-2026         | Selective SSMs; linear-time sequence modeling.      |
| 12  | [[12 - DeepSeek-R1 2025]]                         | 2025 | 2024-2026         | Verifiable-reward RL; open-weights reasoning.       |
| 13  | [[13 - Luong Attention 2015]]                     | 2015 | Attention Origins | Multiplicative (dot-product) attention.             |
| 14  | [[14 - GPT-1 2018]]                               | 2018 | Transformers      | Pretrain-then-finetune for generative models.       |
| 15  | [[15 - GPT-2 2019]]                               | 2019 | LLMs              | Zero-shot task transfer; scaling hypothesis.        |
| 16  | [[16 - Transformer-XL 2019]]                      | 2019 | Efficient Attention| Segment recurrence + relative position.            |
| 17  | [[17 - Reformer 2020]]                            | 2020 | Efficient Attention| LSH attention + reversible layers.                 |
| 18  | [[18 - Longformer 2020]]                          | 2020 | Efficient Attention| Sliding window + global attention.                 |
| 19  | [[19 - Linformer 2020]]                           | 2020 | Efficient Attention| Low-rank attention projection.                     |
| 20  | [[20 - BigBird 2020]]                             | 2020 | Efficient Attention| Local + global + random; theoretical guarantees.   |
| 21  | [[21 - Vision Transformer ViT 2020]]              | 2020 | Transformers      | Transformers for vision; patch-based.              |
| 22  | [[22 - Performer 2021]]                           | 2021 | Efficient Attention| Random Fourier features; linearized attention.     |
| 23  | [[23 - Swin Transformer 2021]]                    | 2021 | Transformers      | Shifted window; hierarchical vision Transformer.   |
| 24  | [[24 - GPT-4 Technical Report 2023]]              | 2023 | 2024-2026         | Multimodal; professional-grade capability.         |
| 25  | [[25 - LLaMA 2023]]                               | 2023 | LLMs              | Open-weights LLM that catalyzed the ecosystem.     |
| 26  | [[26 - Mistral 7B 2023]]                          | 2023 | LLMs              | SWA + GQA; 7B beats 13B.                           |
| 27  | [[27 - FlashAttention-2 and FlashAttention-3]]    | 2023-24 | Efficient Attention| 2× FA2; Hopper-optimized FA3.                  |
| 28  | [[28 - DeepSeek-V2 and V3 2024]]                  | 2024 | 2024-2026         | MLA + auxiliary-loss-free MoE; $5.5M training.     |
| 29  | [[29 - GQA 2024]]                                 | 2024 | Efficient Attention| Grouped-Query Attention; default for modern LLMs. |
| 30  | [[30 - Kimi Linear 2025]]                         | 2025 | 2024-2026         | Hybrid linear/attention for million-token context. |
| 31  | [[31 - Constitutional AI 2022]]                   | 2022 | Alignment         | RLAIF; AI feedback instead of human feedback.      |
| 32  | [[32 - Reflexion 2023]]                           | 2023 | Agents and RAG    | Verbal reinforcement learning; self-critique loop. |
| 33  | [[33 - Self-Refine 2023]]                          | 2023 | Agents and RAG    | Iterative self-critique and refinement.             |
| 34  | [[34 - Tree of Thoughts 2023]]                    | 2023 | Agents and RAG    | Search over reasoning trees; planning.              |
| 35  | [[35 - RAG 2020]]                                 | 2020 | Agents and RAG    | Original retrieval-augmented generation paper.      |
| 36  | [[36 - Perceiver 2022]]                           | 2022 | Multimodal        | Asymmetric attention; general perception.           |
| 37  | [[37 - Flamingo 2022]]                            | 2022 | Multimodal        | Few-shot visual-language model; Perceiver resampler.|
| 38  | [[38 - Self-Consistency 2022]]                     | 2022 | Agents and RAG    | Sample N CoT paths, majority vote; +10–20% reasoning.|
| 39  | [[39 - Graph of Thoughts 2023]]                    | 2023 | Agents and RAG    | Generalize ToT to DAGs; merge + refine operations.  |
| 40  | [[40 - BLIP-2 2023]]                               | 2023 | Multimodal        | Q-Former bridge between frozen vision + frozen LLM. |
| 41  | [[41 - Jamba 2024]]                                | 2024 | 2024-2026         | First production hybrid SSM-Transformer; 1:7 ratio.|
| 42  | [[42 - Scaling Laws (Kaplan and Chinchilla)]]      | 2020/22 | 2024-2026      | Power-law scaling; Chinchilla's 20 tokens/param.   |
| 43  | [[43 - MiniMax-01 2025]]                           | 2025 | 2024-2026         | Linear-attention hybrid; first open 1M context.     |
| 44  | [[44 - H3 2022]]                                   | 2022 | 2024-2026         | Hybrid SSM+attention; identified induction-head bottleneck. |
| 45  | [[45 - Mamba-2 2024]]                              | 2024 | 2024-2026         | SSD framework unifies SSMs and linear attention; 8192 state size. |
| 46  | [[46 - Titans 2024]]                               | 2024 | 2024-2026         | Neural memory + test-time learning; million-token context. |
| 47  | [[47 - Based 2024]]                                | 2024 | 2024-2026         | Simple Taylor-expansion linear attention; reproducible hybrid. |
| 48  | [[48 - ColPali 2024]]                              | 2024 | Multimodal        | Vision-native document retrieval; eliminates OCR.   |
| 49  | [[49 - Medusa and EAGLE 2024]]                     | 2024 | Efficient Attention| Single-model speculative decoding; 2–4x speedup. |
| 50  | [[50 - Process Reward Models 2023]]                | 2023 | Alignment         | Step-level reward models; foundation for reasoning models. |
| 51  | [[51 - EAGLE-3 2025]]                              | 2025 | Efficient Attention| Confidence-aware spec decoding; 4–6× speedup.       |
| 52  | [[52 - MTP Multi-Token Prediction]]               | 2024 | Efficient Attention| Training-time multi-token prediction (DeepSeek-V3). |
| 53  | [[53 - Verifiable Rewards vs PRMs]]                | 2025 | Alignment         | RLVR vs PRM comparison; the R1-Zero paradigm shift. |
| 54  | [[54 - DeiT v2 2024]]                              | 2024 | Transformers      | Modernized ViT training recipe; VLM vision encoder. |
| 55  | [[55 - SigLIP-2 2025]]                             | 2025 | Multimodal        | Default 2026 VLM vision encoder; multilingual.     |

## Sub-Domains

- [[26 - Papers/Attention Origins/MOC|Attention Origins]] — notes 01, 13
- [[26 - Papers/Transformers/MOC|Transformers]] — notes 02, 03, 05, 14, 21, 23, 54
- [[26 - Papers/LLMs/MOC|LLMs]] — notes 04, 15, 25, 26
- [[26 - Papers/Efficient Attention/MOC|Efficient Attention]] — notes 08, 10, 16, 17, 18, 19, 20, 22, 27, 29, 49, 51, 52
- [[26 - Papers/Alignment/MOC|Alignment]] — notes 06, 07, 09, 31, 50, 53
- [[26 - Papers/Agents and RAG/MOC|Agents and RAG]] — notes 32, 33, 34, 35, 38, 39
- [[26 - Papers/Multimodal/MOC|Multimodal]] — notes 36, 37, 40, 48, 55
- [[26 - Papers/2024-2026/MOC|2024-2026]] — notes 11, 12, 24, 28, 30, 41, 42, 43, 44, 45, 46, 47

## Reading Order (Chronological)

### 2014–2017: Attention Origins and the Transformer
1. Bahdanau 2014 → Luong 2015 → Vaswani 2017 (Attention Is All You Need)

### 2018–2019: Encoder and Decoder Era
4. GPT-1 2018 → BERT 2018 → GPT-2 2019 → T5 2019 → Transformer-XL 2019

### 2020: Scaling and Efficiency
5. GPT-3 2020 → Reformer, Longformer, Linformer, BigBird, ViT 2020

### 2021: Components Refined
6. LoRA 2021 → Performer 2021 → Swin Transformer 2021

### 2022: Alignment and Efficiency Breakthroughs
7. FlashAttention 2022 → InstructGPT 2022 → Constitutional AI 2022 → Flamingo 2022 → Perceiver IO 2022

### 2023: The Open-Weights Explosion + Reasoning Techniques
8. LLaMA 2023 → Mistral 7B 2023 → DPO 2023 → PagedAttention 2023 → Mamba 2023 → Reflexion 2023 → Self-Refine 2023 → Tree of Thoughts 2023 → GPT-4 2023 → FlashAttention-2 2023

### 2024–2025: MoE, Reasoning, and Hybrids
9. GQA 2024 → DeepSeek-V2/V3 2024 → FlashAttention-3 2024 → Jamba 2024 (hybrid SSM-Transformer) → DeepSeek-R1 2025 → Kimi Linear 2025 → MiniMax-01 2025 (linear-attention hybrid, 1M context)

### Foundational Scaling Theory
10. Scaling Laws (Kaplan 2020 + Chinchilla 2022) — power-law scaling; 20 tokens/param recipe.

### Reasoning Techniques (Sampling and Search)
11. Self-Consistency 2022 (sample + vote) → Tree of Thoughts 2023 (search) → Graph of Thoughts 2023 (DAG search)

## Reading Order (By Topic)

### Attention evolution
1. [[01 - Bahdanau Attention 2014]] → [[13 - Luong Attention 2015]] → [[02 - Vaswani Attention Is All You Need 2017]] → [[08 - FlashAttention 2022]] → [[27 - FlashAttention-2 and FlashAttention-3]]

### Efficient attention
1. [[16 - Transformer-XL 2019]] → [[17 - Reformer 2020]] → [[18 - Longformer 2020]] → [[19 - Linformer 2020]] → [[20 - BigBird 2020]] → [[22 - Performer 2021]] → [[08 - FlashAttention 2022]] → [[29 - GQA 2024]]

### LLMs
1. [[14 - GPT-1 2018]] → [[15 - GPT-2 2019]] → [[04 - GPT-3 2020]] → [[24 - GPT-4 Technical Report 2023]] → [[25 - LLaMA 2023]] → [[26 - Mistral 7B 2023]] → [[28 - DeepSeek-V2 and V3 2024]] → [[12 - DeepSeek-R1 2025]]

### Alignment
1. [[07 - InstructGPT 2022]] → [[31 - Constitutional AI 2022]] → [[09 - DPO 2023]] → [[12 - DeepSeek-R1 2025]]

### Vision Transformers
1. [[21 - Vision Transformer ViT 2020]] → [[23 - Swin Transformer 2021]]

### Agents and Reasoning
1. [[35 - RAG 2020]] → [[02 - Chain-of-Thought]] (chapter 15) → [[38 - Self-Consistency 2022]] → [[32 - Reflexion 2023]] → [[33 - Self-Refine 2023]] → [[34 - Tree of Thoughts 2023]] → [[39 - Graph of Thoughts 2023]] → [[12 - DeepSeek-R1 2025]]

### Multimodal
1. [[02 - CLIP]] (chapter 23) → [[21 - Vision Transformer ViT 2020]] → [[36 - Perceiver 2022]] → [[37 - Flamingo 2022]] → [[40 - BLIP-2 2023]] → [[03 - LLaVA]] (chapter 23)

### Hybrid Architectures
1. [[11 - Mamba 2023]] → [[41 - Jamba 2024]] → [[30 - Kimi Linear 2025]] → [[43 - MiniMax-01 2025]]

### Training Theory
1. [[42 - Scaling Laws (Kaplan and Chinchilla)]] → [[04 - GPT-3 2020]] → [[25 - LLaMA 2023]] → [[28 - DeepSeek-V2 and V3 2024]]

## Planned for Iteration 14+

- 2026 frontier model architectures (GPT-5, Claude 5, Gemini 3 — when technical reports emerge).
- Long-context breakthroughs (Ring Attention variants, new positional schemes).
- Multimodal reasoning papers.
- Agent benchmarks and evaluation frameworks.

## Iteration 13 — Papers Added

- **51 - EAGLE-3 2025**: confidence-aware spec decoding; 4–6× speedup.
- **52 - MTP Multi-Token Prediction**: DeepSeek-V3's training-time multi-token prediction.
- **53 - Verifiable Rewards vs PRMs**: comparison note; the R1-Zero paradigm shift.
- **54 - DeiT v2 2024**: modernized ViT training recipe; VLM vision encoder.
- **55 - SigLIP-2 2025**: default 2026 VLM vision encoder; multilingual.

## See Also

- [[00 - Vault Management/Master Roadmap|Master Roadmap]] § 26
- [[00 - Vault Management/Research Queue|Research Queue]]
