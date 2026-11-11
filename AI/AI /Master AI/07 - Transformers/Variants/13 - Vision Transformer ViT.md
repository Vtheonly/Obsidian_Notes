---
tags: [transformer, vit, vision, multimodal]
iteration: 8
created: 2026-08-07
last_updated: 2026-08-08
aliases: [ViT, Vision Transformer]
---

# 13 - Vision Transformer (ViT)

> [!info] TL;DR
> ViT (Dosovitskiy et al. 2020) applies the Transformer to images by splitting an image into patches, embedding each patch as a token, and processing with a standard Transformer encoder. Now the dominant architecture for vision, especially at scale.

## The Idea

Images are 2D grids of pixels — too many tokens for naive Transformer attention. ViT's solution: **break the image into patches**, flatten each patch, and project to an embedding.

```
Image (224x224x3) → 14x14 = 196 patches of 16x16x3
                  → each patch flattened to 768-dim vector (via linear projection)
                  → add positional embedding
                  → process with Transformer encoder (12-32 layers)
                  → output: 196 contextualized patch embeddings
```

For classification, prepend a `[CLS]` token and use its final-layer representation.

## Architecture

```
Image
  ↓
Patch extraction (16x16 patches)
  ↓
Linear projection to d_model dimensions (patch embedding)
  ↓
Add positional embeddings (learned, 2D)
  ↓
Optional: prepend [CLS] token
  ↓
Transformer encoder (N blocks)
  ↓
For classification: [CLS] representation → linear head
For dense tasks: patch representations → decoder
```

## Why ViT Replaced CNNs

At scale, ViT beats ResNet-style CNNs on ImageNet and downstream tasks. Reasons:
- **Global attention** captures long-range dependencies that CNNs need many layers to learn.
- **Scales better** with data and compute.
- **Simpler architecture** — no convolution-specific design choices.
- **Multi-modal compatibility** — patches are tokens; can mix with text tokens.

But ViT has weaknesses:
- **Data-hungry** — needs large datasets to learn what CNNs learn implicitly (translation invariance, locality).
- **Less efficient on small images** — CNNs win for 32x32 (CIFAR).
- **No built-in inductive bias** for vision — the model must learn everything.

## Variants and Successors

- **DeiT** (Touvron et al. 2021): data-efficient ViT training with distillation. Works on standard ImageNet.
- **Swin Transformer** (Liu et al. 2021): hierarchical ViT with shifted windows; better for dense prediction tasks.
- **CLIP** (Radford et al. 2021): ViT image encoder + text encoder, contrastive training. Foundation for multimodal AI.
- **DINOv2 / DINOv3** (Caron et al. 2021, 2024): self-supervised ViT; produces excellent general-purpose image embeddings.
- **SigLIP** (Zhai et al. 2023): improved CLIP with sigmoid loss; better at scale.

## ViT in Multimodal Models

Modern multimodal LLMs (LLaVA, Qwen-VL, GPT-4V) use a ViT to encode images:

```
Image → ViT → patch embeddings → projector → LLM token space → LLM
```

The ViT produces image "tokens" that the LLM attends to via cross-attention (or treats as additional input tokens).

## Worked Example

```python
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

image = Image.open("cat.jpg").convert("RGB")
inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
predicted_class = logits.argmax(-1)
```

## Why This Matters for AI

- ViT is the **standard vision encoder** in 2026. Every multimodal LLM uses a ViT or ViT-derivative.
- The "patches as tokens" idea is the conceptual basis for treating any modality (audio, video, 3D) as a sequence.
- For **RAG with images** (PDFs with figures, screenshots, diagrams), ViT-based encoders produce the embeddings.

## Production Implications

- For **image classification** with sufficient data, fine-tune a pretrained ViT. HuggingFace `timm` library has hundreds of variants.
- For **embedding images in RAG**, use DINOv2 or SigLIP — produce general-purpose image embeddings.
- For **multimodal LLMs** (LLaVA, Qwen-VL), the ViT is the image encoder; choose a model with a strong ViT.
- **Quantization**: ViT quantizes well to INT8. Most serving frameworks support it.
- **Patch size matters**: smaller patches = more tokens = more compute. 16x16 is standard; 14x14 for higher resolution.

## Common Pitfalls

- **Wrong image preprocessing** — ViT expects specific normalization (ImageNet stats typically). Mismatch → silent quality loss.
- **Image size mismatch** — ViT's positional embeddings are tied to the training resolution. Resizing requires interpolating positional embeddings.
- **Too few patches for high-res** — for fine-grained tasks, use a smaller patch size or higher resolution.
- **Forgetting `[CLS]` for classification** — global average pooling works too, but `[CLS]` is the ViT default.

## Further Reading

- Dosovitskiy et al. (2020), *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale* (ViT).
- Touvron et al. (2021), *Training data-efficient image transformers & distillation through attention* (DeiT).
- Liu et al. (2021), *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*.
- Radford et al. (2021), *Learning Transferable Visual Models From Natural Language Supervision* (CLIP).

## The Patchify Operation in Detail

The patchify step is the conceptual bridge from images to sequences. Given an image $X \in \mathbb{R}^{H \times W \times C}$ and patch size $P$, you split $X$ into $N = (H/P) \cdot (W/P)$ non-overlapping patches, each of shape $P \times P \times C$. Each patch is flattened to a $P^2 C$-vector and projected to $d_{\text{model}}$ via a linear layer.

For the standard ViT-Base/16 on 224×224 images: $N = 14 \times 14 = 196$ patches, $P=16$, $C=3$, so each flattened patch has $16 \cdot 16 \cdot 3 = 768$ elements — conveniently equal to $d_{\text{model}} = 768$, so the projection is essentially identity plus a learned bias. This is not a coincidence; the patch size and $d_{\text{model}}$ were chosen to make the math clean.

Equivalent implementations:
```python
# Option A: Convolution with stride = patch size (most common)
self.patch_embed = nn.Conv2d(3, d_model, kernel_size=16, stride=16)
# x: (B, 3, 224, 224) → (B, d_model, 14, 14) → reshape (B, 196, d_model)

# Option B: Explicit unfold + linear
patches = x.unfold(2, 16, 16).unfold(3, 16, 16)  # (B, 3, 14, 14, 16, 16)
patches = patches.contiguous().view(B, 196, 768)
tokens = self.proj(patches)  # (B, 196, d_model)
```

The Conv2d version is preferred — it's a single fused op and is faster. The unfold version is more pedagogical.

## Computational Complexity of ViT

For an image of $N$ patches with hidden size $d$ and $L$ layers:
- **Self-attention**: $O(N^2 \cdot d)$ per layer (the same quadratic complexity as text attention).
- **FFN**: $O(N \cdot d^2)$ per layer.
- **Total**: $O(L \cdot N^2 \cdot d + L \cdot N \cdot d^2)$.

For 224×224 images with 16×16 patches: $N=196$, totally fine. For 1024×1024 images: $N=4096$, $N^2 \approx 17M$ — memory becomes the bottleneck. This is why high-resolution vision models use:
- **Windowed attention** (Swin): $O(N \cdot w^2)$ instead of $O(N^2)$.
- **Hierarchical downsampling** (Swin, ViTDet): reduce $N$ after early layers.
- **Linear attention** (Perceiver, Hyena): replace softmax with a kernelized approximation.

## Positional Embeddings: Why Learned Beats Sinusoidal for Vision

The original ViT used **learned** 1D positional embeddings (one vector per patch position), unlike the original Transformer (sinusoidal). This works because:
1. Image patches have a clear 2D structure, but the 1D positional embedding is sufficient because the model can learn the 2D layout from the data.
2. Sinusoidal 1D positional encodings don't naturally encode 2D structure.
3. Learned embeddings are simpler and empirically equivalent or better.

For **variable resolution** (e.g., processing 224×224 and 384×384 with the same model), the learned embeddings need to be interpolated. The standard technique:
```python
# Interpolate positional embeddings to new resolution
import torch.nn.functional as F
pos_embed = model.pos_embed  # (1, 197, d)  — 196 patches + CLS
new_N = (new_size // patch_size) ** 2
old_grid = int((pos_embed.shape[1] - 1) ** 0.5)  # 14
new_grid = int(new_N ** 0.5)                      # e.g., 24
pos_tokens = pos_embed[:, 1:]  # drop CLS
pos_tokens = pos_tokens.reshape(1, old_grid, old_grid, d).permute(0, 3, 1, 2)
pos_tokens = F.interpolate(pos_tokens, size=(new_grid, new_grid), mode='bicubic', align_corners=False)
pos_tokens = pos_tokens.permute(0, 2, 3, 1).reshape(1, new_N, d)
new_pos_embed = torch.cat([pos_embed[:, :1], pos_tokens], dim=1)
```

This bicubic interpolation works well — fine-tuning a 224×224 model at 384×384 is a standard trick to boost accuracy by ~1-2%.

## Variants Comparison Table

| Variant       | Year | Key Innovation                                  | Best For                              |
|---------------|------|-------------------------------------------------|---------------------------------------|
| ViT           | 2020 | Patches as tokens, plain Transformer encoder    | Large-scale classification            |
| DeiT          | 2021 | Distillation token, strong augmentation         | Data-efficient training (ImageNet only)|
| Swin          | 2021 | Shifted window attention, hierarchical          | Dense prediction (detection, segmentation) |
| ViTDet        | 2022 | Plain ViT for detection via simple neck         | Detection without hierarchical backbone |
| BEiT          | 2021 | Masked image modeling (BERT for images)         | Self-supervised pretraining           |
| MAE           | 2022 | Masked autoencoders (75% masking)               | Efficient self-supervised pretraining |
| DINOv2/v3     | 2023-24 | Self-distillation + image-level contrastive   | General-purpose frozen features       |
| SigLIP        | 2023 | Sigmoid loss (vs softmax) for CLIP training     | Image-text alignment at scale         |
| EVA / EVA-02  | 2023-24 | CLIP-initialized, weakly-supervised scaling  | State-of-the-art open vision encoder  |
| NaViT         | 2023 | Native aspect ratio, no resizing                | Variable-resolution training          |

## Modern ViT Encoder Used in VLMs

The vision encoders in 2024-2026 VLMs (LLaVA-NeXT, Qwen2-VL, InternVL, Cambrian) typically use:
- **Open-CLIP ViT-L/14@336** or **SigLIP-SO/14@384** as the backbone.
- Frozen or LoRA-tuned vision encoder.
- 2-4 layer MLP projector (or Q-Former for BLIP-2) to map ViT tokens to LLM embedding space.
- Optional dynamic resolution (NaViT-style) to handle arbitrary aspect ratios.

A typical LLaVA-NeXT setup:
```python
class LlavaVisionEncoder(nn.Module):
    def __init__(self, llm_dim=4096):
        super().__init__()
        self.vit = create_vit("siglip-so400m-patch14-384")  # frozen
        self.projector = nn.Sequential(
            nn.Linear(self.vit.dim, llm_dim),
            nn.GELU(),
            nn.Linear(llm_dim, llm_dim),
        )
    def forward(self, images):
        with torch.no_grad():
            patch_features = self.vit(images)  # (B, N_patches, vit_dim)
        return self.projector(patch_features)  # (B, N_patches, llm_dim)
```

The number of image tokens depends on resolution: 384×384 / 14² = 27×27 = 729 tokens, or 1024×1024 → 5329 tokens. This is why high-res VLMs are expensive — each image can consume thousands of context tokens.

## Common Failure Modes in Production

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Quality drop on real images vs benchmarks | Wrong normalization stats | Use ImageNet stats or model-specific stats from the model card |
| Quality varies wildly with image size | Positional embedding not interpolated | Use bicubic interpolation when resizing |
| Image tokens leak into text generation | Chat template misconfigured | Check the chat template handles `<image>` tokens correctly |
| Out-of-memory on long-context VLM | Too many image tokens at high res | Tile the image (LLaVA-NeXT) or use lower resolution |
| ViT works on 224 but fails on 384 | Forgot to interpolate pos embeddings | Always interpolate when changing resolution |
| Different results from `transformers` vs `timm` | Different default preprocessing | Use the exact processor for the model you loaded |

## Connection to Other Concepts

- [[07 - BERT]] — ViT is "BERT for images": same encoder-only architecture, different input tokenization.
- [[23 - Multimodal AI/Vision-Language/02 - CLIP|CLIP]] — most common use of ViT as one tower of a contrastive model.
- [[23 - Multimodal AI/Vision-Language/03 - LLaVA|LLaVA]] — ViT as the vision encoder in a VLM.
- [[23 - Multimodal AI/Diffusion/05 - DiT and FLUX|DiT/FLUX]] — same patchify idea applied to diffusion models.
- [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA|GQA/MQA]] — modern ViT variants use GQA for efficiency.
- [[04 - Neural Networks/Architectures/03 - CNNs|CNNs]] — the architecture ViT replaced at scale.

## Interview Questions

1. **Q: How does ViT convert an image into a sequence?**
   A: Patchify — split the image into non-overlapping $P \times P$ patches, flatten each, linearly project to $d_{\text{model}}$, add positional embeddings, prepend an optional `[CLS]` token. For 224×224 with $P=16$, this gives 196 patch tokens.

2. **Q: Why does ViT need more data than CNNs to train from scratch?**
   A: CNNs have built-in inductive biases — locality (convolution kernel), translation invariance (weight sharing), and hierarchical feature composition. ViT has none of these — attention is permutation-invariant (positional embeddings add order, not locality). Without these priors, ViT must learn them from data, requiring ~10-100× more images than CNNs to match performance.

3. **Q: How do you fine-tune a ViT pretrained at 224 resolution on 384 resolution images?**
   A: Bicubic-interpolate the learned positional embeddings to the new grid size (14×14 → 24×24 for 384), keep the patch size constant (16), and fine-tune for a few epochs. The model adapts quickly because the patch embeddings are resolution-agnostic; only the position information changes.

4. **Q: When would you choose Swin over ViT?**
   A: For dense prediction tasks (object detection, semantic segmentation, panoptic). Swin's hierarchical features (multi-scale) and windowed attention ($O(N)$ instead of $O(N^2)$) make it dramatically more efficient for high-resolution outputs. For classification or as a VLM encoder, plain ViT is usually better — Swin's hierarchical structure complicates the projector.

5. **Q: Why is the [CLS] token used for classification instead of global average pooling?**
   A: Two reasons. (1) The [CLS] token is explicitly trained to aggregate information for the classification task (it has no positional content of its own, so it must learn to attend globally). (2) Global average pooling averages all patch tokens, including those far from the salient object, which can dilute signal. Empirically, [CLS] is ~0.5% better on ImageNet, but GAP works nearly as well and is simpler.

6. **Q: How many tokens does a 1024×1024 image produce with patch size 14?**
   A: $(1024/14)^2 \approx 73^2 = 5329$ tokens. With $d_{\text{model}}=1152$, this is 6.1M elements per image — significant context budget. This is why VLMs use dynamic resolution (NaViT) or tiling (LLaVA-NeXT) to manage cost.

## See Also

- [[04 - Neural Networks/Architectures/03 - CNNs|CNNs]]
- [[07 - BERT]] — ViT is essentially "BERT for images"
- [[23 - Multimodal AI/MOC|Multimodal AI MOC]]
- [[07 - Transformers/MOC|Transformers MOC]]