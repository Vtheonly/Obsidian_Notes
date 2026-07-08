---
tags:
  - search
  - alpha-beta
  - pruning
  - optimization
  - core-algorithm
chapter: "02"
---

# Alpha-Beta Pruning

## Overview

**Alpha-Beta Pruning** is the single most important optimization in game-tree search. It dramatically reduces the number of nodes evaluated while guaranteeing the exact same result as full [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax]] search. Without alpha-beta, competitive chess engines would be impossible — it is the algorithmic breakthrough that makes deep search feasible.

This note explains alpha-beta in exhaustive detail: the alpha and beta windows, how cutoffs work, fail-soft vs. fail-hard, the mathematical limits, and the critical connection to [[03-Search-Accelerators/02 - Move Ordering|move ordering]].

---

## The Core Insight

### Why Explore Every Node?

Full Minimax explores every node in the game tree. But many of these nodes **cannot possibly affect the final result**. Consider:

You're at a max node and have already found a move worth +5. You start examining the next move. If the first child of this next move returns -3 (from the child min node, which chose its minimum), then you know this move is worth at most -3... but you already have +5. **Nothing this subtree can produce will change your decision.** You can prune it immediately.

This is alpha-beta pruning: **cut off branches that cannot influence the final decision.**

### The Analogy

Imagine you're choosing the best restaurant. You've already found one rated 4.5 stars. You start investigating another restaurant. The first review you read gives it 2 stars. Even if subsequent reviews might be higher, the *average* cannot possibly exceed 4.5 — you already know this restaurant can't beat your current best. You stop reading and move on.

---

## The Alpha and Beta Windows

### Definitions

- **Alpha ($\alpha$)**: The **minimum score** that the maximizing player is guaranteed (the best score White has found so far on this path). Alpha starts at $-\infty$.
- **Beta ($\beta$)**: The **maximum score** that the minimizing player will allow (the best score Black has found so far on this path). Beta starts at $+\infty$.

The **alpha-beta window** $[\alpha, \beta]$ defines the range of scores that are still "interesting." Scores below $\alpha$ are too good for the minimizer (the maximizer already has better). Scores above $\beta$ are too good for the maximizer (the minimizer already has better).

### The Pruning Condition

$$\text{If } \alpha \geq \beta, \text{ prune (cutoff)}$$

When the alpha floor meets or exceeds the beta ceiling, the window has collapsed. No score in this range can affect the decision at a higher level.

---

## Alpha-Beta with Negamax

Using the [[02-Search-Algorithms/02 - Negamax Formulation|Negamax]] framework, alpha-beta becomes particularly elegant:

```python
def negamax_ab(position, depth, alpha, beta):
    if depth == 0 or position.is_terminal():
        return evaluate_for_side(position)

    for move in position.generate_legal_moves():
        position.make_move(move)
        # Negate score AND swap alpha/beta for the opponent's perspective
        score = -negamax_ab(position, depth - 1, -beta, -alpha)
        position.unmake_move(move)

        if score >= beta:
            return beta    # Beta cutoff — position is too good for us
                           # Opponent would never allow this
        if score > alpha:
            alpha = score  # New best score found

    return alpha
```

### Key Observations

1. **Beta cutoff** (`score >= beta`): We found a move so good that the opponent (who chose this branch) would never allow it — they have a better option elsewhere. We can stop searching this node's remaining moves.

2. **Alpha update** (`score > alpha`): We found a better move than our previous best. Update alpha to tighten the window.

3. **Window negation**: When recursing, we pass `-beta, -alpha` because the child evaluates from the opponent's perspective. Their alpha is our negated beta, and their beta is our negated alpha.

---

## How Beta Cutoffs Work: A Tree Diagram

Consider this depth-3 tree with branching factor 2:

```
              MAX (α=-∞, β=+∞)
             /                    \
        MIN (α=-∞, β=+∞)     MIN (α=-∞, β=+∞)
        /          \              /          \
     MAX         MAX          MAX          MAX
    / \         / \          / \          / \
   3    5     2    6      1    8       ← PRUNED
```

**Trace with alpha-beta:**

1. **Root (MAX, α=-∞, β=+∞)**: Search left child first.

2. **Left MIN (α=-∞, β=+∞)**: Search its left child.
   - Left-left MAX evaluates leaf 3 and leaf 5.
   - Returns max(3, 5) = 5.
   - Left MIN: α stays -∞, update β = min(+∞, 5) = 5.

3. **Left MIN continues**: Search its right child.
   - Left-right MAX evaluates leaf 2 and leaf 6.
   - Returns max(2, 6) = 6.
   - But 6 ≥ β(5) → this entire branch returns 5 (or 6 in fail-soft).
   - **Beta cutoff!** The minimizer already had a 5, and this branch offers at least 6. Since minimizer wants minimum, they prefer the 5.

4. **Left MIN returns 5**. Root updates α = max(-∞, 5) = 5.

5. **Root searches right child (α=5, β=+∞)**: Right MIN (α=-5, β=+∞ via negation... actually let's trace directly).

6. **Right MIN**: Search its left child.
   - Right-left MAX evaluates leaf 1 and leaf 8.
   - Returns max(1, 8) = 8.
   - Right MIN: update β = min(+∞, 8) = 8.

7. **Right MIN continues**: About to search its right child.
   - But wait — Root's α = 5. If this right MIN returns anything ≤ 5, Root won't choose it.
   - The right MIN already found a value of 8. If the other child is worse (for Black), the min could be anything ≤ 8.
   - Actually, let's trace more carefully...

The key point is that **alpha-beta prunes branches that cannot affect the root's decision**. The exact pruning depends on the order of moves and the values encountered.

---

## Fail-Soft vs. Fail-Hard

### Fail-Hard Alpha-Beta

In fail-hard alpha-beta, the returned score is always within the $[\alpha, \beta]$ window:

```python
def negamax_ab_fail_hard(position, depth, alpha, beta):
    if depth == 0 or position.is_terminal():
        return evaluate_for_side(position)

    for move in position.generate_legal_moves():
        position.make_move(move)
        score = -negamax_ab_fail_hard(position, depth - 1, -beta, -alpha)
        position.unmake_move(move)

        if score >= beta:
            return beta    # Clamp to beta
        if score > alpha:
            alpha = score

    return alpha           # Clamp to alpha
```

### Fail-Soft Alpha-Beta

In fail-soft, the returned score may fall outside the window. This provides more information to the parent:

```python
def negamax_ab_fail_soft(position, depth, alpha, beta):
    if depth == 0 or position.is_terminal():
        return evaluate_for_side(position)

    best_score = -INFINITY   # Track actual best, not clamped

    for move in position.generate_legal_moves():
        position.make_move(move)
        score = -negamax_ab_fail_soft(position, depth - 1, -beta, -alpha)
        position.unmake_move(move)

        if score > best_score:
            best_score = score
        if score >= beta:
            break            # Cutoff, but return actual score
        if score > alpha:
            alpha = score

    return best_score        # Return actual best, may be outside [α, β]
```

### Why Fail-Soft Is Preferred

1. **Better TT integration**: When storing scores in the [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|transposition table]], fail-soft provides the actual score, which is more informative than the clamped fail-hard score.

2. **Aspiration windows**: [[03-Search-Accelerators/01 - Iterative Deepening|Aspiration window search]] relies on knowing how far outside the window a position scored, to decide whether to re-search with a wider window.

3. **More accurate bounds**: Fail-soft provides tighter bounds (e.g., "score is at least +6.2" rather than "score is at least +5.0").

---

## The Mathematical Limit

### Best Case: Perfect Move Ordering

With **perfect move ordering** (the best move is always searched first), alpha-beta prunes the maximum number of nodes. The effective branching factor drops from $B$ to $\sqrt{B}$.

**Proof sketch**: In the best case, at every max node, the first move is so good that all remaining moves are pruned at the min node below. The tree effectively becomes a series of "verification" searches at reduced depth.

The number of nodes evaluated with perfect ordering at depth $D$:

$$N_{\text{best}}(D) = B^{D/2} + B^{D/2} - 1 \approx 2 \cdot B^{D/2}$$

For $B = 35$, $D = 10$:
- **Without alpha-beta**: $35^{10} \approx 2.76 \times 10^{15}$ nodes
- **With alpha-beta (perfect ordering)**: $2 \times 35^5 \approx 1.05 \times 10^8$ nodes

That's a reduction from **quadrillions** to **hundred millions** — a speedup of over **10 million times**.

### Worst Case: Pathological Ordering

If the worst move is always searched first, alpha-beta never prunes, and the node count equals full Minimax: $B^D$.

### Typical Case: Good Ordering

With good (but not perfect) move ordering, the effective branching factor is approximately $B^{0.75}$. For $B = 35$:

- Effective branching factor: $35^{0.75} \approx 14.4$
- At depth 10: $14.4^{10} \approx 3.8 \times 10^{11}$ nodes (vs. $2.76 \times 10^{15}$ without pruning)

Still a massive improvement, but far from the theoretical best. This is why [[03-Search-Accelerators/02 - Move Ordering|move ordering]] is the **most important optimization** in a chess engine.

---

## Full C++ Implementation

```cpp
#include <limits>
#include <vector>

constexpr int INFINITY_SCORE = 100000;
constexpr int MATE_SCORE = 99999;

struct SearchInfo {
    int nodes_searched = 0;
    int beta_cutoffs = 0;
};

int negamax_ab(Position& pos, int depth, int alpha, int beta, SearchInfo& info) {
    info.nodes_searched++;

    // Terminal conditions
    if (depth <= 0) {
        return quiescence(pos, alpha, beta, info); // See Quiescence Search note
    }

    if (pos.is_draw()) return 0;

    // Check extension: search one ply deeper when in check
    bool in_check = pos.is_in_check();
    if (in_check) depth++;

    // Generate moves
    MoveList moves = pos.generate_legal_moves();

    if (moves.count == 0) {
        if (in_check) return -MATE_SCORE + pos.ply(); // Checkmate
        return 0; // Stalemate
    }

    int best_score = -INFINITY_SCORE;

    for (int i = 0; i < moves.count; i++) {
        // Move ordering would happen here (see Move Ordering note)
        pick_best_move(moves, i);

        Move move = moves.moves[i];
        pos.make_move(move);
        int score = -negamax_ab(pos, depth - 1, -beta, -alpha, info);
        pos.unmake_move(move);

        if (score > best_score) {
            best_score = score;
        }

        if (score >= beta) {
            info.beta_cutoffs++;
            return best_score; // Fail-soft beta cutoff
        }

        if (score > alpha) {
            alpha = score;
        }
    }

    return best_score;
}

// Root search function
Move search(Position& pos, int max_depth) {
    Move best_move = Move::none();
    int best_score = -INFINITY_SCORE;
    SearchInfo info;

    MoveList moves = pos.generate_legal_moves();

    for (int depth = 1; depth <= max_depth; depth++) {
        int alpha = -INFINITY_SCORE;
        int beta = INFINITY_SCORE;
        best_score = -INFINITY_SCORE;

        for (int i = 0; i < moves.count; i++) {
            pos.make_move(moves.moves[i]);
            int score = -negamax_ab(pos, depth - 1, -beta, -alpha, info);
            pos.unmake_move(moves.moves[i]);

            if (score > best_score) {
                best_score = score;
                best_move = moves.moves[i];
            }
            if (score > alpha) {
                alpha = score;
            }
        }

        // Output for UCI protocol
        std::cout << "depth " << depth
                  << " score cp " << best_score
                  << " nodes " << info.nodes_searched
                  << " pv " << best_move.to_uci() << std::endl;
    }

    return best_move;
}
```

---

## The Relationship Between Alpha-Beta and Move Ordering

Alpha-beta's effectiveness is **entirely dependent on move ordering**. This cannot be overstated.

| Move Ordering Quality | Effective Branching Factor | Depth 10 Nodes | Speedup vs. Minimax |
|-----------------------|---------------------------|----------------|---------------------|
| None (worst) | 35 | 2.76 × 10¹⁵ | 1× |
| Poor | 25 | 9.77 × 10¹³ | 28× |
| Moderate | 15 | 5.77 × 10¹¹ | 4,785× |
| Good | 10 | 10¹⁰ | 276,000× |
| Perfect (best) | √35 ≈ 5.9 | 5.1 × 10⁷ | 54,000,000× |

The move ordering hierarchy (from [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]]):

1. **TT Move** — the best move from a previous search of this position
2. **Captures (MVV-LVA)** — winning captures first
3. **Killer Moves** — quiet moves that caused cutoffs at this ply
4. **History Heuristic** — moves that caused cutoffs globally

Each level of move ordering improvement translates directly into deeper search within the same time budget.

---

## Connection to Explainability

Alpha-beta pruning is not just a performance optimization — it provides a **natural framework for explaining why certain moves were not chosen**.

### Explainable Cutoffs

When a beta cutoff occurs, the explanation system can record:

```
Branch pruned: After examining Nc3 (score: +3.50), the move Nf3
(score: +2.80) was not fully explored because:
  - Nc3 already guarantees a score of +3.50
  - Nf3's subtree cannot produce a score above +2.80
  - Therefore, Nf3 cannot beat the current best option
```

This is an **explanation by elimination**: "We didn't choose this move because we already had a better option, and this move's subtree couldn't catch up."

### The Principal Variation

The sequence of moves from the root to the leaf that produces the final score is called the **Principal Variation (PV)**. This is the engine's "story" — the line of play it considers optimal for both sides. The PV is the backbone of the explanation:

```
Principal Variation: 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6

The engine's reasoning:
  1. e4 — Best opening move, controlling the center
     Black responds: 1...e5 — Symmetrically contesting the center
  2. Nf3 — Developing and attacking e5
     Black responds: 2...Nc6 — Defending the e5 pawn
  3. Bb5 — Pinning the knight and preparing castling
     Black responds: 3...a6 — Challenging the bishop
```

The PV is the engine's **narrative** — the sequence of "best play for both sides" that leads to the evaluated position. See [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] for more.

---

## Key Takeaways

- **Alpha-Beta Pruning** eliminates branches that cannot affect the final decision, guaranteeing the same result as Minimax with far fewer node evaluations.
- **Alpha** = the best score the maximizer can guarantee; **Beta** = the best score the minimizer can guarantee. When $\alpha \geq \beta$, prune.
- **Beta cutoffs** occur when we find a move so good that the opponent would never allow it.
- **Fail-soft** returns the actual score (may be outside the window); **fail-hard** clamps to the window. Fail-soft is preferred for TT integration.
- With **perfect move ordering**, the branching factor drops from $B$ to $\sqrt{B}$, enabling dramatically deeper search.
- **Move ordering is the most important optimization** — it directly determines alpha-beta's pruning effectiveness.
- For explainability, alpha-beta provides **explainable cutoffs** and the **Principal Variation** as the engine's "reasoning story."

## Cross-References

- [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax Algorithm]] — the unpruned foundation
- [[02-Search-Algorithms/02 - Negamax Formulation|Negamax Formulation]] — the framework alpha-beta is built on
- [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — further optimization using narrow windows
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — the critical optimization for alpha-beta efficiency
- [[03-Search-Accelerators/05 - Quiescence Search|Quiescence Search]] — the search that continues when alpha-beta reaches depth 0
- [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|Transposition Table Architecture]] — how TT bounds interact with alpha-beta
