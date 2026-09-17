---
tags: [foundation-models, moc]
iteration: 6
created: 2026-08-07
---

# 09 — Foundation Models MOC

> [!info] Foundation models — pretrained on massive data, adaptable to many downstream tasks. This chapter covers the major categories beyond text LLMs. Iteration 6 added three new notes: Code Models (Codex, StarCoder, DeepSeek-Coder), Multimodal Foundation Models (GPT-4V, Gemini, Llama-Vision), and Embedding Model Training (contrastive learning recipe).

## Reading Order

| #   | Note                                              | Sub-domain        | Purpose                                            |
|-----|---------------------------------------------------|-------------------|----------------------------------------------------|
| 01  | [[01 - Vision Foundation Models]]                 | Vision            | ViT, CLIP, DINOv2, SigLIP, SAM.                    |
| 02  | [[02 - Embedding Models for Retrieval]]           | Embedding Models  | BGE, E5, GTE; the backbone of RAG.                 |
| 03  | [[03 - Reasoning Models]]                         | Reasoning         | o1, R1, Claude thinking; test-time compute.        |
| 04  | [[04 - Code Models]]                              | Code Models       | Codex, StarCoder, Code Llama, DeepSeek-Coder.      |
| 05  | [[05 - Multimodal Foundation Models]]             | Multimodal        | GPT-4V, Gemini, Claude, Llama-Vision, Qwen-VL.     |
| 06  | [[06 - Embedding Model Training]]                 | Embedding Models  | Contrastive learning recipe; hard negatives.       |

## Sub-Domains

- [[09 - Foundation Models/Vision/01 - Vision Foundation Models|Vision]] — note 01
- [[09 - Foundation Models/Multimodal/05 - Multimodal Foundation Models|Multimodal]] — note 05
- [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval|Embedding Models]] — notes 02, 06
- [[09 - Foundation Models/Code Models/04 - Code Models|Code Models]] — note 04
- [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models|Reasoning Models]] — note 03

## Why This Chapter Matters

Foundation models are the substrate of modern AI engineering. Understanding their categories, capabilities, and limitations is essential for choosing the right model for a task:

- **Vision tasks** (image classification, object detection): use vision foundation models.
- **Multimodal tasks** (VQA, document AI, UI agents): use multimodal foundation models.
- **Code tasks** (completion, generation, agentic coding): use code models.
- **Retrieval tasks** (RAG, semantic search): use embedding models.
- **Reasoning tasks** (math, multi-step problems): use reasoning models.

Choosing the wrong category (e.g., a general LLM for code, or a text-only LLM for vision) produces dramatically worse results than choosing the right one.

## Cross-Domain Connections

- Code models often share architecture with text LLMs but differ in training data and tokenization. See [[04 - Code Models]] and [[08 - LLMs/MOC|08 LLMs]].
- Multimodal models build on vision encoders (chapter 23) and text LLMs (chapter 08). See [[05 - Multimodal Foundation Models]] and [[23 - Multimodal AI/MOC|23 Multimodal AI]].
- Embedding models are the foundation of RAG (chapter 17). See [[06 - Embedding Model Training]] and [[17 - RAG/MOC|17 RAG]].
- Reasoning models build on the test-time compute paradigm. See [[03 - Reasoning Models]] and [[06 - Test-Time Compute Scaling]].

## Future Expansion (Iteration 7+)

- Audio foundation models (Whisper deep dive, music models).
- Video foundation models (Sora-class).
- 3D foundation models (NeRF, Gaussian Splatting).
- Multimodal embedding models (CLIP-style joint embeddings).

## See Also

- [[07 - Transformers/MOC|07 Transformers]] — the architecture
- [[23 - Multimodal AI/MOC|23 Multimodal AI]] — deep dive on multimodal
- [[08 - LLMs/MOC|08 LLMs]] — text foundation models
- [[17 - RAG/MOC|17 RAG]] — where embedding models matter most
- [[10 - Model Architecture Research/MOC|10 Model Architecture Research]] — per-model deep dives
