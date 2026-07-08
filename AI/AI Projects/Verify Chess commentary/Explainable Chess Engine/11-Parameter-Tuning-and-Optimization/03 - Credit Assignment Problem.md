# Credit Assignment Problem

> **Chapter 11 — Parameter Tuning & Optimization** | ← [[Texel Tuning Method]] | → [[L1 Regularization and Sparsity]]

---

## The Fundamental Problem

In [[Texel Tuning Method|Texel tuning]], we optimize weights on game outcomes. But when multiple rules fire simultaneously (which is almost always the case in chess), how do we determine **which rule deserves credit** for the position's evaluation? This is the **credit assignment problem**, and it's the central challenge in tuning a chess evaluation function.

### A Concrete Example

Consider a position where White has:
- A knight on an outpost (rule fires: +45cp)
- A protected passed pawn (rule fires: +60cp)
- The bishop pair (rule fires: +40cp)
- An open file for the rook (rule fires: +25cp)

Total evaluation: +170cp. White wins the game. How much credit does each rule deserve?

The naive answer: all of them, proportionally. But what if the bishop pair was actually irrelevant because the opponent had no knights? What if the outpost was on the queenside while the game was decided on the kingside? The evaluation says +170cp, but the **true** contribution might be very different from the nominal contribution.

---

## Multicollinearity in Chess Features

### Definition

**Multicollinearity** occurs when two or more features are highly correlated—when they tend to fire together. In chess, this is pervasive:

| Feature Pair | Correlation | Reason |
|---|---|---|
| `Material` and `King_Safety` | Moderate | Material advantage often accompanies safer king |
| `Passed_Pawn` and `Space` | High | Space advantage often creates passed pawns |
| `Knight_Outpost` and `Center_Control` | Very High | Outposts are typically in the center |
| `Mobility` and `Piece_Activity` | Very High | Nearly synonymous |
| `Pawn_Shield` and `King_Safety` | High | Pawn shield is a component of king safety |
| `Rook_Open_File` and `Rook_Activity` | Very High | Open file = active rook |

### The Mathematical Consequence

When features are correlated, the weight optimization has a **degenerate solution space**. Instead of a single optimal weight vector, there's a manifold of solutions:

$$w_1 F_1 + w_2 F_2 = (w_1 + \epsilon) F_1 + (w_2 - \epsilon \cdot \frac{\text{Cov}(F_1, F_2)}{\text{Var}(F_1)}) F_2$$

For highly correlated features ($\text{Cov}(F_1, F_2) \approx \text{Var}(F_1)$), shifting weight from $F_1$ to $F_2$ barely changes the prediction. The optimizer can't distinguish between the "true" weights and shifted versions.

### Credit Dilution

The optimizer tends to **spread reward evenly** among correlated features, diluting the credit that should go to the truly important one:

```
True importance:  Knight_Outpost = 80%, Center_Control = 20%
With correlation: Knight_Outpost = 45%, Center_Control = 55%
```

This is catastrophic for **explainability**: the engine attributes the move to "center control" when it was really about the "knight outpost." See [[Explanation Quality Metrics]] for how this affects explanation faithfulness.

---

## Defense 1: Move-Delta Training

### The Idea

Instead of training on **static position evaluations**, train on **evaluation changes** (deltas). The delta pipeline from [[The Heuristic Delta Pipeline]] computes the change in each rule's score caused by a specific move. By training on deltas, we focus the optimization on **what changed**, not what was already there.

### Why This Helps

In a static evaluation, both `Knight_Outpost` and `Center_Control` might fire simultaneously, creating correlation. But in a delta-based evaluation:

- Moving a knight to an outpost: `Knight_Outpost` delta = +45, `Center_Control` delta = +5
- Playing a central pawn push: `Knight_Outpost` delta = 0, `Center_Control` delta = +25

The deltas are much less correlated than the absolute scores because different moves affect different rules differently.

### Mathematical Formulation

Standard Texel tuning optimizes:

$$\text{Loss} = \frac{1}{N} \sum_{i=1}^{N} \left( R_i - E\left(\sum_j w_j F_{i,j}\right) \right)^2$$

Move-delta training optimizes:

$$\text{Loss}_{\Delta} = \frac{1}{N} \sum_{i=1}^{N} \left( R_i - E\left(\sum_j w_j \Delta_{i,j}\right) \right)^2$$

Where $\Delta_{i,j} = F_{i,j}^{\text{after}} - F_{i,j}^{\text{before}}$ is the delta for rule $j$ on move $i$.

### Implementation

```python
class MoveDeltaDataset(Dataset):
    """Dataset of move deltas with game outcomes.

    Each sample is the delta between positions before and after a move,
    paired with the game outcome. This reduces feature correlation.
    """

    def __init__(self, move_records: List[Dict]):
        """
        Args:
            move_records: List of dicts with keys:
                - 'features_before': numpy array (n_features,)
                - 'features_after': numpy array (n_features,)
                - 'result': float (0.0, 0.5, or 1.0)
        """
        self.deltas = torch.tensor(
            np.array([
                r['features_after'] - r['features_before']
                for r in move_records
            ]),
            dtype=torch.float32
        )
        self.results = torch.tensor(
            [r['result'] for r in move_records],
            dtype=torch.float32
        )

    def __len__(self):
        return len(self.results)

    def __getitem__(self, idx):
        return self.deltas[idx], self.results[idx]
```

### Limitations

Move-delta training has its own challenges:

1. **Label noise**: The game outcome is determined by *all* moves, not just one. A good move in a losing game still gets labeled as a loss.
2. **Propensity problem**: We only see moves that were actually played, not moves that should have been played.
3. **Opponent moves**: The outcome depends on the opponent's responses, which we don't model.

---

## Defense 2: L1 Regularization (Lasso)

### The Idea

Add an **L1 penalty** to the loss function that drives irrelevant weights to exactly zero. This forces the optimizer to make hard choices about which features matter, reducing credit dilution.

$$\text{Loss}_{L1} = \text{Loss}_{MSE} + \lambda \sum_{j=1}^{n} |w_j|$$

See [[L1 Regularization and Sparsity]] for the full mathematical treatment.

### Why This Helps for Credit Assignment

Without L1, the optimizer might set:
- `Knight_Outpost` = 40cp, `Center_Control` = 35cp (split credit)

With L1, the optimizer prefers:
- `Knight_Outpost` = 55cp, `Center_Control` = 0cp (concentrated credit)

The L1 penalty makes it "expensive" to have two correlated features both non-zero. The optimizer will keep the more predictive one and zero out the other.

### Tuning λ

The regularization strength $\lambda$ controls the trade-off between prediction accuracy and sparsity:

| λ Value | Effect | Use Case |
|---|---|---|
| 0 | No regularization, full credit dilution | Maximum prediction accuracy |
| 0.001 | Mild sparsity, some credit concentration | Balanced |
| 0.01 | Moderate sparsity, clear credit assignment | Recommended for explainability |
| 0.1 | Aggressive sparsity, very few active rules | Maximum explainability |

The optimal $\lambda$ is found via **cross-validation**: train with different λ values and choose the one that gives the best validation loss while maintaining acceptable sparsity.

---

## Defense 3: Feature Orthogonality

### The Idea

Design rules that are **mutually exclusive**—they can never fire simultaneously. This eliminates correlation at the source.

### What Makes Rules Orthogonal

Two rules $R_1$ and $R_2$ are orthogonal if there is no position where both are active:

$$R_1 \cap R_2 = \emptyset$$

### Examples

**Bad design (overlapping)**:
- `Is_Check` and `Is_Queen_Check`: Every queen check is also a check, so these always overlap
- `Knight_Outpost` and `Center_Control`: Outposts are usually central

**Good design (orthogonal)**:
- `Minor_Piece_Check` and `Major_Piece_Check`: A check is either by a minor piece or a major piece, never both
- `Kingside_Attack` and `Queenside_Play`: These operate on different board sectors

### The Orthogonality Test

```python
def test_orthogonality(rule_pairs: List[Tuple[str, str]],
                        positions: List[Dict],
                        threshold: float = 0.3) -> List[dict]:
    """Test whether rule pairs are approximately orthogonal.

    Args:
        rule_pairs: Pairs of rule names to test
        positions: Sample positions with computed features
        threshold: Maximum acceptable correlation

    Returns:
        List of results with correlation values
    """
    results = []

    for rule_a, rule_b in rule_pairs:
        vals_a = [p['features'][rule_a] for p in positions]
        vals_b = [p['features'][rule_b] for p in positions]

        # Compute Pearson correlation
        correlation = np.corrcoef(vals_a, vals_b)[0, 1]

        # Compute co-activation rate (both non-zero)
        both_active = sum(
            1 for a, b in zip(vals_a, vals_b) if a != 0 and b != 0
        ) / len(positions)

        results.append({
            'rule_a': rule_a,
            'rule_b': rule_b,
            'correlation': correlation,
            'co_activation_rate': both_active,
            'is_orthogonal': abs(correlation) < threshold,
            'violation_severity': 'high' if abs(correlation) > 0.5
                                  else 'medium' if abs(correlation) > threshold
                                  else 'low'
        })

    return results
```

See [[Feature Orthogonality Design]] for the complete methodology.

---

## The Interaction Between Defenses

These three defenses are complementary and should be used together:

```
                    Credit Assignment Problem
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
    Move-Delta       L1 Regularization  Feature
    Training         (Lasso)            Orthogonality
            │              │              │
            ▼              ▼              ▼
    Reduces           Forces sparse     Eliminates
    correlation       weight vectors    overlap at
    in training       → clear credit    design time
    data              assignment
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                   Better Explanations
                   (Faithful, Complete)
```

### Recommended Pipeline

1. **Design time**: Apply [[Feature Orthogonality Design]] to minimize rule overlap
2. **Data preparation**: Use move-delta training to reduce correlation
3. **Optimization**: Apply L1 regularization during [[Texel Tuning Method|Texel tuning]]
4. **Validation**: Check credit assignment using the ablation test from [[Explanation Quality Metrics]]

---

## Quantifying Credit Assignment Quality

### The Ablation Fidelity Score

After tuning, we can measure how well the weights reflect true importance:

$$\text{Ablation Fidelity} = \frac{1}{n} \sum_{j=1}^{n} \text{corr}\left(|w_j|, \quad \Delta\text{Loss}_{-j}\right)$$

Where $\Delta\text{Loss}_{-j}$ is the change in validation loss when weight $w_j$ is ablated (set to zero).

If weights with large magnitude also cause large loss increases when ablated, credit assignment is good. If some weights are large but their ablation barely matters, credit has been misassigned.

```python
def compute_ablation_fidelity(model, dataset, n_features):
    """Compute ablation fidelity score for credit assignment quality."""
    baseline_loss = evaluate_model(model, dataset)

    ablation_effects = []
    weight_magnitudes = []

    for j in range(n_features):
        if j == 0:  # Skip frozen pawn weight
            continue

        original_weight = model.weights[j].item()
        weight_magnitudes.append(abs(original_weight))

        # Ablate weight j
        with torch.no_grad():
            model.weights[j] = 0.0
        ablated_loss = evaluate_model(model, dataset)
        effect = ablated_loss - baseline_loss
        ablation_effects.append(effect)

        # Restore weight
        with torch.no_grad():
            model.weights[j] = original_weight

    # Compute correlation between weight magnitude and ablation effect
    fidelity = np.corrcoef(weight_magnitudes, ablation_effects)[0, 1]
    return fidelity
```

---

## Connections

- **Previous**: [[Texel Tuning Method]] — The tuning algorithm where credit assignment matters
- **Next**: [[L1 Regularization and Sparsity]] — Deep dive into the L1 defense
- **Related**: [[Feature Orthogonality Design]] — Design-time defense against correlation
- **Related**: [[Constrained Optimization]] — Additional constraints during tuning
- **Downstream**: [[Explanation Quality Metrics]] — How credit assignment affects explanations
- **Downstream**: [[The Heuristic Delta Pipeline]] — Move-delta computation
