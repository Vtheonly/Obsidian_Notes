---
tags:
  - search
  - quiescence
  - horizon-effect
  - captures
  - tactical-stability
chapter: "03"
---

# Quiescence Search

## Overview

**Quiescence Search** (also called "quiet search" or "qsearch") is the search that continues after the main [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta]] search reaches depth 0. Its purpose is to resolve **unstable positions** — positions where captures, promotions, or checks are still pending — before returning a static evaluation. Without quiescence search, the engine suffers from the **Horizon Effect**, where it evaluates positions mid-exchange and produces wildly inaccurate assessments. Quiescence search ensures that explanations are not based on "hallucinated" material advantages.

---

## The Horizon Effect Problem

### The Core Issue

When the main search reaches depth 0, it stops and returns the static evaluation. But what if the position is **not quiet** — what if a queen is about to be captured, or a series of exchanges is in progress?

**Example**:

```
Position: White queen on e4, Black rook on e8 (capturing)
Main search depth: 0

Static evaluation: +5.00 (White has a queen vs. a rook)
Actual value: +1.00 (After Re8xe4, White has lost the queen)

The static evaluation is WRONG because it doesn't account for
the imminent capture.
```

This is the **Horizon Effect**: the engine's "horizon" (search depth) ends in the middle of a tactical sequence, and the static evaluation doesn't see the continuation. The engine thinks it's winning because it can't see the capture that's about to happen.

### Why the Horizon Effect Matters for Explainability

If the engine returns +5.00 for a position where the queen is about to be captured, the explanation system would say: "Your position is excellent — you have a queen advantage." This is **hallucinated** — the queen is not actually safe. The explanation would be based on a false evaluation.

Quiescence search prevents this by continuing the search beyond depth 0 for as long as there are **forcing moves** (captures, promotions, and sometimes checks) available.

---

## How Quiescence Search Works

### The Algorithm

1. At depth 0, compute the **stand-pat score** (the static evaluation, from the side-to-move's perspective)
2. If the stand-pat score is ≥ beta, return beta (beta cutoff — position is already good enough)
3. If the stand-pat score > alpha, update alpha
4. Generate **capture moves** (and sometimes promotions and checks)
5. For each capture:
   a. Make the move
   b. Recursively call quiescence search
   c. Unmake the move
   d. If the score ≥ beta, return (cutoff)
   e. If the score > alpha, update alpha
6. Return alpha

### Stand-Pat Score

The **stand-pat score** is the evaluation of the position if the side to move chooses **not to make any capture**. It serves as the baseline: if the side to move cannot improve their position by capturing, they can always choose to "stand pat" (do nothing in the quiescence phase).

This is fundamentally different from the main search, where the side to move MUST make a move. In quiescence, the side to move has the **option** to not capture. This prevents the qsearch from forcing a sequence of bad captures.

### Pseudocode

```python
def quiescence(position, alpha, beta):
    # Stand-pat: the score if we choose not to capture
    stand_pat = evaluate_for_side(position)

    if stand_pat >= beta:
        return beta  # Position is already good enough

    if stand_pat > alpha:
        alpha = stand_pat  # New baseline

    # Generate captures only
    for move in position.generate_captures():
        # Delta pruning: skip obviously bad captures
        if stand_pat + piece_value(victim) + 200 < alpha:
            continue  # Even capturing this piece can't raise alpha

        position.make_move(move)
        score = -quiescence(position, -beta, -alpha)
        position.unmake_move(move)

        if score >= beta:
            return beta  # Beta cutoff

        if score > alpha:
            alpha = score

    return alpha
```

---

## Detailed Implementation

### C++ Implementation

```cpp
int quiescence(Position& pos, int alpha, int beta, SearchInfo& info) {
    info.nodes_searched++;

    // Stand-pat evaluation
    int stand_pat = evaluate_for_side(pos);

    // Beta cutoff: position is already too good for the opponent
    if (stand_pat >= beta) {
        return beta;
    }

    // Delta pruning threshold
    const int DELTA = 200; // Margin for error

    // Big delta: the maximum possible gain from a single capture (queen + 200)
    const int BIG_DELTA = 900 + DELTA;

    // Alpha update
    if (stand_pat > alpha) {
        alpha = stand_pat;
    }

    // Generate capture moves, ordered by MVV-LVA
    MoveList captures = pos.generate_captures();
    order_captures_mvv_lva(pos, captures);

    for (int i = 0; i < captures.count; i++) {
        Move move = captures[i];

        // Delta pruning: if this capture can't possibly raise alpha, skip it
        int capture_gain = piece_value[type_of(pos.piece_on(move.to()))];
        if (stand_pat + capture_gain + DELTA < alpha && !move.is_promotion()) {
            continue;
        }

        // SEE pruning: skip captures that are clearly losing
        if (see(pos, move) < -50) {
            continue;
        }

        pos.make_move(move);
        int score = -quiescence(pos, -beta, -alpha, info);
        pos.unmake_move(move);

        if (score >= beta) {
            return beta;
        }

        if (score > alpha) {
            alpha = score;
        }
    }

    return alpha;
}
```

### MVV-LVA Ordering in Quiescence

Captures within quiescence search are ordered by the same [[03-Search-Accelerators/02 - Move Ordering|MVV-LVA]] heuristic used in the main search. This ensures the most promising captures are tried first, maximizing the chance of early cutoffs:

```cpp
void order_captures_mvv_lva(const Position& pos, MoveList& captures) {
    int scores[256];

    for (int i = 0; i < captures.count; i++) {
        Piece victim = pos.piece_on(captures[i].to());
        Piece attacker = pos.piece_on(captures[i].from());
        scores[i] = piece_value[type_of(victim)] * 10 - piece_value[type_of(attacker)];
    }

    // Sort descending by score (simple insertion sort for small lists)
    for (int i = 1; i < captures.count; i++) {
        int j = i;
        while (j > 0 && scores[j] > scores[j - 1]) {
            std::swap(captures[j], captures[j - 1]);
            std::swap(scores[j], scores[j - 1]);
            j--;
        }
    }
}
```

---

## Pruning Optimizations in Quiescence

### Delta Pruning

**Delta pruning** skips captures that cannot possibly raise the score above alpha. The idea: if the stand-pat score plus the value of the captured piece plus a safety margin is still below alpha, there's no point in trying this capture.

$$\text{Skip if: } \text{stand\_pat} + \text{Value}(\text{captured}) + \Delta < \alpha$$

Where $\Delta$ is a safety margin (typically 200 centipawns) to account for the possibility that the capture enables further gains (e.g., a fork after the capture).

**Why 200 centipawns?**: A capture might not just gain the captured piece's value — it might also lead to a fork, pin, or discovered attack. The 200 centipawn margin accounts for these secondary gains.

### SEE Pruning in Quiescence

**Static Exchange Evaluation (SEE)** can prune captures that are clearly losing. If capturing a defended piece results in a net material loss, the capture is skipped:

```cpp
if (see(pos, move) < -50) {
    continue; // Skip losing captures
}
```

The threshold of -50 centipawns allows marginally losing captures (e.g., a bishop for two pawns) to still be searched, while pruning clearly losing exchanges.

### Move Generation Optimization

In quiescence, we only generate **captures and promotions**. This is a much smaller set of moves than the full legal move list:

- Typical position: 30-40 legal moves, but only 3-8 captures
- Endgame: 5-10 legal moves, 1-3 captures

The smaller move list makes qsearch much faster than the main search.

---

## Quiescence Search Depth

### Does Quiescence Search Have a Depth Limit?

In theory, quiescence search continues until the position is **quiet** (no captures available). In practice, most engines impose a maximum qsearch depth to prevent pathological cases:

```cpp
constexpr int MAX_QS_DEPTH = 64; // Very deep but not infinite

int quiescence(Position& pos, int alpha, int beta, int qs_depth, SearchInfo& info) {
    if (qs_depth >= MAX_QS_DEPTH) {
        return evaluate_for_side(pos);
    }

    // ... normal quiescence logic ...
}
```

In practice, qsearch rarely exceeds depth 10-15, because capture sequences naturally terminate — pieces are exchanged and the board empties.

### Check Extensions in Quiescence

Some engines extend quiescence search when in check — generating all legal moves (not just captures) to ensure the position is fully resolved:

```cpp
if (pos.is_in_check()) {
    // Generate ALL legal moves (not just captures) when in check
    MoveList moves = pos.generate_legal_moves();
    // ... search all moves ...
} else {
    // Generate captures only
    MoveList captures = pos.generate_captures();
    // ... search captures only ...
}
```

This is more expensive but prevents the engine from returning an evaluation while one side is in check with no resolution. Checks in qsearch are sometimes called "check extensions" even though they're not extending the main search depth.

---

## The Horizon Effect: A Concrete Example

### Without Quiescence Search

```
Position: White: Ke1, Qd1, Re1. Black: Ke8, Nc6, Pa7.
It's White's turn. Search depth: 4.

Depth 4: White plays Qd5 (threatens Qxc6)
Depth 3: Black plays Nb4 (knight moves away from threat)
Depth 2: White plays Qd8# (checkmate!)

Wait — what if Black plays Nc6xBd5 instead?
Depth 3: Black plays Nxd5 (captures the queen!)
Depth 2: White plays Rxe8# (checkmate? No — the knight moved from c6)

Actually, let's use a simpler example:

Position: White: Kf1, Qe2. Black: Kg8, Re8.
Search depth: 3.

Depth 3: White plays Qe7 (attacking the rook)
Depth 2: Black plays Re8-e7?? No — Rxe7 wins the queen? No...
```

Let me use the simplest possible example:

```
Position: White queen on d1, Black rook on d8.
Search depth: 0 (at the leaf).

Without qsearch: eval = +5.00 (queen advantage)
  → Engine thinks White is winning

With qsearch: 
  Capture Qxd8: White captures the rook
  But wait, after Qxd8, can Black recapture? No rook left.
  Score after Qxd8: +9.00 (queen captured rook, material: Q vs nothing)
  
Hmm, that's not right either. Let me reverse it:

Position: Black rook on d8 attacks White queen on d4.
Search depth: 0 (at the leaf).

Without qsearch: eval = +5.00 (queen advantage, but queen is about to be captured!)
  → HORRIBLY WRONG

With qsearch:
  Stand-pat: +5.00
  White can't improve by capturing — the queen is under attack
  Black's capture Rxd4: score from Black's view = +5.00 - 9.00 + 5.00 = +1.00 (rook advantage)
  Wait, let me just compute directly:
  After Rxd4, White has no queen, Black has a rook on d4.
  Material: White has nothing, Black has a rook → eval from White's view = -5.00
  But White gets to recapture... if there's nothing to recapture with, 
  the qsearch correctly returns -5.00 instead of the hallucinated +5.00.
```

The key insight: **without quiescence search, the engine returns the static evaluation (+5.00) which is completely wrong because the queen is about to be captured. With quiescence search, the engine sees the capture and returns the correct evaluation (-5.00 or whatever the true value is after the exchange is resolved).**

---

## Quiescence Search Statistics

In a typical search:
- The main search accounts for **~60-70%** of nodes
- Quiescence search accounts for **~30-40%** of nodes
- Qsearch is called at every leaf of the main search tree
- The average qsearch depth is **3-5 plies** (capture sequences are short)

Despite accounting for 30-40% of nodes, qsearch is essential — without it, the engine would be **hundreds of Elo weaker** due to systematic evaluation errors.

---

## Connection to Explainability

### Preventing Hallucinated Explanations

The primary role of quiescence search in the explanation system is to ensure that **explanations are not based on false evaluations**. Without qsearch:

```
 WITHOUT QUIESCENCE:
"Your position is excellent! You have a queen advantage (+5.00)."
Reality: The queen is about to be captured. The explanation is a hallucination.
```

```
 WITH QUIESCENCE:
"Your position is difficult (-1.00). While you have a queen, 
it's under attack from the rook on d8, and after the exchange, 
you'll be down material."
```

### Explaining Exchange Sequences

Quiescence search naturally produces exchange sequences that the explanation system can present:

```
Exchange analysis for position:
  1. ...Rxd4 (Black captures queen, gaining +900 centipawns)
  2. No recapture available for White
  Result: Black wins the queen for free
  Net material change: -900 centipawns for White

Conclusion: This position is NOT favorable for White despite
the temporary queen advantage. The queen was undefended.
```

### The "Quiet Position" Guarantee

When the main search returns a score, quiescence search guarantees that the evaluation is based on a **quiet position** — one where no immediate captures are pending. This means the explanation can focus on **strategic factors** rather than tactical emergencies:

```
After resolving all tactical sequences (quiescence search),
the position is quiet. The evaluation of +0.35 is based on:
  (1) Slight center control advantage (+0.15)
  (2) Better pawn structure (+0.10)
  (3) More active piece placement (+0.10)
```

Without the "quiet" guarantee, the explanation would be unreliable — tactical imbalances could make the strategic analysis meaningless.

---

## Key Takeaways

- **Quiescence search** continues the search beyond depth 0 for as long as there are captures (and sometimes checks/promotions) available.
- It prevents the **Horizon Effect**: evaluating positions mid-exchange and producing wildly inaccurate assessments.
- The **stand-pat score** serves as the baseline — the side to move can always choose not to capture.
- **Delta pruning** skips captures that cannot possibly raise the score above alpha.
- **SEE pruning** skips clearly losing captures.
- **MVV-LVA ordering** ensures the most promising captures are tried first.
- Qsearch accounts for **30-40%** of search nodes but is essential for evaluation accuracy.
- For explainability, qsearch ensures that **explanations are based on resolved positions**, not hallucinated material advantages.

## Cross-References

- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the main search that calls qsearch at depth 0
- [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax Algorithm]] — the Horizon Effect in the context of depth-limited search
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — MVV-LVA ordering within qsearch
- [[01-Foundations/03 - Move Generation|Move Generation]] — capture-only generation for qsearch
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — preventing hallucinated explanations
