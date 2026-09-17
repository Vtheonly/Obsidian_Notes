---
tags: [clustering, kmeans]
---

# K-Means

> **Definition.** K-Means partitions $n$ points into $k$ clusters by minimizing within-cluster variance.

## Algorithm

1. Initialize $k$ centroids (random, k-means++, etc.).
2. Assign each point to its nearest centroid.
3. Update each centroid as the mean of its assigned points.
4. Repeat 2-3 until convergence.

## Objective

$$\min_{\{C_i\}} \sum_{i=1}^k \sum_{x \in C_i} \|x - \mu_i\|^2$$

where $\mu_i$ is the centroid of cluster $C_i$.

## Strengths

- Simple, fast.
- Works well for convex clusters.
- Scales to large datasets.

## Limitations

- Must choose $k$.
- Assumes spherical clusters of similar size.
- Sensitive to outliers.
- Cannot find non-convex clusters.
- Cannot find clusters of varying density.

## In Buildings

K-Means on object features (size, position, type):

- Cluster walls by size.
- Cluster rooms by area.
- Cluster windows by dimensions.

But: K-Means finds **visually similar** objects, not **structurally meaningful** components. See [[Frequency vs Meaning]].

## Related Concepts

- [[DBSCAN]]
- [[HDBSCAN]]
- [[Hierarchical Clustering]]
- [[Frequency vs Meaning]]
