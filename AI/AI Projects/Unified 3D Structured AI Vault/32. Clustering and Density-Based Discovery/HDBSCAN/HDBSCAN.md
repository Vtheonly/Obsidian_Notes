---
tags: [clustering, hdbscan]
---

# HDBSCAN

> **Definition.** *Hierarchical DBSCAN*. Extends DBSCAN to handle clusters of varying density.

## Algorithm

1. Compute the mutual reachability distance between all pairs of points.
2. Build a minimum spanning tree (MST) of the mutual reachability graph.
3. Build a cluster hierarchy by removing MST edges in decreasing order of weight.
4. Condense the hierarchy (prune unstable branches).
5. Extract stable clusters.

## Strengths

- Does not require $k$.
- Handles varying density.
- Robust to noise.
- Produces a hierarchy (can choose granularity).
- Only one parameter (`min_cluster_size`).

## Limitations

- More complex than DBSCAN.
- Slower than K-Means.
- Sensitive to `min_cluster_size`.

## In Buildings

HDBSCAN on point clouds:

- Find clusters of varying density (sparse outdoor, dense indoor).
- Discover natural groupings without pre-specifying count.

See [[DBSCAN]], [[Hierarchical Clustering]].

## Related Concepts

- [[DBSCAN]]
- [[OPTICS]]
- [[Hierarchical Clustering]]
