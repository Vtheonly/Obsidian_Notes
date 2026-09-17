---
tags: [neural-rep, self-supervised]
---

# Self-Supervised Structure Learning

> **Definition.** Learn structure-aware representations from unlabeled data by designing pretext tasks that require understanding structure.

## Pretext Tasks

- **Masked structure modeling**: mask a part of the structure, predict it.
- **Structure ordering**: shuffle parts, predict the correct order.
- **Contrastive**: contrast similar vs. dissimilar structures.
- **Reconstruction**: reconstruct the structure from a corrupted version.
- **Next-node prediction**: predict the next node in a tree (like BERT for trees).

## In Buildings

- Mask a wall's geometry, predict it from context.
- Shuffle rooms in a storey, predict the correct order.
- Contrast two views of the same building.
- Reconstruct a building from a partial BIM.

## Why It Works

- Forces the model to understand structure (not just appearance).
- Produces embeddings that capture structural similarity.
- Scales to large unlabeled datasets.

See [[Contrastive Learning for Structure]], [[Embedding Spaces for Structure]].

## Related Concepts

- [[Contrastive Learning for Structure]]
- [[Embedding Spaces for Structure]]
- [[Neural Representation Learning]]
