---
tags: [clustering, hierarchical]
---

# Hierarchical Clustering

> **Definition.** Build a tree of clusters (dendrogram) by recursively merging or splitting.

## Types

- **Agglomerative** (bottom-up): start with each point as a cluster; merge closest pairs.
- **Divisive** (top-down): start with one cluster; split recursively.

## Linkage

- **Single**: minimum distance between clusters.
- **Complete**: maximum distance.
- **Average**: average distance.
- **Ward**: minimize variance.

## Strengths

- Produces a hierarchy (matches building hierarchy).
- No need to specify $k$ upfront (cut dendrogram at desired level).
- Deterministic.

## Limitations

- $O(n^3)$ or $O(n^2 \log n)$ time.
- Greedy merges cannot be undone.
- Sensitive to linkage choice.

## In Buildings

Hierarchical clustering naturally matches the building's hierarchical structure:

- Cluster elements → components → rooms → storeys.

This is the basis of [[Recursive Component Discovery]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[HDBSCAN]]
- [[Hierarchical Component Discovery]]
