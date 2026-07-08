# Threats and Tactical Patterns

> "Tactics flow from a superior position." — Bobby Fischer

## The Bridge Between Strategy and Tactics

All the evaluation terms we've discussed so far—[[Material Evaluation]], [[Piece-Square Tables]], [[Pawn Structure Evaluation]], [[King Safety Evaluation]], [[Mobility and Piece Activity]]—are **strategic**. They assess long-term, slow-moving features of the position. But chess is ultimately decided by **tactics**: the concrete, forcing sequences that win material, deliver checkmate, or gain decisive positional advantages.

[[Threats and Tactical Patterns]] evaluation bridges the gap between strategy and tactics. It asks: **Right now, what can be captured, attacked, or exploited?** Unlike strategic evaluation (which changes slowly), threat evaluation can swing wildly from move to move—a piece that was safe one move ago might now be hanging.

## Static vs. Dynamic Threat Detection

There are two approaches to threat detection:

### Static Threat Detection

Static threat detection examines the **current position** without searching ahead. It identifies patterns like "this piece is attacked and not defended" or "this piece is pinned." This is what the evaluation function does.

**Advantages**: Fast ($O(1)$ to $O(n^2)$), explainable, deterministic.
**Disadvantages**: Cannot detect multi-move combinations, silent threats, or deferred tactics.

### Dynamic Threat Detection

Dynamic threat detection uses **search** (even a shallow 1-2 ply search) to discover threats that are not immediately visible. This is what the [[Alpha-Beta Search]] and [[Quiescence Search]] do.

**Advantages**: Can detect complex combinations, silent threats, deferred tactics.
**Disadvantages**: Expensive, harder to explain (the "why" is embedded in the search tree).

Our engine uses **primarily static threat detection** in the evaluation function, supplemented by dynamic detection in the search. Every static threat generates an [[EvalTerm]] with an explanation.

## 1. Hanging Pieces (LPDO)

**LPDO** stands for **Loose Pieces Drop Off**—a term coined by Dan Heisman. A "loose" piece is one that is **not defended by any friendly piece**. If a loose piece is also **attacked** by an enemy piece, it is **hanging** and can be captured for free (or won via a combination).

LPDO is one of the most common tactical errors in amateur chess and one of the easiest to detect statically.

```python
def is_defended(board: Board, square: int, color: Color) -> bool:
    """
    Check if a piece on 'square' is defended by any friendly piece.
    A piece is defended if at least one friendly piece attacks its square.
    """
    # Check if any friendly piece attacks this square
    for sq in range(64):
        piece = board.piece_at(sq)
        if piece is None or piece.color != color:
            continue
        if sq == square:
            continue
        # Does this piece attack 'square'?
        attacks = board.attacks_from(sq)
        if (1 << square) & attacks:
            return True
    return False

def is_attacked(board: Board, square: int, by_color: Color) -> bool:
    """Check if a square is attacked by any piece of the given color."""
    for sq in range(64):
        piece = board.piece_at(sq)
        if piece is None or piece.color != by_color:
            continue
        attacks = board.attacks_from(sq)
        if (1 << square) & attacks:
            return True
    return False

HANGING_PIECE_PENALTY = {
    PAWN: -50,
    KNIGHT: -200,
    BISHOP: -200,
    ROOK: -300,
    QUEEN: -500,
}

def evaluate_hanging_pieces(board: Board) -> Tuple[int, List[EvalTerm]]:
    """
    Detect hanging pieces (attacked but not defended).
    These are immediate tactical liabilities.
    """
    terms = []
    score = 0

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None or piece.type == KING:
            continue

        enemy_color = BLACK if piece.color == WHITE else WHITE

        if not is_defended(board, square, piece.color) and is_attacked(board, square, enemy_color):
            # This piece is HANGING
            penalty = HANGING_PIECE_PENALTY.get(piece.type, -100)
            sign = 1 if piece.color == WHITE else -1
            score += sign * penalty

            terms.append(EvalTerm(
                name=f"Hanging {'White' if piece.color == WHITE else 'Black'} {piece.type.name}",
                value=sign * penalty,
                reason=f"The {piece.type.name} on {square_name(square)} is attacked but not defended—it can be captured!",
                priority=0  # Highest priority—immediate threat
            ))

    return score, terms
```

**Explanation**: *"Black's bishop on c5 is hanging—it's attacked by White's queen but not defended by any Black piece. It can be captured for free! (-200 cp)"*

## 2. Forks

A **fork** is a tactical pattern where one piece attacks two or more enemy pieces simultaneously. Knights and queens are the most common forking pieces.

Static fork detection checks whether a piece attacks two or more valuable enemy targets:

```python
def detect_forks(board: Board, square: int) -> List[str]:
    """
    Detect potential forks from a piece on 'square'.
    A fork exists when a piece attacks 2+ enemy pieces of sufficient value.
    """
    piece = board.piece_at(square)
    if piece is None:
        return []

    attacks = board.attacks_from(square)
    fork_targets = []

    for target_sq in range(64):
        if not ((1 << target_sq) & attacks):
            continue
        target = board.piece_at(target_sq)
        if target is None or target.color == piece.color:
            continue
        if target.type != PAWN:  # Forking pawns alone isn't interesting
            fork_targets.append(f"{target.type.name} on {square_name(target_sq)}")

    forks = []
    if len(fork_targets) >= 2:
        for i in range(len(fork_targets)):
            for j in range(i + 1, len(fork_targets)):
                forks.append(f"{piece.type.name} on {square_name(square)} forks {fork_targets[i]} and {fork_targets[j]}")

    return forks

FORK_BONUS = 50  # centipawns per fork

def evaluate_forks(board: Board) -> Tuple[int, List[EvalTerm]]:
    """Evaluate fork opportunities for both sides."""
    terms = []
    score = 0

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None:
            continue

        forks = detect_forks(board, square)
        for fork_desc in forks:
            bonus = FORK_BONUS
            sign = 1 if piece.color == WHITE else -1
            score += sign * bonus

            terms.append(EvalTerm(
                name="Fork",
                value=sign * bonus,
                reason=fork_desc,
                priority=1
            ))

    return score, terms
```

**Explanation**: *"White's knight on e5 forks Black's queen on d7 and rook on f7—Black cannot save both pieces (+50 cp)."*

## 3. Pins

A **pin** is a tactical pattern where a piece cannot move because doing so would expose a more valuable piece behind it. Pins are detected along rays (files, ranks, diagonals).

```python
def detect_pins(board: Board, square: int, color: Color) -> List[str]:
    """
    Detect pins where a piece on 'square' is pinned to a more valuable piece.
    A pin occurs when a sliding piece attacks through one enemy piece to a
    more valuable enemy piece behind it.
    """
    pins = []
    enemy_color = BLACK if color == WHITE else WHITE

    # Check all ray directions from the square
    for direction in DIRECTIONS:
        # Walk along the ray
        current = square
        first_piece = None
        second_piece = None

        while True:
            current = current + direction
            if not (0 <= current <= 63):
                break

            p = board.piece_at(current)
            if p is not None:
                if first_piece is None:
                    first_piece = (current, p)
                elif second_piece is None:
                    second_piece = (current, p)
                    break

        # Check if this is a pin
        if first_piece and second_piece:
            fp_sq, fp = first_piece
            sp_sq, sp = second_piece

            # First piece must be enemy, second piece must be same color as first
            if (fp.color == enemy_color and sp.color == enemy_color and
                PIECE_VALUES.get(sp.type, 0) > PIECE_VALUES.get(fp.type, 0)):
                pins.append(
                    f"{fp.type.name} on {square_name(fp_sq)} is pinned to "
                    f"{sp.type.name} on {square_name(sp_sq)} by "
                    f"{board.piece_at(square).type.name} on {square_name(square)}"
                )

    return pins

PIN_PENALTY = -30  # centipawns per pinned piece

def evaluate_pins(board: Board) -> Tuple[int, List[EvalTerm]]:
    """Evaluate pins for both sides."""
    terms = []
    score = 0

    # Check for pins by each sliding piece
    for square in range(64):
        piece = board.piece_at(square)
        if piece is None:
            continue
        if piece.type not in [BISHOP, ROOK, QUEEN]:
            continue

        pins = detect_pins(board, square, piece.color)
        for pin_desc in pins:
            sign = 1 if piece.color == WHITE else -1
            score += sign * abs(PIN_PENALTY)

            terms.append(EvalTerm(
                name="Pin",
                value=sign * abs(PIN_PENALTY),
                reason=pin_desc,
                priority=2
            ))

    return score, terms
```

**Explanation**: *"Black's knight on c6 is pinned to the king on e8 by White's bishop on a4—the knight cannot move without exposing the king to check (-30 cp for Black)."*

## 4. Skewers

A **skewer** is the inverse of a pin: the more valuable piece is in front, and moving it exposes a less valuable piece behind. Skewers win material because the front piece must move.

```python
def detect_skewers(board: Board, square: int, color: Color) -> List[str]:
    """
    Detect skewers where a sliding piece on 'square' forces a more valuable
    enemy piece to move, exposing a less valuable piece behind it.
    """
    skewers = []
    enemy_color = BLACK if color == WHITE else WHITE

    for direction in DIRECTIONS:
        current = square
        first_piece = None
        second_piece = None

        while True:
            current = current + direction
            if not (0 <= current <= 63):
                break

            p = board.piece_at(current)
            if p is not None:
                if first_piece is None:
                    first_piece = (current, p)
                elif second_piece is None:
                    second_piece = (current, p)
                    break

        if first_piece and second_piece:
            fp_sq, fp = first_piece
            sp_sq, sp = second_piece

            # Skewer: first piece is more valuable, second is less valuable
            if (fp.color == enemy_color and sp.color == enemy_color and
                PIECE_VALUES.get(fp.type, 0) > PIECE_VALUES.get(sp.type, 0)):
                skewers.append(
                    f"{board.piece_at(square).type.name} on {square_name(square)} "
                    f"skewers {fp.type.name} on {square_name(fp_sq)} and "
                    f"{sp.type.name} on {square_name(sp_sq)}"
                )

    return skewers

SKEWER_BONUS = 40  # centipawns per skewer

def evaluate_skewers(board: Board) -> Tuple[int, List[EvalTerm]]:
    """Evaluate skewer opportunities for both sides."""
    terms = []
    score = 0

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None or piece.type not in [BISHOP, ROOK, QUEEN]:
            continue

        skewers = detect_skewers(board, square, piece.color)
        for skewer_desc in skewers:
            sign = 1 if piece.color == WHITE else -1
            score += sign * SKEWER_BONUS

            terms.append(EvalTerm(
                name="Skewer",
                value=sign * SKEWER_BONUS,
                reason=skewer_desc,
                priority=2
            ))

    return score, terms
```

**Explanation**: *"White's rook on d1 skewers Black's queen on d8 and bishop on d5—when the queen moves, the bishop is lost (+40 cp)."*

## 5. Discovered Attacks

A **discovered attack** occurs when a piece moves off a line, revealing an attack by a friendly piece behind it. The moving piece can make a second threat (e.g., a check), creating a double attack that is very hard to defend.

```python
def detect_discovered_attacks(board: Board, square: int, color: Color) -> List[str]:
    """
    Detect potential discovered attacks.
    If the piece on 'square' moves off a ray, does a friendly sliding piece
    behind it gain an attack on a valuable target?
    """
    discoveries = []

    # Check if any friendly sliding piece is behind this piece on a ray
    for direction in DIRECTIONS:
        # Walk backward along the ray to find a friendly slider
        prev = square
        while True:
            prev = prev - direction
            if not (0 <= prev <= 63):
                break
            p = board.piece_at(prev)
            if p is not None:
                if p.color == color and p.type in [BISHOP, ROOK, QUEEN]:
                    # Found a friendly slider behind us
                    # Now check what it would attack if we moved
                    ray_target = square + direction
                    while 0 <= ray_target <= 63:
                        target = board.piece_at(ray_target)
                        if target is not None:
                            if target.color != color and target.type in [QUEEN, ROOK, KING]:
                                discoveries.append(
                                    f"Moving {board.piece_at(square).type.name} from "
                                    f"{square_name(square)} discovers an attack by "
                                    f"{p.type.name} on {square_name(prev)} against "
                                    f"{target.type.name} on {square_name(ray_target)}"
                                )
                            break
                        ray_target += direction
                break  # Found a piece (blocked the ray)

    return discoveries

DISCOVERED_ATTACK_BONUS = 45

def evaluate_discovered_attacks(board: Board) -> Tuple[int, List[EvalTerm]]:
    """Evaluate discovered attack opportunities."""
    terms = []
    score = 0

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None:
            continue

        discoveries = detect_discovered_attacks(board, square, piece.color)
        for disc_desc in discoveries:
            sign = 1 if piece.color == WHITE else -1
            score += sign * DISCOVERED_ATTACK_BONUS
            terms.append(EvalTerm(
                name="Discovered Attack",
                value=sign * DISCOVERED_ATTACK_BONUS,
                reason=disc_desc,
                priority=1
            ))

    return score, terms
```

**Explanation**: *"White can play Nd5!, moving the knight off the d-file to discover a rook attack on Black's queen on d8 (+45 cp)."*

## Complete Threat Evaluation

```python
def evaluate_threats(board: Board) -> Tuple[int, List[EvalTerm]]:
    """
    Full threat evaluation combining all tactical patterns.
    Returns (score, terms) where score is White-positive.
    """
    all_terms = []
    total = 0

    # Hanging pieces (highest priority)
    h_score, h_terms = evaluate_hanging_pieces(board)
    total += h_score
    all_terms.extend(h_terms)

    # Forks
    f_score, f_terms = evaluate_forks(board)
    total += f_score
    all_terms.extend(f_terms)

    # Pins
    p_score, p_terms = evaluate_pins(board)
    total += p_score
    all_terms.extend(p_terms)

    # Skewers
    s_score, s_terms = evaluate_skewers(board)
    total += s_score
    all_terms.extend(s_terms)

    # Discovered attacks
    d_score, d_terms = evaluate_discovered_attacks(board)
    total += d_score
    all_terms.extend(d_terms)

    return total, all_terms
```

## The Limitation of Static Threat Detection

It is crucial to understand what static threat detection **cannot** do:

1. **Multi-move combinations**: A sacrifice that wins material two moves later is invisible to static evaluation.
2. **Silent threats**: A piece that is safe now but will be trapped next move if it moves.
3. **Zwischenzugs**: Intermediate moves that change the evaluation of a threat.
4. **Defensive resources**: The opponent may have a way to parry the threat that static analysis doesn't see.

This is why the [[Alpha-Beta Search]] and [[Quiescence Search]] are essential: they explore the consequences of threats and verify whether they actually win material. The static evaluation provides the **initial assessment**; the search provides the **verification**.

In our explainable engine, we clearly distinguish between these two levels of analysis:

> **Static assessment**: "Black's bishop on c5 is hanging and can be captured for free."
> **Search verification**: "After 1.Qxc5, Black plays 1...Qd1+ 2.Kh2 Qxd4 with counterplay, so the capture only nets +30 cp, not +200 cp."

---

**See also:** [[Static Evaluation Overview]], [[King Safety Evaluation]], [[Mobility and Piece Activity]], [[Alpha-Beta Search]], [[Quiescence Search]], [[LPDO]], [[Fork]], [[Pin]], [[Skewer]], [[Discovered Attack]]
