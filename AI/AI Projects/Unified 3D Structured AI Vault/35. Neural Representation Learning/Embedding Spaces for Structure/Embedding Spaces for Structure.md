---
tags: [neural-rep, embedding]
---

# Embedding Spaces for Structure

> **Definition.** A learned vector space where similar structures are nearby and dissimilar structures are far.

## What to Embed

- **Elements**: walls, doors, windows → element embeddings.
- **Subtrees**: small tree fragments → subtree embeddings.
- **Subgraphs**: small graph patterns → subgraph embeddings.
- **Whole structures**: entire buildings → building embeddings.

## Why It Matters

- Embeddings enable similarity search (find similar structures).
- Embeddings enable clustering (group similar structures).
- Embeddings enable generation (sample in embedding space, decode).
- Embeddings enable transfer (pre-train on large data, fine-tune).

## Methods

- **Contrastive**: see [[Contrastive Learning for Structure]].
- **Auto-encoder**: encode structure, decode it.
- **VAE**: probabilistic version.
- **Tree/graph neural networks**: encode trees/graphs directly.

## In Buildings

- Embed elements → cluster to discover types.
- Embed subtrees → discover motifs.
- Embed buildings → find similar buildings for transfer.

See [[Contrastive Learning for Structure]], [[Self Supervised Structure Learning]].

## Related Concepts

- [[Contrastive Learning for Structure]]
- [[Self Supervised Structure Learning]]
- [[Embedding Based Clustering]]
