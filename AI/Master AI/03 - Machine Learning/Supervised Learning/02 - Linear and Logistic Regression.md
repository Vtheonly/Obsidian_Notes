---
tags: [ml, supervised, regression, logistic]
iteration: 2
created: 2026-08-07
aliases: [Linear and Logistic Regression]
---

# 02 - Linear and Logistic Regression

> [!info] TL;DR
> Linear and logistic regression are the simplest ML models — and still among the most useful. They're the conceptual basis for every neural network layer. Understanding them deeply makes the rest of ML make sense.

## Linear Regression

Predict a continuous target as a linear function of features:

$$
\hat{y} = \mathbf{w} \cdot \mathbf{x} + b
$$

### Loss: Mean Squared Error (MSE)

$$
L(\mathbf{w}, b) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2
$$

### Closed-form solution (Normal Equations)

$$
\hat{\mathbf{w}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

For small problems, this is the exact solution — no iteration needed. For large problems, use gradient descent (or SGD) instead; the matrix inverse is $O(d^3)$.

### Probabilistic interpretation: MLE = MSE

If we assume $y_i = \mathbf{w} \cdot \mathbf{x}_i + \epsilon$ with $\epsilon \sim \mathcal{N}(0, \sigma^2)$, the maximum likelihood estimator of $\mathbf{w}$ is exactly the MSE minimizer. So **MSE = MLE under Gaussian noise**. See [[02 - Mathematics/Probability/09 - Gaussian Distribution|Gaussian Distribution]].

### Ridge regression (L2 regularization)

Add an L2 penalty:

$$
L_{\text{ridge}} = \text{MSE} + \lambda \|\mathbf{w}\|^2
$$

Closed form: $\hat{\mathbf{w}} = (\mathbf{X}^T \mathbf{X} + \lambda \mathbf{I})^{-1} \mathbf{X}^T \mathbf{y}$. The $\lambda \mathbf{I}$ term makes the inverse always well-defined (no singularity), and shrinks weights toward zero. This is also **MAP under a Gaussian prior** on $\mathbf{w}$. See [[02 - Mathematics/Probability/08 - Bayes Theorem Deep Dive|Bayes]].

### Lasso (L1 regularization)

Add an L1 penalty:

$$
L_{\text{lasso}} = \text{MSE} + \lambda \|\mathbf{w}\|_1
$$

Lasso produces **sparse** solutions — many weights become exactly zero. Useful for feature selection. MAP under a Laplace prior.

## Logistic Regression

Binary classification with a probabilistic output:

$$
p(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w} \cdot \mathbf{x} + b)}}
$$

### Loss: Binary Cross-Entropy

For one example:

$$
L = -[y \log \hat{p} + (1-y) \log(1 - \hat{p})]
$$

For a batch:

$$
L = -\frac{1}{N} \sum_i [y_i \log \hat{p}_i + (1-y_i) \log(1 - \hat{p}_i)]
$$

### Probabilistic interpretation: MLE = cross-entropy

Logistic regression is MLE for a Bernoulli model: $y_i \sim \text{Bernoulli}(\sigma(\mathbf{w} \cdot \mathbf{x}_i))$. The negative log-likelihood is exactly the binary cross-entropy loss. See [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy Cross-Entropy KL]].

### Multiclass: Softmax Regression

For $K$ classes:

$$
p(y = k \mid \mathbf{x}) = \frac{\exp(\mathbf{w}_k \cdot \mathbf{x})}{\sum_j \exp(\mathbf{w}_j \cdot \mathbf{x})}
$$

This is **softmax** — and softmax regression is exactly the output layer of every modern LLM. The loss is categorical cross-entropy. See [[06 - Attention Mechanisms/Self-Attention/Self-Attention|Self-Attention]] for the softmax mechanics.

## Why These Models Matter

### 1. They're the building blocks of neural networks
A dense layer is a linear regression + activation. A classification head is softmax regression. Every Transformer is built from these primitives.

### 2. Strong baselines
For many problems, logistic regression is a perfectly good model — and it's interpretable, fast, and easy to deploy. Don't reach for a neural network before trying logistic regression.

### 3. Calibration
Logistic regression produces **calibrated probabilities** by construction (when the model is correctly specified). Neural networks often need post-hoc temperature scaling to calibrate.

### 4. The math generalizes
MLE → cross-entropy → backprop. Once you understand the chain from "model the data distribution" to "loss function" to "gradient descent", you understand the conceptual core of all supervised learning.

## Worked Example

```python
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
import numpy as np

X = np.random.randn(100, 5)
y_reg = X @ np.array([1, -2, 0.5, 0, 3]) + 0.1 * np.random.randn(100)
y_cls = (X @ np.array([1, -2, 0.5, 0, 3]) > 0).astype(int)

# Linear regression
lr = LinearRegression().fit(X, y_reg)
print(lr.coef_)  # ≈ [1, -2, 0.5, 0, 3]

# Ridge (L2)
ridge = Ridge(alpha=1.0).fit(X, y_reg)

# Logistic regression
logr = LogisticRegression(C=1.0).fit(X, y_cls)  # C = 1/lambda
print(logr.coef_)  # ≈ direction separating classes
```

## When to Use Classical Regression vs Neural Networks

| Use classical regression when...            | Use neural networks when...                     |
|---------------------------------------------|-------------------------------------------------|
| Tabular data, small dataset (<10k rows)     | Unstructured data (text, images, audio)         |
| Interpretability is required                | Pure predictive accuracy matters                |
| Linear relationships are plausible          | Nonlinear relationships expected                 |
| Fast iteration / deployment needed          | You have lots of data and compute               |
| Need calibrated probabilities out of the box| Willing to add temperature scaling              |

For tabular data, **gradient boosting** ([[03 - Decision Trees and Gradient Boosting]]) is often a better choice than both.

## Production Implications

- **Always start with a simple baseline** — logistic regression with feature engineering. Beats jumping straight to deep learning.
- **For high-stakes probability estimates** (credit risk, medical diagnosis), logistic regression's calibration is a real advantage.
- **For tabular data, use XGBoost** — typically outperforms both logistic regression and deep learning.
- **Feature scaling** matters for regularized linear models. Standardize features before applying L1/L2.

## Common Pitfalls

- **Multicollinearity** — correlated features produce unstable coefficients in unregularized regression. Use ridge.
- **Extrapolation** — linear models extrapolate linearly, which can be wildly wrong outside the training range.
- **Imbalanced classes in logistic regression** — the model will be biased toward the majority class. Use class weighting or resampling.
- **Forgetting that logistic regression is linear** — the decision boundary is a hyperplane. If classes aren't linearly separable (even in feature space), it won't work well.

## Further Reading

- Hastie, Tibshirani, Friedman, *ESL*, Chapter 3 (regression) and 4 (classification).
- Murphy, *Probabilistic Machine Learning*, Chapter 10–11.

## See Also

- [[01 - Bias Variance Tradeoff]]
- [[06 - Regularization Techniques]]
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy Cross-Entropy KL]]
- [[03 - Machine Learning/MOC|ML MOC]]
