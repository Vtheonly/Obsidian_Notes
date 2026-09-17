---
tags: [structured-generation, loss]
---

# Structured Loss

> **Definition.** A *structured loss* is a loss function that compares structured outputs (trees, graphs) rather than flat sequences.

## Why It Is Needed

Per-token cross-entropy treats each token independently. Two outputs can have identical tokens but different structures, or identical structures but different tokens.

## Examples

| Loss                          | Compares                                | Use case                          |
| ----------------------------- | --------------------------------------- | --------------------------------- |
| Tree edit distance            | Tree (number of edits to transform)     | AST, expression tree              |
| Graph edit distance           | Graph (number of edits)                 | Scene graph                       |
| Hamming on adjacency matrix   | Graph (per-edge difference)             | Scene graph                       |
| Chamfer distance              | Point sets                              | 3D shape                          |
| IoU                           | Voxel grids / bounding boxes            | 3D detection                      |
| Structured SVM margin         | Score gap to best wrong structure      | Generic structured prediction     |

## Tree Edit Distance

The **tree edit distance** between trees $T_1, T_2$ is the minimum number of node insertions, deletions, and relabels to transform $T_1$ into $T_2$.

Algorithm: Zhang-Shasha, $O(|T_1| \cdot |T_2| \cdot \min(\text{depth}_1, \text{leaves}_1) \cdot \min(\text{depth}_2, \text{leaves}_2))$.

## Soft vs Hard Structured Loss

- **Hard**: exact structured loss (e.g. exact tree edit distance). Expensive but precise.
- **Soft**: differentiable surrogate (e.g. per-node cross-entropy on tree-aligned positions). Cheaper but less faithful.

## Structured SVM

A structured SVM maximizes the margin between the correct structure $y$ and the best-scoring wrong structure $\hat y$:

$$\mathcal{L} = \max(0, 1 - s(x, y) + \max_{\hat y \neq y} [s(x, \hat y) + \Delta(\hat y, y)])$$

where $\Delta$ is the structured loss (e.g. tree edit distance). The inner max is the **loss-augmented decoding**.

## Related Concepts

- [[Structured Prediction]]
- [[Structural Scoring]]
- [[Constrained Decoding]]
