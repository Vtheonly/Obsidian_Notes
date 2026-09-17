---
tags: [clustering, deep]
---

# Deep Clustering

> **Definition.** Joint learning of embeddings and cluster assignments.

## Methods

- **DEC** (Deep Embedded Clustering): jointly refine embeddings and clusters.
- **IIC** (Invariant Information Clustering): maximize mutual information between cluster assignments of augmented views.
- **DeepCluster**: K-Means on embeddings, then use assignments as pseudo-labels to update the embedding network.

## Strengths

- Learns task-specific embeddings.
- Can outperform two-stage (embed then cluster).
- End-to-end trainable.

## Limitations

- Hard to train (unstable).
- Sensitive to initialization.
- Number of clusters may need to be specified.

## In Buildings

Deep clustering on building element embeddings:

- Discover element types without labels.
- Find recurring configurations.

See [[Embedding Based Clustering]], [[Contrastive Learning for Structure]].

## Related Concepts

- [[Embedding Based Clustering]]
- [[Contrastive Learning for Structure]]
