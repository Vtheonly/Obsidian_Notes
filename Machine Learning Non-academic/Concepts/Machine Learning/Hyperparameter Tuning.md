# Hyperparameter Tuning

## What is a Hyperparameter?

A **hyperparameter** is a configuration setting that is set **before** the training process begins and is **not learned** from the data. Unlike model parameters (like weights and biases in neural networks), hyperparameters control the learning process itself.

### Hyperparameter vs Parameter

| Aspect | Parameter | Hyperparameter |
|--------|-----------|----------------|
| **When Set** | During training | Before training |
| **Learned From** | Data | Not learned from data |
| **Examples** | Weights, biases | Learning rate, K in KNN |
| **Control** | Model behavior | Learning process |

---

## Common Hyperparameters by Algorithm

### 1. K-Nearest Neighbors (KNN)
- **K** (number of neighbors)
- Distance metric (Euclidean, Manhattan)

### 2. Support Vector Machines (SVM)
- **C** (regularization parameter)
- **Gamma** (kernel coefficient)
- Kernel type (linear, RBF, polynomial)

### 3. Neural Networks
- **Learning rate**
- Number of hidden layers
- Number of neurons per layer
- Batch size
- Number of epochs
- Dropout rate
- Activation functions

### 4. Decision Trees & Random Forests
- Max depth
- Min samples split
- Number of trees (for Random Forest)

---

## Why Hyperparameter Tuning Matters

The choice of hyperparameters significantly impacts:

1. **Model Performance**: Poor choices lead to underfitting or overfitting
2. **Training Speed**: Some settings affect convergence time
3. **Generalization**: Proper tuning helps the model work well on unseen data

---

## Hyperparameter Tuning Methods

### 1. Grid Search
Exhaustively tries all combinations of hyperparameter values from a predefined grid.

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20]
}

grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
```

### 2. Random Search
Randomly samples hyperparameter combinations from specified distributions.

```python
from sklearn.model_selection import RandomizedSearchCV

param_distributions = {
    'n_estimators': [50, 100, 200, 500],
    'max_depth': [None, 10, 20, 30, 50]
}

random_search = RandomizedSearchCV(model, param_distributions, n_iter=10, cv=5)
random_search.fit(X_train, y_train)
```

### 3. Bayesian Optimization
Uses probabilistic models to guide the search toward promising hyperparameter regions.

- More efficient than grid/random search
- Learns from previous evaluations
- Tools: Optuna, Hyperopt, Ray Tune

### 4. Manual Tuning
Domain knowledge-based selection and iterative refinement.

---

## Best Practices

1. **Use [[Cross-Validation]]**: Always evaluate hyperparameters using CV to avoid overfitting
2. **Start Simple**: Begin with coarse grid, then refine
3. **Prioritize**: Focus on hyperparameters with the most impact first
4. **Track Experiments**: Use tools like MLflow, Weights & Biases
5. **Consider Compute**: Balance thoroughness with computational resources

---

## Example: Learning Rate Impact

| Learning Rate | Effect |
|---------------|--------|
| Too High | Overshooting, divergence |
| Too Low | Slow convergence, stuck in local minima |
| Optimal | Fast, stable convergence |

---

## Summary

- **Hyperparameters** are pre-training configuration settings
- They **control** how the model learns, not what it learns
- **Tuning** is the process of finding optimal values
- Methods include **Grid Search**, **Random Search**, and **Bayesian Optimization**