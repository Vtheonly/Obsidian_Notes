---
tags: [mathematics, linear-algebra, dot-product, inner-product]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Dot Product, Inner Product, Scalar Product]
---

# Dot Product

> [!info] TL;DR
> The dot product of two vectors is the sum of their element-wise products. It is the single most important operation in deep learning — every matrix multiplication is a collection of dot products, and attention is built on dot products. This note covers the formal definition, geometric and algebraic interpretations, properties, generalizations (inner products, tensor contraction), numerical considerations, worked examples, and the role of the dot product across the entire AI stack.

## Definition

For two vectors $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n$:

$$
\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^{n} x_i y_i
$$

The result is a **scalar** (a single number). The operation is also called the **inner product** (in the general sense), the **scalar product** (because the result is a scalar), or written $\langle \mathbf{x}, \mathbf{y} \rangle$.

In PyTorch:

```python
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])
torch.dot(x, y)        # tensor(32.)
(x * y).sum()          # same thing
torch.einsum('i,i->', x, y)  # also same, explicit einsum
```

For batches of vectors, use `torch.bmm` or `torch.einsum`:

```python
# X: (B, D), Y: (B, D) -> output: (B,)
batch_dot = (X * Y).sum(dim=-1)  # or einsum('bd,bd->b', X, Y)

# X: (B, D), Y: (D,) -> output: (B,) broadcasted
broadcast_dot = X @ Y  # matrix-vector product
```

## Geometric Interpretation

The dot product has an equivalent geometric form:

$$
\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \, \|\mathbf{y}\| \cos\theta
$$

where $\theta$ is the angle between the two vectors. This means:

- The dot product is large and positive when vectors point in the same direction ($\theta$ small, $\cos\theta \approx 1$).
- The dot product is 0 when vectors are orthogonal ($\theta = 90°$, $\cos\theta = 0$).
- The dot product is large and negative when vectors point in opposite directions ($\theta = 180°$, $\cos\theta = -1$).
- The dot product equals $\|\mathbf{x}\| \|\mathbf{y}\|$ when the vectors are parallel and aligned.

This geometric form is what makes the dot product useful for **similarity**: if both vectors are normalized (unit length), the dot product equals cosine similarity, which is a measure of directional agreement.

### Derivation of the Geometric Form

The geometric form can be derived from the algebraic form using the **law of cosines**. Consider the vector $\mathbf{x} - \mathbf{y}$ (the difference vector). Its squared norm is:

$$
\|\mathbf{x} - \mathbf{y}\|^2 = \|\mathbf{x}\|^2 + \|\mathbf{y}\|^2 - 2 \mathbf{x} \cdot \mathbf{y}
$$

(by expanding $(\mathbf{x} - \mathbf{y}) \cdot (\mathbf{x} - \mathbf{y})$ and using bilinearity). The law of cosines says:

$$
\|\mathbf{x} - \mathbf{y}\|^2 = \|\mathbf{x}\|^2 + \|\mathbf{y}\|^2 - 2 \|\mathbf{x}\| \|\mathbf{y}\| \cos\theta
$$

Equating the two gives $\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \|\mathbf{y}\| \cos\theta$.

### Projection Interpretation

The dot product gives the **projection** of one vector onto another (when the second is a unit vector):

$$
\text{proj}_{\hat{\mathbf{y}}}(\mathbf{x}) = (\mathbf{x} \cdot \hat{\mathbf{y}}) \hat{\mathbf{y}}
$$

where $\hat{\mathbf{y}} = \mathbf{y} / \|\mathbf{y}\|$ is the unit vector in the direction of $\mathbf{y}$. The scalar $\mathbf{x} \cdot \hat{\mathbf{y}}$ is the **signed length** of the projection (positive if the projection points in the same direction as $\mathbf{y}$, negative if opposite).

This is what attention does: each value vector is weighted by the projection of the query onto the corresponding key direction.

## Algebraic Properties

- **Commutative**: $\mathbf{x} \cdot \mathbf{y} = \mathbf{y} \cdot \mathbf{x}$.
- **Distributive over addition**: $\mathbf{x} \cdot (\mathbf{y} + \mathbf{z}) = \mathbf{x} \cdot \mathbf{y} + \mathbf{x} \cdot \mathbf{z}$.
- **Bilinear**: linear in each argument. $\mathbf{x} \cdot (a\mathbf{y} + b\mathbf{z}) = a(\mathbf{x} \cdot \mathbf{y}) + b(\mathbf{x} \cdot \mathbf{z})$.
- **Positive semi-definite**: $\mathbf{x} \cdot \mathbf{x} = \|\mathbf{x}\|^2 \geq 0$, with equality iff $\mathbf{x} = \mathbf{0}$.
- **Cauchy-Schwarz**: $|\mathbf{x} \cdot \mathbf{y}| \leq \|\mathbf{x}\| \, \|\mathbf{y}\|$, with equality iff $\mathbf{x}$ and $\mathbf{y}$ are linearly dependent.
- **Triangle inequality** (derived from Cauchy-Schwarz): $\|\mathbf{x} + \mathbf{y}\| \leq \|\mathbf{x}\| + \|\mathbf{y}\|$.
- **Pythagorean theorem** (for orthogonal vectors): if $\mathbf{x} \perp \mathbf{y}$, then $\|\mathbf{x} + \mathbf{y}\|^2 = \|\mathbf{x}\|^2 + \|\mathbf{y}\|^2$.
- **Parallelogram law**: $\|\mathbf{x} + \mathbf{y}\|^2 + \|\mathbf{x} - \mathbf{y}\|^2 = 2(\|\mathbf{x}\|^2 + \|\mathbf{y}\|^2)$.

## Why It Matters for AI

### 1. It is the basic operation of neural networks

A single neuron computes:

$$
y = \sigma(\mathbf{w} \cdot \mathbf{x} + b)
$$

— a dot product between the input vector $\mathbf{x}$ and the weight vector $\mathbf{w}$, followed by a bias and an activation function. Every dense layer is just a batch of such dot products. See [[01 - Perceptrons and MLPs]].

Geometrically, $\mathbf{w} \cdot \mathbf{x} + b = 0$ defines a **hyperplane** in input space. The neuron fires (output > 0) on one side of the hyperplane and doesn't fire on the other. A neural network is a stack of such hyperplane tests, composed and curved by the activation function.

### 2. Matrix multiplication is a collection of dot products

The matrix product $\mathbf{A}\mathbf{B}$ is computed by taking the dot product of each row of $\mathbf{A}$ with each column of $\mathbf{B}$:

$$
(\mathbf{A}\mathbf{B})_{ij} = \sum_k A_{ik} B_{kj} = \mathbf{A}_{i,:} \cdot \mathbf{B}_{:,j}
$$

See [[04 - Matrix Multiplication]]. Every linear layer in a neural network is a matrix multiplication; thus every linear layer is a batch of dot products.

### 3. Attention is built on dot products

[[04 - Self-Attention|Scaled dot-product attention]] computes the dot product between a query vector and every key vector to determine how much weight to assign to each value:

$$
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right) \mathbf{V}
$$

The matrix product $\mathbf{Q}\mathbf{K}^T$ is a matrix where each entry is a dot product between a query row and a key row. This is the heart of the Transformer — the most important architecture in modern AI.

### 4. Cosine similarity is a normalized dot product

When comparing embeddings (e.g., for RAG retrieval), we use cosine similarity, which is the dot product of normalized vectors:

$$
\cos(\mathbf{x}, \mathbf{y}) = \frac{\mathbf{x} \cdot \mathbf{y}}{\|\mathbf{x}\| \, \|\mathbf{y}\|} = \hat{\mathbf{x}} \cdot \hat{\mathbf{y}}
$$

See [[03 - Cosine Similarity]]. This is the standard similarity metric for vector search, RAG retrieval, and embedding-based clustering.

### 5. The dot product defines orthogonality

Two vectors are **orthogonal** iff their dot product is 0. Orthogonality is fundamental to linear algebra (orthogonal bases, QR decomposition, SVD) and shows up in ML (orthogonal initialization, decorrelated features, Gram-Schmidt process, PCA).

### 6. The dot product measures alignment in feature spaces

In kernel methods (SVM with RBF kernel, kernel PCA), the kernel function $k(\mathbf{x}, \mathbf{y})$ is a generalization of the dot product — it's a dot product in a (possibly infinite-dimensional) feature space. The "kernel trick" lets us compute in feature space without explicitly mapping to it.

### 7. The dot product is the building block of attention scoring

In neural attention (Bahdanau, Luong, Transformer), the attention score is computed as a dot product (or its generalization) between query and key. The softmax of these scores produces the attention weights. The dot product is thus the foundation of all attention mechanisms.

## Worked Examples

### Example 1: Basic Dot Product

Let $\mathbf{x} = (1, 2, 3)$ and $\mathbf{y} = (4, 5, 6)$.

$$
\mathbf{x} \cdot \mathbf{y} = (1)(4) + (2)(5) + (3)(6) = 4 + 10 + 18 = 32
$$

The norms are $\|\mathbf{x}\| = \sqrt{14} \approx 3.74$ and $\|\mathbf{y}\| = \sqrt{77} \approx 8.77$. So:

$$
\cos\theta = \frac{32}{3.74 \times 8.77} \approx 0.974
$$

The angle is $\theta \approx 13°$ — the vectors point in very similar directions.

### Example 2: Orthogonal Vectors

Let $\mathbf{x} = (1, 0)$ and $\mathbf{y} = (0, 1)$ — the standard basis vectors.

$$
\mathbf{x} \cdot \mathbf{y} = (1)(0) + (0)(1) = 0
$$

Confirms orthogonality. $\cos\theta = 0$, so $\theta = 90°$.

### Example 3: Opposite Vectors

Let $\mathbf{x} = (1, 2, 3)$ and $\mathbf{y} = (-1, -2, -3) = -\mathbf{x}$.

$$
\mathbf{x} \cdot \mathbf{y} = -1 - 4 - 9 = -14 = -\|\mathbf{x}\|^2
$$

$\cos\theta = -1$, so $\theta = 180°$ — opposite directions.

### Example 4: Attention Score

In a Transformer with $d_k = 64$, suppose $\mathbf{q} \cdot \mathbf{k} = 12.8$. The scaled score is $12.8 / \sqrt{64} = 1.6$. After softmax with other scores, this contributes proportionally to the attention weight. Without scaling, raw dot products of high-dimensional vectors can be very large (order $\sqrt{d_k}$ for random vectors), pushing softmax into saturation.

### Example 5: Cosine Similarity in RAG

Two documents have embeddings $\mathbf{d}_1 = (0.8, 0.6, 0.0)$ and $\mathbf{d}_2 = (0.6, 0.8, 0.0)$ (both unit length, in 3-d for illustration).

$$
\cos(\mathbf{d}_1, \mathbf{d}_2) = 0.8 \times 0.6 + 0.6 \times 0.8 + 0 = 0.96
$$

High similarity — these documents are about similar topics. A query $\mathbf{q} = (0.0, 0.0, 1.0)$ (orthogonal topic) gives $\cos(\mathbf{q}, \mathbf{d}_1) = 0$ — no match.

## Higher-Rank Generalization: Tensor Contraction

The dot product generalizes to tensors of any rank. The **contraction** of two tensors along a shared axis is a sum of products, exactly like a dot product but possibly along multiple axes simultaneously. This is what `torch.matmul`, `torch.einsum`, and similar APIs do.

For example, in attention we compute $\mathbf{Q}\mathbf{K}^T$ — a matrix product where each entry is a dot product between a query row and a key row:

```python
# Q: (B, H, L, D), K: (B, H, L, D) -> scores: (B, H, L, L)
scores = torch.einsum('bhld,bhmd->bhlm', Q, K)  # batched dot product
```

The `einsum` notation `'bhld,bhmd->bhlm'` says: "for each batch $b$ and head $h$, compute the dot product (over $d$) between every $l$-th query and every $m$-th key, producing a matrix indexed by $(l, m)$".

General tensor contraction underlies:
- **Batched matrix multiplication** (every attention head's QK^T).
- **Attention score computation** (the `bhld,bhmd->bhlm` pattern above).
- **Gradient computation** in backprop (chain rule as tensor contractions).
- **Einstein summation** in physics and ML.

## Inner Products (Generalization)

The dot product is a specific instance of an **inner product** — a function $\langle \cdot, \cdot \rangle: V \times V \to \mathbb{R}$ satisfying:

1. **Symmetry**: $\langle \mathbf{x}, \mathbf{y} \rangle = \langle \mathbf{y}, \mathbf{x} \rangle$ (or conjugate symmetry for complex spaces).
2. **Linearity** in the first argument: $\langle a\mathbf{x} + b\mathbf{y}, \mathbf{z} \rangle = a\langle \mathbf{x}, \mathbf{z} \rangle + b\langle \mathbf{y}, \mathbf{z} \rangle$.
3. **Positive-definiteness**: $\langle \mathbf{x}, \mathbf{x} \rangle \geq 0$, with equality iff $\mathbf{x} = \mathbf{0}$.

Other inner products include:

- **Weighted inner product**: $\langle \mathbf{x}, \mathbf{y} \rangle_W = \mathbf{x}^T \mathbf{W} \mathbf{y}$ for a positive-definite matrix $\mathbf{W}$. Used in Mahalanobis distance.
- **Polynomial kernel**: $k(\mathbf{x}, \mathbf{y}) = (\mathbf{x} \cdot \mathbf{y} + c)^d$. Implicit dot product in a higher-dimensional feature space.
- **RBF kernel**: $k(\mathbf{x}, \mathbf{y}) = \exp(-\gamma \|\mathbf{x} - \mathbf{y}\|^2)$. Dot product in an infinite-dimensional feature space.
- **Function inner product**: $\langle f, g \rangle = \int f(x) g(x) dx$ for functions $f, g$. Used in functional analysis and physics.

The dot product is the **standard Euclidean inner product** on $\mathbb{R}^n$ — simple, fast to compute, and well-suited to GPU acceleration.

## Computational Complexity

The dot product of two $n$-dimensional vectors requires:
- **$n$ multiplications** and **$n-1$ additions** → $O(n)$ arithmetic operations.
- **$n$ memory reads** (one per element of each vector) → $O(n)$ memory traffic.

For $n = 4096$ (typical LLM hidden size), this is 4096 multiplies + 4095 adds = 8191 FLOPs per dot product. A matrix multiplication $\mathbf{A}\mathbf{B}$ where $\mathbf{A} \in \mathbb{R}^{m \times n}$ and $\mathbf{B} \in \mathbb{R}^{n \times p}$ requires $m \times p$ dot products of length $n$ → $O(mnp)$ FLOPs.

### Arithmetic Intensity

The dot product has **arithmetic intensity** = FLOPs / bytes = $2n / (2n \cdot \text{dtype_size})$. For FP32: $2n / (8n) = 0.25$ FLOPs/byte. This is very low — the operation is **memory-bound**, not compute-bound. GPUs can do many more FLOPs per second than the memory bandwidth supports.

This is why dot products are typically batched into matrix multiplications: the matrix-matrix version has higher arithmetic intensity ($2mnp / ((mn + np + mp) \cdot \text{dtype_size})$) and can utilize Tensor Cores.

## Numerical Stability

The dot product is generally numerically stable, but there are edge cases:

### Overflow in Mixed Precision

In **fp16/bf16** mixed-precision training, large dot products can overflow. The classic example is the $QK^T$ product in attention, which is why we scale by $\sqrt{d_k}$ — see [[04 - Self-Attention]] § "Why scale by √d_k".

For random vectors with components of unit variance, the dot product has standard deviation $\sqrt{n}$, so for $n = 4096$, the dot product can easily reach 64+. FP16 maxes out at 65504 — close to overflow.

### Catastrophic Cancellation

When summing $x_i y_i$ with mixed signs, significant digits can cancel. The classic example is computing variance as $\sum x_i^2 - n \bar{x}^2$ — numerically unstable. Use the "shifted" form $\sum (x_i - \bar{x})^2$ instead.

For dot products, this is rarely an issue in practice because ML vectors typically have non-negative components after activations (ReLU, softmax) or balanced signs (embeddings).

### Accumulation Precision

Summing $n$ numbers in FP16 accumulates rounding errors of order $\sqrt{n} \cdot \epsilon_{FP16} \approx \sqrt{4096} \cdot 10^{-3} \approx 0.06$. For dot products of length 4096, FP16 accumulation loses ~2 decimal digits. Many GPUs accumulate in FP32 even when inputs are FP16 — check your hardware.

### Kahan Summation

For numerical stability when summing many terms, **Kahan summation** compensates for rounding errors:

```python
def kahan_dot(x, y):
    sum_ = 0.0
    c = 0.0  # compensation
    for xi, yi in zip(x, y):
        product = xi * yi
        y_ = product - c
        t = sum_ + y_
        c = (t - sum_) - y_
        sum_ = t
    return sum_
```

In practice, GPUs use hardware accumulation in FP32, which is good enough for most ML applications. Kahan summation is rarely needed.

## Common Pitfalls

- **Forgetting to align dimensions** — the dot product requires both vectors to have the same dimension. A shape mismatch in code is usually a sign that you meant to broadcast or to take a matrix product instead.
- **Confusing dot product with element-wise product** — the element-wise (Hadamard) product `x * y` returns a vector, not a scalar. The dot product is the sum of the element-wise products.
- **Forgetting to normalize for similarity** — a high dot product can simply mean "long vectors", not "similar directions". Use [[03 - Cosine Similarity]] when you care about direction.
- **Mixing dtypes** — `torch.dot(float_tensor, double_tensor)` raises an error. Always ensure both vectors have the same dtype.
- **Forgetting to detach** — when computing dot products for logging (e.g., gradient norm), call `.detach()` to avoid building a computation graph and leaking memory.
- **Numerical issues with high-dim dot products** — for $d > 1000$, raw dot products can be very large. Scale (e.g., by $1/\sqrt{d}$) or use normalized versions.
- **Negative dot product confusion** — for embeddings, the dot product can be negative (especially for unnormalized vectors). Cosine similarity ranges from -1 to 1; if you need a probability-like score, apply $(\cos + 1) / 2$ or temperature-scaled softmax.
- **Batched dot product gotchas** — `torch.dot` requires 1-D inputs. For batched dot products, use `(X * Y).sum(dim=-1)` or `torch.einsum('bd,bd->b', X, Y)`.

## Production Implications

- The dot product (and the matrix multiplication built from it) is the single most optimized operation in deep learning hardware. **Tensor Cores** on NVIDIA GPUs are essentially dot-product accelerators — they perform $4 \times 4 \times 4$ matrix multiplications (= 64 dot products of length 4) in a single cycle.
- For very large dot products (e.g., computing attention scores over a long context), the operation becomes **memory-bound** rather than compute-bound. This is what [[11 - FlashAttention]] addresses — by tiling and fusing, it reduces memory traffic by 5-10×.
- GPU peak FLOPs for dot products: H100 SXM5 reaches ~989 TFLOPs in FP8, ~1979 TFLOPs in FP4 with sparsity. Most of this is dot-product compute.
- **Vectorized vs. scalar implementations**: a naive Python loop computing a 4096-d dot product takes ~1ms; the vectorized `torch.dot` takes ~5μs — a 200× speedup. Always vectorize.
- **Custom CUDA kernels**: for specialized dot products (e.g., sparse, quantized, with custom layouts), custom kernels can outperform `torch.dot` by 2-5×. This is the basis of FlashAttention, FlashAttention-2/3, and many production optimizations.
- **Energy cost**: a 4096-d FP16 dot product consumes ~8 nJ on H100. At 1M dot products per second (typical for batch inference), that's 8 mW — small per op, but multiplied by billions of ops per query, it adds up to the GPU's 350W TDP.

## Cross-Domain Connections

The dot product appears in nearly every chapter of this vault:

- **Chapter 02 (Mathematics)**: the operation itself, and the basis for matrix multiplication, decomposition, and tensor contraction.
- **Chapter 03 (Machine Learning)**: every linear model is a dot product; SVMs use dot products (or kernels) for margin computation.
- **Chapter 04 (Neural Networks)**: every neuron is a dot product + activation.
- **Chapter 05 (NLP)**: word embeddings are vectors; similarity is dot product.
- **Chapter 06 (Attention)**: attention scores are dot products (Q · K).
- **Chapter 07 (Transformers)**: every linear layer is a batch of dot products.
- **Chapter 08 (LLMs)**: the entire model is a stack of dot products.
- **Chapter 13 (Inference)**: most inference optimizations (FlashAttention, quantization, kernel fusion) target dot products.
- **Chapter 17 (RAG)**: retrieval is dot product (or cosine similarity, which is normalized dot product).
- **Chapter 18 (Memory)**: vector memory retrieval is dot product.

Understanding the dot product deeply is the single highest-leverage mathematical concept for AI engineering.

## Interview Questions

- **Q: Why is the dot product of random high-dimensional vectors typically close to zero?**  
  A: For random vectors with i.i.d. components of mean 0 and variance $\sigma^2$, the dot product has mean 0 and standard deviation $\sigma^2 \sqrt{n}$. The dot product grows as $\sqrt{n}$, but the norms grow as $\sqrt{n}$ too, so cosine similarity (normalized dot product) concentrates around 0 for high-dimensional random vectors — the "curse of dimensionality" makes random vectors nearly orthogonal.

- **Q: Why do we scale by $\sqrt{d_k}$ in attention?**  
  A: For random Q, K with components of unit variance, $\mathbf{q} \cdot \mathbf{k}$ has variance $d_k$. So the dot product grows as $\sqrt{d_k}$, and for large $d_k$ the softmax saturates (one entry dominates, gradients vanish). Dividing by $\sqrt{d_k}$ keeps the variance at 1, stabilizing training.

- **Q: What's the difference between the dot product and the inner product?**  
  A: The dot product is the standard Euclidean inner product on $\mathbb{R}^n$. The inner product is a more general concept — any symmetric, bilinear, positive-definite function. Weighted inner products, polynomial kernels, and RBF kernels are all inner products.

- **Q: How would you compute the cosine similarity of two vectors efficiently?**  
  A: Normalize both vectors (divide by L2 norm), then take the dot product. For batched computation, normalize along the last dimension with `x / x.norm(dim=-1, keepdim=True)`, then matrix multiply.

- **Q: Why are random vectors in high dimensions nearly orthogonal?**  
  A: In $\mathbb{R}^n$, the number of "nearly orthogonal" directions grows exponentially with $n$. For any fixed vector, the volume of directions within angle $\theta$ of it shrinks as $\theta^{n-1}$. So for high $n$, most random directions are nearly orthogonal. This is why embeddings work — high-dimensional spaces have room for many dissimilar items.

## Further Reading

- Strang, *Introduction to Linear Algebra* — Chapter 1 (dot product), Chapter 3 (orthogonality).
- Goodfellow et al., *Deep Learning* — Chapter 2 (linear algebra review).
- Trefethen & Bau, *Numerical Linear Algebra* — computational perspective.
- Higham, *Accuracy and Stability of Numerical Algorithms* — for numerical stability of summation.
- Hennessy & Patterson, *Computer Architecture* — for hardware implementation of dot products (SIMD, Tensor Cores).

## See Also

- [[01 - Vectors]]
- [[03 - Cosine Similarity]]
- [[04 - Matrix Multiplication]]
- [[05 - Matrix Decomposition]]
- [[06 - Tensors and Broadcasting]]
- [[04 - Self-Attention]] — the most important use of the dot product in modern AI
- [[01 - Perceptrons and MLPs]] — a neuron is a dot product + activation
- [[11 - FlashAttention]] — optimizing the dot product for long contexts
- [[02 - Mathematics/MOC|Mathematics MOC]]
