---
tags: [mathematics, linear-algebra, similarity]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Cosine Similarity]
---

# Cosine Similarity

> [!info] TL;DR
> Cosine similarity is the dot product of two normalized vectors. It measures the **angle** between them — independent of their magnitudes. It's the default similarity metric for comparing embeddings.

## Definition

For two non-zero vectors $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n$:

$$
\text{cos}(\mathbf{x}, \mathbf{y}) = \frac{\mathbf{x} \cdot \mathbf{y}}{\|\mathbf{x}\| \, \|\mathbf{y}\|} = \cos\theta
$$

where $\theta$ is the angle between the two vectors.

The value is in $[-1, 1]$:

- $+1$ — vectors point in the same direction (maximally similar).
- $0$ — vectors are orthogonal (independent).
- $-1$ — vectors point in opposite directions (maximally dissimilar).

In PyTorch:

```python
import torch.nn.functional as F
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])
F.cosine_similarity(x.unsqueeze(0), y.unsqueeze(0))  # tensor([0.9746])
```

## Intuition

Imagine two vectors as arrows from the origin. The cosine of the angle between them tells you how much they "agree" in direction. Magnitude doesn't matter — only direction.

This is **crucial** for embeddings because the magnitude of an embedding often carries no semantic meaning (it's a side effect of training dynamics or input length), while the **direction** carries semantic content.

## Why Not Just Dot Product?

The raw dot product $\mathbf{x} \cdot \mathbf{y}$ depends on both direction and magnitude:

$$
\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \, \|\mathbf{y}\| \cos\theta
$$

So two short vectors pointing in the same direction can have a smaller dot product than two long vectors pointing in opposite directions. That's usually not what you want for similarity.

**Cosine similarity = dot product with magnitude factored out.**

## Relation to Euclidean Distance

If $\mathbf{x}$ and $\mathbf{y}$ are **unit-normalized** (i.e., $\|\mathbf{x}\| = \|\mathbf{y}\| = 1$), then:

$$
\|\mathbf{x} - \mathbf{y}\|^2 = 2 - 2 \cos\theta
$$

So **cosine similarity and Euclidean distance are equivalent for normalized vectors** — they're related by a monotonic transformation. Many vector databases internally use L2 distance even when the user-facing metric is cosine similarity, because the underlying ANN (Approximate Nearest Neighbor) index supports L2 natively.

## Use in AI

### 1. Embedding-based retrieval (RAG)

The canonical use: compare a query embedding against document embeddings, return the top-k most similar. This is the **retrieval step** of every RAG system. See [[17 - RAG/Retrieval|Retrieval]].

```python
# Compute cosine similarity between a query and all documents
sims = F.cosine_similarity(query_emb.unsqueeze(0), doc_embs)
top_k = sims.topk(k=5)
```

### 2. Embedding training (contrastive loss)

Contrastive learning (e.g., [[Word2Vec GloVe FastText|Word2Vec]], CLIP, sentence embeddings) pushes positive pairs toward cosine similarity 1 and negative pairs toward 0 (or below). See [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Embeddings]].

### 3. Clustering

Cosine similarity is often used as the affinity measure in clustering algorithms when the data is directional (e.g., text embeddings).

### 4. Monitoring embedding drift

Track the average cosine similarity between current production embeddings and a baseline. A drift indicates the input distribution has shifted.

## Worked Example

Let $\mathbf{x} = (1, 0)$ and $\mathbf{y} = (1, 1)$.

$$
\mathbf{x} \cdot \mathbf{y} = 1, \quad \|\mathbf{x}\| = 1, \quad \|\mathbf{y}\| = \sqrt{2}
$$

$$
\cos\theta = \frac{1}{1 \cdot \sqrt{2}} \approx 0.707 \quad\Rightarrow\quad \theta = 45°
$$

## When Not to Use Cosine Similarity

- **When magnitude carries information.** For example, image feature vectors where the magnitude encodes confidence. Use raw dot product or L2.
- **When the data is not naturally directional.** For low-dimensional numeric features (e.g., age, income), Euclidean distance with appropriate scaling is often more appropriate.
- **When you need a true metric.** Cosine similarity is not a distance metric (it doesn't satisfy the triangle inequality). For a metric, use **angular distance**:

$$
d(\mathbf{x}, \mathbf{y}) = \frac{\cos^{-1}(\cos\theta)}{\pi}
$$

## Variants

- **Dot product (no normalization)** — when magnitude matters.
- **Pearson correlation** — cosine similarity after mean-centering both vectors. Used when you care about co-variation, not co-direction.
- **Soft cosine similarity** — incorporates a feature-similarity matrix; useful when features themselves have semantic relationships.

## Production Implications

- **Pre-normalize embeddings at ingestion time.** Most vector databases support cosine similarity natively, but if you normalize vectors before inserting them, you can use L2 distance (often faster) and get the same ranking.
- **Quantization impact:** INT8 quantization degrades cosine similarity slightly. For high-precision retrieval, use FP16 or mixed precision.
- **Approximate Nearest Neighbor (ANN) indexes** (HNSW, IVF, ScaNN) trade a small amount of recall for huge speedups. Cosine similarity is well-supported by all major ANN libraries.

## Common Pitfalls

- **Forgetting to normalize** — if you compute the raw dot product and call it "cosine similarity", you'll get wrong answers when vectors have different magnitudes.
- **Comparing embeddings from different models** — embeddings from model A and model B live in different spaces; their cosine similarities are meaningless even if dimensions match.
- **Treating cosine similarity as a probability** — it's a similarity in $[-1, 1]$, not a probability in $[0, 1]$. If you need a probability, apply a softmax over similarities.

## Further Reading

- Manning, Raghavan, Schütze, *Introduction to Information Retrieval* — Chapter 6.
- For ANN indexes, see [[17 - RAG/Retrieval|Retrieval]] (planned).

## Mathematical Properties (Detailed)

### Range and bounds

Cosine similarity is bounded: $\cos\theta \in [-1, 1]$. The bound $+1$ is achieved iff $\mathbf{x} = c \mathbf{y}$ for some $c > 0$ (vectors point in the same direction). The bound $-1$ is achieved iff $\mathbf{x} = c \mathbf{y}$ for some $c < 0$ (opposite direction). Zero means orthogonal: $\mathbf{x} \cdot \mathbf{y} = 0$.

For non-negative vectors (e.g., bag-of-words, TF-IDF), $\cos\theta \in [0, 1]$ because the dot product is non-negative. This is why cosine similarity is so natural for text retrieval — it gives a clean $[0, 1]$ similarity without any transformation.

### Not a metric (but related to one)

Cosine similarity is **not a distance metric** — it doesn't satisfy the triangle inequality. To get a true metric, use **angular distance**:

$$
d_{\text{ang}}(\mathbf{x}, \mathbf{y}) = \frac{\cos^{-1}(\cos\theta)}{\pi} \in [0, 1]
$$

This satisfies all metric axioms (non-negativity, identity, symmetry, triangle inequality). Some ANN libraries (FAISS, ScaNN) use angular distance internally even when the user-facing metric is cosine similarity.

An equivalent metric on normalized vectors is the **Euclidean distance**:

$$
\|\hat{\mathbf{x}} - \hat{\mathbf{y}}\|_2 = \sqrt{2 - 2\cos\theta} \in [0, 2]
$$

where $\hat{\mathbf{x}} = \mathbf{x}/\|\mathbf{x}\|$. This is why vector databases can implement cosine similarity via L2 distance on normalized vectors — the rankings are identical.

### Relation to Pearson correlation

Pearson correlation is cosine similarity **after mean-centering** both vectors:

$$
\rho(\mathbf{x}, \mathbf{y}) = \cos(\mathbf{x} - \bar{\mathbf{x}}, \mathbf{y} - \bar{\mathbf{y}})
$$

where $\bar{\mathbf{x}}$ is the mean of $\mathbf{x}$'s components. Pearson removes the mean (DC component) before measuring alignment; cosine doesn't. Use Pearson when you care about co-variation (e.g., two stocks moving together); use cosine when you care about co-direction (e.g., two embeddings pointing to the same concept).

### Behavior in high dimensions

In high-dimensional spaces ($d \gg 100$), random vectors tend to be nearly orthogonal — $\cos\theta \approx 0$ for random $\mathbf{x}, \mathbf{y} \in \mathbb{R}^d$. This is the **curse of dimensionality** for similarity search: the contrast between "similar" and "dissimilar" shrinks as dimension grows.

Mitigations:
- **Reduce dimension** before similarity search (PCA,UMAP, or learned projections).
- **Use dot product** instead — if embeddings are trained with dot-product loss, magnitude carries signal.
- **Use approximate methods** (HNSW, IVF) that exploit local structure even in high-D.
- **Whiten the embeddings** — decorrelate and normalize dimensions so each contributes equally.

## Why Cosine Similarity for Embeddings (Deep Justification)

Embedding models (CLIP, BGE, GTE, sentence-transformers) are typically trained with **contrastive losses** that use cosine similarity or dot product as the similarity function. The choice is not arbitrary:

1. **Magnitude is meaningless for embeddings.** The training process doesn't constrain the norm of the output vector — two embeddings of the same concept can have different norms depending on input length, tokenization, or training noise. Normalizing removes this nuisance.

2. **Cosine is invariant to scale.** If the embedding model is retrained with a different output scale, cosine similarities are preserved — dot product similarities are not. This makes cosine more robust to model version changes.

3. **Cosine matches the training objective.** Most embedding losses (InfoNCE, triplet) normalize embeddings before computing similarity. Retrieval should use the same similarity function the model was trained with.

4. **Cosine is bounded.** $[-1, 1]$ (or $[0, 1]$ for non-negative) gives interpretable thresholds: "similarity > 0.8 means very similar." Dot product has no natural threshold.

5. **Cosine is the standard.** Every vector database, embedding benchmark, and retrieval evaluation uses cosine. Using anything else creates friction.

**Exception**: some models (e.g., OpenAI's `text-embedding-3-large`) are trained with dot product and recommend NOT normalizing. Always check the model card.

## Worked Example: Building a Semantic Search System

```python
import torch
import torch.nn.functional as F
import numpy as np
from typing import List, Dict

class SemanticSearch:
    def __init__(self, embedding_model, dim: int):
        self.model = embedding_model
        self.dim = dim
        self.embeddings: np.ndarray = None  # (N, dim), normalized
        self.documents: List[Dict] = []

    def _embed_and_normalize(self, texts: List[str]) -> np.ndarray:
        """Embed texts and L2-normalize for cosine similarity."""
        with torch.no_grad():
            embs = self.model.encode(texts)  # (N, dim)
        embs = F.normalize(torch.from_numpy(embs), dim=-1).numpy()
        return embs

    def add_documents(self, texts: List[str], metadata: List[Dict]):
        new_embs = self._embed_and_normalize(texts)
        if self.embeddings is None:
            self.embeddings = new_embs
        else:
            self.embeddings = np.vstack([self.embeddings, new_embs])
        self.documents.extend(metadata)

    def search(self, query: str, k: int = 5) -> List[Dict]:
        query_emb = self._embed_and_normalize([query])[0]  # (dim,)
        # Cosine similarity = dot product of normalized vectors
        sims = self.embeddings @ query_emb  # (N,)
        top_k_idx = np.argpartition(-sims, k)[:k]
        top_k_idx = top_k_idx[np.argsort(-sims[top_k_idx])]
        return [
            {"document": self.documents[i], "score": float(sims[i])}
            for i in top_k_idx
        ]

# Production notes:
# - For >100K documents, use FAISS/Annoy/HNSW instead of numpy matmul.
# - For real-time updates, use HNSW (supports incremental insertion).
# - For multi-tenant, partition the index per tenant.
# - Cache query embeddings — same query repeated is common.
```

Key implementation details:
- **Normalize at ingestion**, not at query time — saves a normalization per query.
- **Use dot product on normalized vectors** instead of `F.cosine_similarity` — faster (single matmul vs. pairwise).
- **`np.argpartition` for top-k** — $O(N)$ instead of $O(N \log N)$ for full sort.

## Comparison of Similarity Metrics

| Metric                 | Formula                                    | Range      | When to Use                                  |
|------------------------|--------------------------------------------|------------|----------------------------------------------|
| Cosine similarity      | $\frac{\mathbf{x} \cdot \mathbf{y}}{\|\mathbf{x}\|\|\mathbf{y}\|}$ | $[-1, 1]$ | Embeddings (default)                         |
| Dot product            | $\mathbf{x} \cdot \mathbf{y}$              | $(-\infty, \infty)$ | When magnitude matters (some models)        |
| Euclidean (L2)         | $\|\mathbf{x} - \mathbf{y}\|_2$            | $[0, \infty)$ | Spatial data, normalized embeddings (equivalent to cosine) |
| Manhattan (L1)         | $\sum_i |x_i - y_i|$                       | $[0, \infty)$ | Sparse data, robust to outliers             |
| Pearson correlation    | cosine of mean-centered vectors            | $[-1, 1]$  | Co-variation (not co-direction)              |
| Jaccard                | $\frac{|A \cap B|}{|A \cup B|}$            | $[0, 1]$   | Sets (e.g., token overlap)                   |
| Angular distance       | $\frac{\cos^{-1}(\cos\theta)}{\pi}$        | $[0, 1]$   | True metric (triangle inequality)            |
| Hyperbolic (Poincaré)  | distance in hyperbolic space               | $[0, \infty)$ | Hierarchical data (taxonomies, ontologies)  |

## Common Failure Modes in Production

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| All similarities cluster near 0.9+ | Curse of dimensionality; embeddings not discriminative | Reduce dim (PCA), retrain with harder negatives |
| Same query gets different results over time | Embedding model version changed | Pin model version; re-embed all docs on model change |
| Similarity scores don't match human judgment | Embedding model trained on different distribution | Fine-tune on domain data; try different model |
| Top-k results all semantically identical | Lack of diversity; embeddings too clustered | Use MMR (Maximal Marginal Relevance) for diversification |
| Cosine sim > 1.0 (numerical error) | Floating point precision after normalization | Clip to [-1, 1] before arccos; use float32 not float16 |
| ANN recall lower than expected | Index parameters too aggressive | Tune `ef_search` (HNSW) or `nprobe` (IVF); benchmark recall |
| Cross-model similarity is meaningless | Different embedding spaces | Never compare embeddings from different models |

## Connection to Other Concepts

- [[02 - Mathematics/Linear Algebra/01 - Vectors|Vectors]] — the underlying objects.
- [[02 - Mathematics/Linear Algebra/02 - Dot Product|Dot Product]] — the numerator; raw (un-normalized) similarity.
- [[02 - Mathematics/Linear Algebra/04 - Matrix Multiplication|Matrix Multiplication]] — batched similarity computation.
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy/Cross-Entropy/KL]] — alternative (probabilistic) similarity measures.
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Word2Vec/GloVe/FastText]] — trained with cosine-based contrastive losses.
- [[05 - NLP Fundamentals/Embeddings/06 - Contextual Embeddings ELMo to BERT|Contextual Embeddings]] — modern embedding models.
- [[17 - RAG/Ingestion and Retrieval/01 - RAG Pipeline Overview|RAG Pipeline]] — cosine similarity is the retrieval step.
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking/Hybrid/Reranking]] — production retrieval patterns.
- [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval|Embedding Models for Retrieval]] — models designed for cosine similarity.
- [[14 - Interpretability/Probing/05 - Probing|Probing]] — cosine similarity used to compare learned directions.

## Interview Questions

1. **Q: Why is cosine similarity preferred over dot product for embedding retrieval?**
   A: Four reasons. (1) Magnitude is meaningless for embeddings — it's a side effect of training dynamics, not semantics. (2) Cosine is scale-invariant, so retraining with a different output scale preserves similarities. (3) Cosine matches the training objective (most embedding losses normalize before computing similarity). (4) Cosine is bounded $[-1, 1]$, giving interpretable thresholds. Exception: some models (OpenAI text-embedding-3) are trained with dot product and recommend NOT normalizing.

2. **Q: How can you implement cosine similarity using L2 distance?**
   A: L2-normalize both vectors first, then L2 distance is $\|\hat{\mathbf{x}} - \hat{\mathbf{y}}\|_2 = \sqrt{2 - 2\cos\theta}$. The ranking by L2 distance on normalized vectors is identical to the ranking by cosine similarity. This is why vector databases (FAISS, pgvector) can implement cosine similarity via L2 distance — they normalize at ingestion and use L2 internally (often faster due to hardware optimization).

3. **Q: Why does cosine similarity fail in very high dimensions?**
   A: The "curse of dimensionality": random vectors in $\mathbb{R}^d$ for $d \gg 100$ tend to be nearly orthogonal ($\cos\theta \approx 0$). The contrast between "similar" and "dissimilar" shrinks — all similarities cluster near 0. Mitigations: reduce dimension (PCA, UMAP), use dot product if magnitude carries signal, use approximate methods (HNSW) that exploit local structure, or whiten the embeddings.

4. **Q: What's the difference between cosine similarity and Pearson correlation?**
   A: Pearson correlation is cosine similarity after mean-centering both vectors: $\rho(\mathbf{x}, \mathbf{y}) = \cos(\mathbf{x} - \bar{\mathbf{x}}, \mathbf{y} - \bar{\mathbf{y}})$. Pearson removes the DC component before measuring alignment. Use Pearson when you care about co-variation (e.g., two stocks moving together regardless of mean return); use cosine when you care about co-direction (e.g., two embeddings pointing to the same concept).

5. **Q: You observe cosine similarities all clustering near 0.95 in your retrieval system. What's wrong?**
   A: Likely the curse of dimensionality — embeddings are too high-dimensional and not discriminative enough. Fixes: (1) reduce dimension via PCA or a learned projection, (2) retrain the embedding model with harder negatives to increase contrast, (3) check if the embedding model is appropriate for your domain, (4) use MMR for diversification to break up the cluster. Also verify the embeddings are actually normalized — un-normalized embeddings can produce misleading similarity scores.

6. **Q: Is cosine similarity a distance metric?**
   A: No. It doesn't satisfy the triangle inequality: $\cos(\mathbf{x}, \mathbf{z})$ can be less than $\cos(\mathbf{x}, \mathbf{y}) + \cos(\mathbf{y}, \mathbf{z})$ even when $\mathbf{z}$ is "between" $\mathbf{x}$ and $\mathbf{y}$. For a true metric, use angular distance $d = \cos^{-1}(\cos\theta)/\pi \in [0, 1]$, which satisfies all metric axioms. Most ANN libraries use angular or L2 distance internally even when the user-facing metric is cosine similarity.

## See Also

- [[Vectors]]
- [[Dot Product]]
- [[Matrix Multiplication]]
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Embeddings]] (planned)
- [[17 - RAG/MOC|RAG MOC]]