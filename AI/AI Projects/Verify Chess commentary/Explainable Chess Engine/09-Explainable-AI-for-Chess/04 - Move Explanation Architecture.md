---
tags:
  - chapter-09
  - xai
  - move-explanation
  - heuristic-delta
  - explanation-pipeline
  - architecture
  - delta-formula
---

# 04 - Move Explanation Architecture

## The Full Pipeline for Explaining a Move

The move explanation architecture is the **crown jewel** of the explainable chess engine. It is the system that takes a position, a move, and the engine's analysis, and produces a coherent, human-readable explanation of why the move was played.

The pipeline has five stages:

### Stage 1: Engine Selects Best Move via Search

The search algorithm ([[02-Search-Algorithms/01 - Minimax Algorithm|minimax]] with [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta pruning]], [[03-Search-Accelerators/01 - Iterative Deepening|iterative deepening]], and [[06-Adaptive-Depth-Control/01 - The Depther Philosophy|adaptive depth]]) selects the best move. This stage produces:

- **Best move**: The move the engine recommends
- **Search depth**: How deeply the position was analyzed
- **Principal variation**: The main line of play
- **Raw score**: The minimax evaluation

This stage is the "thinking" phase—it determines *what* the best move is. The remaining stages determine *why*.

### Stage 2: Run All Rules on the Position Before and After the Move

The [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|rule engine]] evaluates the position comprehensively:

```python
def evaluate_position_with_rules(board: chess.Board, 
                                  color: chess.Color) -> dict[str, tuple[int, str]]:
    """
    Run all rules on a position.
    Returns dict of rule_name → (score, reason).
    """
    results = {}
    for rule in ALL_RULES:
        result = rule.evaluate(board, color=color)
        results[rule.name] = (result.effective_score, result.reason)
    return results
```

This produces two snapshots:
- **Before snapshot**: Rule scores in the position before the move
- **After snapshot**: Rule scores in the position after the move

### Stage 3: Compute Deltas for Each Rule

The **Heuristic Delta Formula** computes the change in each rule's score:

$$\Delta_{\text{Rule}} = \text{Score}_{\text{After}}(\text{Rule}) - \text{Score}_{\text{Before}}(\text{Rule})$$

This formula is the mathematical foundation of the explanation system. It converts the *absolute* evaluation of a position into the *relative* impact of a move. A rule that scores +30 before and +65 after the move has a delta of +35—the move improved this aspect by 35 centipawns.

```python
def compute_rule_deltas(board: chess.Board, move: chess.Move,
                        color: chess.Color) -> dict[str, int]:
    """
    Compute the heuristic deltas for all rules.
    
    Δ_Rule = Score_After(Rule) - Score_Before(Rule)
    
    Positive delta = the move improved this aspect
    Negative delta = the move worsened this aspect
    """
    # Evaluate before
    before_results = evaluate_position_with_rules(board, color)
    
    # Evaluate after
    board.push(move)
    after_results = evaluate_position_with_rules(board, color)
    board.pop()
    
    # Compute deltas
    deltas = {}
    for rule_name in before_results:
        before_score = before_results[rule_name][0]
        after_score = after_results[rule_name][0]
        delta = after_score - before_score
        
        if abs(delta) >= 3:  # Significance threshold (3cp)
            deltas[rule_name] = delta
    
    return deltas
```

### Stage 4: The Dominant Positive Delta = Primary Strategic Driver

The rule with the **largest positive delta** is the **primary strategic driver**—the main reason the move is good:

```python
def find_primary_driver(deltas: dict[str, int]) -> tuple[str, int]:
    """
    Find the primary strategic driver: the rule with the
    largest positive delta.
    """
    positive_deltas = {name: delta for name, delta in deltas.items() if delta > 0}
    
    if not positive_deltas:
        # No rule improved — this might be a "least bad" move
        return ("none", 0)
    
    primary = max(positive_deltas.items(), key=lambda x: x[1])
    return primary
```

The rule with the **largest negative delta** is the **primary objection**—the main cost of the move:

```python
def find_primary_objection(deltas: dict[str, int]) -> tuple[str, int]:
    """
    Find the primary objection: the rule with the
    largest negative delta.
    """
    negative_deltas = {name: delta for name, delta in deltas.items() if delta < 0}
    
    if not negative_deltas:
        return ("none", 0)
    
    primary = min(negative_deltas.items(), key=lambda x: x[1])
    return primary
```

### Stage 5: Format Explanation for the Appropriate Audience Level

The final stage takes the structured data (deltas, primary driver, objections) and formats it into a human-readable explanation at the appropriate [[09-Explainable-AI-for-Chess/05 - Audience-Adaptive Explanations|audience level]].

## The Heuristic Delta Formula in Detail

### Mathematical Formulation

Given a position $P$, a move $m$, and a set of rules $\{R_1, R_2, \ldots, R_N\}$:

$$\Delta_{R_i} = \text{Score}_{P'}(R_i) - \text{Score}_{P}(R_i)$$

Where $P' = \text{Apply}(P, m)$ is the position after the move.

The **total heuristic delta** is:

$$\Delta_{\text{total}} = \sum_{i=1}^{N} w_i \cdot \Delta_{R_i}$$

The **primary driver** is:

$$R^* = \arg\max_{R_i} (w_i \cdot \Delta_{R_i})$$

The **primary objection** is:

$$R^- = \arg\min_{R_i} (w_i \cdot \Delta_{R_i})$$

### Why Deltas, Not Absolute Scores?

It might seem more natural to just report the absolute rule scores after the move ("the position has a knight outpost worth +35cp"). But deltas are better for explanation because:

1. **Moves change things**: The user wants to know what *changed*, not what *is*. "This move creates a knight outpost" is more informative than "the position has a knight outpost."
2. **Attribution**: Deltas directly attribute the change to the move. If the knight was already on the outpost before the move, the delta is zero—the move didn't create the outpost.
3. **Comparability**: Deltas enable comparison between moves. "Move A improves the outpost by +35cp; Move B improves king safety by +20cp"—which matters more depends on context, but the delta makes the comparison possible.
4. **Negation**: Negative deltas explain *costs*—what the player gives up by making the move. This is essential for honest, balanced explanations.

### Example: Explaining Nd5

Consider a position where White plays Nd5:

| Rule | Score Before | Score After | Delta | Reason |
|------|-------------|------------|-------|--------|
| Knight Outpost | 0 | +50 | **+50** | Knight now on d5 outpost |
| Material Count | 0 | 0 | 0 | No material change |
| King Safety (our) | +25 | +25 | 0 | No change |
| LPDO Detection | -15 | -15 | 0 | Still undefended bishop on c1 |
| Pawn Structure | -10 | -10 | 0 | Isolated e-pawn unchanged |
| Prophylaxis | 0 | +15 | **+15** | Prevents opponent's ...c5 |
| King Safety (opponent) | -5 | -30 | **-25** | Opponent's king now less safe |

**Primary driver**: Knight Outpost (+50cp) — "Nd5 places the knight on a powerful outpost where it cannot be attacked by enemy pawns"
**Secondary driver**: Prophylaxis (+15cp) — "Nd5 also prevents the opponent's ...c5 pawn break"
**Primary objection**: None significant — this move has no major drawbacks in this position

**Final explanation**: "Nd5 places the knight on a powerful outpost on d5 where it cannot be attacked by pawns, controlling the critical f6 and e7 squares near Black's king. It also prevents Black's desired ...c5 pawn break."

## Full Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    MOVE EXPLANATION PIPELINE                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐                                                 │
│  │  Position P  │                                                │
│  └──────┬──────┘                                                 │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────┐     ┌──────────────────┐                    │
│  │  Search Engine   │────►│  Best Move: Nd5  │                    │
│  │  (Minimax + AB)  │     │  Score: +1.5     │                    │
│  └─────────────────┘     └────────┬─────────┘                    │
│                                   │                              │
│         ┌─────────────────────────┘                              │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────┐                     │
│  │  STAGE 2: Rule Evaluation               │                     │
│  │                                          │                     │
│  │  Before (P):                             │                     │
│  │  ┌─────────────────────────────────┐    │                     │
│  │  │ Knight Outpost: 0               │    │                     │
│  │  │ Material: 0                     │    │                     │
│  │  │ King Safety: +25               │    │                     │
│  │  │ Prophylaxis: 0                  │    │                     │
│  │  │ LPDO: -15                      │    │                     │
│  │  └─────────────────────────────────┘    │                     │
│  │                                          │                     │
│  │  After (P' = Apply(P, Nd5)):            │                     │
│  │  ┌─────────────────────────────────┐    │                     │
│  │  │ Knight Outpost: +50             │    │                     │
│  │  │ Material: 0                     │    │                     │
│  │  │ King Safety: +25               │    │                     │
│  │  │ Prophylaxis: +15               │    │                     │
│  │  │ LPDO: -15                      │    │                     │
│  │  └─────────────────────────────────┘    │                     │
│  └──────────────────┬──────────────────────┘                     │
│                     │                                            │
│                     ▼                                            │
│  ┌─────────────────────────────────────────┐                     │
│  │  STAGE 3: Compute Deltas                │                     │
│  │                                          │                     │
│  │  Δ_Knight Outpost = +50 - 0 = +50       │                     │
│  │  Δ_Material = 0 - 0 = 0                 │                     │
│  │  Δ_King Safety = +25 - +25 = 0          │                     │
│  │  Δ_Prophylaxis = +15 - 0 = +15          │                     │
│  │  Δ_LPDO = -15 - (-15) = 0               │                     │
│  └──────────────────┬──────────────────────┘                     │
│                     │                                            │
│                     ▼                                            │
│  ┌─────────────────────────────────────────┐                     │
│  │  STAGE 4: Identify Primary Driver       │                     │
│  │                                          │                     │
│  │  Primary Driver: Knight Outpost (+50)    │                     │
│  │  Secondary: Prophylaxis (+15)            │                     │
│  │  Primary Objection: None                 │                     │
│  └──────────────────┬──────────────────────┘                     │
│                     │                                            │
│                     ▼                                            │
│  ┌─────────────────────────────────────────┐                     │
│  │  STAGE 5: Format Explanation             │                     │
│  │                                          │                     │
│  │   Beginner:                            │                     │
│  │  "The knight moves to a strong central   │                     │
│  │   square where it can't be attacked by   │                     │
│  │   pawns."                                │                     │
│  │                                          │                     │
│  │   Intermediate:                        │                     │
│  │  "Nd5 places the knight on an outpost    │                     │
│  │   where it cannot be attacked by pawns,  │                     │
│  │   controlling f6 and e7. It also         │                     │
│  │   prevents ...c5."                       │                     │
│  │                                          │                     │
│  │   Advanced:                            │                     │
│  │  "The knight occupies the d5 outpost,    │                     │
│  │   supported by the e4 pawn. The outpost  │                     │
│  │   is permanent as no black pawn can      │                     │
│  │   challenge it. The knight controls the  │                     │
│  │   critical f6 and e7 squares,            │                     │
│  │   restricting Black's king and           │                     │
│  │   preventing the ...c5 pawn break that   │                     │
│  │   would activate Black's queenside."     │                     │
│  └─────────────────────────────────────────┘                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Implementation: The Complete Explanation Engine

```python
class MoveExplanationEngine:
    """
    The complete engine for explaining moves.
    Orchestrates all five stages of the pipeline.
    """
    
    def __init__(self, rule_engine: RuleEngine, search_engine=None):
        self.rule_engine = rule_engine
        self.search_engine = search_engine
    
    def explain_move(self, board: chess.Board, move: chess.Move,
                     audience: str = "intermediate") -> MoveExplanation:
        """
        Generate a complete explanation for a move.
        """
        color = board.turn
        
        # Stage 1: Search (if search engine available)
        search_result = None
        if self.search_engine:
            search_result = self.search_engine.search(board)
        
        # Stage 2: Evaluate with rules before and after
        eval_before = self.rule_engine.evaluate_position(board, color)
        board.push(move)
        eval_after = self.rule_engine.evaluate_position(board, color)
        board.pop()
        
        # Stage 3: Compute deltas
        deltas = {}
        delta_reasons = {}
        for rule_name in eval_before.contributions:
            before_val = eval_before.contributions.get(rule_name, 0)
            after_val = eval_after.contributions.get(rule_name, 0)
            delta = after_val - before_val
            if abs(delta) >= 3:
                deltas[rule_name] = delta
                # Get the reason from the after-evaluation (more relevant)
                delta_reasons[rule_name] = eval_after.reasons.get(rule_name, "")
        
        # Stage 4: Identify primary driver and objection
        positive = {n: d for n, d in deltas.items() if d > 0}
        negative = {n: d for n, d in deltas.items() if d < 0}
        
        primary_driver = max(positive.items(), key=lambda x: x[1]) if positive else None
        primary_objection = min(negative.items(), key=lambda x: x[1]) if negative else None
        
        total_delta = sum(deltas.values())
        
        # Stage 5: Format explanation
        explanation = self._format_explanation(
            board, move, deltas, delta_reasons,
            primary_driver, primary_objection,
            total_delta, audience
        )
        
        return MoveExplanation(
            move=move,
            move_san=board.san(move),
            deltas=deltas,
            delta_reasons=delta_reasons,
            primary_driver=primary_driver,
            primary_objection=primary_objection,
            total_delta=total_delta,
            explanation=explanation,
            audience=audience,
            search_result=search_result
        )
    
    def _format_explanation(self, board, move, deltas, reasons,
                            primary_driver, primary_objection,
                            total_delta, audience) -> str:
        """Format the explanation for the given audience level."""
        move_san = board.san(move)
        
        if not deltas:
            return f"{move_san} maintains the current position without significant changes."
        
        if audience == "beginner":
            return self._format_beginner(move_san, primary_driver, primary_objection, reasons)
        elif audience == "intermediate":
            return self._format_intermediate(move_san, deltas, primary_driver, primary_objection, reasons)
        elif audience == "advanced":
            return self._format_advanced(move_san, deltas, primary_driver, primary_objection, reasons, total_delta)
        
        return f"{move_san}: {total_delta:+d}cp"
    
    def _format_beginner(self, move_san, driver, objection, reasons) -> str:
        if driver:
            name, delta = driver
            reason = reasons.get(name, "")
            text = f"{move_san} is a good move because {reason.lower()}."
        else:
            text = f"{move_san} is the best available move."
        
        if objection and abs(objection[1]) > 20:
            text += f" Be careful: {reasons.get(objection[0], 'this creates a weakness').lower()}."
        
        return text
    
    def _format_intermediate(self, move_san, deltas, driver, objection, reasons) -> str:
        parts = [move_san]
        
        if driver:
            name, delta = driver
            parts.append(f"improves {name.lower()} ({reasons.get(name, '')})")
        
        # Add secondary factors
        secondary = [(n, d) for n, d in sorted(deltas.items(), key=lambda x: -x[1]) 
                     if d > 0 and n != (driver[0] if driver else "")]
        if secondary:
            sec_names = [f"{n.lower()}" for n, _ in secondary[:2]]
            parts.append(f"and also improves {', '.join(sec_names)}")
        
        if objection:
            name, delta = objection
            parts.append(f"though {name.lower()} worsens ({reasons.get(name, '')})")
        
        return " — ".join(parts) + "."
    
    def _format_advanced(self, move_san, deltas, driver, objection, reasons, total) -> str:
        parts = [f"{move_san} (net: {total:+d}cp)"]
        
        # All contributing factors
        sorted_deltas = sorted(deltas.items(), key=lambda x: -x[1])
        
        for name, delta in sorted_deltas[:5]:
            reason = reasons.get(name, "")
            parts.append(f"{name}: {delta:+d}cp — {reason}")
        
        return "\n".join(parts)


@dataclass
class MoveExplanation:
    """Complete explanation for a move."""
    move: chess.Move
    move_san: str
    deltas: dict[str, int]
    delta_reasons: dict[str, str]
    primary_driver: Optional[tuple[str, int]]
    primary_objection: Optional[tuple[str, int]]
    total_delta: int
    explanation: str
    audience: str
    search_result: Optional[any] = None
    
    def __str__(self) -> str:
        return self.explanation
    
    def detailed(self) -> str:
        """Return a detailed breakdown with all deltas."""
        lines = [f"Move: {self.move_san}", f"Total delta: {self.total_delta:+d}cp", ""]
        
        for name, delta in sorted(self.deltas.items(), key=lambda x: -x[1]):
            reason = self.delta_reasons.get(name, "")
            marker = "" if delta > 0 else "" if delta < 0 else ""
            lines.append(f"  {marker} {name}: {delta:+d}cp — {reason}")
        
        return "\n".join(lines)
```

## The Heuristic Delta as a Universal Explanation Method

The Heuristic Delta Formula is the universal explanation method because it can explain *any* move in terms of *any* rule set. The same pipeline explains:

- **Tactical moves**: Large deltas in material, LPDO, or hanging capture rules
- **Strategic moves**: Large deltas in outpost, structure, or prophylaxis rules
- **Defensive moves**: Large negative deltas prevented in safety rules
- **Prophylactic moves**: Large deltas in prophylaxis rule
- **Endgame moves**: Large deltas in pawn structure and material rules

The delta framework is what makes the engine a true [[09-Explainable-AI-for-Chess/02 - Concept Bottleneck Models|Concept Bottleneck Model]]: the explanation is not a separate system bolted on after the fact, but a direct measurement of how the move affects each human concept in the bottleneck.

---

*Previous: [[09-Explainable-AI-for-Chess/03 - Post-Hoc Rationalization and Surrogate Models|03 - Post-Hoc Rationalization and Surrogate Models]] ←*
*Next: [[09-Explainable-AI-for-Chess/05 - Audience-Adaptive Explanations|05 - Audience-Adaptive Explanations]] →*
*See also: [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|Multi-Rule Decision Making]] | [[08-Rule-Based-Reasoning-Systems/05 - The Rule Module System (Code)|The Rule Module System]] | [[07-Chess-Psychology-and-Human-Thinking/01 - Human Chess Thinking Models|Human Chess Thinking Models]]*
