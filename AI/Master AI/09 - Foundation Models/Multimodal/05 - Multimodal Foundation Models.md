---
tags: [foundation-models, multimodal, gpt-4v, gemini, llama-vision]
iteration: 6
created: 2026-08-08
aliases: [Multimodal Foundation Models, VLM, MLLM, Vision-Language Models]
---

# 05 — Multimodal Foundation Models

> [!info] TL;DR
> Multimodal foundation models process more than one modality — typically text + images, but increasingly text + images + audio + video. The major families are **GPT-4V/4o/5** (OpenAI, closed), **Gemini** (Google, closed), **Claude 3/3.5/4 Sonnet & Opus** (Anthropic, closed), **Llama 3.2 Vision / Llama 4** (Meta, open), **Qwen-VL / Qwen2-VL** (Alibaba, open), and **InternVL** (Shanghai AI Lab, open). Two architectural paradigms dominate: **multimodal-native** (trained from scratch on interleaved multimodal data, e.g., Gemini) and **bolt-on** (vision encoder added to a pretrained LLM, e.g., LLaVA, Llama-Vision). Each has different capability profiles and training costs.

## Why Multimodal Foundation Models Matter

Most real-world information is multimodal. Documents have text and figures. Web pages have text and images. Conversations have speech and gestures. A text-only LLM is blind to half of this information.

Multimodal foundation models close this gap. They can:

- **Answer questions about images**: "What's in this picture?", "Read the text on this sign."
- **Understand documents**: parse PDFs with text, tables, and figures.
- **Reason about UIs**: "Click the submit button" (for UI agents).
- **Process video**: summarize, answer questions, detect events.
- **Transcribe and translate speech**: end-to-end speech-to-text and speech-to-speech translation.

The economic significance is large: document AI, accessibility tools, robotics, autonomous vehicles, and content moderation all rely on multimodal understanding.

## Two Architectural Paradigms

### Multimodal-Native (Trained from Scratch)

The model is trained from initialization on interleaved multimodal data: sequences that mix text tokens, image patches, and audio frames. The attention mechanism operates across modalities from the start.

- **Pros**: tight cross-modal integration; the model learns joint representations rather than late fusion.
- **Cons**: requires massive multimodal training data from the start; expensive; can't reuse a pretrained text-only LLM.
- **Examples**: Gemini (Google), GPT-4o (OpenAI). **Status:** Officially Confirmed for Gemini; Strongly Inferred for GPT-4o.

In a multimodal-native model, the modalities share the same transformer blocks. An image patch and a text token attend to each other in every layer. This produces deeper integration than bolt-on approaches.

### Bolt-On (Vision Encoder + Pretrained LLM)

The model starts with a pretrained LLM and adds a vision encoder (CLIP, SigLIP, etc.). A projection module maps vision features into the LLM's embedding space. The LLM is then fine-tuned on image-text data.

- **Pros**: reuses expensive pretrained components (LLM and vision encoder); fast to train (hours-days vs. months).
- **Cons**: looser cross-modal integration; vision features enter the LLM as "soft tokens" that the LLM must learn to interpret.
- **Examples**: LLaVA, Llama 3.2 Vision, Qwen-VL, InternVL.

The bolt-on approach dominates open-weights VLMs because it's tractable without massive compute. See [[03 - LLaVA]] and [[10 - Build a Vision-Language Model]] for the LLaVA recipe.

### Hybrid (Mostly Bolt-On, Partially Native)

Some models (GPT-4V, Claude 3.5 Sonnet) appear to use a hybrid: a pretrained LLM core with vision added early in training, but not from initialization. **Status:** Strongly Inferred — neither OpenAI nor Anthropic has disclosed architecture details.

## The Major Multimodal Model Families

### GPT-4V / GPT-4o / GPT-5 (OpenAI, closed)

GPT-4V (2023) was OpenAI's first multimodal model, added to GPT-4. GPT-4o (2024) is "omnimodal" — natively handles text, image, and audio. GPT-5 (if released) is presumed to extend this. **Architecture:** Not officially disclosed. **Strongly Inferred:** multimodal-native (based on GPT-4o's low latency for audio, suggesting end-to-end audio processing without a separate ASR step). **Strengths:** broad capability, excellent OCR, strong visual reasoning. **Status as of 2026:** GPT-4o and successors are the default multimodal API for most developers.

### Gemini (Google, closed)

Gemini 1.0 (2023) was Google's first multimodal-native model. Gemini 1.5 Pro (2024) added a 1M-2M token context window. Gemini 2.0 (late 2024) and 2.5 (2025) improved reasoning. **Architecture:** multimodal-native, MoE in some versions. **Officially Confirmed** for the multimodal-native property (Gemini 1 paper, 2023). **Strengths:** massive context, native video understanding, strong document AI.

### Claude 3 / 3.5 / 4 (Anthropic, closed)

Claude 3 (2024) added vision to Claude. Claude 3.5 Sonnet (2024) significantly improved visual reasoning. Claude 4 / Opus (2025) extended this. **Architecture:** Not officially disclosed. **Strongly Inferred:** bolt-on or hybrid vision approach. **Strengths:** strong document understanding, careful refusals, good handwriting OCR. Anthropic publishes less about architecture than Google but more about capabilities.

### Llama 3.2 Vision / Llama 4 (Meta, open)

Llama 3.2 Vision (2024): 11B and 90B parameter vision-language models based on Llama 3.1 text. Llama 4 (2025, if released) extends to multimodal-native. **Architecture:** bolt-on (vision encoder + adapter on Llama 3.1). **Strengths:** open weights, strong performance, reusable for fine-tuning. **Licensing:** Llama community license.

### Qwen-VL / Qwen2-VL / Qwen2.5-VL (Alibaba, open)

Qwen-VL (2023): first-generation vision-language model from Alibaba. Qwen2-VL (2024): significantly improved, supports dynamic resolution (variable image sizes). Qwen2.5-VL (2025): further improvements, strong on document AI. **Architecture:** bolt-on (ViT + adapter on Qwen2). **Strengths:** excellent OCR, dynamic resolution, permissive licensing. **Best open-weights VLM** for many use cases as of 2025.

### InternVL (Shanghai AI Lab, open)

InternVL (2024): a family of VLMs from Shanghai AI Lab. Uses a large ViT (6B parameters in InternVL-Chat-V1.5) for richer vision features. **Architecture:** bolt-on with oversized vision encoder. **Strengths:** strong on fine-grained visual detail (small text, distant objects). Permissive MIT license.

## Key Architectural Components

### Vision Encoders

Most VLMs use one of:

- **CLIP** (OpenAI, 2021): the original vision-language encoder. See [[02 - CLIP]].
- **SigLIP** (Google, 2023): sigmoid loss instead of softmax; better at scale.
- **DINOv2** (Meta, 2023): self-supervised vision encoder; richer features for some tasks.
- **Custom large ViTs**: InternVL uses a 6B-parameter ViT; some Gemini versions reportedly use custom vision encoders.

The vision encoder matters more than people initially expected. LLaVA-1.5 with SigLIP outperforms LLaVA-1.5 with CLIP, even with identical LLMs and projections.

### Projection Modules

- **Linear**: simplest, used in LLaVA-1. Works okay but limited capacity.
- **MLP**: 2-layer MLP with GELU; used in LLaVA-1.5+. Significantly better than linear.
- **Perceiver Resampler**: a small cross-attention module that compresses N vision tokens to K (e.g., 576 → 64). Used in Flamingo, Qwen-VL. Reduces the LLM's vision-token burden.
- **Pixel Shuffle**: rearranges spatial dimensions into channels, reducing the number of vision tokens. Used in Qwen2-VL.

### Tokenization of Images

- **Patch embeddings**: standard ViT approach. Image is split into 14×14 (or 16×16) patches, each embedded into a vector.
- **Dynamic resolution**: instead of resizing all images to 336×336, the model accepts variable image sizes and tiles large images into multiple 336×336 patches. Used in Qwen2-VL, LLaVA-NeXT, InternVL.
- **Multi-scale**: some models process the image at multiple resolutions in parallel.

Dynamic resolution is the most important recent innovation. It allows VLMs to read small text in high-resolution images — a capability the original LLaVA completely lacked.

### Position Embeddings for Vision

Vision encoders use 2D positional embeddings (sinusoidal or learned) to encode patch positions. When the vision features are projected into the LLM, the LLM's 1D position embeddings take over. Some VLMs (Qwen2-VL) use 2D-aware position embeddings even in the LLM, preserving spatial information.

## Training Recipes

### Stage 1: Projection Pretraining

Train only the projection (the MLP mapping vision features to LLM space) on image-caption pairs. Vision encoder and LLM are frozen. This teaches the projection to translate vision features into the LLM's vocabulary.

- **Data**: ~500K image-caption pairs (e.g., CC3M, LAION-COCO).
- **Compute**: hours on a single GPU.
- **Result**: a model that can describe images but doesn't follow instructions well.

### Stage 2: Instruction Tuning

Train the projection and (optionally) the LLM on image-text instruction data. The LLM is usually fine-tuned with LoRA to keep parameter count manageable.

- **Data**: ~500K image-instruction-response triples (e.g., LLaVA-Instruct).
- **Compute**: days on a single GPU, or hours on multi-GPU.
- **Result**: a model that follows instructions about images.

### Stage 3: Multimodal RLHF (Optional)

Some VLMs (GPT-4V, Gemini) undergo RLHF with multimodal preferences. The reward model scores image-text responses on helpfulness, harmlessness, and hallucination. **Status:** rarely done in open-weights VLMs due to the cost of collecting multimodal preference data.

## Evaluation

Multimodal models are evaluated on:

- **VQA** (Visual Question Answering): answer questions about images.
- **GQA**: a more rigorous VQA with structured question types.
- **MMMU** (Massive Multi-discipline Multimodal Understanding): college-level questions requiring visual reasoning across disciplines.
- **MMBench**: a multilingual multimodal benchmark.
- **DocVQA**: question answering about document images.
- **ChartQA**: question answering about charts.
- **MMMU-Pro**: a harder version of MMMU designed to defeat pattern-matching.
- **Video-MME**: video understanding benchmark.

The frontier benchmarks (MMMU, MMMU-Pro) are where 2026-era models differentiate. Early VLMs scored 30-40% on MMMU; current frontier models score 60-70%.

## Strengths and Limitations of Current Multimodal Models

### Strengths

- **Image captioning**: most VLMs produce fluent, accurate captions for common images.
- **Document understanding**: reading text in images, parsing tables, understanding forms.
- **Visual reasoning**: answering questions that require spatial reasoning, object relationships, and common sense.
- **OCR**: modern VLMs rival dedicated OCR systems for printed text and exceed them for handwriting.

### Limitations

- **Hallucination**: VLMs sometimes describe objects that aren't in the image. Mitigation: train on negative examples ("What's in this image?" → "Nothing relevant").
- **Counting**: VLMs are unreliable at counting more than ~5 objects.
- **Spatial reasoning**: "left of", "behind" are often wrong, especially in complex scenes.
- **Fine-grained recognition**: identifying specific breeds of dog, models of car, etc.
- **Video understanding**: temporal reasoning in video is much weaker than image understanding.
- **Audio understanding**: only GPT-4o-class models handle audio natively; most VLMs are text+image only.

## Future Directions

- **True omnimodal models**: text + image + audio + video, all natively.
- **Better long-video understanding**: current models handle ~1 minute of video; we need 1-hour.
- **Embodied AI**: VLMs that control robots, understanding the world through cameras.
- **3D understanding**: VLMs that understand depth, occlusion, and 3D structure from 2D images.
- **Multimodal reasoning**: models that reason across modalities ("this graph shows X, therefore Y").

## See Also

- [[01 - Vision Foundation Models]] — the vision encoders VLMs use
- [[02 - Embedding Models for Retrieval]] — sister domain
- [[03 - Reasoning Models]] — sister domain
- [[04 - Code Models]] — sister domain
- [[06 - Embedding Model Training]] — related training approach
- [[01 - Multimodal AI Overview]] — chapter 23 deep dive
- [[02 - CLIP]] — the vision encoder most VLMs use
- [[03 - LLaVA]] — the simplest VLM recipe
- [[06 - Cross-Modal Attention]] — fusion architectures
- [[10 - Build a Vision-Language Model]] — implement a VLM
- [[09 - Foundation Models/MOC|09 Foundation Models MOC]]
