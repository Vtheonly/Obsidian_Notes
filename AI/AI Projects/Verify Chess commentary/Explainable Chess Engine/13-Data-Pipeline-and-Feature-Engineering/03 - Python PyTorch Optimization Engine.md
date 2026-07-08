# Python PyTorch Optimization Engine

> **Chapter 13.03** | [[02 - Feature Extraction in C++|Prev: Feature Extraction in C++]] | [[04 - The Puzzle Database System|Next: Puzzle Database]]
> **Related**: [[01 - Data Pipeline Architecture|Data Pipeline]], [[02 - Feature Extraction in C++|Feature Extraction]], [[05 - Android Puzzle App Architecture|Android App]]

---

## Overview

The Python PyTorch Optimization Engine is the training pipeline that takes the feature vectors extracted by the [[02 - Feature Extraction in C++|C++ Feature Extractor]] and learns the optimal weights for each rule in the [[Explainable Chess Engine]]. The core technique is **Texel Tuning** — a regression method originally developed for chess engines that optimizes evaluation parameters by minimizing the prediction error against game outcomes.

Unlike deep neural network approaches (like AlphaZero), the Texel Tuning approach maintains full interpretability: every weight corresponds directly to a human-understandable rule, and the trained model can be explained in plain English.

---

## The TexelTuner Model Architecture

### Why a Linear Model?

The [[Explainable Chess Engine]] requires that every component of the evaluation be explainable. A deep neural network with millions of parameters would produce accurate evaluations but no explanations. A linear model with constrained weights produces evaluations **and** explanations:

$$\text{evaluation}(p) = \sum_{i=1}^{220} w_i \cdot f_i(p)$$

Where:
- $f_i(p)$ is the $i$-th feature value for position $p$ (extracted by C++)
- $w_i$ is the learned weight for feature $i$
- The evaluation is a simple weighted sum — each term is directly explainable

### The Sigmoid Mapping

The raw evaluation (in centipawns) is mapped to a win probability using the sigmoid function:

$$\sigma(E) = \frac{1}{1 + e^{-E/K}}$$

Where $K$ is a scaling constant (typically $K = 400$ for centipawn evaluations). The training objective is to make the predicted win probability match the actual game result.

### PyTorch Model Definition

```python
# texel_tuner.py
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional, Tuple

class TexelTuner(nn.Module):
    """
    A linear model for chess evaluation tuning.

    Each weight corresponds to a human-understandable feature.
    The model outputs a win probability after sigmoid transformation.

    Architecture:
        Input (220 features) → Linear (220 weights, no bias) → Sigmoid → Win Probability
    """

    def __init__(self, num_features: int = 220, k_factor: float = 400.0):
        super().__init__()
        self.num_features = num_features
        self.k_factor = k_factor

        # Single linear layer — no bias, no hidden layers
        # This ensures every parameter is directly interpretable
        self.linear = nn.Linear(num_features, 1, bias=False)

        # Initialize weights to reasonable chess values
        self._initialize_weights()

    def _initialize_weights(self):
        """Initialize weights to approximate known chess heuristics."""
        with torch.no_grad():
            weights = self.linear.weight.data[0]

            # Material weights (features 120-129)
            weights[120] = 1.0    # white_material (centipawn scale)
            weights[121] = -1.0   # black_material
            weights[122] = 1.0    # material_diff

            # Bishop pair bonus (~50 centipawns)
            weights[2] = 50.0     # bishop_pair_w
            weights[3] = -50.0    # bishop_pair_b

            # Isolated pawn penalty (~15 centipawns)
            weights[30] = -15.0   # isolated_pawn_w
            weights[31] = 15.0    # isolated_pawn_b (good for Black's opponent)

            # Passed pawn bonus (~30 centipawns)
            weights[34] = 30.0    # passed_pawn_w
            weights[35] = -30.0   # passed_pawn_b

            # King safety
            weights[55] = 40.0    # pawn_shield_intact_w

            # Piece activity
            weights[60] = -20.0   # bad_bishop_w (penalty)
            weights[61] = 25.0    # knight_outpost_w (bonus)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass: features → evaluation → win probability

        Args:
            features: Tensor of shape (batch_size, num_features)

        Returns:
            Win probability tensor of shape (batch_size, 1)
        """
        # Linear combination: sum of weighted features
        raw_eval = self.linear(features)  # Shape: (batch_size, 1)

        # Scale by K factor and apply sigmoid
        # Dividing by k_factor converts centipawns to sigmoid input range
        win_probability = torch.sigmoid(raw_eval / self.k_factor)

        return win_probability

    def get_evaluation(self, features: torch.Tensor) -> torch.Tensor:
        """Get raw centipawn evaluation (before sigmoid)."""
        return self.linear(features)

    def get_weight_dict(self) -> Dict[str, float]:
        """Export weights as a dictionary mapping feature names to values."""
        feature_names = self.get_feature_names()
        weights = self.linear.weight.data[0].cpu().numpy()
        return {name: float(w) for name, w in zip(feature_names, weights)}

    @staticmethod
    def get_feature_names() -> List[str]:
        """Return ordered list of feature names matching the C++ extractor."""
        names = []

        # Material rules (0-19)
        names.extend([
            "has_queen_w", "has_queen_b", "bishop_pair_w", "bishop_pair_b",
            "rook_pair_w", "rook_pair_b", "no_bishops_w", "no_bishops_b",
            "opposite_bishops", "has_rook_w", "has_rook_b",
            "has_knight_w", "has_knight_b", "queen_vs_minor_w",
            "queen_vs_minor_b", "rook_vs_pawn_w", "rook_vs_pawn_b",
            "heavy_piece_imbalance_w", "heavy_piece_imbalance_b",
            "total_piece_count"
        ])

        # Pawn structure rules (20-49)
        names.extend([
            "isolated_pawn_w", "isolated_pawn_b", "doubled_pawn_w",
            "doubled_pawn_b", "passed_pawn_w", "passed_pawn_b",
            "backward_pawn_w", "backward_pawn_b", "pawn_chain_w",
            "pawn_chain_b", "connected_passed_pawns_w",
            "connected_passed_pawns_b", "pawn_island_w", "pawn_island_b",
            "candidate_passed_w", "candidate_passed_b",
            "protected_pawn_w", "protected_pawn_b",
            "half_open_file_w", "half_open_file_b",
            "full_open_file_w", "full_open_file_b",
            "pawn_break_possible_w", "pawn_break_possible_b",
            "center_pawns_w", "center_pawns_b",
            "wing_pawns_w", "wing_pawns_b",
            "blocked_pawn_w", "blocked_pawn_b"
        ])

        # King safety rules (50-74)
        names.extend([
            "can_castle_king_side_w", "can_castle_queen_side_w",
            "has_castled_w", "has_castled_b",
            "king_exposed_w", "king_exposed_b",
            "open_file_near_king_w", "open_file_near_king_b",
            "semi_open_file_near_king_w", "semi_open_file_near_king_b",
            "pawn_shield_intact_w", "pawn_shield_intact_b",
            "king_in_corner_w", "king_in_corner_b",
            "king_in_center_w", "king_in_center_b",
            "king_attackers_near_w", "king_attackers_near_b",
            "king_tropism_w", "king_tropism_b"
        ])

        # ... Continue for all 220 features
        # (Abbreviated for clarity — the full list is in feature_names.py)

        return names
```

---

## Loading C++ Extracted Features into PyTorch Tensors

### The Dataset Class

```python
# chess_dataset.py
import torch
from torch.utils.data import Dataset, DataLoader
import sqlite3
import numpy as np
import struct
from pathlib import Path

class ChessPositionDataset(Dataset):
    """
    PyTorch Dataset that loads chess positions from the SQLite database
    produced by the [[01 - Data Pipeline Architecture|C++ Data Pipeline]].

    Each sample is:
        - features: FloatTensor of shape (220,) — the feature vector
        - result: FloatTensor of shape (1,) — game result from mover's perspective
    """

    def __init__(
        self,
        db_path: str,
        min_elo: int = 2000,
        max_positions: Optional[int] = None,
        normalize_features: bool = True
    ):
        self.db_path = db_path
        self.normalize_features = normalize_features

        # Connect and load data
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Count total positions
        self.cursor.execute("SELECT COUNT(*) FROM training_positions")
        self.total_count = self.cursor.fetchone()[0]

        # Load positions into memory (for faster access)
        # For very large datasets, use a streaming approach instead
        query = """
            SELECT feature_vector, result
            FROM training_positions
            WHERE elo_white >= ? AND elo_black >= ?
        """
        params = [min_elo, min_elo]

        if max_positions:
            query += " ORDER BY RANDOM() LIMIT ?"
            params.append(max_positions)

        self.cursor.execute(query, params)

        self.features_list = []
        self.results_list = []

        for feature_blob, result in self.cursor:
            # Unpack binary feature vector
            num_features = len(feature_blob) // 4  # 4 bytes per float
            features = struct.unpack(f'{num_features}f', feature_blob)
            self.features_list.append(features)
            self.results_list.append(result)

        self.features = torch.tensor(self.features_list, dtype=torch.float32)
        self.results = torch.tensor(self.results_list, dtype=torch.float32).unsqueeze(1)

        # Normalize features to [0, 1] range where appropriate
        if self.normalize_features:
            self._normalize()

        print(f"Loaded {len(self)} positions from {db_path}")

    def _normalize(self):
        """Normalize numeric features to reasonable ranges."""
        # Binary features (0-119) are already in [0, 1]
        # Numeric features (120-199) need normalization
        numeric_start = 120
        numeric_end = 200

        # Compute mean and std for numeric features
        numeric = self.features[:, numeric_start:numeric_end]
        self.feature_mean = numeric.mean(dim=0)
        self.feature_std = numeric.std(dim=0)
        self.feature_std[self.feature_std < 1e-6] = 1.0  # Prevent division by zero

        # Standardize
        self.features[:, numeric_start:numeric_end] = (
            numeric - self.feature_mean
        ) / self.feature_std

    def __len__(self) -> int:
        return len(self.results)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.features[idx], self.results[idx]

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
```

### Creating DataLoaders

```python
def create_dataloaders(
    db_path: str,
    batch_size: int = 16384,
    train_ratio: float = 0.9,
    min_elo: int = 2000
) -> Tuple[DataLoader, DataLoader]:
    """Create train/validation DataLoaders from the SQLite database."""

    dataset = ChessPositionDataset(db_path, min_elo=min_elo)

    # Split into train/val
    train_size = int(train_ratio * len(dataset))
    val_size = len(dataset) - train_size

    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )

    return train_loader, val_loader
```

---

## Training Loop with Gradient Descent

### The Loss Function

We use **Mean Squared Error** between predicted and actual results, which is the standard for Texel Tuning:

$$L = \frac{1}{N} \sum_{i=1}^{N} (\sigma(E_i / K) - R_i)^2$$

Where:
- $E_i$ is the raw evaluation for position $i$
- $\sigma$ is the sigmoid function
- $R_i$ is the game result (0, 0.5, or 1.0)
- $K$ is the scaling factor (400)

### Full Training Code

```python
# train.py
import torch
import torch.nn as nn
import torch.optim as optim
import json
import logging
from pathlib import Path
from typing import Dict, List

from texel_tuner import TexelTuner
from chess_dataset import create_dataloaders

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class TexelTrainer:
    """
    Training pipeline for the Explainable Chess Engine evaluation weights.

    Uses Texel Tuning: minimize MSE between predicted win probability
    and actual game outcomes.
    """

    def __init__(
        self,
        db_path: str,
        output_dir: str = "weights",
        num_features: int = 220,
        k_factor: float = 400.0,
        learning_rate: float = 0.01,
        weight_decay: float = 1e-4,
        batch_size: int = 16384,
        num_epochs: int = 100,
        early_stop_patience: int = 10,
        min_elo: int = 2000,
        device: str = "auto"
    ):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.num_features = num_features
        self.k_factor = k_factor
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.early_stop_patience = early_stop_patience
        self.min_elo = min_elo

        # Device selection
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        logger.info(f"Training on device: {self.device}")

    def train(self) -> Dict[str, float]:
        """Run the full training loop and return the final weights."""

        # Create model
        model = TexelTuner(
            num_features=self.num_features,
            k_factor=self.k_factor
        ).to(self.device)

        # Loss function: MSE between predicted and actual win probability
        criterion = nn.MSELoss()

        # Optimizer: Adam with weight decay for regularization
        optimizer = optim.Adam(
            model.parameters(),
            lr=self.learning_rate,
            weight_decay=self.weight_decay
        )

        # Learning rate scheduler: reduce on plateau
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=0.5,
            patience=3,
            verbose=True
        )

        # Load data
        train_loader, val_loader = create_dataloaders(
            self.db_path,
            batch_size=self.batch_size,
            min_elo=self.min_elo
        )

        # Training loop
        best_val_loss = float('inf')
        best_weights = None
        patience_counter = 0

        for epoch in range(self.num_epochs):
            # ---- Training Phase ----
            model.train()
            train_loss = 0.0
            train_samples = 0

            for batch_features, batch_results in train_loader:
                batch_features = batch_features.to(self.device)
                batch_results = batch_results.to(self.device)

                # Forward pass
                predictions = model(batch_features)

                # Compute loss
                loss = criterion(predictions, batch_results)

                # Backward pass
                optimizer.zero_grad()
                loss.backward()

                # Gradient clipping to prevent weight explosion
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

                # Update weights
                optimizer.step()

                # Track metrics
                train_loss += loss.item() * batch_features.size(0)
                train_samples += batch_features.size(0)

            avg_train_loss = train_loss / train_samples

            # ---- Validation Phase ----
            model.eval()
            val_loss = 0.0
            val_samples = 0
            correct_predictions = 0

            with torch.no_grad():
                for batch_features, batch_results in val_loader:
                    batch_features = batch_features.to(self.device)
                    batch_results = batch_results.to(self.device)

                    predictions = model(batch_features)
                    loss = criterion(predictions, batch_results)

                    val_loss += loss.item() * batch_features.size(0)
                    val_samples += batch_features.size(0)

                    # Accuracy: prediction > 0.5 means White wins
                    predicted_winner = (predictions > 0.5).float()
                    actual_winner = (batch_results > 0.5).float()
                    correct_predictions += (predicted_winner == actual_winner).sum().item()

            avg_val_loss = val_loss / val_samples
            val_accuracy = correct_predictions / val_samples

            # Update learning rate
            scheduler.step(avg_val_loss)

            logger.info(
                f"Epoch {epoch+1}/{self.num_epochs} | "
                f"Train Loss: {avg_train_loss:.6f} | "
                f"Val Loss: {avg_val_loss:.6f} | "
                f"Val Accuracy: {val_accuracy:.4f} | "
                f"LR: {optimizer.param_groups[0]['lr']:.6f}"
            )

            # Early stopping check
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                best_weights = model.get_weight_dict()
                patience_counter = 0

                # Save best weights
                self._save_weights(best_weights, epoch + 1)
                logger.info(f"  → New best weights saved! (val_loss: {best_val_loss:.6f})")
            else:
                patience_counter += 1
                if patience_counter >= self.early_stop_patience:
                    logger.info(
                        f"Early stopping at epoch {epoch+1} "
                        f"(no improvement for {self.early_stop_patience} epochs)"
                    )
                    break

        return best_weights

    def _save_weights(self, weights: Dict[str, float], epoch: int):
        """Save weights to JSON file for the C++ engine to load."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_path = self.output_dir / f"weights_epoch_{epoch}.json"
        with open(output_path, 'w') as f:
            json.dump({
                "epoch": epoch,
                "k_factor": self.k_factor,
                "num_features": self.num_features,
                "weights": weights,
                "metadata": {
                    "description": "Explainable Chess Engine evaluation weights",
                    "format": "feature_name -> centipawn_value",
                    "positive_values": "beneficial for White",
                    "negative_values": "beneficial for Black"
                }
            }, f, indent=2)

        # Also save as "latest"
        latest_path = self.output_dir / "weights_latest.json"
        with open(latest_path, 'w') as f:
            json.dump(weights, f, indent=2)

        logger.info(f"Weights saved to {output_path} and {latest_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Train Explainable Chess Engine weights")
    parser.add_argument("--data", required=True, help="Path to SQLite training database")
    parser.add_argument("--output-dir", default="weights", help="Output directory for weights")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16384)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--k-factor", type=float, default=400.0)
    parser.add_argument("--min-elo", type=int, default=2000)
    args = parser.parse_args()

    trainer = TexelTrainer(
        db_path=args.data,
        output_dir=args.output_dir,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        k_factor=args.k_factor,
        min_elo=args.min_elo
    )

    weights = trainer.train()
    print("\n=== Top 10 Most Positive Weights (Good for White) ===")
    for name, value in sorted(weights.items(), key=lambda x: -x[1])[:10]:
        print(f"  {name}: {value:+.2f}")

    print("\n=== Top 10 Most Negative Weights (Good for Black) ===")
    for name, value in sorted(weights.items(), key=lambda x: x[1])[:10]:
        print(f"  {name}: {value:+.2f}")


if __name__ == "__main__":
    main()
```

---

## Weight Extraction and Export to JSON

### The Weight Export Format

The trained weights are exported as JSON for the C++ engine to load:

```json
{
  "epoch": 47,
  "k_factor": 400.0,
  "num_features": 220,
  "weights": {
    "has_queen_w": 0.0,
    "bishop_pair_w": 48.32,
    "bishop_pair_b": -47.91,
    "isolated_pawn_w": -18.45,
    "isolated_pawn_b": 17.23,
    "passed_pawn_w": 32.67,
    "passed_pawn_b": -31.89,
    "doubled_pawn_w": -12.34,
    "pawn_shield_intact_w": 42.11,
    "bad_bishop_w": -22.56,
    "knight_outpost_w": 27.89,
    "rook_on_7th_w": 55.23,
    "material_diff": 1.02,
    "knight_mobility_w": 3.45,
    "king_exposed_w": -65.78,
    "open_file_near_king_w": -35.12
  },
  "metadata": {
    "description": "Explainable Chess Engine evaluation weights",
    "format": "feature_name -> centipawn_value",
    "positive_values": "beneficial for White",
    "negative_values": "beneficial for Black"
  }
}
```

### How the C++ Engine Loads Weights

```cpp
// weight_loader.h
#pragma once
#include <string>
#include <unordered_map>
#include <fstream>
#include <nlohmann/json.hpp>

class WeightLoader {
public:
    struct WeightEntry {
        std::string name;
        float value;
        float min_constraint;  // Optional: force weight to stay positive/negative
        float max_constraint;
    };

    // Load weights from JSON file produced by PyTorch training
    static std::unordered_map<std::string, float> load_from_json(
        const std::string& json_path
    ) {
        std::ifstream file(json_path);
        if (!file.is_open()) {
            throw std::runtime_error("Cannot open weights file: " + json_path);
        }

        nlohmann::json j;
        file >> j;

        std::unordered_map<std::string, float> weights;

        // Handle both formats: full (with metadata) and simple (weights only)
        if (j.contains("weights")) {
            for (auto& [key, value] : j["weights"].items()) {
                weights[key] = value.get<float>();
            }
        } else {
            for (auto& [key, value] : j.items()) {
                weights[key] = value.get<float>();
            }
        }

        return weights;
    }

    // Validate weights against constraints
    static bool validate_weights(
        const std::unordered_map<std::string, float>& weights
    ) {
        // White features should generally be positive (good for White)
        // Black features should generally be negative (good for Black)
        // This is a soft constraint — violations are logged but not errors

        bool all_valid = true;
        for (const auto& [name, value] : weights) {
            // White symmetric features should be positive
            if (name.ends_with("_w") && value < -100.0f) {
                std::cerr << "WARNING: White feature " << name
                          << " has unexpectedly negative weight: " << value << std::endl;
                all_valid = false;
            }
            // Black symmetric features should be negative
            if (name.ends_with("_b") && value > 100.0f) {
                std::cerr << "WARNING: Black feature " << name
                          << " has unexpectedly positive weight: " << value << std::endl;
                all_valid = false;
            }
        }
        return all_valid;
    }
};
```

---

## Weight Constraints and Interpretability

### Enforcing Logical Constraints

To maintain interpretability, we can apply constraints during training:

```python
class ConstrainedTexelTuner(TexelTuner):
    """
    TexelTuner with weight constraints for logical consistency.

    Constraints ensure that:
    1. Symmetric features have symmetric weights (e.g., isolated_pawn_w = -isolated_pawn_b)
    2. Penalty features stay negative (e.g., isolated_pawn_w ≤ 0)
    3. Bonus features stay positive (e.g., passed_pawn_w ≥ 0)
    """

    def __init__(self, num_features: int = 220, k_factor: float = 400.0):
        super().__init__(num_features, k_factor)
        self._setup_constraints()

    def _setup_constraints(self):
        """Define weight constraints based on chess logic."""
        self.penalty_features = {
            30, 31,   # isolated_pawn_w, isolated_pawn_b
            32, 33,   # doubled_pawn_w, doubled_pawn_b
            36, 37,   # backward_pawn_w, backward_pawn_b
            60,       # bad_bishop_w
        }
        self.bonus_features = {
            34, 35,   # passed_pawn_w, passed_pawn_b
            55,       # pawn_shield_intact_w
            61,       # knight_outpost_w
        }

    def apply_constraints(self):
        """Apply constraints after each gradient step."""
        with torch.no_grad():
            weights = self.linear.weight.data[0]

            # Penalty features: White penalties should be ≤ 0
            for idx in self.penalty_features:
                if idx in self.penalty_features:
                    weights[idx] = torch.clamp(weights[idx], max=0.0)

            # Bonus features: should be ≥ 0
            for idx in self.bonus_features:
                if idx in self.bonus_features:
                    weights[idx] = torch.clamp(weights[idx], min=0.0)
```

### The Symmetry Constraint

For features that are symmetric (same concept for both sides), the weights should be equal in magnitude but opposite in sign:

```python
def enforce_symmetry(model: TexelTuner, feature_pairs: List[Tuple[int, int]]):
    """
    Enforce that symmetric feature pairs have weights equal in magnitude.

    For example: isolated_pawn_w should equal -isolated_pawn_b
    """
    with torch.no_grad():
        weights = model.linear.weight.data[0]

        for w_idx, b_idx in feature_pairs:
            # Average the magnitudes and apply signs
            w_val = weights[w_idx].item()
            b_val = weights[b_idx].item()

            # The symmetric value is the average magnitude
            avg_magnitude = (abs(w_val) + abs(b_val)) / 2.0

            weights[w_idx] = -avg_magnitude  # Penalty for White
            weights[b_idx] = avg_magnitude   # Bonus for Black's opponent

# Define symmetric pairs
SYMMETRIC_PAIRS = [
    (30, 31),  # isolated_pawn_w, isolated_pawn_b
    (32, 33),  # doubled_pawn_w, doubled_pawn_b
    (34, 35),  # passed_pawn_w, passed_pawn_b
    (36, 37),  # backward_pawn_w, backward_pawn_b
    (120, 121),  # material_w, material_b
]
```

---

## Evaluation: How Good Are the Weights?

### Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Validation MSE | Mean squared error on held-out positions | < 0.15 |
| Prediction Accuracy | Correct win/draw/loss prediction | > 70% |
| Weight Plausibility | Do weights match chess intuition? | Manual check |
| Correlation with Engines | Correlation with Stockfish eval | > 0.90 |

### Cross-Validation with Engine Evaluations

```python
def correlate_with_stockfish(weights: Dict[str, float], test_positions: List[str]):
    """Check correlation between our evaluation and Stockfish's."""
    import subprocess

    our_evals = []
    sf_evals = []

    for fen in test_positions:
        # Our evaluation
        features = extract_features(fen)  # Call C++ extractor
        our_eval = sum(w * f for w, f in zip(weights.values(), features))
        our_evals.append(our_eval)

        # Stockfish evaluation
        sf_eval = query_stockfish(fen)
        sf_evals.append(sf_eval)

    # Compute Pearson correlation
    correlation = np.corrcoef(our_evals, sf_evals)[0, 1]
    print(f"Correlation with Stockfish: {correlation:.4f}")
    return correlation
```

---

## The Complete Training Workflow

```bash
# Step 1: Run the C++ data pipeline
python run_pipeline.py --input /data/lichess_2023.pgn --output /data/training.db

# Step 2: Train weights with PyTorch
python train.py --data /data/training.db --output-dir weights --epochs 100 --lr 0.01

# Step 3: Validate weights against Stockfish
python validate_weights.py --weights weights/weights_latest.json --positions test_positions.fen

# Step 4: Export weights to C++ engine format
python export_weights.py --input weights/weights_latest.json --output src/engine/eval_weights.h

# Step 5: Recompile C++ engine with new weights
cd build && cmake .. && make -j8
```

---

## Summary

The Python PyTorch Optimization Engine provides:

1. **A linear model** (TexelTuner) where every weight is directly interpretable — no hidden layers, no black boxes
2. **Texel Tuning** methodology that optimizes evaluation weights against millions of game results
3. **Weight constraints** for logical consistency: penalties stay negative, bonuses stay positive, symmetric features maintain symmetry
4. **JSON export** format that bridges Python training and C++ inference
5. **Validation** against Stockfish evaluations to ensure the learned weights produce reasonable assessments
6. **Full interpretability**: the contribution of each rule to a position's evaluation is simply `weight × feature_value`

The trained weights flow directly into the [[Explainable Chess Engine]]'s evaluation function, where each active feature generates a [[RuleExplanation]] that can be presented to the user in plain language.
