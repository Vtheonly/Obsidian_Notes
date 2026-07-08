---
source_collections:
  - "TAMER 1"
  - "TAMER 3"
original_paths:
  - "TAMER 1/Chapter 2/2.4 2D Positional Encodings.md"
  - "TAMER 3/04_Sequence_Generation_The_Voice/04_Section_3_2D_Positional_Encoding_and_Spatial_Awareness.md"
roles_in_master:
  - "supplement"
  - "unique"
topic: "2d_pos_enc"
master_chapter: "50_Swin_Transformer_v2"
master_filename: "08_2D_Positional_Encodings.md"
n_source_files_merged: 2
merged: True
---

# 2.4 2D Positional Encodings

Transformers have no inherent concept of order or geometry. If you feed an image into a Transformer, it treats the pixels like a randomized "bag of features." In HMER, where the relative position of symbols (superscripts, fractions) is critical, we must explicitly inject spatial coordinates.

##  Why Positional Encoding is Required

Unlike a CNN, which implicitly learns spatial relationships through local filters, the **Self-Attention** mechanism in a Transformer treats every patch equally, regardless of distance. Position encoding "tags" each patch with its coordinate on the 2D plane.

##  2D Sinusoidal Encoding

For 1D text, we use sine and cosine waves of different frequencies. For 2D images, we split the embedding dimension (typically $d = 256$ or $512$) in half:

1.  **Y-axis (Height):** The first $D/2$ dimensions encode the vertical position using sine/cosine waves.
2.  **X-axis (Width):** The remaining $D/2$ dimensions encode the horizontal position using sine/cosine waves.

The final encoding is a concatenation of these two, ensuring the model inherently "knows" exactly where each patch originated on the 2D Cartesian plane.

### Implementation Logic
TAMER uses Sinusoidal Positional Encoding for both:
*   **Visual Features:** Tagging the 2D image patches.
*   **LaTeX Word Embeddings:** Tagging the 1D sequence of tokens.

 **Pro Tip:** In HMER, if your model correctly identifies all characters but places them in the wrong order (e.g., $2x$ instead of $x^2$), the issue is almost always a failure in **Positional Encoding**. The "vision" is working, but the "spatial logic" is broken.

---
> [!NOTE]
> **Why Sine/Cosine?** Using trigonometric functions allows the model to generalize to sequence lengths or image sizes it hasn't seen during training, as the relative distance between positions is encoded in the phase shift.

---

## Supplementary Perspective — from TAMER 3

> **Original file:** `TAMER 3/04_Sequence_Generation_The_Voice/04_Section_3_2D_Positional_Encoding_and_Spatial_Awareness.md`  
> **Role in master vault:** supplement perspective from TAMER 3 — T3 supplement appended to T1 2.4 canonical for 2D positional encoding topic.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

### 3. 2D Positional Encoding and Spatial Awareness

#### Why Transformers Need Positional Encoding

The self-attention operation is **permutation equivariant**: if you shuffle the order of input patches, the output patches are shuffled in the same way but otherwise unchanged. The attention weights between any two patches depend only on their content, not their positions. The model has no concept of "up" or "down" or "left" or "right".

This is appropriate for some tasks (e.g., set-membership queries) but catastrophically wrong for spatial tasks. The number `2` in the superscript position of $x^2$ means something completely different from the number `2` in the base position of $\log_2 x$.

Positional encoding injects spatial coordinate information into the feature vectors.

---

#### TAMER's Learned 2D Positional Encoding

TAMER uses separate 1D learned embeddings for rows and columns, then concatenates them to form a full 2D position embedding.

Let the output feature map have shape $R \times C$ (rows × columns of patches, e.g., 8 × 32).

**Row Embedding Table:** $E_R \in \mathbb{R}^{R_{max} \times D_r}$, where $R_{max}$ is the maximum number of rows (64), $D_r = D/2$.

**Column Embedding Table:** $E_C \in \mathbb{R}^{C_{max} \times D_c}$, where $C_{max}$ is the maximum number of columns (128), $D_c = D/2$.

For a patch at position $(r, c)$:

$$PE_{(r,c)} = [E_R[r] ; E_C[c]]$$

Where $[;]$ denotes concatenation. The result is a $D$-dimensional position embedding that encodes both the row and column position independently.

This is added to the Swin feature map:

$$X_{with\_pos} = X_{swin} + PE$$

The model learns the embeddings during training. It discovers that row embeddings for rows 0 and 1 should be similar (nearby rows are visually similar) and that row embeddings for rows 0 and 7 should be different. This structure emerges naturally from the gradient updates without any hand-engineering.

> **Important reminder:** The row and column embeddings are separate lookup tables, not a function of each other. This means the 2D position encoding is factored as $R + C$ parameters rather than $R \times C$ parameters. For a 64×128 grid with $D=768$, the factored approach uses $(64 + 128) \times 384 = 73{,}728$ parameters. The full grid approach would use $64 \times 128 \times 768 = 6{,}291{,}456$ parameters. The factored approach is 85 times smaller, more regularized, and generalizes better to image sizes not seen during training.

---
