---
tags:
  - chapter-08
  - rule-engine
  - knowledge-representation
  - propositional-rules
  - feature-vectors
  - rule-dictionaries
  - explainability
  - weights
---

# 02 - Chess Knowledge Representation

## How Chess Knowledge Becomes Computation

The central challenge of building an explainable chess engine is **representation**: how do we encode chess knowledge in a form that is both computationally useful and human-readable? This is not just a technical problem—it is the fundamental problem that determines whether the engine can explain its reasoning.

A neural network encodes chess knowledge as millions of floating-point numbers in weight matrices. This representation is computationally efficient but completely opaque. A human cannot look at a weight matrix and say "this neuron detects isolated pawns." Our engine must use a representation where the mapping between knowledge and computation is transparent.

## Propositional Rules

### What Are Propositional Rules?

A **propositional rule** is a simple logical statement about a chess position:

$$\text{IF } \text{condition} \text{ THEN } \text{score} \text{ BECAUSE } \text{reason}$$

Each rule has three components:
1. **Condition**: A boolean test on the position (e.g., "there is an isolated pawn")
2. **Score**: A numerical value in centipawns (e.g., -20)
3. **Reason**: A human-readable explanation (e.g., "isolated d-pawn is a structural weakness")

This is the simplest possible knowledge representation, and it is ideally suited for explainability because every component has a direct human interpretation.

### Examples of Propositional Rules

```python
# Rule: Isolated Pawn Penalty
# IF: There exists a pawn with no friendly pawns on adjacent files
# THEN: -20 centipawns
# BECAUSE: "Isolated pawn on [file] is a structural weakness — it cannot be defended by other pawns"

class IsolatedPawnRule(Rule):
    name = "Isolated Pawn"
    description = "Penalizes pawns with no friendly pawns on adjacent files"
    weight = 0.8
    category = "strategy"
    
    def evaluate(self, board: chess.Board, move: chess.Move = None,
                 color: chess.Color = None) -> tuple[int, str]:
        penalty = 0
        isolated_files = []
        
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece is None or piece.piece_type != chess.PAWN:
                continue
            if piece.color != color:
                continue
            
            file = chess.square_file(sq)
            
            # Check for friendly pawns on adjacent files
            has_adjacent_pawn = False
            for adj_file in [file - 1, file + 1]:
                if 0 <= adj_file <= 7:
                    for rank in range(8):
                        adj_sq = chess.square(adj_file, rank)
                        adj_piece = board.piece_at(adj_sq)
                        if (adj_piece and adj_piece.piece_type == chess.PAWN 
                            and adj_piece.color == color):
                            has_adjacent_pawn = True
                            break
            
            if not has_adjacent_pawn:
                penalty += 20
                isolated_files.append(chess.file_name(sq))
        
        if penalty > 0:
            return (-penalty, f"Isolated pawn(s) on {', '.join(isolated_files)} — "
                    f"structural weakness (cannot be defended by other pawns)")
        
        return (0, "")
```

### The Propositional Rule Template

Every propositional rule follows this template:

```python
class [RuleName]Rule(Rule):
    """
    [Human-readable description of the chess concept]
    
    Condition: [What must be true for the rule to fire]
    Score: [Typical score range]
    Explanation: [Template for the reason string]
    """
    name = "[Rule Name]"
    description = "[Description]"
    weight = [0.0 to 1.0]
    category = "[material|tactical|opening|trap|strategy|safety]"
    
    def evaluate(self, board, move=None, color=None):
        # 1. Check condition
        if not self._condition_met(board, color):
            return (0, "")
        
        # 2. Compute score
        score = self._compute_score(board, color)
        
        # 3. Generate reason
        reason = self._generate_reason(board, color)
        
        return (score, reason)
    
    def _condition_met(self, board, color):
        """Check if the rule's condition is satisfied."""
        raise NotImplementedError
    
    def _compute_score(self, board, color):
        """Compute the numerical score for this rule."""
        raise NotImplementedError
    
    def _generate_reason(self, board, color):
        """Generate a human-readable reason string."""
        raise NotImplementedError
```

## Numeric Weights

### What Weights Represent

Each rule has a **weight** that represents the **confidence** or **importance** of that rule. The weight scales the rule's score when combined with other rules:

$$\text{weighted\_score}_i = w_i \cdot s_i$$

Weights serve multiple purposes:
1. **Confidence**: A weight of 1.0 means "I'm fully confident in this rule's score." A weight of 0.5 means "This rule's score should be discounted by 50%."
2. **Importance**: In the final evaluation, higher-weighted rules have more influence on the total score.
3. **Tunable parameter**: Weights can be adjusted to calibrate the engine's play style and accuracy.

### Weight Assignment Philosophy

Weights are assigned based on:

| Factor | High Weight (>0.8) | Medium Weight (0.5-0.8) | Low Weight (<0.5) |
|--------|-------------------|------------------------|-------------------|
| **Reliability** | Always produces correct score | Usually correct | Sometimes correct |
| **Impact** | Game-changing when relevant | Significant | Modest |
| **Specificity** | Clear condition, no ambiguity | Mostly clear | Context-dependent |
| **Verifiability** | Easy to test and verify | Testable | Hard to verify |

Examples:
- **Material Count**: weight = 1.0 (always correct, always impactful)
- **Knight Outpost**: weight = 0.7 (usually good but context-dependent)
- **Prophylaxis**: weight = 0.5 (hard to verify, context-dependent)

```python
# Weight examples from the rule system
WEIGHT_TABLE = {
    # Material (high confidence)
    "Material Count": 1.0,
    "Bishop Pair": 0.8,
    "Exchange Advantage": 0.7,
    
    # Tactical (high confidence when they fire)
    "LPDO Detection": 0.9,
    "Hanging Capture": 1.0,
    "Pin Detection": 0.8,
    
    # Opening (moderate confidence)
    "Development": 0.8,
    "Castling": 0.9,
    "Central Control": 0.7,
    
    # Trap (variable confidence)
    "Back Rank Mate": 0.9,
    "Sacrifice Pattern": 0.6,
    
    # Strategy (moderate confidence, context-dependent)
    "Pawn Structure": 0.8,
    "Knight Outpost": 0.7,
    "Bad Bishop": 0.6,
    "Prophylaxis": 0.5,
    
    # Safety (high confidence, high impact)
    "Pawn Shield": 0.9,
    "King Exposure": 0.9,
    "Attack Units": 1.0,
}
```

## Feature Vectors

### From Rules to Features

While individual rules are the primary knowledge representation, we can also represent a position as a **feature vector**—a fixed-length array of numbers where each element corresponds to a rule's score. This representation is useful for:

1. **Machine learning**: Training weights based on game data
2. **Visualization**: Plotting position characteristics
3. **Similarity comparison**: Comparing two positions by their feature vectors
4. **Classification**: Categorizing positions by their dominant features

```python
class FeatureVector:
    """
    Represents a position as a feature vector where each dimension
    corresponds to a rule's score.
    """
    
    def __init__(self, rule_names: list[str]):
        self.rule_names = rule_names
        self.scores = {name: 0 for name in rule_names}
        self.reasons = {name: "" for name in rule_names}
        self.weights = {name: 1.0 for name in rule_names}
    
    def set_score(self, rule_name: str, score: int, reason: str, weight: float = 1.0):
        """Set the score for a specific rule."""
        self.scores[rule_name] = score
        self.reasons[rule_name] = reason
        self.weights[rule_name] = weight
    
    def to_vector(self) -> list[float]:
        """Convert to a numerical feature vector."""
        return [self.scores[name] * self.weights[name] for name in self.rule_names]
    
    def to_dict(self) -> dict[str, float]:
        """Convert to a dictionary of weighted scores."""
        return {name: self.scores[name] * self.weights[name] for name in self.rule_names}
    
    def dominant_features(self, n: int = 3) -> list[tuple[str, float, str]]:
        """
        Return the n most influential features (by absolute weighted score).
        """
        weighted = [(name, self.scores[name] * self.weights[name], self.reasons[name])
                    for name in self.rule_names
                    if self.reasons[name]]  # Only fired rules
        
        weighted.sort(key=lambda x: abs(x[1]), reverse=True)
        return weighted[:n]
    
    def __repr__(self) -> str:
        total = sum(self.scores[name] * self.weights[name] for name in self.rule_names)
        dominant = self.dominant_features(3)
        features_str = "; ".join(f"{n}: {s:+.0f}" for n, s, _ in dominant)
        return f"FeatureVector(total={total:+.0f}cp, top: {features_str})"
```

### The Feature Vector as a Positional Fingerprint

Every position has a unique feature vector that acts as a "positional fingerprint." Two positions with similar feature vectors have similar strategic characteristics, even if the piece placement is different. This enables:

- **Position classification**: "This is an isolated queen pawn position" (high Isolated Pawn feature)
- **Plan suggestion**: "The dominant negative feature is Bad Bishop, so the plan should be to improve the bishop"
- **Move comparison**: "This move changes the feature vector from [A] to [B], primarily by improving the Knight Outpost feature"

## Rule Dictionaries

### The Master Dictionary

All rules are organized in a **rule dictionary**—a centralized registry that maps rule names to rule instances. This dictionary is the single source of truth for which rules are active and how they are configured:

```python
class RuleDictionary:
    """
    Central registry of all evaluation rules.
    Manages rule registration, activation, and configuration.
    """
    
    def __init__(self):
        self.rules: dict[str, Rule] = {}
        self.categories: dict[str, list[str]] = {}
        self._register_default_rules()
    
    def _register_default_rules(self):
        """Register all default rules organized by category."""
        # Material
        self.register(MaterialCountRule())
        self.register(BishopPairRule())
        self.register(ExchangeAdvantageRule())
        
        # Tactical
        self.register(LPDORule())
        self.register(PinDetectionRule())
        self.register(HangingCaptureRule())
        
        # Opening
        self.register(DevelopmentRule())
        self.register(CastlingRule())
        self.register(CentralControlRule())
        
        # Trap
        self.register(BackRankMateRule())
        self.register(SacrificePatternRule())
        
        # Strategy
        self.register(IsolatedPawnRule())
        self.register(KnightOutpostRule())
        self.register(BadBishopRule())
        self.register(RookOnOpenFileRule())
        self.register(ProphylaxisRule())
        
        # Safety
        self.register(PawnShieldRule())
        self.register(KingExposureRule())
        self.register(AttackUnitsRule())
    
    def register(self, rule: Rule):
        """Register a rule in the dictionary."""
        self.rules[rule.name] = rule
        if rule.category not in self.categories:
            self.categories[rule.category] = []
        self.categories[rule.category].append(rule.name)
    
    def get_rule(self, name: str) -> Rule:
        """Get a rule by name."""
        return self.rules[name]
    
    def get_rules_by_category(self, category: str) -> list[Rule]:
        """Get all rules in a category."""
        return [self.rules[name] for name in self.categories.get(category, [])]
    
    def get_all_rules(self) -> list[Rule]:
        """Get all registered rules."""
        return list(self.rules.values())
    
    def evaluate_all(self, board: chess.Board, move: chess.Move = None,
                     color: chess.Color = None) -> FeatureVector:
        """
        Evaluate all rules and return a FeatureVector.
        """
        fv = FeatureVector(list(self.rules.keys()))
        
        for name, rule in self.rules.items():
            score, reason = rule.evaluate(board, move, color)
            fv.set_score(name, score, reason, rule.weight)
        
        return fv
```

## How This Representation Enables Explanation

The key insight is that our knowledge representation is **designed for explanation from the ground up**. Unlike a neural network where explanation must be extracted post-hoc (see [[09-Explainable-AI-for-Chess/03 - Post-Hoc Rationalization and Surrogate Models|Post-Hoc Rationalization]]), our rule-based representation produces explanations naturally:

1. **Each rule has a name**: The name is the concept (e.g., "Isolated Pawn")
2. **Each rule produces a reason**: The reason is the explanation (e.g., "Isolated d-pawn is a structural weakness")
3. **The feature vector shows relative importance**: The dominant features explain what matters most
4. **The feature delta shows what changed**: Comparing feature vectors before and after a move shows the move's effect

This means the explanation is not a separate system—it is an inherent property of the evaluation. You cannot have the score without also having the explanation. This is the fundamental design principle of our engine, and it is what makes it a true [[09-Explainable-AI-for-Chess/02 - Concept Bottleneck Models|Concept Bottleneck Model]].

---

*Previous: [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|01 - Rule Engine Architecture]] ←*
*Next: [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|03 - Multi-Rule Decision Making]] →*
*See also: [[05-Evaluation-Functions-and-Heuristics/01 - Static Evaluation Overview|Static Evaluation Overview]] | [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|The Rule Module System]]*
