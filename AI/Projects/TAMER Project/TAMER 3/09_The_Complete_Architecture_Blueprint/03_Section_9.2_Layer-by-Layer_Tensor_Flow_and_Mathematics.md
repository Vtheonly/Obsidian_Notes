## 9.2 Layer-by-Layer Tensor Flow and Mathematics

This section traces the exact mathematical transformation applied to every tensor at every layer. The goal is that you can mentally simulate a forward pass without running the code.

### The Input Tensor

Before the image enters any neural network layer, the raw pixel values (integers 0-255) are normalized to zero-mean, unit-variance floats using ImageNet statistics:

$$x_{norm} = \frac{x_{pixel}/255 - \mu}{\sigma}$$

Where:
- $\mu = [0.485, 0.456, 0.406]$ (per-channel means, RGB order)
- $\sigma = [0.229, 0.224, 0.225]$ (per-channel standard deviations)

After normalization, the pixel values are no longer integers in [0, 255]. They are floats in approximately [-2.1, 2.6] (the exact range depends on the channel). This normalization is important because:
- It centers the input distribution around zero, which helps gradient flow through the initial layers.
- It matches the statistics of ImageNet data, which the Swin-v2 backbone was pretrained on. Feeding unnormalized data to a pretrained backbone produces garbage features because the backbone's learned filters expect data in this specific numerical range.

**Input tensor shape:** `[B, 3, 256, 1024]`
- `B`: Batch size (up to 864 in Beast Mode).
- `3`: RGB channels.
- `256`: Height in pixels (after aspect-ratio-preserving resize and pad).
- `1024`: Width in pixels (after aspect-ratio-preserving resize and pad).

---

### Phase 1: Swin-v2 Backbone Extraction

#### The Patch Partition

The Swin backbone begins by partitioning the image into non-overlapping $4 \times 4$ pixel patches and linearly projecting each patch to a $C$-dimensional vector.

For a $256 \times 1024$ image with $4 \times 4$ patches:
$$\text{Number of patches} = \frac{256}{4} \times \frac{1024}{4} = 64 \times 256 = 16{,}384 \text{ patches}$$

Each patch covers 16 pixels ($4 \times 4$) across 3 channels = 48 raw values per patch. A linear layer (the "patch embedding") projects these 48 values to 128 dimensions (the channel width of Swin-v2-Base at Stage 1):

$$\text{Patch Embedding}: \mathbb{R}^{48} \to \mathbb{R}^{128}$$

After patch embedding, the tensor shape is `[B, 64, 256, 128]` (batch, height-patches, width-patches, channels).

#### The Four Hierarchical Stages

Swin-v2-Base has four stages, each consisting of Swin Transformer blocks followed by patch merging (downsampling):

| Stage | Input Resolution | Window Size | Channels | Output Resolution |
|---|---|---|---|---|
| Stage 1 | 64 × 256 patches | 8 × 8 | 128 | 64 × 256 |
| Patch Merge 1-2 | 64 × 256 | — | 128 → 256 | 32 × 128 |
| Stage 2 | 32 × 128 patches | 8 × 8 | 256 | 32 × 128 |
| Patch Merge 2-3 | 32 × 128 | — | 256 → 512 | 16 × 64 |
| Stage 3 | 16 × 64 patches | 8 × 8 | 512 | 16 × 64 |
| Patch Merge 3-4 | 16 × 64 | — | 512 → 1024 | 8 × 32 |
| Stage 4 | 8 × 32 patches | 8 × 8 | 1024 | 8 × 32 |

The `out_index=(3,)` parameter in your `timm.create_model` call means you extract the output of Stage 4 (index 3, zero-indexed). This is the deepest, most semantically rich feature map.

**Stage 4 output shape:** `[B, 1024, 8, 32]` (PyTorch convention: channels first)

The permute operation in your encoder converts this to channels-last format:
```
[B, 1024, 8, 32] → permute(0, 2, 3, 1) → [B, 8, 32, 1024]
```

This rearrangement is necessary because PyTorch's `nn.Linear` operates on the last dimension. With channels last, a linear layer can be applied to the 1024-channel dimension directly without any additional reshaping.

#### What the Stage 4 Features Represent

Each of the $8 \times 32 = 256$ vectors in the Stage 4 output corresponds to a $32 \times 32$ pixel region of the original image (since the feature map has been downsampled by $4 \times$ per stage over 2 stages of patch merging: $4 \times 4$ patch size $\times$ $2 \times 2$ merge $\times$ $2 \times 2$ merge = $4 \times 4 \times 4 = 32 \times 32$ pixels per feature vector... wait, let's recount):

Actually: the patch size is $4 \times 4$ pixels. Each stage with patch merging combines $2 \times 2$ neighboring patches into one. Stages 1→2, 2→3, and 3→4 each merge (3 merge operations). So the total downsampling from pixels to Stage 4 features is $4 \times 2 \times 2 \times 2 = 32 \times$:
- Original image: $256 \times 1024$ pixels
- Stage 4 features: $256/32 = 8$ height, $1024/32 = 32$ width → confirmed $8 \times 32$ features.

Each Stage 4 vector has a receptive field covering a $32 \times 32$ pixel region of the original image. These are high-level semantic features. A $32 \times 32$ region is large enough to contain an entire small symbol (like `x`, `+`, `=`) or a meaningful portion of a larger symbol (like the top half of `\Sigma`).

---

### Phase 2: The Spatial Bridge

#### Step A: Dimensionality Reduction (The Projection)

The Swin Stage 4 output has 1024 channels. Your model dimension `d_model` is 768 (matching the Transformer decoder dimension). A linear projection reduces the channel dimension:

$$W_{proj} \in \mathbb{R}^{1024 \times 768}$$

$$X_{proj} = X_{swin} W_{proj} + b_{proj}$$

**Shape:** `[B, 8, 32, 1024]` → Linear → `[B, 8, 32, 768]`

This projection is a learned dimensionality reduction. It is not a random compression. The gradient descent process trains this linear layer to preserve the most information relevant to predicting LaTeX tokens while reducing from 1024 to 768 dimensions. The 256 discarded dimensions are learned to be the least useful for the OCR task.

#### Step B: Layer Normalization

Layer Normalization is applied across the feature dimension (768):

$$\text{LayerNorm}(x) = \frac{x - \mu_x}{\sigma_x + \epsilon} \cdot \gamma + \beta$$

Where $\mu_x$ and $\sigma_x$ are computed per-sample and per-spatial-position across the 768 feature dimensions, and $\gamma, \beta$ are learned scale and shift parameters.

**Why LayerNorm after projection?**
The linear projection can produce feature values at wildly different scales across different batches and spatial positions. If some feature dimensions have values in the range [0, 100] and others in the range [-0.01, 0.01], the subsequent attention operations will be dominated by the large-scale dimensions. LayerNorm equalizes the scale, ensuring all 768 dimensions contribute equally to the attention computation.

**Shape:** `[B, 8, 32, 768]` → LayerNorm → `[B, 8, 32, 768]` (same shape, normalized values)

#### Step C: 2D Positional Encoding

Two separate embedding tables encode the spatial position of each patch:

$$E_R \in \mathbb{R}^{R_{max} \times 384}, \quad E_C \in \mathbb{R}^{C_{max} \times 384}$$

For each patch at grid position $(r, c)$ where $r \in [0, 7]$ and $c \in [0, 31]$:

$$PE_{2D}(r, c) = \text{concat}(E_R[r], E_C[c]) \in \mathbb{R}^{768}$$

The positional encoding is added to the normalized features:

$$X_{pos}(r, c) = X_{norm}(r, c) + PE_{2D}(r, c)$$

**Shape:** `[B, 8, 32, 768]` → Add PE → `[B, 8, 32, 768]`

After this step, each of the 256 feature vectors encodes both:
- **What** is visually present at that patch location (from the Swin features).
- **Where** in the image that patch is located (from the positional encoding).

---