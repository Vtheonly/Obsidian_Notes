---
tags:
  - foundations
  - explainability
  - core-concept
  - multi-rule
  - confidence-scoring
chapter: "01"
---

# The Explainability Problem

## Overview

This is the **core note** of the entire Explainable Chess Engine project. Everything else — the [[01-Foundations/02 - Board Representation|board representation]], the [[02-Search-Algorithms/03 - Alpha-Beta Pruning|search algorithms]], the [[03-Search-Accelerators/02 - Move Ordering|acceleration techniques]] — exists to support the goal articulated here: building a chess engine that doesn't just find the best move, but can **explain why** using human-understandable reasoning.

---

## The Black Box Problem

### Traditional Chess Engines Are Opaque

Modern chess engines like Stockfish, Leela Chess Zero, and Komodo are extraordinarily strong — far stronger than any human player. Yet their "reasoning" is completely opaque:

```
Stockfish 16.1 on position r1bqkbnr/pppppppp/2n5/8/4P3/8/PPPP1PPP/RNBQKBNR:
  Best move: d2d4
  Evaluation: +0.35
  Depth: 28
  Nodes searched: 45,230,891
```

The engine tells us **what** it wants to play and **how good** it thinks the position is. It tells us nothing about **why**. The number +0.35 is a single scalar that compresses all of chess wisdom — material, structure, king safety, piece activity, pawn dynamics, timing — into one inscrutable number.

### The Gap Between Engine Evaluation and Human Understanding

Human chess players do not think in terms of "+0.35". They think in terms of **principles**:

- "I'm controlling the center with my pawns."
- "My knight has an outpost on d5."
- "My opponent's king is exposed — I should open the position."
- "If I trade bishops, his remaining bishop is bad."
- "This pawn push creates a passed pawn."

These are **declarative, conceptual, and qualitative** statements. The engine's evaluation is **numerical, procedural, and quantitative**. There is a fundamental **representation gap** between how the engine "thinks" and how humans understand chess.

This gap has real consequences:
- **Learning**: Players cannot improve by studying engine moves if they don't understand the reasoning.
- **Trust**: Players may reject engine recommendations because they seem counterintuitive, even when the engine is correct.
- **Accessibility**: Chess engines are tools for the elite; beginners gain little from "+0.35".
- **Debugging**: Engine developers cannot easily understand why their engine makes a particular choice.

---

## What an "Explanation" Means in Chess

### Defining Chess Explanation

An **explanation** for a chess move is a structured argument that identifies which **principles, rules, and heuristics** support (or oppose) that move, along with a **confidence weight** indicating how much each principle contributed to the decision.

Formally, let $M^*$ be the chosen move. An explanation is a set of weighted principles:

$$\text{Explain}(M^*) = \{(P_1, w_1), (P_2, w_2), \ldots, (P_n, w_n)\}$$

Where:
- $P_i$ is a chess principle (e.g., "controls the center", "develops a piece", "improves king safety")
- $w_i \in [0, 1]$ is the weight or confidence that $P_i$ supports $M^*$
- $\sum_{i=1}^{n} w_i = 1$ (normalized to 100%)
- Each $P_i$ may itself have a **justification** (evidence from the position)

### Example Explanation

Position: After `1. e4 c5 2. Nf3` (Sicilian Defense)

**Engine output without explainability:**
```
Best move: Nf3
Score: +0.20
```

**Engine output with explainability:**
```
Best move: Nf3

Explanation:
  (1) Develops a piece toward the center (+35%)
      - The knight moves from g1 to f3, controlling d4 and e5
      - f3 is a natural development square for the king's knight
  (2) Prepares to castle kingside (+25%)
      - The knight clears g1, but more importantly, Nf3 is part of
        the standard kingside development path (Nf3, Bc4/Bb5, O-O)
  (3) Controls key central squares (+20%)
      - Nf3 attacks d4 and e5, contesting Black's central influence
  (4) Maintains flexibility (+10%)
      - After Nf3, White can play d4, Bc4, Bb5, or Nc3 depending
        on Black's response
  (5) Follows opening principle: "Knights before bishops" (+10%)
      - The knight has fewer optimal squares than the bishop in the
        opening; developing it first is generally correct
```

This explanation decomposes the single evaluation number into **five human-understandable principles**, each with a weight and supporting evidence.

---

## The Multi-Rule Decision Problem

### Multiple Principles Can Support the Same Move

In most positions, a good move is supported by **multiple independent principles** simultaneously. The move `Nf3` above is good because it develops, controls the center, prepares castling, and maintains flexibility. No single principle fully explains the move — it is the **convergence of multiple principles** that makes it the best choice.

### Principles Can Conflict

Consider a position where:
- Pushing a pawn gains central control (principle: "control the center")
- But weakens the king's pawn shield (principle: "maintain king safety")
- And creates a backward pawn on an open file (principle: "avoid pawn weaknesses")

The engine must navigate this **tradeoff**: the same move is supported by one principle and opposed by others. The explanation must capture this conflict:

```
Best move: e4

Explanation:
  (1) Controls the center — challenges Black's d5 pawn (+40%)
  (2) Opens lines for the bishop on c1 (+15%)
  (3) BUT weakens d4 square — opponent can place a piece there (-15%)
  (4) BUT slightly exposes the king if castled queenside (-5%)

Net: The central control and piece activity outweigh the structural
     weaknesses in this position.
```

### The Weighting Challenge

Assigning weights $w_i$ to each principle is itself a non-trivial problem. Several approaches exist:

1. **Correlation with evaluation delta**: Measure how much each principle's score changes between the position before and after the move, and use the proportional change as the weight.

2. **Ablation analysis**: Temporarily disable each principle in the evaluation function and measure how much the move's score drops. The larger the drop, the more important that principle was.

3. **Feature attribution from machine learning**: Train a model to predict the engine's evaluation from principle scores, then use SHAP values or gradient-based attribution to determine each principle's contribution.

4. **Rule-based confidence**: Each principle computes a confidence score based on the position, and weights are proportional to these scores.

This project primarily uses approach **4** (rule-based confidence) with validation from approach **1** (evaluation delta correlation).

---

## Confidence Scoring

### Definition

A **confidence score** $c(P, m)$ represents how strongly principle $P$ supports move $m$ in the current position. It ranges from $-1$ (strongly opposes) to $+1$ (strongly supports), with $0$ meaning the principle is neutral or irrelevant.

### Computation

Each principle implements a scoring function:

```cpp
struct PrincipleScore {
    float score;      // -1.0 to +1.0
    float weight;     // How important this principle is in this position
    std::string reason; // Human-readable justification
};

class Principle {
public:
    virtual PrincipleScore evaluate(const Position& before,
                                    const Position& after,
                                    Move move) = 0;
    virtual std::string name() const = 0;
};
```

Example implementation for "Center Control":

```cpp
class CenterControl : public Principle {
    static constexpr uint64_t CENTER = (1ULL << D4) | (1ULL << D5)
                                      | (1ULL << E4) | (1ULL << E5);

    PrincipleScore evaluate(const Position& before, const Position& after,
                           Move move) override {
        uint64_t old_attacks = get_side_attacks(before, before.side_to_move);
        uint64_t new_attacks = get_side_attacks(after, before.side_to_move);

        int old_center = __builtin_popcountll(old_attacks & CENTER);
        int new_center = __builtin_popcountll(new_attacks & CENTER);

        float delta = (float)(new_center - old_center) / 4.0f; // Normalize to [-1, 1]

        PrincipleScore result;
        result.score = std::clamp(delta, -1.0f, 1.0f);
        result.weight = 0.3f; // Center control is moderately important
        result.reason = fmt::format("Center control: {} -> {} squares",
                                    old_center, new_center);
        return result;
    }

    std::string name() const override { return "Center Control"; }
};
```

### Aggregation

The final confidence for each principle is:

$$w_i = \frac{c(P_i, m) \cdot \text{importance}(P_i)}{\sum_j |c(P_j, m)| \cdot \text{importance}(P_j)}$$

This normalizes the weights to sum to 1.0, with each principle's contribution proportional to both its confidence score and its contextual importance.

---

## Three Audience Levels

Chess explanations must adapt to the audience. A grandmaster needs different information than a beginner.

### Level 1: Beginner

**Focus**: Simple, visual, concrete. No abstract concepts.

```
Move: Nf3

Why this move is good:
   The knight moves to a better square in the center
   It attacks two important squares in the middle of the board
   It helps prepare castling to keep your king safe

The knight was doing nothing on g1, and now it's active in the center!
```

### Level 2: Intermediate

**Focus**: Named principles, tactical themes, positional concepts.

```
Move: Nf3

Explanation:
  (1) Development (+35%) — The knight develops toward the center,
      following the principle "knights before bishops"
  (2) Center control (+30%) — Nf3 pressures d4 and e5, key central
      squares in the Sicilian structure
  (3) King safety (+25%) — Nf3 is a key step toward O-O castling,
      securing the king
  (4) Flexibility (+10%) — Keeps multiple setup options available
```

### Level 3: Advanced

**Focus**: Deep strategic reasoning, concrete variations, engine-level analysis.

```
Move: Nf3

Explanation:
  (1) Central tension management (+35%)
      - Nf3 maintains the e4 pawn while contesting d4
      - In the Open Sicilian (d4 next), Nf3 recaptures on d4
        preserving the central pawn majority
      - Alternative: Nc3 commits to a different structure where
        d4 is less supported

  (2) Development efficiency (+25%)
      - f3 is the highest-utility square for the g1 knight
      - Controls 4 key squares: d4, e5, g1, h4
      - Piece-square table value: +30 centipawns improvement

  (3) Castling pathway (+20%)
      - Nf3 is prerequisite for O-O in standard Sicilian lines
      - Delayed castling after Nc3/e2 is possible but
        statistically weaker at master level

  (4) Tactical coverage (+15%)
      - Nf3 prevents ...Qh4 in some lines
      - Blocks the h5-e8 diagonal for Black's queen

  (5) Transpositional flexibility (+5%)
      - Can reach Open, Closed, Alapin, and Grand Prix setups
```

### Implementation

The explanation engine produces all three levels simultaneously, selecting the appropriate one based on the user's preference:

```cpp
struct Explanation {
    Move move;
    std::vector<WeightedPrinciple> principles;
    std::string beginner_text;
    std::string intermediate_text;
    std::string advanced_text;
};
```

---

## How This Project Differs from Stockfish

### Stockfish's Approach

Stockfish is a **pure performance engine**. Its goals are:
1. Find the strongest move as quickly as possible
2. Evaluate positions as accurately as possible
3. Search as deeply as possible

Stockfish's evaluation is a complex neural network (NNUE) that takes the board state as input and outputs a single number. This number is an excellent predictor of the position's objective value, but it is completely **opaque** — even the Stockfish developers cannot decompose the NNUE output into human concepts.

Stockfish's search is heavily optimized with pruning (alpha-beta, LMR, null move) and acceleration (TT, move ordering). The search determines the best move, but the search tree is discarded after the decision — there is no record of *why* branches were pruned or *why* moves were preferred.

### This Project's Approach

The Explainable Chess Engine has a **fundamentally different goal**:

| Aspect | Stockfish | This Project |
|--------|-----------|-------------|
| Goal | Best move, fastest | Best move, explained |
| Evaluation | NNUE (black box) | Decomposed principles |
| Search output | Move + score | Move + score + reasoning chain |
| Pruning justification | None | "This branch was cut because..." |
| User output | +0.35 | Structured explanation |
| Audience | Engine developers | Chess players at all levels |

### Key Architectural Differences

1. **Decomposed evaluation**: Instead of a monolithic NNUE, the evaluation function consists of **independently scored principles** (material, center control, king safety, piece activity, pawn structure, etc.) that can be individually inspected and explained.

2. **Reasoning trace**: The search records a **reasoning trace** — not just the best move, but which principles were active at each decision point, which branches were pruned and why, and how the evaluation changed across the search tree.

3. **Multi-level output**: The explanation system produces beginner, intermediate, and advanced explanations from the same underlying analysis.

4. **Confidence-weighted principles**: Each principle contributes a weighted score, and the weights form the basis of the explanation. "This move was chosen because principle A contributed 40%, principle B contributed 30%..."

5. **Explainable pruning**: When a branch is pruned (alpha-beta cutoff, LMR, null move), the explanation system records *why* — what was the threshold, what was the current best, and what principle made the current best strong enough to justify the cutoff.

---

## The Vision

The ultimate goal is a chess engine that produces output like:

```
Position: r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4

Best move: d2d3 (d3)

Explanation for intermediate players:

  This move was chosen because:

  (1) Develops the dark-squared bishop (+30%)
      After d3, the bishop on c1 can develop to f4 or e3,
      completing your minor piece development.

  (2) Solidifies the center (+25%)
      d3 supports the e4 pawn, preventing Black from
      challenging it with ...d5 or ...Nxe4 tricks.

  (3) Prepares castling (+20%)
      With d3 played, the queen's bishop has a clear path
      out, and O-O can follow on the next move.

  (4) Maintains pawn structure integrity (+15%)
      Unlike d4, d3 does not create potential pawn weaknesses
      if Black exchanges on d4.

  (5) Follows Italian Game theory (+10%)
      d3 is the modern treatment of the Italian Game,
      preferred at top level over the older d4 lines.

  Alternatives considered:
  - d4: Also strong but creates more tactical complexity
    and potential pawn weaknesses (supported by center
    control at +50% but opposed by structure concerns at -20%)
  - Nc3: Develops a piece but blocks the c-pawn and
    doesn't support e4 as well (supported by development
    at +40% but opposed by flexibility at -15%)
```

This is the promise of explainable chess — not just answers, but **understanding**.

---

## Key Takeaways

- Traditional engines are **black boxes** — they output a move and a score but not *why*.
- An **explanation** decomposes the single evaluation number into multiple human-understandable principles with confidence weights.
- The **multi-rule decision problem** means multiple principles can simultaneously support or oppose a move, and the system must navigate conflicts.
- **Confidence scoring** assigns weights to each principle based on its contribution to the move's evaluation.
- **Three audience levels** (beginner, intermediate, advanced) ensure explanations are accessible to all players.
- This project differs from Stockfish in its **fundamental goal**: not just finding the best move, but explaining why using human concepts.
- The vision is an engine that says "This move was chosen because: (1) principle A (+40%), (2) principle B (+30%), (3) principle C (+20%), (4) principle D (+10%)".

## Cross-References

- [[01-Foundations/01 - Chess as a Zero-Sum Game|Chess as a Zero-Sum Game]] — why the zero-sum property helps explanation symmetry
- [[01-Foundations/02 - Board Representation|Board Representation]] — how bitboards enable fast principle checking
- [[01-Foundations/03 - Move Generation|Move Generation]] — the move list that feeds the explanation pipeline
- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — explainable pruning: "this branch was cut because..."
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — move ordering as the engine's "intuition"
