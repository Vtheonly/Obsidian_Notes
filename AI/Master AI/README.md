---
tags: [vault, readme, moc]
iteration: 1
created: 2026-08-07
---

# AI Engineering Obsidian Vault

> [!info] What this is
> A production-quality Obsidian vault for mastering **AI Engineering** — from mathematical foundations through 2026 research frontiers. Designed to function as a **university curriculum, technical book, research notebook, professional engineering handbook, and internal AI-company knowledge base**.

> [!tip] How to use this vault
> - Start at [[MOC|the Master Map of Content]].
> - Or follow the [[Learning Roadmap]] if you want a curriculum order.
> - Or jump to any domain folder below.
> - Use Obsidian's graph view to see how concepts connect.
> - Every note has YAML frontmatter (`tags`, `created`, `iteration`) so you can query with Dataview or Bases.

## Vault Status

**Iteration:** 1 (first iteration — Mode A)
**State:** Foundation established. Architecture complete (175 folders). Foundational notes generated for the most dependency-critical concepts. Many chapters still at `Planned` — see [[00 - Vault Management/Vault Status|Vault Status]] for the full accounting.

This vault is **iteratively constructed**. Each iteration leaves it in a clean, recoverable state. To resume work, read [[00 - Vault Management/Next Iteration|Next Iteration]].

## Domains

| #   | Domain                            | Purpose                                                                  | Status            |
|-----|-----------------------------------|--------------------------------------------------------------------------|-------------------|
| 00  | [[00 - Vault Management/MOC]]     | Persistent project state — roadmap, status, logs, audits.                | ✅ Complete       |
| 01  | [[01 - AI Foundations/MOC]]       | What AI engineering is; roles; the modern AI stack.                      | 🟡 Planned        |
| 02  | [[02 - Mathematics/MOC]]          | Linear algebra, probability, calculus, optimization, information theory. | 🟢 Partial        |
| 03  | [[03 - Machine Learning/MOC]]     | Supervised / unsupervised / reinforcement learning, evaluation.          | 🟡 Planned        |
| 04  | [[04 - Neural Networks/MOC]]      | Perceptrons, MLPs, CNNs, RNNs, training, regularization.                 | 🟢 Partial        |
| 05  | [[05 - NLP Fundamentals/MOC]]     | Tokenization, embeddings, language modeling, pre-transformer NLP.        | 🟢 Partial        |
| 06  | [[06 - Attention Mechanisms/MOC]] | Bahdanau → Luong → self-attention → multi-head → positional → efficient. | 🟢 Partial        |
| 07  | [[07 - Transformers/MOC]]         | The Transformer block, encoder/decoder variants, components.             | 🟢 Partial        |
| 08  | [[08 - LLMs/MOC]]                 | LLM architecture, context/KV, sampling, evaluation, capabilities.        | 🟢 Partial        |
| 09  | [[09 - Foundation Models/MOC]]    | Vision, multimodal, embedding, code, reasoning foundation models.        | 🟡 Planned        |
| 10  | [[10 - Model Architecture Research/MOC]] | Per-model architecture analysis (Llama, DeepSeek, GPT, Claude, etc.). | 🟡 Planned        |
| 11  | [[11 - Training/MOC]]             | Pretraining, alignment, data, distributed training.                      | 🟡 Planned        |
| 12  | [[12 - Fine-Tuning/MOC]]          | PEFT, RLHF, DPO, instruction tuning, distillation.                      | 🟢 Partial        |
| 13  | [[13 - Inference/MOC]]            | KV cache, decoding, quantization, serving, optimization.                 | 🟢 Partial        |
| 14  | [[14 - Interpretability/MOC]]     | Mechanistic interp, attention analysis, SAEs, probing.                   | 🟡 Planned        |
| 15  | [[15 - AI Agents/MOC]]            | Agent architecture, planning, reasoning, tool calling, autonomy.         | 🟢 Partial        |
| 16  | [[16 - Multi-Agent Systems/MOC]]  | Architectures, communication, coordination, enterprise patterns.         | 🟡 Planned        |
| 17  | [[17 - RAG/MOC]]                  | Ingestion, chunking, retrieval, reranking, evaluation, advanced patterns.| 🟢 Partial        |
| 18  | [[18 - Memory Systems/MOC]]       | Memory types, architectures, operations, vector/KG memory.               | 🟡 Planned        |
| 19  | [[19 - MCP/MOC]]                  | Model Context Protocol — architecture, components, security, integration.| 🟡 Planned        |
| 20  | [[20 - AI Infrastructure/MOC]]    | Serving, storage, messaging, compute, observability.                     | 🟡 Planned        |
| 21  | [[21 - LLMOps and MLOps/MOC]]     | Pipelines, monitoring, evaluation, deployment, cost optimization.        | 🟡 Planned        |
| 22  | [[22 - Production AI/MOC]]        | Reference architectures, reliability, security, scaling, patterns.       | 🟡 Planned        |
| 23  | [[23 - Multimodal AI/MOC]]        | Vision-language, audio, video, diffusion, fusion architectures.          | 🟡 Planned        |
| 24  | [[24 - Research Frontiers/MOC]]   | SSMs, hybrids, reasoning, long-context, efficiency, 2026 emerging.       | 🟡 Planned        |
| 25  | [[25 - Frameworks and Tools/MOC]] | LangChain, LangGraph, vLLM, Ollama, vector DBs, etc.                     | 🟡 Planned        |
| 26  | [[26 - Papers/MOC]]               | Landmark papers — Bahdanau → 2026.                                       | 🟡 Planned        |
| 27  | [[27 - Projects/MOC]]             | Implementations, mini-projects, capstones.                               | 🟡 Planned        |
| 28  | [[28 - Glossary/MOC]]             | A–Z glossary, acronyms, notation conventions.                            | 🟡 Planned        |
| 29  | [[29 - Interview Prep/MOC]]       | Conceptual, system design, coding interview banks.                       | 🟡 Planned        |
| 99  | (Archives)                        | Superseded / deprecated content.                                         | 🟡 Planned        |

## Recommended Reading Orders

### A. Curriculum order (beginner → advanced)

1. [[01 - AI Foundations/MOC]]
2. [[02 - Mathematics/MOC]]
3. [[03 - Machine Learning/MOC]]
4. [[04 - Neural Networks/MOC]]
5. [[05 - NLP Fundamentals/MOC]]
6. [[06 - Attention Mechanisms/MOC]]
7. [[07 - Transformers/MOC]]
8. [[08 - LLMs/MOC]]
9. [[11 - Training/MOC]] → [[12 - Fine-Tuning/MOC]]
10. [[13 - Inference/MOC]]
11. [[15 - AI Agents/MOC]] → [[16 - Multi-Agent Systems/MOC]]
12. [[17 - RAG/MOC]] → [[18 - Memory Systems/MOC]] → [[19 - MCP/MOC]]
13. [[20 - AI Infrastructure/MOC]] → [[21 - LLMOps and MLOps/MOC]] → [[22 - Production AI/MOC]]
14. [[23 - Multimodal AI/MOC]]
15. [[24 - Research Frontiers/MOC]]
16. [[10 - Model Architecture Research/MOC]]
17. [[26 - Papers/MOC]]
18. [[27 - Projects/MOC]]
19. [[29 - Interview Prep/MOC]]

### B. Researcher path (frontier-focused)

1. [[06 - Attention Mechanisms/MOC]] (full)
2. [[07 - Transformers/MOC]]
3. [[24 - Research Frontiers/MOC]]
4. [[10 - Model Architecture Research/MOC]]
5. [[26 - Papers/MOC]]

### C. Engineer path (production-focused)

1. [[08 - LLMs/MOC]]
2. [[13 - Inference/MOC]]
3. [[15 - AI Agents/MOC]]
4. [[17 - RAG/MOC]]
5. [[19 - MCP/MOC]]
6. [[20 - AI Infrastructure/MOC]]
7. [[21 - LLMOps and MLOps/MOC]]
8. [[22 - Production AI/MOC]]
9. [[25 - Frameworks and Tools/MOC]]

## Construction Protocol

This vault follows the iterative construction protocol defined in `Master AI/What to do.md`:

- **Mode A (first iteration):** architect the system, establish roadmap, build foundations.
- **Mode B (subsequent):** recover state from `00 - Vault Management/`, continue from where the previous iteration stopped.

See [[00 - Vault Management/README|Vault Management README]] for details.

## Quality Standards

Every concept note in this vault follows:

- One coherent concept per note.
- YAML frontmatter (`tags`, `created`, `iteration`).
- Definition → intuition → motivation → internal operation → (math when applicable) → code example → production implications → cross-links.
- Mermaid diagrams where they aid understanding.
- Wikilinks to at least 3 related notes.
- Closed-source model claims labeled per [[00 - Vault Management/Architecture Decisions#ADR-006 — Source-labelling convention for closed-source model architectures|ADR-006]].
- No fabrication. No placeholders presented as final content.

See [[00 - Vault Management/Architecture Decisions|Architecture Decisions]] for the full set of standards.

## Source

Built from `Master AI/Ultimate Prompt.md` and `Master AI/What to do.md` in the [ObsidainAgentGithubUplaod](https://github.com/Vtheonly/ObsidainAgentGithubUplaod) repository.

---

See also: [[MOC]] · [[Learning Roadmap]] · [[Reading Order]] · [[00 - Vault Management/Master Roadmap|Master Roadmap]]
