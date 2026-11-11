---
tags: [mathematics, linear-algebra, vectors]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Vectors, Vector, Vector Spaces]
---

# Vectors

> [!info] TL;DR
> A vector is an ordered list of numbers. Vectors represent points, directions, features, embeddings, gradients — almost every object in AI is ultimately a vector or a collection of vectors. This note covers the formal definition, geometric and algebraic interpretations, the full operation set, vector spaces, norms, the role of vectors across the AI stack, common implementation pitfalls, and production considerations for vector-heavy systems.

## Definition

A vector $\mathbf{x} \in \mathbb{R}^n$ is an ordered tuple of $n$ real numbers:

$$
\mathbf{x} = (x_1, x_2, \ldots, x_n)
$$

The number $n$ is the **dimension** (or **dimensionality**) of the vector. The set of all $n$-dimensional real vectors is the vector space $\mathbb{R}^n$. Each $x_i$ is called a **component** or **element** of the vector.

More generally, vectors can live in any vector space over any field — complex numbers $\mathbb{C}^n$, finite fields, function spaces. In deep learning we almost always work with real vectors $\mathbb{R}^n$, occasionally complex vectors $\mathbb{C}^n$ (e.g., in signal processing and some RoPE formulations).

In PyTorch / NumPy:

```python
import torch
x = torch.tensor([1.0, 2.0, 3.0])  # a 3-d vector
print(x.shape)  # torch.Size([3])
print(x.dtype)  # torch.float32
print(x.dim())  # 1 (a 1-D tensor)
```

A batch of vectors is a 2-D tensor of shape `(batch_size, dim)`:

```python
batch = torch.randn(32, 768)  # 32 vectors, each 768-d
print(batch.shape)  # torch.Size([32, 768])
```

## Intuition

A vector can represent several conceptually different things, and AI uses all of them:

1. **A point in space** — e.g., the coordinates of an item in a feature space.
2. **A direction** — e.g., the direction of steepest ascent (a gradient).
3. **A feature vector** — the embedding of a token, image, or document.
4. **A probability distribution** — a non-negative vector that sums to 1 (output of softmax).
5. **A weights vector** — the parameters of a linear classifier.
6. **A difference / displacement** — e.g., the residual `f(x) - x` in a ResNet block.
7. **A normal vector** — perpendicular to a hyperplane; used in SVMs and normalization.

These roles are interchangeable: a feature vector is a point in feature space; a gradient is a direction in parameter space; a softmax output is a point on the probability simplex. The same mathematical object serves different conceptual roles depending on context.

### The Column vs. Row Convention

In mathematics, vectors are typically column vectors by default:

$$
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix} \in \mathbb{R}^{n \times 1}
$$

In code, a 1-D tensor has no orientation — it's just a sequence. When you need orientation (e.g., for matrix multiplication), you explicitly reshape:

```python
x = torch.tensor([1.0, 2.0, 3.0])  # shape (3,)
x_col = x.unsqueeze(-1)  # shape (3, 1) — column vector
x_row = x.unsqueeze(0)   # shape (1, 3) — row vector
```

Most ML code avoids explicit column/row vectors and uses batched 2-D tensors throughout, relying on broadcasting.

## Vector Operations

### Addition

$$
\mathbf{x} + \mathbf{y} = (x_1 + y_1, \ldots, x_n + y_n)
$$

Geometrically: tip-to-tail addition. Place the tail of $\mathbf{y}$ at the tip of $\mathbf{x}$; the result goes from the tail of $\mathbf{x}$ to the tip of $\mathbf{y}$.

In ML, this is used everywhere — e.g., the residual in a ResNet skip connection is `x + f(x)`, the bias term in a linear layer is `Wx + b`, and the position embedding is added to the token embedding: `token_emb + pos_emb`.

### Scalar Multiplication

$$
c \mathbf{x} = (c x_1, \ldots, c x_n)
$$

Stretches or shrinks the vector by factor $c$ (and reverses direction if $c < 0$). Combined with addition, this gives **linear combinations**: $a\mathbf{x} + b\mathbf{y}$. The set of all linear combinations of a set of vectors is their **span**.

### Dot Product (Inner Product)

See [[02 - Dot Product|the dedicated note]]. Briefly:

$$
\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^{n} x_i y_i
$$

The dot product measures **alignment**: positive when vectors point in similar directions, zero when orthogonal, negative when opposite. It's the foundation of attention, similarity search, and most neural network operations.

### Element-wise (Hadamard) Product

$$
(\mathbf{x} \odot \mathbf{y})_i = x_i y_i
$$

Returns a vector (not a scalar). Used in gating mechanisms (LSTM forget gate, SwiGLU), in masking (causal mask, padding mask), and in gradient flow (chain rule applied element-wise).

```python
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])
x * y  # tensor([4., 10., 18.]) — element-wise product
```

### Outer Product

$$
(\mathbf{x} \otimes \mathbf{y})_{ij} = x_i y_j
$$

Returns a matrix of shape $(n, m)$. Used in rank-1 updates (e.g., in LoRA, in the outer-product form of attention scores $\mathbf{Q}\mathbf{K}^T$ is a collection of outer products).

### Cross Product (3-D Only)

$$
\mathbf{x} \times \mathbf{y} = (x_2 y_3 - x_3 y_2, \; x_3 y_1 - x_1 y_3, \; x_1 y_2 - x_2 y_1)
$$

Returns a vector perpendicular to both inputs, with magnitude equal to the area of the parallelogram they span. Rare in deep learning; more common in graphics and physics. Mentioned here for completeness.

### Norm (Length)

The **L2 norm** (Euclidean length):

$$
\|\mathbf{x}\|_2 = \sqrt{\sum_{i=1}^{n} x_i^2}
$$

The **L1 norm** (Manhattan / taxicab length):

$$
\|\mathbf{x}\|_1 = \sum_{i=1}^{n} |x_i|
$$

The **max norm** (Chebyshev):

$$
\|\mathbf{x}\|_\infty = \max_i |x_i|
$$

The general **Lp norm**:

$$
\|\mathbf{x}\|_p = \left( \sum_{i=1}^{n} |x_i|^p \right)^{1/p}
$$

Norms measure "size". They're used in:
- **Regularization**: L1 → sparsity (Lasso), L2 → weight decay (Ridge), L1+L2 → Elastic Net.
- **Normalization**: LayerNorm, RMSNorm (uses L2 norm of centered/uncentered features).
- **Distance**: Euclidean distance $\|\mathbf{x} - \mathbf{y}\|_2$, Manhattan distance $\|\mathbf{x} - \mathbf{y}\|_1$.
- **Gradient clipping**: `clip_grad_norm_` uses L2 norm of the concatenated gradient vector.

### Normalization to Unit Vectors

$$
\hat{\mathbf{x}} = \frac{\mathbf{x}}{\|\mathbf{x}\|_2}
$$

The result is a **unit vector** — same direction, length 1. Used everywhere in ML: cosine similarity is the dot product of unit vectors; attention scores are sometimes computed with normalized queries and keys.

## Vector Spaces

A **vector space** is a set $V$ equipped with vector addition and scalar multiplication that satisfy the standard axioms (closure, associativity, commutativity, identity, inverse, distributivity, etc.). Formally, $V$ is a module over a field (typically $\mathbb{R}$ or $\mathbb{C}$).

Key concepts:

- **Subspace** — a subset of $V$ that is itself a vector space (e.g., the column space of a matrix, the null space, the row space). Subspaces are central to understanding linear transformations.
- **Span** — the set of all linear combinations of a set of vectors. The span of $k$ vectors is at most $k$-dimensional.
- **Linear independence** — no vector in a set can be written as a combination of the others. A maximal independent set is a basis.
- **Basis** — a maximal set of linearly independent vectors; the size of the basis is the **dimension** of the space. A basis is not unique, but all bases of a space have the same size.
- **Orthogonality** — two vectors are orthogonal if their dot product is 0. An **orthonormal basis** is a basis where all vectors are mutually orthogonal and have unit length. Orthonormal bases simplify many computations (e.g., Fourier analysis, PCA).
- **Inner product space** — a vector space equipped with an inner product (generalization of the dot product). Enables angles, projections, and orthogonality.
- **Normed space** — a vector space equipped with a norm. Enables distance and length.
- **Banach space** — a complete normed space (limits of sequences stay in the space).
- **Hilbert space** — a complete inner product space. The setting for quantum mechanics and much of functional analysis. Infinite-dimensional Hilbert spaces appear in kernel methods and neural tangent kernel theory.

### Important Subspaces in ML

For a matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$:

- **Column space** (range): $\text{Col}(\mathbf{A}) = \{ \mathbf{A}\mathbf{x} : \mathbf{x} \in \mathbb{R}^n \} \subseteq \mathbb{R}^m$. The set of vectors $\mathbf{A}$ can produce. The output of a linear layer lives in the column space of its weight matrix.
- **Null space** (kernel): $\text{Null}(\mathbf{A}) = \{ \mathbf{x} : \mathbf{A}\mathbf{x} = \mathbf{0} \} \subseteq \mathbb{R}^n$. The set of inputs $\mathbf{A}$ maps to zero.
- **Row space**: span of the rows of $\mathbf{A}$, equal to $\text{Col}(\mathbf{A}^T)$.
- **Left null space**: $\text{Null}(\mathbf{A}^T)$.

The **rank** of $\mathbf{A}$ is the dimension of its column space (equivalently, its row space). The **rank-nullity theorem** states: $\text{rank}(\mathbf{A}) + \dim(\text{Null}(\mathbf{A})) = n$.

## Projections

The **projection** of $\mathbf{y}$ onto $\mathbf{x}$ is the component of $\mathbf{y}$ in the direction of $\mathbf{x}$:

$$
\text{proj}_{\mathbf{x}}(\mathbf{y}) = \frac{\mathbf{x} \cdot \mathbf{y}}{\mathbf{x} \cdot \mathbf{x}} \mathbf{x} = \frac{\mathbf{x} \cdot \mathbf{y}}{\|\mathbf{x}\|^2} \mathbf{x}
$$

If $\mathbf{x}$ is a unit vector, this simplifies to $(\mathbf{x} \cdot \mathbf{y}) \mathbf{x}$.

Projections are used in:
- **PCA**: project data onto principal components to reduce dimensionality.
- **Gradient descent**: the update is a step in the negative gradient direction, which is a projection onto the gradient vector.
- **Attention**: the attention score $\mathbf{q} \cdot \mathbf{k}$ is (up to scaling) the projection of the value vector onto the query direction.
- **Orthogonalization**: Gram-Schmidt process removes components along existing basis vectors by subtracting projections.

## Why Vectors Matter for AI

- **Embeddings** — tokens, images, documents, even users are represented as vectors in a learned space. Similarity in that space reflects semantic similarity. See [[05 - Word2Vec GloVe FastText]] and [[06 - Contextual Embeddings ELMo to BERT]].
- **Parameters** — a neural network's parameters are a (very long) vector. Training is the process of moving that vector through parameter space. The total parameter count is the dimension of this vector.
- **Activations** — the intermediate outputs of a network layer are vectors (or batches of vectors). The hidden state of an RNN is a vector; the output of a Transformer layer is a sequence of vectors.
- **Gradients** — the gradient of a loss with respect to parameters is a vector pointing in the direction of steepest ascent. Gradient descent moves in the negative direction.
- **Attention** — attention computes dot products between query and key **vectors**. See [[04 - Self-Attention]]. The attention head's "feature subspace" is the span of the head's projection.
- **Softmax output** — a probability distribution over vocabulary is a vector that sums to 1. The vector lives on the **probability simplex**, a subspace of $\mathbb{R}^V$.
- **Vector databases** — RAG systems store and retrieve vectors. See [[04 - Vector Memory Backends]].

## Vector Representation in Code

### Dense vs. Sparse Vectors

Most ML vectors are **dense** — every component is stored, even if it's zero. For high-dimensional vectors with few non-zero components (e.g., bag-of-words, TF-IDF), **sparse** representations save memory:

```python
# Dense: stores all 1M components
dense = torch.zeros(1_000_000)
dense[42] = 1.0
dense[1337] = 2.0

# Sparse: stores only non-zero components
from scipy import sparse
sparse_vec = sparse.csr_matrix(([1.0, 2.0], ([42, 1337], [0])), shape=(1_000_000, 1))
```

Sparse vectors are essential for retrieval (BM25 uses sparse term vectors) but most neural network operations require dense format.

### Quantized Vectors

For storage and inference efficiency, vectors can be **quantized** to lower precision:

- **FP32** (4 bytes/element): default for training.
- **FP16/BF16** (2 bytes): mixed-precision training, common for inference.
- **INT8** (1 byte): quantized inference, 4× memory reduction.
- **INT4** (0.5 bytes): aggressive quantization, used in GGUF and GPTQ.
- **Binary** (1 bit): extreme quantization, used in binary embeddings for fast retrieval.

A 4096-d embedding takes 16 KB in FP32, 4 KB in INT8, 512 bytes in binary.

### Vectorized Operations

ML operations are **vectorized** — applied to entire vectors at once, not element-by-element. This is essential for GPU performance:

```python
# Slow (Python loop)
result = 0
for i in range(len(x)):
    result += x[i] * y[i]

# Fast (vectorized)
result = (x * y).sum()
# Or
result = torch.dot(x, y)
```

Vectorized operations leverage SIMD (CPU) and SIMT (GPU) parallelism. A dot product of two 4096-d vectors takes microseconds vectorized, milliseconds in a Python loop.

## Common Pitfalls

- **Confusing dimension and shape** — a PyTorch tensor of shape `(32, 768)` represents 32 vectors of dimension 768. The "dimension" of each vector is 768; the "batch size" is 32.
- **Forgetting that vectors have no inherent "position"** — they are defined relative to a basis and an origin. Changing the basis changes the coordinates. PCA is essentially a basis change.
- **Treating a vector as a 1-D tensor vs. a column vector** — mathematically a vector is 1-D; in ML code it's often represented as a column vector of shape `(n, 1)` or a row vector of shape `(1, n)` depending on context. Be explicit.
- **Mixing dtypes** — `torch.dot(float_tensor, double_tensor)` errors. Always ensure both vectors have the same dtype.
- **Forgetting to detach** — when computing vector statistics for logging (e.g., gradient norm), call `.detach()` to avoid building a computation graph.
- **L2 norm of zero vector** — division by $\|\mathbf{x}\|$ fails when $\mathbf{x} = \mathbf{0}$. Always add $\epsilon$: $\hat{\mathbf{x}} = \mathbf{x} / (\|\mathbf{x}\| + \epsilon)$. This is what LayerNorm does internally.
- **Numerical overflow in norm** — for very large vectors, $\sum x_i^2$ can overflow before the sqrt. Use `torch.norm` (which uses a stable algorithm) instead of `(x**2).sum().sqrt()`.

## Production Implications

- **Embedding dimension** is a key architectural choice. Small (e.g., 128) → less expressive but faster and cheaper. Large (e.g., 4096+) → more expressive but more memory and compute. Modern LLMs use hidden dimensions in the thousands (Llama 3 8B: 4096; Llama 3 70B: 8192; GPT-4 inferred: ~12288).
- **Vector storage** at scale requires specialized infrastructure. See [[04 - Vector Memory Backends]] and the vector databases chapter. For 100M vectors of dimension 768 in FP32, storage is 100M × 768 × 4 = 286 GB. Quantization and approximate search are essential.
- **Vector operations dominate compute** in LLMs. The vast majority of FLOPs in a forward pass are matrix multiplications (which are collections of dot products). See [[04 - Matrix Multiplication]]. GPU vendors (NVIDIA, AMD, Google TPU) all optimize heavily for dense matrix-vector products via Tensor Cores / Matrix Units.
- **Memory bandwidth** often bounds vector operations. For element-wise ops and reductions, the cost is reading/writing the vector, not the arithmetic. This is why kernel fusion (combining multiple element-wise ops into one kernel) is so effective.
- **Vector database cost** is dominated by RAM (vectors must be in memory for fast retrieval). At ~$10/GB-month for cloud RAM, 100M 768-d FP32 vectors cost ~$2,860/month just for storage. Quantization to INT8 cuts this 4×.
- **Vector quantization trade-offs**: lower precision saves memory and bandwidth but loses information. FP8 typically loses <1% accuracy; INT4 loses 1-5%; binary loses 5-15%. The right choice depends on the downstream task's sensitivity to embedding noise.

## Mathematical Extensions

### Complex Vectors

A vector in $\mathbb{C}^n$ has complex components. The inner product is conjugated:

$$
\langle \mathbf{x}, \mathbf{y} \rangle = \sum_{i=1}^{n} x_i^* y_i
$$

where $x_i^*$ is the complex conjugate of $x_i$. Complex vectors appear in signal processing (FFT) and in some positional encoding formulations (RoPE uses complex multiplication).

### Random Vectors

A **random vector** $\mathbf{X} \in \mathbb{R}^n$ is a vector whose components are random variables. Characterized by:

- **Mean vector** $\boldsymbol{\mu} = \mathbb{E}[\mathbf{X}]$.
- **Covariance matrix** $\boldsymbol{\Sigma} = \mathbb{E}[(\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^T]$.
- **Multivariate Gaussian** $\mathbf{X} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$.

Random vectors are central to probabilistic ML (VAEs, diffusion, Gaussian processes). The covariance matrix captures correlations between components.

### Vector Calculus

For a scalar function $f: \mathbb{R}^n \to \mathbb{R}$:

- **Gradient** $\nabla f \in \mathbb{R}^n$: vector of partial derivatives. Points in the direction of steepest ascent.
- **Hessian** $\mathbf{H}_f \in \mathbb{R}^{n \times n}$: matrix of second partials. Captures local curvature.

For a vector function $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$:

- **Jacobian** $\mathbf{J}_\mathbf{f} \in \mathbb{R}^{m \times n}$: matrix of partial derivatives. The best linear approximation of $\mathbf{f}$ at a point.

These are the foundation of backpropagation (chain rule applied to vector-valued functions).

## Worked Example: Computing a Gradient

Consider $f(\mathbf{x}) = \|\mathbf{x}\|^2 = \sum_i x_i^2$. The gradient is:

$$
\nabla f = \left( \frac{\partial f}{\partial x_1}, \ldots, \frac{\partial f}{\partial x_n} \right) = (2x_1, \ldots, 2x_n) = 2\mathbf{x}
$$

At $\mathbf{x} = (3, 4)$, $\nabla f = (6, 8)$. The direction of steepest ascent is $(6, 8)$, normalized to $(0.6, 0.8)$. To minimize $f$ via gradient descent, we step in the opposite direction: $\mathbf{x}_{t+1} = \mathbf{x}_t - \eta \nabla f = (3, 4) - 0.1 \cdot (6, 8) = (2.4, 3.2)$.

This is exactly what PyTorch's autograd computes automatically:

```python
x = torch.tensor([3.0, 4.0], requires_grad=True)
f = (x ** 2).sum()
f.backward()
print(x.grad)  # tensor([6., 8.])
```

## Interview Questions

- **Q: What's the difference between a vector and a scalar?**  
  A: A scalar is a single number; a vector is an ordered list of numbers with a notion of direction and magnitude.

- **Q: Why is the dot product of orthogonal vectors zero?**  
  A: $\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \|\mathbf{y}\| \cos\theta$. For orthogonal vectors, $\theta = 90°$, so $\cos\theta = 0$.

- **Q: What's the geometric interpretation of the L2 norm vs. the L1 norm?**  
  A: L2 is the straight-line (Euclidean) distance; L1 is the Manhattan (taxicab) distance — the sum of absolute coordinate differences.

- **Q: Why do we use L2 regularization (weight decay) more often than L1 in deep learning?**  
  A: L2 is differentiable everywhere (smooth gradient), works well with SGD/Adam, and tends to keep all weights small. L1 produces sparsity (many zero weights), which is useful for feature selection but harder to optimize.

- **Q: How would you normalize a vector, and why?**  
  A: Divide by its L2 norm: $\hat{\mathbf{x}} = \mathbf{x} / \|\mathbf{x}\|$. This makes it a unit vector — same direction, length 1. Useful for cosine similarity (dot product of unit vectors), for stable training (RMSNorm, LayerNorm), and for attention score scaling.

- **Q: What's the rank-nullity theorem, and why does it matter?**  
  A: $\text{rank}(\mathbf{A}) + \dim(\text{Null}(\mathbf{A})) = n$. It says the input dimension $n$ is partitioned into the part $\mathbf{A}$ "uses" (column space, dim = rank) and the part it "kills" (null space). Matters for understanding what a linear layer can and cannot represent.

## Further Reading

- Strang, *Introduction to Linear Algebra* — Chapter 1 (vectors), Chapter 2 (matrices), Chapter 3 (subspaces).
- Goodfellow, Bengio, Courville, *Deep Learning* — Chapter 2 (linear algebra review).
- Axler, *Linear Algebra Done Right* — rigorous treatment of vector spaces and linear maps.
- 3Blue1Brown, *Essence of Linear Algebra* (YouTube series) — exceptional geometric intuition.
- Trefethen & Bau, *Numerical Linear Algebra* — computational perspective.

## See Also

- [[02 - Dot Product]]
- [[03 - Cosine Similarity]]
- [[04 - Matrix Multiplication]]
- [[05 - Matrix Decomposition]]
- [[06 - Tensors and Broadcasting]]
- [[04 - Self-Attention]] — attention is built on dot products of query/key vectors
- [[01 - Perceptrons and MLPs]] — a neuron is a dot product + activation
- [[02 - Mathematics/MOC|Mathematics MOC]]
