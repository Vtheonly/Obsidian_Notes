---
tags:
  - search
  - null-move
  - pruning
  - zugzwang
  - heuristic
chapter: "03"
---

# Null Move Pruning (NMP)

## Overview

**Null Move Pruning (NMP)** is a heuristic that exploits a simple but powerful insight: if a position is so strong that **skipping your turn** still keeps your score above beta, then the position is almost certainly winning, and no further search is needed at this node. NMP is one of the most effective pruning techniques in chess, typically saving **30-60%** of search nodes. However, it carries a critical danger: it fails catastrophically in **zugzwang** positions where any move worsens your position.

---

## The Insight

### "Even Doing Nothing Is Winning"

In most chess positions, having the move is an advantage — you can improve your position. If we skip our turn (make a "null move") and the opponent gets to move twice in a row, our position should worsen. But if it's **still above beta** even after the opponent moves twice, then our position must be overwhelmingly dominant.

Formally: if $V(\text{null-move}(s), D-R-1) \geq \beta$, then $V(s, D) \geq \beta$ with very high probability.

### Why This Works

Consider a position where White has an extra queen. Even if Black gets two moves in a row (White's turn + Black's turn), White's position remains winning because the material advantage is so large. The null move search detects this dominance cheaply: instead of searching the full tree at depth $D$, we search a single continuation at depth $D - 1 - R$.

---

## The Algorithm

### Basic Null Move Search

```python
def search_with_nmp(position, depth, alpha, beta):
    if depth <= 0:
        return quiescence(position, alpha, beta)

    # Null move pruning
    if depth >= 3 and not position.is_in_check() and not position.is_endgame():
        position.make_null_move()  # Skip our turn
        R = 2  # Reduction constant
        score = -search_with_nmp(position, depth - 1 - R, -beta, -beta + 1)
        position.unmake_null_move()

        if score >= beta:
            return beta  # Position is so strong that even doing nothing wins

    # Normal search
    for move in position.generate_legal_moves():
        position.make_move(move)
        score = -search_with_nmp(position, depth - 1, -beta, -alpha)
        position.unmake_move(move)

        if score >= beta:
            return score  # Beta cutoff
        if score > alpha:
            alpha = score

    return alpha
```

### The Reduction Constant $R$

The null move is searched at reduced depth $D - 1 - R$, where $R$ is typically:

- **$R = 2$**: Most common. Conservative but safe. Used at moderate depths.
- **$R = 3$**: More aggressive. Used at higher depths (depth ≥ 6) where the position is less likely to be zugzwang.
- **Adaptive $R$**: Some engines use $R = 2 + \lfloor D/6 \rfloor$, increasing the reduction at deeper depths.

```cpp
int null_move_reduction(int depth) {
    if (depth >= 6) return 3;
    return 2;
}
```

---

## Implementation Details

### Making the Null Move

A null move is a special operation that switches the side to move without making any piece movement:

```cpp
void Position::make_null_move() {
    // Save state for unmake
    history[ply].en_passant = en_passant_square;
    history[ply].castling = castling_rights;
    history[ply].side = side_to_move;

    // Switch side to move
    side_to_move = ~side_to_move;

    // Clear en passant (it's invalid after a null move — the opponent didn't push a pawn)
    en_passant_square = -1;

    ply++;
}

void Position::unmake_null_move() {
    ply--;
    side_to_move = history[ply].side;
    en_passant_square = history[ply].en_passant;
    castling_rights = history[ply].castling;
}
```

**Critical**: The en passant square must be cleared after a null move. If White played a null move and the en passant square was set (from Black's previous double pawn push), it would be incorrect for Black to capture en passant — White didn't actually push a pawn.

### Full C++ Implementation

```cpp
int search(Position& pos, int depth, int alpha, int beta, bool is_null_move) {
    // Terminal conditions
    if (depth <= 0) {
        return quiescence(pos, alpha, beta);
    }

    if (pos.is_draw()) return 0;

    bool in_check = pos.is_in_check();
    if (in_check) depth++; // Check extension

    // ===== Null Move Pruning =====
    // Conditions:
    //   1. Not already in a null move (no consecutive null moves)
    //   2. Depth >= 3
    //   3. Not in check
    //   4. Not an endgame (to avoid zugzwang)
    //   5. Static eval >= beta (position looks promising)
    if (!is_null_move && depth >= 3 && !in_check && !pos.is_endgame()) {
        int static_eval = evaluate(pos);
        if (static_eval >= beta) {
            int R = null_move_reduction(depth);

            pos.make_null_move();
            int null_score = -search(pos, depth - 1 - R, -beta, -beta + 1, true);
            pos.unmake_null_move();

            if (null_score >= beta) {
                // Verify: don't return unverified mate scores
                if (null_score >= MATE_SCORE - MAX_DEPTH) {
                    return beta; // Return beta, not the mate score
                }
                return null_score;
            }
        }
    }

    // ===== Normal Search =====
    MoveList moves = pos.generate_legal_moves();
    if (moves.count == 0) {
        return in_check ? -MATE_SCORE + pos.ply() : 0;
    }

    order_moves(pos, moves);

    int best_score = -INFINITY_SCORE;

    for (int i = 0; i < moves.count; i++) {
        pos.make_move(moves[i]);
        int score = -search(pos, depth - 1, -beta, -alpha, false);
        pos.unmake_move(moves[i]);

        if (score > best_score) best_score = score;
        if (score >= beta) {
            update_cutoff_info(pos, moves[i], depth);
            return best_score;
        }
        if (score > alpha) alpha = score;
    }

    return best_score;
}
```

### The `is_null_move` Flag

The boolean parameter `is_null_move` prevents **consecutive null moves** — two null moves in a row would allow the same side to move three times, which is nonsensical. After a null move, the next recursive call cannot also be a null move.

---

## The Zugzwang Trap

### What Is Zugzwang?

**Zugzwang** (German: "compulsion to move") is a situation where any legal move worsens your position. In a zugzwang, the null move search would conclude "even doing nothing is good" — but in reality, you are **forced** to move, and every move is bad.

### Example: Simple Zugzwang

```
White: King on g1, Pawn on f3
Black: King on g3

It's White's turn. White is in zugzwang:
- Kg2?? allows Kxf3 (loses the pawn)
- Kf1?? allows Kh2 (king invades)
- f4?? creates a passed pawn but Black's king catches it
- Any move worsens White's position

Null move search: "Skip White's move, Black plays Kg4 or Kh2 — 
but White's position is still drawable." 
Actual: White must move, and every move loses.
```

### When Zugzwang Occurs

Zugzwang is most common in:
1. **Pawn endgames**: With only pawns and kings, every pawn push may create a weakness
2. **Blockaded positions**: Where pieces are pinned to defensive squares
3. **Mutual zugzwang**: Both sides would prefer not to move

### NMP Safety Conditions

To minimize the risk of zugzwang-related errors, NMP is disabled when:

1. **In check**: The position is tactical; every move matters
2. **Endgame**: Fewer pieces mean more frequent zugzwang
3. **Few pieces**: Specifically, when only kings and pawns remain
4. **Depth < 3**: The null move search would be too shallow to be reliable
5. **Already in a null move**: Prevents double-null-move chains

```cpp
bool is_endgame(const Position& pos) {
    // Endgame detection: few major pieces
    int total_material = 0;
    for (Color c : {WHITE, BLACK}) {
        total_material += __builtin_popcountll(pos.queens[c]) * 900;
        total_material += __builtin_popcountll(pos.rooks[c]) * 500;
        total_material += __builtin_popcountll(pos.bishops[c]) * 330;
        total_material += __builtin_popcountll(pos.knights[c]) * 320;
    }
    return total_material <= 1500; // Roughly: no queens, at most one rook per side
}
```

### Verification Search

Some engines implement a **verification search** after NMP cuts off: when the null move indicates a cutoff, instead of returning immediately, a reduced-depth search is performed with the null move disabled:

```cpp
if (null_score >= beta) {
    // Verify with a shallow search (no null move allowed)
    int verify_score = search(pos, depth - 1 - R, alpha, beta, true);
    if (verify_score >= beta) {
        return verify_score;
    }
    // Verification failed — possible zugzwang, continue normal search
}
```

This adds safety at the cost of some speed. Most engines skip verification for non-endgame positions but enable it in the endgame.

---

## Advanced NMP Techniques

### Adaptive Null Move Reduction

Instead of a fixed $R$, some engines adapt the reduction based on the position:

```cpp
int adaptive_null_reduction(int depth, int static_eval, int beta) {
    int R = 2;

    // More aggressive reduction when eval is far above beta
    if (static_eval - beta > 200) R++;  // Position is crushing
    if (static_eval - beta > 400) R++;  // Position is overwhelming

    // More aggressive at deep depths
    if (depth >= 8) R++;

    return R;
}
```

### Null Move in PVS Framework

In the [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] framework, the null move search uses a null window $[-\beta, -\beta + 1]$, consistent with the PVS approach:

```cpp
int null_score = -search(pos, depth - 1 - R, -beta, -beta + 1, true);
```

If this fails high, the position is above beta and we can return. No re-search is needed because we only need to know whether the position is above beta.

---

## NMP and Elo Impact

Null Move Pruning is estimated to provide **200-300 Elo** of improvement. Without NMP, engines would search 4-6 plies shallower, missing many tactical and positional insights.

| Configuration | Effective Depth | Estimated Elo |
|---------------|----------------|--------------|
| No NMP | ~16-18 ply | ~2800 |
| NMP (R=2) | ~20-24 ply | ~3100 |
| NMP (adaptive R) | ~22-26 ply | ~3200 |

---

## Connection to Explainability

### "The Position Was So Strong That Even Doing Nothing Was Winning"

NMP provides one of the most intuitive explanations in chess: when the null move search confirms a cutoff, the explanation system can say:

```
The engine determined that this position is so favorable that
even if you passed your turn (doing nothing), your position
would still be better than the minimum acceptable threshold.

Specifically: After a null move (skipping your turn), your
opponent gets two moves in a row, but your advantage remains
+1.20, which is above the threshold of +0.80 needed to
prune this branch.

Key factors making your position dominant:
  (1) Material advantage: +2 pawns
  (2) Piece activity: All your pieces are well-placed
  (3) King safety: Your king is well-protected
```

### Explaining Why NMP Was NOT Applied

When NMP is disabled (e.g., in an endgame), the explanation system can note:

```
Note: Null Move Pruning was NOT applied at this node because
the position is an endgame with few pieces. In endgames,
the "compulsion to move" (zugzwang) can make doing nothing
appear better than it actually is, since you are forced to
make a move that may worsen your position.
```

### Zugzwang as an Explanatory Concept

Zugzwang is itself an important chess concept that the explanation system should teach:

```
ZUGZWANG DETECTED: This position features zugzwang — any move
White makes will worsen their position. This is because:

  (1) The king is confined to defensive squares
  (2) Every pawn push creates a weakness
  (3) No piece can improve its position

In such positions, the side NOT to move has an advantage
even with equal material. The concept of zugzwang is
critical for endgame understanding.
```

---

## Key Takeaways

- **Null Move Pruning** tests whether "doing nothing" still keeps the score above beta. If so, the position is overwhelmingly dominant and the branch can be pruned.
- The null move is searched at **reduced depth** $D - 1 - R$ where $R$ is typically 2-3.
- **Zugzwang is the critical danger**: in positions where any move worsens your position, NMP incorrectly concludes the position is good.
- **Safety conditions** prevent NMP in check, endgames, shallow depths, and consecutive null moves.
- NMP provides **200-300 Elo** of improvement by enabling 4-6 additional plies of search.
- For explainability, NMP provides the intuitive explanation: "the position was so strong that even doing nothing was winning."

## Cross-References

- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the framework within which NMP operates
- [[03-Search-Accelerators/03 - Late Move Reductions (LMR)|LMR]] — another depth-reduction heuristic
- [[03-Search-Accelerators/05 - Quiescence Search|Quiescence Search]] — the search that follows when depth reaches 0
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — how NMP's "doing nothing is winning" concept supports explanation
