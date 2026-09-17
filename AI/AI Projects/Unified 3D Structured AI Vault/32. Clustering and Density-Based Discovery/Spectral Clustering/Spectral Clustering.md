---
tags: [clustering, spectral]
---

# Spectral Clustering

> **Definition.** Cluster points by analyzing the eigenvectors of a similarity graph's Laplacian.

## Algorithm

1. Build a similarity graph (e.g. k-NN graph with Gaussian similarity).
2. Compute the graph Laplacian $L = D - A$.
3. Compute the first $k$ eigenvectors of $L$.
4. Embed each point by its eigenvector values.
5. Cluster the embeddings (e.g. with K-Means).

## Strengths

- Finds non-convex clusters.
- Works on graph data (not just feature vectors).
- Theoretically grounded (graph cut minimization).

## Limitations

- $O(n^3)$ for eigendecomposition (approximations exist).
- Need to choose similarity / graph construction.
- Number of clusters $k$ must be specified.

## In Buildings

Spectral clustering on building scene graphs:

- Cluster rooms by adjacency (find zones).
- Cluster elements by relation patterns.

See [[Graph Community Detection]], [[Hierarchical Clustering]].

## Related Concepts

- [[Graph Community Detection]]
- [[Hierarchical Clustering]]
