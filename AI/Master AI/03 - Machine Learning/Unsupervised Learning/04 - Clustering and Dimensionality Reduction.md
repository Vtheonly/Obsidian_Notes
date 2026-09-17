---
tags: [ml, unsupervised, clustering, dimensionality-reduction]
iteration: 2
created: 2026-08-07
aliases: [Clustering and Dimensionality Reduction]
---

# 04 - Clustering and Dimensionality Reduction

> [!info] TL;DR
> Unsupervised learning finds structure in unlabeled data. **Clustering** groups similar examples; **dimensionality reduction** projects high-dim data to a lower-dim space that preserves structure. Both are essential for exploration, visualization, and as preprocessing for downstream models.

## Clustering

### K-Means

The simplest and most-used clustering algorithm.

1. Pick $K$ random initial centroids.
2. Assign each point to the nearest centroid.
3. Recompute centroids as the mean of their assigned points.
4. Repeat until assignments stop changing.

**Objective**: minimize the sum of squared distances from points to their cluster centroids (inertia).

**Pros**: simple, fast ($O(NK)$ per iteration), scales well.
**Cons**: assumes spherical clusters of similar size; sensitive to initialization; need to choose $K$.

**Choosing K**: elbow method (find the "elbow" in inertia vs. K), silhouette score, or domain knowledge.

### DBSCAN

Density-based clustering: a cluster is a region of high density separated from other clusters by low-density regions.

- No need to choose $K$.
- Handles non-spherical clusters.
- Marks low-density points as noise (outliers).
- Sensitive to `eps` (neighborhood radius) and `min_samples` parameters.

### Hierarchical clustering

Builds a tree of clusters (dendrogram). Either agglomerative (bottom-up: merge closest clusters) or divisive (top-down: split).

- No need to choose $K$ upfront — cut the dendrogram at the desired level.
- Produces interpretable hierarchy.
- $O(N^2)$ or worse — doesn't scale to large datasets.

### When to use what

- **K-means**: large data, roughly spherical clusters, know K.
- **DBSCAN**: arbitrary cluster shapes, want outlier detection.
- **Hierarchical**: small data, want to understand cluster structure.

## Dimensionality Reduction

### PCA (Principal Component Analysis)

Linear projection to the directions of maximum variance. See [[02 - Mathematics/Linear Algebra/05 - Matrix Decomposition|Matrix Decomposition]] for the math.

- Fast, deterministic, no hyperparameters (except # components).
- Only captures linear structure.
- Good baseline and preprocessing step.

### t-SNE

Nonlinear reduction optimized for **visualization** (2D or 3D).

- Preserves local structure (nearby points stay nearby).
- Does NOT preserve global structure (cluster distances are meaningless).
- Slow on large data; use for visualization, not as model input.
- Stochastic — different runs give different plots.

### UMAP

Modern alternative to t-SNE:

- Faster than t-SNE.
- Better preserves global structure.
- Can be used as a preprocessing step (unlike t-SNE) because it generalizes to new points.
- Has meaningful hyperparameters (`n_neighbors`, `min_dist`).

### Autoencoders

Neural networks trained to reconstruct their input through a low-dimensional "bottleneck" layer. The bottleneck is the reduced representation.

- Can capture highly nonlinear structure.
- Trainable end-to-end with the rest of a model.
- Variants: VAE (variational, generative), denoising AE (robust), contractive AE (explicit regularization).

### When to use what

- **Visualization**: UMAP or t-SNE.
- **Preprocessing for downstream ML**: PCA or UMAP.
- **Nonlinear structure, end-to-end training**: autoencoders.
- **Generative modeling**: VAEs.

## Worked Example

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

# K-means
kmeans = KMeans(n_clusters=5).fit(X)
labels = kmeans.labels_

# PCA
X_pca = PCA(n_components=2).fit_transform(X)

# t-SNE (visualization)
X_tsne = TSNE(n_components=2, perplexity=30).fit_transform(X)

# UMAP
X_umap = umap.UMAP(n_components=2).fit_transform(X)
```

## Why This Matters for AI

- **Embedding visualization**: UMAP / t-SNE on text or image embeddings reveals clusters, outliers, structure. Essential for inspecting embedding models.
- **Vector DB indexing**: many ANN indexes (e.g., IVF) cluster vectors with k-means for fast retrieval.
- **Data exploration**: before training any model, cluster and visualize to understand the data.
- **Anomaly detection**: cluster outliers or low-density points flag anomalies.
- **Feature compression**: PCA / autoencoders reduce feature dim, speeding downstream training.

## Production Implications

- **Always visualize embeddings with UMAP** before deploying. If the visualization doesn't match your intuition about the data, something is wrong.
- **For real-time clustering**, use mini-batch k-means (sklearn `MiniBatchKMeans`).
- **PCA before K-means** can speed up clustering on high-dim data, but loses interpretability.
- **Anomaly detection with clustering**: compute distance to nearest cluster centroid; flag points with distance > threshold.

## Common Pitfalls

- **Using t-SNE distances for analysis** — they're meaningless. Use it only for visualization.
- **Not standardizing features before PCA** — features with large scale dominate.
- **Choosing K wrong** — elbow method is heuristic; check silhouette scores too.
- **Forgetting that clustering is unsupervised** — labels are arbitrary; cluster 0 isn't "better" than cluster 1.
- **UMAP hyperparameters matter** — `n_neighbors` and `min_dist` dramatically affect results; don't use defaults blindly.

## Further Reading

- Hastie et al., *ESL*, Chapter 14 (unsupervised learning).
- McInnes et al. (2018), *UMAP: Uniform Manifold Approximation and Projection*.
- van der Maaten & Hinton (2008), *Visualizing Data using t-SNE*.

## See Also

- [[02 - Mathematics/Linear Algebra/05 - Matrix Decomposition|Matrix Decomposition (PCA)]]
- [[01 - Bias Variance Tradeoff]]
- [[03 - Machine Learning/MOC|ML MOC]]
