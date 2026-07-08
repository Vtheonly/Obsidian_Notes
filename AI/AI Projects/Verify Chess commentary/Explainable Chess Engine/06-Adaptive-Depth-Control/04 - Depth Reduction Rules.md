# Depth Reduction Rules

> "The art of search is knowing where NOT to look." — Chess Programming Wisdom

## What Are Depth Reductions?

A **depth reduction** subtracts one or more plies from the search depth for a specific move. It tells the engine: "This line is unlikely to be important—spend less time on it." Reductions are the [[Depther]]'s primary tool for **saving computation** on lines that are probably not relevant to the final decision.

Reductions are the complement of [[Depth Extension Rules|extensions]]. If extensions are investments in promising lines, reductions are savings from unpromising ones. The key insight is that **most moves at most positions are not worth searching deeply**—only a few critical lines determine the evaluation.

Every reduction follows the same pattern as extensions:

1. **What**: The condition that triggers the reduction.
2. **Why**: The chess reason why less search depth is warranted.
3. **How**: The code that detects the condition.
4. **When**: The game situations where the reduction fires.

## The Safety Net: Re-Search

Before diving into specific rules, it is essential to understand that **reductions are never final**. If a reduced search returns a score above the current alpha bound (meaning the move is surprisingly good), the engine **re-searches the move at full depth**. This safety net ensures that reductions never cause the engine to miss a good move—they only save time on moves that are genuinely poor.

```python
def search_with_reductions(board: Board, move: Move, depth: int,
                           alpha: int, beta: int,
                           reduction: int) -> int:
    """
    Search a move with a potential reduction.
    If the result is surprisingly good, re-search at full depth.
    """
    # Search with reduced depth
    reduced_depth = max(1, depth - reduction)
    board.push(move)
    score = -negamax(board, reduced_depth - 1, -beta, -alpha)

    # Re-search at full depth if this move is surprisingly good
    if score > alpha and reduction > 0:
        score = -negamax(board, depth - 1, -beta, -alpha)

    board.pop()
    return score
```

## Rule 1: Late Move Reduction (LMR) (-1)

### What
Moves that appear **late in the move ordering** (not captures, not checks, not killer moves) are reduced by 1 ply. This is the famous **Late Move Reduction** (LMR) technique, pioneered by various engines in the 2000s and now universally used.

### Why
Move ordering heuristics (see [[Root-Level Selectivity]]) sort moves by expected quality. The first few moves are likely to be the best; the later moves are unlikely to improve the alpha bound. Searching them at full depth is wasteful because:
- They are unlikely to be the best move.
- Even if they are searched at reduced depth, they will almost certainly score below alpha.
- The re-search safety net catches the rare cases where a late move is surprisingly good.

The expected savings are enormous: in a position with 35 legal moves, the first 5 might be searched at full depth, while the remaining 30 are reduced, saving roughly 30% of search time.

### How
```python
def lmr_reduction(board: Board, move: Move, move_index: int, depth: int) -> DepthDelta:
    """
    Late Move Reduction: reduce depth for late, quiet moves.
    Only apply if:
    1. Move index is high (not one of the first few moves)
    2. Move is quiet (not capture, not check, not promotion)
    3. Depth is sufficient (LMR at depth 1-2 is meaningless)
    """
    # Conditions for LMR
    is_capture = board.is_capture(move)
    gives_check = board.gives_check(move)
    is_promotion = move.promotion is not None
    is_killer = move in killer_moves

    is_quiet = not (is_capture or gives_check or is_promotion or is_killer)

    if not is_quiet:
        return DepthDelta(delta=0, rule_name="lmr", reason="")

    if move_index < 3:
        # Don't reduce early moves—even quiet ones might be good
        return DepthDelta(delta=0, rule_name="lmr", reason="")

    if depth < 3:
        # LMR is meaningless at very shallow depths
        return DepthDelta(delta=0, rule_name="lmr", reason="")

    # Reduction amount increases with move index
    reduction = 1
    if move_index >= 6 and depth >= 6:
        reduction = 2  # Aggressive LMR for very late moves at high depth

    return DepthDelta(
        delta=-reduction,
        rule_name="lmr",
        reason=f"Reducing by {reduction} ply: this is a quiet move ranked {move_index+1} in the move order—unlikely to be the best move"
    )
```

### When
- **Positional maneuvers**: Moves like a3, h3, Rac1 that are quiet and non-forcing.
- **Candidate moves with alternatives**: When there are better-looking moves already searched.
- **Non-critical positions**: Where the evaluation is stable and unlikely to change.

### Explanation
> "Reducing by 1 ply: a3 is a quiet pawn move ranked 8th in the move order. It's unlikely to improve on the current best move, so we search it more shallowly."

---

## Rule 2: Quiet Move Reduction (-1)

### What
A **quiet move** (non-capture, non-check, non-promotion, non-killer) that doesn't significantly improve the position's evaluation heuristic is reduced by 1 ply.

### Why
This is a stricter version of LMR that applies even to moves that are early in the ordering but are demonstrably quiet. The distinction from LMR is that this rule fires based on the **character of the move itself**, not its position in the move list.

### How
```python
def quiet_move_reduction(board: Board, move: Move) -> DepthDelta:
    """
    Reduce depth for moves that are completely quiet.
    A quiet move has no tactical significance whatsoever.
    """
    if board.is_capture(move):
        return DepthDelta(delta=0, rule_name="quiet_move", reason="")
    if board.gives_check(move):
        return DepthDelta(delta=0, rule_name="quiet_move", reason="")
    if move.promotion:
        return DepthDelta(delta=0, rule_name="quiet_move", reason="")

    # Check if the move improves the static evaluation significantly
    piece = board.piece_at(move.from_square)
    if piece:
        current_pst = pst_value(piece.type, move.from_square, piece.color, phase)
        new_pst = pst_value(piece.type, move.to_square, piece.color, phase)
        pst_change = new_pst - current_pst

        if pst_change < -10:
            # Moving to a worse square—definitely reduce
            return DepthDelta(
                delta=-1,
                rule_name="quiet_move",
                reason=f"Reducing by 1 ply: {move_san(move)} is a quiet move that doesn't improve piece positioning"
            )

    return DepthDelta(
        delta=-1,
        rule_name="quiet_move",
        reason=f"Reducing by 1 ply: {move_san(move)} is a quiet move with no tactical significance"
    )
```

### When
- **Repositioning moves**: Moving a piece from one square to another similar square.
- **Prophylactic moves**: Moves that prevent threats rather than create them.
- **Non-forcing pawn moves**: Pushing pawns that don't create immediate threats.

---

## Rule 3: Mindless Exchange Reduction (-1)

### What
When a sequence of captures leads to a **neutral exchange** (neither side gains material), the continuation beyond the exchange is reduced.

### Why
Mindless exchanges (trading pieces with no positional advantage) are common in amateur games but rarely lead to interesting positions. The evaluation after a neutral exchange is typically the same as before it, minus the traded pieces. Reducing depth on these lines saves time for more interesting continuations.

### How
```python
def mindless_exchange_reduction(board: Board, move: Move, ply: int) -> DepthDelta:
    """
    Reduce depth for captures that are part of a mindless (neutral) exchange.
    Detect by checking if the capture value roughly equals the recapture value.
    """
    if not board.is_capture(move):
        return DepthDelta(delta=0, rule_name="mindless_exchange", reason="")

    victim = board.piece_at(move.to_square)
    attacker = board.piece_at(move.from_square)

    if victim is None or attacker is None:
        return DepthDelta(delta=0, rule_name="mindless_exchange", reason="")

    victim_value = PIECE_VALUES.get(victim.type, 0)
    attacker_value = PIECE_VALUES.get(attacker.type, 0)

    # If the attacker is worth more than the victim, this might be a sacrifice
    # If the attacker is worth less, this is a winning capture (don't reduce!)
    # If they're similar value, it's a mindless exchange
    value_diff = abs(victim_value - attacker_value)

    if value_diff <= 50:  # Within half a pawn—roughly equal exchange
        return DepthDelta(
            delta=-1,
            rule_name="mindless_exchange",
            reason=f"Reducing by 1 ply: {move_san(move)} is a roughly equal exchange (attacker: {attacker_value}cp, victim: {victim_value}cp)"
        )

    return DepthDelta(delta=0, rule_name="mindless_exchange", reason="")
```

### When
- **Knight for bishop trades**: The "exchange of minor pieces."
- **Rook for rook trades**: Neutralizing the position.
- **Queen for queen trades**: Simplifying to an endgame.

---

## Rule 4: Rim Knight Reduction (-1)

### What
A move that places a **knight on the edge of the board** (a-file, h-file, 1st rank, 8th rank) is reduced by 1 ply.

### Why
The chess proverb says it all: "A knight on the rim is dim." Edge knights control fewer squares (2-4 instead of 8 in the center) and are rarely the best move. In most positions, moving a knight to the edge is a sign of poor planning. There are exceptions (e.g., Na6 in the Najdorf), but they are rare enough that the reduction is justified.

### How
```python
def rim_knight_reduction(board: Board, move: Move) -> DepthDelta:
    """Reduce depth for moves that place a knight on the rim."""
    piece = board.piece_at(move.from_square)
    if piece is None or piece.type != KNIGHT:
        return DepthDelta(delta=0, rule_name="rim_knight", reason="")

    to_file = move.to_square % 8
    to_rank = move.to_square // 8

    # Edge files (a, h) or edge ranks (1, 8)
    is_rim = to_file == 0 or to_file == 7 or to_rank == 0 or to_rank == 7

    # Corner squares are especially bad
    is_corner = (to_file == 0 or to_file == 7) and (to_rank == 0 or to_rank == 7)

    if is_corner:
        return DepthDelta(
            delta=-2,  # Extra reduction for corner knights
            rule_name="rim_knight",
            reason=f"Reducing by 2 plies: placing a knight on {square_name(move.to_square)} (corner) gives it minimal control"
        )
    elif is_rim:
        return DepthDelta(
            delta=-1,
            rule_name="rim_knight",
            reason=f"Reducing by 1 ply: placing a knight on {square_name(move.to_square)} (edge) limits its mobility—a knight on the rim is dim"
        )

    return DepthDelta(delta=0, rule_name="rim_knight", reason="")
```

### When
- **Na4/Nh4 maneuvers**: Common beginner moves that waste time.
- **Knight retreats to the edge**: When the knight has no good central squares.
- **Defensive knight moves**: When a knight retreats to the edge to avoid capture.

---

## Rule 5: Historical Failure Reduction (-1)

### What
If a move has been **previously searched and found to be significantly worse than the best move** (a "historical failure"), it is reduced by 1 ply in subsequent iterations.

### Why
The [[History Heuristic]] tracks how often each move has been the best move in similar positions. Moves with low history scores are unlikely to be good. Reducing their depth avoids wasting time on moves that have repeatedly been poor.

### How
```python
def historical_failure_reduction(board: Board, move: Move,
                                 history_table: dict) -> DepthDelta:
    """
    Reduce depth for moves that have historically been poor.
    Uses the history heuristic table.
    """
    from_sq = move.from_square
    to_sq = move.to_square
    piece = board.piece_at(from_sq)

    if piece is None:
        return DepthDelta(delta=0, rule_name="historical_failure", reason="")

    history_score = history_table.get(piece.type, {}).get(from_sq * 64 + to_sq, 0)

    # Normalize: history_score is a cumulative counter
    # Low scores mean this move has rarely/never been best
    if history_score < -100:
        return DepthDelta(
            delta=-1,
            rule_name="historical_failure",
            reason=f"Reducing by 1 ply: this move has consistently performed poorly in similar positions (history score: {history_score})"
        )

    return DepthDelta(delta=0, rule_name="historical_failure", reason="")
```

### When
- **Repeatedly rejected moves**: Moves that were searched in previous iterations and scored poorly.
- **Anti-killer moves**: Moves that are the opposite of killer moves—they have never been good.
- **Position-specific failures**: Moves that might look good but fail tactically in this specific position type.

---

## Rule 6: Stable Quiet Reduction (-1)

### What
When the **evaluation has been stable** across multiple iterations (the best move and its score haven't changed), quiet moves in subsequent iterations are reduced by 1 ply.

### Why
Stability in iterative deepening is a strong signal that the search has converged on the correct evaluation. If the best move has been the same for the last 3 iterations and the score has barely changed, there's little value in exploring quiet alternatives deeply. The engine has effectively "solved" this position.

### How
```python
def stable_quiet_reduction(move: Move, iteration_stability: int,
                           is_capture: bool, gives_check: bool) -> DepthDelta:
    """
    Reduce depth for quiet moves when the search is stable.
    Stability means the best move and score haven't changed across iterations.
    """
    if is_capture or gives_check:
        return DepthDelta(delta=0, rule_name="stable_quiet", reason="")

    if iteration_stability >= 3:
        return DepthDelta(
            delta=-1,
            rule_name="stable_quiet",
            reason=f"Reducing by 1 ply: the search has been stable for {iteration_stability} iterations, making deep exploration of quiet alternatives unlikely to change the result"
        )

    return DepthDelta(delta=0, rule_name="stable_quiet", reason="")
```

### When
- **Converged searches**: When iterative deepening has stabilized.
- **Clear best move**: When one move has dominated the search.
- **Time pressure**: When the engine needs to save time for more promising positions.

---

## Reduction Interaction and Capping

Multiple reductions can stack: a late, quiet, rim knight with poor history might trigger 4 different reduction rules. However, the total reduction is **capped** (see [[Safety and Control Rules]]) to prevent over-reducing:

```python
MAX_REDUCTION_PER_MOVE = 3  # Never reduce more than 3 plies

def compute_total_reduction(board: Board, move: Move, context: SearchContext) -> DepthDelta:
    """
    Compute the total depth reduction for a move.
    Multiple reductions can stack, but are capped.
    """
    deltas = []

    for rule in REDUCTION_RULES:
        delta = rule(board, move, context)
        if delta.delta != 0:
            deltas.append(delta)

    total_delta = max(-MAX_REDUCTION_PER_MOVE, sum(d.delta for d in deltas))
    reasons = [d.reason for d in deltas if d.reason]

    return DepthDelta(
        delta=total_delta,
        rule_name="combined_reductions",
        reason="; ".join(reasons)
    )
```

## The Reduction Budget

Just as extensions must be "paid for," reductions create a **budget** that can be spent on extensions elsewhere. In a well-tuned engine, the total depth saved by reductions roughly equals the total depth spent on extensions:

$$
\sum_{\text{reductions}} |\delta| \approx \sum_{\text{extensions}} \delta
$$

This budget balancing ensures that the engine doesn't search deeper overall (which would be slower) but searches **more intelligently**—deeper on important lines, shallower on unimportant ones.

## Summary

Depth reductions are the engine's way of saying **"this line probably doesn't matter—spend less time on it."** Each reduction is triggered by a specific heuristic, from the universal (LMR) to the specific (rim knight). The re-search safety net ensures that no good move is ever permanently missed, and each reduction carries a human-readable explanation of why the engine chose to search less deeply.

---

**See also:** [[The Depther Philosophy]], [[Depth Extension Rules]], [[Safety and Control Rules]], [[Quiescence Termination Rules]], [[The Depth Rules Module (Code Architecture)]], [[LMR]], [[History Heuristic]], [[Killer Moves]]
