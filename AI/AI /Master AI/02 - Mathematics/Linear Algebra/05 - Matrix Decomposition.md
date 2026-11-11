---
tags: [mathematics, linear-algebra, svd, pca, decomposition]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Matrix Decomposition, SVD, PCA]
---

# 05 - Matrix Decomposition (SVD, Eigendecomposition, PCA)

> [!info] TL;DR
> Matrix decomposition breaks a matrix into simpler building blocks. The most important is **SVD** (Singular Value Decomposition): every matrix factors as $U \Sigma V^T$. SVD powers PCA, LoRA's intuition, recommender systems, and many ML algorithms.

## Why Decompose?

Working with a matrix directly is hard. Working with simpler matrices that combine to form it is often much easier. Decompositions reveal structure: rank, principal directions, low-rank approximations.

Common decompositions:
- **Eigendecomposition**: $\mathbf{A} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^{-1}$ (square matrices with linearly independent eigenvectors).
- **SVD**: $\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$ (any matrix).
- **LU**: $\mathbf{A} = \mathbf{L}\mathbf{U}$ (lower × upper triangular).
- **QR**: $\mathbf{A} = \mathbf{Q}\mathbf{R}$ (orthogonal × upper triangular).
- **Cholesky**: $\mathbf{A} = \mathbf{L}\mathbf{L}^T$ (symmetric positive definite).

For ML, SVD and eigendecomposition are by far the most important.

## Eigendecomposition

For a square matrix $\mathbf{A} \in \mathbb{R}^{n \times n}$, an **eigenvalue** $\lambda$ and **eigenvector** $\mathbf{v}$ satisfy:

$$
\mathbf{A} \mathbf{v} = \lambda \mathbf{v}
$$

The eigenvector is a direction that $\mathbf{A}$ only stretches (by $\lambda$) without rotating.

If $\mathbf{A}$ has $n$ linearly independent eigenvectors, we can write:

$$
\mathbf{A} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^{-1}
$$

where $\mathbf{Q}$'s columns are eigenvectors and $\mathbf{\Lambda}$ is a diagonal matrix of eigenvalues.

### When does this exist?
- Always for symmetric matrices (and then $\mathbf{Q}$ is orthogonal: $\mathbf{Q}^{-1} = \mathbf{Q}^T$).
- For non-symmetric matrices, may not exist (or may have complex eigenvalues).

### Why it matters
- PCA is eigendecomposition of the covariance matrix.
- Spectral clustering uses eigendecomposition of the graph Laplacian.
- PageRank is the principal eigenvector of the link matrix.
- Matrix powers: $\mathbf{A}^k = \mathbf{Q} \mathbf{\Lambda}^k \mathbf{Q}^{-1}$ (just raise the diagonal).

## Singular Value Decomposition (SVD)

SVD works for **any** matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$:

$$
\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T
$$

where:
- $\mathbf{U} \in \mathbb{R}^{m \times m}$ — orthogonal matrix; columns are **left singular vectors**.
- $\mathbf{\Sigma} \in \mathbb{R}^{m \times n}$ — diagonal matrix of **singular values** $\sigma_1 \geq \sigma_2 \geq \ldots \geq 0$.
- $\mathbf{V} \in \mathbb{R}^{n \times n}$ — orthogonal matrix; columns are **right singular vectors**.

### Geometric interpretation

Any linear transformation $\mathbf{A}$ can be decomposed as:
1. Rotate ($\mathbf{V}^T$).
2. Scale along axes ($\mathbf{\Sigma}$).
3. Rotate again ($\mathbf{U}$).

So every linear map is "rotate, stretch, rotate." The singular values are the stretch factors.

### Relation to eigendecomposition

- $\mathbf{A}^T \mathbf{A}$ has eigenvectors = right singular vectors of $\mathbf{A}$, eigenvalues = $\sigma_i^2$.
- $\mathbf{A} \mathbf{A}^T$ has eigenvectors = left singular vectors of $\mathbf{A}$, eigenvalues = $\sigma_i^2$.

So SVD is essentially eigendecomposition of $\mathbf{A}^T \mathbf{A}$ and $\mathbf{A} \mathbf{A}^T$.

## Low-Rank Approximation: The Magic of SVD

The rank-$k$ approximation of $\mathbf{A}$ is:

$$
\mathbf{A}_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^T
$$

— keep only the top $k$ singular values.

**Eckart-Young theorem**: $\mathbf{A}_k$ is the best rank-$k$ approximation of $\mathbf{A}$ in Frobenius norm (and spectral norm). No other rank-$k$ matrix is closer to $\mathbf{A}$.

This is the foundation of:
- **PCA** (see below).
- **LoRA** — the assumption that fine-tuning updates are low-rank. See [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]].
- **Recommender systems** — user-item matrices are approximately low-rank.
- **Image compression** — discard small singular values.
- **Latent semantic analysis** — find topics in term-document matrices.

## Principal Component Analysis (PCA)

PCA finds the directions of maximum variance in data. Given centered data $\mathbf{X} \in \mathbb{R}^{n \times d}$:

1. Compute the covariance matrix $\mathbf{C} = \frac{1}{n-1} \mathbf{X}^T \mathbf{X}$.
2. Eigendecompose $\mathbf{C} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^T$.
3. The eigenvectors (principal components) are the directions of maximum variance; eigenvalues are the variances.
4. To reduce dimensionality, project onto the top $k$ eigenvectors.

Equivalently (and more numerically stable): SVD of $\mathbf{X} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$. The principal components are the columns of $\mathbf{V}$, and the variances are $\sigma_i^2 / (n-1)$.

### Why PCA works
The first principal component is the direction that captures the most variance. The second is the direction perpendicular to the first that captures the most remaining variance. And so on. Discarding low-variance components loses little information.

## Worked Example (PCA)

Suppose we have 2D data points roughly along the line $y = x$ with some noise. The covariance matrix might look like:

$$
\mathbf{C} = \begin{pmatrix} 2 & 1.8 \\ 1.8 & 2 \end{pmatrix}
$$

Eigenvalues: $\lambda_1 \approx 3.8$, $\lambda_2 \approx 0.2$. The first principal component (along $(1,1)/\sqrt{2}$) captures 95% of the variance; the second is mostly noise. Projecting to 1D keeps almost all the information.

## Implementation (NumPy)

```python
import numpy as np

# SVD
A = np.random.randn(5, 3)
U, S, Vt = np.linalg.svd(A, full_matrices=False)
# A ≈ U @ np.diag(S) @ Vt

# Rank-2 approximation
A_rank2 = U[:, :2] @ np.diag(S[:2]) @ Vt[:2, :]

# PCA
X = np.random.randn(100, 5)
X_centered = X - X.mean(axis=0)
U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
components = Vt  # principal components
explained_variance = (S ** 2) / (X.shape[0] - 1)
```

## Why This Matters for AI

- **LoRA is built on SVD intuition**. The pretrained weight matrix $\mathbf{W}$ is fixed; the fine-tune delta $\Delta \mathbf{W}$ is assumed to be approximately low-rank, so it's parameterized as $\mathbf{B}\mathbf{A}$ (rank $r$). See [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]].
- **PCA** is a baseline dimensionality reduction everywhere — embeddings, feature visualization, data preprocessing.
- **Recommender systems** — collaborative filtering is SVD on user-item matrices (with missing entries).
- **Quantization and compression** — low-rank approximations reduce model size.

## Production Implications

- SVD is **expensive** ($O(\min(mn^2, m^2n))$). For large matrices, use randomized SVD (`sklearn.utils.extmath.randomized_svd`).
- For very large sparse matrices (recommender systems), use alternating least squares or gradient descent instead of exact SVD.
- PCA before clustering or classification can dramatically speed up downstream algorithms — but loses interpretability.

## Common Pitfalls

- **Forgetting to center data before PCA** — without centering, the first PC is dominated by the mean.
- **Mixing up SVD and eigendecomposition** — SVD always exists; eigendecomposition may not.
- **Confusing singular values with eigenvalues** — they're related but different ($\sigma_i = \sqrt{\lambda_i}$ for $\mathbf{A}^T\mathbf{A}$).
- **Over-interpreting PCA** — PCs are directions of variance, not necessarily meaningful axes. They can capture noise as easily as signal.

## Further Reading

- Strang, *Introduction to Linear Algebra*, Chapter 7 (SVD).
- Goodfellow et al., *Deep Learning*, Section 2.12 (PCA).
- Eckart-Young theorem original paper (1936).

## The Eckart-Young Theorem (Proof Sketch)

The Eckart-Young theorem states that the rank-$k$ SVD truncation $\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$ is the best rank-$k$ approximation of $\mathbf{A}$ in both Frobenius and spectral norms.

### Frobenius norm proof (sketch)
The Frobenius norm of $\mathbf{A} - \mathbf{A}_k$ is:
$$
\|\mathbf{A} - \mathbf{A}_k\|_F^2 = \sum_{i=k+1}^r \sigma_i^2
$$

For any rank-$k$ matrix $\mathbf{B}$, we have $\|\mathbf{A} - \mathbf{B}\|_F^2 \ge \sum_{i=k+1}^r \sigma_i^2$ (by the Eckart-Young bound). Equality holds for $\mathbf{B} = \mathbf{A}_k$.

### Why this matters
- **LoRA's theoretical foundation**: the assumption that fine-tuning updates are low-rank is empirically justified — SVD of trained weight deltas shows rapid singular value decay.
- **PCA optimality**: PCA is the best linear dimensionality reduction (in terms of preserved variance) — no other $k$-dimensional projection preserves more variance.
- **Compression**: discard small singular values with minimal information loss — the foundation of image compression, latent semantic analysis, and model compression.

## SVD in Modern AI (Detailed)

### LoRA and low-rank adaptation
LoRA parameterizes weight updates as $\Delta \mathbf{W} = \mathbf{B}\mathbf{A}$ where $\mathbf{A} \in \mathbb{R}^{r \times d}$, $\mathbf{B} \in \mathbb{R}^{d \times r}$, $r \ll d$. This is a rank-$r$ matrix — equivalent to keeping only the top-$r$ singular values in the SVD of $\Delta \mathbf{W}$.

Empirical finding: trained $\Delta \mathbf{W}$ matrices have rapidly decaying singular values, so rank $r = 8$ to $64$ captures most of the update. This is why LoRA works — the "intrinsic rank" of fine-tuning updates is low, even for large models.

### Embedding dimensionality reduction
Pretrained embeddings (CLIP, BGE, GTE) are often 768-1536 dimensions. For retrieval at scale:
- Compute SVD of the embedding matrix.
- Keep top 256-512 dimensions (95%+ variance preserved).
- Index in the reduced space — 3-6× faster search, 3-6× less memory.

This is standard practice for production RAG systems with >10M documents.

### Quantization via low-rank compensation
When quantizing weights to INT4/INT8, the quantization error can be compensated by a low-rank correction:
- Quantize $\mathbf{W}$ to $\hat{\mathbf{W}}$.
- Compute error $\mathbf{E} = \mathbf{W} - \hat{\mathbf{W}}$.
- Approximate $\mathbf{E} \approx \mathbf{U}_r \mathbf{\Sigma}_r \mathbf{V}_r^T$ (rank-$r$ SVD).
- Store $\hat{\mathbf{W}}$ (INT4) + $\mathbf{U}_r, \mathbf{\Sigma}_r, \mathbf{V}_r$ (FP16).
- At inference: $\mathbf{W}\mathbf{x} \approx \hat{\mathbf{W}}\mathbf{x} + \mathbf{U}_r \mathbf{\Sigma}_r \mathbf{V}_r^T \mathbf{x}$.

This is the foundation of QALoRA, QLoRA's low-rank correction variant.

### Attention approximation
The attention matrix $\text{softmax}(QK^T / \sqrt{d_k})$ is approximately low-rank for long sequences (most attention weight is on a few tokens). This is exploited by:
- **Linformer**: project $K$ and $V$ to lower dimension via SVD-like projection.
- **Nyströmformer**: approximate attention via Nyström method (SVD-like).
- **Performer**: kernel approximation of softmax — conceptually related.

See [[06 - Attention Mechanisms/Efficient Attention/13 - Linear Attention|Linear Attention]].

## PCA in Production (Detailed)

### When to use PCA
- **Visualization**: project high-D embeddings to 2D/3D for inspection.
- **Preprocessing**: reduce dimensionality before clustering or classification.
- **Compression**: reduce embedding storage (3-6× compression with <5% recall loss).
- **Denoising**: discard low-variance components (often noise).
- **Multicollinearity**: PCA features are uncorrelated, useful for linear models.

### When NOT to use PCA
- **Interpretability required**: PCs are linear combinations of all features — hard to interpret.
- **Non-linear structure**: PCA is linear; t-SNE/UMAP better for non-linear manifolds.
- **Sparse data**: PCA dense-ifies sparse features; use NMF or sparse PCA instead.
- **Categorical data**: PCA assumes continuous features; one-hot encoding + PCA is suboptimal.

### Randomized SVD for large matrices
Exact SVD is $O(\min(mn^2, m^2n))$ — infeasible for $m, n > 10^4$. **Randomized SVD** approximates the top-$k$ singular vectors in $O(mnk)$ time:

```python
from sklearn.utils.extmath import randomized_svd

# Approximate top-50 SVD of a 1M x 10K matrix
U, S, Vt = randomized_svd(A, n_components=50, n_iter=5, random_state=42)
# A ≈ U @ np.diag(S) @ Vt, but only top-50 components
```

This is the standard for large-scale PCA, recommender systems, and LSA.

## Worked Example: PCA for Embedding Visualization

```python
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 10K embeddings, 768-dim each
embeddings = np.random.randn(10000, 768)  # replace with real embeddings
labels = np.random.randint(0, 10, 10000)  # 10 classes

# PCA to 2D for visualization
pca = PCA(n_components=2)
emb_2d = pca.fit_transform(embeddings)

print(f"Explained variance: {pca.explained_variance_ratio_.sum():.3f}")
# Typically 0.05-0.15 for 768→2 — most variance is in higher PCs

# For better visualization, use UMAP/t-SNE on PCA-reduced data
# (PCA to 50D first, then t-SNE to 2D — standard pipeline)
pca_50 = PCA(n_components=50).fit_transform(embeddings)
# Then apply t-SNE or UMAP to pca_50
```

The standard visualization pipeline: PCA to 50D (fast, denoising) → t-SNE/UMAP to 2D (non-linear, preserves local structure). Direct PCA to 2D loses too much variance.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| PCA first PC captures the mean | Forgot to center data | Always center before PCA (`X - X.mean(axis=0)`) |
| SVD doesn't converge | Matrix is ill-conditioned | Add regularization; use randomized SVD |
| Low-rank approximation poor | Singular values don't decay | Increase rank; matrix is genuinely high-rank |
| PCA components uninterpretable | Features have different scales | Standardize features (`StandardScaler`) before PCA |
| LoRA fine-tune doesn't converge | Rank too low for the task | Increase rank; check if task requires high-rank updates |
| Quantization + low-rank correction slow | Rank too high | Reduce rank; benchmark quality vs. speed tradeoff |

## Connection to Other Concepts

- [[02 - Mathematics/Linear Algebra/01 - Vectors|Vectors]] — the underlying objects.
- [[02 - Mathematics/Linear Algebra/04 - Matrix Multiplication|Matrix Multiplication]] — sum-of-outer-products view connects to SVD.
- [[02 - Mathematics/Calculus/11 - Jacobians and Hessians|Jacobians and Hessians]] — Hessian eigendecomposition.
- [[03 - Machine Learning/Unsupervised Learning/04 - Clustering and Dimensionality Reduction|Clustering and Dimensionality Reduction]] — PCA for clustering.
- [[04 - Neural Networks/Foundations/01 - Perceptrons and MLPs|Perceptrons and MLPs]] — low-rank weight matrices.
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — low-rank adaptation.
- [[12 - Fine-Tuning/PEFT/02 - QLoRA|QLoRA]] — quantization + low-rank.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — low-rank compensation.
- [[06 - Attention Mechanisms/Efficient Attention/13 - Linear Attention|Linear Attention]] — low-rank attention approximation.
- [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval|Embedding Models]] — PCA for embedding reduction.

## Interview Questions

1. **Q: What is SVD, and why is it more general than eigendecomposition?**
   A: SVD factors any matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$ as $\mathbf{U}\mathbf{\Sigma}\mathbf{V}^T$ where $\mathbf{U}, \mathbf{V}$ are orthogonal and $\mathbf{\Sigma}$ is diagonal with non-negative singular values. Eigendecomposition $\mathbf{A} = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1}$ only works for square matrices with linearly independent eigenvectors. SVD always exists, even for non-square or singular matrices. For symmetric PSD matrices, SVD = eigendecomposition.

2. **Q: State the Eckart-Young theorem and explain its significance.**
   A: The rank-$k$ SVD truncation $\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$ is the best rank-$k$ approximation of $\mathbf{A}$ in Frobenius and spectral norms. Significance: (1) justifies PCA as optimal linear dimensionality reduction, (2) justifies LoRA's low-rank assumption, (3) foundation of image compression and LSA, (4) gives a principled way to choose $k$ (look at singular value decay).

3. **Q: How does LoRA relate to SVD?**
   A: LoRA parameterizes weight updates as $\Delta \mathbf{W} = \mathbf{B}\mathbf{A}$ (rank $r$) — equivalent to keeping only the top-$r$ singular values in the SVD of $\Delta \mathbf{W}$. The empirical finding is that trained $\Delta \mathbf{W}$ matrices have rapidly decaying singular values, so $r = 8$ to $64$ captures most of the update. This is the theoretical foundation of LoRA — fine-tuning updates are intrinsically low-rank.

4. **Q: Why does PCA require centering the data?**
   A: Without centering, the first principal component is dominated by the mean of the data (the direction of largest variance includes the mean offset). Centering removes the mean, so PCA finds directions of variance around the mean — the actual structure. Forgetting to center is the most common PCA bug; the first PC will point in the direction of the mean, not the data structure.

5. **Q: When would you use randomized SVD instead of exact SVD?**
   A: For large matrices ($m, n > 10^4$), exact SVD is $O(\min(mn^2, m^2n))$ — infeasible. Randomized SVD approximates the top-$k$ singular vectors in $O(mnk)$ time, which is much faster when $k \ll \min(m, n)$. Use randomized SVD for: large-scale PCA, recommender systems, LSA on large corpora, and any application where you only need the top-$k$ components.

6. **Q: How can SVD compensate for quantization error?**
   A: Quantize $\mathbf{W}$ to $\hat{\mathbf{W}}$ (INT4/INT8), compute error $\mathbf{E} = \mathbf{W} - \hat{\mathbf{W}}$, approximate $\mathbf{E} \approx \mathbf{U}_r \mathbf{\Sigma}_r \mathbf{V}_r^T$ (rank-$r$ SVD). Store $\hat{\mathbf{W}}$ (INT4) + low-rank correction (FP16). At inference: $\mathbf{W}\mathbf{x} \approx \hat{\mathbf{W}}\mathbf{x} + \mathbf{U}_r \mathbf{\Sigma}_r \mathbf{V}_r^T \mathbf{x}$. This recovers most of the quantization quality loss with a small memory overhead. Foundation of QALoRA and similar methods.

## See Also

- [[01 - Vectors]]
- [[04 - Matrix Multiplication]]
- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — low-rank adaptation, SVD intuition
- [[02 - Mathematics/MOC|Mathematics MOC]]