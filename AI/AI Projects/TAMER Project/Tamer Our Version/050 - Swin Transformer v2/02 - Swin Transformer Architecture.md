---
source_collections:
  - "TAMER 1"
  - "TAMER 2"
  - "TAMER 3"
original_paths:
  - "TAMER 2/Chapter 4 - Swin Transformer v2/2. Swin Transformer Architecture.md"
  - "TAMER 1/Chapter 2/2.2 Swin Transformer V2.md"
  - "TAMER 3/04_Sequence_Generation_The_Voice/03_Section_2_Swin_Transformer_v2_Architecture.md"
roles_in_master:
  - "canonical"
  - "supplement"
topic: "swin_arch"
master_chapter: "50_Swin_Transformer_v2"
master_filename: "02_Swin_Transformer_Architecture.md"
n_source_files_merged: 3
merged: True
---

# 2. Swin Transformer Architecture

## 2.1 Swin = Shifted Window Transformer

The **Swin Transformer** (Liu et al., 2021) was designed to solve the fundamental scalability problem of Vision Transformers: global self-attention is $O(n^2)$ in the number of tokens, making it infeasible for high-resolution images. Swin's solution is elegantly simple yet powerful: **compute attention within local windows**, and **shift the windows** between layers to enable cross-window communication.

"Swin" stands for **S**hifted **Win**dow, and this dual mechanism — local windows + shifting — is the key innovation that makes hierarchical Vision Transformers practical for high-resolution inputs like math formula images.

The name also references the "shifted window" approach being analogous to how a swan glides across water — smooth, efficient, and covering the full surface through overlapping passes.

## 2.2 Local Window Attention

Instead of computing attention over all $n$ tokens (which costs $O(n^2)$), Swin computes attention within non-overlapping windows of size $M \times M$ (default $M=7$).

For a feature map of size $H \times W$ with $M \times M$ windows:

- Number of windows: $\frac{H}{M} \times \frac{W}{M}$
- Tokens per window: $M \times M = M^2$
- Attention cost per window: $O(M^4)$ (since each of $M^2$ tokens attends to $M^2$ others)
- **Total attention cost**: $O\left(\frac{HW}{M^2} \times M^4\right) = O(HW \times M^2)$

This is **linear** in the image size ($HW$), compared to the quadratic $O((HW)^2)$ of global attention! For TAMER's 16,384 patches:

| Method | Complexity | Relative Cost |
|---|---|---|
| Global attention | $O(16{,}384^2) = O(2.68 \times 10^8)$ | 336× |
| Window attention (M=7) | $O(16{,}384 \times 49) = O(8.03 \times 10^5)$ | 1× |

This **336× reduction** is what makes it feasible to process math formula images at full resolution.

## 2.3 Window Partitioning

The process of dividing a feature map into windows is straightforward:

1. Start with a feature map of shape $(B, H, W, C)$ where $B$ is batch size, $H \times W$ is the spatial dimensions, and $C$ is the channel dimension.
2. Reshape to $(B, H/M, M, W/M, M, C)$ — splitting height and width into grid cells of size $M$.
3. Permute and reshape to $(B \times H/M \times W/M, M^2, C)$ — each window is now a separate "sequence" of $M^2$ tokens.
4. Apply self-attention independently to each window.
5. Reverse the reshaping to restore the original spatial layout.

```python
def window_partition(x, window_size):
    """Partition feature map into non-overlapping windows."""
    B, H, W, C = x.shape
    x = x.view(B, H // window_size, window_size, W // window_size, window_size, C)
    windows = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size**2, C)
    return windows  # (num_windows * B, window_size**2, C)

def window_reverse(windows, window_size, H, W):
    """Reverse window partitioning."""
    B = int(windows.shape[0] / (H * W / window_size / window_size))
    x = windows.view(B, H // window_size, W // window_size, window_size, window_size, -1)
    x = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(B, H, W, -1)
    return x
```

**Important constraint**: The feature map dimensions ($H$ and $W$) must be divisible by the window size $M$. If they are not, the image must be padded to the nearest multiple of $M$.

## 2.4 The Shifted Window: Enabling Cross-Window Communication

Local window attention has a critical limitation: **tokens in different windows cannot communicate**. If window attention is applied repeatedly without any mechanism for cross-window information flow, each window would develop an isolated representation, and the model would behave like a set of independent small Transformers.

The **shifted window** solves this elegantly. In alternating layers:

- **Regular (W-MSA)**: Windows are partitioned starting from position $(0, 0)$
- **Shifted (SW-MSA)**: Windows are partitioned starting from position $(M/2, M/2)$, i.e., the grid is shifted by half a window size

By shifting the window partition, tokens that were in different windows in the regular layer are now in the same window in the shifted layer. Over two consecutive layers (regular + shifted), every token can communicate with every neighboring token — and through stacking many such pairs, information propagates across the entire feature map.

Think of it like a checkerboard: in the first layer, you process the black squares; in the next layer, you process a shifted checkerboard where the white squares are now grouped together with their black neighbors.

### How Much Information Propagates?

In one regular+shifted pair, each token can reach its $M \times M$ neighborhood (regular) plus the shifted neighborhood. After $k$ pairs, information can propagate across approximately $k \times M$ patches in each direction. For $M=7$ and 4 stages of [2, 2, 18, 2] blocks (24 total, 12 pairs), information can propagate across roughly $12 \times 7 = 84$ patches — covering the entire feature map at the lower-resolution stages.

## 2.5 Cyclic Shifting: Efficient Implementation

A naive implementation of the shifted window would require padding to handle the boundary windows (which are smaller than $M \times M$ after shifting). Instead, Swin uses **cyclic shifting**:

1. **Shift the feature map** circularly by $(M/2, M/2)$ positions
2. **Partition into regular windows** (all windows are now full $M \times M$)
3. **Compute attention** within each window
4. **Reverse the partitioning** and **shift back** circularly

The cyclic shift moves tokens from the right edge to the left edge and from the bottom edge to the top edge. This creates some "boundary windows" that contain tokens from non-adjacent regions of the image. To prevent these unrelated tokens from attending to each other, an **attention mask** is applied that zeros out cross-boundary attention scores.

```python
# Cyclic shift
shifted_x = torch.roll(x, shifts=(-shift_size, -shift_size), dims=(1, 2))

# Partition into windows
windows = window_partition(shifted_x, window_size)

# Compute attention with mask
attn_windows = self.attn(windows, mask=attn_mask)

# Reverse partitioning and shift back
shifted_x = window_reverse(attn_windows, window_size, H, W)
x = torch.roll(shifted_x, shifts=(shift_size, shift_size), dims=(1, 2))
```

The attention mask is precomputed and cached, so there is no runtime overhead for creating it. This implementation is significantly more efficient than padding-based approaches because it avoids variable-size windows and the associated memory fragmentation.

## 2.6 The Hierarchical Structure: 4 Stages

Swin Transformer follows a **hierarchical** design inspired by CNNs like ResNet. The network consists of 4 stages, each operating at a different spatial resolution and channel dimension:

| Stage | Spatial Resolution | Channels | Blocks | Patch Count (256×1024) |
|---|---|---|---|---|
| 1 | $\frac{H}{4} \times \frac{W}{4}$ | 96 | 2 | $64 \times 256 = 16{,}384$ |
| 2 | $\frac{H}{8} \times \frac{W}{8}$ | 192 | 2 | $32 \times 128 = 4{,}096$ |
| 3 | $\frac{H}{16} \times \frac{W}{16}$ | 384 | 18 | $16 \times 64 = 1{,}024$ |
| 4 | $\frac{H}{32} \times \frac{W}{32}$ | 768 | 2 | $8 \times 32 = 256$ |

The first stage starts with high spatial resolution and low channel count (fine details, simple features). Each subsequent stage halves the spatial resolution and doubles the channels (coarser spatial, more abstract features). This is analogous to how CNNs build hierarchical representations.

**Why stage 3 has 18 blocks**: Stage 3 operates at the "sweet spot" of resolution and channel depth — $16 \times 64$ patches with 384 channels. This resolution is coarse enough for efficient window attention but still fine enough to capture important spatial relationships. The 18 blocks give the model ample capacity to learn complex mid-level features. This is also the most computationally expensive stage.

## 2.7 Patch Merging: Downsampling Between Stages

Between stages, Swin uses **patch merging** to reduce the spatial resolution and increase the channel dimension. This operation is analogous to strided convolution or pooling in CNNs.

Patch merging works as follows:

1. Take each group of $2 \times 2$ neighboring patches
2. Concatenate their features along the channel dimension: $4C \rightarrow 4C$
3. Apply a linear layer to reduce channels: $4C \rightarrow 2C$
4. The result has half the spatial resolution and twice the channels

```python
class PatchMerging(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.norm = nn.LayerNorm(4 * dim)
        self.reduction = nn.Linear(4 * dim, 2 * dim, bias=False)

    def forward(self, x, H, W):
        # x: (B, H*W, C)
        x0 = x[:, 0::2, 0::2, :]  # Top-left
        x1 = x[:, 1::2, 0::2, :]  # Bottom-left
        x2 = x[:, 0::2, 1::2, :]  # Top-right
        x3 = x[:, 1::2, 1::2, :]  # Bottom-right

        x = torch.cat([x0, x1, x2, x3], dim=-1)  # (B, H/2, W/2, 4C)
        x = x.view(B, -1, 4 * C)

        x = self.norm(x)
        x = self.reduction(x)  # (B, H/2 * W/2, 2C)
        return x
```

**Why not strided convolution?** Patch merging preserves all information from the $2 \times 2$ group by concatenation before reduction. Strided convolution would discard some information through the stride operation. Patch merging is a lossless combination followed by a learned, lossy compression — giving the model more control over what to preserve.

## 2.8 Swin-Base Configuration

TAMER uses the **Swin-Base** variant of Swin Transformer v2, with the following specifications:

| Parameter | Value |
|---|---|
| Model variant | Swin-Base |
| Embedding dimension ($d_{\text{model}}$) | 96 (initial), expanding to 768 at stage 4 |
| Number of attention heads | [3, 6, 12, 24] across stages (ratio: dim/head = 32) |
| Window size ($M$) | 7 |
| Depths (blocks per stage) | [2, 2, 18, 2] = 24 total blocks |
| Drop path rate | 0.1–0.3 (stochastic depth) |
| Total parameters | ~88M |

The head dimension is consistently 32 across all stages (96/3 = 192/6 = 384/12 = 768/24 = 32). This is a design choice that keeps the per-head computation constant while scaling the number of heads with the channel dimension.

**Why Swin-Base and not Swin-Small or Swin-Large?**
- **Swin-Tiny** (28M params): Too few parameters for the complexity of math formulas
- **Swin-Small** (50M params): Adequate but less capacity for fine-grained recognition
- **Swin-Base** (88M params): Good balance of capacity and efficiency
- **Swin-Large** (197M params): More capacity but significantly slower, with diminishing returns for OCR

## 2.9 Relative Position Bias

Within each window, Swin Transformer uses **relative position bias (RPB)** instead of absolute positional embeddings. The bias is added to the attention scores before softmax:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + B\right) V$$

Where $B \in \mathbb{R}^{M^2 \times M^2}$ is the relative position bias matrix. Each entry $B_{ij}$ corresponds to the relative position between token $i$ and token $j$ within the window.

**Why relative instead of absolute?**

- **Translation equivariance**: A symbol's identity depends on its relative position to other symbols, not its absolute position. The fraction bar's meaning doesn't change whether it's in the top-left or center of the image.
- **Parameter efficiency**: The number of unique relative positions is $(2M-1) \times (2M-1) = 169$ for $M=7$, which is far fewer than $M^2 \times M^2 = 2401$ absolute position pairs. The bias table has only 169 learnable parameters.
- **Generalization**: Relative positions generalize to different image sizes — the same bias table works regardless of how many windows there are.

The relative position bias is indexed by computing the 2D offset $(\Delta x, \Delta y)$ between each pair of positions within a window and looking up the corresponding bias value from a learnable table.

## 2.10 Stochastic Depth (Drop Path)

Swin Transformer uses **stochastic depth** (also called DropPath) as a regularization technique. During training, each residual block has a probability $p$ of being "dropped" (bypassed), which means only the residual connection is active:

$$\text{output} = x + \text{DropPath}(\text{Sublayer}(x))$$

When dropped, the output is simply $x$ (identity). When not dropped, it is $x + \text{Sublayer}(x)$ as usual.

The drop rate increases linearly with depth: earlier blocks have lower drop rates, later blocks have higher rates. This makes sense because:
- Early blocks capture fundamental features that later blocks depend on
- Later blocks are more redundant (deeper networks have more capacity than needed)
- Dropping later blocks provides regularization without destabilizing the network

For Swin-Base with 24 blocks and a maximum drop rate of 0.3:
- Block 1 drop rate: ~0.01
- Block 12 drop rate: ~0.15
- Block 24 drop rate: ~0.30

## 2.11 Mermaid Diagram: Swin Hierarchy

```mermaid
flowchart TD
    Input["Input Image<br/>(256 × 1024 × 3)"] --> PatchEmb["Patch Embedding<br/>4×4 Conv, stride 4<br/>(64 × 256 × 96)"]

    PatchEmb --> Stage1["Stage 1<br/>2 × SwinBlock<br/>W-MSA → SW-MSA<br/>16,384 patches × 96d"]

    Stage1 --> Merge1["Patch Merging<br/>2×2 → 1<br/>96d → 192d"]

    Merge1 --> Stage2["Stage 2<br/>2 × SwinBlock<br/>W-MSA → SW-MSA<br/>4,096 patches × 192d"]

    Stage2 --> Merge2["Patch Merging<br/>2×2 → 1<br/>192d → 384d"]

    Merge2 --> Stage3["Stage 3<br/>18 × SwinBlock<br/>W-MSA → SW-MSA<br/>1,024 patches × 384d"]

    Stage3 --> Merge3["Patch Merging<br/>2×2 → 1<br/>384d → 768d"]

    Merge3 --> Stage4["Stage 4<br/>2 × SwinBlock<br/>W-MSA → SW-MSA<br/>256 patches × 768d"]

    subgraph SwinBlockDetail ["Swin Block Pair"]
        WMSA["W-MSA<br/>(Regular Windows)"] --> SWMSA["SW-MSA<br/>(Shifted Windows)"]
    end

    subgraph WindowDetail ["Window Attention"]
        WinReg["Regular: 7×7 windows<br/>aligned to (0,0)"]
        WinShift["Shifted: 7×7 windows<br/>aligned to (3,3)"]
    end

    style Input fill:#f4e8e8,stroke:#7d2d2d
    style Stage1 fill:#fff3cd,stroke:#856404
    style Stage2 fill:#fff3cd,stroke:#856404
    style Stage3 fill:#f8d7da,stroke:#721c24
    style Stage4 fill:#d1ecf1,stroke:#0c5460
    style PatchEmb fill:#d4edda,stroke:#155724
```

> **Key Takeaway**: The Swin Transformer's genius lies in combining local window attention (for efficiency) with shifted windows (for cross-window communication). The hierarchical 4-stage structure progressively trades spatial resolution for channel depth, reducing 16,384 patches to 256 while building increasingly abstract representations. Relative position bias within windows provides translation-equivariant spatial awareness, and patch merging enables clean spatial downsampling between stages.

---

## Supplementary Perspective — from TAMER 1

> **Original file:** `TAMER 1/Chapter 2/2.2 Swin Transformer V2.md`  
> **Role in master vault:** supplement perspective from TAMER 1 — T1 supplement appended to T2 Ch 4.2 canonical for Swin architecture topic.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

## 2.2 Swin Transformer V2

If a standard Vision Transformer is like an eye looking at a whole scene at once, a **Swin Transformer** (Shifted Window Transformer) is like an eye scanning a page line by line, but with the ability to see connections across windows.

###  Why "Swin"?
The name comes from **S**hifted **Win**dows. This architecture was designed specifically to bridge the gap between CNNs (which are efficient but "local") and Transformers (which are powerful but "global").

####  1. Hierarchical Architecture
Unlike a standard ViT, which processes images as a flat list of fixed-size patches, a Swin Transformer starts with small patches and gradually merges them into larger ones, just like a CNN's hierarchy (e.g., edges $\rightarrow$ shapes $\rightarrow$ objects).
*   **Layer 1:** Looks at $4 \times 4$ pixels.
*   **Layer 2:** Merges $2 \times 2$ adjacent patches into $8 \times 8$.
*   **Layer 3:** Further merges into $16 \times 16$.

**Why it matters for Math:** Math symbols vary wildly in size. A tiny subscript and a giant summation ($\sum$) or fraction bar need different "zoom levels". This hierarchical approach handles that perfectly.

####  2. Window-based Attention
Instead of calculating attention across the *entire* image (which takes $O(\text{Pixels}^2)$ complexity), Swin calculates attention only within small windows (e.g., $7 \times 7$ patches).
*   **Benefit:** It's incredibly fast and efficient. It can handle high-resolution images where a standard Transformer would run out of memory.

####  3. Shifted Windowing (The "Secret Sauce")
Calculating attention *only* inside windows means that a symbol on the edge of Window A couldn't "see" a symbol on the edge of Window B. To fix this, Swin **shifts** the window grid in alternating layers.

```mermaid
graph TD
    A[Layer L: Regular Windowing] --> B[Calculate Local Attention]
    B --> C[Layer L+1: Shift Windows by 1/2 size]
    C --> D[Calculate Cross-Window Attention]
    D --> E[Information flows across entire image]
```

This allows the model to understand that the "x" in Window 1 and the "^2" in Window 2 are part of the same expression $x^2$.

###  Improvements in V2 (The "Enhanced" part of your project)
You'll notice your code uses **Swin-V2**. Here are the two key technical differences that make it better for math:

1.  **Post-Normalization (Post-Norm):** In V1, the model normalized features *before* attention. In V2, it does it *after*. This makes training much more stable, especially when you have deep layers and small batches (like in Colab).
2.  **Log-spaced Relative Position Bias:** Math symbols are often far apart but logically linked. Swin-V2 incorporates a **Relative Positional Bias** matrix directly into the attention calculation:
    $$Attention(Q, K, V) = \text{SoftMax}\left(\frac{QK^T}{\sqrt{d}} + B\right)V$$
    Where $B$ is a learnable matrix representing the relative 2D distance between patch $i$ and patch $j$.

---
###  Reasoning: Why did we pick Swin-V2 for TAMER?
Standard OCR models use CNNs because they are fast. But in HMER, we need the "Global Reasoning" of a Transformer to know that a tiny dot 100 pixels away is actually the end of a long complex proof. **Swin-V2 gives us the speed of a CNN with the global "IQ" of a Transformer.**

> [!IMPORTANT]
> **Key Term: Patch Merging**. This is the process of concatenating $2 \times 2$ neighboring patches and reducing their dimensionality. It is the "Transformer equivalent" of a CNN's Pooling layer, but much more sophisticated.

> [!TIP]
> **Points Students Often Miss:** The "Shifted Window" is NOT the same as a "Sliding Window" in a CNN. A CNN slides across every pixel; Swin stays in its window for one layer and then shifts the *grid* for the next. This is what makes it computationally efficient ($O(N)$ vs $O(N^2)$).

---

## Supplementary Perspective — from TAMER 3

> **Original file:** `TAMER 3/04_Sequence_Generation_The_Voice/03_Section_2_Swin_Transformer_v2_Architecture.md`  
> **Role in master vault:** supplement perspective from TAMER 3 — T3 supplement appended to T2 Ch 4.2 canonical.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

### 2. Swin Transformer v2 Architecture

#### The Quadratic Complexity Problem

Standard ViT (Vision Transformer) applies global self-attention across all $N$ patches. For a 256×1024 image with 4×4 patches:

$$N = \frac{256}{4} \times \frac{1024}{4} = 64 \times 256 = 16{,}384 \text{ patches}$$

The attention matrix $Q K^T$ has shape $16{,}384 \times 16{,}384 = 268{,}435{,}456$ elements. At float32 (4 bytes each), this is ~1GB per head per layer. With 12 heads and 12 layers, this is 144GB just for attention matrices. Completely impossible on any GPU.

---

#### Swin's Window-Based Solution

Swin (Shifted Window) Transformer solves this by restricting attention to local windows. Instead of computing attention globally over all $N$ patches, it partitions the feature map into non-overlapping windows of fixed size $M \times M$ (e.g., $7 \times 7$) and computes attention independently within each window.

**Complexity reduction:**
- Global ViT: $O(N^2)$ = $O(16384^2) = O(268M)$
- Swin with $M=7$ windows: Each window has $M^2 = 49$ patches. Attention within window is $O(M^2) = O(2401)$. Total windows: $N / M^2 = 16384 / 49 = 334$ windows. Total complexity: $O(N \cdot M^2) = O(N)$. Linear in $N$.

This is an improvement of $N / M^2 = 16384 / 49 \approx 334\times$ in computational complexity.

---

#### The Shifted Window Mechanism

The problem with standard window attention: information cannot cross window boundaries. Two patches in adjacent windows never communicate.

The solution: alternate between two attention patterns.

**Layer 1: Regular Windows**
Windows are aligned to a fixed grid. Patches inside each window attend to each other.

**Layer 2: Shifted Windows**
Windows are shifted by $(\lfloor M/2 \rfloor, \lfloor M/2 \rfloor)$ positions. The new window boundaries cut across the old ones. Patches that were in different windows in Layer 1 are now in the same window in Layer 2, so they can finally communicate.

Over multiple layers, this alternating shift allows information to propagate globally despite local computation.

```mermaid
flowchart TD
    A["Input Image\n256 x 1024 pixels"] --> B["Patch Partition\n4x4 pixel patches\n64 x 256 = 16384 patches"]
    B --> C["Stage 1: Swin Block Layer 1\nRegular Window Attention\nWindow size: 7x7"]
    C --> D["Stage 1: Swin Block Layer 2\nShifted Window Attention\nShift: 3x3"]
    D --> E["Patch Merging\nMerge 2x2 patches\nResolution halved\nChannels doubled"]
    E --> F["Stage 2: Swin Blocks\n32 x 128 resolution\n192 channels"]
    F --> G["Patch Merging"]
    G --> H["Stage 3: Swin Blocks\n16 x 64 resolution\n384 channels"]
    H --> I["Patch Merging"]
    I --> J["Stage 4: Swin Blocks\n8 x 32 resolution\n768 channels"]
    J --> K["Output Feature Map\nB x 256 x 768\nFlattened to B x 256 x 768"]
```

---

#### v2-Specific Improvements Over Swin-v1

**Scaled Cosine Attention:**
Swin-v1 uses the standard dot-product attention where $Q K^T$ can produce very large or very small values. Swin-v2 uses cosine similarity instead:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{\cos(Q, K)}{\tau}\right) V$$

Where $\tau$ is a learnable temperature parameter per head. This makes attention more stable when fine-tuning at resolutions different from pre-training resolution (which is exactly TAMER's use case: pre-trained on ImageNet images, fine-tuned on math formula images).

**Log-Spaced Continuous Positional Bias:**
Swin-v2 uses a log-space relative position bias instead of the linear spacing in v1. This allows the model to smoothly extrapolate to larger resolution inputs without performance degradation. This is critical for TAMER because math formula images may span a much wider range of resolutions than the ImageNet pre-training images.

---
