# Depth Extension Rules

> "Extend where the position demands it; reduce where it doesn't." — The Depther's Creed

## What Are Depth Extensions?

A **depth extension** adds one or more plies to the search depth for a specific move. It tells the engine: "This line is important—search it deeper than the base depth." Extensions are the [[Depther]]'s primary tool for ensuring that critical tactical lines are fully explored.

Every extension in our engine follows the pattern:

1. **What**: The concrete condition that triggers the extension.
2. **Why**: The chess reason why deeper search is warranted.
3. **How**: The code that detects the condition.
4. **When**: The game situations where the extension fires.
5. **Explanation**: The human-readable reason string.

## Rule 1: Check Extension (+1)

### What
When a move delivers **check**, the search depth is extended by 1 ply.

### Why
Check is the most forcing move in chess—it requires an immediate, mandatory response. The opponent has no choice but to deal with the check, which means:
- The branching factor drops dramatically (often to 1-3 legal responses).
- Tactical sequences involving checks are the most common way to win material or deliver checkmate.
- Failing to extend on check would create the **horizon effect**: the engine might stop searching just before a decisive check sequence.

### How
```python
def check_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply when the move gives check."""
    if board.gives_check(move):
        return DepthDelta(
            delta=+1,
            rule_name="check_extension",
            reason=f"Extending: {move_san(move)} gives check, forcing the opponent's response"
        )
    return DepthDelta(delta=0, rule_name="check_extension", reason="")
```

### When
- **Fork checks**: A knight or queen delivers check while attacking another piece.
- **Discovered checks**: A piece moves to reveal a check from a piece behind it.
- **Double checks**: Both the moving piece and the discovered piece give check (only king moves are legal).
- **Perpetual check attempts**: Repeated checks that the opponent cannot escape.

### Explanation
> "Extending this line by 1 ply because Nf7+ gives check—the opponent must respond immediately, and the forcing nature of the check may lead to tactical gains."

---

## Rule 2: Capture/Tactical Extension (+1)

### What
When a move **captures a piece** (especially a significant capture), the search depth is extended by 1 ply.

### Why
Captures directly change the material balance. After a capture, the opponent often recaptures, leading to a **forced sequence** of exchanges. Extending on captures ensures that:
- The engine sees the full consequence of the exchange.
- It doesn't stop in the middle of a capture chain, misjudging the final material balance.
- It can evaluate whether the sacrifice is sound.

### How
```python
def capture_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply for significant captures."""
    if board.is_capture(move):
        victim = board.piece_at(move.to_square)
        if victim and victim.type != PAWN:  # Extend on piece captures, not pawn captures
            return DepthDelta(
                delta=+1,
                rule_name="capture_extension",
                reason=f"Extending: {move_san(move)} captures a {victim.type.name}, changing the material balance"
            )
    return DepthDelta(delta=0, rule_name="capture_extension", reason="")
```

### When
- **Queen captures**: The most significant material change.
- **Rook captures**: The exchange changes the game character.
- **Sacrifice sequences**: Where one side gives up material for positional or tactical compensation.
- **Exchange sacrifices**: Rook for minor piece, requiring deeper search to evaluate compensation.

### Explanation
> "Extending by 1 ply because Rxf3 captures a bishop—the material balance shifts, and the full consequences of this exchange must be evaluated."

---

## Rule 3: Promotion Threat Extension (+1)

### What
When a move creates a **pawn promotion threat** (a pawn that can promote on the next move), the search depth is extended by 1 ply.

### Why
Promotion is the most dramatic single move in chess—a pawn becomes a queen (or other piece). The gain is approximately 800-900 centipawns (queen value minus pawn value). This is too significant to miss due to depth limitations.

### How
```python
def promotion_threat_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply when a move creates a promotion threat."""
    piece = board.piece_at(move.from_square)
    if piece and piece.type == PAWN:
        # Check if this pawn will be on the 7th rank (for White) or 2nd rank (for Black)
        to_rank = move.to_square // 8
        if (piece.color == WHITE and to_rank == 6) or (piece.color == BLACK and to_rank == 1):
            # Pawn advancing to penultimate rank—promotion threat!
            return DepthDelta(
                delta=+1,
                rule_name="promotion_threat_extension",
                reason=f"Extending: {move_san(move)} advances a pawn to the 7th rank, threatening promotion"
            )
    return DepthDelta(delta=0, rule_name="promotion_threat_extension", reason="")
```

### When
- **Passed pawn advance**: A passed pawn reaching the 7th rank.
- **Pawn races**: Both sides have pawns racing to promote.
- **Promotion sacrifices**: A side sacrifices material to push a pawn through.

### Explanation
> "Extending by 1 ply because e7 advances the pawn to the 7th rank—on the next move it could promote to a queen, a gain of ~800 centipawns."

---

## Rule 4: Recapture/Tunnel Vision Extension (+1)

### What
When a move **recaptures** on the same square where the opponent just captured, the search depth is extended by 1 ply.

### Why
Recaptures are the natural response to captures—they restore material balance. In a recapture sequence, both sides are forced to continue capturing on the same square ("tunnel vision"). This forced sequence should be fully explored because:
- The final material balance after the exchange chain determines the evaluation.
- Stopping mid-chain would give an inaccurate assessment.
- The recapture is often the only reasonable move, so the branching factor is low.

### How
```python
def recapture_extension(board: Board, move: Move, last_move: Optional[Move]) -> DepthDelta:
    """Extend by 1 ply for recaptures on the same square."""
    if last_move is None:
        return DepthDelta(delta=0, rule_name="recapture_extension", reason="")

    if (board.is_capture(move) and
        move.to_square == last_move.to_square):
        return DepthDelta(
            delta=+1,
            rule_name="recapture_extension",
            reason=f"Extending: {move_san(move)} recaptures on {square_name(move.to_square)}, continuing the exchange sequence"
        )

    return DepthDelta(delta=0, rule_name="recapture_extension", reason="")
```

### When
- **Exchange chains**: Qxd5, Rxd5, Nxd5, etc.
- **Sacrifice recaptures**: After Nxf7, Kxf7—the king recaptures.
- **Center captures**: After exd5, cxd5—recapturing in the center.

### Explanation
> "Extending by 1 ply because Rxe4 recaptures on e4—the exchange sequence must be fully resolved to determine the final material balance."

---

## Rule 5: Trojan Discovery/Retreat Extension (+1)

### What
When a move **reveals an attack by a piece behind it** (discovered attack) or **retreats a piece from a discovered attack**, the search depth is extended by 1 ply.

### Why
Discovered attacks are among the most dangerous tactical patterns because they create **two threats simultaneously**: the moving piece's threat and the discovered piece's attack. The opponent can typically only deal with one, meaning the other wins material.

### How
```python
def trojan_discovery_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply for moves that create or respond to discovered attacks."""
    # Check if moving this piece reveals an attack from a friendly piece behind it
    from_sq = move.from_square
    piece = board.piece_at(from_sq)

    if piece is None:
        return DepthDelta(delta=0, rule_name="trojan_discovery", reason="")

    # Simulate moving the piece and check for discovered attacks
    board.push(move)
    for direction in RAY_DIRECTIONS:
        # Look along the ray from the vacated square
        current = from_sq
        while True:
            current += direction
            if not (0 <= current <= 63):
                break
            p = board.piece_at(current)
            if p is not None:
                if p.color == piece.color and p.type in [BISHOP, ROOK, QUEEN]:
                    # Found a friendly slider that now has a clear ray
                    # Check if it attacks a valuable target
                    # ... (simplified: check if it gives check or attacks a piece)
                    if board.is_check() or has_valuable_target(board, current):
                        board.pop()
                        return DepthDelta(
                            delta=+1,
                            rule_name="trojan_discovery",
                            reason=f"Extending: {move_san(move)} creates a discovered attack by the {p.type.name}"
                        )
                break  # Ray blocked

    board.pop()
    return DepthDelta(delta=0, rule_name="trojan_discovery", reason="")
```

### When
- **Discovered checks**: The most dangerous type—e.g., Nd5+ revealing a bishop check.
- **Discovered attacks on queen**: The opponent must save the queen, allowing the moving piece to make a second threat.
- **Retreat discoveries**: Moving a piece back to reveal an attack behind it.

### Explanation
> "Extending by 1 ply because Nd5 creates a discovered attack—White's bishop on b3 now attacks Black's queen on g8, and the knight simultaneously threatens c7."

---

## Rule 6: Sniper Line Extension (+1)

### What
When a **long-range piece** (bishop, rook, queen) has a clear line (file, rank, or diagonal) to a valuable target, the search depth is extended by 1 ply.

### Why
A "sniper" piece aims at a target from a distance. The threat is not immediate (there may be pieces in the way), but if the line is cleared, the attack becomes devastating. This is a **latent threat** that deeper search can verify.

### How
```python
def sniper_line_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply when a move creates a sniper line to a valuable target."""
    piece = board.piece_at(move.from_square)
    if piece is None or piece.type not in [BISHOP, ROOK, QUEEN]:
        return DepthDelta(delta=0, rule_name="sniper_line", reason="")

    board.push(move)
    moved_piece = board.piece_at(move.to_square)

    # Check if this piece now has a clear or semi-clear line to a valuable target
    for direction in get_piece_directions(moved_piece.type):
        current = move.to_square + direction
        obstacles = 0
        while 0 <= current <= 63:
            p = board.piece_at(current)
            if p is not None:
                if p.color != moved_piece.color and p.type in [QUEEN, ROOK, KING]:
                    # Found a valuable target!
                    if obstacles == 0:
                        board.pop()
                        return DepthDelta(
                            delta=+1,
                            rule_name="sniper_line",
                            reason=f"Extending: {move_san(move)} places a {moved_piece.type.name} on a direct line to the enemy {p.type.name}"
                        )
                obstacles += 1
                if obstacles >= 2:
                    break  # Too blocked to be a real sniper line
            current += direction

    board.pop()
    return DepthDelta(delta=0, rule_name="sniper_line", reason="")
```

### When
- **Bishop batteries**: Two bishops on the same diagonal targeting the king.
- **Rook on open file**: A rook aligned with the enemy king with only one piece in the way.
- **Queen aiming at the king**: A queen with a clear diagonal to the castled king.

### Explanation
> "Extending by 1 ply because Re1 places the rook on the e-file with a clear line to Black's king on e8—only the e5 pawn blocks the attack."

---

## Rule 7: Forced Response Extension (+1)

### What
When the opponent has **only one legal move** (or all moves are effectively forced), the search depth is extended by 1 ply.

### Why
When the opponent's response is forced, the branching factor drops to 1. This means the extra ply costs almost nothing in computation but could reveal critical information. A forced sequence is essentially a **single extended line**, and the engine should follow it to its conclusion.

### How
```python
def forced_response_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply when the opponent's response is forced."""
    board.push(move)

    legal_moves = list(board.legal_moves())

    if len(legal_moves) == 1:
        board.pop()
        return DepthDelta(
            delta=+1,
            rule_name="forced_response",
            reason=f"Extending: after {move_san(move)}, the opponent has only one legal move—the position is forced"
        )

    # Also extend if all moves are essentially the same
    # (e.g., all king moves when in check)
    if board.is_check() and len(legal_moves) <= 2:
        board.pop()
        return DepthDelta(
            delta=+1,
            rule_name="forced_response",
            reason=f"Extending: after {move_san(move)}, the opponent is in check with only {len(legal_moves)} responses"
        )

    board.pop()
    return DepthDelta(delta=0, rule_name="forced_response", reason="")
```

### When
- **Zugzwang**: The opponent has no good moves (all moves worsen the position).
- **Forced check sequences**: When in check with only one escape square.
- **Pawn races**: Both sides must push their pawns.

### Explanation
> "Extending by 1 ply because after Qh7+, the only legal move is Kf8—the forcing sequence must be followed to its conclusion."

---

## Rule 8: Mate Threat Extension (+1)

### What
When a move creates a **threat of checkmate** (the opponent would be mated if they don't respond), the search depth is extended by 1 ply.

### Why
Mate threats are the most significant threats in chess. Missing a mate threat due to depth limitations is catastrophic. The engine must verify whether the mate threat is real and whether the opponent has adequate defenses.

### How
```python
def mate_threat_extension(board: Board, move: Move) -> DepthDelta:
    """Extend by 1 ply when a move creates a mate threat."""
    board.push(move)

    # Check if any of the opponent's responses leads to checkmate
    # (This is a simplified check—full implementation would use null-move)
    opponent_moves = list(board.legal_moves())

    if not opponent_moves:
        # Checkmate or stalemate already—no extension needed
        board.pop()
        return DepthDelta(delta=0, rule_name="mate_threat", reason="")

    # Check if the opponent must respond to avoid mate
    mate_threats = 0
    for response in opponent_moves[:5]:  # Check first 5 responses
        board.push(response)
        our_moves = list(board.legal_moves())
        for our_move in our_moves:
            if board.gives_check(our_move):
                board.push(our_move)
                if board.is_checkmate():
                    mate_threats += 1
                board.pop()
        board.pop()

    board.pop()

    if mate_threats >= 2:
        return DepthDelta(
            delta=+1,
            rule_name="mate_threat",
            reason=f"Extending: {move_san(move)} creates a serious mate threat—the opponent must find the right defense"
        )

    return DepthDelta(delta=0, rule_name="mate_threat", reason="")
```

### When
- **Back-rank mate threats**: A rook on the 8th rank with the enemy king trapped.
- **Smothered mate patterns**: Knight delivering mate with the king surrounded by its own pieces.
- **Sacrificial mate attacks**: Queen sacrifices leading to forced checkmate.

### Explanation
> "Extending by 1 ply because Qh7 creates a mate threat on h8—the opponent must defend precisely or face checkmate."

---

## Extension Interaction Rules

When multiple extensions fire simultaneously, the total extension is **capped** (see [[Safety and Control Rules]]). However, the interaction between extensions provides rich explainability:

```python
def compute_total_extension(board: Board, move: Move, context: SearchContext) -> DepthDelta:
    """
    Compute the total depth extension for a move by combining all rules.
    """
    deltas = []

    for rule in EXTENSION_RULES:
        delta = rule(board, move, context)
        if delta.delta != 0:
            deltas.append(delta)

    total_delta = min(sum(d.delta for d in deltas), MAX_EXTENSION_PER_MOVE)
    reasons = [d.reason for d in deltas if d.reason]

    combined_reason = "; ".join(reasons) if reasons else ""

    return DepthDelta(
        delta=total_delta,
        rule_name="combined_extensions",
        reason=combined_reason
    )
```

## Summary

Depth extensions are the engine's way of saying **"this line matters—follow it further."** Each extension is triggered by a specific chess principle, from the universal (check extension) to the subtle (sniper line). Together, they ensure that the engine's search effort is concentrated on the most important lines, and each one carries a human-readable explanation of why it was granted.

---

**See also:** [[The Depther Philosophy]], [[Depth Reduction Rules]], [[Safety and Control Rules]], [[Quiescence Termination Rules]], [[The Depth Rules Module (Code Architecture)]], [[Alpha-Beta Search]], [[Horizon Effect]]
