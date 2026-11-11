---
tags: [mathematics, moc]
iteration: 5
created: 2026-08-07
---

# 02 — Mathematics MOC

> [!info] The mathematical foundations for AI engineering. Skip at your own risk — every subsequent chapter depends on this. Iteration 5 added the Statistics sub-domain (notes 16–17).

## Reading Order

| #   | Note                                              | Sub-domain        | Purpose                                            |
|-----|---------------------------------------------------|-------------------|----------------------------------------------------|
| 01  | [[01 - Vectors]]                                  | Linear Algebra    | The fundamental object.                            |
| 02  | [[02 - Dot Product]]                              | Linear Algebra    | The most important operation.                      |
| 03  | [[03 - Cosine Similarity]]                        | Linear Algebra    | Direction-only similarity.                         |
| 04  | [[04 - Matrix Multiplication]]                    | Linear Algebra    | The workhorse of deep learning.                    |
| 05  | [[05 - Matrix Decomposition]]                     | Linear Algebra    | SVD, eigendecomposition, PCA.                      |
| 06  | [[06 - Tensors and Broadcasting]]                 | Linear Algebra    | Multi-dim arrays; clean vectorized code.           |
| 07  | [[07 - Probability Essentials]]                   | Probability       | Distributions, MLE, MAP.                           |
| 08  | [[08 - Bayes Theorem Deep Dive]]                  | Probability       | Updating beliefs; generative vs discriminative.    |
| 09  | [[09 - Gaussian Distribution]]                    | Probability       | Why Gaussians are everywhere; CLT; max entropy.    |
| 10  | [[10 - Gradient and Chain Rule]]                  | Calculus          | Foundation of backprop.                            |
| 11  | [[11 - Jacobians and Hessians]]                   | Calculus          | Multivariate derivatives; curvature.               |
| 12  | [[12 - Optimization Essentials]]                  | Optimization      | SGD → Adam overview.                               |
| 13  | [[13 - Adam Derivation]]                          | Optimization      | Full derivation of Adam/AdamW.                     |
| 14  | [[14 - Learning Rate Schedules]]                  | Optimization      | Warmup, cosine decay, linear scaling.              |
| 15  | [[15 - Entropy Cross-Entropy KL]]                 | Information Theory| The loss function; KL as regularizer.              |
| 16  | [[16 - Estimators and Bias]]                      | Statistics        | MLE, MAP, bias-variance, consistency.              |
| 17  | [[17 - Hypothesis Testing]]                       | Statistics        | p-values, confidence intervals, multiple testing.  |

## Sub-Domains

- [[02 - Mathematics/Linear Algebra/01 - Vectors|Linear Algebra]] — notes 01–06
- [[02 - Mathematics/Probability|Probability]] — notes 07–09
- [[02 - Mathematics/MOC|Calculus]] — notes 10–11
- [[02 - Mathematics/Optimization/12 - Optimization Essentials|Optimization]] — notes 12–14
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Information Theory]] — note 15
- [[02 - Mathematics/Statistics/16 - Estimators and Bias|Statistics]] — notes 16–17

## Why This Matters

Modern AI engineering rests on a small set of mathematical ideas:

1. **Linear algebra** — every model is a stack of matrix multiplications and the operations around them.
2. **Probability & information theory** — language modeling is probability estimation; cross-entropy is the loss; KL divergence is the regularizer.
3. **Calculus** — backpropagation is the chain rule applied to a computation graph.
4. **Optimization** — training is gradient descent (and its variants).
5. **Statistics** — evaluating experiments (is model A really better than model B?) requires hypothesis testing.

If you can re-derive [[06 - Attention Mechanisms/Self-Attention/Self-Attention|scaled dot-product attention]] on a whiteboard, you have enough math. If you can't, this chapter is for you.

## See Also

- [[03 - Machine Learning/MOC|03 Machine Learning]] — applies these foundations
- [[04 - Neural Networks/MOC|04 Neural Networks]] — neural networks = linear algebra + calculus + optimization
- [[06 - Attention Mechanisms/MOC|06 Attention Mechanisms]] — attention = dot products + softmax
- [[00 - Vault Management/Master Roadmap|Master Roadmap]]
