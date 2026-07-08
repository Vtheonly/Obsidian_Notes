# L1 Regularization and Sparsity

> **Chapter 11 — Parameter Tuning & Optimization** | ← [[Credit Assignment Problem]] | → [[Constrained Optimization]]

---

## The L1 Penalty

### Definition

L1 regularization adds a penalty proportional to the **absolute value** of the weights to the loss function:

$$\text{Loss}_{L1}(\mathbf{W}) = \text{Loss}_{MSE}(\mathbf{W}) + \lambda \sum_{j=1}^{n} |w_j|$$

Where:
- $\text{Loss}_{MSE}$ = the mean squared error from [[Texel Tuning Method]]
- $\lambda$ = regularization strength (hyperparameter)
- $|w_j|$ = absolute value of weight $j$

This is also known as **Lasso regression** (Least Absolute Shrinkage and Selection Operator).

### Contrast with L2 Regularization (Ridge)

L2 regularization uses the **square** of the weights:

$$\text{Loss}_{L2}(\mathbf{W}) = \text{Loss}_{MSE}(\mathbf{W}) + \lambda \sum_{j=1}^{n} w_j^2$$

The difference seems minor—absolute value vs. square—but the consequences are profound:

| Property | L1 (Lasso) | L2 (Ridge) |
|---|---|---|
| Drives weights to exactly 0? |  Yes |  No (only approaches 0) |
| Produces sparse solutions? |  Yes |  No |
| Feature selection? |  Automatic |  No |
| Handles multicollinearity? | Selects one feature | Spreads weight evenly |
| Effect on small weights | Zeroes them out | Shrinks them slightly |
| Effect on large weights | Shrinks proportionally | Shrinks quadratically |
| Geometric shape of constraint | Diamond (vertices on axes) | Circle (smooth) |

---

## Geometric Intuition: Why L1 Produces Sparsity

### The Constraint Region

Regularization is equivalent to constraining the weight vector to lie within a region. For L1:

$$\sum_{j=1}^{n} |w_j| \leq t$$

This defines a **diamond** (in 2D) or a **cross-polytope** (in higher dimensions). The vertices of the diamond lie on the axes, meaning one weight is non-zero and the others are zero.

For L2:

$$\sum_{j=1}^{n} w_j^2 \leq t$$

This defines a **circle** (in 2D) or a **sphere** (in higher dimensions). There are no vertices on the axes.

### The Optimization Geometry

The optimal weight vector is the point where the **loss contour** (ellipses) first touches the **constraint region**:

```
L1 Constraint (Diamond):          L2 Constraint (Circle):

     w2                              w2
      |                               |
      ◇                               ○
     / \                             /   \
    /   \        ← Loss contours    /     \     ← Loss contours
   /  *  \       touch at vertex   /   *   \    touch on edge
  /       \      (w1=0, sparse!)  /         \   (both non-zero)
 ◇─────────◇ w1                 ○───────────○ w1
```

The loss contours (ellipses representing equal MSE) are more likely to touch the L1 diamond at a **vertex** than the L2 circle at an **axis point**. This is why L1 naturally produces sparsity: the optimal point often has one weight exactly zero.

### Formal Proof Sketch

The subgradient of $|w_j|$ at $w_j = 0$ is the interval $[-1, 1]$. This means the gradient of the loss can be "absorbed" by the subgradient without moving the weight away from zero, if:

$$\left|\frac{\partial \text{Loss}_{MSE}}{\partial w_j}\right| \leq \lambda$$

In other words, if a weight's contribution to reducing MSE is smaller than $\lambda$, L1 will drive it to exactly zero. L2 has no such threshold effect.

---

## Why Sparsity Is Desirable for Explainability

### Fewer Active Rules = Clearer Explanations

An explanation that mentions 3 rules is clearer than one that mentions 15:

> **Dense (15 rules)**: "The move improves material, pawn structure, king safety, mobility, center control, piece activity, connectivity, space, threats, passed pawns, bishop pair, rook activity, knight placement, weak squares, and pawn shields."

> **Sparse (3 rules)**: "The knight occupies a powerful outpost, supported by the d4 pawn, and creates pressure on the opponent's king."

### The Sparsity-Explainability Trade-off

| Number of Active Rules | Playing Strength (Elo) | Explanation Quality |
|---|---|---|
| 300 (all rules) | 2800 | Terrible — information overload |
| 50 (moderate sparsity) | 2750 | Good — manageable detail |
| 15 (high sparsity) | 2600 | Excellent — crystal clear |
| 3 (extreme sparsity) | 2300 | Perfect explanation, bad engine |

The optimal operating point is around **20-50 active rules**: enough to play strong chess, few enough to produce coherent explanations.

### Quantifying Sparsity

The sparsity of a weight vector is measured by the fraction of zero weights:

$$\text{Sparsity} = \frac{|\{j : w_j = 0\}|}{n}$$

Or, for near-zero weights (which are practically irrelevant):

$$\text{Effective Sparsity} = \frac{|\{j : |w_j| < \epsilon\}|}{n}$$

Where $\epsilon$ is a small threshold (e.g., 2 centipawns — anything smaller is negligible).

---

## Choosing λ via Cross-Validation

### The Regularization Path

As $\lambda$ increases, more weights are driven to zero. We can trace the **regularization path** by training with different $\lambda$ values:

```python
import numpy as np
from typing import List, Tuple

def regularization_path(tuner_class, dataset,
                         lambda_values: List[float]) -> List[dict]:
    """Trace the regularization path for different λ values.

    Returns a list of results, one per λ, showing sparsity and loss.
    """
    results = []

    for lam in lambda_values:
        tuner = tuner_class(
            n_features=300,
            l1_lambda=lam
        )
        train_result = tuner.train(dataset, n_epochs=100)

        weights = train_result['final_weights']
        n_zero = sum(1 for w in weights.values() if abs(w) < 2.0)
        sparsity = n_zero / len(weights)

        results.append({
            'lambda': lam,
            'sparsity': sparsity,
            'val_loss': train_result['best_val_loss'],
            'n_active_rules': len(weights) - n_zero,
            'active_rules': {
                k: v for k, v in weights.items() if abs(v) >= 2.0
            }
        })

    return results


# Typical lambda search range
lambda_values = [0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
```

### The Elbow Method

Plot validation loss vs. sparsity. The optimal $\lambda$ is at the "elbow" — the point where further sparsity causes disproportionate loss increase:

```
Val Loss
  |
  |  *
  |    *
  |      *       ← Elbow: λ_optimal ≈ 0.01
  |        *
  |          * * * * *    ← Too sparse, performance collapses
  |
  +--------------------→ Sparsity
   0%      50%      100%
```

### K-Fold Cross-Validation

```python
def cross_validate_lambda(dataset, lambda_values,
                           k_folds: int = 5) -> Tuple[float, dict]:
    """Find the optimal λ using k-fold cross-validation."""
    n_samples = len(dataset)
    fold_size = n_samples // k_folds

    lambda_scores = {lam: [] for lam in lambda_values}

    for fold in range(k_folds):
        # Split into train/val
        val_start = fold * fold_size
        val_end = val_start + fold_size

        for lam in lambda_values:
            tuner = TexelTuningTrainer(n_features=300, l1_lambda=lam)
            result = tuner.train(dataset, n_epochs=80)

            # Evaluate on validation fold
            val_loss = result['best_val_loss']
            lambda_scores[lam].append(val_loss)

    # Find λ with lowest average validation loss
    avg_losses = {lam: np.mean(scores)
                  for lam, scores in lambda_scores.items()}
    best_lambda = min(avg_losses, key=avg_losses.get)

    return best_lambda, avg_losses
```

---

## L1 in the PyTorch Training Loop

### Modified Loss Computation

```python
def compute_loss_with_l1(model, predictions, targets, l1_lambda):
    """Compute MSE loss with L1 regularization."""
    mse_loss = nn.MSELoss()(predictions, targets)

    # L1 penalty: sum of absolute weights
    # Exclude the frozen pawn weight from the penalty
    weights_excluding_pawn = torch.cat([
        model.weights[:model.pawn_idx],
        model.weights[model.pawn_idx + 1:]
    ])
    l1_penalty = l1_lambda * torch.sum(torch.abs(weights_excluding_pawn))

    total_loss = mse_loss + l1_penalty
    return total_loss, mse_loss, l1_penalty
```

### Proximal Gradient Descent (Soft Thresholding)

For L1, a more sophisticated optimization approach is **proximal gradient descent**, which uses the **soft thresholding operator**:

$$\text{prox}_{\lambda}(w) = \text{sign}(w) \cdot \max(|w| - \lambda, 0)$$

This operator shrinks each weight toward zero by $\lambda$, and sets it to exactly zero if it crosses the origin. This guarantees sparsity at every step, not just asymptotically.

```python
def soft_threshold(weights: torch.Tensor, lambda_val: float,
                    pawn_idx: int) -> torch.Tensor:
    """Apply soft thresholding (proximal operator for L1).

    This guarantees exact sparsity: weights with |w| < λ become exactly 0.
    """
    with torch.no_grad():
        # Apply soft thresholding to all weights except pawn
        for j in range(len(weights)):
            if j == pawn_idx:
                continue  # Never threshold the pawn weight

            w = weights[j].item()
            if w > lambda_val:
                weights[j] = w - lambda_val
            elif w < -lambda_val:
                weights[j] = w + lambda_val
            else:
                weights[j] = 0.0

    return weights
```

### Integration into Training

```python
class L1TexelTuner(TexelTuner):
    """Texel tuner with L1 regularization via proximal gradient descent."""

    def __init__(self, n_features, pawn_idx=0, k=1.13, l1_lambda=0.01):
        super().__init__(n_features, pawn_idx, k)
        self.l1_lambda = l1_lambda

    def train_step(self, features, results, optimizer):
        """Single training step with L1 proximal update."""
        # Standard gradient step
        optimizer.zero_grad()
        predictions = self.forward(features)
        mse_loss = nn.MSELoss()(predictions, results)
        mse_loss.backward()

        # Zero gradient for frozen pawn weight
        self.weights.grad[self.pawn_idx] = 0.0

        optimizer.step()

        # Proximal step: soft thresholding for L1
        self.weights = nn.Parameter(
            soft_threshold(self.weights, self.l1_lambda, self.pawn_idx)
        )

        return mse_loss.item()
```

---

## Analyzing the Sparse Weight Vector

After training with L1, we can analyze which rules survived and which were eliminated:

```python
def analyze_sparsity(weights: Dict[str, float],
                      threshold: float = 2.0) -> dict:
    """Analyze the sparse weight vector after L1 training."""
    active = {k: v for k, v in weights.items() if abs(v) >= threshold}
    zeroed = {k: v for k, v in weights.items() if abs(v) < threshold}

    # Categorize active rules
    categories = {
        'material': [],
        'pawn_structure': [],
        'piece_placement': [],
        'king_safety': [],
        'mobility': [],
        'threats': [],
        'other': []
    }

    CATEGORY_MAP = {
        'Material': 'material', 'Pawn': 'pawn_structure',
        'Knight': 'piece_placement', 'Bishop': 'piece_placement',
        'Rook': 'piece_placement', 'King': 'king_safety',
        'Mobility': 'mobility', 'Threat': 'threats',
        'Passed': 'pawn_structure', 'Outpost': 'piece_placement',
    }

    for name, value in active.items():
        categorized = False
        for key, cat in CATEGORY_MAP.items():
            if key in name:
                categories[cat].append((name, value))
                categorized = True
                break
        if not categorized:
            categories['other'].append((name, value))

    return {
        'total_rules': len(weights),
        'active_rules': len(active),
        'zeroed_rules': len(zeroed),
        'sparsity': len(zeroed) / len(weights),
        'active_by_category': categories,
        'largest_active': sorted(active.items(),
                                  key=lambda x: abs(x[1]),
                                  reverse=True)[:20],
        'eliminated': list(zeroed.keys())
    }
```

### Typical Results

After L1 tuning with $\lambda = 0.01$ on a 300-rule engine:

| Category | Rules Before | Active After L1 | Sparsity |
|---|---|---|---|
| Material | 6 | 6 | 0% (all kept) |
| Pawn Structure | 35 | 18 | 49% |
| Piece Placement | 55 | 22 | 60% |
| King Safety | 28 | 15 | 46% |
| Mobility | 18 | 8 | 56% |
| Threats | 25 | 12 | 52% |
| Other | 133 | 40 | 70% |
| **Total** | **300** | **121** | **60%** |

60% of rules are zeroed out, leaving 121 active rules. This is a much more explainable engine while still maintaining strong play.

---

## Connections

- **Previous**: [[Credit Assignment Problem]] — Why L1 helps with credit assignment
- **Next**: [[Constrained Optimization]] — Additional constraints beyond L1
- **Related**: [[Texel Tuning Method]] — The base tuning algorithm
- **Related**: [[Feature Orthogonality Design]] — Complementary approach to reducing correlation
- **Downstream**: [[Explanation Quality Metrics]] — Sparsity directly improves explanations
