---
tags: [ml, evaluation, metrics, calibration]
iteration: 2
created: 2026-08-07
aliases: [ML Evaluation Metrics]
---

# 05 - ML Evaluation Metrics

> [!info] TL;DR
> Choosing the right metric is as important as choosing the right model. This note covers accuracy, precision/recall, F1, ROC/AUC, log loss, regression metrics, and calibration. Most production ML failures are evaluation failures — using the wrong metric for the business objective.

## Classification Metrics

### Accuracy
$$
\text{Accuracy} = \frac{\text{correct predictions}}{\text{total predictions}}
$$

Simple, intuitive, but **misleading on imbalanced data**. A spam filter that always says "not spam" gets 99% accuracy if 1% of emails are spam — and is useless.

### Confusion Matrix

For binary classification:

|                 | Predicted Positive | Predicted Negative |
|-----------------|---------------------|--------------------|
| Actual Positive | TP (true positive)  | FN (false negative)|
| Actual Negative | FP (false positive) | TN (true negative) |

All metrics below are derived from these four counts.

### Precision and Recall

$$
\text{Precision} = \frac{TP}{TP + FP} \quad \text{(of predicted positives, how many are actually positive)}
$$

$$
\text{Recall} = \frac{TP}{TP + FN} \quad \text{(of actual positives, how many did we catch)}
$$

Tradeoff: high precision = few false positives; high recall = few false negatives. Which matters depends on the cost of each error type.

- **Spam filter**: precision matters more (false positives = real email in spam folder).
- **Cancer screening**: recall matters more (false negatives = missed cancer).

### F1 Score

$$
F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
$$

The harmonic mean of precision and recall. Favors balanced precision/recall. Use **F-beta** to weight recall (beta > 1) or precision (beta < 1).

### ROC Curve and AUC

Plot **True Positive Rate (recall)** vs. **False Positive Rate** as the decision threshold varies.

- **AUC** (Area Under Curve): probability that the model ranks a random positive above a random negative. 0.5 = random; 1.0 = perfect.
- AUC is **threshold-independent** — useful when you haven't picked a threshold yet.
- AUC is **insensitive to class imbalance** — useful for comparing models on imbalanced data.

But AUC can be misleading on highly imbalanced data; consider PR-AUC (precision-recall AUC) instead.

### Log Loss (Cross-Entropy)

$$
\text{Log Loss} = -\frac{1}{N} \sum_i \left[ y_i \log \hat{p}_i + (1 - y_i) \log(1 - \hat{p}_i) \right]
$$

Penalizes confident wrong predictions heavily. **The standard loss for classification** ([[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|cross-entropy]]). Lower is better.

### Multiclass

For $K$-class:
- **Macro F1**: average F1 across classes (treats all classes equally).
- **Micro F1**: aggregates TP/FP/FN across classes then computes F1 (favors larger classes).
- **Top-k accuracy**: fraction of examples where the true class is in the top-k predictions. Common for ImageNet-style eval (top-5).

## Regression Metrics

### Mean Squared Error (MSE)
$$
\text{MSE} = \frac{1}{N} \sum_i (y_i - \hat{y}_i)^2
$$

Penalizes large errors heavily (quadratic). Sensitive to outliers. The default loss for regression.

### Mean Absolute Error (MAE)
$$
\text{MAE} = \frac{1}{N} \sum_i |y_i - \hat{y}_i|
$$

Linear penalty. More robust to outliers. Easier to interpret ("average error is $5").

### Root Mean Squared Error (RMSE)
$$
\text{RMSE} = \sqrt{\text{MSE}}
$$

Same units as the target. Easier to interpret than MSE.

### R² (Coefficient of Determination)
$$
R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}
$$

Fraction of variance explained. 1 = perfect; 0 = as good as predicting the mean; <0 = worse than the mean.

### Huber Loss
Smooth combination of MSE (small errors) and MAE (large errors). Robust to outliers while remaining differentiable. Often used in regression losses for deep learning.

## Ranking Metrics

For search / recommendation / retrieval:

- **NDCG** (Normalized Discounted Cumulative Gain): rewards relevant items at top of ranking; discounts by rank.
- **MRR** (Mean Reciprocal Rank): reciprocal of the rank of the first relevant item.
- **MAP** (Mean Average Precision): average precision across all relevant items.
- **Hit Rate@K**: fraction of queries where any relevant item is in top K.

See also [[17 - RAG/MOC|RAG MOC]] for retrieval-specific metrics.

## Calibration

A model is **calibrated** if predicted probabilities match empirical frequencies. If the model says "80% chance of spam" 100 times, about 80 should actually be spam.

### Reliability diagram
Bin predictions by predicted probability; plot predicted vs. empirical frequency. A calibrated model's curve lies on the diagonal.

### Expected Calibration Error (ECE)
Average distance from the diagonal in the reliability diagram.

### Fixing miscalibration
- **Temperature scaling**: divide logits by a learned scalar $T$. Cheap, effective.
- **Platt scaling**: fit a logistic regression on the logits.
- **Isotonic regression**: nonparametric calibration.

Modern neural networks are notoriously miscalibrated (Guo et al. 2017) — they're overconfident. **Temperature scaling is almost always worth applying.**

## Worked Example

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, log_loss, mean_squared_error, r2_score
)

# Binary classification
y_true = [1, 0, 1, 1, 0]
y_pred = [1, 0, 1, 0, 0]
y_prob = [0.9, 0.1, 0.8, 0.4, 0.2]  # predicted probabilities

print(accuracy_score(y_true, y_pred))   # 0.8
print(precision_score(y_true, y_pred))  # 1.0
print(recall_score(y_true, y_pred))     # 0.667
print(f1_score(y_true, y_pred))         # 0.8
print(roc_auc_score(y_true, y_prob))    # 1.0
print(log_loss(y_true, y_prob))         # 0.36
```

## Why This Matters for AI

- **Choosing the right metric** is the difference between shipping a useful model and shipping a useless one. A model with 99% accuracy can be worthless if the 1% errors are catastrophic.
- **Most ML mistakes are evaluation mistakes**: leaking test data, optimizing the wrong metric, ignoring calibration, evaluating on a non-representative sample.
- **LLM evaluation** ([[08 - LLMs/Evaluation/MOC|08 LLM Eval]]) inherits most of these concepts (precision/recall for classification benchmarks; log loss for perplexity; calibration for probability outputs).

## Production Implications

- **Pick the metric before the model.** If you can't articulate what "good" looks like in business terms, you're not ready to train.
- **Track multiple metrics.** Accuracy alone hides precision/recall tradeoffs; F1 alone hides calibration.
- **Always evaluate on held-out data**; use cross-validation for small data.
- **For imbalanced data**: prefer PR-AUC and macro F1 over accuracy.
- **Calibrate before deploying** — temperature scaling takes 5 minutes and prevents overconfident wrong predictions.
- **For high-stakes decisions**: track the cost matrix (FP and FN have different costs) rather than aggregate metrics.

## Common Pitfalls

- **Using accuracy on imbalanced data** — almost always misleading.
- **Optimizing ROC-AUC when you actually need precision at a fixed recall** — different objectives.
- **Forgetting that probabilities need calibration** — your model's "90%" might mean "70%".
- **Test set leakage** — feature engineering on the whole dataset, time-based splits ignored.
- **Reporting only the best metric across hyperparameters** — overstates performance; use nested CV.

## Further Reading

- Hastie et al., *ESL*, Chapter 7 (model assessment).
- Guo et al. (2017), *On Calibration of Modern Neural Networks*.
- Washburn et al. (2023), *A Note on ML Evaluation Metrics* (good survey).

## See Also

- [[01 - Bias Variance Tradeoff]]
- [[02 - Linear and Logistic Regression]]
- [[02 - Mathematics/Information Theory/15 - Entropy Cross-Entropy KL|Entropy Cross-Entropy KL]]
- [[17 - RAG/MOC|RAG MOC]] (retrieval metrics)
- [[03 - Machine Learning/MOC|ML MOC]]
