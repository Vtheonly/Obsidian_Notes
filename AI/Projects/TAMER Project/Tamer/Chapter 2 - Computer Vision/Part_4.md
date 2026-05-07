# Chapter 2: Computer Vision and The Encoder

## 9. Encoder Architecture: SwinV2-Base and the Visual Projection Layer

Your encoder is not just a "backbone"; it is a hierarchical feature extractor designed to preserve the spatial density of mathematical ink.

**1. The Backbone:**
You utilize the `swinv2_base_window12_192` model. 
*   **Input Tensor:** $(B, 3, 384, 1280)$ — Batch size, RGB channels, Height, Width.
*   **Hierarchical Downsampling:** The Swin backbone passes the image through four stages. By the final stage (Stage 4), the image has been downsampled by a total factor of **32x**.
*   **Raw Output:** At your target resolution of $384 \times 1280$, the output is a grid of $12 \times 40$ feature patches.
*   **Feature Depth:** Each of these 480 patches has a vector depth of **1024**. This is the `in_channels` of your encoder.

**2. The Projection Layer:**
The Swin features (1024-dim) are too "heavy" for a standard transformer decoder. You implemented a Projection Layer:
*   **Component:** `nn.Linear(1024, 768)` followed by `nn.LayerNorm(768)`.
*   **Logic:** This projects the high-dimensional visual information into the "Latent Space" of the decoder ($d_{model}=768$). It acts as a semantic filter, discarding visual noise (like paper texture) and keeping mathematical features.

## 10. GPS Mechanics: 2D Row-Column Parameterization

This is the most critical custom part of your project. Instead of using a standard 1D sequence position, you built a **2D GPS system**.

**The Components:**
*   `self.row_embed`: A parameter of shape $(256, 384)$.
*   `self.col_embed`: A parameter of shape $(256, 384)$.
*(Wait: You chose $768$ as your $d_{model}$. These embeddings are each half of that, $384$, because they are concatenated.)*

**The Mathematical Logic:**
1.  **Selection:** The model slices the first 12 rows from `row_embed` and the first 40 columns from `col_embed`.
2.  **Expansion:** It "stretches" (repeats) the row embeddings horizontally and the column embeddings vertically.
3.  **Concatenation:** For every single patch in the $12 \times 40$ grid, it concatenates the specific Row-vector and Column-vector.
    *   *Resulting Dimension:* $384 \text{ (row)} + 384 \text{ (col)} = 768$.
4.  **Injection:** This $12 \times 40 \times 768$ grid is added directly to your projected visual features.

**Why this works:**
Because you added the position *before* flattening the grid into a sequence, every token now carries an immutable "address." Even if the decoder is processing a sequence of 480 tokens, it knows that token #41 is physically located at (Row 2, Column 1), placing it exactly underneath token #1 (Row 1, Column 1). This is how your model understands that a denominator is "below" a numerator.
