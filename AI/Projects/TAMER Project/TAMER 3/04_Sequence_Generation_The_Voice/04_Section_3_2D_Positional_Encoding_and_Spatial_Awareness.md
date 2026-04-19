## 3. 2D Positional Encoding and Spatial Awareness

### Why Transformers Need Positional Encoding

The self-attention operation is **permutation equivariant**: if you shuffle the order of input patches, the output patches are shuffled in the same way but otherwise unchanged. The attention weights between any two patches depend only on their content, not their positions. The model has no concept of "up" or "down" or "left" or "right".

This is appropriate for some tasks (e.g., set-membership queries) but catastrophically wrong for spatial tasks. The number `2` in the superscript position of $x^2$ means something completely different from the number `2` in the base position of $\log_2 x$.

Positional encoding injects spatial coordinate information into the feature vectors.

---

### TAMER's Learned 2D Positional Encoding

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