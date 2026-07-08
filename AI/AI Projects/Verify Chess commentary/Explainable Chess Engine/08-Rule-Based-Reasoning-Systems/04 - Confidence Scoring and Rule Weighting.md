---
tags:
  - chapter-08
  - rule-engine
  - confidence-scoring
  - rule-weighting
  - dynamic-weights
  - normalization
  - explanation-pipeline
---

# 04 - Confidence Scoring and Rule Weighting

## Weight as Confidence

### The Dual Meaning of Weights

In our rule engine, the **weight** of a rule serves a dual purpose:

1. **Influence**: It determines how much the rule's score affects the total evaluation
2. **Confidence**: It represents how confident we are that the rule's score is correct

These two meanings are closely related: we want highly confident rules to have more influence, and less confident rules to have less influence. A rule with weight 1.0 is saying "I am completely confident in my score." A rule with weight 0.5 is saying "My score is an approximation; treat it as half as important."

### Confidence vs. Accuracy

It's important to distinguish **confidence** from **accuracy**:
- **Confidence**: How reliable the rule is across different positions
- **Accuracy**: How close the rule's score is to the "true" value in a specific position

A rule can be confident but inaccurate (consistently overvalues a feature) or accurate but not confident (correct in some positions, wrong in others). Our weight system primarily reflects confidence, while accuracy is addressed through score calibration.

## Normalizing to Percentages

### The Normalization Problem

Rule scores are in centipawns, but their raw magnitudes vary enormously. A material count rule might produce scores of ±1000cp, while a prophylaxis rule might produce scores of ±15cp. If we simply add these together, the material rule would dominate the evaluation, and the strategic rules would be irrelevant.

Normalization addresses this by scaling all rule scores to a comparable range. The most common approach is to normalize to **percentages of a reference value**:

$$s_i^{\text{norm}} = \frac{s_i}{\max(|s_i|)} \cdot 100$$

### Score Ranges by Category

```python
# Expected score ranges for each category (in centipawns)
CATEGORY_RANGES = {
    "material": (0, 3000),      # Material can be decisive
    "tactical": (0, 500),       # Tactical threats can be large
    "opening": (0, 100),        # Opening penalties are modest
    "trap": (0, 300),           # Traps can be significant
    "strategy": (0, 80),        # Strategic factors are moderate
    "safety": (0, 400),         # Safety can be game-deciding
}

def normalize_score(score: int, category: str) -> float:
    """
    Normalize a score to a percentage of its category's typical range.
    """
    min_score, max_score = CATEGORY_RANGES.get(category, (0, 100))
    range_size = max_score - min_score
    
    if range_size == 0:
        return 0.0
    
    # Normalize to [-100, 100] percentage
    normalized = (score / range_size) * 100
    return max(-100, min(100, normalized))  # Clamp
```

### Percentage-Based Explanations

When scores are normalized to percentages, the explanation can use more intuitive language:

| Percentage | Description |
|-----------|-------------|
| 90-100% | "Decisive advantage" |
| 60-90% | "Significant advantage" |
| 30-60% | "Clear advantage" |
| 10-30% | "Slight advantage" |
| -10 to 10% | "Roughly equal" |
| -30 to -10% | "Slight disadvantage" |
| -60 to -30% | "Clear disadvantage" |
| -100 to -60% | "Significant disadvantage" |

## Rule Activation Strength

### Not All Firings Are Equal

A rule **fires** when its condition is met, but the **strength** of the firing varies. Consider the Isolated Pawn rule:
- A single isolated pawn on the edge of the board: **Weak activation** (minor penalty)
- A central isolated queen pawn in the middlegame: **Strong activation** (significant penalty)
- Two isolated pawns in a complex position: **Very strong activation** (major penalty)

The activation strength reflects the *degree* to which the rule's condition is met, not just whether it's met at all.

```python
class RuleActivation:
    """
    Represents the activation strength of a rule.
    Strength ranges from 0.0 (not activated) to 1.0 (fully activated).
    """
    
    def __init__(self, rule_name: str, strength: float, score: int, reason: str):
        self.rule_name = rule_name
        self.strength = strength  # 0.0 to 1.0
        self.score = score
        self.reason = reason
    
    @property
    def effective_score(self) -> int:
        """The score adjusted by activation strength."""
        return int(self.score * self.strength)
    
    @property
    def effective_weight(self) -> float:
        """The weight adjusted by activation strength."""
        rule = get_rule_by_name(self.rule_name)
        return rule.weight * self.strength
    
    def __repr__(self) -> str:
        return (f"Activation({self.rule_name}, strength={self.strength:.2f}, "
                f"score={self.score}, effective={self.effective_score})")
```

### Computing Activation Strength

```python
def compute_activation_strength(rule: Rule, board: chess.Board, 
                                 color: chess.Color) -> float:
    """
    Compute how strongly a rule activates for the given position.
    Returns a value from 0.0 (not activated) to 1.0 (fully activated).
    """
    # The base activation is whether the rule fires at all
    score, reason = rule.evaluate(board, color=color)
    
    if not reason:  # Rule didn't fire
        return 0.0
    
    # The activation strength depends on the score magnitude
    # relative to the rule's typical range
    min_score, max_score = CATEGORY_RANGES.get(rule.category, (0, 100))
    typical_range = max_score
    
    # Strength = min(1.0, |score| / typical_threshold)
    threshold = typical_range * 0.3  # 30% of typical range = moderate activation
    strength = min(1.0, abs(score) / threshold)
    
    return strength
```

## Dynamic and Context-Dependent Weights

### The Problem with Static Weights

Static weights assume that a rule's importance is the same in every position. But in chess, the importance of strategic features depends heavily on context:

- **Material balance**: When ahead in material, safety rules become more important (protect your advantage)
- **Game phase**: Pawn structure matters more in the endgame; king safety matters more in the middlegame
- **Position type**: In open positions, piece activity dominates; in closed positions, pawn structure dominates
- **Tactical situation**: When significant tactics exist, positional rules should be deprioritized

### Context-Dependent Weight Adjustment

```python
class DynamicWeightCalculator:
    """
    Adjusts rule weights based on the current game context.
    """
    
    def __init__(self, base_weights: dict[str, float]):
        self.base_weights = base_weights
    
    def compute_weights(self, board: chess.Board) -> dict[str, float]:
        """
        Compute context-adjusted weights for all rules.
        """
        weights = dict(self.base_weights)
        
        # Factor 1: Game phase
        phase = self._compute_game_phase(board)
        weights = self._adjust_for_phase(weights, phase)
        
        # Factor 2: Material balance
        material_balance = self._compute_material_balance(board)
        weights = self._adjust_for_material(weights, material_balance)
        
        # Factor 3: Position openness
        openness = self._compute_position_openness(board)
        weights = self._adjust_for_openness(weights, openness)
        
        # Factor 4: Tactical density
        tactical_density = self._compute_tactical_density(board)
        weights = self._adjust_for_tactics(weights, tactical_density)
        
        return weights
    
    def _compute_game_phase(self, board: chess.Board) -> str:
        """
        Determine the game phase based on material on the board.
        """
        total_material = 0
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece and piece.piece_type not in [chess.PAWN, chess.KING]:
                total_material += PIECE_VALUES.get(piece.piece_type, 0)
        
        if total_material > 5000:
            return "opening"
        elif total_material > 2500:
            return "middlegame"
        else:
            return "endgame"
    
    def _adjust_for_phase(self, weights: dict[str, float], phase: str) -> dict[str, float]:
        """Adjust weights based on game phase."""
        adjusted = dict(weights)
        
        if phase == "opening":
            adjusted["Development"] *= 1.5
            adjusted["Castling"] *= 1.5
            adjusted["Central Control"] *= 1.3
            adjusted["Queen Early"] *= 1.2
        elif phase == "middlegame":
            adjusted["King Exposure"] *= 1.3
            adjusted["Attack Units"] *= 1.2
            adjusted["Knight Outpost"] *= 1.2
        elif phase == "endgame":
            adjusted["Pawn Structure"] *= 1.3
            adjusted["Rook on Open File"] *= 1.2
            adjusted["Material Count"] *= 1.5
            adjusted["Development"] *= 0.3  # Less relevant in endgame
        
        return adjusted
    
    def _adjust_for_material(self, weights: dict[str, float], balance: int) -> dict[str, float]:
        """Adjust weights based on material balance."""
        adjusted = dict(weights)
        
        if abs(balance) > 200:  # Significant material advantage
            # When ahead, prioritize safety; simplify
            adjusted["King Exposure"] *= 1.3
            adjusted["Pawn Shield"] *= 1.2
            adjusted["LPDO Detection"] *= 1.2
            # Deprioritize risky strategies
            adjusted["Sacrifice Pattern"] *= 0.5
        
        return adjusted
    
    def _compute_position_openness(self, board: chess.Board) -> float:
        """
        Compute how open the position is (0.0 = closed, 1.0 = open).
        Based on number of open files and diagonals.
        """
        open_files = 0
        for file_idx in range(8):
            has_pawn = False
            for rank_idx in range(8):
                sq = chess.square(file_idx, rank_idx)
                piece = board.piece_at(sq)
                if piece and piece.piece_type == chess.PAWN:
                    has_pawn = True
                    break
            if not has_pawn:
                open_files += 1
        
        # Normalize: 0 open files = closed, 4+ open files = very open
        return min(1.0, open_files / 4.0)
    
    def _adjust_for_openness(self, weights: dict[str, float], openness: float) -> dict[str, float]:
        """Adjust weights based on position openness."""
        adjusted = dict(weights)
        
        if openness > 0.5:  # Open position
            adjusted["Rook on Open File"] *= 1.0 + openness * 0.5
            adjusted["Mobility"] *= 1.0 + openness * 0.3
            adjusted["Knight Outpost"] *= 1.0 - openness * 0.2  # Less important in open positions
        else:  # Closed position
            adjusted["Knight Outpost"] *= 1.0 + (1 - openness) * 0.3
            adjusted["Pawn Structure"] *= 1.0 + (1 - openness) * 0.2
            adjusted["Bad Bishop"] *= 1.0 + (1 - openness) * 0.3
        
        return adjusted
    
    def _compute_tactical_density(self, board: chess.Board) -> float:
        """
        Compute how tactically dense the position is.
        Higher = more tactical elements present.
        """
        tactical_elements = 0
        
        # Count hanging pieces
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece and piece.piece_type not in [chess.PAWN, chess.KING]:
                if board.is_attacked_by(not piece.color, sq):
                    tactical_elements += 1
        
        # Count checks available
        for move in board.legal_moves:
            board.push(move)
            if board.is_check():
                tactical_elements += 2
            board.pop()
        
        # Normalize
        return min(1.0, tactical_elements / 10.0)
    
    def _adjust_for_tactics(self, weights: dict[str, float], density: float) -> dict[str, float]:
        """Adjust weights when tactics are present."""
        adjusted = dict(weights)
        
        if density > 0.5:  # Many tactical elements
            # Tactical rules become more important
            adjusted["LPDO Detection"] *= 1.0 + density * 0.5
            adjusted["Hanging Capture"] *= 1.0 + density * 0.5
            adjusted["Pin Detection"] *= 1.0 + density * 0.3
            
            # Strategic rules become less important
            adjusted["Prophylaxis"] *= 1.0 - density * 0.3
            adjusted["Pawn Structure"] *= 1.0 - density * 0.2
            adjusted["Knight Outpost"] *= 1.0 - density * 0.2
        
        return adjusted
```

## Feeding into the Explanation Pipeline

### The Weight-Aware Explanation

Dynamic weights affect both the score and the explanation. When a rule's weight is increased by context, the explanation should note this:

> "In this endgame position, the pawn structure becomes more important. The isolated d-pawn is a significant weakness (-40cp, doubled from normal due to the endgame phase)."

```python
def generate_weight_aware_explanation(rule_name: str, score: int, 
                                       base_weight: float, 
                                       dynamic_weight: float,
                                       reason: str) -> str:
    """
    Generate an explanation that notes weight adjustments.
    """
    weight_ratio = dynamic_weight / base_weight if base_weight > 0 else 1.0
    
    if abs(weight_ratio - 1.0) < 0.1:
        # No significant adjustment
        return f"[{rule_name}] {reason} ({score:+d}cp)"
    elif weight_ratio > 1.0:
        adjustment = "more important" if weight_ratio < 1.5 else "much more important"
        return f"[{rule_name}] {reason} ({score:+d}cp, {adjustment} in this position)"
    else:
        adjustment = "less important" if weight_ratio > 0.5 else "much less important"
        return f"[{rule_name}] {reason} ({score:+d}cp, {adjustment} in this position)"
```

### The Full Confidence Pipeline

The complete flow from rule evaluation to explanation:

1. **Rule evaluates** → (raw_score, reason)
2. **Activation strength computed** → effective_score = raw_score × strength
3. **Dynamic weight computed** → adjusted_weight = base_weight × context_factor
4. **Final contribution** = effective_score × adjusted_weight
5. **Explanation generated** including weight context if adjusted

This pipeline ensures that every number in the final explanation is traceable back to its source: the rule that produced it, the activation strength, and the context-dependent weight adjustment. This is the foundation of the [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|move explanation architecture]].

---

*Previous: [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|03 - Multi-Rule Decision Making]] ←*
*Next: [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|05 - The Rule Module System (Code)]] →*
*See also: [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]] | [[08-Rule-Based-Reasoning-Systems/02 - Chess Knowledge Representation|Chess Knowledge Representation]] | [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|Move Explanation Architecture]]*
