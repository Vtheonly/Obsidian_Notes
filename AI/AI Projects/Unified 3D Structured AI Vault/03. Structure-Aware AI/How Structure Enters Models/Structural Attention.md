---
tags: [structure-aware, attention]
---

# Structural Attention

> **Definition.** *Structural attention* modifies the standard self-attention to bias toward structurally related elements (e.g. parent, child, sibling, neighbor).

## Standard Attention

$$\text{Attn}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right) V$$

Every position attends to every other position with equal prior.

## Tree-Structured Attention

Add a bias $b_{ij}$ to the attention logits based on tree relationship:

$$\text{logit}_{ij} = \frac{q_i \cdot k_j}{\sqrt{d}} + b_{ij}$$

where $b_{ij}$ depends on the relationship between $i$ and $j$ in the tree:

- $b_{ij}$ large if $i$ is parent of $j$,
- $b_{ij}$ large if $i$ is sibling of $j$,
- $b_{ij}$ small otherwise.

Variants:

- **Hard mask**: set $b_{ij} = -\infty$ for unrelated pairs (effectively masking).
- **Soft bias**: $b_{ij}$ is a learned parameter per relationship type.
- **Distance-based**: $b_{ij}$ is a function of tree distance $d(i, j)$.

## Graph Attention

For graph-structured data, attention can be restricted to (or biased toward) graph neighbors. See [[Graph Attention]].

## Strength and Limitation

- **Strength**: lets the model focus on relevant structure; improves long-range coherence.
- **Limitation**: still a *statistical* preference; invalid structures can still occur.

See [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[How Structure Enters Models]]
- [[Structural Embeddings]]
- [[Graph Attention]]
- [[Tree Based Transformers]]
