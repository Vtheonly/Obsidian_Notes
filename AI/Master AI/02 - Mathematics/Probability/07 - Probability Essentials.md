---
tags: [mathematics, probability, distributions, bayes]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Probability Essentials]
---

# Probability Essentials

> [!info] TL;DR
> Probability theory is the language of machine learning. Language modeling is probability estimation; classification is computing conditional probabilities; training is maximum likelihood; regularization is often a prior. This note covers the essentials: distributions, Bayes' theorem, expectation/variance, and the Gaussian distribution.

## Why Probability for AI

Machine learning is fundamentally about **making predictions under uncertainty**. Probability theory gives us the tools to:

- **Quantify uncertainty** — what's the probability that this email is spam?
- **Update beliefs given evidence** — given this new email, how should I update my belief that the user is on vacation?
- **Define learning objectives** — maximum likelihood, MAP, Bayesian inference.
- **Model distributions** — language models are probability distributions over sequences.

## Probability Distributions

A **probability distribution** assigns a probability to each possible outcome, such that probabilities are non-negative and sum (or integrate) to 1.

### Discrete distributions

For a discrete random variable $X$ taking values $\{x_1, x_2, \ldots\}$, the probability mass function (PMF) is $P(X = x_i) = p_i$, with $p_i \geq 0$ and $\sum p_i = 1$.

Examples:
- **Bernoulli** ($p$) — coin flip, $X \in \{0, 1\}$.
- **Categorical** ($p_1, \ldots, p_K$) — K-sided die. **This is what softmax produces.**
- **Binomial** ($n, p$) — number of heads in $n$ flips.

### Continuous distributions

For a continuous random variable $X$, the probability density function (PDF) is $p(x)$, with $p(x) \geq 0$ and $\int p(x) dx = 1$. Probabilities of intervals are integrals: $P(a \leq X \leq b) = \int_a^b p(x) dx$.

Examples:
- **Uniform** on $[a, b]$
- **Gaussian** (see below)
- **Exponential**

## Conditional Probability and Bayes' Theorem

The **conditional probability** of $A$ given $B$ is:

$$
P(A \mid B) = \frac{P(A, B)}{P(B)}
$$

Rearranged, this gives **Bayes' theorem**:

$$
P(A \mid B) = \frac{P(B \mid A) \, P(A)}{P(B)}
$$

In the Bayesian-interpretation form:

$$
\text{posterior} = \frac{\text{likelihood} \times \text{prior}}{\text{evidence}}
$$

Bayes' theorem is the foundation of:
- **Bayesian inference** — update beliefs about model parameters given data.
- **Naive Bayes classifiers** — $P(\text{class} \mid \text{features}) \propto P(\text{features} \mid \text{class}) P(\text{class})$.
- **Generative models** — model $P(\text{data})$ directly rather than $P(\text{label} \mid \text{data})$.

## Expectation, Variance, Covariance

The **expected value** of $X$ is:

$$
\mathbb{E}[X] = \sum_i x_i P(X = x_i) \quad \text{(discrete)}
$$

$$
\mathbb{E}[X] = \int x \, p(x) \, dx \quad \text{(continuous)}
$$

The **variance** measures spread:

$$
\text{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2
$$

The **standard deviation** is $\sigma = \sqrt{\text{Var}(X)}$.

The **covariance** of two random variables measures how they vary together:

$$
\text{Cov}(X, Y) = \mathbb{E}[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])]
$$

The **correlation** is normalized covariance:

$$
\rho(X, Y) = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1]
$$

Covariance matrices are central to PCA, Gaussian distributions, and many ML algorithms.

## The Gaussian Distribution

The **(univariate) Gaussian** (normal) distribution has PDF:

$$
\mathcal{N}(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)
$$

The **multivariate Gaussian** in $d$ dimensions has PDF:

$$
\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma}) = \frac{1}{(2\pi)^{d/2} |\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)
$$

where $\boldsymbol{\mu}$ is the mean vector and $\boldsymbol{\Sigma}$ is the covariance matrix.

### Why Gaussians are everywhere

- **Central Limit Theorem** — the sum of many independent random variables is approximately Gaussian, regardless of their original distribution. This is why noise is often modeled as Gaussian.
- **Maximum entropy** — the Gaussian is the maximum-entropy distribution with a given mean and variance. So if you only know the mean and variance, the Gaussian is the least-assuming choice.
- **Closed-form operations** — marginals and conditionals of Gaussians are Gaussian. Kalman filters, Gaussian processes, and many Bayesian models rely on this.
- **Initialization** — neural network weights are typically initialized from a Gaussian (e.g., Xavier: $\mathcal{N}(0, 1/n)$, He: $\mathcal{N}(0, 2/n)$).

## Maximum Likelihood Estimation

The most common training objective in ML is **maximum likelihood**:

$$
\hat{\boldsymbol{\theta}} = \arg\max_{\boldsymbol{\theta}} P(\text{data} \mid \boldsymbol{\theta})
$$

For i.i.d. data $\{x_1, \ldots, x_N\}$:

$$
P(\text{data} \mid \boldsymbol{\theta}) = \prod_{i=1}^{N} P(x_i \mid \boldsymbol{\theta})
$$

Taking logs (for numerical stability and to turn products into sums):

$$
\log P(\text{data} \mid \boldsymbol{\theta}) = \sum_{i=1}^{N} \log P(x_i \mid \boldsymbol{\theta})
$$

Equivalently, minimize the **negative log-likelihood (NLL)**:

$$
\mathcal{L}(\boldsymbol{\theta}) = -\sum_{i=1}^{N} \log P(x_i \mid \boldsymbol{\theta})
$$

### MLE for classification = cross-entropy loss

For categorical outputs with predicted probabilities $\hat{p}_i$ and true one-hot labels $y_i$:

$$
\mathcal{L} = -\sum_i y_i \log \hat{p}_i
$$

This is exactly **cross-entropy loss**. See [[Entropy Cross-Entropy KL]].

### MLE for regression = MSE loss

For Gaussian noise with fixed variance, MLE of the mean gives the mean-squared error loss. So training a network with MSE is implicitly assuming Gaussian residuals.

## MAP and Bayesian Inference

**Maximum A Posteriori (MAP)** adds a prior:

$$
\hat{\boldsymbol{\theta}}_{\text{MAP}} = \arg\max_{\boldsymbol{\theta}} P(\text{data} \mid \boldsymbol{\theta}) P(\boldsymbol{\theta})
$$

- L2 regularization corresponds to a Gaussian prior on weights.
- L1 regularization corresponds to a Laplace prior on weights (induces sparsity).

**Full Bayesian inference** doesn't pick a single $\hat{\boldsymbol{\theta}}$ — it maintains the full posterior $P(\boldsymbol{\theta} \mid \text{data})$ and averages predictions over it. This is more accurate but usually computationally intractable; approximations include variational inference and MCMC.

## Sampling

To estimate expectations under a distribution, we use **Monte Carlo sampling**:

$$
\mathbb{E}_{x \sim p}[f(x)] \approx \frac{1}{N} \sum_{i=1}^{N} f(x_i), \quad x_i \sim p
$$

This is how we estimate gradients in stochastic gradient descent (SGD), how LLMs generate text (sampling tokens from softmax), and how RL estimators work.

## Common Pitfalls

- **Confusing PDF with probability** — for continuous distributions, $p(x)$ is a density, not a probability. It can be greater than 1.
- **Forgetting the normalizer** — when defining a distribution, you must ensure probabilities sum (or integrate) to 1. This is what softmax does for the categorical distribution.
- **Assuming independence** — many ML mistakes come from assuming samples are i.i.d. when they aren't (e.g., correlated training data).
- **Ignoring the prior in MAP** — the choice of prior matters, especially with limited data.

## Production Implications

- **Calibration**: a model's predicted probabilities should match empirical frequencies. Modern neural networks are often poorly calibrated — see [[03 - Machine Learning/Evaluation/05 - ML Evaluation Metrics|Evaluation]] (planned).
- **Temperature scaling**: post-hoc calibration by dividing logits by a learned temperature. Cheap and effective.
- **Bayesian deep learning**: marginalizing over the posterior gives uncertainty estimates; useful for high-stakes applications but expensive.

## Further Reading

- Wasserman, *All of Statistics* — concise reference.
- Bishop, *Pattern Recognition and Machine Learning* — Chapter 1–2.
- Murphy, *Probabilistic Machine Learning* — modern treatment.

## See Also

- [[Entropy Cross-Entropy KL]]
- [[Gradient and Chain Rule]]
- [[Optimization Essentials]]
- [[02 - Mathematics/MOC|Mathematics MOC]]
- [[05 - NLP Fundamentals/Language Modeling/Perplexity|Perplexity]] (planned)

## The Cramér-Rao Lower Bound and Fisher Information

For an unbiased estimator $\hat{\theta}$ of parameter $\theta$ with likelihood $p(x \mid \theta)$, the **Fisher information** measures how much information an observable random variable $X$ carries about $\theta$:

$$
I(\theta) = \mathbb{E}\left[ \left( \frac{\partial}{\partial \theta} \log p(X \mid \theta) \right)^2 \right] = -\mathbb{E}\left[ \frac{\partial^2}{\partial \theta^2} \log p(X \mid \theta) \right]
$$

The **Cramér-Rao lower bound** states that the variance of any unbiased estimator is bounded below by the inverse Fisher information:

$$
\text{Var}(\hat{\theta}) \geq \frac{1}{I(\theta)}
$$

This is the theoretical floor — no unbiased estimator can do better. MLE achieves this bound asymptotically as $n \to \infty$, which is why MLE is the asymptotically efficient default. In practice, with finite data, regularized estimators (MAP) often beat MLE because they trade a small bias for a large variance reduction.

### Connection to the Hessian

The Fisher information matrix is the expected Hessian of the negative log-likelihood. This is why the Hessian is so important in optimization: it tells you the local curvature of the loss, which determines the optimal step size and how much you can trust the gradient. Newton's method uses the Hessian directly; gradient descent implicitly assumes it's identity (isotropic); Adam approximates it with a diagonal of squared gradients. See [[11 - Jacobians and Hessians]] for the full treatment.

## Conjugate Priors — Practical Bayesian Computation

A **conjugate prior** is a prior distribution that, when combined with a particular likelihood, yields a posterior in the same family. This makes Bayesian inference tractable — you don't need numerical integration.

| Likelihood              | Conjugate prior          | Posterior                | Use case                            |
|-------------------------|--------------------------|--------------------------|-------------------------------------|
| Bernoulli / Binomial    | Beta$(\alpha, \beta)$    | Beta$(\alpha + k, \beta + n - k)$ | Click-through rates, conversion   |
| Categorical / Multinomial | Dirichlet              | Dirichlet               | Topic models, token distributions   |
| Gaussian (known var)    | Gaussian                | Gaussian                 | Mean estimation                     |
| Gaussian (unknown var)  | Inverse-Gamma           | Inverse-Gamma            | Variance estimation                 |
| Poisson                 | Gamma                   | Gamma                    | Event count rates                   |
| Exponential             | Gamma                   | Gamma                    | Time-to-event rates                 |

### Beta-Bernoulli example (the canonical case)

You observe $k$ clicks out of $n$ impressions. You want to estimate the click-through rate $\theta$. With a Beta$(\alpha, \beta)$ prior (e.g., $\alpha = \beta = 1$ for uniform, or $\alpha = \beta = 10$ for a prior centered at 0.5), the posterior is:

$$
\theta \mid \text{data} \sim \text{Beta}(\alpha + k, \beta + n - k)
$$

The posterior mean is $\frac{\alpha + k}{\alpha + \beta + n}$ — a weighted average of the prior mean and the empirical click rate. With $n$ large, the data dominates; with $n$ small, the prior dominates. This is exactly the right behavior for cold-start recommendation: don't trust a single click; trust a thousand.

```python
import numpy as np
from scipy import stats

# Beta-Bernoulli Bayesian update
prior_alpha, prior_beta = 1, 1  # Uniform prior
k_clicks = 7
n_impressions = 100

posterior = stats.beta(prior_alpha + k_clicks, prior_beta + n_impressions - k_clicks)
print(f"Posterior mean: {posterior.mean():.4f}")  # ~0.079
print(f"95% credible interval: {posterior.interval(0.95)}")  # ~(0.035, 0.140)

# Compare with MLE: 7/100 = 0.07. The Bayesian estimate is slightly higher (prior influence).
# The credible interval quantifies uncertainty — MLE gives only a point estimate.
```

### Why this matters for production A/B testing

In an A/B test with $n=1000$ users per arm and a 5% conversion rate, you observe 50 vs. 55 conversions. Is B really better? The Bayesian Beta-Binomial model gives you a posterior over the difference $\theta_B - \theta_A$. You can compute $P(\theta_B > \theta_A \mid \text{data})$ directly — much more interpretable than a p-value. Most modern A/B testing platforms (Optimizely, Statsig) use this approach.

## Monte Carlo Methods and Variance Reduction

Monte Carlo estimates $\mathbb{E}_{x \sim p}[f(x)] \approx \frac{1}{N} \sum_{i=1}^N f(x_i)$ with $x_i \sim p$. The standard error is $\sigma / \sqrt{N}$. Three variance reduction techniques are essential for ML:

### 1. Importance sampling

Sample from a proposal distribution $q$ instead of $p$, reweighting:

$$
\mathbb{E}_{x \sim p}[f(x)] = \mathbb{E}_{x \sim q}\left[ f(x) \frac{p(x)}{q(x)} \right] \approx \frac{1}{N} \sum_{i=1}^N f(x_i) \frac{p(x_i)}{q(x_i)}, \quad x_i \sim q
$$

Choose $q$ to oversample regions where $f$ is large (high-loss examples, rare events). Used in off-policy reinforcement learning, rare event simulation, and active learning.

### 2. Control variates

If you know the expectation $\mu_g$ of a correlated function $g$, you can reduce variance:

$$
\hat{\mu}_f = \frac{1}{N} \sum_{i=1}^N \left[ f(x_i) - c (g(x_i) - \mu_g) \right]
$$

Choose $c = \text{Cov}(f, g) / \text{Var}(g)$. The estimator is unbiased with variance reduced by factor $1 - \rho^2$ where $\rho$ is the correlation.

### 3. Common random numbers

When comparing two systems (e.g., two model variants), use the same random seed for both. The variance of the difference $\hat{\mu}_A - \hat{\mu}_B$ is $\text{Var}(\hat{\mu}_A) + \text{Var}(\hat{\mu}_B) - 2 \text{Cov}(\hat{\mu}_A, \hat{\mu}_B)$. Positive covariance (from shared random numbers) reduces the variance of the difference, making comparisons more sensitive.

```python
import torch

# Importance sampling for off-policy evaluation
def estimate_value_off_policy(trajectories, behavior_policy_probs, target_policy_probs, rewards):
    """Estimate value of target_policy using data from behavior_policy."""
    # Importance weights: p_target / p_behavior
    weights = target_policy_probs / behavior_policy_probs
    # Weighted return estimator
    weighted_returns = weights * rewards
    return weighted_returns.mean(), weighted_returns.std() / (len(rewards) ** 0.5)

# Off-policy evaluation example
n = 1000
behavior_probs = torch.rand(n) * 0.5 + 0.25  # Uniform [0.25, 0.75]
target_probs = torch.rand(n) * 0.3 + 0.1      # Uniform [0.1, 0.4]
rewards = torch.randn(n) * 2 + 1  # Some reward signal

mean, stderr = estimate_value_off_policy(None, behavior_probs, target_probs, rewards)
print(f"Estimated value: {mean:.4f} ± {stderr:.4f}")
```

## Probability in Modern AI: A Survey of Connections

### In language modeling

A language model is a probability distribution over token sequences. The chain rule decomposes the joint:

$$
P(w_1, \ldots, w_T) = \prod_{t=1}^T P(w_t \mid w_1, \ldots, w_{t-1})
$$

Training minimizes the cross-entropy (negative log-likelihood). Perplexity is $2^{H}$ where $H$ is cross-entropy — it's the effective vocabulary size, the number of choices the model is uncertain about at each step. Lower perplexity = better model. See [[08 - Perplexity]].

### In RLHF and DPO

RLHF trains a reward model $r_\phi(x, y)$ to predict human preferences. The Bradley-Terry model converts rewards to probabilities:

$$
P(y_w \succ y_l \mid x) = \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))
$$

where $\sigma$ is sigmoid. Training maximizes the log-likelihood of observed preferences. DPO derives a closed-form solution to the RLHF objective by eliminating the reward model, expressing the policy directly in terms of preference probabilities. See [[09 - DPO 2023]] and [[05 - RLHF with PPO]].

### In quantization

INT8 quantization maps fp32 weights $w \in [a, b]$ to integers $q \in [-128, 127]$. The scale $s = (b - a) / 255$ and zero point $z = \text{round}(-a / s)$. The mapping is $q = \text{round}(w / s) + z$. The probability distribution of weights matters: a heavy-tailed distribution needs more scale headroom; a uniform distribution quantizes nearly losslessly. See [[03 - Quantization]].

### In calibration

A well-calibrated classifier's predicted probabilities match empirical frequencies: of all examples predicted with 80% confidence, 80% should be correct. Modern neural networks are poorly calibrated — they're overconfident. **Temperature scaling** divides logits by $T > 1$ to soften predictions. Find $T$ by minimizing NLL on a validation set. This is a cheap, post-hoc fix that dramatically improves calibration without retraining. See [[05 - ML Evaluation Metrics]].

### In Bayesian optimization

Bayesian optimization uses a Gaussian process surrogate to model the objective function $f(x)$. At each step, it computes the posterior over $f$, then uses an acquisition function (e.g., expected improvement, upper confidence bound) to choose the next point. The probability calculus is what makes this efficient — you can quantify uncertainty about $f$ at untested points, balancing exploration vs. exploitation.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|--------|--------------|-----|
| Probabilities don't sum to 1 | Forgetting to normalize; or numerical underflow | Use log-space; subtract log-sum-exp |
| NaN in cross-entropy | log(0) when predicted probability is 0 | Add small epsilon: `log(p + 1e-10)`; or use `F.cross_entropy` which handles it |
| Variance blows up in Monte Carlo | High-variance estimator, insufficient samples | Use importance sampling with a better proposal; or control variates |
| Calibration is poor (overconfident) | Modern neural nets are overconfident | Apply temperature scaling on a validation set |
| A/B test gives inconsistent results | Multiple comparisons, peeking, optional stopping | Pre-register; use sequential testing; correct for multiple comparisons |
| Reward model overfits preferences | Small dataset, high-capacity model | Use Bayesian model; regularize; ensemble |

## Connection to Other Concepts

- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy, Cross-Entropy, KL]] — entropy measures uncertainty; cross-entropy is the NLL; KL measures distribution divergence.
- [[02 - Mathematics/Calculus/10 - Gradient and Chain Rule|Gradient and Chain Rule]] — gradients of expected values require the score function or reparameterization trick.
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization Essentials]] — MLE minimizes NLL; gradient descent finds the MLE.
- [[02 - Mathematics/Statistics/16 - Estimators and Bias|Estimators and Bias]] — MLE / MAP / Bayesian inference formalized.
- [[02 - Mathematics/Statistics/17 - Hypothesis Testing|Hypothesis Testing]] — p-values, confidence intervals, A/B testing.
- [[02 - Mathematics/Probability/09 - Gaussian Distribution|Gaussian Distribution]] — the most important continuous distribution.
- [[02 - Mathematics/Probability/08 - Bayes Theorem Deep Dive|Bayes Theorem Deep Dive]] — Bayesian inference formalized.
- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining Objectives]] — language modeling is MLE on token sequences.
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF with PPO]] — Bradley-Terry model for preference learning.
- [[12 - Fine-Tuning/DPO/04 - DPO Derivation|DPO Derivation]] — closed-form solution to RLHF via probability ratios.
- [[03 - Machine Learning/Evaluation/05 - ML Evaluation Metrics|ML Evaluation Metrics]] — calibration, NLL, Brier score.
- [[21 - LLMOps and MLOps/Evaluation/04 - LLM-as-Judge Evaluation|LLM-as-Judge Evaluation]] — LLM judges produce probability-like scores.
- [[21 - LLMOps and MLOps/Deployment/07 - A-B Testing and Shadow Deployment|A/B Testing]] — Bayesian A/B testing uses Beta-Bernoulli.

## Interview Questions

1. **Q: What is the difference between MLE and MAP? When would you use each?**
   A: MLE finds $\hat{\theta} = \arg\max_\theta P(\text{data} \mid \theta)$ — the parameters that make the data most likely. MAP finds $\hat{\theta} = \arg\max_\theta P(\theta \mid \text{data}) = \arg\max_\theta P(\text{data} \mid \theta) P(\theta)$ — adding a prior. MLE is a special case of MAP with a uniform prior. Use MLE when you have lots of data (the prior is dominated) or when you have no prior knowledge. Use MAP when data is limited (the prior regularizes and prevents overfitting) or when you have genuine prior knowledge (e.g., weights should be small — Gaussian prior = L2 regularization). For LLMs: pretraining uses MLE (cross-entropy loss = NLL); fine-tuning with weight decay uses MAP (Gaussian prior). See [[16 - Estimators and Bias]].

2. **Q: Explain the chain rule of probability and why it matters for language modeling.**
   A: The chain rule decomposes a joint distribution: $P(w_1, \ldots, w_T) = \prod_{t=1}^T P(w_t \mid w_1, \ldots, w_{t-1})$. For language models, this means a sequence probability is the product of per-token conditional probabilities. Training minimizes the negative log of this product — the cross-entropy loss. This is why LLM training is exactly MLE: we maximize the probability the model assigns to the observed token sequences. The chain rule also explains why LLMs are autoregressive — each token depends on all previous tokens, and you generate by sampling one token at a time.

3. **Q: How does the Beta-Bernoulli conjugate prior work, and why is it useful for A/B testing?**
   A: The Beta distribution is conjugate to the Bernoulli likelihood: if you observe $k$ successes out of $n$ trials with a Beta$(\alpha, \beta)$ prior, the posterior is Beta$(\alpha + k, \beta + n - k)$. This is closed-form — no numerical integration needed. For A/B testing, you compute the posterior over each arm's conversion rate, then directly compute $P(\theta_B > \theta_A \mid \text{data})$. This is more interpretable than a p-value: instead of "reject the null at $\alpha = 0.05$", you say "there's an 87% probability that B is better than A." Most modern A/B testing platforms (Optimizely, Statsig) use this approach.

4. **Q: What is the Fisher information and why does it matter for optimization?**
   A: The Fisher information $I(\theta)$ measures how much information observable data carries about parameter $\theta$. It equals the expected Hessian of the negative log-likelihood. The Cramér-Rao lower bound states $\text{Var}(\hat{\theta}) \geq 1/I(\theta)$ — no unbiased estimator beats this. In optimization, the Fisher information is the curvature of the loss landscape. Newton's method uses the Hessian directly (and thus the Fisher); gradient descent implicitly assumes it's identity (isotropic); Adam approximates it with the diagonal of squared gradients. This is why Adam adapts to ill-conditioned problems — it's approximating the local curvature.

5. **Q: Why are modern neural networks poorly calibrated, and how do you fix it?**
   A: Modern nets are overconfident — of examples predicted with 90% confidence, only ~70% are correct. This happens because cross-entropy loss pushes probabilities to extremes (the gradient is largest near 0 and 1), and modern nets have enough capacity to memorize the training set, achieving near-zero training loss. The cheap fix is **temperature scaling**: divide the logits by $T > 1$ (found by minimizing NLL on a validation set). This softens predictions without changing the ranking (so accuracy is unchanged) but dramatically improves calibration. More expensive fixes: ensemble methods, Bayesian neural networks, or focal loss during training.

6. **Q: How does probability theory underpin RLHF and DPO?**
   A: In RLHF, a reward model $r_\phi(x, y)$ predicts human preferences. The Bradley-Terry model converts rewards to preference probabilities: $P(y_w \succ y_l \mid x) = \sigma(r(x, y_w) - r(x, y_l))$. Training the reward model is MLE on this likelihood. PPO then optimizes the policy to maximize the reward subject to a KL constraint to a reference policy. DPO (Direct Preference Optimization) derives a closed-form solution by eliminating the reward model: the optimal policy is $\pi^*(y \mid x) \propto \pi_{\text{ref}}(y \mid x) \exp(r(x, y) / \beta)$. Substituting into the Bradley-Terry formula gives a loss directly in terms of policies — no reward model needed. This is a beautiful example of probability theory (specifically, the exponential family and convex duality) leading to a simpler algorithm.

## See Also

- [[Entropy Cross-Entropy KL]]
- [[Gradient and Chain Rule]]
- [[Optimization Essentials]]
- [[Estimators and Bias]]
- [[Hypothesis Testing]]
- [[Gaussian Distribution]]
- [[Bayes Theorem Deep Dive]]
- [[02 - Mathematics/MOC|Mathematics MOC]]
- [[05 - NLP Fundamentals/Language Modeling/Perplexity|Perplexity]]
- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining Objectives]]
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF with PPO]]
- [[12 - Fine-Tuning/DPO/04 - DPO Derivation|DPO Derivation]]
- [[03 - Machine Learning/Evaluation/05 - ML Evaluation Metrics|ML Evaluation Metrics]]
- [[21 - LLMOps and MLOps/Deployment/07 - A-B Testing and Shadow Deployment|A/B Testing]]
