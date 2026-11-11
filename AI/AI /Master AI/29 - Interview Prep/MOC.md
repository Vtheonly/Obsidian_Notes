---
tags: [moc, interview, interview-prep]
iteration: 13
created: 2026-08-07
last_updated: 2026-08-08
---

# 29 — Interview Prep MOC

> [!info] Interview preparation for AI engineering roles. Iteration 3 added system design and coding interview notes, covering the three most common LLM system design questions and four core coding implementations. Iteration 10 added part 2 of both system design and coding notes, covering advanced topics: reasoning model serving, VLM deployment, MCP-based agent platforms, multi-agent production systems, GRPO loss, VLM patch embedding, MCP server implementation, MoE routing, PagedAttention, and INT4 quantization. Iteration 13 added part 3 of conceptual and coding notes: conceptual Q2 covers reasoning models, VLMs, MCP, GRPO, hybrid architectures, scaling laws, spec decoding, quantization, DPO variants, GraphRAG, long-context, and 2026 frontier architectures; coding Q3 covers YaRN, GQA, RoPE scaling, KV cache compression, EAGLE-2 spec decoding, and GPTQ quantization.

## Reading Order

| #   | Note                                              | Sub-domain      | Purpose                                            |
|-----|---------------------------------------------------|-----------------|----------------------------------------------------|
| 01  | [[01 - Conceptual Interview Questions]]           | Conceptual      | Attention, training, fine-tuning, RAG conceptual Q&A. |
| 02  | [[02 - System Design Interview Questions]]        | System Design   | Multi-tenant RAG, LLM serving, agent platform.     |
| 03  | [[03 - Coding Interview Questions]]               | Coding          | Attention, MHA, sampling, RoPE from scratch.       |
| 04  | [[04 - Coding Interview Questions 2]]             | Coding          | GRPO loss, patch embedding, MCP server, MoE routing, PagedAttention, INT4. |
| 05  | [[05 - System Design Interview Questions 2]]      | System Design   | Reasoning model serving, VLM deployment, MCP platform, multi-agent. |
| 06  | [[06 - Conceptual Interview Questions 2]]          | Conceptual      | Reasoning models, VLMs, MCP, GRPO, hybrid architectures, scaling, spec decoding, quantization, DPO variants, GraphRAG, long-context, 2026 frontier. |
| 07  | [[05 - Coding Interview Questions 3]]              | Coding          | YaRN, GQA, RoPE scaling, KV cache compression, EAGLE-2 spec decoding, GPTQ quantization. |

## Sub-Domains

- [[29 - Interview Prep/Conceptual/01 - Conceptual Interview Questions|Conceptual]] — notes 01, 06
- [[29 - Interview Prep/System Design/02 - System Design Interview Questions|System Design]] — notes 02, 05
- [[29 - Interview Prep/Coding/03 - Coding Interview Questions|Coding]] — notes 03, 04, 07

## Why This Matters for AI

- AI engineering interviews have converged on three question types: conceptual (do you understand the concepts?), system design (can you architect a production system?), and coding (can you implement core components?).
- The system design questions test integration knowledge: how do serving, retrieval, caching, monitoring, and cost optimization fit together?
- The coding questions test depth: can you implement attention, sampling, RoPE, KV cache from scratch? If you can, you understand them; if you can't, you don't.
- Iteration 13 expanded coverage to the new topics introduced in iterations 10–13: reasoning models, VLMs, MCP, GRPO, hybrid architectures, scaling laws, spec decoding, quantization, DPO variants, GraphRAG, long-context, and 2026 frontier architectures.

## Production Implications

- For system design: always address cost and quality explicitly. Most candidates focus only on latency and miss these.
- For coding: know the shapes. Most bugs in attention implementations are shape errors.
- For both: have a scale-up plan. Show how the design evolves from 1K to 1M users.

## Common Interview Topics (by chapter)

| Topic                              | Chapter | Key Concept Notes                          |
|------------------------------------|---------|--------------------------------------------|
| Attention                          | 06      | [[04 - Self-Attention]], [[05 - Multi-Head Attention]] |
| Transformers                       | 07      | [[01 - Transformer Block]], [[07 - BERT]] |
| LLMs                               | 08      | [[01 - Decoder-Only Architecture]], [[06 - LLM Benchmarks]] |
| Fine-Tuning                        | 12      | [[01 - LoRA]], [[05 - RLHF with PPO]] |
| Inference                          | 13      | [[02 - KV Cache Mechanics]], [[04 - vLLM and Continuous Batching]] |
| Agents                             | 15      | [[03 - ReAct Pattern]], [[04 - Function Calling]] |
| RAG                                | 17      | [[01 - RAG Pipeline Overview]], [[02 - Chunking Hybrid Search Reranking]] |
| Production                         | 22      | [[01 - LLM Security and Prompt Injection]] |
| Reasoning models (iter 10)         | 09      | [[03 - Reasoning Models]] — see coding Q4 (GRPO) and SD Q1 (reasoning serving) |
| Vision-Language Models (iter 10)   | 23      | [[03 - LLaVA]] — see coding Q2 (patch embedding) and SD Q2 (VLM deployment) |
| MCP (iter 10)                      | 19      | [[01 - MCP Overview]] — see coding Q3 (MCP server) and SD Q3 (MCP platform) |
| Multi-Agent Systems (iter 10)      | 16      | [[01 - Multi-Agent Architectures]] — see SD Q4 (multi-agent production) |
| Mixture of Experts (iter 10)       | 07      | [[15 - Mixture of Experts Transformer]] — see coding Q4 (MoE routing) |
| KV cache paging (iter 10)          | 13      | [[02 - PagedAttention]] — see coding Q5 (PagedAttention) |
| Quantization (iter 10)             | 13      | [[03 - Quantization]] — see coding Q6 (INT4) |
| YaRN / RoPE scaling (iter 13)       | 06      | [[10 - YaRN and NTK-aware Scaling]] — see coding Q3 part 3 |
| GQA (iter 13)                       | 06      | [[14 - GQA MQA MLA]] — see coding Q3 part 3 |
| Speculative decoding (iter 13)      | 13      | [[05 - Speculative Decoding]] — see coding Q3 part 3 (EAGLE-2) |
| GraphRAG (iter 13)                  | 17      | see conceptual Q2 part 2 |
| Long-context eval (iter 13)         | 08      | see conceptual Q2 part 2 |
| 2026 frontier architectures (iter 13) | 10    | [[2026 Frontier Model Synthesis]] — see conceptual Q2 part 2 |
| DPO variants (iter 13)              | 12      | [[04 - DPO Derivation]] — see conceptual Q2 part 2 |
| Hybrid architectures (iter 13)      | 24      | [[01 - SSMs Mamba and Frontiers]] — see conceptual Q2 part 2 |

## Iteration 13 — Interview Prep Added

- **06 - Conceptual Interview Questions 2**: 25+ Q&A covering reasoning models, VLMs, MCP, GRPO, hybrid architectures, scaling laws, spec decoding, quantization, DPO variants, GraphRAG, long-context, 2026 frontier architectures.
- **05 - Coding Interview Questions 3**: 6 from-scratch implementations covering YaRN, GQA, RoPE scaling, KV cache compression, EAGLE-2 spec decoding, GPTQ quantization.

## See Also

- [[01 - Build Attention and Transformer From Scratch]]
- [[02 - Build a Mini RAG Pipeline]]
- [[03 - Build a Mini Agent]]
- [[29 - Interview Prep/MOC|29 Interview Prep MOC]]
