---
tags: [clustering, dbscan]
---

# DBSCAN

> **Definition.** *Density-Based Spatial Clustering of Applications with Noise*. Clusters points by density: a cluster is a maximal set of density-connected points.

## Parameters

- $\epsilon$: neighborhood radius.
- $\text{minPts}$: minimum points to form a dense region.

## Algorithm

1. For each point $p$:
   - Find its $\epsilon$-neighborhood.
   - If the neighborhood has ≥ $\text{minPts}$ points, $p$ is a **core point**.
2. Expand clusters from core points: any point in the $\epsilon$-neighborhood of a core point is in the same cluster.
3. Points not in any cluster are **noise**.

## Strengths

- Does not require $k$.
- Finds clusters of arbitrary shape.
- Robust to outliers (labels them as noise).
- Finds clusters of varying shape.

## Limitations

- Sensitive to $\epsilon$ and $\text{minPts}$.
- Struggles with clusters of varying density.
- Distance metric matters (Euclidean assumes isotropic features).

## In Buildings

DBSCAN on point clouds:

- Cluster wall points (planar clusters).
- Cluster window openings (rectangular clusters).
- Detect outliers (noise = isolated points).

## Variants

- **HDBSCAN** (see [[HDBSCAN]]): handles varying density.
- **OPTICS** (see [[OPTICS]]): produces a cluster ordering.

## Related Concepts

- [[HDBSCAN]]
- [[OPTICS]]
- [[Hierarchical Clustering]]
