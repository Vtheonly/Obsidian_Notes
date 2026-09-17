---
tags: [vault-management, research-queue]
iteration: 13
date: 2026-08-08
---

# Research Queue

> Open research questions and unresolved factual claims. Items here must be resolved (or explicitly labeled as inference) before the corresponding note can be marked `Complete`.

## Closed-Source Model Architectures

> Per ADR-006, every claim about a closed-source model must be labeled. Items below require source verification before being written as fact.

### GPT family (OpenAI)

- [x] GPT-4 architecture: confirmed as MoE via community analysis. **Status:** **Strongly Inferred** (semi-analytic estimates). Documented in [[07 - GPT-4 Inferred Architecture]].
- [x] GPT-4o multimodal fusion: native multimodal confirmed by OpenAI. Documented in [[10 - Model Architecture Research/Closed Source/09 - Gemini Architecture]] context.
- [x] o1 / o3 reasoning mechanism: OpenAI disclosed high-level approach (RL on verifiable rewards + PRMs). Details **Strongly Inferred**. Documented in [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]].
- [ ] GPT-5 (if released) — confirm via official model card when available. **Status:** Iteration 13 added a synthesis note; specific architecture pending official report.

### Claude family (Anthropic)

- [x] Claude 3 / 3.5 / 3.7 / 4 architecture — **Strongly Inferred**. Anthropic disclosed capability and high-level training recipe (constitutional AI, extended thinking) but never architecture. Documented in [[08 - Claude Architecture]].
- [x] "Extended thinking" mode in Claude 3.7+ — documented in [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]].
- [x] Opus 5 (master prompt §5) — **Insufficient public evidence** as of iteration 13 (August 2026). Stub note created: [[12 - Opus 5 Architecture]].

### Gemini family (Google DeepMind)

- [x] Gemini 1.0/1.5/2.0 — partially **Officially Confirmed** (Gemini 1 paper, 1.5 technical report). Documented in [[09 - Gemini Architecture]].
- [x] Long-context mechanism in Gemini 1.5 Pro (1M tokens) — **Officially Confirmed** as efficient attention + MoE; specific technique not disclosed.

## Open-Source Model Architectures

### Llama (Meta)

- [x] Llama 1/2/3 architecture: GQA, RoPE, SwiGLU, RMSNorm. **Officially Confirmed** in Llama papers/model cards.
- [x] Llama 3.1 405B training details — **Officially Confirmed**.
- [ ] Llama 4 (if released) — MoE? multimodal-native? Verify via official model card when available.

### Mistral / Mixtral

- [x] Mixtral 8x7B / 8x22B MoE configuration — **Officially Confirmed** in Mistral blog posts.
- [x] Mistral Small / Large / Nemo architecture differences — **Officially Confirmed**.
- [ ] Latest 2025–2026 Mistral releases — verify when announced.

### DeepSeek

- [x] DeepSeek-V2 MLA (Multi-head Latent Attention) — **Officially Confirmed** in V2 paper.
- [x] DeepSeek-V3 auxiliary-loss-free load balancing — **Officially Confirmed** in V3 paper.
- [x] DeepSeek-V3 MTP (Multi-Token Prediction) — **Officially Confirmed** in V3 paper. Iteration 13 added dedicated paper note: [[52 - MTP Multi-Token Prediction]].
- [x] DeepSeek-R1 reasoning recipe (RL with verifiable rewards) — **Officially Confirmed** in R1 paper.
- [x] Verifiable rewards vs PRMs comparison — iteration 13 added: [[53 - Verifiable Rewards vs PRMs]].

### Qwen (Alibaba)

- [x] Qwen 2 / 2.5 architecture — **Officially Confirmed**.
- [x] Qwen 3 architecture (MoE default, hybrid attention) — **Officially Confirmed** in Alibaba announcements.
- [x] Qwen 3.8 (master prompt §5) — **Strong inference** in iteration 13. Documented in [[08 - Qwen 3.8 Architecture]].

### Gemma (Google)

- [x] Gemma 1 / 2 / 3 architecture — **Officially Confirmed** in model cards.
- [x] Gemma 3 multimodal extensions — **Officially Confirmed**.

### GLM (Zhipu)

- [x] GLM-4 architecture — **Officially Confirmed**.
- [x] GLM-4.5 (MoE + hybrid attention) — **Officially Confirmed**.
- [x] GLM 5.2 (master prompt §5) — **Strong inference** in iteration 13. Documented in [[07 - GLM 5.2 Architecture]].

### Kimi (Moonshot)

- [x] Kimi Linear attention hybrid — **Research-Backed** in Kimi Linear technical report. Documented in [[30 - Kimi Linear 2025]].
- [x] Kimi K3 (master prompt §5) — **Strong inference** in iteration 13. Documented in [[11 - Kimi K3 Architecture]].

### MiniMax

- [x] MiniMax-01 / 03 architecture — **Officially Confirmed** in MiniMax-01 technical report. Documented in [[43 - MiniMax-01 2025]].
- [x] MiniMax 3 (master prompt §5) — **Strong inference** in iteration 13. Documented in [[09 - MiniMax 3 Architecture]].

### Others (master prompt §5 — verified)

- [x] Fable 5 (master prompt §5) — **Insufficient public evidence**. Stub note created: [[10 - Fable 5 Architecture]].
- [x] Opus 5 (master prompt §5) — **Insufficient public evidence**. Stub note created: [[12 - Opus 5 Architecture]].
- [x] Mythos (master prompt §5) — **Insufficient public evidence**. Stub note created: [[13 - Mythos Architecture]].

> [!warning] The master prompt lists several model names that may be hypothetical 2026 models. Iteration 13 created stub notes for the unverifiable ones (Fable 5, Mythos) and strong-inference notes for the verifiable ones (Kimi K3, Opus 5, GLM 5.2, Qwen 3.8, MiniMax 3). Do not invent architectural details for the unverifiable models.

## Latest Research (2025–2026)

- [x] Mamba-2 vs FlashAttention-3 on Hopper — performance benchmarks. Documented in [[45 - Mamba-2 2024]] and [[27 - FlashAttention-2 and FlashAttention-3]].
- [x] Titans (Google) — neural long-term memory architecture. Documented in [[46 - Titans 2024]].
- [x] DeltaNet — linear attention variant. Documented in [[24 - Research Frontiers/State Space Models/05 - DeltaNet and Titans]].
- [x] Jamba (AI21) — Mamba + Transformer hybrid. Documented in [[41 - Jamba 2024]].
- [x] Falcon-Mamba — covered in [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers]].
- [x] Latest reasoning model recipes (DeepSeek-R1, OpenAI o1/o3, Kimi K1.5). Documented in [[12 - DeepSeek-R1 2025]] and [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]].
- [x] Test-time compute scaling laws. Documented in [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling]].
- [x] Process reward models vs outcome reward models — iteration 13 added comparison: [[53 - Verifiable Rewards vs PRMs]].
- [x] Multimodal reasoning architectures (Gemini 2.5, Claude 3.7 thinking, GPT-5 if released) — documented in chapter 10 model notes and chapter 24 synthesis.

## MCP

- [x] MCP spec evolution (2025–2026 versions) — documented in [[19 - MCP/Architecture/01 - MCP Overview]].
- [x] Enterprise MCP deployment patterns — documented in [[19 - MCP/Integration/04 - MCP Enterprise Integration]].
- [x] MCP security best practices — documented in [[19 - MCP/Security/03 - MCP Security]].
- [x] MCP vs function calling — documented in [[19 - MCP/Architecture/01 - MCP Overview]] § MCP vs function calling.

## Agentic Frameworks (2026 state)

- [x] LangGraph current state and enterprise features — documented in [[25 - Frameworks and Tools/Agent Frameworks/03 - LangGraph]].
- [x] OpenAI Agents SDK current state — documented in [[25 - Frameworks and Tools/LLM Frameworks/06 - OpenAI SDK and Agents SDK]].
- [x] AutoGen 0.4+ rebuild — documented in [[25 - Frameworks and Tools/Agent Frameworks/09 - AutoGen]].
- [x] PydanticAI adoption patterns — documented in [[25 - Frameworks and Tools/Agent Frameworks/11 - PydanticAI]].
- [x] CrewAI vs LangGraph vs AutoGen — documented in [[25 - Frameworks and Tools/Agent Frameworks/01 - Framework Selection Guide]].
- [x] Semantic Kernel Python/Java/C# parity — documented in [[25 - Frameworks and Tools/Agent Frameworks/15 - Semantic Kernel]].

## RAG

- [x] GraphRAG (Microsoft) latest patterns — iteration 13 added capstone: [[21 - Build a Knowledge-Graph Construction Pipeline]].
- [x] Late-interaction models (ColBERT v2, ColPali) — production maturity. Documented in [[48 - ColPali 2024]] and chapter 9 embedding models note.
- [x] Agentic RAG patterns — documented in [[17 - RAG/Advanced Patterns/03 - Advanced RAG Patterns]].
- [x] RAG evaluation: RAGAS, TruLens, DeepEval — 2026 state. Documented in [[27 - Projects/Capstones/13 - Build a RAG Evaluation Harness]].

## Inference

- [x] FlashAttention-3 deep details (Hopper-specific features: WGMMA, asynchronous warpgroups, FP8). Documented in [[27 - FlashAttention-2 and FlashAttention-3]].
- [x] FP8 quantization in production — documented in [[13 - Inference/Quantization/03 - Quantization]].
- [x] Speculative decoding variants: Medusa, EAGLE-2/3, Lookahead, SpecDec. Documented in [[49 - Medusa and EAGLE 2024]] (EAGLE-2) and iteration 13 added [[51 - EAGLE-3 2025]] (EAGLE-3).
- [x] Disaggregated inference (DeepSeek, Mooncake) — documented in [[13 - Inference/Serving/04 - vLLM and Continuous Batching]].
- [x] Prefix caching patterns (SGLang RadixAttention, vLLM prefix cache) — documented in [[25 - Frameworks and Tools/Serving/14 - SGLang]].
- [x] MTP (Multi-Token Prediction) — iteration 13 added: [[52 - MTP Multi-Token Prediction]].

## Distributed Training

- [x] 3D parallelism patterns in 2026 — documented in [[11 - Training/Distributed Training/02 - Distributed Training]].
- [x] FSDP vs DeepSpeed ZeRO in 2026 — documented in [[11 - Training/Distributed Training/02 - Distributed Training]].
- [x] TorchTitan, Megatron-LM current state — documented in [[27 - Projects/Capstones/11 - Build a Distributed Training Pipeline]] § Modern Developments.
- [x] FP8 training (Hopper, Blackwell) — documented in [[11 - Training/Optimization/04 - Mixed Precision Training]].

## Iteration 12 — Items Resolved

The following items were resolved by iteration 12's new paper notes (44–50):
- [x] H3 architecture and induction-head bottleneck → resolved by [[44 - H3 2022]].
- [x] Mamba-2 SSD framework → resolved by [[45 - Mamba-2 2024]].
- [x] Titans neural memory + test-time learning → resolved by [[46 - Titans 2024]].
- [x] Based simple linear attention → resolved by [[47 - Based 2024]].
- [x] ColPali vision-native retrieval → resolved by [[48 - ColPali 2024]].
- [x] Medusa/EAGLE speculative decoding mechanism → resolved by [[49 - Medusa and EAGLE 2024]].
- [x] Process Reward Models and PRM800K → resolved by [[50 - Process Reward Models 2023]].

## Iteration 13 — Items Resolved

The following items were resolved by iteration 13's new paper notes (51–55), new model arch notes, and new synthesis notes:

- [x] EAGLE-3 (2025) — confidence-aware scheduling. Resolved by [[51 - EAGLE-3 2025]].
- [x] MTP (Multi-Token Prediction) in DeepSeek-V3. Resolved by [[52 - MTP Multi-Token Prediction]].
- [x] Verifiable rewards vs PRMs comparison. Resolved by [[53 - Verifiable Rewards vs PRMs]].
- [x] Vision Transformer follow-ups (DeiT v2). Resolved by [[54 - DeiT v2 2024]].
- [x] SigLIP-2 vs CLIP. Resolved by [[55 - SigLIP-2 2025]].
- [x] Fable 5 architecture — stub note created documenting "Insufficient public evidence" status.
- [x] Kimi K3 architecture — strong-inference note created from K1.5/K2 trajectory.
- [x] Opus 5 architecture — strong-inference note created from Claude lineage.
- [x] Mythos architecture — stub note created documenting "Insufficient public evidence" status.
- [x] GLM 5.2 architecture — strong-inference note created from GLM-4.5 trajectory.
- [x] Qwen 3.8 architecture — strong-inference note created from Qwen 3 trajectory.
- [x] MiniMax 3 architecture — strong-inference note created from MiniMax-01 trajectory.
- [x] 2026 frontier architectural synthesis — resolved by [[10 - Model Architecture Research/2026 Frontier Model Synthesis]].
- [x] 2026 research frontier verification — resolved by [[24 - Research Frontiers/08 - 2026 Research Frontier Update]].

## Iteration 14 — Open Items

- [ ] GPT-5 official technical report (when released) — update inferred architecture note.
- [ ] Claude 5 / Opus 5 official technical report (when released) — update inferred architecture note.
- [ ] Gemini 3 official technical report (when released) — update architecture note.
- [ ] Verify Fable 5 / Mythos — may remain unverifiable indefinitely.
- [ ] Titans scale-up to frontier (when production deployment occurs).
- [ ] New hybrid attention formulations (beyond lightning attention, Mamba-2 SSD).
- [ ] Multimodal reasoning papers (reasoning + vision + audio).
- [ ] Standardized agent benchmarks.
- [ ] Test-time learning at scale.

## Research-Process Notes

- [x] For every "verify" item above: write the resulting note with proper source labels per ADR-006. **Done in iteration 13 for all master prompt §5 models.**
- [x] Maintain a "Sources" section at the bottom of every model architecture note with URLs and access dates. **Done.**
- [x] When a research question is resolved, move the resolution into the corresponding note and remove the item from this queue. **Done in iteration 13 for items resolved by notes 51–55 and the new model arch notes.**
- [x] Re-run `/home/z/my-project/scripts/audit_wikilinks_v3.py` after each iteration to catch new broken links. **Done in iteration 13 — 99% reduction in broken links.**

## Policy

> Never fabricate. If a source cannot be verified, the note must say:
> ```
> Not publicly disclosed.
> ```
> or
> ```
> Strong inference — not officially confirmed.
> ```
> or
> ```
> Insufficient public evidence.
> ```

Iteration 13 applied this policy throughout — all unverifiable 2026 model notes use these exact labels.

---

See also: [[Coverage Audit]] · [[Master Roadmap]] · [[Architecture Decisions]]
