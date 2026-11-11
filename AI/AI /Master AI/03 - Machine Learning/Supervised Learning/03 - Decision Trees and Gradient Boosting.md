---
tags: [ml, supervised, trees, gradient-boosting, xgboost]
iteration: 2
created: 2026-08-07
aliases: [Decision Trees and Gradient Boosting]
---

# 03 - Decision Trees and Gradient Boosting

> [!info] TL;DR
> Decision trees recursively split feature space. Random forests average many trees. Gradient boosting (XGBoost, LightGBM, CatBoost) builds trees sequentially, each correcting the previous. **For tabular data, gradient boosting is still SOTA in 2026** — beating deep learning on most benchmarks.

## Decision Trees

A decision tree recursively splits the feature space:

```
                       age > 35?
                      /         \
                  yes            no
                  /               \
            income > 60k?     student?
            /         \         /     \
         yes         no       yes     no
          |           |        |       |
       "buy"      "hold"   "buy"   "sell"
```

### Training

At each node, find the feature and threshold that best separates the classes (for classification) or reduces variance (for regression). Common split criteria:
- **Classification**: Gini impurity, information gain (entropy).
- **Regression**: variance reduction, MSE.

Recursion stops when: max depth reached, too few samples, or pure node.

### Pros
- Interpretable — you can trace any prediction through the tree.
- Handles categorical and numerical features naturally.
- No feature scaling needed.
- Captures nonlinearities and interactions.

### Cons
- **High variance** — small data changes produce very different trees.
- Easily overfits deep trees.
- Cannot extrapolate (predictions are constant in each leaf).

## Random Forests

Train $N$ decision trees on bootstrap samples of the data, with random feature subsets at each split. Average (regression) or majority-vote (classification).

$$
\hat{f}_{\text{RF}}(\mathbf{x}) = \frac{1}{N} \sum_{i=1}^{N} T_i(\mathbf{x})
$$

**Why it works**: averaging many high-variance, low-bias trees reduces variance without increasing bias. This is the **bias-variance tradeoff** ([[01 - Bias Variance Tradeoff]]) in action — bagging reduces variance.

Random forests are robust, fast, and need little tuning. They're a great baseline for tabular data.

## Gradient Boosting

Instead of averaging independent trees (random forest), **boosting** trains trees sequentially, each correcting the previous one's errors.

### Algorithm

1. Start with a constant prediction $F_0(\mathbf{x})$ (e.g., mean of $y$).
2. For $m = 1, \ldots, M$:
   - Compute residuals $r_i = y_i - F_{m-1}(\mathbf{x}_i)$.
   - Train a tree $T_m$ to predict the residuals.
   - Update: $F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \nu \cdot T_m(\mathbf{x})$, where $\nu$ is the learning rate.

The final model: $F_M(\mathbf{x}) = F_0(\mathbf{x}) + \nu \sum_{m=1}^M T_m(\mathbf{x})$.

### Why it works

Each tree learns the **gradient direction** (residual = negative gradient of MSE). Boosting is functional gradient descent in function space — each tree takes a step in the direction that reduces the loss.

### Modern implementations

- **XGBoost** (2014) — the original; introduced regularization, second-order gradients, handling of missing values.
- **LightGBM** (2017) — Microsoft; histogram-based splits, faster on large data.
- **CatBoost** (2018) — Yandex; handles categorical features natively, often best out-of-the-box.

All three are widely used in production and Kaggle competitions.

### Key hyperparameters

- `n_estimators` (M): number of trees. More = lower bias, higher variance.
- `learning_rate` ($\nu$): step size. Lower = needs more trees but often better generalization. Typical: 0.01–0.1.
- `max_depth`: per-tree depth. Shallow (3–8) works best — each tree is weak but they accumulate.
- `subsample`: fraction of data per tree (adds randomness, like bagging).
- `colsample_bytree`: fraction of features per tree.
- Regularization: L1, L2, min_child_weight, gamma.

## Worked Example (XGBoost)

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    early_stopping_rounds=20,
)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
preds = model.predict(X_test)
print(accuracy_score(y_test, preds))
```

Early stopping is essential — it halts training when validation loss stops improving, preventing overfitting.

## Why Gradient Boosting Beats Deep Learning on Tabular Data

Empirical studies (e.g., Grinsztajn et al. 2022) consistently show tree-based models beat deep learning on tabular data. Reasons:

1. **Trees handle irregular target functions and non-smooth features** naturally. Neural networks assume some smoothness.
2. **No feature scaling needed**. Neural networks are sensitive to feature scale.
3. **Implicit feature selection**. Trees pick the most informative splits; NNs use all features.
4. **Robust to irrelevant features**. Trees ignore them; NNs can overfit to noise.
5. **Smaller data regimes**. Trees work well with thousands of samples; NNs need more.

Deep learning dominates **unstructured data** (text, images, audio) and **very large tabular datasets** (millions of rows). For typical enterprise tabular data, gradient boosting is the right choice.

## Why This Matters for AI

- **Most enterprise ML is tabular ML.** If you work in industry, gradient boosting will be your bread and butter, not LLMs.
- **Feature engineering is still alive.** Trees can't invent features; they need good inputs. Domain knowledge + gradient boosting often beats raw-data + deep learning.
- **Interpretability**: tree-based models offer feature importance, SHAP values, individual tree traces. Useful for regulated industries.
- **Ensembling for production**: stacking XGBoost + a neural network often gives the best of both worlds.

## Production Implications

- **Default to gradient boosting for tabular classification/regression.** Don't reach for deep learning first.
- **Use early stopping** — never train to a fixed number of trees.
- **Tune hyperparameters via Bayesian optimization** (Optuna, Hyperopt) — better than grid search for high-dim hyperparameter spaces.
- **SHAP for explanations** — gives per-prediction feature attributions. Critical for compliance.
- **Monitor feature distributions in production** — tree-based models fail silently when feature distributions shift.
- **CatBoost for categorical features** — if your data has many categoricals, CatBoost saves you from one-hot encoding headaches.

## Common Pitfalls

- **Too-deep trees** — high variance. Keep max_depth in 3–8.
- **Forgetting early stopping** — overfits badly.
- **Target leakage** — features that include future information. Always split by time for temporal data.
- **Class imbalance** — use `scale_pos_weight` or sampling.
- **Treating "feature importance" as causation** — it's not. SHAP is closer but still correlational.

## Further Reading

- Hastie, Tibshirani, Friedman, *ESL*, Chapter 9 (additive models, trees), Chapter 10 (boosting).
- Chen & Guestrin (2016), *XGBoost: A Scalable Tree Boosting System*.
- Grinsztajn et al. (2022), *Why do tree-based models still outperform deep learning on tabular data?*

## See Also

- [[01 - Bias Variance Tradeoff]]
- [[02 - Linear and Logistic Regression]]
- [[06 - Regularization Techniques]]
- [[03 - Machine Learning/MOC|ML MOC]]
