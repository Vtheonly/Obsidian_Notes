# Texel Tuning Method

> **Chapter 11 — Parameter Tuning & Optimization** | ← [[The Tuning Problem]] | → [[Credit Assignment Problem]]

---

## Historical Background

The Texel tuning method was popularized by **Peter Österlund**, the author of the chess engine **Texel**, in 2014. The key insight was beautifully simple: **treat chess evaluation as logistic regression on game outcomes**. Instead of hand-tuning parameters or using expensive self-play, simply download a large database of high-quality games, extract positions, and optimize the evaluation weights to predict the game result.

This approach was subsequently adopted and refined by many engines, including early versions of Stockfish (before SPSA and NNUE took over). It remains one of the most efficient methods for tuning an evaluation function with limited computational resources.

---

## Mathematical Foundation

### The Logistic Regression Framework

Given a position $i$ with evaluation score $S_i$ (computed from our [[Declarative Rule Engine with Bitboards|rule engine]]), we want to predict the game outcome $R_i \in \{0, 0.5, 1\}$ (Black wins, Draw, White wins).

The prediction uses a **sigmoid function** that maps the evaluation score to a probability:

$$\hat{R}_i = E(S_i) = \frac{1}{1 + 10^{-K \cdot S_i / 400}}$$

Where:
- $S_i$ = the evaluation score in centipawns for position $i$
- $K$ = a scaling constant (typically $K \approx 1.13$)
- $\hat{R}_i$ = predicted probability of White winning

### The Sigmoid Mapping

The sigmoid function has important properties:

| Property | Value |
|---|---|
| $E(0)$ | 0.5 (equal position → 50-50 outcome) |
| $E(+\infty)$ | 1.0 (White winning → certain White win) |
| $E(-\infty)$ | 0.0 (Black winning → certain Black win) |
| Monotonicity | Strictly increasing |
| Symmetry | $E(-S) = 1 - E(S)$ |

The factor of $400$ in the denominator comes from the **Elo rating system**: a 400 Elo advantage corresponds to a 10:1 expected score ratio. The constant $K$ adjusts the steepness of the curve to match the observed relationship between centipawn evaluations and game outcomes.

### The K Constant

The value of $K$ must be determined empirically. A common method is:

1. Set up the evaluation function with initial weights
2. For each candidate $K$ value, compute the mean squared error over the training set
3. Choose the $K$ that minimizes the error

```python
def find_optimal_k(positions: list, weights: dict,
                    k_range: tuple = (0.5, 2.0),
                    k_step: float = 0.01) -> float:
    """Find the optimal K constant for the sigmoid mapping."""
    best_k = k_range[0]
    best_error = float('inf')

    for k_int in range(int(k_range[0] * 100), int(k_range[1] * 100)):
        k = k_int / 100.0
        error = compute_mse(positions, weights, k)
        if error < best_error:
            best_error = error
            best_k = k

    return best_k
```

Typical optimal values: $K \in [1.00, 1.30]$, with $K = 1.13$ being a common default.

---

## The Loss Function

### Mean Squared Error

The loss function is the **Mean Squared Error** between predicted and actual outcomes:

$$\text{Loss}(\mathbf{W}) = \frac{1}{N} \sum_{i=1}^{N} \left( R_i - E(S_i(\mathbf{W})) \right)^2$$

Where:
- $N$ = number of training positions
- $R_i$ = actual game outcome (1.0, 0.5, or 0.0)
- $E(S_i(\mathbf{W}))$ = predicted outcome from the sigmoid

### The Linear Evaluation

The evaluation score $S_i$ is a **linear function** of the weights and features:

$$S_i(\mathbf{W}) = \sum_{j=1}^{n} w_j \cdot F_{i,j}$$

Where:
- $w_j$ = weight for rule $j$ (what we're optimizing)
- $F_{i,j}$ = feature value for rule $j$ in position $i$ (computed by the engine)
- $n$ = total number of rules/features

This linearity is crucial: it makes the loss function differentiable, enabling gradient-based optimization.

### The Gradient

The gradient of the loss with respect to weight $w_j$ is:

$$\frac{\partial \text{Loss}}{\partial w_j} = -\frac{2}{N} \sum_{i=1}^{N} \left( R_i - E(S_i) \right) \cdot E'(S_i) \cdot F_{i,j}$$

Where the derivative of the sigmoid is:

$$E'(S) = \frac{K \cdot \ln(10)}{400} \cdot E(S) \cdot (1 - E(S))$$

This gradient tells us how to adjust each weight to reduce the prediction error.

---

## The Pawn Anchor

### Why We Need It

The evaluation is linear: $S_i = \sum w_j F_{i,j}$. If we scale all weights by a constant $c$, the evaluation becomes $c \cdot S_i$. The sigmoid then gives:

$$E(c \cdot S_i) = \frac{1}{1 + 10^{-K \cdot c \cdot S_i / 400}}$$

This is equivalent to using a different $K$ value. Without an anchor, the optimization has infinite equivalent solutions.

### The Fix: Freeze W_pawn = 100

We **fix the pawn weight at 100 centipawns** and optimize everything else relative to this anchor. This:

1. Removes the scaling ambiguity
2. Ensures all weights are in interpretable centipawn units
3. Provides a meaningful reference point for all other weights

```python
PAWN_WEIGHT = 100  # Frozen, never updated during optimization
```

---

## Full PyTorch Implementation

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Tuple, Dict

class ChessPositionDataset(Dataset):
    """Dataset of chess positions with game outcomes."""

    def __init__(self, positions: List[Dict]):
        """
        Args:
            positions: List of dicts with keys:
                - 'features': numpy array of shape (n_features,)
                - 'result': float, 0.0, 0.5, or 1.0
        """
        self.features = torch.tensor(
            np.array([p['features'] for p in positions]),
            dtype=torch.float32
        )
        self.results = torch.tensor(
            [p['result'] for p in positions],
            dtype=torch.float32
        )

    def __len__(self):
        return len(self.results)

    def __getitem__(self, idx):
        return self.features[idx], self.results[idx]


class TexelTuner(nn.Module):
    """PyTorch module for Texel-style evaluation tuning."""

    def __init__(self, n_features: int, pawn_feature_idx: int = 0,
                 k_constant: float = 1.13):
        """
        Args:
            n_features: Number of evaluation features/rules
            pawn_feature_idx: Index of the pawn material feature (frozen at 100)
            k_constant: The K constant for sigmoid scaling
        """
        super().__init__()
        self.n_features = n_features
        self.pawn_idx = pawn_feature_idx
        self.k_constant = k_constant

        # Initialize weights (small random values around common chess weights)
        self.weights = nn.Parameter(
            torch.randn(n_features) * 10,
            requires_grad=True
        )

        # Freeze the pawn weight
        with torch.no_grad():
            self.weights[pawn_feature_idx] = 100.0

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """Compute predicted outcomes for a batch of positions.

        Args:
            features: Tensor of shape (batch_size, n_features)

        Returns:
            Predicted outcomes, tensor of shape (batch_size,)
        """
        # Linear evaluation: S = W · F
        scores = torch.matmul(features, self.weights)

        # Sigmoid mapping: E(S) = 1 / (1 + 10^(-K·S/400))
        exponent = -self.k_constant * scores / 400.0
        # Use clamp to prevent overflow in 10^x
        exponent = torch.clamp(exponent, -20, 20)
        predictions = 1.0 / (1.0 + torch.pow(10.0, exponent))

        return predictions

    def get_weights(self) -> Dict[str, float]:
        """Return the current weight values as a dictionary."""
        return {f"rule_{i}": self.weights[i].item()
                for i in range(self.n_features)}


class TexelTuningTrainer:
    """Trains evaluation weights using the Texel tuning method."""

    def __init__(self, n_features: int, pawn_feature_idx: int = 0,
                 k_constant: float = 1.13, learning_rate: float = 1.0,
                 l1_lambda: float = 0.0):
        self.model = TexelTuner(n_features, pawn_feature_idx, k_constant)
        self.pawn_idx = pawn_feature_idx
        self.l1_lambda = l1_lambda

        # Use SGD with a relatively large learning rate
        # (the loss landscape is smooth)
        self.optimizer = optim.SGD(
            self.model.parameters(), lr=learning_rate
        )

        # MSE loss
        self.criterion = nn.MSELoss()

    def train(self, dataset: ChessPositionDataset,
              n_epochs: int = 100,
              batch_size: int = 16384,
              validation_split: float = 0.1,
              patience: int = 10) -> Dict:
        """Train the model on the dataset.

        Args:
            dataset: Chess positions with outcomes
            n_epochs: Maximum training epochs
            batch_size: Mini-batch size
            validation_split: Fraction of data for validation
            patience: Early stopping patience

        Returns:
            Training history and final weights
        """
        # Split into train/validation
        n_total = len(dataset)
        n_val = int(n_total * validation_split)
        n_train = n_total - n_val

        train_set, val_set = torch.utils.data.random_split(
            dataset, [n_train, n_val]
        )

        train_loader = DataLoader(
            train_set, batch_size=batch_size, shuffle=True
        )
        val_loader = DataLoader(
            val_set, batch_size=batch_size, shuffle=False
        )

        history = {
            'train_loss': [], 'val_loss': [],
            'best_val_loss': float('inf'), 'best_epoch': 0
        }

        for epoch in range(n_epochs):
            # Training
            self.model.train()
            train_loss = 0.0
            n_batches = 0

            for features, results in train_loader:
                self.optimizer.zero_grad()

                predictions = self.model(features)
                loss = self.criterion(predictions, results)

                # Add L1 regularization if specified
                if self.l1_lambda > 0:
                    l1_penalty = self.l1_lambda * torch.sum(
                        torch.abs(self.model.weights)
                    )
                    loss = loss + l1_penalty

                loss.backward()

                # Zero out the gradient for the frozen pawn weight
                self.model.weights.grad[self.pawn_idx] = 0.0

                self.optimizer.step()

                # Clamp weights to reasonable ranges
                with torch.no_grad():
                    self._apply_constraints()

                train_loss += loss.item()
                n_batches += 1

            avg_train_loss = train_loss / max(n_batches, 1)
            history['train_loss'].append(avg_train_loss)

            # Validation
            val_loss = self._evaluate(val_loader)
            history['val_loss'].append(val_loss)

            # Track best
            if val_loss < history['best_val_loss']:
                history['best_val_loss'] = val_loss
                history['best_epoch'] = epoch
                best_weights = self.model.get_weights().copy()

            # Early stopping
            if epoch - history['best_epoch'] > patience:
                print(f"Early stopping at epoch {epoch}")
                break

            if epoch % 10 == 0:
                print(f"Epoch {epoch}: train_loss={avg_train_loss:.6f}, "
                      f"val_loss={val_loss:.6f}")

        # Restore best weights
        with torch.no_grad():
            for i, (name, value) in enumerate(best_weights.items()):
                self.model.weights[i] = value

        return {
            'history': history,
            'final_weights': self.model.get_weights(),
            'best_val_loss': history['best_val_loss']
        }

    def _evaluate(self, loader: DataLoader) -> float:
        """Evaluate the model on a data loader."""
        self.model.eval()
        total_loss = 0.0
        n_batches = 0

        with torch.no_grad():
            for features, results in loader:
                predictions = self.model(features)
                loss = self.criterion(predictions, results)
                total_loss += loss.item()
                n_batches += 1

        return total_loss / max(n_batches, 1)

    def _apply_constraints(self):
        """Apply domain constraints to weights after each update."""
        # Pawn weight stays at 100
        self.model.weights[self.pawn_idx] = 100.0

        # Knight, Bishop must be positive (you wouldn't remove one for free)
        # These indices are engine-specific; adjust as needed
        KNIGHT_IDX = 1
        BISHOP_IDX = 2
        ROOK_IDX = 3
        QUEEN_IDX = 4

        self.model.weights[KNIGHT_IDX] = max(
            self.model.weights[KNIGHT_IDX], 100.0
        )
        self.model.weights[BISHOP_IDX] = max(
            self.model.weights[BISHOP_IDX], 100.0
        )
        self.model.weights[ROOK_IDX] = max(
            self.model.weights[ROOK_IDX], 200.0
        )
        self.model.weights[QUEEN_IDX] = max(
            self.model.weights[QUEEN_IDX], 600.0
        )

        # Knight_On_Rim must be negative
        # (find the index in your feature list)
        # self.model.weights[KRIM_IDX] = min(self.model.weights[KRIM_IDX], 0.0)
```

### Usage Example

```python
def main():
    # Load training data (positions with features and outcomes)
    positions = load_positions_from_pgn("elite_games.pgn")
    dataset = ChessPositionDataset(positions)

    # Create tuner
    tuner = TexelTuningTrainer(
        n_features=300,       # Number of rules
        pawn_feature_idx=0,   # Pawn material is feature 0
        k_constant=1.13,      # Standard K value
        learning_rate=0.5,    # Relatively aggressive for smooth landscape
        l1_lambda=0.001       # Mild L1 for sparsity (see [[L1 Regularization and Sparsity]])
    )

    # Train
    result = tuner.train(
        dataset,
        n_epochs=200,
        batch_size=16384,
        patience=15
    )

    # Print top weights
    weights = sorted(result['final_weights'].items(),
                     key=lambda x: abs(x[1]), reverse=True)
    print("\nTop 20 weights by magnitude:")
    for name, value in weights[:20]:
        print(f"  {name}: {value:.2f} cp")

    # Export weights for the C++ engine
    export_weights_to_cpp(result['final_weights'], "tuned_weights.h")


def export_weights_to_cpp(weights: Dict[str, float], filepath: str):
    """Export weights as a C++ header file."""
    with open(filepath, 'w') as f:
        f.write("// Auto-generated by Texel Tuning\n")
        f.write("// Do not edit manually\n\n")
        f.write("#pragma once\n\n")
        f.write("namespace EvalWeights {\n")
        for name, value in sorted(weights.items()):
            rule_name = name.replace("rule_", "")
            f.write(f"    constexpr int W_{rule_name} = {int(round(value))};\n")
        f.write("}\n")
```

---

## Practical Considerations

### Data Filtering

Not all positions from games are equally useful for training:

| Filter | Rationale |
|---|---|
| Remove first 10 moves | Opening theory, not evaluation-dependent |
| Remove positions with extreme evals (|S| > 1000cp) | Decisive positions don't test subtlety |
| Remove time trouble positions | Low quality play distorts outcomes |
| Use only games with both players > 2500 Elo | High-quality play ensures reliable outcomes |
| Remove book draw positions | Don't penalize correct evaluations |

### Mini-Batch Size

Chess tuning benefits from **large batch sizes** (8192–65536). The loss landscape is smooth, and large batches provide stable gradient estimates. Small batches introduce too much noise.

### Learning Rate Schedule

A common schedule:

```
Epochs 0-20:    lr = 1.0
Epochs 20-50:   lr = 0.5
Epochs 50-100:  lr = 0.1
Epochs 100+:    lr = 0.01
```

### Convergence Criterion

The optimization has converged when the validation loss stops improving for `patience` epochs. Typical convergence: 50-150 epochs.

---

## Connections

- **Previous**: [[The Tuning Problem]] — Why tuning is needed
- **Next**: [[Credit Assignment Problem]] — Why correlated features make tuning harder
- **Related**: [[L1 Regularization and Sparsity]] — Ensuring sparse, interpretable weights
- **Related**: [[Constrained Optimization]] — Domain constraints during training
- **Related**: [[Feature Orthogonality Design]] — Designing features that are easier to tune
