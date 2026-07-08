# Static Evaluation Overview

> "The evaluation function is the soul of a chess engine. It encodes everything the engine 'knows' about chess in a single number."
> — Chess Programming Wiki

## What Is Static Evaluation?

[[Static Evaluation]] is the process of assigning a **single numeric score** to a chess position **without searching any moves deeper**. It is a snapshot assessment—a heuristic judgment of "who is better and by how much" based purely on the configuration of pieces on the board at this exact moment. In classical chess programming, the static evaluation function (often called `evaluate()`) is the most frequently called function in the entire engine, invoked millions of times per search. Its design therefore embodies a fundamental tension: **accuracy versus speed**.

The evaluation function takes a position $P$ and returns a score $s$:

$$
s = \text{evaluate}(P) \in \mathbb{Z}
$$

In our engine, the score is measured in **centipawns** (1/100th of a pawn), where positive values favor White and negative values favor Black. A score of +100 means White is ahead by roughly one pawn; +300 means roughly the equivalent of a minor piece.

## Why Must Evaluation Be Fast?

The evaluation function sits at the **leaf nodes** of the [[Alpha-Beta Search]] tree. Every time the search reaches a leaf—or every time [[Quiescence Search]] needs to stand pat—the evaluation function is called. Consider the math:

- A depth-8 search with average branching factor 35 explores roughly $35^4 \approx 1.5$ million nodes (with alpha-beta pruning cutting the effective branching factor).
- Modern engines evaluate **1–10 million positions per second**.
- If evaluation takes 1 microsecond, that is 1 second per million calls. If it takes 10 microseconds, that is 10 seconds—already a significant chunk of time budget.

**Every microsecond matters.** This is why traditional evaluation functions use:

1. **Incremental updates** — only recalculate what changed after a move, not the whole board.
2. **Piece-Square Tables** — simple array lookups, $O(1)$ per piece.
3. **Lazy evaluation** — if the material balance is so lopsided that the position is clearly won/lost, skip the expensive terms.
4. **Cache** — [[Transposition Table]] entries store evaluation scores alongside search results.

In our explainable engine, we accept a modest performance cost to generate **reasoning traces** alongside the score. We do not use neural networks (which are fast at inference but opaque); instead, we use **rule-based heuristics** where every term has a human-readable name and explanation.

## Material as the Foundation

The most fundamental component of any evaluation function is **material count**—the total point value of each side's pieces. Material is the bedrock because:

- It is **objective**: a rook is worth about 5 pawns regardless of position (with rare exceptions).
- It is **easy to compute**: sum up piece values.
- It **dominates** the evaluation in most positions: the side with more material usually wins.

All other evaluation terms—[[Piece-Square Tables]], [[Pawn Structure]], [[King Safety]], [[Mobility and Piece Activity]]—are modifiers layered on top of the material base. They add nuance, but material is the anchor.

The general form of our evaluation is:

$$
s = \underbrace{M}_{\text{material}} + \underbrace{PST}_{\text{piece-square}} + \underbrace{PS}_{\text{pawn structure}} + \underbrace{KS}_{\text{king safety}} + \underbrace{MO}_{\text{mobility}} + \underbrace{TH}_{\text{threats}} + \ldots
$$

Each term is computed independently and summed. This **additive model** is simple, fast, and—crucially for our project—**explainable**. We can report: "The position is +150 because: material +100, bishop pair +50, king safety -20, pawn structure +20."

## Side-to-Move Perspective

A critical design decision: **from whose perspective is the score reported?** There are two conventions:

1. **White-positive**: Positive = White is better, always. This is the traditional convention used in [[Centipawns|centipawn]] reporting.
2. **Side-to-move-positive**: Positive = the side whose turn it is to move is better. This is used internally by many search algorithms because it simplifies [[Negamax]].

Our engine uses **side-to-move-positive internally** (for Negamax compatibility) and converts to **White-positive for display and explanation**. The conversion is trivial:

```python
def evaluate(board: Board) -> int:
    """Return score from side-to-move's perspective (Negamax convention)."""
    raw = _raw_evaluate(board)  # White-positive
    return raw if board.turn == WHITE else -raw
```

This convention ensures that the search can always maximize the score without worrying about sign flips.

## Explainability: The Design Principle

Unlike neural-network evaluators (e.g., [[NNUE]] used in Stockfish), our evaluation function is **fully decomposable and explainable**. Every score component carries metadata:

```python
@dataclass
class EvalTerm:
    name: str           # e.g., "Material Balance"
    value: int          # centipawns, e.g., +150
    reason: str         # e.g., "White has an extra knight"
    priority: int       # for narrative ordering, lower = more important

@dataclass
class EvalResult:
    score: int                    # total score
    terms: List[EvalTerm]         # individual contributions
    explanation: str              # natural language summary

    def summary(self) -> str:
        parts = [f"{t.name}: {t.value:+d}" for t in sorted(self.terms, key=lambda t: t.priority)]
        return f"Score: {self.score:+d} cp | " + ", ".join(parts)
```

This means that when the engine recommends a move, it can answer **"why?"** with a breakdown:

> "The position is +230 centipawns. Material: +100 (White has an extra pawn). Bishop Pair: +50 (White has both bishops). King Safety: -20 (White's king lacks pawn shield). Passed Pawn: +100 (White has a passed pawn on e6)."

This is the core promise of the [[Explainable Chess Engine]] project: every number has a name, and every name has a story.

## The Evaluation Pipeline

Our evaluation pipeline follows a strict ordering, from cheapest to most expensive to compute:

```
┌─────────────────┐
│  Material       │  ← O(1) per piece, simple sum
├─────────────────┤
│  Piece-Square   │  ← O(1) per piece, table lookup
├─────────────────┤
│  Pawn Structure │  ← O(pawns), pawn-specific heuristics
├─────────────────┤
│  King Safety    │  ← O(1), check pawn shield + attackers
├─────────────────┤
│  Mobility       │  ← O(pieces × moves), count legal moves
├─────────────────┤
│  Threats        │  ← O(pieces × pieces), attack detection
└─────────────────┘
```

Each stage can **short-circuit**: if the material imbalance exceeds a threshold (e.g., >1000 centipawns), the function can return early without computing the more expensive terms. This is the [[Lazy Evaluation]] optimization.

## Relationship to Search

It is essential to understand that static evaluation is **not** the final word on a position's value. The search algorithm (see [[Alpha-Beta Search]], [[Iterative Deepening]]) uses static evaluation as a **stand-in** for "the truth" at leaf nodes. The search can override the evaluation when it discovers tactical sequences (checks, captures, threats) that the static eval misses.

This is why [[Quiescence Search]] exists: to continue searching captures and checks at depth 0, preventing the **horizon effect** where the engine evaluates a position as +200 but misses that the opponent can recapture a queen on the next move.

The interplay between evaluation and search is the engine's core dynamic:

- **Evaluation** provides the heuristic assessment.
- **Search** verifies or corrects that assessment through tactical exploration.
- **Explainability** bridges the two: the engine can say "I evaluated this position as +150 based on these heuristics, and the search confirmed it by finding no tactical refutation."

## Performance Constraints in Practice

Here are the typical performance budgets for each evaluation term, measured in nanoseconds on a modern CPU:

| Term | Time (ns) | % of Total |
|------|-----------|------------|
| Material | 50 | 5% |
| Piece-Square Tables | 100 | 10% |
| Pawn Structure | 200 | 20% |
| King Safety | 150 | 15% |
| Mobility | 300 | 30% |
| Threats | 200 | 20% |
| **Total** | **1000** | **100%** |

At 1000 ns per evaluation, we can evaluate roughly 1 million positions per second—adequate for a depth-8 search within a 5-second time budget. Our explainability overhead (generating `EvalTerm` objects and reason strings) adds roughly 30% to this cost, but we consider it acceptable for the explanatory benefit.

## Evaluation in the Game Phase

Chess positions evolve through phases: opening → middlegame → endgame. Our evaluation function **interpolates between middlegame and endgame tables** based on the total material remaining:

```python
def game_phase(board: Board) -> float:
    """Return 0.0 (endgame) to 1.0 (middlegame)."""
    total_material = sum(PIECE_VALUES[p] for p in board.pieces if p != KING and p != PAWN)
    max_material = 2 * (2 * 320 + 2 * 330 + 2 * 500 + 900)  # both sides full
    return min(1.0, total_material / max_material)
```

This allows [[Piece-Square Tables]] and [[King Safety]] to smoothly transition: the king should hide in the corner during the middlegame but activate in the endgame.

---

**See also:** [[Material Evaluation]], [[Piece-Square Tables]], [[Pawn Structure Evaluation]], [[King Safety Evaluation]], [[Mobility and Piece Activity]], [[Threats and Tactical Patterns]], [[Alpha-Beta Search]], [[Quiescence Search]], [[Lazy Evaluation]], [[NNUE]]
