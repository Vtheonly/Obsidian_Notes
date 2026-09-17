---
tags: [mathematics, probability, gaussian, normal]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Gaussian Distribution]
---

# 09 - The Gaussian Distribution

> [!info] TL;DR
> The Gaussian (normal) distribution is the most important distribution in ML and statistics. The Central Limit Theorem explains why noise is Gaussian; maximum entropy explains why we default to Gaussian assumptions; and closed-form conjugate priors make Bayesian inference tractable.

## Definition

The **univariate Gaussian** with mean $\mu$ and variance $\sigma^2$ has PDF:

$$
\mathcal{N}(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)
$$

The **multivariate Gaussian** in $d$ dimensions has PDF:

$$
\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma}) = \frac{1}{(2\pi)^{d/2} |\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)
$$

where $\boldsymbol{\mu} \in \mathbb{R}^d$ is the mean vector and $\boldsymbol{\Sigma} \in \mathbb{R}^{d \times d}$ is the (symmetric positive-definite) covariance matrix.

## Why Gaussians Are Everywhere

### 1. Central Limit Theorem

The sum of $n$ i.i.d. random variables (with finite mean and variance) converges to a Gaussian as $n \to \infty$, regardless of the original distribution.

This is why **noise is Gaussian** in many physical systems — it's the sum of many independent small perturbations. Measurement errors, thermal noise, gradient descent noise — all approximately Gaussian.

### 2. Maximum Entropy

Among all distributions with a given mean and variance, the Gaussian has the **maximum entropy**. So if you only know the mean and variance of a distribution, the Gaussian is the least-assuming choice — it doesn't introduce structure you didn't observe.

This makes Gaussians the "default" distribution when you have limited information. Many ML algorithms assume Gaussian noise not because they've verified it, but because it's the safest assumption.

### 3. Closed-Form Bayesian Inference

Gaussians are **conjugate** to themselves: if the prior and likelihood are both Gaussian, the posterior is also Gaussian, with closed-form mean and covariance. This makes Bayesian linear regression, Kalman filtering, and Gaussian processes all tractable.

### 4. Initialization

Neural network weights are typically initialized from a Gaussian:
- **Xavier (Glorot)**: $\mathcal{N}(0, 1/\text{fan\_in})$ — for tanh/sigmoid.
- **He (Kaiming)**: $\mathcal{N}(0, 2/\text{fan\_in})$ — for ReLU.
- These choices keep activations at a stable scale across layers. See [[04 - Neural Networks/Training/Initialization Schemes|Initialization Schemes]] (planned).

## Properties

### Affine transformation
If $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$, then $\mathbf{A}\mathbf{x} + \mathbf{b} \sim \mathcal{N}(\mathbf{A}\boldsymbol{\mu} + \mathbf{b}, \mathbf{A}\boldsymbol{\Sigma}\mathbf{A}^T)$.

This is essential for sampling: to sample from $\mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$, sample $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ and compute $\boldsymbol{\mu} + \mathbf{L}\mathbf{z}$ where $\mathbf{L}\mathbf{L}^T = \boldsymbol{\Sigma}$ (Cholesky decomposition).

### Marginal and conditional
Both marginals and conditionals of a multivariate Gaussian are Gaussian. Concretely, partition:

$$
\mathbf{x} = \begin{pmatrix} \mathbf{x}_1 \\ \mathbf{x}_2 \end{pmatrix}, \quad \boldsymbol{\mu} = \begin{pmatrix} \boldsymbol{\mu}_1 \\ \boldsymbol{\mu}_2 \end{pmatrix}, \quad \boldsymbol{\Sigma} = \begin{pmatrix} \boldsymbol{\Sigma}_{11} & \boldsymbol{\Sigma}_{12} \\ \boldsymbol{\Sigma}_{21} & \boldsymbol{\Sigma}_{22} \end{pmatrix}
$$

The marginal $P(\mathbf{x}_1) = \mathcal{N}(\boldsymbol{\mu}_1, \boldsymbol{\Sigma}_{11})$.

The conditional $P(\mathbf{x}_1 \mid \mathbf{x}_2) = \mathcal{N}(\boldsymbol{\mu}_{1|2}, \boldsymbol{\Sigma}_{1|2})$ where:

$$
\boldsymbol{\mu}_{1|2} = \boldsymbol{\mu}_1 + \boldsymbol{\Sigma}_{12} \boldsymbol{\Sigma}_{22}^{-1} (\mathbf{x}_2 - \boldsymbol{\mu}_2)
$$

$$
\boldsymbol{\Sigma}_{1|2} = \boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12} \boldsymbol{\Sigma}_{22}^{-1} \boldsymbol{\Sigma}_{21}
$$

These closed forms are the basis of Kalman filtering, Gaussian processes, and many other Bayesian methods.

### Product of Gaussians is Gaussian
(un-normalized) — useful for Bayesian updates.

### KL divergence between Gaussians

For two Gaussians $p = \mathcal{N}(\boldsymbol{\mu}_p, \boldsymbol{\Sigma}_p)$ and $q = \mathcal{N}(\boldsymbol{\mu}_q, \boldsymbol{\Sigma}_q)$:

$$
D_{KL}(p \| q) = \frac{1}{2} \left[ \log\frac{|\boldsymbol{\Sigma}_q|}{|\boldsymbol{\Sigma}_p|} - d + \text{tr}(\boldsymbol{\Sigma}_q^{-1} \boldsymbol{\Sigma}_p) + (\boldsymbol{\mu}_q - \boldsymbol{\mu}_p)^T \boldsymbol{\Sigma}_q^{-1} (\boldsymbol{\mu}_q - \boldsymbol{\mu}_p) \right]
$$

This is used in **VAEs** (variational autoencoders) where the KL between the approximate posterior and a standard Gaussian prior is part of the loss.

## Worked Example: Sampling

```python
import torch

# Univariate
x = torch.randn(1000)  # standard normal
y = 2.0 * x + 3.0      # N(3, 4)

# Multivariate
mu = torch.tensor([1.0, 2.0])
Sigma = torch.tensor([[1.0, 0.5], [0.5, 2.0]])
L = torch.linalg.cholesky(Sigma)
z = torch.randn(1000, 2)
samples = mu + z @ L.T  # 1000 samples from N(mu, Sigma)
```

## Gaussian vs. Heavy-Tailed Distributions

Gaussians have **thin tails** — the probability of $|x - \mu| > 5\sigma$ is ~$6 \times 10^{-7}$. Real-world data often has heavier tails:

- Financial returns (fat tails; crashes happen more often than Gaussian predicts).
- Word frequencies (Zipf / power-law).
- Network degrees (power-law).

For such data, **Student's t**, **Laplace**, or power-law distributions are better models. Using Gaussian assumptions on heavy-tailed data leads to systematic underestimation of extreme events.

## Why This Matters for AI

- **Initialization**: every neural network starts with Gaussian weights. The variance choice (Xavier, He) determines training stability.
- **Noise modeling**: diffusion models assume Gaussian noise at each step — that's why the math works out cleanly.
- **VAEs**: the encoder outputs a Gaussian over the latent space; the KL term is the Gaussian-Gaussian KL above.
- **Gaussian processes**: a Bayesian non-parametric model that uses Gaussian distributions over functions.
- **Mixed precision training**: gradients are roughly Gaussian (CLT), which is why techniques like gradient clipping work.

## Production Implications

- **Monitor for non-Gaussian behavior**: if your data is heavy-tailed, your models will systematically underpredict extreme events. Use robust loss functions (Huber) or heavy-tailed likelihoods.
- **Outlier detection**: Gaussian-based outlier detection (z-score) fails on heavy-tailed data. Use percentile-based methods instead.
- **Initialization matters**: wrong Gaussian variance at init can cause training to never converge. Always match init to the activation function.

## Common Pitfalls

- **Assuming Gaussian without checking** — many real distributions are heavy-tailed, bimodal, or skewed. Plot the data.
- **Using z-score outliers on heavy-tailed data** — flags too many points as outliers, or misses the real ones.
- **Forgetting that the multivariate Gaussian's covariance matrix must be positive-definite** — sampling will fail otherwise. Use Cholesky decomposition.
- **Numerical issues with $\boldsymbol{\Sigma}^{-1}$** — use the precision matrix or Cholesky-based formulations instead.

## Further Reading

- Bishop, *PRML*, Chapter 2 (Gaussian distribution deep dive).
- Wasserman, *All of Statistics*, Chapter 3.
- Murphy, *Probabilistic Machine Learning*, Chapter 3.

## Derivation of the Gaussian PDF (Why $e^{-x^2/2}$?)

The Gaussian PDF's form is not arbitrary — it falls out of three independent derivations:

### 1. Maximum entropy derivation
Among all distributions on $\mathbb{R}$ with mean $\mu$ and variance $\sigma^2$, the Gaussian maximizes differential entropy:

$$
h(p) = -\int p(x) \log p(x) \, dx
$$

subject to $\int p = 1$, $\int x p = \mu$, $\int (x-\mu)^2 p = \sigma^2$. Using Lagrange multipliers, the optimum is:

$$
p(x) \propto \exp\left(-\lambda_1 x - \lambda_2 (x-\mu)^2\right)
$$

which is the Gaussian form. So if you only know mean and variance, the Gaussian is the **least-assuming** (max-entropy) choice — it doesn't introduce structure you didn't observe.

### 2. CLT derivation
The sum of $n$ i.i.d. random variables (with finite mean $\mu$ and variance $\sigma^2$) converges in distribution to $\mathcal{N}(n\mu, n\sigma^2)$. The normalized sum $\frac{1}{\sqrt{n}} \sum (X_i - \mu)$ converges to $\mathcal{N}(0, \sigma^2)$. The proof uses characteristic functions and Lévy's continuity theorem.

### 3. Stable distribution derivation
A stable distribution is one where the sum of two independent copies (suitably scaled) has the same distribution. The Gaussian is the only stable distribution with finite variance. This is why measurement noise (sum of many small independent perturbations) is Gaussian.

## The Multivariate Gaussian in Detail

The multivariate Gaussian's PDF has three interpretations of the quadratic form $\mathcal{M}^2 = (\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})$:

1. **Mahalanobis distance squared** — the distance from $\mathbf{x}$ to $\boldsymbol{\mu}$, accounting for the covariance structure. Points with the same Mahalanobis distance lie on an ellipsoid.

2. **Negative log-likelihood (up to constants)** — $\log p(\mathbf{x}) = -\frac{1}{2}\mathcal{M}^2 + \text{const}$. Maximizing likelihood = minimizing Mahalanobis distance.

3. **Energy** — in physics-inspired formulations, $\mathcal{M}^2/2$ is the "energy" of $\mathbf{x}$; the Gaussian is the Boltzmann distribution at temperature 1.

### Geometry of the covariance matrix

The covariance matrix $\boldsymbol{\Sigma}$ has eigendecomposition $\boldsymbol{\Sigma} = \mathbf{V} \boldsymbol{\Lambda} \mathbf{V}^T$ where $\mathbf{V}$ are eigenvectors (principal axes) and $\boldsymbol{\Lambda}$ are eigenvalues (variances along each axis). The level sets of the Gaussian are ellipsoids with:
- Axes along the eigenvectors of $\boldsymbol{\Sigma}$.
- Axis lengths proportional to $\sqrt{\lambda_i}$ (standard deviations).

If $\boldsymbol{\Sigma} = \sigma^2 \mathbf{I}$ (isotropic), the ellipsoids are spheres — all directions have the same variance. Most ML assumes isotropic Gaussians for simplicity, but real data is often anisotropic.

### Conditional Gaussian (Detailed)

The conditional $P(\mathbf{x}_1 \mid \mathbf{x}_2)$ has mean $\boldsymbol{\mu}_{1|2} = \boldsymbol{\mu}_1 + \boldsymbol{\Sigma}_{12} \boldsymbol{\Sigma}_{22}^{-1} (\mathbf{x}_2 - \boldsymbol{\mu}_2)$ and covariance $\boldsymbol{\Sigma}_{1|2} = \boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12} \boldsymbol{\Sigma}_{22}^{-1} \boldsymbol{\Sigma}_{21}$.

Key insights:
- The conditional mean is a **linear function** of $\mathbf{x}_2$.
- The conditional covariance **does not depend on** $\mathbf{x}_2$ — it's the same for all observations.
- The conditional covariance is always smaller (in PSD order) than the marginal $\boldsymbol{\Sigma}_{11}$ — observing $\mathbf{x}_2$ always reduces uncertainty.

These properties make Gaussian conditioning the foundation of **Kalman filtering** (sequential Bayesian updating) and **Gaussian processes** (regression with uncertainty).

## Worked Example: Gaussian Process Regression

```python
import numpy as np
from scipy.linalg import cho_solve, cho_factor

def gp_posterior(X_train, y_train, X_test, kernel, noise_var=0.1):
    """Gaussian process posterior mean and covariance.
    kernel: function (x1, x2) -> scalar
    """
    n = len(X_train)
    m = len(X_test)

    # Compute covariance matrices
    K_xx = np.array([[kernel(x1, x2) for x2 in X_train] for x1 in X_train])
    K_xz = np.array([[kernel(x1, x2) for x2 in X_test] for x1 in X_train])
    K_zz = np.array([[kernel(x1, x2) for x2 in X_test] for x1 in X_test])

    # Add observation noise
    K_xx += noise_var * np.eye(n)

    # Posterior: P(f_test | X_train, y_train, X_test)
    # Mean: K_zx (K_xx + noise I)^-1 y_train
    # Cov:  K_zz - K_zx (K_xx + noise I)^-1 K_xz
    L = cho_factor(K_xx)
    alpha = cho_solve(L, y_train)              # K_xx^-1 y
    mean = K_xz.T @ alpha                      # (m,)
    v = cho_solve(L, K_xz)                     # K_xx^-1 K_xz
    cov = K_zz - K_xz.T @ v                    # (m, m)

    return mean, cov

# RBF kernel
def rbf(x1, x2, length=1.0, sigma=1.0):
    return sigma**2 * np.exp(-0.5 * ((x1 - x2) / length)**2)

# Usage
X_train = np.array([1.0, 2.0, 3.0, 5.0])
y_train = np.array([1.2, 0.9, 1.5, 2.1])
X_test = np.linspace(0, 6, 50)
mean, cov = gp_posterior(X_train, y_train, X_test, rbf)
```

This is the foundation of Gaussian process regression — a Bayesian non-parametric model that uses the multivariate Gaussian's conditioning properties. The posterior mean is the prediction; the posterior covariance gives uncertainty estimates.

## Gaussians in Modern AI (Detailed)

### Diffusion models
Diffusion models (DDPM, score-based) are built on Gaussian noise:
- **Forward process**: $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \boldsymbol{\epsilon}$, where $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$.
- **Reverse process**: denoising step is also Gaussian: $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}(\boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t))$.
- The Gaussian assumption makes the math tractable (closed-form KL divergences, score functions).

### Variational Autoencoders (VAEs)
VAEs use Gaussians in three places:
1. **Prior**: $p(\mathbf{z}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$ — standard Gaussian prior on the latent.
2. **Approximate posterior**: $q_\phi(\mathbf{z} \mid \mathbf{x}) = \mathcal{N}(\boldsymbol{\mu}_\phi(\mathbf{x}), \text{diag}(\boldsymbol{\sigma}_\phi^2(\mathbf{x})))$ — Gaussian encoder.
3. **KL term**: $D_{KL}(q \| p) = \frac{1}{2} \sum_i (\mu_i^2 + \sigma_i^2 - \log \sigma_i^2 - 1)$ — closed-form Gaussian-Gaussian KL.

### Initialization
Neural network weights are initialized from Gaussians (Xavier, He). The variance choice determines activation stability across layers. See [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]].

### Gradient noise
SGD gradients are approximately Gaussian (CLT) — the sum of many independent per-example gradients. This is why:
- **Gradient clipping** works — large gradients are outliers in a Gaussian distribution.
- **Momentum** works — averaging gradients reduces variance ($\sigma/\sqrt{n}$).
- **Adam** works — it adapts per-parameter based on gradient mean and variance.

### Mixed precision training
The Gaussian assumption justifies FP16/BF16 training:
- Gradients are roughly Gaussian $\Rightarrow$ most values cluster near 0.
- FP16 has high density near 0 (denormals) $\Rightarrow$ good representation of typical gradients.
- Loss scaling handles the rare large gradients (outliers).

### Quantization
INT8/INT4 quantization assumes activations are roughly Gaussian:
- Symmetric quantization ranges are $[-k\sigma, k\sigma]$ for $k \approx 3$ (3-sigma rule).
- Outliers (large activations) are clipped — rare for Gaussian, common for heavy-tailed.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Outlier detection flags too many points | Data is heavy-tailed, not Gaussian | Use percentile-based or robust methods (IQR, MAD) |
| VAE generates blurry samples | Gaussian likelihood too restrictive | Use Gaussian mixture or discrete latents; increase latent dim |
| GP regression overconfident | Noise variance too small | Increase `noise_var`; check kernel hyperparameters |
| Diffusion training unstable | Noise schedule wrong | Use cosine schedule; check $\bar{\alpha}_t$ monotonicity |
| Mixed precision NaNs | Gradient overflow | Use gradient scaling; switch to BF16 (wider range) |
| Cholesky fails on covariance | Matrix not positive-definite | Add jitter ($10^{-6} \mathbf{I}$); use eigendecomposition |

## Connection to Other Concepts

- [[02 - Mathematics/Probability/07 - Probability Essentials|Probability Essentials]] — foundational concepts.
- [[02 - Mathematics/Probability/08 - Bayes Theorem Deep Dive|Bayes Theorem]] — Gaussian conjugate priors.
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy/Cross-Entropy/KL]] — KL divergence between Gaussians.
- [[02 - Mathematics/Statistics/16 - Estimators and Bias|Estimators and Bias]] — Gaussian MLE.
- [[02 - Mathematics/Statistics/17 - Hypothesis Testing|Hypothesis Testing]] — z-tests, t-tests assume Gaussian.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — Xavier/He init use Gaussians.
- [[04 - Neural Networks/Training/08 - Vanishing and Exploding Gradients|Vanishing/Exploding Gradients]] — bad init variance causes this.
- [[23 - Multimodal AI/Diffusion/05 - DiT and FLUX|DiT/FLUX]] — diffusion models are built on Gaussian noise.
- [[11 - Training/Optimization/04 - Mixed Precision Training|Mixed Precision Training]] — Gaussian gradient assumption.
- [[13 - Inference/Quantization/03 - Quantization|Quantization]] — Gaussian activation assumption.

## Interview Questions

1. **Q: Why is the Gaussian distribution so common in ML and statistics?**
   A: Three reasons. (1) Central Limit Theorem: sums of independent random variables converge to Gaussian, so noise (sum of many perturbations) is Gaussian. (2) Maximum entropy: among distributions with given mean and variance, Gaussian is the least-assuming (maximizes entropy) — the safest default when you only know mean and variance. (3) Mathematical tractability: conjugate priors, closed-form conditionals, closed-form KL — Bayesian inference is computationally feasible with Gaussians.

2. **Q: Derive the Gaussian PDF from the maximum entropy principle.**
   A: Maximize $h(p) = -\int p \log p$ subject to $\int p = 1$, $\int x p = \mu$, $\int (x-\mu)^2 p = \sigma^2$. Lagrangian: $\mathcal{L} = -p \log p + \lambda_0 p + \lambda_1 x p + \lambda_2 (x-\mu)^2 p$. Take functional derivative wrt $p$: $-(\log p + 1) + \lambda_0 + \lambda_1 x + \lambda_2 (x-\mu)^2 = 0$. Solve: $p(x) \propto \exp(\lambda_1 x + \lambda_2 (x-\mu)^2)$. Apply constraints to determine $\lambda_1, \lambda_2$ — get the Gaussian form.

3. **Q: What is the Mahalanobis distance, and why does it matter?**
   A: $\mathcal{M}^2 = (\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})$ — the distance from $\mathbf{x}$ to $\boldsymbol{\mu}$ accounting for covariance. It's the negative log-likelihood (up to constants), so maximizing likelihood = minimizing Mahalanobis distance. Points with the same Mahalanobis distance lie on an ellipsoid (the level sets of the Gaussian). It's the "right" distance metric for Gaussian-distributed data — Euclidean distance ignores covariance.

4. **Q: How are Gaussians used in diffusion models?**
   A: Three ways. (1) Forward process adds Gaussian noise: $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t} \boldsymbol{\epsilon}$, $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$. (2) Reverse process denoising step is Gaussian: $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}(\boldsymbol{\mu}_\theta, \boldsymbol{\Sigma}_\theta)$. (3) The training loss (predict noise) is the MSE between predicted and actual Gaussian noise. The Gaussian assumption makes the math tractable — closed-form KL divergences, score functions, and reverse process.

5. **Q: Why do VAEs use Gaussian latents, and what's the KL term?**
   A: Three reasons for Gaussian latents: (1) prior is standard Gaussian $\mathcal{N}(\mathbf{0}, \mathbf{I})$, (2) encoder outputs Gaussian $q_\phi(\mathbf{z} \mid \mathbf{x}) = \mathcal{N}(\boldsymbol{\mu}, \text{diag}(\boldsymbol{\sigma}^2))$, (3) the KL between two Gaussians has closed form: $D_{KL} = \frac{1}{2} \sum_i (\mu_i^2 + \sigma_i^2 - \log \sigma_i^2 - 1)$. This KL term regularizes the latent space toward the prior — without it, the encoder could collapse to a delta function (no information).

6. **Q: When does the Gaussian assumption fail, and what are the consequences?**
   A: Fails for heavy-tailed data (financial returns, word frequencies, network degrees) and multimodal data (mixtures). Consequences: (1) outlier detection (z-score) flags too many points or misses real outliers, (2) confidence intervals too narrow — extreme events underestimated, (3) models fit to Gaussian assumptions are overconfident. Fixes: use Student's t or Laplace for heavy tails, Gaussian mixtures for multimodal, or non-parametric methods.

## See Also

- [[07 - Probability Essentials]]
- [[08 - Bayes Theorem Deep Dive]]
- [[15 - Entropy Cross-Entropy KL]]
- [[02 - Mathematics/MOC|Mathematics MOC]]