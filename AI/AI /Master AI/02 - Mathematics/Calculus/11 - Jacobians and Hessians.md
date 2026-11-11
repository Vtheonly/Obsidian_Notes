---
tags: [mathematics, calculus, jacobian, hessian]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Jacobians and Hessians]
---

# 11 - Jacobians and Hessians

> [!info] TL;DR
> The Jacobian generalizes the gradient to vector-valued functions. The Hessian is the matrix of second derivatives. Both are essential for understanding optimization, Newton's method, and the geometry of loss landscapes.

## Recap: Gradient

For a scalar function $f: \mathbb{R}^n \to \mathbb{R}$, the **gradient** is the vector of partial derivatives:

$$
\nabla f = \left( \frac{\partial f}{\partial x_1}, \ldots, \frac{\partial f}{\partial x_n} \right)
$$

The gradient is a row-vector of partials. It points in the direction of steepest ascent. See [[10 - Gradient and Chain Rule|Gradient and Chain Rule]].

## The Jacobian

For a vector-valued function $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$, the **Jacobian** is the $m \times n$ matrix of all first-order partial derivatives:

$$
\mathbf{J} = \begin{pmatrix} 
\frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n}
\end{pmatrix}
$$

Each row is the gradient of one output component. The Jacobian is the natural generalization of the derivative to multivariate vector-valued functions.

### Geometric meaning

The Jacobian describes the **local linear approximation** of $\mathbf{f}$ near a point:

$$
\mathbf{f}(\mathbf{x} + \mathbf{h}) \approx \mathbf{f}(\mathbf{x}) + \mathbf{J} \mathbf{h}
$$

For a transformation $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^n$, $|\det \mathbf{J}|$ is the **local volume scaling factor** — how much $\mathbf{f}$ stretches or shrinks volume near each point. This is the **Jacobian determinant** that appears in probability density transformations:

$$
p_{\mathbf{Y}}(\mathbf{y}) = p_{\mathbf{X}}(\mathbf{x}) \cdot \left| \det \frac{\partial \mathbf{x}}{\partial \mathbf{y}} \right|
$$

Critical for normalizing flows (a generative modeling technique) and for any change-of-variables in probability.

### Chain rule with Jacobians

If $\mathbf{z} = \mathbf{f}(\mathbf{y})$ and $\mathbf{y} = \mathbf{g}(\mathbf{x})$, then:

$$
\mathbf{J}_{\mathbf{f} \circ \mathbf{g}}(\mathbf{x}) = \mathbf{J}_\mathbf{f}(\mathbf{g}(\mathbf{x})) \cdot \mathbf{J}_\mathbf{g}(\mathbf{x})
$$

This is the multivariate chain rule — backpropagation is essentially computing this product in reverse order. See [[04 - Neural Networks/Training/Backpropagation|Backpropagation]].

## The Hessian

For a scalar function $f: \mathbb{R}^n \to \mathbb{R}$, the **Hessian** is the $n \times n$ matrix of second-order partial derivatives:

$$
\mathbf{H} = \begin{pmatrix}
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots \\
\vdots & & \ddots
\end{pmatrix}
$$

The Hessian is the **derivative of the gradient**. It describes how the gradient itself changes — the **curvature** of $f$.

### Eigenvalues of the Hessian

The eigenvalues of $\mathbf{H}$ at a critical point ($\nabla f = 0$) tell you the local shape:

- All eigenvalues positive → **local minimum**.
- All negative → **local maximum**.
- Mixed signs → **saddle point**.
- Some zero → **degenerate** (need higher-order info).

In high dimensions (typical for neural networks), saddle points vastly outnumber local minima. This is why "saddle points vs local minima" was a major research topic in deep learning optimization (2014–2017).

### Condition number

The condition number $\kappa = \lambda_{\max} / \lambda_{\min}$ measures how "ill-conditioned" the loss is. High $\kappa$ means the gradient points mostly toward the steep direction, but the minimum lies in the flat direction — gradient descent oscillates. This is why **momentum** and **Adam** (which adapt per-dimension) help.

## Newton's Method

Newton's method uses the Hessian to take a more informed step:

$$
\mathbf{x}_{t+1} = \mathbf{x}_t - \mathbf{H}^{-1} \nabla f(\mathbf{x}_t)
$$

The Hessian inverse "corrects" for curvature — Newton's method converges quadratically (much faster than gradient descent's linear convergence), **when it works**.

### Why Newton's method isn't used in deep learning

- **Hessian is huge**: for a 1B-parameter model, the Hessian is $10^9 \times 10^9$ — completely impossible to store or invert.
- **Hessian computation is expensive**: requires $O(n^2)$ second-derivative evaluations.
- **Not always positive-definite**: far from a minimum, the Hessian can have negative eigenvalues, and Newton steps can diverge.

Approximations like **L-BFGS** (quasi-Newton) and **K-FAC** (block-diagonal Hessian approximation) are used in some niche settings, but the standard deep learning optimizers (SGD, Adam, AdamW) are first-order — they use only gradients, not Hessians.

## Worked Example

Let $f(x, y) = x^2 + 3xy + 2y^2$.

Gradient: $\nabla f = (2x + 3y, 3x + 4y)$.

Hessian:

$$
\mathbf{H} = \begin{pmatrix} 2 & 3 \\ 3 & 4 \end{pmatrix}
$$

Eigenvalues: $\lambda = 3 \pm \sqrt{10}$. One positive, one negative — so the origin is a **saddle point** (not a minimum).

## Inverse Hessian-Vector Products (HVPs)

In practice, we rarely compute the full Hessian, but we often need **Hessian-vector products** $\mathbf{H} \mathbf{v}$. These can be computed efficiently via autodiff (Pearlmutter's trick) without materializing $\mathbf{H}$:

$$
\mathbf{H} \mathbf{v} = \nabla (\nabla f \cdot \mathbf{v})
$$

HVPs power:
- **Newton's method** with conjugate gradient (Hessian-free).
- **Influence functions** (which training points most affect a prediction?).
- **Sharpness-aware minimization (SAM)**.
- **Laplace approximation** for Bayesian neural networks.

## Why This Matters for AI

- **Backpropagation is reverse-mode autodiff over the Jacobian**. Understanding Jacobians = understanding backprop.
- **Loss landscape geometry**: Hessian eigenvalues explain why optimization is hard in high dimensions and why first-order methods work as well as they do.
- **Sharpness and generalization**: flatter minima (small Hessian eigenvalues) correlate with better generalization. This motivates SAM and other sharpness-aware optimizers.
- **Probability transformations**: the Jacobian determinant is essential for normalizing flows and any change-of-variables in continuous probability.

## Production Implications

- Most deep learning practitioners never compute Hessians directly — first-order methods are sufficient.
- For **second-order methods** (rare in deep learning, common in classical optimization), L-BFGS or Hessian-free Newton are the practical choices.
- **Influence functions** (for data debugging) require HVPs — tractable but expensive.
- **Sharpness-aware minimization (SAM)** can improve generalization at the cost of 2x forward passes per step.

## Common Pitfalls

- **Confusing Jacobian and Hessian** — Jacobian is for vector-output functions (first derivatives); Hessian is for scalar-output functions (second derivatives).
- **Forgetting that the Hessian is symmetric** — Clairaut's theorem says mixed partials are equal (under continuity). Hessian is always symmetric.
- **Trying to compute the full Hessian of a neural network** — infeasible past a few thousand parameters. Use HVPs or approximations.
- **Treating "Hessian eigenvalues" as a single number** — they're a spectrum, and the distribution matters.

## Further Reading

- Goodfellow et al., *Deep Learning*, Chapter 4 (Numerical Computation) for condition numbers and Newton's method.
- Nocedal & Wright, *Numerical Optimization* — for second-order methods.
- Pearlmutter (1994), *Fast Exact Multiplication by the Hessian* (HVP trick).

## The Jacobian in Probability (Change of Variables)

The Jacobian determinant is essential for transforming probability densities. If $\mathbf{Y} = \mathbf{f}(\mathbf{X})$ where $\mathbf{f}$ is invertible, then:

$$
p_{\mathbf{Y}}(\mathbf{y}) = p_{\mathbf{X}}(\mathbf{f}^{-1}(\mathbf{y})) \cdot \left| \det \mathbf{J}_{\mathbf{f}^{-1}}(\mathbf{y}) \right|
$$

This is the **change of variables formula**. It's why:
- **Normalizing flows** work: a simple Gaussian is transformed through a sequence of invertible functions; the log-likelihood includes the sum of log-Jacobian determinants.
- **VAEs** avoid the Jacobian: they use an encoder/decoder with a stochastic forward pass, sidestepping the change-of-variables by using the reparameterization trick instead.
- **Diffusion models** avoid the Jacobian: they model the score function $\nabla \log p(\mathbf{x})$ directly, not the density.

### Worked example: log-normal distribution
If $X \sim \mathcal{N}(\mu, \sigma^2)$ and $Y = e^X$, then $Y$ is log-normal. The transformation $f(x) = e^x$ has Jacobian determinant $e^x = y$. So:

$$
p_Y(y) = p_X(\log y) \cdot \frac{1}{y} = \frac{1}{y \sigma \sqrt{2\pi}} \exp\left(-\frac{(\log y - \mu)^2}{2\sigma^2}\right)
$$

This is the log-normal PDF. The $1/y$ factor is the Jacobian contribution.

## Hessian Eigenvalue Spectrum in Deep Learning

The Hessian eigenvalue spectrum reveals the geometry of the loss landscape:

### At a critical point ($\nabla f = 0$)
- All positive eigenvalues → local minimum.
- All negative → local maximum.
- Mixed signs → saddle point.
- Some zero → flat direction (degenerate).

### In high dimensions
For a $d$-dimensional parameter space, the number of possible eigenvalue sign patterns is $2^d$. Only one pattern (all positive) is a local minimum. So saddle points outnumber minima by $2^d - 1$ to 1. In deep learning ($d \sim 10^9$), local minima are vanishingly rare — almost all critical points are saddle points.

This resolved the mystery of why deep networks train well despite non-convex loss: gradient descent escapes saddle points efficiently (the gradient is non-zero in the direction of negative curvature), so saddle points don't trap training.

### Empirical Hessian spectra
Studies of real network Hessians (e.g., Ghorbani et al. 2019) find:
- A few large positive eigenvalues (steep directions).
- A bulk of small eigenvalues near 0 (flat directions).
- A few negative eigenvalues near critical points (saddle structure).

The "flat" directions are why neural networks can have many near-equivalent solutions — small Hessian eigenvalues mean the loss is insensitive to perturbations in those directions. This connects to generalization: flatter minima (smaller Hessian eigenvalues) generalize better.

## Condition Number and Optimization Difficulty

The condition number $\kappa = \lambda_{\max} / \lambda_{\min}$ measures how ill-conditioned the loss is. Geometrically, the level sets of $f$ are ellipsoids with axis ratios $\sqrt{\kappa}$.

### Effect on gradient descent
Gradient descent converges at rate $(1 - 1/\kappa)^t$ — for $\kappa = 1000$, it takes ~1000 steps to halve the distance to the minimum. The gradient points mostly toward the steep direction (large $\lambda$), but the minimum is in the flat direction (small $\lambda$) — gradient descent oscillates in the steep direction while slowly progressing in the flat direction.

### Why adaptive methods help
- **Momentum**: averages gradients, smoothing out oscillations in the steep direction.
- **Adam**: adapts per-dimension step size based on gradient variance — effectively normalizing the condition number.
- **Newton's method**: uses $\mathbf{H}^{-1}$ to perfectly correct for curvature — but infeasible at scale.

### Preconditioning
In classical optimization, **preconditioning** multiplies the gradient by a matrix $\mathbf{M}$ that approximates $\mathbf{H}^{-1}$, reducing the effective condition number. Adam is a diagonal preconditioner (using the diagonal of the empirical Hessian). K-FAC uses a block-diagonal approximation. Shampoo (Google 2022) uses a richer preconditioner.

## Hessian-Vector Products (Pearlmutter's Trick)

Computing the full Hessian is $O(n^2)$ storage and $O(n^2)$ compute — infeasible for $n > 10^4$. But we often only need **Hessian-vector products** $\mathbf{H}\mathbf{v}$, which can be computed in $O(n)$ via autodiff:

$$
\mathbf{H}\mathbf{v} = \nabla (\nabla f \cdot \mathbf{v})
$$

This is Pearlmutter's trick (1994). It works because:
1. Compute $\mathbf{g} = \nabla f$ (one backward pass).
2. Compute $\mathbf{g} \cdot \mathbf{v}$ (a scalar).
3. Compute $\nabla(\mathbf{g} \cdot \mathbf{v})$ (another backward pass) — this is $\mathbf{H}\mathbf{v}$.

Two backward passes give an exact HVP, no Hessian materialization needed.

### Applications of HVPs
- **Hessian-free Newton**: solve $\mathbf{H}\mathbf{p} = -\nabla f$ via conjugate gradient (using HVPs), avoiding $\mathbf{H}^{-1}$.
- **Influence functions**: $\mathbf{H}^{-1}\nabla f$ (via HVP + CG) tells you which training points most affect a prediction.
- **Sharpness-aware minimization (SAM)**: $\mathbf{H}\mathbf{v}$ for the SAM perturbation direction.
- **Laplace approximation**: $\mathbf{H}^{-1}$ approximates posterior covariance in Bayesian neural networks.
- **Hessian eigenvalue computation**: Lanczos iteration with HVPs gives extremal eigenvalues without materializing $\mathbf{H}$.

## Worked Example: Computing HVP in PyTorch

```python
import torch

def hvp(f, x, v):
    """Compute Hessian-vector product H @ v for f at x.
    H is the Hessian of f w.r.t. x. v is a vector with same shape as x.
    """
    # First backward: compute gradient
    grad = torch.autograd.grad(f, x, create_graph=True)[0]
    # Second backward: compute gradient of (grad . v)
    hv = torch.autograd.grad(grad, x, grad_outputs=v, create_graph=False)[0]
    return hv

# Example: f(x) = sum(x^4), H = diag(12 x^2)
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
f = (x ** 4).sum()
v = torch.tensor([1.0, 1.0, 1.0])

hv = hvp(f, x, v)
print(f"HVP: {hv}")  # Should be [12, 48, 108] = 12 * x^2 * v
# Verify: H = diag(12, 48, 108), H @ [1,1,1] = [12, 48, 108]
```

This is the foundation of all second-order methods in deep learning — exact HVPs via autodiff, no Hessian materialization.

## Why First-Order Methods Dominate Deep Learning

Despite Newton's method's quadratic convergence, first-order methods (SGD, Adam) dominate deep learning:

| Aspect                  | Newton's Method          | Adam (First-Order)       |
|-------------------------|--------------------------|--------------------------|
| Per-step cost           | $O(n^2)$ storage, $O(n^3)$ solve | $O(n)$ storage, $O(n)$ compute |
| Convergence rate        | Quadratic (when close)   | Linear (constant factor) |
| Saddle point handling   | Bad (can converge to saddles) | Good (gradient escape) |
| Mini-batch compatibility| Hard (stochastic Hessian) | Native (stochastic gradient) |
| Distributed training    | Hard (Hessian all-reduce) | Easy (gradient all-reduce) |
| Practical scale         | ~10K params              | ~100B+ params            |

The cost ratio is catastrophic: for a 1B-parameter model, Newton needs $10^{18}$ storage; Adam needs $10^9$. Adam is also more robust to saddle points and stochasticity. The practical conclusion: first-order methods scale; second-order methods don't.

## Connection to Other Concepts

- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — first-order foundation.
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — gradient descent, momentum.
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] — adaptive first-order method.
- [[02 - Mathematics/Linear Algebra/05 - Matrix Decomposition|Matrix Decomposition]] — eigendecomposition of Hessian.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — reverse-mode autodiff.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — Jacobian spectral radius.
- [[03 - Machine Learning/Generalization/01 - Bias Variance Tradeoff|Bias Variance Tradeoff]] — flat vs sharp minima.
- [[14 - Interpretability/Mechanistic/01 - Mechanistic Interpretability|Mechanistic Interpretability]] — loss landscape analysis.

## Interview Questions

1. **Q: What's the difference between the Jacobian and the Hessian?**
   A: The Jacobian is the matrix of first derivatives of a vector-valued function $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$ (shape $m \times n$). The Hessian is the matrix of second derivatives of a scalar function $f: \mathbb{R}^n \to \mathbb{R}$ (shape $n \times n$, symmetric). The Jacobian generalizes the gradient; the Hessian generalizes the second derivative.

2. **Q: Why are saddle points more common than local minima in deep networks?**
   A: In a $d$-dimensional parameter space, the Hessian at a critical point has $d$ eigenvalues, each with 2 possible signs. So $2^d$ sign patterns, but only 1 (all positive) is a local minimum. For $d = 10^9$, local minima are a $10^{-9 \log_{10} 2}$ fraction of critical points — vanishingly rare. Almost all critical points are saddle points. This is why deep networks train well despite non-convex loss: gradient descent escapes saddles efficiently.

3. **Q: How do you compute a Hessian-vector product without materializing the Hessian?**
   A: Pearlmutter's trick: $\mathbf{H}\mathbf{v} = \nabla(\nabla f \cdot \mathbf{v})$. Compute $\nabla f$ with one backward pass (with `create_graph=True`), compute the scalar $\nabla f \cdot \mathbf{v}$, then take the gradient of that scalar w.r.t. $\mathbf{x}$ — another backward pass. Two backward passes give an exact HVP in $O(n)$ time, no $O(n^2)$ Hessian storage.

4. **Q: Why isn't Newton's method used for deep learning?**
   A: Three reasons. (1) Storage: Hessian is $n \times n$ = $10^{18}$ for 1B params — infeasible. (2) Compute: solving $\mathbf{H}\mathbf{p} = -\nabla f$ is $O(n^3)$ — infeasible. (3) Saddle points: Newton can converge to saddles (it minimizes the quadratic approximation, which is maximized in negative-curvature directions). First-order methods (SGD, Adam) are $O(n)$ per step, handle saddles well, and scale to 100B+ parameters.

5. **Q: What does the condition number of the Hessian tell you about optimization?**
   A: $\kappa = \lambda_{\max} / \lambda_{\min}$ measures ill-conditioning. High $\kappa$ means the loss landscape is a long thin ellipsoid — gradient descent oscillates in the steep direction (large $\lambda$) while slowly progressing in the flat direction (small $\lambda$). Convergence rate is $(1 - 1/\kappa)^t$ — for $\kappa = 1000$, ~1000 steps to halve the distance. Adaptive methods (Adam) and preconditioning reduce the effective $\kappa$.

6. **Q: How does the Hessian connect to generalization?**
   A: Flatter minima (smaller Hessian eigenvalues) generalize better — the model is less sensitive to perturbations in parameter space, so it's less overfit to the training data. This motivates **sharpness-aware minimization (SAM)**: perturb parameters in the direction of largest Hessian eigenvalue before computing the gradient, encouraging convergence to flat minima. SAM improves generalization at the cost of 2× forward passes per step.

## See Also

- [[10 - Gradient and Chain Rule]]
- [[12 - Optimization Essentials]]
- [[13 - Adam Derivation]]
- [[04 - Neural Networks/Training/Backpropagation|Backpropagation]]
- [[02 - Mathematics/MOC|Mathematics MOC]]