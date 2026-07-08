---
tags:
  - chapter-08
  - rule-engine
  - architecture
  - declarative-rules
  - modularity
  - evaluation
  - explainability
---

# 01 - Rule Engine Architecture

## The Overall Architecture

The rule engine is the heart of the explainable chess engine. It is the system that takes a board position and a candidate move, applies a collection of named, described rules, and produces both a **score** (how good is this move?) and a **reasoning trace** (why is this move good or bad?). This dual output—score plus explanation—is what makes our engine fundamentally different from conventional chess engines.

The architecture is designed around three foundational principles:

1. **Declarative**: Each rule is a self-contained entity that declares what it evaluates, not how it fits into the overall system. The rule knows nothing about other rules, about the search algorithm, or about the overall evaluation pipeline.
2. **Modular**: Rules can be added, removed, or modified independently without affecting other rules. The system is open for extension but closed for modification (the Open-Closed Principle).
3. **Transparent**: Every score component is traceable to a named rule with a human-readable description. There are no "hidden" contributions to the evaluation.

These three principles ensure that the engine can always answer the question **"why?"**—every component of the evaluation has a name, a description, and a numerical contribution that can be inspected, questioned, and modified.

## The Declarative Rule System

### What "Declarative" Means

In a declarative system, each rule is a **named, described, weighted entity** that knows how to evaluate itself. The rule doesn't need to know about other rules, about the search algorithm, or about the overall evaluation. It simply answers two questions:

1. **What is my score for this position/move?** (in centipawns)
2. **Why did I give this score?** (in natural language)

This is in contrast to an imperative system, where the evaluation is computed by a single monolithic function that combines all factors in a specific order. The declarative approach has significant advantages:

| Aspect | Declarative (Our Engine) | Imperative (Neural Network) |
|--------|-------------------------|----------------------------|
| **Transparency** | Each rule is individually inspectable | Weights are opaque matrices |
| **Modifiability** | Rules can be added/removed/modified independently | Requires full retraining |
| **Explainability** | Every score has a named reason | No direct explanation possible |
| **Composition** | Rules combine additively (simple, predictable) | Features interact non-linearly (powerful but opaque) |
| **Accuracy** | Limited by hand-crafting | Can capture subtle, non-linear patterns |
| **Speed** | Can be slower (many function calls) | Very fast inference after training |
| **Debuggability** | Each rule testable independently | Black-box debugging only |

The key insight is that **declarative rules trade some accuracy for complete explainability**. Our engine accepts this trade-off because explainability is the primary goal—not maximum playing strength.

### The Rule Interface

Every rule in the system implements the same interface:

```python
from abc import ABC, abstractmethod
import chess

class Rule(ABC):
    """
    Abstract base class for all evaluation rules.
    
    Each rule:
    - Has a name (for identification and display)
    - Has a description (for human explanation)
    - Has a weight (for importance/confidence)
    - Has a category (for grouping and organization)
    - Implements evaluate() which returns (score, reason)
    
    The evaluate() method is the core of the rule. It takes a board state
    and optionally a move and color, and returns:
    - score: integer in centipawns (>0 = good for moving color, <0 = bad)
    - reason: human-readable string explaining the score ("" if rule doesn't fire)
    """
    
    name: str = "Unnamed Rule"
    description: str = "No description"
    weight: float = 1.0
    category: str = "general"
    
    @abstractmethod
    def evaluate(self, board: chess.Board, move: chess.Move = None, 
                 color: chess.Color = None) -> tuple[int, str]:
        """
        Evaluate the rule for the given context.
        
        Args:
            board: The current board state
            move: The candidate move (if evaluating a move-specific rule)
            color: The perspective color (if evaluating for a specific side)
            
        Returns:
            (score, reason): score in centipawns, reason as human-readable string
            score > 0 = good for the moving color
            score < 0 = bad for the moving color
            reason = "" if the rule doesn't fire
        """
        pass
    
    def __repr__(self) -> str:
        return f"Rule({self.name}, weight={self.weight}, category={self.category})"
    
    def __str__(self) -> str:
        return f"[{self.category}/{self.name}] {self.description} (weight: {self.weight})"
```

## Rule Categories

Rules are organized into **six categories** that reflect the major domains of chess knowledge. This categorization serves multiple purposes: it organizes the codebase, it enables category-level weighting, and it provides the first level of explanation grouping.

### Category 1: Material Rules

Rules that evaluate material balance and material-related features. These are the most fundamental and highest-weighted rules.

| Rule Name | What It Evaluates | Weight | Typical Score Range |
|-----------|-------------------|--------|-------------------|
| Material Count | Basic piece counting | 1.0 | ±1000+ |
| Bishop Pair | Having both bishops | 0.8 | +30 to +50 |
| Material Imbalance | Non-standard material configurations | 0.6 | ±50 |
| Exchange Advantage | Being up the exchange | 0.7 | +50 to +60 |
| Pawn Promotion Threat | Near-promotion pawns | 0.9 | +100 to +900 |

```python
class MaterialCountRule(Rule):
    name = "Material Count"
    description = "Evaluates the material balance based on standard piece values"
    weight = 1.0
    category = "material"
    
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }
    
    def evaluate(self, board: chess.Board, move: chess.Move = None,
                 color: chess.Color = None) -> tuple[int, str]:
        white_material = sum(self.PIECE_VALUES[p.piece_type] 
                           for sq in chess.SQUARES 
                           if (p := board.piece_at(sq)) and p.color == chess.WHITE 
                           and p.piece_type != chess.KING)
        black_material = sum(self.PIECE_VALUES[p.piece_type] 
                           for sq in chess.SQUARES 
                           if (p := board.piece_at(sq)) and p.color == chess.BLACK 
                           and p.piece_type != chess.KING)
        
        score = white_material - black_material
        if color == chess.BLACK:
            score = -score
        
        if abs(score) < 10:
            return (0, "Material is equal")
        elif score > 0:
            return (score, f"Material advantage: +{score/100:.1f} pawns")
        else:
            return (score, f"Material disadvantage: {score/100:.1f} pawns")
```

### Category 2: Tactical Rules

Rules that evaluate tactical features—threats, pins, forks, hanging pieces, and combinative potential.

| Rule Name | What It Evaluates | Weight | Typical Score Range |
|-----------|-------------------|--------|-------------------|
| LPDO Detection | Undefended pieces as tactical targets | 0.9 | ±50 to ±300 |
| Pin Detection | Pieces that are pinned | 0.8 | ±30 to ±100 |
| Fork Detection | Potential fork patterns | 0.7 | ±50 to ±200 |
| Discovered Attack | Unmasked attack potential | 0.7 | ±50 to ±200 |
| Hanging Capture | Undefended pieces that can be captured | 1.0 | ±100 to ±900 |

### Category 3: Opening Rules

Rules that evaluate opening-specific features—development, king safety, central control.

| Rule Name | What It Evaluates | Weight | Typical Score Range |
|-----------|-------------------|--------|-------------------|
| Development | Piece development in the opening | 0.8 | ±30 to ±60 |
| Castling | Whether the king has castled | 0.9 | ±50 to ±100 |
| Central Control | Control of central squares | 0.7 | ±20 to ±40 |
| Queen Early | Penalty for early queen development | 0.6 | -30 to 0 |
| Opening Repertoire | Known opening line adherence | 0.3 | ±10 |

### Category 4: Trap Rules

Rules that detect and evaluate common traps and tactical motifs.

| Rule Name | What It Evaluates | Weight | Typical Score Range |
|-----------|-------------------|--------|-------------------|
| Back Rank Mate | Vulnerability to back rank mate | 0.9 | ±50 to ±200 |
| Smothered Mate | Potential for smothered mate | 0.7 | ±100 to ±200 |
| Sacrifice Pattern | Sound vs. unsound sacrifices | 0.6 | ±50 to ±300 |
| Stalemate Trap | Potential stalemate in endgame | 0.5 | ±50 |

### Category 5: Strategy Rules

Rules that evaluate positional and strategic features—the "human" concepts that make chess interesting.

| Rule Name | What It Evaluates | Weight | Typical Score Range |
|-----------|-------------------|--------|-------------------|
| Pawn Structure | Doubled, isolated, passed pawns | 0.8 | ±20 to ±60 |
| Knight Outpost | Knight on a strong outpost | 0.7 | +30 to +60 |
| Bad Bishop | Bishop blocked by own pawns | 0.6 | -20 to -50 |
| Rook on Open File | Rook controlling an open file | 0.7 | +20 to +40 |
| Prophylaxis | Preventing opponent's plan | 0.5 | +10 to +40 |
| Piece Improvement | Improving worst piece | 0.5 | +10 to +30 |

### Category 6: Safety Rules

Rules that evaluate king safety and defensive soundness—the highest-stakes category.

| Rule Name | What It Evaluates | Weight | Typical Score Range |
|-----------|-------------------|--------|-------------------|
| Pawn Shield | Pawns protecting the castled king | 0.9 | ±30 to ±80 |
| King Exposure | How exposed the king is to attack | 0.9 | ±50 to ±200 |
| Attack Units | Concentration of attacking pieces near king | 1.0 | ±50 to ±150 |
| Open Files Near King | Files that give rooks access to the king | 0.8 | ±30 to ±100 |

## How Rules Are Evaluated: The evaluate() Interface

The `evaluate()` method is called for every rule in every position. The method takes three arguments:

1. **board**: The current board state (after the candidate move has been made, for move-specific evaluation)
2. **move**: The candidate move being evaluated (optional—some rules evaluate the position, not the move)
3. **color**: The perspective color (optional—defaults to the side to move)

The method returns a tuple:
- **score**: An integer in centipawns. Positive means good for the moving color; negative means bad.
- **reason**: A string explaining the score. Empty string if the rule doesn't fire.

A rule **fires** when it has something meaningful to say. If a position has no isolated pawns, the `IsolatedPawnRule` returns `(0, "")` rather than `(0, "No isolated pawns")`. This distinction is important because the explanation pipeline only includes rules that fire—silent rules don't clutter the explanation.

```python
def evaluate_all_rules(board: chess.Board, move: chess.Move, 
                       color: chess.Color) -> list[tuple[str, int, str, float]]:
    """
    Evaluate all rules for the given position and move.
    Returns list of (rule_name, score, reason, weight) tuples.
    Only includes rules that fired (reason != "").
    """
    results = []
    
    for rule in ALL_RULES:
        score, reason = rule.evaluate(board, move, color)
        if reason:  # Only include rules that fired
            results.append((rule.name, score, reason, rule.weight))
    
    return results
```

## How Rule Scores Are Combined

Rule scores are combined using **weighted additive aggregation**:

$$S_{total} = \sum_{i=1}^{N} w_i \cdot s_i$$

Where:
- $S_{total}$ is the total score
- $N$ is the number of rules
- $w_i$ is the weight of rule $i$
- $s_i$ is the score from rule $i$

The additive combination is a deliberate design choice. It ensures that:
1. Each rule's contribution is **independent** and **inspectable**
2. The total score is **decomposable**—you can see exactly which rules contributed and by how much
3. There are no **interaction effects** that make the total score unpredictable

```python
def combine_rule_scores(results: list[tuple[str, int, str, float]]) -> tuple[int, list[str]]:
    """
    Combine rule scores using weighted additive aggregation.
    
    Args:
        results: List of (rule_name, score, reason, weight) tuples
    
    Returns:
        (total_score, all_reasons)
    """
    total_score = 0
    all_reasons = []
    
    for rule_name, score, reason, weight in results:
        weighted_score = int(score * weight)
        total_score += weighted_score
        
        if weighted_score != 0:
            all_reasons.append(f"[{rule_name}] {reason} (weighted: {weighted_score}cp)")
    
    return total_score, all_reasons
```

## The Separation Between Evaluation Rules and Depth Rules

A critical architectural decision is the **separation** between evaluation rules (which produce scores and explanations) and depth rules (which produce depth deltas and reasons). These two systems are independent but complementary:

| System | Purpose | Output | Module |
|--------|---------|--------|--------|
| Evaluation Rules | Score a position/move | (score, reason) | [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|Rule Module System]] |
| Depth Rules | Adjust search depth | (delta, reason) | [[06-Adaptive-Depth-Control/07 - The Depth Rules Module (Code Architecture)|Depth Rules Module]] |

They interact through the search algorithm:

1. Depth rules determine **how deeply** to search
2. Evaluation rules determine **what score** to give the positions found
3. Both contribute **reasons** to the explanation pipeline

This separation allows each system to be developed, tested, and optimized independently. A new evaluation rule doesn't affect the search depth, and a new depth rule doesn't affect the evaluation scores. But in the final explanation, both are combined to tell the full story: "This move was searched to extra depth because [depth rule reason], and the resulting position scores well because [evaluation rule reason]."

## Why Modularity Matters

### 1. Rules Can Be Added Without Modifying Existing Code

Adding a new rule requires only creating a new class and registering it. No existing code needs to be modified. This is the **Open-Closed Principle** in action.

### 2. Rules Can Be Removed Without Breaking the System

If a rule is found to be inaccurate, removing it is trivial—the rest of the system continues to function.

### 3. Rules Can Be Tuned Independently

Each rule's weight can be adjusted independently. If the bishop pair bonus is too high, reduce its weight. This independent tunability is essential for calibration.

### 4. Rules Can Be Tested Individually

Each rule can be unit-tested with specific positions, far more manageable than testing a monolithic evaluation function.

```python
def test_isolated_pawn_rule():
    rule = IsolatedPawnRule()
    board = chess.Board("rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    score, reason = rule.evaluate(board, color=chess.WHITE)
    assert score < 0, "Isolated pawn should produce negative score"
    assert "isolated" in reason.lower(), "Reason should mention isolation"
```

### 5. The Explanation System Benefits From Modularity

Because each rule produces its own reason string, the explanation system can present a granular, structured explanation that shows the contribution of each factor—something impossible with a monolithic evaluation function or a neural network.

---

*Next: [[08-Rule-Based-Reasoning-Systems/02 - Chess Knowledge Representation|02 - Chess Knowledge Representation]] →*
*See also: [[05-Evaluation-Functions-and-Heuristics/01 - Static Evaluation Overview|Static Evaluation Overview]] | [[06-Adaptive-Depth-Control/07 - The Depth Rules Module (Code Architecture)|The Depth Rules Module]] | [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|The Rule Module System]]*
