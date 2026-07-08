# Feature Orthogonality Design

> **Chapter 11 — Parameter Tuning & Optimization** | ← [[Constrained Optimization]] | Return to [[The Tuning Problem]]

---

## The Orthogonality Principle

Two features are **orthogonal** if they can never both be active (non-zero) in the same position. Formally, features $F_j$ and $F_k$ are orthogonal if:

$$P(F_j \neq 0 \land F_k \neq 0) = 0$$

In other words, there is no chess position where both rules fire simultaneously. This eliminates the correlation that causes the [[Credit Assignment Problem|credit assignment problem]] and makes [[Texel Tuning Method|weight tuning]] much more reliable.

### Why Orthogonality Matters

| Property | Orthogonal Features | Correlated Features |
|---|---|---|
| Weight tuning | Well-conditioned, unique solution | Ill-conditioned, many equivalent solutions |
| Credit assignment | Clear, unambiguous | Diluted, ambiguous |
| Explanation clarity | One reason per delta | Multiple overlapping reasons |
| Constraint satisfaction | Fewer violations | Frequent violations |
| L1 effectiveness | True zero elimination | May zero the wrong feature |

---

## Bad Design: Overlapping Rules

### Example 1: Is_Check and Is_Queen_Check

```python
# BAD: These rules always overlap
def eval_is_check(pos):
    """Returns 1 if the side to move is in check."""
    return 1 if pos.in_check() else 0

def eval_is_queen_check(pos):
    """Returns 1 if the side to move is in check from a queen."""
    return 1 if pos.in_check() and pos.checker_type() == QUEEN else 0
```

**Problem**: Whenever `Is_Queen_Check` fires, `Is_Check` also fires. They are perfectly correlated on the subset of queen check positions. The optimizer can't assign independent weights.

**Consequence for explanation**: "The move delivers a check and a queen check" — redundant and confusing.

### Example 2: Knight_Outpost and Center_Control

```python
# BAD: Outposts are usually in the center, creating correlation
def eval_knight_outpost(pos):
    """Bonus for knight on a square not attackable by enemy pawns."""
    if pos.knight_on_outpost():
        return KNIGHT_OUTPOST_BONUS
    return 0

def eval_center_control(pos):
    """Bonus for controlling central squares (d4, d5, e4, e5)."""
    return count_center_controls(pos) * CENTER_CONTROL_PER_SQUARE
```

**Problem**: A knight on e5 (a central outpost) triggers both rules. The optimizer splits credit between them, and explanations become muddled: "The move improves the knight outpost and center control" — when the outpost IS the center control.

### Example 3: Pawn_Structure and Doubled_Pawns

```python
# BAD: Doubled pawns is a subset of pawn structure
def eval_pawn_structure(pos):
    """Overall pawn structure assessment."""
    score = 0
    score += eval_doubled_pawns(pos)
    score += eval_isolated_pawns(pos)
    score += eval_backward_pawns(pos)
    score += eval_pawn_chains(pos)
    return score

def eval_doubled_pawns(pos):
    """Penalty specifically for doubled pawns."""
    return -DOUBLED_PAWN_PENALTY * count_doubled_pawns(pos)
```

**Problem**: `Doubled_Pawns` is already included in `Pawn_Structure`. Having both as separate rules means the doubled pawn penalty is applied twice, and the optimizer has to figure out the split.

---

## Good Design: Orthogonal Rules

### Example 1: Minor_Piece_Check and Major_Piece_Check

```python
# GOOD: Mutually exclusive — a check is either by a minor or major piece
def eval_minor_piece_check(pos):
    """Bonus for check from knight or bishop."""
    if pos.in_check() and pos.checker_type() in (KNIGHT, BISHOP):
        return MINOR_CHECK_BONUS
    return 0

def eval_major_piece_check(pos):
    """Bonus for check from rook or queen."""
    if pos.in_check() and pos.checker_type() in (ROOK, QUEEN):
        return MAJOR_CHECK_BONUS
    return 0
```

**Why it's orthogonal**: A check comes from exactly one piece. If it's a minor piece check, it can't also be a major piece check. These rules partition the "check" space into two non-overlapping subsets.

### Example 2: Kingside_Attack and Queenside_Play

```python
# GOOD: Board sectors are disjoint
def eval_kingside_attack(pos):
    """Bonus for attacking the opponent's kingside (files a-e for Black)."""
    if pos.opponent_king_file() <= 4:  # King on a-e
        return compute_kingside_attack(pos) * KINGSIDE_ATTACK_WEIGHT
    return 0

def eval_queenside_play(pos):
    """Bonus for queenside play (files d-h for opponent)."""
    if pos.opponent_king_file() >= 4:  # King on d-h
        return compute_queenside_play(pos) * QUEENSIDE_PLAY_WEIGHT
    return 0
```

**Why it's orthogonal**: While there's a small overlap when the king is on the d- or e-file, the attack patterns are fundamentally different. Kingside attacks involve pawn storms and piece sacrifices; queenside play involves pawn majorities and space advantages.

### Example 3: Piece-Specific Outpost Rules

```python
# GOOD: Different pieces, different outpost characteristics
def eval_knight_outpost(pos):
    """Bonus for knight on a supported, unchallengeable square."""
    # Knight outposts: supported by own pawns, not attackable by enemy pawns
    return compute_knight_outpost_score(pos) * KNIGHT_OUTPOST_W

def eval_bishop_outpost(pos):
    """Bonus for bishop on a strong diagonal anchor point."""
    # Bishop "outposts": less common, but bishops can be strong on
    # fixed diagonals (e.g., g7 fianchetto bishop)
    return compute_bishop_outpost_score(pos) * BISHOP_OUTPOST_W
```

**Why it's orthogonal**: A square occupied by a knight cannot simultaneously be occupied by a bishop. The rules fire on different squares and have different evaluation criteria.

---

## How to Audit Your Rule Set for Overlaps

### The Audit Algorithm

```python
import numpy as np
from itertools import combinations
from typing import List, Dict, Tuple

class OrthogonalityAuditor:
    """Audits a rule set for feature overlap and correlation."""

    def __init__(self, rule_engine, sample_positions: List[str]):
        """
        Args:
            rule_engine: The C++ rule engine (via ctypes)
            sample_positions: List of FEN strings for testing
        """
        self.engine = rule_engine
        self.positions = sample_positions
        self.feature_matrix = self._compute_features()

    def _compute_features(self) -> np.ndarray:
        """Compute all features for all sample positions."""
        n_positions = len(self.positions)
        n_features = self.engine.get_feature_count()

        matrix = np.zeros((n_positions, n_features), dtype=np.float32)

        for i, fen in enumerate(self.positions):
            features = self.engine.extract_features(fen)
            matrix[i] = features

        return matrix

    def find_highly_correlated_pairs(self,
                                      threshold: float = 0.5
                                      ) -> List[dict]:
        """Find pairs of features with correlation above threshold."""
        n_features = self.feature_matrix.shape[1]
        results = []

        for j, k in combinations(range(n_features), 2):
            col_j = self.feature_matrix[:, j]
            col_k = self.feature_matrix[:, k]

            # Skip pairs where either feature is constant
            if np.std(col_j) < 1e-6 or np.std(col_k) < 1e-6:
                continue

            correlation = np.corrcoef(col_j, col_k)[0, 1]

            if abs(correlation) > threshold:
                results.append({
                    'feature_j': j,
                    'feature_k': k,
                    'correlation': correlation,
                    'co_activation_rate': self._co_activation_rate(j, k),
                    'severity': (
                        'critical' if abs(correlation) > 0.8
                        else 'high' if abs(correlation) > 0.6
                        else 'moderate'
                    )
                })

        # Sort by absolute correlation, descending
        results.sort(key=lambda x: abs(x['correlation']), reverse=True)
        return results

    def _co_activation_rate(self, j: int, k: int) -> float:
        """Fraction of positions where both features are non-zero."""
        both_active = np.sum(
            (self.feature_matrix[:, j] != 0) &
            (self.feature_matrix[:, k] != 0)
        )
        return both_active / len(self.positions)

    def find_subset_relationships(self) -> List[dict]:
        """Find feature pairs where one is always active when the other is."""
        n_features = self.feature_matrix.shape[1]
        results = []

        for j, k in combinations(range(n_features), 2):
            active_j = self.feature_matrix[:, j] != 0
            active_k = self.feature_matrix[:, k] != 0

            # Is j always active when k is active? (j is a subset of k)
            if np.sum(active_k) > 0:
                j_given_k = np.sum(active_j & active_k) / np.sum(active_k)
            else:
                j_given_k = 0

            # Is k always active when j is active? (k is a subset of j)
            if np.sum(active_j) > 0:
                k_given_j = np.sum(active_j & active_k) / np.sum(active_j)
            else:
                k_given_j = 0

            if j_given_k > 0.9:
                results.append({
                    'subset_feature': j,
                    'superset_feature': k,
                    'conditional_prob': j_given_k,
                    'direction': f'F_{j} ⊆ F_{k}',
                    'recommendation': f'Consider merging F_{j} into F_{k} or making them orthogonal'
                })

            if k_given_j > 0.9:
                results.append({
                    'subset_feature': k,
                    'superset_feature': j,
                    'conditional_prob': k_given_j,
                    'direction': f'F_{k} ⊆ F_{j}',
                    'recommendation': f'Consider merging F_{k} into F_{j} or making them orthogonal'
                })

        return results

    def generate_report(self, correlation_threshold: float = 0.5
                         ) -> dict:
        """Generate a complete orthogonality audit report."""
        correlated = self.find_highly_correlated_pairs(correlation_threshold)
        subsets = self.find_subset_relationships()

        # Compute overall orthogonality score
        n_features = self.feature_matrix.shape[1]
        n_pairs = n_features * (n_features - 1) // 2
        n_violations = len(correlated)
        orthogonality_score = 1.0 - (n_violations / max(n_pairs, 1))

        return {
            'orthogonality_score': orthogonality_score,
            'total_feature_pairs': n_pairs,
            'correlated_pairs': n_violations,
            'critical_correlations': [
                r for r in correlated if r['severity'] == 'critical'
            ],
            'subset_relationships': subsets,
            'recommendations': self._generate_recommendations(
                correlated, subsets
            )
        }

    def _generate_recommendations(self, correlated, subsets):
        """Generate actionable recommendations for improving orthogonality."""
        recs = []

        for pair in correlated:
            if pair['severity'] == 'critical':
                recs.append(
                    f"CRITICAL: Features {pair['feature_j']} and "
                    f"{pair['feature_k']} have correlation "
                    f"{pair['correlation']:.3f}. "
                    f"Redesign one to eliminate overlap. "
                    f"Co-activation rate: {pair['co_activation_rate']:.1%}"
                )

        for sub in subsets:
            recs.append(
                f"SUBSET: {sub['direction']} with conditional probability "
                f"{sub['conditional_prob']:.1%}. {sub['recommendation']}"
            )

        return recs
```

---

## The Orthogonality Test

### Formal Definition

Two rules $R_j$ and $R_k$ pass the orthogonality test if there exists **no position** where both rules produce non-zero scores:

$$\forall \text{Position } P: \neg (F_j(P) \neq 0 \land F_k(P) \neq 0)$$

In practice, we test this on a large sample of positions:

```python
def orthogonality_test(rule_j_name: str, rule_k_name: str,
                        positions: List[str],
                        engine,
                        tolerance: float = 0.01) -> dict:
    """Test whether two rules are orthogonal on a position sample.

    Returns:
        dict with 'is_orthogonal', 'co_activation_rate', and 'positions_violating'
    """
    co_activations = 0
    violating_positions = []

    for fen in positions:
        features = engine.extract_features(fen)
        val_j = features[rule_j_name]
        val_k = features[rule_k_name]

        if abs(val_j) > tolerance and abs(val_k) > tolerance:
            co_activations += 1
            violating_positions.append(fen)

    rate = co_activations / len(positions)

    return {
        'rule_j': rule_j_name,
        'rule_k': rule_k_name,
        'is_orthogonal': rate < 0.01,  # Less than 1% co-activation
        'co_activation_rate': rate,
        'positions_violating': violating_positions[:10],  # Sample
        'recommendation': (
            'PASS: Rules are orthogonal' if rate < 0.01
            else 'FAIL: Redesign to eliminate overlap' if rate > 0.1
            else 'WARNING: Minor overlap, consider redesigning'
        )
    }
```

---

## Redesign Strategies

When the audit finds overlapping rules, here are the strategies to make them orthogonal:

### Strategy 1: Partition (Split into Mutually Exclusive Categories)

Instead of:
```
Is_Check (fires for all checks)
Is_Queen_Check (fires for queen checks — subset!)
```

Redesign as:
```
Is_Minor_Check (knight or bishop check)
Is_Major_Check (rook or queen check)
Is_Discovered_Check (check from piece behind the moving piece)
Is_Double_Check (two pieces checking simultaneously)
```

These are mutually exclusive categories that cover all check types.

### Strategy 2: Decompose (Factor Out the Shared Component)

Instead of:
```
Knight_Outpost (fires for knight on unchallengeable square)
Center_Control (fires for pieces controlling center — overlaps with outpost)
```

Redesign as:
```
Knight_Outpost_Support (knight on a square supported by own pawn)
Knight_Outpost_Unchallengeable (no enemy pawn can attack the knight's square)
Center_Pawn_Control (pawns controlling d4/d5/e4/e5 — not pieces!)
```

Now `Knight_Outpost` has been decomposed into two more specific features, and `Center_Control` is restricted to pawns only (not pieces), eliminating the overlap.

### Strategy 3: Hierarchy (Use a Tree, Not a Flat List)

Instead of flat rules, organize in a hierarchy:

```
Positional_Advantage
├── Structure
│   ├── Pawn_Chain (+)
│   ├── Doubled_Pawns (-)
│   ├── Isolated_Pawn (-)
│   └── Passed_Pawn (+)
├── Piece_Quality
│   ├── Knight_Outpost (+)
│   ├── Bad_Bishop (-)
│   ├── Bishop_Pair (+)
│   └── Rook_Open_File (+)
└── King
    ├── King_Safety (+)
    ├── King_Protection (+)
    └── King_Activity_EG (+)
```

At each level, the children are orthogonal. The parent score is a weighted sum of children. This allows both fine-grained and coarse-grained explanations.

---

## Measuring Orthogonality Improvement

After redesigning rules, re-run the audit and track improvement:

```python
def measure_improvement(before_report: dict, after_report: dict) -> dict:
    """Compare orthogonality before and after rule redesign."""
    return {
        'orthogonality_score_before': before_report['orthogonality_score'],
        'orthogonality_score_after': after_report['orthogonality_score'],
        'improvement': (
            after_report['orthogonality_score'] -
            before_report['orthogonality_score']
        ),
        'critical_correlations_before': len(
            before_report['critical_correlations']
        ),
        'critical_correlations_after': len(
            after_report['critical_correlations']
        ),
        'subset_relationships_before': len(
            before_report['subset_relationships']
        ),
        'subset_relationships_after': len(
            after_report['subset_relationships']
        ),
    }
```

### Target Metrics

| Metric | Minimum | Target | Excellent |
|---|---|---|---|
| Orthogonality score | 0.80 | 0.90 | 0.95 |
| Critical correlations | < 10 | < 5 | 0 |
| Subset relationships | < 15 | < 5 | 0 |
| Co-activation rate (avg) | < 15% | < 8% | < 3% |

---

## Connections

- **Previous**: [[Constrained Optimization]] — Constraints complement orthogonality
- **Upstream**: [[Credit Assignment Problem]] — The problem orthogonality solves
- **Upstream**: [[The Tuning Problem]] — Why well-designed features matter
- **Downstream**: [[Declarative Rule Engine with Bitboards]] — Implementation of orthogonal rules
- **Downstream**: [[Explanation Quality Metrics]] — How orthogonality improves explanations
- **Related**: [[L1 Regularization and Sparsity]] — L1 helps when perfect orthogonality isn't achievable
