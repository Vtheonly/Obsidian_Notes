---
tags: [interview, conceptual, reasoning-models, vlms, mcp, grpo, hybrid, scaling, spec-decoding, quantization, dpo-variants]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Conceptual Interview Questions 2, Advanced Interview Q&A, Iteration 13 Interview Questions]
---

# 06 - Conceptual Interview Questions (Part 2)

> [!info] TL;DR
> Companion to [[01 - Conceptual Interview Questions]] — covers the new topics introduced in iterations 10–13: reasoning models, VLMs, MCP, GRPO, hybrid architectures, scaling laws, speculative decoding, quantization, DPO variants, GraphRAG, long-context, and 2026 frontier architectures. Designed for senior AI engineering interviews; questions get progressively harder within each section.

## Reasoning Models and Test-Time Compute

### Q: How does DeepSeek-R1 differ from o1?
Both use RL on verifiable rewards. Differences: (1) **R1 is open-weights**; o1 is API-only. (2) **R1's CoT is visible**; o1's is hidden. (3) **R1-Zero** showed that pure RL (no SFT first) produces emergent CoT; o1 likely used SFT before RL. (4) **R1 uses GRPO** (no value model); o1 likely uses PPO with a value model. (5) **R1 builds on DeepSeek-V3** (MLA + aux-loss-free MoE); o1's architecture is undisclosed. See [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025]].

### Q: Why does test-time compute scale logarithmically with accuracy?
Snell et al. (2024) showed accuracy scales as $\log(\text{tokens})$. The intuition: reasoning is a search problem; doubling search budget adds a constant number of "additional branches" the model can explore. Each branch has diminishing probability of being correct. So 2× tokens gives a constant accuracy gain (not 2× accuracy). This is why reasoning models are 10–100× more expensive than standard LLMs — the log scaling means accuracy gains require exponentially more compute. See [[24 - Research Frontiers/Reasoning/06 - Test-Time Compute Scaling]].

### Q: What is "aha moment" in R1-Zero's training?
During R1-Zero's RL training, the model spontaneously developed a behavior of reflecting on its own reasoning ("Wait, let me reconsider this..."). This wasn't trained explicitly — it emerged from the reward signal (correct answers correlate with self-correction). The "aha moment" was DeepSeek's term for this emergent behavior. It demonstrates that RL on verifiable rewards can produce sophisticated reasoning behaviors without explicit supervision. See [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025]].

### Q: How do you serve a reasoning model cost-effectively?
Three techniques. (1) **Speculative decoding** (EAGLE-3): the model's CoT is highly predictable (it's repetitive, structured). EAGLE-3 spec decoding gives 4–6× speedup on R1-style models. (2) **Adaptive thinking**: route easy queries to a non-reasoning model; only use the reasoning model for hard queries. Saves 5–10× cost. (3) **Distillation**: distill the reasoning model into a smaller student (DeepSeek's R1-Distill series). The student inherits ~85% of the reasoning capability at 10× lower cost. See [[27 - Projects/Capstones/24 - Build a Model Distillation Pipeline]].

### Q: Why are reasoning models 10–100× more expensive than standard LLMs?
Because they generate 10–50K thinking tokens per query. At $60/1M output tokens (o1), 30K CoT = $1.80 per query just for thinking. Standard LLMs generate 500–1000 output tokens. The cost ratio is (30K / 1K) × (output_token_price_ratio) ≈ 30–100×. Mitigations: spec decoding (4–6× cost reduction), distillation (10× cost reduction), adaptive thinking (5–10× cost reduction for mixed workloads). See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]].

## Vision-Language Models

### Q: How does SigLIP-2 differ from CLIP?
Three differences. (1) **Loss**: CLIP uses softmax contrastive (pick matching text out of N candidates); SigLIP-2 uses sigmoid (each pair independently classified). Sigmoid is simpler, works at smaller batch sizes. (2) **Self-supervised pretraining**: SigLIP-2 does DINOv2-style self-supervised vision pretraining *before* contrastive training. CLIP trains from scratch. (3) **Multilingual**: SigLIP-2 supports 100+ languages natively; CLIP is primarily English. SigLIP-2 beats CLIP by 6+ points on ImageNet zero-shot. See [[26 - Papers/Multimodal/55 - SigLIP-2 2025]].

### Q: When does a VLM cost more than 10× a text LLM?
When images consume 1000+ tokens each AND there are 10+ images per query. A 1024×1024 image in GPT-4o = ~750 tokens. For a document-heavy app (10+ pages), that's 7.5K tokens just for images. At $5/1M input tokens, that's $0.04 per query just for images. Mitigations: (1) tile large images, (2) cache image embeddings, (3) use smaller vision encoders, (4) OCR + text LLM for purely textual content in images. See [[23 - Multimodal AI/Vision-Language/01 - Multimodal AI Overview]].

### Q: Why are native multimodal models (Gemini) better than stitched (LLaVA)?
Native multimodal models train on text + images + audio from the start; the Transformer learns cross-modal representations during pretraining. Stitched models (LLaVA) bolt a vision encoder onto a pretrained LLM via a projector; the LLM doesn't natively understand images. Native models have: (1) better cross-modal reasoning, (2) lower latency (no separate vision encoder forward pass), (3) better grounding (image features are deeply integrated). Trade-off: native models require massive multimodal training data and compute; stitched models are cheaper to train. See [[23 - Multimodal AI/Vision-Language/01 - Multimodal AI Overview]].

### Q: How does ColPali differ from traditional document RAG?
Traditional document RAG: OCR the document → chunk → embed → retrieve. ColPali: skip OCR entirely; embed the document page as an image (using SigLIP/CLIP-style encoder) → retrieve via late interaction (max-sim over patches). ColPali is faster (no OCR), handles visual content better (charts, tables, diagrams), and matches text-only retrieval quality. The trade-off: ColPali requires VLM-grade vision encoders, which are larger than text-only embedders. See [[26 - Papers/Multimodal/48 - ColPali 2024]].

## MCP (Model Context Protocol)

### Q: How does MCP compare to function calling?
Function calling is the LLM API feature (LLM emits a structured tool-call request). MCP is a *protocol* that wraps function calling with: server discovery, schema management, authentication, and a standard client-server architecture. MCP uses function calling internally but adds the protocol layer. Use MCP for cross-client tool sharing (a single MCP server works with Claude, Cursor, custom apps); use function calling for app-specific tools. See [[19 - MCP/Architecture/01 - MCP Overview]].

### Q: How do you secure an MCP server?
Six layers. (1) **Authentication**: OAuth 2.0 or API keys; never trust the client. (2) **Authorization**: per-tool permissions; not every client should call every tool. (3) **Input validation**: validate all tool inputs against a strict schema; reject malformed inputs. (4) **Rate limiting**: per-client rate limits to prevent DoS. (5) **Audit logging**: log every tool call for forensics. (6) **Sandboxing**: run dangerous tools (file system, shell) in a sandbox; never on the host. See [[19 - MCP/Security/03 - MCP Security]].

### Q: What's the difference between MCP resources, prompts, and tools?
- **Tools**: functions the LLM can call (e.g., `search_database`, `send_email`). Schema-based; LLM decides when to call.
- **Resources**: data the LLM can read (e.g., file contents, database rows). Client decides what to expose.
- **Prompts**: pre-written prompt templates the user can invoke (e.g., "summarize this file"). User-initiated, not LLM-initiated.

Tools are LLM-driven; resources are client-driven; prompts are user-driven. See [[19 - MCP/Components/02 - MCP Components]].

### Q: How would you design an MCP marketplace?
A registry for publishing/discovering MCP servers. Components: (1) **Server registry**: list of published MCP servers with metadata (name, version, description, owner). (2) **Discovery**: search by capability ("find servers that expose `send_email`"). (3) **Security scanning**: scan published servers for known vulnerabilities (prompt injection, command injection, excessive permissions). (4) **Versioning**: support multiple versions per server; allow rollback. (5) **Reviews/ratings**: community-driven quality signal. See [[27 - Projects/Capstones/18 - Build an MCP Marketplace]].

## GRPO and Reasoning Training

### Q: How does GRPO differ from PPO?
GRPO (Group Relative Policy Optimization, DeepSeek-R1): samples N completions per prompt, uses group mean as baseline. Doesn't need a separate value model. PPO uses a learned value model to estimate expected reward. GRPO is simpler (no value model to train), more stable for verifiable rewards (math, code), and works well when reward signal is sharp. PPO with value model remains valuable for non-verifiable rewards (chat alignment). See [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025]].

### Q: Why did DeepSeek-R1-Zero skip SFT?
R1-Zero: pure RL on verifiable rewards (no SFT first). The hypothesis: SFT on reasoning traces biases the model toward specific reasoning patterns; pure RL lets the model discover its own reasoning strategies. The result: R1-Zero's CoT is longer, more exploratory, and less polished than R1's (which used SFT). R1-Zero demonstrated that SFT is not strictly necessary for emergent CoT — RL alone suffices. But R1 (with SFT) is more readable and safer, so production uses R1 not R1-Zero.

### Q: When does RLVR beat PRM?
RLVR (Reinforcement Learning with Verifiable Rewards) beats PRM (Process Reward Model) when: (1) **the answer is verifiable** — math, code, formal logic. (2) **annotation budget is limited** — RLVR is free (rule-based verifier); PRM requires labels. (3) **reward hacking matters** — RLVR is immune (rule-based); PRM is susceptible. PRM wins when: (1) **answer is not verifiable** — creative writing, subjective tasks. (2) **credit assignment matters** — PRM gives per-step signal. (3) **reasoning is long** — PRM's dense signal helps convergence. Most 2026 reasoning models use RLVR alone or RLVR + PRM hybrid. See [[26 - Papers/Alignment/53 - Verifiable Rewards vs PRMs]].

## Hybrid Architectures and Linear Attention

### Q: Why do hybrid SSM-Transformer models (Jamba, Kimi K2) outperform pure SSMs?
Pure SSMs (Mamba, Mamba-2) compress history into a fixed-size state, losing exact token-level information. They fail at in-context retrieval (looking up a specific earlier token). Hybrids add a few attention layers (1:7 ratio is common) for retrieval + ICL, while using many SSM layers for efficiency. Best of both: O(n) complexity from SSMs + exact recall from attention. H3 (2022) was the first to demonstrate this pattern. See [[26 - Papers/2024-2026/44 - H3 2022]].

### Q: What is "lightning attention" in MiniMax-01?
Lightning attention is MiniMax's specific linear-attention formulation. It's a kernel-friendly variant of linear attention that achieves near-optimal throughput on modern GPUs. The key innovation: a specific tensor contraction pattern that maps well to GPU memory hierarchy (similar to FlashAttention for softmax attention). Other labs use different formulations (Kimi's Mamba-style selective scan, GLM's sparse attention). The 2026 hybrid-attention landscape has multiple competing formulations; it's unclear which will win. See [[26 - Papers/2024-2026/43 - MiniMax-01 2025]].

### Q: How does Titans (Google, 2024) differ from attention and SSMs?
Titans introduces a **neural long-term memory module** that persists across sequences, updated via gradient descent on a "surprise" metric. Unlike attention (no persistent state) or SSMs (fixed-size state), Titans learn what to memorize and what to forget. The memory module is updated online during inference (test-time learning). This is a potential third way beyond attention and SSMs — but production deployment is still early. See [[26 - Papers/2024-2026/46 - Titans 2024]].

### Q: Why is the 7:1 SSM:attention ratio common in hybrids?
Empirically, 7:1 (Jamba) and similar ratios (MiniMax-01, Kimi K2) balance efficiency and quality. Lower ratios (more attention) → better quality but quadratic cost. Higher ratios (more SSM) → better efficiency but worse retrieval. 7:1 was found to be a sweet spot — enough attention layers to enable induction heads and in-context learning, enough SSM layers to keep compute O(n). Different ratios work for different use cases: code generation benefits from more attention; long-context summarization benefits from more SSM. See [[24 - Research Frontiers/Hybrid Architectures/03 - RWKV and RetNet]].

## Scaling Laws and Compute-Optimal Training

### Q: What does Chinchilla scaling law say?
Compute-optimal training uses ~20 tokens per parameter. Pre-Chinchilla models (GPT-3, original Llama) were undertrained — too few tokens for their size. Post-Chinchilla models (Llama 2, Mistral) follow the recipe. Modern small models (Llama 3 8B, trained on 15T tokens) are *overtrained* — far more tokens than Chinchilla-optimal — because inference cost dominates total cost. Overtraining makes the model better at inference time, which justifies the extra pretraining compute. See [[26 - Papers/2024-2026/42 - Scaling Laws (Kaplan and Chinchilla)]].

### Q: Why does Llama 3 8B use 15T tokens (way more than Chinchilla's 20:1)?
Llama 3 8B has 8B parameters, so Chinchilla-optimal would be 160B tokens. Llama 3 8B was trained on 15T tokens — ~94× Chinchilla. Why? Because Llama 3 8B is a *serving model* (will be used billions of times); the extra pretraining compute is amortized over many inference calls. Chinchilla assumed pretraining and inference compute are equally weighted; in practice, inference dominates. So overtraining is optimal when inference is the bottleneck. See [[26 - Papers/2024-2026/42 - Scaling Laws (Kaplan and Chinchilla)]].

### Q: How do you compute the FLOPs for training a transformer?
Approximate FLOPs ≈ 6 × N × D, where N is parameter count and D is token count. The factor 6 comes from: 2 (forward pass: matmul) × 2 (backward pass: matmul + gradient) × 1 (master weight). For Llama 3 70B (70B params, 15T tokens): 6 × 70e9 × 15e12 = 6.3e24 FLOPs ≈ 6 × 10²⁴ FLOPs. At 50% MFU on H100 (700 TFLOPs BF16), this takes ~110k H100-hours = ~4600 H100-days. At $2/H100-hour, ~$220K. Frontier models (10²⁵+ FLOPs) cost tens of millions in compute alone.

## Speculative Decoding

### Q: Why is spec decoding bit-identical to vanilla decoding?
Spec decoding uses **rejection sampling** to preserve the target model's distribution. For each speculated token: (1) compute P_target(token) and P_draft(token); (2) accept with probability min(1, P_target / P_draft); (3) if rejected, resample from the corrected distribution (P_target - P_draft, normalized). This procedure is provably equivalent to sampling from P_target directly. No quality loss. The output distribution is identical to vanilla decoding given the same random seed. See [[26 - Papers/Efficient Attention/49 - Medusa and EAGLE 2024]].

### Q: How does EAGLE-3 achieve 4–6× speedup?
Three innovations. (1) **Confidence-aware scheduling**: predict which speculated branches will be accepted (via a small MLP), prune low-confidence branches before the verification forward pass. (2) **Training-time MTP**: the target model is trained with multi-token prediction, making its hidden states "speculation-friendly". (3) **Longer speculation**: K=8–16 (vs EAGLE-2's K=4–8). Combined: 90–97% acceptance rate (vs EAGLE-2's 85–95%), giving 4–6× speedup. See [[26 - Papers/Efficient Attention/51 - EAGLE-3 2025]].

### Q: When does spec decoding hurt performance?
Five cases. (1) **Very short generations** (<50 tokens): draft overhead > speedup. (2) **Low acceptance rate** (<50%): rejected drafts waste compute. (3) **Large batch sizes** (>32): tree verification has diminishing returns at high batch. (4) **Code generation**: draft models struggle with code's discrete structure. (5) **Highly creative tasks** (poetry, brainstorming): draft models predict "safe" continuations that get rejected. For these, fall back to vanilla. Adaptive routers detect these cases and switch modes. See [[26 - Papers/Efficient Attention/49 - Medusa and EAGLE 2024]].

### Q: How does MTP (Multi-Token Prediction) relate to spec decoding?
MTP is a *training-time* technique: the model is trained to predict multiple future tokens, producing a built-in draft head. Spec decoding (EAGLE-3) is an *inference-time* technique that leverages MTP-trained models. Without MTP, EAGLE-3 falls back to EAGLE-2-style behavior. MTP makes the target model's hidden states "speculation-friendly" — explicitly trained to support multi-token lookahead. DeepSeek-V3 uses MTP; EAGLE-3 achieves 4–6× on DeepSeek-V3. See [[26 - Papers/Efficient Attention/52 - MTP Multi-Token Prediction]].

## Quantization

### Q: When would you use INT4 vs INT8 vs FP8?
- **INT8**: ~1% quality loss, 2× memory reduction. Easy. Default for general serving.
- **INT4 (GPTQ/AWQ)**: ~1–2% quality loss, 4× memory reduction. Standard for serving 70B+ models on consumer GPUs.
- **FP8 (Hopper+)**: <0.5% quality loss, 2× reduction. Best quality, requires H100+ hardware.

Production: use FP8 on H100+ (best quality, easy); INT8 on A100 (good quality, broad hardware support); INT4 when memory is constrained (consumer GPUs, edge). See [[13 - Inference/Quantization/03 - Quantization]].

### Q: How does GPTQ differ from AWQ?
- **GPTQ** (Frantar et al., 2022): post-training quantization using second-order information (Hessian of weights). Quantizes weights column-by-column, updating remaining weights to compensate. Accurate but slow (minutes per model).
- **AWQ** (Lin et al., 2023): activation-aware quantization. Identifies "important" weights (high-magnitude activations) and keeps them in higher precision; quantizes the rest to INT4. Faster than GPTQ, comparable quality.

Both produce INT4 models; AWQ is generally preferred for production (faster, similar quality). See [[13 - Inference/Quantization/03 - Quantization]].

### Q: Why is FP8 better than INT8?
Three reasons. (1) **Dynamic range**: FP8 has exponent + mantissa, so it can represent both very small and very large values; INT8 is fixed-point, limited range. (2) **No calibration**: FP8 quantization doesn't require a calibration dataset (just convert); INT8 requires running sample inputs to determine scaling factors. (3) **Hardware native**: H100+ has native FP8 tensor cores, so FP8 matmul is as fast as INT8. Trade-off: FP8 requires Hopper+ hardware; INT8 works on older GPUs. See [[13 - Inference/Quantization/03 - Quantization]].

### Q: How do you quantize a 70B model to fit on a single 80GB GPU?
Use **QLoRA + INT4**. Steps: (1) Load base model in INT4 (4-bit weights, ~35GB for 70B). (2) Add LoRA adapters (rank 16, ~50M params, ~200MB). (3) Train LoRA on top of frozen INT4 base. (4) Merge LoRA back into base for deployment. (5) Serve merged INT4 model on single 80GB GPU. Quality: ~2–3% loss vs BF16; cost: 1× GPU instead of 2×. See [[12 - Fine-Tuning/PEFT/02 - QLoRA]].

## DPO Variants

### Q: What are IPO, KTO, SimPO, and how do they differ from DPO?
- **DPO** (2023): direct preference optimization on (prompt, chosen, rejected) pairs. Standard recipe.
- **IPO** (2024): Identity Preference Optimization. Fixes DPO's overfitting on noisy preferences by regularizing the preference gap. More conservative than DPO.
- **KTO** (2024): Kahneman-Tversky Optimization. Uses single-sided preferences (good/bad) instead of pairs. Doesn't need paired data — works on thumbs-up/thumbs-down signals.
- **SimPO** (2024): length-normalized DPO. Removes DPO's length bias (DPO can prefer longer responses). Better for production chat alignment.

By 2026, **SimPO is the default** for new projects; DPO remains for backward compatibility; KTO for thumbs-up/down datasets; IPO for noisy preferences. See [[27 - Projects/Capstones/19 - Build a Fine-Tuning Pipeline with LoRA and DPO]] § Modern Developments.

### Q: Why does DPO have a length bias?
DPO's loss compares log P(chosen) - log P(rejected). If the chosen response is longer, log P(chosen) is naturally lower (more tokens to predict). The model can game this by making responses shorter, increasing log P(chosen) artificially. SimPO normalizes by length: log P(chosen) / len(chosen) - log P(rejected) / len(rejected). Removes the length bias. See [[12 - Fine-Tuning/DPO/04 - DPO Derivation]].

### Q: When would you use KTO instead of DPO?
KTO (Kahneman-Tversky Optimization) uses single-sided preferences: each response is labeled "good" or "bad" (thumbs up/down), not paired. Use KTO when: (1) **you only have unary feedback** (thumbs up/down from users, no paired comparisons). (2) **collecting paired data is expensive** (KTO works on any unary feedback). (3) **the dataset is imbalanced** (more thumbs up than down, or vice versa). DPO requires paired data (chosen vs rejected); KTO doesn't. Trade-off: paired data has more signal per example (relative comparison), so DPO converges faster when you have pairs. See [[12 - Fine-Tuning/DPO/04 - DPO Derivation]].

## GraphRAG and Knowledge Graphs

### Q: When does GraphRAG beat vector RAG?
Three cases. (1) **Multi-hop reasoning**: questions requiring connecting info across documents ("Who founded the company that acquired X?"). (2) **Entity-centric queries**: questions about a specific entity ("What do we know about OpenAI?"). (3) **Global questions**: questions about the whole corpus ("What are the main themes?"). For single-hop factual questions, vector RAG is sufficient and faster. See [[27 - Projects/Capstones/21 - Build a Knowledge-Graph Construction Pipeline]].

### Q: How do you handle entity deduplication in GraphRAG?
Three approaches. (1) **String normalization**: lowercase, strip punctuation, remove legal suffixes (Inc, Corp, Ltd). Catches obvious cases. (2) **Embedding similarity**: embed entity names, cluster by cosine similarity (>0.9), merge clusters. Catches semantic duplicates. (3) **LLM-based matching**: for each new entity, ask LLM "is this the same as any existing entity?" Catches subtle cases (acronyms, aliases). Production: combine all three — normalization first (cheap), then embedding (medium cost), then LLM (expensive, only for ambiguous cases). See [[27 - Projects/Capstones/21 - Build a Knowledge-Graph Construction Pipeline]].

### Q: How does Microsoft GraphRAG differ from a basic GraphRAG pipeline?
Two key additions. (1) **Hierarchical summarization**: detects communities (clusters of related entities), summarizes each community into a higher-level description. Enables global questions ("what are the main themes?") that pure entity-lookup can't answer. (2) **Query routing**: detects whether a query is "local" (specific entity, multi-hop) or "global" (corpus-wide theme) and routes to different retrieval strategies. Local uses entity lookup + subgraph extraction; global uses community summaries. See [[27 - Projects/Capstones/21 - Build a Knowledge-Graph Construction Pipeline]] § Modern Developments.

## Long-Context

### Q: What is "lost in the middle"?
Models retrieve information well at the start and end of context but fail in the middle. The heatmap (position × accuracy) shows a U-shape: high accuracy at 0% and 100%, low in 50%. Caused by attention's positional bias (some positions get more attention weight than others, regardless of content). Mitigations: (1) reorder context to put important info at edges, (2) use YaRN/NTK scaling for better position encoding, (3) use hybrid attention (Jamba, MiniMax-01) which is more uniform. See [[27 - Projects/Capstones/22 - Build a Long-Context Evaluation Harness]].

### Q: How does YaRN extend RoPE to longer contexts?
YaRN (Yet another RoPE extensioN) interpolates RoPE frequencies non-uniformly — higher frequencies interpolated more aggressively, lower frequencies less. This is based on the observation that high-frequency components encode local position (less affected by length extension) while low-frequency components encode global position (more affected). Extends RoPE models to 4–32× training length without retraining. Used by Llama 3.1 to extend from 8K to 128K. See [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling]].

### Q: How do hybrid attention models (Kimi K2, MiniMax-01) achieve 1M context?
Hybrid attention models use mostly linear-attention layers (O(n) complexity) with periodic full-attention layers (O(n²) but sparse). The KV cache grows linearly with most layers (linear attention has fixed-size state) and quadratically only with the few full-attention layers. Net: KV cache grows ~O(n) instead of O(n²). A pure-attention model at 1M tokens would need ~500GB of KV cache; a hybrid can fit in ~50GB. See [[26 - Papers/2024-2026/30 - Kimi Linear 2025]] and [[26 - Papers/2024-2026/43 - MiniMax-01 2025]].

## 2026 Frontier Architectures

### Q: What's the converged 2026 frontier recipe?
By 2026, every frontier model uses: **MoE capacity** (8–256 experts, 2–8 active) + **hybrid attention** (linear + full, ~7:1 ratio) + **RoPE with YaRN scaling** + **RMSNorm pre-norm** + **SwiGLU activation** + **long context** (256K–1M tokens) + **RL on verifiable rewards** for reasoning + **native multimodal** fusion + **EAGLE-3 spec decoding** for inference. The convergence is striking — the 2024 "Llama-style" recipe has been extended with sparse capacity and hybrid attention. See [[10 - Model Architecture Research/2026 Frontier Model Synthesis]].

### Q: Why has the field converged on MoE + hybrid attention?
Two reasons. (1) **Compute efficiency**: MoE decouples capacity from compute (more parameters at same FLOPs); hybrid attention reduces context complexity from O(n²) to O(n). Both directly reduce cost. (2) **Quality**: empirically, MoE matches dense quality at lower compute; hybrid attention matches pure-attention quality at lower compute. Both have been validated at frontier scale (DeepSeek-V3, Kimi K2, MiniMax-01). The combination gives 5–10× cost reduction vs dense pure-attention models at the same quality. See [[10 - Model Architecture Research/2026 Frontier Model Synthesis]].

### Q: What's the next architectural revolution after MoE + hybrid attention?
Unclear. Candidates: (1) **Titans-style test-time learning** (neural memory updated at inference). (2) **Truly sub-quadratic attention** (better than current linear attention formulations). (3) **Multimodal-native architectures** (single Transformer for text+image+audio+video, not separate encoders). (4) **Neuro-symbolic hybrids** (neural + symbolic reasoning). None of these has reached frontier-scale production deployment as of 2026. The field may be entering a period of consolidation rather than revolution. See [[10 - Model Architecture Research/2026 Frontier Model Synthesis]] § What's Genuinely Novel.

## How to Use This Note

For each question:
1. Try to answer without looking.
2. Check the answer above.
3. Read the linked concept note for depth.
4. Practice out loud — interview answers should be 30–60 seconds, not 5 minutes.
5. For conceptual depth, also read the "Interview Questions" section at the end of each linked concept note.

## See Also

- [[29 - Interview Prep/MOC|Interview Prep MOC]]
- [[29 - Interview Prep/Conceptual/01 - Conceptual Interview Questions]] — part 1 (covers iterations 1–9 topics).
- [[29 - Interview Prep/Coding/03 - Coding Interview Questions]] — coding questions.
- [[29 - Interview Prep/Coding/04 - Coding Interview Questions 2]] — advanced coding.
- [[29 - Interview Prep/System Design/02 - System Design Interview Questions]] — system design.
- [[29 - Interview Prep/System Design/05 - System Design Interview Questions 2]] — advanced system design.
- [[28 - Glossary/MOC|Glossary MOC]]
- [[MOC|Master Map of Content]]
