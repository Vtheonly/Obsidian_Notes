---
tags: [paper, vit, vision, vision-transformer]
iteration: 4
created: 2026-08-08
aliases: [ViT 2020, Dosovitskiy 2020, An Image is Worth 16x16 Words]
---

# 21 — Vision Transformer / ViT (Dosovitskiy et al., 2020)

> [!info] TL;DR
> ViT applied the standard Transformer encoder (with no convolutional components) to images by splitting them into 16×16 patches, embedding each patch, and processing the sequence with self-attention. With enough pretraining data (JFT-300M, 300M images), ViT matched or exceeded CNN-based SOTA on ImageNet while using fewer parameters and compute. ViT proved that Transformers are domain-agnostic sequence models — the same architecture that works for text works for images, audio, and other modalities.

## Citation

Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., & Houlsby, N. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR 2021. arXiv:2010.11929.

## The Problem Being Solved

By 2020, Transformers dominated NLP (BERT, GPT-2, T5) but CNNs still dominated computer vision. The inductive biases of CNNs — locality (each filter sees only a small region), translation invariance (filters are shared across the image), and hierarchy (early layers detect edges, later layers detect objects) — seemed essential for vision.

Attempts to apply Transformers to images had been limited by the O(N²) cost of attention. A 224×224 image has 50,176 pixels; full attention over pixels would be 2.5B operations per layer — impractical. Prior work (Stand-Alone Self-Attention, Local Relation Networks) used local attention windows, but this reintroduced the locality bias and didn't clearly beat CNNs.

ViT's key insight: don't apply attention to pixels. Apply it to *patches*. Split the image into 16×16 patches (224×224 → 14×14 = 196 patches), embed each patch, and process the resulting 196-token sequence with a standard Transformer. This makes the sequence length manageable (196 vs 50,176) and lets you use the exact same Transformer architecture that works for NLP.

## The Architecture

ViT is a standard Transformer encoder (from [[02 - Vaswani Attention Is All You Need 2017|Vaswani 2017]]), with image-specific input processing:

### Patch Embedding
1. Split the 224×224×3 image into 16×16 patches → 14×14 = 196 patches.
2. Flatten each patch to a 768-dimensional vector (16×16×3 = 768).
3. Project with a linear layer to the model dimension (typically 768).

This is equivalent to a convolution with 16×16 kernel, stride 16, and 768 output channels — but conceptually simpler.

### [CLS] Token
Prepend a learnable `[CLS]` token to the patch sequence. The `[CLS]` token's final hidden state is used as the image representation for classification. This is borrowed directly from BERT.

### Positional Embedding
Add learned absolute positional embeddings to the patch embeddings. The model needs to know which patch came from where in the image, since attention is permutation-invariant.

### Transformer Encoder
A standard Transformer encoder: `L` layers of multi-head self-attention + feed-forward, with pre-norm and residual connections. No vision-specific components — the same architecture as BERT.

### Classification Head
The `[CLS]` token's final hidden state → linear layer → class logits. During pretraining, this head is replaced by an MLP; during fine-tuning, it's a linear classifier.

```mermaid
graph TD
  Img[224×224×3 image] --> Split[Split into 16×16 patches]
  Split --> Patches[196 patches, each 16×16×3=768]
  Patches --> Linear[Linear projection to d_model]
  Linear --> Emb[Patch embeddings: 196×768]
  CLS[[CLS] token: 1×768] --> Concat
  Emb --> Concat[Concatenate: 197×768]
  Pos[Positional embeddings: 197×768] --> Add
  Concat --> Add
  Add --> Enc[Transformer Encoder: L layers]
  Enc --> Final[Final hidden states: 197×768]
  Final --> CLSOut[[CLS] output: 768]
  CLSOut --> Head[Linear classification head]
  Head --> Logits[Class logits]
```

## The Pretraining Recipe

ViT's success depended critically on pretraining data scale. The paper compared three datasets:

| Dataset          | Size         | Result                                     |
|------------------|--------------|--------------------------------------------|
| ImageNet-1K      | 1.3M images  | ViT underperforms ResNet — insufficient data|
| ImageNet-21K     | 14M images   | ViT matches ResNet                          |
| JFT-300M         | 300M images  | ViT exceeds ResNet, fewer params + compute  |

The key finding: **ViT lacks the inductive biases of CNNs** (locality, translation invariance). CNNs can learn from small datasets because their architecture encodes useful priors. ViT must *learn* these priors from data, which requires large-scale pretraining.

With JFT-300M (300M images), ViT learns the priors and exceeds CNNs. With ImageNet-1K (1.3M images), ViT cannot learn the priors and underperforms. This "data hunger" was the main criticism of ViT and motivated subsequent work (DeiT, SWAG, DINOv2) that made ViT competitive with less data.

## Key Results

ViT matched or exceeded CNN-based SOTA on ImageNet, with fewer parameters and less pretraining compute:

| Model               | Params | Pretraining Data | ImageNet Top-1 |
|---------------------|--------|------------------|----------------|
| ResNet-152          | 60M    | ImageNet-1K      | 80.2           |
| ViT-Base            | 86M    | JFT-300M         | 84.0           |
| ViT-Large           | 307M   | JFT-300M         | 85.2           |
| ViT-Huge            | 632M   | JFT-300M         | 88.5           |

The most important comparison was on compute efficiency: ViT-Large achieved 85.2% with ~2,500 TPU-days of pretraining, while Noisy Student (a CNN-based approach) achieved 88.4% with ~9,000 TPU-days. ViT was more compute-efficient at scale.

## Why It Worked

### Patches Make Attention Tractable
By splitting the image into 16×16 patches, ViT reduces the sequence length from 50,176 to 196 — manageable for standard attention. The patch size is a trade-off: smaller patches give finer detail but longer sequences; larger patches are coarser but faster. 16×16 is a common default.

### Standard Transformer Architecture
ViT uses the exact same Transformer encoder as BERT — no vision-specific components. This means all the NLP research on Transformer optimization (FlashAttention, better positional encodings, scaling laws) transfers directly to vision. This cross-domain transfer has been hugely valuable.

### Pretraining Data Replaces Inductive Bias
CNNs encode useful priors (locality, translation invariance) in their architecture. ViT learns these priors from data. With enough data, learned priors are *better* than hardcoded priors — they adapt to the actual statistics of images rather than a designer's intuition.

### Scaling Laws Apply
Like NLP Transformers, ViT follows scaling laws: bigger models + more data + more compute = better performance, with predictable power-law relationships. This made it possible to plan model sizes and training budgets in advance.

## Limitations

### Data Hunger
ViT requires large-scale pretraining (10M+ images) to match CNNs. This was a significant barrier to adoption — most researchers don't have access to JFT-300M. Subsequent work (DeiT, DINOv2) addressed this with better training recipes and self-supervised pretraining.

### Fixed Patch Size
The 16×16 patch size is fixed at model design time. This means ViT cannot naturally handle images of arbitrary resolution — larger images require more patches, which changes the sequence length and may exceed the model's context. Modern variants (Swin Transformer, NaViT) address this with hierarchical or native-resolution approaches.

### [CLS] Token Is Limited for Dense Tasks
The [CLS] token is great for classification but not for dense prediction (segmentation, detection). For these tasks, you need per-patch representations, and ViT's flat architecture doesn't naturally provide multi-scale features the way CNN hierarchies do.

### Computational Cost for High Resolution
For high-resolution images (e.g., 1024×1024 for detection), the number of patches grows quadratically (1024/16 = 64, so 64×64 = 4096 patches). Attention is O(4096²) = 16M operations per layer — expensive. Swin Transformer and other hierarchical approaches address this.

## Successors and Modern Variants

### DeiT (Touvron et al., 2021)
"Training data-efficient image Transformers". Showed that ViT can match CNNs with ImageNet-1K-only pretraining, using a distilled [CLS] token and better training recipes. Made ViT practical for researchers without access to JFT-scale data.

### Swin Transformer (Liu et al., 2021)
"Shifted Window Transformer". Hierarchical architecture with shifted local windows. Provides multi-scale features (like CNNs) and scales to high-resolution images. Became the standard for dense prediction tasks.

### DINOv2 (Meta, 2023)
Self-supervised ViT pretraining at scale. Produces general-purpose visual features that match or exceed supervised pretraining. Used as the visual encoder in many multimodal LLMs.

### NaViT (Google, 2023)
"Native Resolution ViT". Processes images at their native resolution (variable patch count) rather than resizing to fixed 224×224. More efficient and flexible.

### SigLIP (Google, 2023)
Sigmoid loss for image-text pretraining (replaces softmax contrastive loss). Better than CLIP for many downstream tasks.

## Impact and Legacy

ViT reshaped computer vision:

1. **Transformers became the default for vision**. By 2022, most new vision models were Transformer-based. CNNs remain useful (especially for efficiency-constrained applications) but are no longer the research frontier.

2. **Cross-domain transfer of NLP innovations**. FlashAttention, RoPE, scaling laws — all developed for NLP — apply directly to vision Transformers. This synergy accelerated both fields.

3. **Foundation for multimodal models**. CLIP, Flamingo, BLIP, LLaVA, Gemini all use ViT-family encoders for the visual modality. ViT made multimodal models practical by providing a Transformer-compatible visual representation.

4. **Self-supervised visual representation**. ViT's architecture enabled DINO, DINOv2, MAE, and other self-supervised methods that learn visual features without labels. These features now power most production vision systems.

5. **End of architecture search**. Before ViT, vision researchers spent significant effort designing CNN architectures (ResNet, EfficientNet, RegNet). After ViT, the architecture question was largely settled — use a Transformer, focus on data and training. This freed research effort for other problems.

For AI engineers, ViT is the foundation of modern computer vision. If you're working with CLIP, LLaVA, SAM, or any vision-language model, you're using ViT-family encoders. Understanding ViT clarifies how images are processed and why certain design choices (patch size, [CLS] token, positional embeddings) matter.

## Further Reading

- Original paper: arXiv:2010.11929
- DeiT: arXiv:2012.12877 — data-efficient ViT training.
- Swin Transformer: arXiv:2103.14030 — hierarchical ViT for dense tasks.
- DINOv2: arXiv:2304.07193 — self-supervised ViT features.

## See Also

- [[13 - Vision Transformer ViT]]
- [[02 - Vaswani Attention Is All You Need 2017]]
- [[03 - BERT 2018]]
- [[01 - Vision Foundation Models]]
- [[01 - Multimodal AI Overview]]
- [[26 - Papers/MOC|Papers MOC]]
