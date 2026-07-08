# Quiescence Termination Rules

> "A search that stops in the middle of a capture sequence is worse than no search at all." — Chess Programming Principle

## The Horizon Problem

The fundamental problem that [[Quiescence Search]] solves is the **horizon effect**: if the search stops at a fixed depth, it may evaluate a position as favorable when in fact a devastating tactical sequence is about to unfold. Consider:

```
Position: White to move, depth 0 reached
White has: Queen on d1, extra pawn
Black has: Rook on d8 attacking White's queen
```

At depth 0, the static evaluation might say "+100" (White has an extra pawn). But on the very next move, Black plays Rxd1—capturing the queen! The "true" evaluation is "-800" (White lost a queen for a pawn). The horizon effect has concealed a tactical catastrophe.

Quiescence search continues the search beyond depth 0 for **tactical moves** (captures, checks, promotions) until the position is **quiet**—no more forcing moves are available. Only then is the static evaluation trusted.

## What Makes a Position "Quiet"?

A position is **quiet** when:

1. No captures are possible (or all captures are clearly losing).
2. No checks are available (or all checks are easily parried).
3. No promotion threats exist.
4. The evaluation is **stable**—it won't change significantly with one more ply.

Conversely, a position is **tactical** (or "noisy") when:

1. Captures are available and at least one is not clearly losing.
2. A check can be delivered.
3. A pawn is about to promote.
4. The evaluation differs significantly from the stand-pat score.

## Quiescence Search Algorithm

The core quiescence search algorithm:

```python
def quiescence(board: Board, alpha: int, beta: int, ply: int) -> int:
    """
    Quiescence search: continue searching tactical moves at depth 0.
    Stops only when the position is quiet (no more profitable captures/checks).
    """
    # Stand-pat: the evaluation if we do nothing
    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta  # Position is already too good for us; opponent won't allow it

    if stand_pat > alpha:
        alpha = stand_pat  # We can at least achieve this score by doing nothing

    # Generate tactical moves (captures and checks)
    tactical_moves = generate_tactical_moves(board)

    # Sort by MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
    tactical_moves.sort(key=lambda m: mvv_lva_score(board, m), reverse=True)

    for move in tactical_moves:
        # Delta pruning: skip captures that can't possibly raise alpha
        if not is_capture_worth_trying(board, move, alpha, stand_pat):
            continue

        board.push(move)
        score = -quiescence(board, -beta, -alpha, ply + 1)
        board.pop()

        if score >= beta:
            return beta

        if score > alpha:
            alpha = score

    return alpha
```

## Termination Rules

The quiescence search must eventually terminate. Our engine uses **five termination rules** to decide when to stop searching and trust the static evaluation.

### Rule 1: No Tactical Moves Available

The simplest rule: if there are no captures, checks, or promotions available, the position is quiet, and we return the static evaluation.

```python
def has_tactical_moves(board: Board) -> bool:
    """Check if any tactical moves (captures, checks, promotions) exist."""
    for move in board.legal_moves():
        if board.is_capture(move):
            return True
        if board.gives_check(move):
            return True
        if move.promotion:
            return True
    return False
```

### Rule 2: Delta Pruning

**Delta pruning** skips captures that cannot possibly raise the score above alpha, even with the most optimistic assumptions. If the captured piece's value plus a safety margin is less than the gap between the stand-pat score and alpha, the capture is futile.

```python
DELTA_MARGIN = 200  # centipawns safety margin

def is_capture_worth_trying(board: Board, move: Move,
                            alpha: int, stand_pat: int) -> bool:
    """
    Delta pruning: skip captures that can't possibly raise alpha.
    Even in the best case, this capture can only gain the victim's value.
    """
    if not board.is_capture(move):
        return True  # Non-captures always worth trying (checks)

    victim = board.piece_at(move.to_square)
    if victim is None:
        return True  # En passant or other special case

    potential_gain = PIECE_VALUES[victim.type] + DELTA_MARGIN
    if stand_pat + potential_gain < alpha:
        return False  # Even the best case can't raise alpha

    return True
```

**Why this matters for explainability**: When delta pruning fires, we can say: "We skipped the capture Bxa3 because even winning the pawn (100 cp) plus a margin (200 cp) cannot raise the score above the current best option (+450 cp)."

### Rule 3: See (Static Exchange Evaluation) Pruning

**SEE pruning** uses the Static Exchange Evaluation to determine whether a capture is winning or losing. If a capture has a negative SEE score (the sequence of recaptures results in a net loss), it is skipped in quiescence search.

```python
def see(board: Board, square: int) -> int:
    """
    Static Exchange Evaluation for a square.
    Computes the net material gain/loss from a sequence of captures
    on the given square.
    """
    gain = [0] * 32  # Gain at each depth of the exchange
    depth = 0
    color = board.color_attacking(square)  # Who attacks first?

    while True:
        # Find the least valuable attacker of the given color
        attacker_sq = board.least_valuable_attacker(square, color)
        if attacker_sq is None:
            break  # No more attackers

        attacker = board.piece_at(attacker_sq)
        gain[depth + 1] = -gain[depth] + PIECE_VALUES[board.piece_at(square).type]

        # If the recapture loses material, stop
        if gain[depth + 1] < -PIECE_VALUES[attacker.type]:
            break

        depth += 1
        # "Remove" the captured piece and the attacker, continue
        color = not color

    # Backpropagate: at each depth, the capturer chooses the best option
    while depth > 0:
        gain[depth - 1] = -max(-gain[depth - 1], gain[depth])
        depth -= 1

    return gain[0]

SEE_PRUNING_THRESHOLD = 0  # Skip captures with negative SEE

def should_try_capture_see(board: Board, move: Move) -> bool:
    """Skip captures with negative SEE in quiescence."""
    if not board.is_capture(move):
        return True

    see_score = see(board, move.to_square)
    return see_score >= SEE_PRUNING_THRESHOLD
```

**Explanation**: *"Skipping Qxa2 because the Static Exchange Evaluation shows it loses material: after Qxa2, Rxa2 loses the queen for a rook and pawn (-380 cp)."*

### Rule 4: Maximum Quiescence Depth

Even with all pruning, the quiescence search could theoretically continue forever (e.g., a series of checks that never resolves). We impose a **maximum quiescence depth** as a safety net:

```python
MAX_QUIESCENCE_DEPTH = 10  # Maximum additional plies beyond depth 0

def quiescence_with_depth_limit(board: Board, alpha: int, beta: int,
                                ply: int, max_ply: int) -> int:
    """
    Quiescence search with a hard depth limit.
    Even if tactical moves are available, stop at max_ply.
    """
    if ply >= max_ply:
        return evaluate(board)  # Force termination

    stand_pat = evaluate(board)
    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    tactical_moves = generate_tactical_moves(board)
    for move in tactical_moves:
        if not is_capture_worth_trying(board, move, alpha, stand_pat):
            continue
        if board.is_capture(move) and not should_try_capture_see(board, move):
            continue

        board.push(move)
        score = -quiescence_with_depth_limit(board, -beta, -alpha, ply + 1, max_ply)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha
```

### Rule 5: Tactical Noise Detection

Sometimes a position has many tactical moves but they are all **noise**—they don't change the evaluation significantly. In such cases, continuing the quiescence search is pointless. We detect this by tracking whether any move has significantly changed the alpha bound:

```python
def quiescence_with_noise_detection(board: Board, alpha: int, beta: int,
                                    ply: int, quiet_streak: int = 0) -> int:
    """
    Quiescence search with tactical noise detection.
    If multiple moves fail to change alpha, the position is 'noisy but stable.'
    """
    stand_pat = evaluate(board)
    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    # If we've had a streak of moves that didn't change alpha, stop
    if quiet_streak >= 3:
        return alpha  # Tactical noise—no meaningful changes

    tactical_moves = generate_tactical_moves(board)
    alpha_changed = False

    for move in tactical_moves:
        board.push(move)
        score = -quiescence_with_noise_detection(
            board, -beta, -alpha, ply + 1,
            0 if not alpha_changed else quiet_streak + 1
        )
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
            alpha_changed = True

    return alpha
```

## The Full Quiescence Pipeline

Combining all rules into a complete quiescence search:

```python
def quiescence_full(board: Board, alpha: int, beta: int, ply: int,
                    context: QuiescenceContext) -> Tuple[int, List[str]]:
    """
    Full quiescence search with all termination rules.
    Returns (score, reasons) for explainability.
    """
    reasons = []

    # Rule 4: Maximum depth
    if ply >= context.max_ply:
        reasons.append("Forced termination: maximum quiescence depth reached")
        return evaluate(board), reasons

    stand_pat = evaluate(board)

    # Beta cutoff
    if stand_pat >= beta:
        return beta, reasons

    # Update alpha
    if stand_pat > alpha:
        alpha = stand_pat

    # Rule 1: No tactical moves
    tactical_moves = generate_tactical_moves(board)
    if not tactical_moves:
        return alpha, ["Position is quiet—no tactical moves available"]

    # Sort by MVV-LVA
    tactical_moves.sort(key=lambda m: mvv_lva_score(board, m), reverse=True)

    for move in tactical_moves:
        # Rule 2: Delta pruning
        if board.is_capture(move) and not is_capture_worth_trying(board, move, alpha, stand_pat):
            reasons.append(f"Delta pruned: {move_san(move)} can't raise alpha")
            continue

        # Rule 3: SEE pruning
        if board.is_capture(move) and not should_try_capture_see(board, move):
            reasons.append(f"SEE pruned: {move_san(move)} loses material in the exchange")
            continue

        board.push(move)
        score, child_reasons = quiescence_full(board, -beta, -alpha, ply + 1, context)
        score = -score
        board.pop()

        if score >= beta:
            return beta, reasons + [f"Beta cutoff after {move_san(move)}"]

        if score > alpha:
            alpha = score

    return alpha, reasons
```

## Quiescence in the Explainable Engine

The quiescence search is a natural point for explanation because it answers the question: **"Did the engine check for tactical consequences?"** The explanation might look like:

> "The static evaluation was +150 cp (White has an extra pawn). The quiescence search verified this by exploring 4 captures: Rxd5 (White recaptures, +150), Qxd5 (Black recaptures the rook, -50), and two delta-pruned captures that couldn't change the outcome. The final quiescence score is +150 cp."

This level of detail is what separates our engine from a black box—it shows its work, even in the tactical "mop-up" phase of the search.

## Summary

Quiescence termination rules ensure that the engine **never trusts a static evaluation in a tactical position**. By continuing to search captures and checks at depth 0, and by using pruning (delta, SEE), depth limits, and noise detection to keep the quiescence search efficient, we achieve both accuracy and speed. Each termination rule carries an explanation, making the quiescence phase as transparent as the rest of the search.

---

**See also:** [[The Depther Philosophy]], [[Depth Extension Rules]], [[Depth Reduction Rules]], [[Safety and Control Rules]], [[Static Evaluation Overview]], [[Delta Pruning]], [[Static Exchange Evaluation]], [[Horizon Effect]]
