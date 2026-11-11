---
tags: [roadmap, curriculum, navigation]
iteration: 1
created: 2026-08-07
---

# Learning Roadmap

> [!info] A curriculum-style path through the vault. Designed for a learner who wants to go from foundations to research frontiers in roughly 12–18 months of part-time study.

## How to Use This Roadmap

Each phase has:
- **Goal** — what you should be able to do at the end.
- **Read** — the MOCs and key notes to read, in order.
- **Build** — a small project to consolidate the material.
- **Checkpoint** — questions you should be able to answer.

Skip a phase only if you can already pass its checkpoint.

---

## Phase 0 — Mathematical Foundations (4–6 weeks)

**Goal:** Re-derive scaled dot-product attention from scratch on a whiteboard.

**Read:**
- [[02 - Mathematics/MOC|02 Mathematics MOC]]
- Linear algebra: vectors, dot products, matrix multiplication, SVD
- Probability: distributions, Bayes, entropy, cross-entropy, KL
- Calculus: gradients, chain rule, Jacobians
- Optimization: gradient descent → AdamW, LR schedules
- Information theory: entropy, mutual information

**Build:**
- Implement softmax from scratch (with numerical stability).
- Implement matrix multiplication from scratch and verify against `numpy`.

**Checkpoint:**
- Why does softmax saturate for large logits?
- Why is cross-entropy the natural loss for classification?
- Why does Adam combine momentum and RMSProp?

---

## Phase 1 — ML & Neural Network Foundations (4–6 weeks)

**Goal:** Train an MLP from scratch (no framework) on MNIST.

**Read:**
- [[03 - Machine Learning/MOC|03 Machine Learning MOC]]
- [[04 - Neural Networks/MOC|04 Neural Networks MOC]]
- Bias-variance, regularization
- Backpropagation derivation (with computation graph)
- MLPs, activation functions (ReLU, GELU)
- Optimizers, initialization (Xavier, He)

**Build:**
- Implement backprop by hand on a 2-layer MLP.
- Then implement the same MLP in PyTorch.

**Checkpoint:**
- Derive the gradient of softmax + cross-entropy.
- Why does He initialization help ReLU networks?

---

## Phase 2 — Sequence Modeling & Pre-Transformer NLP (3–4 weeks)

**Goal:** Understand why attention was invented.

**Read:**
- [[05 - NLP Fundamentals/MOC|05 NLP Fundamentals MOC]]
- Tokenization: BPE, WordPiece, SentencePiece
- Word embeddings: Word2Vec, GloVe, FastText
- N-gram LMs, perplexity
- RNN / LSTM / GRU
- Seq2Seq and the information bottleneck
- Bahdanau attention — [[Bahdanau Attention]]

**Build:**
- Train a small BPE tokenizer on a corpus.
- Train a small character-level RNN-LM.

**Checkpoint:**
- Why does the Seq2Seq encoder-decoder bottleneck motivate attention?
- What problem does BPE solve over word-level tokenization?

---

## Phase 3 — Attention & The Transformer (4–6 weeks)

**Goal:** Implement a Transformer block from scratch in PyTorch.

**Read:**
- [[06 - Attention Mechanisms/MOC|06 Attention Mechanisms MOC]]
- [[07 - Transformers/MOC|07 Transformers MOC]]
- Self-attention — [[Self-Attention]]
- Multi-head attention — [[Multi-Head Attention]]
- Positional encoding — [[Positional Encoding Overview]], [[RoPE]]
- The Transformer block — [[Transformer Block]]
- Pre-norm vs post-norm — [[Pre-Norm vs Post-Norm]]
- LayerNorm / RMSNorm — [[Normalization Layers]]

**Build:**
- Implement scaled dot-product attention.
- Implement multi-head attention.
- Implement a full Transformer encoder block.
- Train it on a toy task (e.g., copy, sort).

**Checkpoint:**
- Why scale by √d_k?
- Why use multiple heads?
- Why RoPE over sinusoidal encoding?

---

## Phase 4 — LLMs (4–6 weeks)

**Goal:** Understand the modern LLM stack end-to-end.

**Read:**
- [[08 - LLMs/MOC|08 LLMs MOC]]
- Decoder-only architecture
- KV cache — [[KV Cache Mechanics]]
- Sampling — [[Sampling Strategies]]
- In-context learning
- Tool use / function calling
- Evaluation: MMLU, GPQA, HumanEval
- Hallucination causes

**Build:**
- Generate text from a small LLM (e.g., GPT-2) with top-k, top-p, temperature.
- Implement a basic KV cache.

**Checkpoint:**
- Why is the KV cache critical for autoregressive inference?
- What's the difference between top-k and top-p?
- What makes a model "instruction-tuned"?

---

## Phase 5 — Training & Fine-Tuning (4–6 weeks)

**Goal:** LoRA-fine-tune a small LLM on a custom dataset.

**Read:**
- [[11 - Training/MOC|11 Training MOC]]
- [[12 - Fine-Tuning/MOC|12 Fine-Tuning MOC]]
- Pretraining objectives
- Scaling laws (Chinchilla)
- Distributed training (DP/TP/PP/ZeRO/FSDP)
- SFT, instruction tuning
- LoRA — [[LoRA]]
- QLoRA — [[QLoRA]]
- RLHF with PPO
- DPO — [[DPO Derivation]]

**Build:**
- LoRA-fine-tune a small LLM (e.g., Llama-3.2-1B) on a custom instruction dataset.
- Optionally: DPO fine-tune.

**Checkpoint:**
- Why is LoRA parameter-efficient?
- Why does DPO not need a reward model?
- Why does PPO need a reference model?

---

## Phase 6 — Inference Engineering (3–4 weeks)

**Goal:** Serve a small LLM with vLLM and understand the internals.

**Read:**
- [[13 - Inference/MOC|13 Inference MOC]]
- KV cache deep dive
- PagedAttention — [[PagedAttention]]
- Continuous batching
- Quantization (INT8, INT4, FP8, GPTQ, AWQ, GGUF)
- Speculative decoding — [[Speculative Decoding]]
- vLLM, TGI, TensorRT-LLM

**Build:**
- Serve a 7B LLM with vLLM.
- Benchmark latency/throughput at different batch sizes.
- Quantize a model with AWQ and measure quality + speed.

**Checkpoint:**
- Why is PagedAttention faster than naive KV caching?
- When does speculative decoding help?
- INT4 vs INT8 — quality/speed/memory tradeoffs.

---

## Phase 7 — Agents & Tool Calling (4–6 weeks)

**Goal:** Build a small agent that uses tools to complete a multi-step task.

**Read:**
- [[15 - AI Agents/MOC|15 AI Agents MOC]]
- Agent vs workflow vs LLM app — [[Agent vs Workflow vs LLM Application]]
- ReAct — [[ReAct Pattern]]
- Chain-of-Thought — [[Chain-of-Thought]]
- Function calling — [[Function Calling]]
- Reflection — [[Reflection]]
- Planner-executor pattern
- Tree-of-Thoughts (planned)

**Build:**
- Build a ReAct agent that can search the web, run Python, and answer multi-step questions.

**Checkpoint:**
- What's the difference between an LLM app, workflow, and agent?
- When does reflection help vs hurt?
- How do you prevent infinite loops in agents?

---

## Phase 8 — RAG & Memory (4–6 weeks)

**Goal:** Build a production-quality RAG pipeline.

**Read:**
- [[17 - RAG/MOC|17 RAG MOC]]
- [[18 - Memory Systems/MOC|18 Memory Systems MOC]]
- RAG pipeline overview — [[RAG Pipeline Overview]]
- Chunking strategies
- Embedding models
- Hybrid search (BM25 + vector)
- Reranking
- GraphRAG, Agentic RAG, Self-RAG
- Memory types
- Vector DBs

**Build:**
- Build a RAG pipeline over a corpus of PDFs.
- Add BM25 + vector hybrid search.
- Add a cross-encoder reranker.
- Evaluate with RAGAS.

**Checkpoint:**
- Why does hybrid search outperform pure vector search?
- When does GraphRAG beat vanilla RAG?
- How do you evaluate citation faithfulness?

---

## Phase 9 — MCP & Multi-Agent Systems (3–4 weeks)

**Goal:** Build a multi-agent system over MCP.

**Read:**
- [[19 - MCP/MOC|19 MCP MOC]]
- [[16 - Multi-Agent Systems/MOC|16 Multi-Agent Systems MOC]]
- MCP architecture
- MCP resources/prompts/tools
- Multi-agent architectures (hierarchical, swarm, blackboard)
- Coordination, communication, consensus

**Build:**
- Expose a small tool over MCP.
- Build a 2-agent system (planner + executor) that uses MCP tools.

**Checkpoint:**
- What problem does MCP solve that function calling doesn't?
- When does a multi-agent system outperform a single agent?

---

## Phase 10 — Infrastructure, LLMOps & Production (4–6 weeks)

**Goal:** Deploy an LLM application to production with monitoring.

**Read:**
- [[20 - AI Infrastructure/MOC|20 AI Infrastructure MOC]]
- [[21 - LLMOps and MLOps/MOC|21 LLMOps MOC]]
- [[22 - Production AI/MOC|22 Production AI MOC]]
- FastAPI, Docker, Kubernetes
- PostgreSQL + pgvector, Redis, Kafka
- Monitoring, drift detection
- Prompt injection defense
- Cost optimization

**Build:**
- Deploy a RAG application with FastAPI + Docker + Postgres + pgvector.
- Add Prometheus + Grafana monitoring.
- Add guardrails (prompt injection detection).

**Checkpoint:**
- How do you detect prompt injection?
- How do you measure and reduce cost per query?
- What's your rollback strategy?

---

## Phase 11 — Model Architecture Research (ongoing)

**Goal:** Read the major model technical reports and understand each architecture's choices.

**Read:**
- [[10 - Model Architecture Research/MOC|10 Model Architecture Research MOC]]
- Llama, Mistral, DeepSeek, Qwen, Gemma
- GPT, Claude, Gemini (publicly disclosed portions)
- MLA (DeepSeek), GQA (Llama), MoE configurations

**Build:**
- Compare architectures in a table.
- Pick one architectural innovation (e.g., MLA) and write a deep note on it.

**Checkpoint:**
- What's the difference between MHA, MQA, GQA, MLA?
- Why does DeepSeek use auxiliary-loss-free load balancing?
- What's the tradeoff between dense and MoE?

---

## Phase 12 — Research Frontiers (ongoing)

**Goal:** Track the bleeding edge.

**Read:**
- [[24 - Research Frontiers/MOC|24 Research Frontiers MOC]]
- Mamba / Mamba-2
- Hybrid architectures (Jamba, Falcon-Mamba)
- Test-time compute, reasoning models
- Long-context (1M+ tokens)
- 2026 emerging architectures

**Build:**
- Pick one frontier topic and write a deep note.
- Reproduce a small experiment from a recent paper.

**Checkpoint:**
- When does Mamba outperform Transformer attention?
- What's the mechanism behind test-time compute scaling?

---

## Phase 13 — Papers & Projects (ongoing)

**Goal:** Read landmark papers and build implementations.

**Read:**
- [[26 - Papers/MOC|26 Papers MOC]]
- [[27 - Projects/MOC|27 Projects MOC]]

**Build (capstones):**
- Implement attention from scratch — [[01 - Build Attention and Transformer From Scratch]] (planned)
- Implement a Transformer from scratch — [[01 - Build Attention and Transformer From Scratch]] (planned)
- Build a mini RAG pipeline — [[Mini RAG Pipeline]] (planned)
- Build a mini agent — [[Mini Agent]] (planned)
- Build a mini MoE — [[Mini MoE]] (planned)

---

## See Also

- [[Reading Order]] — alternative paths (researcher, engineer, interviewer)
- [[00 - Vault Management/Master Roadmap|Master Roadmap]] — the full vault scope
- [[MOC]] — master map of content
