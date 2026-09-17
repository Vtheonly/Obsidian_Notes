---
tags: [clustering, embedding]
---

# Embedding-Based Clustering

> **Definition.** Cluster points in a learned embedding space, not in the raw feature space.

## Pipeline

1. Train an embedding model (contrastive, auto-encoder, VAE).
2. Embed each data point.
3. Cluster embeddings (K-Means, HDBSCAN, etc.).

## Why It Works

- Embeddings capture semantic similarity (not just metric).
- Clusters in embedding space correspond to meaningful groups.
- Robust to noise in raw features.

## In Buildings

- Embed building elements by their context (neighbors, type, geometry).
- Cluster: windows that appear in similar contexts cluster together.
- Discover "types" of windows, doors, walls without manual labeling.

See [[Contrastive Learning for Structure]], [[Deep Clustering]].

## Related Concepts

- [[Deep Clustering]]
- [[Contrastive Learning for Structure]]
- [[Embedding Spaces for Structure]]
