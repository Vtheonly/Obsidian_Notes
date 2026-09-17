---
tags: [exercise, clustering, dbscan, kmeans]
---

# Exercise — DBSCAN vs K-Means on Building Components

## Problem

You have 1000 building elements (walls, doors, windows, slabs) with features (size, position, type). You want to cluster them into "types".

(a) When would K-Means be appropriate?
(b) When would DBSCAN be appropriate?
(c) What are the trade-offs?

## Required Background

- K-Means: see [[K-Means]]. Requires $k$; assumes spherical clusters of similar size.
- DBSCAN: see [[DBSCAN]]. Does not require $k$; finds arbitrary shapes; labels noise.

## Correct Answers

### (a) When K-Means Is Appropriate

- You know the number of types in advance (e.g. 5 types: walls, doors, windows, slabs, columns).
- Clusters are expected to be roughly spherical in feature space.
- Clusters have similar sizes.
- No significant outliers.

### (b) When DBSCAN Is Appropriate

- You don't know the number of types.
- Clusters may have arbitrary shapes (e.g. a "window" type may be a long thin cluster).
- There are outliers (rare elements) that should be labeled as noise.
- Clusters have varying densities.

### (c) Trade-offs

| Aspect             | K-Means                | DBSCAN                       |
| ------------------ | ---------------------- | ---------------------------- |
| Number of clusters | Must specify $k$.      | Determined automatically.    |
| Cluster shape      | Spherical.             | Arbitrary.                   |
| Outliers           | Assigned to a cluster. | Labeled as noise.            |
| Density variation  | Struggles.             | Handles (with HDBSCAN).      |
| Speed              | Fast.                  | Medium.                      |
| Determinism        | Sensitive to init.     | Deterministic.               |
| Parameters         | $k$.                   | $\epsilon$, $\text{minPts}$.|

## Common Mistakes

- Using K-Means without checking cluster shapes (may produce meaningless clusters).
- Using DBSCAN with bad $\epsilon$ (too small → all noise; too large → one big cluster).
- Forgetting to normalize features (DBSCAN is distance-based).

## Edge Cases

- For high-dimensional features, both K-Means and DBSCAN struggle (curse of dimensionality). Use [[Embedding Based Clustering]] instead.
- For varying density, use [[HDBSCAN]].

## Implementation Considerations

```python
from sklearn.cluster import KMeans, DBSCAN

# K-Means
km = KMeans(n_clusters=5).fit(features)

# DBSCAN
db = DBSCAN(eps=0.5, min_samples=5).fit(features)
```

Always normalize features first:

```python
from sklearn.preprocessing import StandardScaler
features = StandardScaler().fit_transform(features)
```

## Related Concepts

- [[K-Means]]
- [[DBSCAN]]
- [[HDBSCAN]]
- [[Embedding Based Clustering]]
- [[Frequency vs Meaning]]
