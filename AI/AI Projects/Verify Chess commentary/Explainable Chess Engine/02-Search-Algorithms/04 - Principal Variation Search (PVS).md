---
tags:
  - search
  - PVS
  - principal-variation
  - null-window
  - optimization
chapter: "02"
---

# Principal Variation Search (PVS)

## Overview

**Principal Variation Search (PVS)**, also known as **NegaScout**, is an optimization of [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta pruning]] that exploits the observation that the **first move** in a well-ordered position is usually the best. Instead of searching every non-first move with a full alpha-beta window, PVS uses a **null-window search** ($\alpha = \beta - 1$) for non-PV moves. If the null-window search fails high, only then is a re-search performed with the full window. In practice, the null-window search confirms that non-PV moves are inferior, and re-searches are rare — saving enormous computation time.

---

## The Assumption Behind PVS

### Move Ordering Is Good

After [[03-Search-Accelerators/02 - Move Ordering|move ordering]], the first move at each node is very likely the best. This move becomes part of the **Principal Variation (PV)** — the engine's current best line of play.

If the first move is indeed the best, then all subsequent moves should score **below** the PV move. We can verify this cheaply using a null-window search: a search with the window $[\alpha, \alpha+1]$ (i.e., $\beta = \alpha + 1$).

### What a Null-Window Search Tells Us

A null-window search $[\alpha, \alpha+1]$ can only return two results:
- **Fail-low** (score ≤ $\alpha$): The move is not better than $\alpha$. Since $\alpha$ is already our best score, this move is inferior. No re-search needed.
- **Fail-high** (score > $\alpha$): The move might be better than our current best. We must re-search with the full window to determine its exact score.

In a well-ordered position, **most non-PV moves fail low**, so the cheap null-window search is sufficient. The expensive full-window re-search is the exception, not the rule.

---

## The PVS Algorithm

### Core Logic

```python
def pvs(position, depth, alpha, beta):
    if depth == 0:
        return quiescence(position, alpha, beta)

    best_score = -INFINITY
    is_first_move = True

    for move in position.generate_legal_moves():
        position.make_move(move)

        if is_first_move:
            # First move: search with full window
            score = -pvs(position, depth - 1, -beta, -alpha)
        else:
            # Non-PV move: search with null window first
            score = -pvs(position, depth - 1, -alpha - 1, -alpha)

            # If null-window fails high, re-search with full window
            if score > alpha and score < beta:
                score = -pvs(position, depth - 1, -beta, -alpha)

        position.unmake_move(move)

        if score > best_score:
            best_score = score
        if score >= beta:
            return best_score  # Beta cutoff
        if score > alpha:
            alpha = score

        is_first_move = False

    return best_score
```

### Step-by-Step Explanation

1. **First move (PV move)**: Search normally with the full $[\alpha, \beta]$ window. This is the "expensive" search that establishes the baseline.

2. **Subsequent moves**: Search with the null window $[\alpha, \alpha+1]$. This is extremely fast because the narrow window causes massive pruning.

3. **If the null-window search fails high** (score > $\alpha$): The move might beat the PV move. Re-search with the full $[\alpha, \beta]$ window to get the exact score.

4. **If the null-window search fails low** (score ≤ $\alpha$): The move is confirmed inferior. No re-search needed. This is the common case.

### Why the Re-Search Condition Is `score > alpha AND score < beta`

- If `score > alpha`: The null-window search failed high — the move might be better than $\alpha$.
- If `score >= beta`: A beta cutoff occurred — the move is so good that the opponent wouldn't allow this line. No need for a re-search; we can return immediately.
- If `score <= alpha`: The move is inferior. No re-search.

The re-search is needed only when the score falls strictly between $\alpha$ and $\beta$ — the move might improve our position but we need to know its exact value.

---

## How PVS Saves Time

### Full Alpha-Beta (without PVS)

At each node with $N$ moves, every move is searched with the full $[\alpha, \beta]$ window. Even after alpha is tightened by the first move, subsequent moves still search with a wide window until a cutoff occurs.

### PVS

At each node:
- **1 move** (PV move) is searched with the full window
- **$N-1$ moves** are searched with the null window (very fast, heavy pruning)
- **Typically 0-2 moves** require re-search (when the null-window fails high)

The time savings come from the fact that null-window searches are **much faster** than full-window searches. The narrow window causes aggressive pruning at every level below:

| Window Type | Effective Pruning | Nodes Examined |
|-------------|-------------------|----------------|
| Full [α, β] | Moderate | Many |
| Null [α, α+1] | Very aggressive | Few |

In practice, PVS typically saves **20-40%** of total search time compared to plain alpha-beta with the same move ordering.

---

## C++ Implementation

```cpp
int pvs(Position& pos, int depth, int alpha, int beta, SearchInfo& info) {
    info.nodes_searched++;

    if (depth <= 0) {
        return quiescence(pos, alpha, beta, info);
    }

    if (pos.is_draw()) return 0;

    bool in_check = pos.is_in_check();
    if (in_check) depth++; // Check extension

    MoveList moves = pos.generate_legal_moves();
    if (moves.count == 0) {
        return in_check ? -MATE_SCORE + pos.ply() : 0;
    }

    // Move ordering (critical for PVS effectiveness)
    order_moves(pos, moves, info);

    int best_score = -INFINITY_SCORE;

    for (int i = 0; i < moves.count; i++) {
        pos.make_move(moves[i]);

        int score;
        if (i == 0) {
            // PV move: full window search
            score = -pvs(pos, depth - 1, -beta, -alpha, info);
        } else {
            // Non-PV move: null-window search
            score = -pvs(pos, depth - 1, -alpha - 1, -alpha, info);

            // Re-search if null-window fails high and is within bounds
            if (score > alpha && score < beta) {
                score = -pvs(pos, depth - 1, -beta, -alpha, info);
            }
        }

        pos.unmake_move(moves[i]);

        if (score > best_score) {
            best_score = score;
        }

        if (score >= beta) {
            // Beta cutoff
            if (!moves[i].is_capture()) {
                info.killer_moves[pos.ply()] = moves[i];
                info.history[moves[i].from()][moves[i].to()] += depth * depth;
            }
            return best_score;
        }

        if (score > alpha) {
            alpha = score;
        }
    }

    return best_score;
}
```

### Integration with Iterative Deepening

PVS works best when combined with [[03-Search-Accelerators/01 - Iterative Deepening|iterative deepening]], because the PV from the previous depth provides an excellent first move:

```cpp
Move iterative_deepening_pvs(Position& pos, int max_depth) {
    Move best_move = Move::none();
    SearchInfo info;

    for (int depth = 1; depth <= max_depth; depth++) {
        int score = pvs(pos, depth, -INFINITY_SCORE, INFINITY_SCORE, info);

        // The PV from this depth becomes the move ordering hint
        // for the next depth's search
        best_move = info.pv_table[0][0];

        std::cout << "depth " << depth
                  << " score " << score
                  << " nodes " << info.nodes_searched
                  << " pv " << get_pv_string(info) << std::endl;
    }

    return best_move;
}
```

---

## The PV Table: Storing the Principal Variation

The PV is stored in a triangular table:

```cpp
struct PVTable {
    Move pv[MAX_DEPTH][MAX_DEPTH];
    int pv_length[MAX_DEPTH];
};

void update_pv(PVTable& table, int ply, Move move) {
    table.pv[ply][0] = move;
    for (int i = 0; i < table.pv_length[ply + 1]; i++) {
        table.pv[ply][i + 1] = table.pv[ply + 1][i];
    }
    table.pv_length[ply] = table.pv_length[ply + 1] + 1;
}
```

When a new best move is found at ply $p$, we copy the PV from ply $p+1$ into the PV at ply $p$, prepending the new move. This builds the PV from the bottom up.

---

## PVS vs. NegaScout

PVS and NegaScout are often used interchangeably, but there is a subtle difference:

- **PVS**: The null-window search always uses $[\alpha, \alpha+1]$, and the re-search uses $[\alpha, \beta]$.
- **NegaScout**: The null-window search uses $[\alpha, \text{score} + 1]$ where `score` is the score of the previous move, creating a "scouting" window that is more adaptive.

In practice, modern implementations use PVS (the simpler version) because the difference in performance is negligible, and PVS is easier to implement correctly.

---

## PVS with Aspiration Windows

PVS combines naturally with **aspiration windows** — narrow search windows around the expected score:

```cpp
Move search_with_aspiration(Position& pos, int max_depth) {
    int prev_score = 0;
    int window_size = 50; // 50 centipawns

    for (int depth = 1; depth <= max_depth; depth++) {
        int alpha = prev_score - window_size;
        int beta  = prev_score + window_size;

        int score = pvs(pos, depth, alpha, beta, info);

        // If score falls outside aspiration window, re-search with full window
        if (score <= alpha || score >= beta) {
            score = pvs(pos, depth, -INFINITY_SCORE, INFINITY_SCORE, info);
        } else {
            prev_score = score;
        }

        // Gradually widen window for stability
        window_size += 10;
    }

    return info.pv_table[0][0];
}
```

Aspiration windows benefit PVS because the narrow initial window makes the null-window searches even more effective — the "expected" range of scores is already narrow.

---

## Why PVS Matters for Explainability

### The PV as the Engine's "Story"

The **Principal Variation** is the most important output for the explanation system. It represents the engine's prediction of optimal play for both sides — the **narrative** of the position:

```
Position: r1bqkb1r/pppppppp/2n2n2/8/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3

PV: 3. d4 cxd4 4. Nxd4 e5 5. Nf3

Engine's reasoning chain:
  Move 1 (d4): White strikes at the center, opening lines
    Black responds (cxd4): Accepting the pawn exchange
  Move 2 (Nxd4): Recapturing with the knight, centralizing it
    Black responds (e5): Challenging the knight with a pawn push
  Move 3 (Nf3): Retreating the knight to maintain flexibility
```

Each move in the PV can be individually explained using the principles from [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]]. The PV provides the **temporal structure** of the explanation: not just "why this move now" but "how this move fits into a plan."

### Explainable Re-Searches

When PVS performs a re-search (the null-window failed high), this is an **interesting event** for the explanation system:

```
Note: The move Bc4 initially appeared inferior to Nc3,
but upon deeper investigation, Bc4 actually scored +0.45
compared to Nc3's +0.38. The re-search revealed that
Bc4's bishop placement creates stronger pressure on f7.
```

Re-searches indicate moves where the engine's initial "intuition" (move ordering) was wrong. These are often the most instructive positions for human learning.

### Cut-Moves as "Disproof"

When the null-window search confirms a move is inferior (fail-low), the explanation can note:

```
Alternative move Be2 was considered but rejected:
  Be2 scores below +0.38 because it does not pressure
  the center or create immediate threats. The bishop is
  passively placed and will need to be repositioned later.
```

---

## Key Takeaways

- **PVS** exploits the assumption that the first move (from TT/iterative deepening) is usually best, using a **null-window search** for non-PV moves.
- The null-window $[\alpha, \alpha+1]$ is extremely fast because it causes aggressive pruning at all lower levels.
- **Re-search** with the full window occurs only when the null-window fails high — this is rare with good move ordering.
- PVS saves **20-40%** of search time compared to plain alpha-beta.
- **The PV is the engine's "story"** — the sequence of optimal moves for both sides that provides the backbone of the explanation.
- **Re-searches are interesting** — they indicate positions where the engine's initial intuition was wrong, which are often the most instructive for human learning.

## Cross-References

- [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax Algorithm]] — the foundation
- [[02-Search-Algorithms/02 - Negamax Formulation|Negamax Formulation]] — the framework
- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the pruning that PVS optimizes
- [[03-Search-Accelerators/01 - Iterative Deepening|Iterative Deepening]] — provides the PV move for PVS
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — critical for PVS effectiveness
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — how the PV drives explanations
