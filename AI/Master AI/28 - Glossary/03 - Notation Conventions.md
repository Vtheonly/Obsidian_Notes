---
tags: [glossary, notation, conventions, mathematics, reference]
iteration: 6
created: 2026-08-08
aliases: [Notation Conventions, Math Notation, Symbol Conventions]
---

# 03 — Notation Conventions

> [!info] TL;DR
> This note defines the mathematical and symbolic notation used throughout the vault. Consistent notation matters because AI engineering spans linear algebra, calculus, probability, information theory, and computer science — each with its own conventions. Without a single reference, the same symbol can mean different things in different notes (e.g., $T$ for temperature vs. $T$ for transpose vs. $T$ for tokens). This note resolves those ambiguities and provides the standard forms for vectors, matrices, attention, gradients, and probability distributions.

## Why Notation Conventions Matter

Mathematical notation in AI is inconsistent across sources. The Transformer paper (Vaswani et al., 2017) uses $d_k$ for key dimension; the BERT paper uses $d$ for hidden size; some tutorials use $H$ for hidden states while others use $h$. Without a reference, readers must infer meaning from context — slow and error-prone.

This note establishes the conventions used throughout the vault. When a note deviates from these conventions, it states the deviation explicitly.

## General Principles

1. **Bold uppercase** ($\mathbf{X}$): matrices.
2. **Bold lowercase** ($\mathbf{x}$): vectors.
3. **Regular lowercase** ($x$, $i$, $j$): scalars and indices.
4. **Uppercase** ($X$, $T$, $N$): random variables or sizes (context-dependent, stated in the note).
5. **Calligraphic** ($\mathcal{L}$, $\mathcal{D}$): sets, loss functions, distributions.
6. **Greek letters**: parameters ($\theta$, $\phi$), hyperparameters ($\alpha$, $\beta$, $\gamma$), small constants ($\epsilon$).
7. **Subscripts**: indices ($x_i$, $h_t$).
8. **Superscripts**: layer or step ($h^{(l)}$, $z^{(t)}$). Use parentheses to distinguish from exponentiation ($x^2$ vs $x^{(2)}$).

## Linear Algebra

### Vectors

- $\mathbf{x} \in \mathbb{R}^d$: a real-valued vector of dimension $d$.
- $x_i$: the $i$-th element of $\mathbf{x}$ (1-indexed unless noted).
- $\|\mathbf{x}\|_2$: L2 norm.
- $\|\mathbf{x}\|_1$: L1 norm.
- $\hat{\mathbf{x}} = \mathbf{x} / \|\mathbf{x}\|_2$: the unit vector in the direction of $\mathbf{x}$.

### Matrices

- $\mathbf{X} \in \mathbb{R}^{m \times n}$: a real-valued matrix with $m$ rows and $n$ columns.
- $\mathbf{X}_{ij}$ or $X_{ij}$: the element at row $i$, column $j$.
- $\mathbf{X}^\top$: transpose.
- $\mathbf{X}^{-1}$: inverse (for square matrices).
- $\mathbf{I}$: identity matrix (size inferred from context).

### Operations

- $\mathbf{x} \cdot \mathbf{y}$ or $\mathbf{x}^\top \mathbf{y}$: dot product (scalar).
- $\mathbf{x} \otimes \mathbf{y}$: outer product (matrix).
- $\mathbf{X} \mathbf{Y}$: matrix product.
- $\mathbf{X} \odot \mathbf{Y}$: Hadamard (element-wise) product.
- $\text{diag}(\mathbf{x})$: diagonal matrix with $\mathbf{x}$ on the diagonal.

### Norms and Similarity

- $\cos(\mathbf{x}, \mathbf{y}) = \frac{\mathbf{x} \cdot \mathbf{y}}{\|\mathbf{x}\|_2 \|\mathbf{y}\|_2}$: cosine similarity.
- $\|\mathbf{x} - \mathbf{y}\|_2$: Euclidean distance.

### Decompositions

- $\mathbf{X} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^\top$: SVD.
- $\mathbf{X} = \mathbf{Q} \mathbf{R}$: QR decomposition.
- $\text{eig}(\mathbf{X})$: eigenvalues.

## Tensors

- $\mathcal{X} \in \mathbb{R}^{n_1 \times n_2 \times \cdots \times n_k}$: a $k$-dimensional tensor.
- $\mathcal{X}_{i_1, i_2, \ldots, i_k}$: an element.
- Broadcasting follows NumPy conventions: dimensions of size 1 are repeated.

## Attention

The Transformer attention mechanism has standard notation:

- $\mathbf{Q}, \mathbf{K}, \mathbf{V}$: query, key, value matrices. Each row is a token's representation.
- $d_k, d_v$: key and value dimensions (often equal; use $d$ when they are).
- $d_{\text{model}}$: model hidden size.
- $h$: number of attention heads.
- $d_h = d_{\text{model}} / h$: per-head dimension.

Scaled dot-product attention:

$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q} \mathbf{K}^\top}{\sqrt{d_k}}\right) \mathbf{V}$$

Multi-head attention:

$$\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) \mathbf{W}^O$$

where $\text{head}_i = \text{Attention}(\mathbf{Q} \mathbf{W}_i^Q, \mathbf{K} \mathbf{W}_i^K, \mathbf{V} \mathbf{W}_i^V)$.

## Probability

### Random Variables

- $X$: a random variable.
- $x$: a specific value of $X$.
- $P(X = x)$ or $P(x)$: probability mass (discrete) or density (continuous).
- $p(x \mid y)$: conditional probability density.

### Distributions

- $\mathcal{N}(\mu, \sigma^2)$: Gaussian with mean $\mu$ and variance $\sigma^2$.
- $\text{Bernoulli}(p)$: Bernoulli with parameter $p$.
- $\text{Cat}(p_1, \ldots, p_K)$: categorical over $K$ classes.
- $\text{Uniform}(a, b)$: uniform on $[a, b]$.

### Statistics

- $\mathbb{E}[X]$: expectation.
- $\text{Var}(X)$: variance.
- $\text{Cov}(X, Y)$: covariance.
- $\hat{\theta}$: an estimate of $\theta$.

### Information Theory

- $H(X) = -\sum_x p(x) \log p(x)$: entropy.
- $H(p, q) = -\sum_x p(x) \log q(x)$: cross entropy.
- $D_{\text{KL}}(p \| q) = \sum_x p(x) \log \frac{p(x)}{q(x)}$: KL divergence.
- $I(X; Y)$: mutual information.

## Calculus and Optimization

### Derivatives

- $\frac{df}{dx}$: derivative of $f$ with respect to $x$.
- $\frac{\partial f}{\partial x}$: partial derivative.
- $\nabla f$: gradient (vector of partials).
- $\nabla_{\mathbf{x}} f$: gradient with respect to $\mathbf{x}$.
- $\nabla^2 f$ or $\mathbf{H}_f$: Hessian (matrix of second partials).
- $\mathbf{J}_f$: Jacobian.

### Optimization

- $\mathcal{L}(\theta)$: loss function.
- $\theta$: model parameters.
- $\phi$: sometimes used for additional parameters (e.g., discriminator in GANs, value function in RL).
- $\alpha$ or $\eta$: learning rate.
- $\nabla_\theta \mathcal{L}$: gradient of loss with respect to parameters.
- $\theta \leftarrow \theta - \alpha \nabla_\theta \mathcal{L}$: gradient descent update.

## Sequences and Time

- $T$: sequence length (number of tokens). **Not** temperature in this context.
- $t$: time step or position index.
- $\mathbf{x}_t$: the token at position $t$.
- $\mathbf{x}_{1:t}$: the sequence $\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_t$.
- $\mathbf{h}_t^{(l)}$: hidden state at position $t$ in layer $l$.

## Special Symbols

- $\tau$: temperature (in softmax and sampling). When used, state explicitly to avoid confusion with $T$.
- $\sigma$: sigmoid function, $\sigma(x) = 1 / (1 + e^{-x})$. **Not** standard deviation (use $s$ or $\sigma_X$ with subscript for std).
- $\text{softmax}$: the softmax function, $\text{softmax}(\mathbf{x})_i = \frac{e^{x_i}}{\sum_j e^{x_j}}$.
- $\epsilon$: small constant (e.g., for numerical stability).
- $\top$: transpose (as superscript).
- $\approx$: approximately equal.
- $\sim$: sampled from (e.g., $x \sim \mathcal{N}(0, 1)$).
- $\propto$: proportional to.

## Reinforcement Learning

- $s_t$: state at time $t$.
- $a_t$: action at time $t$.
- $r_t$: reward at time $t$.
- $\pi(a \mid s)$: policy (probability of action $a$ given state $s$).
- $\gamma$: discount factor.
- $Q(s, a)$: action-value function.
- $V(s)$: state-value function.
- $A(s, a) = Q(s, a) - V(s)$: advantage function.

## Information Theory in ML Context

- $\text{KL}(\pi \| \pi_{\text{ref}})$: KL penalty (used in RLHF to keep policy close to reference).
- $\beta$: KL penalty coefficient.

## Subscripts and Superscripts Summary

| Symbol                  | Meaning                                        |
|-------------------------|------------------------------------------------|
| $x_i$                   | Element $i$ of vector $\mathbf{x}$.            |
| $X_{ij}$                | Element at row $i$, column $j$ of $\mathbf{X}$. |
| $\mathbf{h}^{(l)}$      | Hidden state at layer $l$.                     |
| $\mathbf{h}_t$          | Hidden state at time step $t$.                 |
| $\mathbf{h}_t^{(l)}$    | Hidden state at time $t$, layer $l$.           |
| $\theta_t$              | Parameters at training step $t$.               |
| $\hat{y}$               | Predicted value of $y$.                        |
| $\bar{x}$               | Mean of $x$.                                   |

## Common Conflicts and Disambiguation

| Symbol | Common Meaning 1         | Common Meaning 2                | Resolution                                |
|--------|--------------------------|----------------------------------|--------------------------------------------|
| $T$    | Sequence length          | Temperature                      | Use $\tau$ for temperature.                |
| $H$    | Hidden size              | Entropy                          | Context-dependent; state in note.          |
| $h$    | Hidden state             | Number of attention heads        | Use $d_{\text{model}}$ for size, $h$ for heads. |
| $\sigma$ | Sigmoid                | Standard deviation               | Use $s$ for std; $\sigma_X$ if needed.     |
| $N$    | Number of samples        | Sequence length (some papers)    | Use $T$ for sequence length.               |
| $K$    | Number of classes        | Number of attention heads (rare) | Use $h$ for heads; $K$ for classes.        |
| $V$    | Value matrix             | Vocabulary size (some papers)    | Use $|V|$ for vocab size.                   |
| $D$    | Dataset                  | Dimension                        | Use $d$ for dimension; $\mathcal{D}$ for dataset. |

## Code Conventions

In code blocks:

- Variables match the math: `Q`, `K`, `V`, `d_model`, `num_heads`.
- Function names are lowercase with underscores: `scaled_dot_product_attention`.
- Class names are PascalCase: `MultiHeadAttention`.
- Constants are UPPER_CASE: `MAX_SEQ_LEN`.

## References

The conventions in this note are based on:

- Vaswani et al. (2017) — Transformer notation ($Q, K, V, d_k$).
- Goodfellow, Bengio, Courville (2016) — Deep Learning textbook conventions.
- Bishop (2006) — Pattern Recognition and Machine Learning conventions.
- NumPy / PyTorch documentation — programming conventions.

When a note's source uses different conventions, the note either:

1. Adopts this vault's conventions (preferred), or
2. Uses the source's conventions and states the mapping.

## See Also

- [[A-Z Terms]] — glossary of AI engineering terms
- [[Acronyms Index]] — index of acronyms
- [[28 - Glossary/MOC|28 Glossary MOC]]
- [[02 - Mathematics/MOC|02 Mathematics]] — where most notation is used
