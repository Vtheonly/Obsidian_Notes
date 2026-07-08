---
tags:
  - chapter-09
  - xai
  - post-hoc
  - rationalization
  - surrogate-model
  - stockfish
  - global-surrogate
  - limitations
---

# 03 - Post-Hoc Rationalization and Surrogate Models

## The Idea: Explaining the Silent Genius

Stockfish is a **silent genius**—it finds the best moves with superhuman accuracy but offers no explanation for its choices. It communicates only in numbers: +1.5, depth 30, 45Mnps. There are no words, no concepts, no reasoning traces. Just the cold authority of computation.

What if we could **translate** Stockfish's numerical output into human-readable explanations? This is the promise of **post-hoc rationalization**: taking the output of a black-box model and generating an explanation that approximates the model's reasoning.

In the context of our project, post-hoc rationalization means using our rule-based engine as an **interpreter** of Stockfish's decisions. Stockfish finds the move; our engine explains *why* it's good. The result is the best of both worlds: Stockfish's accuracy plus our engine's explainability.

## Global Surrogate Models

### What Is a Surrogate Model?

A **surrogate model** is a simpler, interpretable model that is trained to mimic the behavior of a complex, opaque model. The surrogate doesn't need to perfectly replicate the complex model—it just needs to approximate it well enough that its explanations are useful.

There are two types of surrogate models:

1. **Global surrogate**: Approximates the complex model's behavior across *all* inputs
2. **Local surrogate**: Approximates the complex model's behavior for a *specific* input (this is what LIME does)

### Our Rule-Based Engine as a Global Surrogate

Our rule-based evaluation engine can function as a **global surrogate** for Stockfish's evaluation. The relationship is:

```
┌────────────┐         ┌──────────────┐
│ Stockfish  │────────►│  Rule-Based  │
│ (Black Box)│  train  │  Engine      │
│            │         │  (Surrogate) │
└────────────┘         └──────────────┘
     │                        │
     ▼                        ▼
 Best Move + Score    Best Move + Explanation
 (authoritative)      (interpretable approximation)
```

The surrogate relationship works as follows:
1. For a given position, Stockfish produces a score and a best move
2. Our rule-based engine evaluates the same position
3. If the rule-based engine agrees with Stockfish's choice, the rule-based explanation is a faithful rationalization
4. If they disagree, the disagreement itself is informative

### Training the Surrogate

To make our rule-based engine a better surrogate for Stockfish, we can **calibrate** its weights using Stockfish's evaluations:

```python
import numpy as np
from scipy.optimize import minimize

class SurrogateCalibrator:
    """
    Calibrate rule weights to best approximate Stockfish evaluations.
    
    This is a form of knowledge distillation: the rule-based engine
    learns to mimic Stockfish's scores while maintaining its
    interpretable structure.
    """
    
    def __init__(self, rule_engine: RuleEngine):
        self.rule_engine = rule_engine
        self.positions = []  # (FEN, stockfish_score) pairs
    
    def add_position(self, fen: str, stockfish_score: int):
        """Add a position with its Stockfish evaluation."""
        self.positions.append((fen, stockfish_score))
    
    def calibrate(self) -> dict[str, float]:
        """
        Optimize rule weights to minimize the difference between
        the rule-based evaluation and Stockfish's evaluation.
        
        Returns the optimized weights.
        """
        # Get rule names
        rule_names = [r.name for r in self.rule_engine.dictionary.get_all_rules()]
        n_rules = len(rule_names)
        
        # Initial weights
        initial_weights = np.array([r.weight for r in self.rule_engine.dictionary.get_all_rules()])
        
        # Collect raw rule scores for all positions
        raw_scores = []
        stockfish_scores = []
        
        for fen, sf_score in self.positions:
            board = chess.Board(fen)
            scores = {}
            for rule in self.rule_engine.dictionary.get_all_rules():
                result = rule.evaluate(board, color=board.turn)
                scores[rule.name] = result.effective_score
            raw_scores.append(scores)
            stockfish_scores.append(sf_score)
        
        # Define optimization objective
        def objective(weights):
            total_error = 0
            for i, (scores, sf_score) in enumerate(zip(raw_scores, stockfish_scores)):
                predicted = sum(weights[j] * scores.get(rule_names[j], 0) 
                              for j in range(n_rules))
                error = (predicted - sf_score) ** 2
                total_error += error
            
            # Regularization: keep weights close to initial values
            reg = 0.01 * np.sum((weights - initial_weights) ** 2)
            
            return total_error / len(self.positions) + reg
        
        # Optimize
        bounds = [(0.0, 2.0)] * n_rules  # Weights between 0 and 2
        result = minimize(objective, initial_weights, bounds=bounds, method='L-BFGS-B')
        
        # Update weights
        optimized_weights = {}
        for j, name in enumerate(rule_names):
            optimized_weights[name] = float(result.x[j])
        
        return optimized_weights
```

## The Rule-Based Engine as Interpreter

### How Interpretation Works

Even without formal surrogate training, our rule-based engine can interpret Stockfish's decisions through the **heuristic delta method** (described in detail in [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|Move Explanation Architecture]]):

1. Stockfish selects the best move (authoritative)
2. Our engine evaluates the position before and after the move
3. The rule(s) with the largest positive delta provide the explanation
4. The explanation is phrased in terms of the rule concepts

This method works because in most positions, Stockfish's best move *does* improve the position in ways that our rules can detect. When Stockfish plays Nd5, our engine detects that the Knight Outpost rule improved by +35cp—this is the explanation.

### When Interpretation Works Well

| Situation | Why It Works | Example |
|-----------|-------------|---------|
| Clear strategic moves | Rules directly capture the improvement | Nd5 to outpost, Rook to open file |
| Tactical moves | Rules detect the material/threat change | Captures, forks, discovered attacks |
| Prophylactic moves | Prophylaxis rule detects the prevention | h3 preventing ...Bg4 |
| Safety moves | Safety rules detect the improvement | Castling, pawn shield moves |

### When Interpretation Fails

| Situation | Why It Fails | Example |
|-----------|-------------|---------|
| Deep positional moves | Rules don't capture the subtle concept | A quiet move that controls a key square over 10+ moves |
| Intuition-based moves | No rule captures the pattern | AlphaZero's famous h-pawn advances |
| Sacrificial moves | The material loss overwhelms strategic gains in the rules | A positional sacrifice where the compensation is long-term |
| Anti-positional moves that work | Rules say "bad" but the move is correct | Moving the knight to the rim for a specific tactical reason |

### Handling Disagreement

When our rule-based engine disagrees with Stockfish—when the rule-based evaluation says a move is bad but Stockfish says it's good—the disagreement itself is valuable:

```python
def handle_disagreement(board: chess.Board, move: chess.Move,
                         rule_eval: MoveEvaluation,
                         stockfish_eval: int) -> str:
    """
    Generate an explanation when the rule engine disagrees with Stockfish.
    """
    move_san = board.san(move)
    rule_delta = rule_eval.total_delta
    
    if stockfish_eval > 50 and rule_delta < -20:
        # Stockfish likes it, rules don't — deep positional understanding needed
        return (f"{move_san} is recommended by deep analysis, though it appears "
                f"to worsen the position by {abs(rule_delta)}cp according to "
                f"our rules. The move likely involves long-term compensation "
                f"or subtle positional factors not captured by our rule system. "
                f"The primary rule objection is: {rule_eval.primary_objection}.")
    
    elif stockfish_eval < -50 and rule_delta > 20:
        # Rules like it, Stockfish doesn't — tactical refutation exists
        return (f"{move_san} looks good strategically (+{rule_delta}cp by rules) "
                f"but deep analysis finds a refutation (Stockfish: {stockfish_eval}cp). "
                f"The likely issue is a tactical resource that our rules don't detect. "
                f"Check for hidden tactics, especially: "
                f"{detect_hidden_tactics(board, move)}.")
    
    else:
        # General disagreement
        return (f"{move_san}: Rules evaluate {rule_delta:+d}cp, "
                f"Stockfish evaluates {stockfish_eval:+d}cp. "
                f"The discrepancy may indicate factors beyond our rule system.")
```

## Limitations of Post-Hoc Explanation

### The Fidelity Problem

The fundamental limitation of post-hoc rationalization is **fidelity**: there is no guarantee that the explanation accurately reflects what Stockfish actually computed. Stockfish's evaluation function uses piece-square tables, king safety heuristics, and mobility calculations that overlap with but are not identical to our rules. When we say "Stockfish chose Nd5 because of the knight outpost," we are attributing our concept to Stockfish's computation—Stockfish may have chosen Nd5 for entirely different reasons.

This fidelity gap is unavoidable in post-hoc explanation. The only way to guarantee fidelity is to use an **ante-hoc** system (like our rule-based engine) where the explanation is built into the computation from the start.

### The Completeness Problem

Post-hoc explanations are only as complete as the concept space they draw from. If our rule system doesn't include a concept (e.g., "opposite-colored bishops in endgame"), then it cannot explain moves that depend on that concept. The explanation will be incomplete—mentioning the factors it can detect but missing the factor that actually drove the decision.

### The Cherry-Picking Problem

When multiple rules contribute positively to a move, the post-hoc explainer must choose which to highlight. This selection process can be biased—toward the rules with the largest scores, toward the rules that are easiest to explain, or toward the rules the developer considers most important. The user sees the selected explanation and assumes it's the *whole* explanation, when in fact it's a curated subset.

### Mitigation Strategies

| Problem | Mitigation |
|---------|-----------|
| Fidelity | Use the rule-based engine as the *primary* evaluator (ante-hoc), not just as a Stockfish interpreter |
| Completeness | Continuously expand the rule set; explicitly flag "unexplained" score components |
| Cherry-picking | Present *all* contributing rules, not just the top ones; let the user explore |
| Disagreement | When rules and Stockfish disagree, explicitly flag the disagreement and investigate |

## When to Use Post-Hoc vs. Ante-Hoc

| Scenario | Recommended Approach |
|----------|---------------------|
| Engine plays its own moves | **Ante-hoc** — Use rule-based engine for both evaluation and explanation |
| Explaining Stockfish's moves | **Post-hoc** — Use rule engine as surrogate interpreter |
| Teaching a student | **Ante-hoc** — Rules provide guaranteed-faithful explanations |
| Analyzing a complex position | **Hybrid** — Use Stockfish for accuracy, rules for explanation, flag disagreements |
| Detecting blunders | **Post-hoc** — Compare player's move with Stockfish's, explain the difference |

The optimal approach depends on the use case. Our engine supports both modes: it can evaluate positions independently (ante-hoc) or interpret Stockfish's evaluations (post-hoc), with clear signaling to the user about which mode is active and what guarantees apply.

---

*Previous: [[09-Explainable-AI-for-Chess/02 - Concept Bottleneck Models|02 - Concept Bottleneck Models]] ←*
*Next: [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|04 - Move Explanation Architecture]] →*
*See also: [[09-Explainable-AI-for-Chess/01 - Explainable AI (XAI) Overview|Explainable AI Overview]] | [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]] | [[08-Rule-Based-Reasoning-Systems/04 - Confidence Scoring and Rule Weighting|Confidence Scoring and Rule Weighting]]*
