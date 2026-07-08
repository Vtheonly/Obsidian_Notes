---
tags:
  - chapter-09
  - xai
  - concept-bottleneck
  - cbm
  - interpretable
  - human-concepts
  - neural-network-comparison
  - guarantee
---

# 02 - Concept Bottleneck Models

## The Concept Bottleneck Architecture

### What Is a Concept Bottleneck Model?

A **Concept Bottleneck Model (CBM)** is an architecture where the model's computation is forced through a layer of human-interpretable concepts. Instead of mapping directly from input to output, the model maps:

$$\text{Input} \xrightarrow{f_1} \text{Human Concepts} \xrightarrow{f_2} \text{Output}$$

The key insight is that the **bottleneck**—the concept layer—is both:
1. **Sufficient for accurate prediction**: The concepts carry enough information to produce good outputs
2. **Human-interpretable**: Each concept has a clear, human-understandable meaning

This architecture was formalized by Koh et al. (2020) in their paper "Concept Bottleneck Models," but the idea has deep roots in expert systems, rule-based reasoning, and any system where intermediate representations are designed to be meaningful.

### The Standard CBM Architecture

```
┌─────────┐      ┌──────────────────┐      ┌──────────┐
│  Input   │─────►│  Concept Layer   │─────►│  Output  │
│ (State)  │  f₁  │ (Human Concepts) │  f₂  │  (Score) │
└─────────┘      └──────────────────┘      └──────────┘
                  │ Knight Outpost: 0.8    │
                  │ Bad Bishop: 0.6        │
                  │ King Safety: 0.9       │
                  │ LPDO: 0.3              │
                  │ Material: +1.0         │
                  └───────────────────────┘
```

Each concept in the bottleneck is a **named, measurable feature** of the input. The concept values are constrained to be meaningful—either binary (present/absent) or on a continuous scale that corresponds to a human-understandable intensity.

## How Our Engine IS a Concept Bottleneck Model

### The Mapping

Our explainable chess engine is a **pure concept bottleneck model**. The mapping is exact:

| CBM Component | Our Engine Component |
|---------------|---------------------|
| Input (State) | Board position (FEN) |
| $f_1$ (State → Concepts) | [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|Rule evaluation system]] — each rule extracts a concept |
| Concept Layer | Rule scores: Knight Outpost +35cp, Bad Bishop -20cp, King Safety +15cp, etc. |
| $f_2$ (Concepts → Output) | [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|Weighted additive combination]] of rule scores |
| Output (Score) | Total evaluation: +30cp |

This mapping is not an approximation or an analogy—our engine's architecture **is** the CBM architecture. Every evaluation passes through the concept bottleneck (the rule scores), and every concept is human-interpretable (each rule has a name and description).

### The Guarantee: Every Score Component Is Traceable

The CBM architecture provides a **guarantee** that pure neural network architectures cannot: every component of the output score is traceable to a specific, named concept.

Consider a position evaluated at +45cp:
- Knight Outpost: +35cp
- Bad Bishop: -20cp (opponent's bishop)
- King Safety: +30cp
- Isolated Pawn: -10cp (opponent's)
- LPDO: -10cp (our undefended piece)
- **Total: +35 - 20 + 30 - 10 - 10 = +25cp** (with weights: +45cp)

Every component of this score has a name, a reason, and a numerical value. The user can inspect, question, and learn from each component. This is the CBM guarantee: **the explanation is not an add-on—it is the computation itself**.

### Why This Guarantee Matters

Without the CBM guarantee, explanations are always suspect. A post-hoc explanation might say "the model cares about king safety," but there's no way to verify that king safety actually contributed to the score. With the CBM guarantee, we can say:

> "King safety contributed +30cp to the total score of +45cp. This contribution came from the KingExposureRule, which detected that Black's king lacks a pawn shield and is exposed to attack along the g-file."

This is not a guess or an approximation—it is an exact accounting of the computation.

## Comparison to Pure Neural Network Approaches

### The Neural Network Alternative

A pure neural network approach to chess evaluation would:
1. Encode the board as a tensor (8×8×12 for piece types)
2. Pass it through several convolutional and fully-connected layers
3. Output a single evaluation score

This approach is powerful—AlphaZero and Leela Chess Zero demonstrate that neural networks can achieve superhuman evaluation accuracy. But they are completely opaque:

| Aspect | Neural Network | Our CBM Engine |
|--------|---------------|----------------|
| **Score accuracy** | Very high | Good (slightly lower) |
| **Explainability** | None (post-hoc only) | Built-in (ante-hoc) |
| **Concept traceability** | Impossible | Guaranteed |
| **Debuggability** | Black box | Each rule testable |
| **Modifiability** | Retrain entire network | Adjust individual rules |
| **Teaching value** | Low (can't explain) | High (explains everything) |

### The Accuracy Gap

The main disadvantage of the CBM approach is the **accuracy gap**: a rule-based evaluation with 30 rules cannot capture the same subtlety as a neural network with millions of parameters. There are positional nuances that rules can't easily express:

- **Latent patterns**: Patterns that humans haven't named or conceptualized
- **Non-linear interactions**: Features that only matter in combination
- **Implicit knowledge**: Knowledge that is "felt" rather than articulated

However, this gap is mitigated by several factors:

1. **Search compensates**: The search algorithm can discover tactical truths that the evaluation misses
2. **The gap is small for strategic evaluation**: Most of chess evaluation *can* be captured by named concepts
3. **Accuracy is not the goal**: Our engine prioritizes explainability over maximum strength
4. **Hybrid approaches are possible**: A neural network could provide the "ground truth" score while the rules provide the explanation (see [[09-Explainable-AI-for-Chess/03 - Post-Hoc Rationalization and Surrogate Models|Post-Hoc Rationalization]])

### The Hybrid CBM-Neural Approach

A promising direction is a hybrid architecture:

```
┌─────────┐      ┌──────────────────┐      ┌──────────┐
│  Board   │─────►│  Concept Layer   │─────►│  Score   │
│  State   │  f₁  │ (Rule Scores)    │  f₂  │ (Rules)  │
└─────────┘      └──────────────────┘      └──────────┘
       │                                          │
       │         ┌──────────────┐                 │
       └────────►│  Neural Net  │─────────────────┤
            g₁   │  (Deep Eval) │    Δ = correction│
                 └──────────────┘                  │
                                                   ▼
                                          ┌──────────────┐
                                          │ Final Score  │
                                          │ = Rule Score │
                                          │ + correction │
                                          └──────────────┘
```

In this hybrid, the rule-based system provides the interpretable score and explanation, while the neural network provides a small correction term that accounts for features the rules miss. The correction is kept small enough that it doesn't dominate the evaluation, but it improves accuracy.

```python
class HybridEvaluation:
    """
    Combines rule-based evaluation (interpretable) with neural network
    evaluation (accurate) in a concept bottleneck framework.
    """
    
    def __init__(self, rule_engine: RuleEngine, neural_net=None):
        self.rule_engine = rule_engine
        self.neural_net = neural_net
    
    def evaluate(self, board: chess.Board, color: chess.Color) -> tuple[int, str]:
        # Rule-based evaluation (interpretable)
        rule_eval = self.rule_engine.evaluate_position(board, color)
        rule_score = rule_eval.total_score
        explanation = rule_eval.summary()
        
        # Neural network correction (if available)
        if self.neural_net:
            neural_score = self.neural_net.evaluate(board)
            correction = neural_score - rule_score
            
            # Limit the correction to prevent it from overwhelming the rules
            max_correction = 50  # Maximum 50cp correction
            correction = max(-max_correction, min(max_correction, correction))
            
            final_score = rule_score + correction
            
            if abs(correction) > 10:
                explanation += f"\n[Neural correction: {correction:+d}cp — subtle factors not captured by rules]"
        else:
            final_score = rule_score
        
        return final_score, explanation
```

## The Concept Space of Chess

### What Concepts Do We Need?

The concept layer of our CBM must contain enough concepts to explain chess reasoning comprehensively. Our concept space is organized into the six categories described in [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]]:

| Category | Concepts | Count |
|----------|----------|-------|
| Material | Piece values, bishop pair, material imbalance, exchange advantage | ~5 |
| Tactical | LPDO, pins, forks, discovered attacks, hanging captures | ~6 |
| Opening | Development, castling, central control, queen early | ~4 |
| Trap | Back rank mate, smothered mate, sacrifice patterns, stalemate | ~4 |
| Strategy | Pawn structure, knight outpost, bad bishop, open file, prophylaxis | ~8 |
| Safety | Pawn shield, king exposure, attack units, open files near king | ~4 |

**Total: ~31 concepts** — enough to explain the vast majority of chess decisions, but small enough that each concept is meaningful and distinct.

### Concept Completeness

Is our concept space **complete**? That is, can every important chess decision be explained using these 31 concepts? The answer is: *almost*. There are edge cases where a concept is missing (e.g., "opposite-colored bishops in endgame" or "rook on the 7th rank"), but these can be added as new rules. The CBM architecture is designed to be **extensible**: new concepts can be added without modifying existing ones.

### Concept Orthogonality

An ideal concept space has **orthogonal** concepts—concepts that measure independent features. In practice, chess concepts are not perfectly orthogonal:
- "Knight Outpost" and "Piece Activity" overlap (an outpost knight is also active)
- "Bad Bishop" and "Pawn Structure" overlap (a bad bishop is defined by pawn structure)
- "King Safety" and "Attack Units" overlap (attack units measure threats to the king)

This overlap leads to some double-counting in the additive score combination, which is a known limitation discussed in [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|Multi-Rule Decision Making]]. The trade-off between orthogonality and comprehensiveness is acceptable because the overlap is small and the concepts are individually meaningful.

## The CBM Guarantee and Chess Education

The ultimate value of the CBM architecture is in **chess education**. When a student asks "why is this move good?", the CBM guarantee ensures that the answer is:
1. **Complete**: Every relevant concept is included
2. **Accurate**: The concepts faithfully represent the computation
3. **Learnable**: The student can study each concept independently
4. **Verifiable**: The student can check the concept values against the position

This transforms the chess engine from a black-box oracle into a transparent teacher—exactly the goal of our project.

---

*Previous: [[09-Explainable-AI-for-Chess/01 - Explainable AI (XAI) Overview|01 - Explainable AI (XAI) Overview]] ←*
*Next: [[09-Explainable-AI-for-Chess/03 - Post-Hoc Rationalization and Surrogate Models|03 - Post-Hoc Rationalization and Surrogate Models]] →*
*See also: [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]] | [[08-Rule-Based-Reasoning-Systems/02 - Chess Knowledge Representation|Chess Knowledge Representation]] | [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]]*
