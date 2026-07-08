---
tags:
  - search
  - LMR
  - late-move-reductions
  - move-ordering-dependent
  - heuristic
chapter: "03"
---

# Late Move Reductions (LMR)

## Overview

**Late Move Reductions (LMR)** is a heuristic that reduces the search depth for moves that are statistically unlikely to be the best move. After [[03-Search-Accelerators/02 - Move Ordering|move ordering]] places the strongest candidates first, the remaining "late" moves are searched at a reduced depth. If a reduced search unexpectedly scores above alpha, a re-search at full depth is performed as a safety valve. LMR is one of the most powerful pruning techniques in modern chess engines, responsible for enabling searches 4-8 plies deeper than would otherwise be possible.

---

## The Statistical Insight

### Why Late Moves Are Rarely Best

After good move ordering, the first move at each node is the best move in **85-95%** of positions. The probability that the $k$-th move in the ordering is the best decreases rapidly:

| Move Index | Probability of Being Best |
|------------|--------------------------|
| 1st (TT/PV) | ~90% |
| 2nd | ~5% |
| 3rd | ~2% |
| 4th+ | <1% each |

This means that spending the same amount of computation on the 10th move as on the 1st move is **wasteful**. The 1st move deserves a deep, thorough search; the 10th move deserves a quick check.

### The LMR Strategy

Instead of searching every move to the full depth $D$:

1. **First few moves** (PV move, captures, killers): Search at full depth $D$
2. **Later moves**: Search at reduced depth $D - R$, where $R$ is the reduction amount
3. **Safety valve**: If the reduced search returns a score above alpha, re-search at full depth $D$

The reduction $R$ is typically 1-3 plies for moderate depths and can be larger at high depths.

---

## The Reduction Formula

### Basic Formula

The standard LMR reduction formula is:

$$R = 1 + \lfloor \ln(D) \times \ln(M) \rfloor$$

Where:
- $D$ = remaining depth
- $M$ = move index (1-based, after the PV move and captures)
- $\ln$ = natural logarithm

This formula gives larger reductions for:
- **Higher depths** (more room to reduce)
- **Later move indices** (lower probability of being best)

### Reduction Table Examples

| Depth $D$ | Move Index $M$ | $\ln(D)$ | $\ln(M)$ | $R = 1 + \lfloor \ln(D) \times \ln(M) \rfloor$ |
|-----------|---------------|----------|----------|-----|
| 4 | 1 | 1.39 | 0 | 1 |
| 4 | 3 | 1.39 | 1.10 | 2 |
| 4 | 6 | 1.39 | 1.79 | 3 |
| 8 | 1 | 2.08 | 0 | 1 |
| 8 | 3 | 2.08 | 1.10 | 3 |
| 8 | 6 | 2.08 | 1.79 | 4 |
| 8 | 15 | 2.08 | 2.71 | 6 |
| 16 | 1 | 2.77 | 0 | 1 |
| 16 | 3 | 2.77 | 1.10 | 4 |
| 16 | 6 | 2.77 | 1.79 | 5 |
| 16 | 15 | 2.77 | 2.71 | 8 |

### Reduction Adjustments

The basic formula is adjusted based on position characteristics:

**Increase reduction (reduce more aggressively) when:**
- The move is not a capture
- The move is not a check
- The move does not give check
- The position is not in check (when in check, all moves must be examined fully)
- The move has a low history score
- The move is not a killer move

**Decrease reduction (search more carefully) when:**
- The move is a capture (even late captures can be critical)
- The move gives check (tactical threat)
- The position is in check (no reduction when in check)
- The move has a high history score
- The move is a pawn push to the 7th rank (potential queening)
- The move improves the evaluation significantly

```cpp
int get_reduction(int depth, int move_index, bool is_capture, bool gives_check,
                  bool in_check, int history_score) {
    if (depth < 3 || move_index <= 2) return 0;  // No reduction for shallow depths or early moves

    int R = lmr_table[depth][move_index];  // Precomputed ln(depth) * ln(move_index)

    // Adjustments
    if (is_capture)   R -= 1;
    if (gives_check)  R -= 1;
    if (in_check)     R = 0;      // Never reduce when in check
    if (history_score > 400) R -= 1;
    if (history_score < 100) R += 1;

    // Ensure minimum reduction of 1 and maximum of depth - 1
    R = std::max(1, std::min(R, depth - 1));

    return R;
}
```

---

## C++ Lookup Table Implementation

### Precomputed LMR Table

Rather than computing logarithms at runtime, we precompute the reduction table:

```cpp
constexpr int MAX_DEPTH = 64;
constexpr int MAX_MOVES = 256;

int lmr_table[MAX_DEPTH][MAX_MOVES];

void init_lmr_table() {
    for (int depth = 1; depth < MAX_DEPTH; depth++) {
        for (int move_index = 1; move_index < MAX_MOVES; move_index++) {
            // R = 1 + ln(depth) * ln(move_index)
            double r = 1.0 + std::log(depth) * std::log(move_index) / 2.0;
            lmr_table[depth][move_index] = std::max(1, (int)std::round(r));
        }
    }
}
```

Note: Many engines use `log(depth) * log(move_index) / 2.0` (dividing by 2) for a more conservative reduction. The exact tuning is engine-specific and determined through self-play testing.

### LMR in the Search Loop

```cpp
int search(Position& pos, int depth, int alpha, int beta, SearchInfo& info) {
    // ... terminal checks, TT lookup ...

    MoveList moves = pos.generate_legal_moves();
    order_moves(pos, moves, info);

    int best_score = -INFINITY_SCORE;
    bool is_first_move = true;

    for (int i = 0; i < moves.count; i++) {
        Move move = moves[i];
        pos.make_move(move);

        int score;

        if (is_first_move) {
            // PV move: full depth, full window
            score = -search(pos, depth - 1, -beta, -alpha, info);
        } else {
            // Determine reduction
            int reduction = 0;
            if (i >= 3 && depth >= 3 && !move.is_capture() && !pos.is_in_check()) {
                reduction = lmr_table[depth][i];
                // Adjust for position-specific factors
                if (move.gives_check()) reduction--;
                if (info.history[move.from()][move.to()] > 400) reduction--;
                reduction = std::max(1, std::min(reduction, depth - 2));
            }

            // Search with reduction
            score = -search(pos, depth - 1 - reduction, -alpha - 1, -alpha, info);

            // Re-search if reduced search fails high
            if (score > alpha && reduction > 0) {
                score = -search(pos, depth - 1, -alpha - 1, -alpha, info);
            }

            // Re-search with full window if null-window fails high
            if (score > alpha && score < beta) {
                score = -search(pos, depth - 1, -beta, -alpha, info);
            }
        }

        pos.unmake_move(move);

        if (score > best_score) best_score = score;
        if (score >= beta) {
            // Beta cutoff
            update_killer_moves(info, pos.ply(), move);
            update_history(info, move, depth);
            return best_score;
        }
        if (score > alpha) alpha = score;

        is_first_move = false;
    }

    return best_score;
}
```

### The Three-Phase Search for Non-PV Moves

Notice the three phases for non-PV moves in the code above:

1. **Reduced null-window search**: `search(depth - 1 - R, -alpha-1, -alpha)` — the cheapest possible search
2. **Full-depth null-window search**: `search(depth - 1, -alpha-1, -alpha)` — if the reduced search failed high
3. **Full-depth full-window search**: `search(depth - 1, -beta, -alpha)` — if the null-window search failed high

Each phase is more expensive but necessary only when the previous phase suggests the move might be good. This combines LMR with [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]].

---

## Why LMR Is Safe ONLY When Move Ordering Is Strong

### The Risk

LMR is a **heuristic**, not a guarantee. If the move ordering is poor and the best move is consistently pushed to late positions, LMR will reduce the search depth for the best move, potentially missing it. The safety valve (re-search when the reduced score is above alpha) mitigates this, but it's not perfect — the reduced search might not score above alpha even if the full-depth search would.

### When LMR Can Miss the Best Move

1. **Quiet positional moves** that are best but not captures, killers, or historically good
2. **Sacrifices** where the compensation is deep (beyond the reduced depth)
3. **Non-obvious defensive moves** that prevent a subtle threat

### Safety Conditions

LMR should NOT be applied when:
- **In check**: Every legal move must be examined fully — the cost of missing a defensive move is catastrophic
- **At shallow depths**: The reduction formula returns 0 for depth < 3, so no reduction occurs
- **For the PV move**: The first move is always searched at full depth
- **For captures that are winning (SEE ≥ 0)**: Tactical precision matters
- **For moves that give check**: Checks are forcing and often the key to the position

---

## LMR and Elo Impact

LMR is one of the highest-impact optimizations in modern chess engines. Estimated impact:

| Configuration | Effective Depth (30s/move) | Estimated Elo |
|---------------|---------------------------|--------------|
| No LMR, no PVS | ~10-12 ply | ~2500 |
| PVS only | ~13-15 ply | ~2700 |
| PVS + LMR (basic) | ~18-22 ply | ~3000 |
| PVS + tuned LMR | ~25-30 ply | ~3300+ |

The ~8-10 ply increase from LMR translates to roughly **600-800 Elo points** — an enormous improvement. This is why virtually every competitive engine uses LMR.

---

## Connection to Explainability

### "These Moves Were Considered but Deemed Low-Priority"

LMR provides the explanation system with a natural way to explain why certain moves were not fully explored:

```
Moves considered at this position:
  1. Nf3 (full depth search, score: +0.45) — PV move, searched deeply
  2. d4 (full depth search, score: +0.38) — strong capture
  3. Bc4 (reduced search, score: +0.20) — briefly examined, not competitive
  4. Be2 (reduced search, score: -0.10) — briefly examined, worse than alpha
  5-35. (reduced or skipped) — low probability of being best
```

The explanation can note: "Moves 5-35 were considered but given reduced search depth because statistical analysis indicates they are unlikely to improve on the current best move (Nf3 at +0.45). If you believe a specific alternative might be strong, the engine can perform a full-depth analysis of that move."

### Re-Search Events as "Discovery Moments"

When a reduced search fails high and triggers a re-search, this is a **discovery moment** — the engine found an unexpected strong move:

```
DISCOVERY: The move h3 appeared weak at reduced depth (-0.05)
but a full-depth search revealed it scores +0.52!

Reason: h3 prevents Bg4, which would have pinned the knight
after ...Bg4 Nbd2 Bxf3 Qxf3, weakening the kingside.
This defensive idea was only visible at full depth.
```

These discovery moments are extremely valuable for the explanation system — they indicate positions where the engine's statistical model (move ordering) underestimated a move, and deeper analysis revealed hidden value.

### LMR Reduction as a Confidence Measure

The amount of reduction applied to a move can serve as a **confidence measure** for the explanation system:

- **R = 0 (no reduction)**: High confidence that this move deserves full analysis (PV move, capture, check)
- **R = 1-2**: Moderate confidence — the move is worth checking but not expected to be best
- **R = 3+**: Low confidence — the move is statistically very unlikely to be best

The explanation system can use this to prioritize which alternative moves to discuss in detail.

---

## Key Takeaways

- **LMR** reduces the search depth for late moves in the ordering, exploiting the statistical insight that they are rarely the best move.
- The **reduction formula** $R = 1 + \lfloor \ln(D) \times \ln(M) \rfloor$ gives larger reductions for higher depths and later move indices.
- A **safety valve** (re-search at full depth) ensures that moves that score above alpha in the reduced search are not missed.
- LMR is **safe only when move ordering is strong** — poor ordering can cause the best move to be reduced and missed.
- LMR is one of the **highest-impact optimizations**, enabling 8-10 additional plies of search and ~600-800 Elo improvement.
- For explainability, LMR tells the explanation system **which moves were considered but deemed low-priority**, and **re-search events** indicate discovery moments where statistical models underestimated a move.

## Cross-References

- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — the critical prerequisite for LMR safety
- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the framework within which LMR operates
- [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — LMR combines naturally with PVS's null-window searches
- [[03-Search-Accelerators/04 - Null Move Pruning (NMP)|Null Move Pruning]] — another depth-reduction heuristic
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — how LMR supports explanation through confidence measures
