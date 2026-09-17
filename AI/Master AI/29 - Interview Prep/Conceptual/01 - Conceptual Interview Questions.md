---
tags: [interview, conceptual, attention, transformers, llms]
iteration: 8
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Interview Questions, Conceptual Q&A]
---

# 01 - Conceptual Interview Questions

> [!info] TL;DR
> Common conceptual AI engineering interview questions with concise answers and pointers to the relevant concept notes. Covers attention, Transformers, LLMs, inference, fine-tuning, RAG, agents.

## Attention and Transformers

### Q: Why scale the dot product by $\sqrt{d_k}$ in attention?
Without scaling, the dot product's variance grows with $d_k$. For large $d_k$, softmax saturates (one entry → 1, others → 0), causing vanishing gradients. Scaling brings variance back to 1, keeping softmax in its non-saturated regime. See [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] § "Why scale by √d_k".

### Q: What's the difference between MHA, MQA, GQA, MLA?
- **MHA**: one K/V per head (most params, best quality).
- **MQA**: one K/V shared across all heads (least params, slight quality loss).
- **GQA**: groups of heads share K/V (sweet spot — Llama, Mistral, Gemma).
- **MLA**: compress K/V into a low-rank latent (DeepSeek; smallest KV cache).

See [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA MQA MLA]].

### Q: Why use multi-head attention instead of a single big head?
Multiple heads let the model attend to different relations simultaneously (one head for previous-token, another for induction, another for syntax). Heads specialize. See [[06 - Attention Mechanisms/Multi-Head Attention/05 - Multi-Head Attention|Multi-Head Attention]].

### Q: Pre-norm vs post-norm?
Pre-norm (norm before sublayer) keeps the residual path clean, enabling stable training of deep Transformers. Post-norm (norm after residual) was the original but is unstable past ~12 layers. All modern LLMs use pre-norm. See [[07 - Transformers/Architecture/02 - Pre-Norm vs Post-Norm|Pre-Norm vs Post-Norm]].

### Q: Why do Transformers need positional encoding?
Self-attention is permutation-invariant — without positional info, the model can't distinguish token order. RoPE (modern default) rotates Q and K by position, making attention depend on relative offset. See [[06 - Attention Mechanisms/Positional Information/06 - Positional Encoding Overview|Positional Encoding Overview]].

### Q: What does FlashAttention do?
FlashAttention is an IO-aware exact attention algorithm. It tiles the computation to keep intermediates in fast GPU SRAM instead of slow HBM. 2–4x faster, 10x less memory, no quality loss. See [[06 - Attention Mechanisms/Efficient Attention/11 - FlashAttention|FlashAttention]].

## LLMs and Training

### Q: What is the KV cache and why does it matter?
The KV cache stores keys and values for all previous tokens so autoregressive generation only computes the new token's Q/K/V, not all tokens'. Without it, generating 1000 tokens from a 4096-token prompt would cost ~4M token-equivalent computations instead of ~4K. See [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics|KV Cache Mechanics]].

### Q: What's the difference between pretraining, SFT, and RLHF/DPO?
- **Pretraining**: train on massive text corpus with next-token prediction. Produces a base model.
- **SFT (supervised fine-tuning)**: fine-tune on instruction-response pairs. Produces a chat-capable model.
- **RLHF/DPO**: align with human preferences via reward model + PPO (RLHF) or direct preference optimization (DPO). Produces an aligned chat model.

See [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining]], [[12 - Fine-Tuning/Instruction Tuning/03 - Instruction Tuning and Chat Templates|SFT]], [[12 - Fine-Tuning/DPO/04 - DPO Derivation|DPO]].

### Q: What does LoRA do and why does it work?
LoRA freezes the pretrained weights and learns low-rank delta matrices alongside them. It works because fine-tuning updates have low intrinsic rank — you don't need full-rank updates to adapt the model. Reduces trainable params 100–1000x. See [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]].

### Q: Chinchilla scaling law — what does it say?
Compute-optimal training uses ~20 tokens per parameter. Most models pre-Chinchilla were undertrained (too few tokens for their size). Modern small models are often overtrained (more tokens than Chinchilla-optimal) because inference cost dominates total cost. See [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining & Scaling Laws]].

## Inference

### Q: How does PagedAttention work?
Manages the KV cache as fixed-size pages (like OS virtual memory) instead of contiguous allocations. Eliminates fragmentation (60–80% memory waste in naive approach), enables continuous batching, gives 2–4x throughput. See [[13 - Inference/KV Cache/02 - PagedAttention|PagedAttention]].

### Q: What is speculative decoding?
Use a small "draft" model to propose multiple tokens, then have the large "target" model verify them in one forward pass. Accepted tokens come free; rejected tokens are resampled. 2–3x speedup, no quality loss. See [[13 - Inference/Speculative Decoding/05 - Speculative Decoding|Speculative Decoding]].

### Q: Why is decode memory-bound at batch size 1?
At batch size 1, each token generation requires reading the full model weights from HBM (e.g., 14 GB for a 7B model in fp16). The actual compute is tiny (one matmul per layer). So you're limited by HBM bandwidth (~3 TB/s), not compute. This is why batching helps — it amortizes weight reads across multiple requests.

### Q: INT4 vs INT8 vs FP8 quantization?
- **INT8**: ~1% quality loss, 2x memory reduction. Easy.
- **INT4 (GPTQ/AWQ)**: ~1–2% quality loss, 4x memory reduction. Standard for serving 70B+ models.
- **FP8 (Hopper+)**: <0.5% quality loss, 2x reduction. Best quality, requires H100+ hardware.

See [[13 - Inference/Quantization/03 - Quantization|Quantization]].

## RAG and Agents

### Q: Why use hybrid search (BM25 + vector)?
Pure vector search misses exact-match queries (product codes, names, error messages). Pure BM25 misses semantic matches. Combining both (typically with reciprocal rank fusion) gives the best of both. See [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking, Hybrid Search, Reranking]].

### Q: What's the difference between an LLM app, a workflow, and an agent?
- **LLM app**: single call, no tools, no state.
- **Workflow**: multi-step with predefined control flow.
- **Agent**: LLM decides next step in a loop with tools.
- **Autonomous agent**: long-running, self-directed.

See [[15 - AI Agents/Architecture/01 - Agent vs Workflow vs LLM Application|Agent vs Workflow vs LLM Application]].

### Q: What is prompt injection and how do you defend?
Adversarial inputs that hijack the model's behavior. Defenses: input filtering, output validation, system prompt isolation, guardrail models (Llama Guard), sandboxing, human-in-the-loop for sensitive actions. No complete defense — use defense-in-depth. See [[22 - Production AI/Security/01 - LLM Security and Prompt Injection|LLM Security]].

### Q: What does ReAct stand for?
**Rea**soning + **A**c**t**ing. The pattern: Thought → Action → Observation → Thought → ... → Finish. Combines chain-of-thought reasoning with tool use. See [[15 - AI Agents/Reasoning/03 - ReAct Pattern|ReAct Pattern]].

## Architecture and Models

### Q: Why does DeepSeek-V3 use MLA instead of GQA?
MLA (Multi-head Latent Attention) compresses K and V into a low-rank latent vector, achieving KV cache sizes even smaller than MQA while maintaining MHA-like quality. This is what makes DeepSeek-V3 (671B) economical to serve. See [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture|DeepSeek Architecture]].

### Q: What is MoE and what problem does it solve?
Mixture-of-Experts replaces each FFN with multiple parallel FFN "experts" plus a router. Each token activates only top-k experts (typically 2). Decouples parameter count from compute — you get more capacity at the same compute cost. See [[07 - Transformers/Variants/15 - Mixture of Experts Transformer|MoE Transformer]].

### Q: What's the difference between a reasoning model and a regular LLM?
Reasoning models (o1, R1, Claude thinking) are trained to produce long internal chain-of-thought before answering. They spend more compute at inference ("test-time compute scaling") to solve harder problems. Same architecture; different training and inference pattern. See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]].

## Production

### Q: How would you design a multi-tenant RAG system?
- Postgres + pgvector for storage; row-level security for tenant isolation.
- Per-tenant namespaces for embeddings and metadata.
- Cache per-tenant (don't share LLM responses across tenants).
- Rate limit per tenant.
- Audit log per tenant.
- PII redaction at ingest.
- Hybrid search (BM25 + vector) + reranker.

See [[17 - RAG/MOC|RAG MOC]], [[20 - AI Infrastructure/Serving/01 - Production AI Stack|Production AI Stack]].

### Q: How do you evaluate an LLM application?
- **Offline**: golden set of 50–200 examples; LLM-as-judge + human review.
- **Online**: A/B testing, shadow deployment, user feedback (thumbs up/down).
- **Monitoring**: latency, cost, error rate, hallucination rate (sampled LLM-as-judge).
- **Benchmarks**: MMLU, GPQA for capability; task-specific for your domain.

See [[08 - LLMs/Evaluation/06 - LLM Benchmarks|LLM Benchmarks]].

## How to Use This Note

For each question:
1. Try to answer without looking.
2. Check the answer above.
3. Read the linked concept note for depth.
4. Practice out loud — interview answers should be 30–60 seconds, not 5 minutes.

## Reasoning Models and Test-Time Compute

### Q: What is test-time compute scaling?
Allowing the model to "think" longer at inference (longer CoT) to solve harder problems. Snell et al. (2024) showed accuracy scales as $\log(\text{tokens})$. A new dimension of capability — pre-2024, capability came from parameters, data, and training compute; test-time compute is the fourth. See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]].

### Q: What's the difference between o1 and R1?
- **o1** (OpenAI, Sep 2024): closed-source, hidden CoT, RL on verifiable rewards + PRMs.
- **R1** (DeepSeek, Jan 2025): open-source, visible CoT, RL on verifiable rewards (GRPO). R1-Zero showed pure RL (no SFT first) can produce emergent CoT.

Both are trained with RL on verifiable rewards; the recipes differ in details. See [[26 - Papers/2024-2026/12 - DeepSeek-R1 2025|DeepSeek-R1 paper]].

### Q: What is GRPO, and how does it differ from PPO?
Group Relative Policy Optimization (DeepSeek): samples N completions per prompt, uses group mean as baseline. Doesn't need a separate value model (PPO does). Simpler, cheaper, more stable for binary-reward settings (math correctness, code passing). See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] § GRPO.

### Q: When should you use a reasoning model vs. a standard LLM?
- **Reasoning model** (o1, R1): hard problems (math, code, multi-step reasoning), batch tasks (latency OK), high-stakes (quality justifies cost).
- **Standard LLM** (GPT-4o, Llama 3): simple Q&A, real-time chat, high-volume, cost-sensitive.
- **Hybrid**: route easy queries to standard LLM, hard to reasoning model. 5-10× cost reduction.

### Q: Why are reasoning models 10-100× more expensive?
Because they generate 10-50K thinking tokens per query. At $60/1M output tokens (o1), 30K CoT = $1.80 per query just for thinking. Standard LLMs generate 500-1000 output tokens. See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] § cost analysis.

## Vision-Language Models

### Q: How does LLaVA work?
Frozen CLIP-ViT encoder → image tokens → MLP projector → LLM. The LLM is fine-tuned (LoRA or full SFT) to consume image tokens alongside text. Simple, modular, cheap to train — only projector + LLM adapter are trained. Limitation: vision encoder can't see text context. See [[23 - Multimodal AI/Vision-Language/03 - LLaVA|LLaVA]].

### Q: What's the difference between stitched, cross-attention, and native multimodal?
- **Stitched** (LLaVA): frozen vision encoder + projector + LLM. Simple, modular, limited fusion.
- **Cross-attention** (BLIP-2): Q-Former compresses image into few tokens, LLM gets via cross-attention. Better fusion, more complex.
- **Native** (GPT-4o): image patches and text tokens in one Transformer. Maximum integration, requires massive multimodal training data.

See [[23 - Multimodal AI/Vision-Language/01 - Multimodal AI Overview|Multimodal Overview]] § architectural patterns.

### Q: Why are VLMs more expensive than text LLMs?
Images consume 500-4000 tokens depending on resolution and model. A 1024×1024 image in GPT-4o = ~750 tokens = ~$0.002 per image. For document-heavy apps (10+ images per query), costs add up. Mitigations: tile large images, cache image embeddings, use smaller vision encoders. See [[23 - Multimodal AI/Vision-Language/01 - Multimodal AI Overview|Multimodal Overview]] § cost.

### Q: When would you use a VLM vs OCR + text LLM?
VLM when (1) visual content adds value beyond extractable text (charts, diagrams, handwriting), (2) task needs visual reasoning, (3) UX benefits from image input. OCR + text LLM when (1) input is mostly text in images, (2) cost/latency critical, (3) task is purely linguistic. VLMs are 5-10× more expensive; only use when visual content adds value.

## MCP (Model Context Protocol)

### Q: What is MCP, and why does it exist?
MCP (Anthropic, 2024) is an open protocol for connecting LLMs to external tools, resources, and prompts. It exists because every LLM provider had their own tool-calling format, fragmenting the ecosystem. MCP standardizes the protocol so an MCP server works with any MCP-compatible client (Claude, Cursor, custom apps). See [[19 - MCP/Architecture/01 - MCP Overview|MCP Overview]].

### Q: What are the three resource types in MCP?
1. **Tools**: functions the LLM can call (e.g., `search_database`, `send_email`). Schema-based; LLM decides when to call.
2. **Resources**: data the LLM can read (e.g., file contents, database rows). Client decides what to expose.
3. **Prompts**: pre-written prompt templates the user can invoke (e.g., "summarize this file").

See [[19 - MCP/Components/02 - MCP Components|MCP Components]].

### Q: How does MCP differ from function calling?
Function calling is the LLM API feature (LLM emits a structured tool-call request). MCP is a protocol that wraps function calling with: server discovery, schema management, authentication, and a standard client-server architecture. MCP uses function calling internally but adds the protocol layer. Use MCP for cross-client tool sharing; use function calling for app-specific tools. See [[19 - MCP/Architecture/01 - MCP Overview|MCP Overview]] § MCP vs function calling.

### Q: What transports does MCP support?
1. **stdio**: client spawns server as subprocess; communication via stdin/stdout. Simple, local.
2. **HTTP+SSE**: client connects to server over HTTP; server-sent events for streaming. Remote, scalable.
3. **WebSocket**: bidirectional, useful for interactive sessions.

Most local MCP servers use stdio; remote/enterprise servers use HTTP+SSE.

## Memory Systems

### Q: What are the four types of memory in AI systems?
1. **Working memory**: current context (the prompt, recent turns).
2. **Episodic memory**: past experiences (specific conversations, events).
3. **Semantic memory**: facts and knowledge (user preferences, world knowledge).
4. **Procedural memory**: how-to knowledge (skills, workflows, tool patterns).

See [[18 - Memory Systems/Types/01 - Memory Types|Memory Types]].

### Q: How does MemGPT work?
MemGPT (Packer et al. 2023) borrows from OS virtual memory: a fixed-size "main context" (LLM's context window) plus a "secondary storage" of older messages. The LLM itself decides when to page in/out (via special function calls). This gives the appearance of unbounded memory within a fixed context window. See [[18 - Memory Systems/Architectures/02 - MemGPT and Letta|MemGPT]].

### Q: When do you need vector memory vs. knowledge graph memory?
- **Vector memory**: unstructured text snippets (past conversations, documents). Best for "find similar past interactions."
- **Knowledge graph memory**: structured entities and relations (user → friends → preferences). Best for "what do I know about this entity and its connections."
- **Hybrid**: most production systems use both — vectors for fuzzy recall, KG for structured queries.

See [[18 - Memory Systems/Vector Memory/04 - Vector Memory Backends|Vector Memory Backends]].

## Production AI

### Q: What is prompt injection, and why is it hard to defend?
Adversarial inputs that hijack the model's behavior. Hard to defend because LLMs can't distinguish "instructions" from "data" — both are text in the same context. No complete defense in 2026; use defense-in-depth (input filtering, output validation, guardrail models, sandboxing). See [[22 - Production AI/Security/01 - LLM Security and Prompt Injection|LLM Security]].

### Q: What's the difference between direct and indirect prompt injection?
- **Direct**: attacker is the user, explicitly trying to override instructions ("ignore previous instructions").
- **Indirect**: attacker embeds instructions in data the model reads (web pages, PDFs, retrieved documents). User is the victim; attacker is a third party. Indirect is more dangerous because the user didn't write the malicious content.

See [[22 - Production AI/Security/01 - LLM Security and Prompt Injection|LLM Security]] § attack taxonomy.

### Q: How do you secure an LLM agent that takes real-world actions?
Six layers: (1) sandbox (Docker, no network), (2) least privilege (minimal auth), (3) allowlist (only approved APIs/tools), (4) human-in-the-loop for destructive actions (email, delete, pay), (5) audit logging, (6) rate limits per session. See [[22 - Production AI/Security/01 - LLM Security and Prompt Injection|LLM Security]] § agent security.

### Q: What is the OWASP Top 10 for LLMs?
The standard LLM security taxonomy: (1) prompt injection, (2) insecure output handling, (3) training data poisoning, (4) model DoS, (5) supply chain, (6) sensitive info disclosure, (7) insecure plugins, (8) excessive agency, (9) overreliance/hallucination, (10) model theft. See [[22 - Production AI/Security/01 - LLM Security and Prompt Injection|LLM Security]] § OWASP.

### Q: How would you reduce LLM serving costs by 80%?
Stack: (1) model routing — 50% reduction (route easy to small model), (2) quantization — 50% reduction (INT8/FP8), (3) prompt caching — 30-60% for templated prompts, (4) continuous batching — 2-5× throughput, (5) response caching — 10-30% for repeated queries. Combined: 80-90% cost reduction with ~1-3% quality loss. See [[20 - AI Infrastructure/Serving/01 - Production AI Stack|Production AI Stack]] § cost optimization.

## Multi-Agent Systems

### Q: When should you use multi-agent vs single-agent?
Multi-agent when: (1) task decomposes into specialist roles, (2) one LLM's context can't hold all info, (3) different sub-tasks need different models, (4) you need verification (one produces, another critiques), (5) long-running with parallelism. Single-agent otherwise — start single, move to multi only when you hit a ceiling. See [[16 - Multi-Agent Systems/Architectures/01 - Multi-Agent Architectures|Multi-Agent Architectures]].

### Q: What are the common multi-agent patterns?
1. **Hierarchical** (planner-executor): clear division of labor, rigid.
2. **Manager-worker**: dynamic delegation, parallel execution.
3. **Peer swarm**: agents discuss as equals, robust but unbounded.
4. **Blackboard**: shared state, decoupled agents.
5. **Marketplace/bidding**: agents bid on tasks, self-organizing.

See [[16 - Multi-Agent Systems/Architectures/01 - Multi-Agent Architectures|Multi-Agent Architectures]] § patterns.

### Q: How do you prevent multi-agent systems from looping forever?
Four safeguards: (1) iteration cap per agent and per workflow, (2) timeout per agent and per task, (3) convergence detection (state stops changing → terminate), (4) cycle detection in graph-based systems (LangGraph has built-in recursion limits). Combine all four.

### Q: Why is LangGraph the production standard for multi-agent in 2026?
Four reasons: (1) durable execution (survives crashes via checkpointing), (2) observable (LangSmith integration), (3) graph-based (explicit state and edges make control flow debuggable), (4) mature (battle-tested at scale). Alternatives (AutoGen, CrewAI) lag on durability and observability.

## Research Frontiers

### Q: What is Mamba, and how does it differ from attention?
Mamba is a selective state space model (SSM). Differences: (1) $O(n)$ training vs $O(n^2)$ for attention, (2) $O(1)$ inference memory (fixed state) vs $O(n)$ (growing KV cache), (3) approximate recall (state compresses history) vs exact recall (attention can copy any token), (4) weaker ICL (no induction heads). See [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs/Mamba]].

### Q: Why do hybrid architectures (Jamba, Zamba) outperform pure Mamba at scale?
At large scale, attention's exact recall and ICL matter more. Pure Mamba compresses history into a fixed state, losing exact details. Hybrids add a few attention layers (1:7 ratio is common) for recall + ICL, while using many Mamba layers for efficiency. Best of both. See [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs/Mamba]] § hybrids.

### Q: What are Titans?
Titans (Google, 2024) introduce a neural long-term memory module that persists across sequences, updated via gradient descent on a "surprise" metric. Unlike attention (no persistent state) or SSMs (fixed state), Titans learn what to memorize and what to forget. A potential third way beyond attention and SSMs. See [[24 - Research Frontiers/State Space Models/01 - SSMs Mamba and Frontiers|SSMs/Mamba]] § Titans.

### Q: What is YaRN, and how does it extend context length?
YaRN (Yet another RoPE extensioN) interpolates RoPE frequencies non-uniformly — higher frequencies interpolated more aggressively, lower frequencies less. Extends RoPE models to 4-32× training length without retraining. Used by Llama 3.1 to extend from 8K to 128K. See [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling|YaRN]].

## Interpretability

### Q: What is mechanistic interpretability?
Reverse-engineering neural networks into understandable circuits. Key findings: (1) the residual stream is a memory bus, (2) attention heads specialize (previous-token, induction, syntactic), (3) features can be decomposed via sparse autoencoders. Pioneered by Anthropic. See [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]].

### Q: What is an induction head?
A two-head circuit that implements in-context learning: (1) a previous-token head writes "the previous token was X" into the residual stream, (2) the induction head finds previous occurrences of X's predecessor and copies its successor. Together: "if you saw A→B before, predict B when you see A." Emerges suddenly during training. See [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] § induction heads.

### Q: What is polysemanticity, and how do SAEs address it?
Polysemanticity: a single neuron fires for multiple unrelated concepts (cat, DNA, French Revolution). Happens because there are more concepts than neurons — the model uses superposition. SAEs decompose activations into many sparse monosemantic features, each firing for one concept. See [[14 - Interpretability/Sparse Autoencoders/03 - Sparse Autoencoders Deep Dive|SAEs]].

### Q: What is a steering vector?
A direction in activation space corresponding to a property (sentiment, honesty, toxicity), found by training a linear probe. You can steer the model by adding/subtracting this direction from the residual stream during inference — adding amplifies the property, subtracting suppresses it. "Representation engineering." See [[14 - Interpretability/Probing/05 - Probing|Probing]] § steering vectors.

## Architecture and Models (Additional)

### Q: What is MoE and how does routing work?
Mixture-of-Experts replaces each FFN with multiple parallel FFN "experts" plus a router. Each token activates only top-k experts (typically 2). The router is a small linear layer that outputs a probability distribution over experts; the top-k are selected. Decouples parameter count from compute — more capacity at the same compute cost. See [[07 - Transformers/Variants/15 - Mixture of Experts Transformer|MoE Transformer]].

### Q: What is the auxiliary-loss-free routing in DeepSeek-V3?
Standard MoE uses an auxiliary loss to balance load across experts (prevents all tokens routing to one expert). DeepSeek-V3's innovation: bias terms added to the router's logits, dynamically adjusted based on actual load. Eliminates the auxiliary loss (which can hurt quality) while maintaining balance. See [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture|DeepSeek Architecture]].

### Q: Why does DeepSeek-V3 use MLA instead of GQA?
MLA (Multi-head Latent Attention) compresses K and V into a low-rank latent vector, achieving KV cache sizes even smaller than MQA while maintaining MHA-like quality. This is what makes DeepSeek-V3 (671B total, 37B active) economical to serve — the KV cache is small enough to fit on a single node. See [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA MQA MLA]] and [[10 - Model Architecture Research/Open Source/01 - DeepSeek Architecture|DeepSeek Architecture]].

### Q: What is the difference between dense and MoE models?
- **Dense** (Llama 3 70B): all parameters active per token. Linear scaling of compute with parameters.
- **MoE** (Mixtral 8x7B, DeepSeek-V3): only top-k experts active per token. Decouples parameters from compute — more capacity at same compute cost.

Trade-off: MoE has higher memory requirements (all experts in memory) but lower compute per token. Better when memory is cheap and compute is expensive (most serving scenarios). See [[07 - Transformers/Variants/15 - Mixture of Experts Transformer|MoE Transformer]].

## How to Use This Note (Updated)

For each question:
1. Try to answer without looking.
2. Check the answer above.
3. Read the linked concept note for depth.
4. Practice out loud — interview answers should be 30–60 seconds, not 5 minutes.
5. For conceptual depth, also read the "Interview Questions" section at the end of each linked concept note (added in iteration 7-8).

## See Also

- [[29 - Interview Prep/MOC|Interview Prep MOC]]
- [[28 - Glossary/MOC|Glossary MOC]]
- [[MOC|Master Map of Content]]