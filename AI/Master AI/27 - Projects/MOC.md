---
tags: [moc, projects, implementation]
iteration: 13
created: 2026-08-07
last_updated: 2026-08-08
---

# 27 — Projects MOC

> [!info] Hands-on implementation projects. Building from scratch is the best way to verify you understand a concept. Iteration 5 added three more projects: Mini MoE, Tiny LLM Trainer, and Multi-Agent System. Iteration 6 added four more: reasoning model fine-tune (GRPO), MCP server, mini SSM, and vision-language model. Iteration 10 added four more capstones: Distributed Training Pipeline (FSDP), Code Agent (SWE-bench style), RAG Evaluation Harness, and Multimodal RAG Pipeline. Iteration 12 added five more capstones: Multimodal Agent, Speculative Decoding Server, Quantization Toolkit, MCP Marketplace, and Fine-Tuning Pipeline with LoRA + DPO. Iteration 13 added five more capstones: RLHF Pipeline with PPO, Knowledge-Graph Construction Pipeline (GraphRAG), Long-Context Evaluation Harness, Agent Observability Platform, and Model Distillation Pipeline. Total: 24 projects.

## Reading Order

| #   | Note                                              | Sub-domain      | Purpose                                            |
|-----|---------------------------------------------------|-----------------|----------------------------------------------------|
| 01  | [[01 - Build Attention and Transformer From Scratch]] | Implementations | Attention, MHA, Transformer block, mini-GPT.  |
| 02  | [[02 - Build a Mini RAG Pipeline]]                | Mini-Projects   | Ingestion, chunking, embedding, retrieval, gen.    |
| 03  | [[03 - Build a Mini Agent]]                       | Mini-Projects   | ReAct loop with web search + calculator tools.     |
| 04  | [[04 - Build a Mini MoE]]                         | Implementations | Mixture-of-Experts layer with routing + aux loss.  |
| 05  | [[05 - Build a Tiny LLM Trainer]]                 | Implementations | nanoGPT-style training loop with LR schedule.      |
| 06  | [[06 - Build a Multi-Agent System]]               | Capstones       | Planner + specialized executors with synthesis.    |
| 07  | [[07 - Build a Reasoning Model Fine-Tune]]        | Capstones       | GRPO with verifiable rewards; R1-style recipe.     |
| 08  | [[08 - Build an MCP Server]]                      | Capstones       | Resources, prompts, tools via MCP protocol.        |
| 09  | [[09 - Build a Mini SSM]]                         | Implementations | Mamba-style selective state space model.           |
| 10  | [[10 - Build a Vision-Language Model]]            | Capstones       | LLaVA-style: vision encoder + projection + LLM.    |
| 11  | [[11 - Build a Distributed Training Pipeline]]    | Capstones       | FSDP across multi-GPU; mixed precision + checkpoints.|
| 12  | [[12 - Build a Code Agent]]                       | Capstones       | SWE-bench-style: navigate repo, edit, run tests.   |
| 13  | [[13 - Build a RAG Evaluation Harness]]           | Capstones       | Retrieval + generation + e2e metrics; RAGAS-style. |
| 14  | [[14 - Build a Multimodal RAG Pipeline]]          | Capstones       | CLIP embeddings + VLM generation; cross-modal retrieval. |
| 15  | [[15 - Build a Multimodal Agent]]                 | Capstones       | VLM perception + planner + vision tools.            |
| 16  | [[16 - Build a Speculative Decoding Server]]      | Capstones       | EAGLE-2 spec decoding via vLLM; 2–4x speedup.      |
| 17  | [[17 - Build a Quantization Toolkit]]             | Capstones       | INT4/INT8/FP8 via GPTQ, AWQ, BnB; quality + latency benchmarks. |
| 18  | [[18 - Build an MCP Marketplace]]                 | Capstones       | Registry for publishing/discovering MCP servers; security scanning. |
| 19  | [[19 - Build a Fine-Tuning Pipeline with LoRA and DPO]] | Capstones | End-to-end SFT+DPO pipeline; QLoRA, merging, deployment. |
| 20  | [[20 - Build an RLHF Pipeline with PPO]]          | Capstones       | SFT → RM → PPO; the canonical RLHF pipeline.       |
| 21  | [[21 - Build a Knowledge-Graph Construction Pipeline]] | Capstones    | Entity/relation extraction; Neo4j; hybrid retrieval. |
| 22  | [[22 - Build a Long-Context Evaluation Harness]]  | Capstones       | Needle-in-haystack; multi-needle; multi-hop; heatmap. |
| 23  | [[23 - Build an Agent Observability Platform]]   | Capstones       | Tracing SDK; collector; anomaly detection; UI.     |
| 24  | [[24 - Build a Model Distillation Pipeline]]      | Capstones       | Response/logit/feature distillation; teacher→student. |

## Sub-Domains

- [[27 - Projects/Implementations/01 - Build Attention and Transformer From Scratch|Implementations]] — notes 01, 04, 05, 09
- [[27 - Projects/Mini-Projects/02 - Build a Mini RAG Pipeline|Mini-Projects]] — notes 02, 03
- [[27 - Projects/Capstones/06 - Build a Multi-Agent System|Capstones]] — notes 06, 07, 08, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24

## Why This Matters for AI

- Implementing from scratch is the only way to verify genuine understanding. Reading papers and using frameworks leaves gaps.
- The mini RAG project covers the full RAG pipeline — every component of [[17 - RAG/MOC|Chapter 17]] becomes transparent.
- The mini agent project covers the ReAct loop — every agent framework becomes transparent.
- The mini MoE project shows how Mixture-of-Experts works — clarifying Mixtral, DeepSeek-V3, GPT-4 (inferred).
- The tiny LLM trainer shows the full training recipe — from data to model to optimizer.
- The multi-agent system shows hierarchical agent orchestration — the pattern used in production.
- The RLHF pipeline (PPO) shows the canonical deep alignment recipe — InstructGPT-style.
- The GraphRAG pipeline shows how knowledge graphs complement vector RAG.
- The long-context eval harness validates claims about million-token models.
- The agent observability platform is the foundation of production debugging.
- The model distillation pipeline is the canonical "compress a frontier model" recipe.

## Production Implications

- Start with these minimal implementations; swap components for production-grade alternatives (vLLM, pgvector, LangSmith) once you understand them.
- Always include evaluation — a RAG or agent without an eval set cannot be improved safely.
- The mini agent's error handling and tracing patterns are the foundation of production agent systems.
- The MoE project's naive implementation is for learning; production MoE requires expert parallelism and kernel fusion.
- Distillation, RLHF, and long-context eval are the highest-ROI projects for production teams — they directly reduce cost and improve quality.

## Future Projects (Planned for Iteration 14+)

- Build a continuous pretraining pipeline (continued pretraining on a new domain).
- Build a multimodal reasoning model (vision + reasoning training).
- Build an MCP-based agent platform (multi-server, multi-tenant).
- Build an automated red-team pipeline (systematic prompt injection testing).
- Build a model routing system (cost-aware routing across multiple models).

## Iteration 13 — Projects Added

- **20 - Build an RLHF Pipeline with PPO**: full SFT → RM → PPO pipeline.
- **21 - Build a Knowledge-Graph Construction Pipeline (GraphRAG)**: entity/relation extraction + Neo4j + hybrid retrieval.
- **22 - Build a Long-Context Evaluation Harness**: needle-in-haystack + multi-needle + multi-hop.
- **23 - Build an Agent Observability Platform**: tracing SDK + collector + anomaly detection + UI.
- **24 - Build a Model Distillation Pipeline**: response/logit/feature distillation.

## See Also

- [[04 - Self-Attention]]
- [[05 - Multi-Head Attention]]
- [[03 - ReAct Pattern]]
- [[01 - RAG Pipeline Overview]]
- [[15 - Mixture of Experts Transformer]]
- [[01 - Multi-Agent Architectures]]
- [[27 - Projects/MOC|27 Projects MOC]]
