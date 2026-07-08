# Mobility and Piece Activity

> "The mobility of the pieces is the most important factor in chess." — Aron Nimzowitsch

## The Principle of Activity

A piece's value is not fixed—it depends on how **active** it is. A bishop trapped behind its own pawns ("bad bishop") is worth far less than a bishop sweeping across open diagonals. A rook on a closed file is inferior to a rook on an open file. [[Mobility and Piece Activity]] evaluation captures this principle: **the more squares a piece can reach, the more valuable it is**.

Mobility is one of the most computationally expensive [[Static Evaluation Overview|evaluation terms]] because it requires counting legal moves or pseudo-legal moves for each piece. However, it provides critical positional assessment that simpler terms like [[Material Evaluation]] and [[Piece-Square Tables]] cannot.

## Defining Mobility

Mobility is measured as the number of squares a piece can move to (or attack). We distinguish between:

1. **Real mobility**: Squares the piece can legally move to (accounts for pins, check).
2. **Pseudo-legal mobility**: Squares the piece can move to ignoring pins and check.
3. **Attack mobility**: Squares the piece controls (includes squares occupied by enemy pieces that can be captured).

For efficiency, most engines use **pseudo-legal mobility** in the evaluation function. The difference from real mobility is small in most positions, and computing real mobility requires checking for pins and checks—which is expensive.

```python
def piece_mobility(board: Board, square: int) -> int:
    """
    Count the number of squares a piece on 'square' can move to.
    Uses pseudo-legal move generation for speed.
    """
    piece = board.piece_at(square)
    if piece is None:
        return 0

    moves = board.pseudo_legal_moves_from(square)
    return len(moves)
```

## Piece-Specific Mobility Evaluation

Different pieces benefit from mobility in different ways. Our engine evaluates each piece type with specific heuristics.

### Knight Mobility and Outposts

Knights are **short-range** pieces. Their mobility is inherently limited, so each additional move is proportionally more valuable. The key concept for knights is the **outpost**—a square on the opponent's side of the board, protected by a friendly pawn, that cannot be attacked by an enemy pawn. A knight on an outpost is a dominant positional asset.

```python
def is_outpost(square: int, color: Color, board: Board) -> bool:
    """
    Check if a square is an outpost for the given color.
    An outpost is:
    1. On the opponent's half of the board (ranks 4-6 for White, 3-5 for Black)
    2. Protected by a friendly pawn
    3. Cannot be attacked by an enemy pawn
    """
    rank = square // 8
    file = square % 8

    # Must be on opponent's half
    if color == WHITE and rank < 4:
        return False
    if color == BLACK and rank > 3:
        return False

    # Must be protected by a friendly pawn
    protected = False
    pawn_protect_rank = rank - 1 if color == WHITE else rank + 1
    for df in [-1, 1]:
        pf = file + df
        if 0 <= pf <= 7 and 0 <= pawn_protect_rank <= 7:
            prot_sq = pawn_protect_rank * 8 + pf
            p = board.piece_at(prot_sq)
            if p and p.type == PAWN and p.color == color:
                protected = True
                break

    if not protected:
        return False

    # Must NOT be attackable by an enemy pawn
    enemy_color = BLACK if color == WHITE else WHITE
    pawn_attack_rank = rank + 1 if color == WHITE else rank - 1
    for df in [-1, 1]:
        pf = file + df
        if 0 <= pf <= 7 and 0 <= pawn_attack_rank <= 7:
            atk_sq = pawn_attack_rank * 8 + pf
            p = board.piece_at(atk_sq)
            if p and p.type == PAWN and p.color == enemy_color:
                return False  # Enemy pawn can attack this square

    return True

KNIGHT_OUTPOST_BONUS = 45  # centipawns
KNIGHT_MOBILITY_BONUS = 4  # per legal move

def evaluate_knight_activity(board: Board, square: int, color: Color) -> Tuple[int, str]:
    """Evaluate a knight's activity based on mobility and outpost status."""
    score = 0
    reasons = []

    # Mobility
    moves = board.pseudo_legal_moves_from(square)
    mobility = len(moves)
    score += mobility * KNIGHT_MOBILITY_BONUS
    if mobility >= 6:
        reasons.append(f"active knight with {mobility} moves")

    # Outpost
    if is_outpost(square, color, board):
        score += KNIGHT_OUTPOST_BONUS
        reasons.append("stationed on a protected outpost")

    reason = "; ".join(reasons) if reasons else "limited activity"
    return score, reason
```

**Explanation**: *"White's knight on d5 is on a powerful outpost—protected by the c4 pawn and impossible for Black pawns to challenge (+45 cp)."*

### Bishop Mobility and Diagonals

Bishops are **long-range** pieces. A bishop on an open diagonal can control 7-13 squares, making it extremely powerful. Conversely, a bishop trapped behind its own pawns on the wrong color complex is a "bad bishop."

```python
BISHOP_MOBILITY_BONUS = 3  # per legal move
BAD_BISHOP_PENALTY = -30    # bishop blocked by own pawns

def evaluate_bishop_activity(board: Board, square: int, color: Color) -> Tuple[int, str]:
    """Evaluate a bishop's activity based on mobility and diagonal access."""
    score = 0
    reasons = []

    # Mobility
    moves = board.pseudo_legal_moves_from(square)
    mobility = len(moves)
    score += mobility * BISHOP_MOBILITY_BONUS
    if mobility >= 8:
        reasons.append(f"strong diagonal control with {mobility} moves")

    # Bad bishop check: are own pawns on the bishop's color complex?
    bishop_color = (square + (square // 8)) % 2  # 0 = light, 1 = dark
    own_pawns_on_color = 0
    for sq in board.get_pawns(color):
        if (sq + (sq // 8)) % 2 == bishop_color:
            own_pawns_on_color += 1

    if own_pawns_on_color >= 3:
        # Many own pawns on same color = bad bishop
        score += BAD_BISHOP_PENALTY
        reasons.append(f"bad bishop blocked by {own_pawns_on_color} own pawns on same color")
    elif mobility >= 8:
        reasons.append("excellent diagonal activity")

    reason = "; ".join(reasons) if reasons else "moderate activity"
    return score, reason
```

**Explanation**: *"White's light-squared bishop is a 'bad bishop'—4 of White's own pawns sit on light squares, blocking its diagonals (-30 cp)."*

### Rook Mobility and Files

Rooks are most powerful on **open files** (no pawns), **semi-open files** (only enemy pawns), and on the **7th rank** (rank 7 for White, rank 2 for Black). Rook mobility is primarily about file access.

```python
ROOK_ON_OPEN_FILE_BONUS = 40
ROOK_ON_SEMI_OPEN_FILE_BONUS = 20
ROOK_ON_7TH_RANK_BONUS = 50
ROOK_MOBILITY_BONUS = 2  # per legal move

def evaluate_rook_activity(board: Board, square: int, color: Color) -> Tuple[int, str]:
    """Evaluate a rook's activity based on file access, rank, and mobility."""
    score = 0
    reasons = []
    rank = square // 8
    file = square % 8

    # Mobility
    moves = board.pseudo_legal_moves_from(square)
    mobility = len(moves)
    score += mobility * ROOK_MOBILITY_BONUS

    # Open file
    own_pawns_on_file = board.count_pawns_on_file(color, file)
    enemy_pawns_on_file = board.count_pawns_on_file(
        BLACK if color == WHITE else WHITE, file
    )

    if own_pawns_on_file == 0 and enemy_pawns_on_file == 0:
        score += ROOK_ON_OPEN_FILE_BONUS
        reasons.append("on an open file")
    elif own_pawns_on_file == 0 and enemy_pawns_on_file > 0:
        score += ROOK_ON_SEMI_OPEN_FILE_BONUS
        reasons.append("on a semi-open file")

    # 7th rank
    if (color == WHITE and rank == 6) or (color == BLACK and rank == 1):
        score += ROOK_ON_7TH_RANK_BONUS
        reasons.append("dominating the 7th rank")

    if not reasons:
        if mobility >= 10:
            reasons.append("high mobility")
        else:
            reasons.append("limited activity")

    reason = "; ".join(reasons)
    return score, reason
```

**Explanation**: *"White's rook on d1 controls the semi-open d-file and can pressure Black's d5 pawn (+20 cp)."*

### Queen Mobility

Queens are powerful everywhere, so mobility evaluation is simpler. The main concern is that the queen should not be **underdeveloped** (still on d1/d8 with pieces behind it).

```python
QUEEN_MOBILITY_BONUS = 1  # per legal move (lower marginal value, queen already strong)
QUEEN_EARLY_DEVELOPMENT_PENALTY = -30

def evaluate_queen_activity(board: Board, square: int, color: Color,
                            move_number: int) -> Tuple[int, str]:
    """Evaluate queen activity with early development penalty."""
    score = 0
    reasons = []

    # Mobility
    moves = board.pseudo_legal_moves_from(square)
    mobility = len(moves)
    score += mobility * QUEEN_MOBILITY_BONUS

    # Early queen development penalty
    if move_number < 10:
        rank = square // 8
        if (color == WHITE and rank >= 4) or (color == BLACK and rank <= 3):
            score += QUEEN_EARLY_DEVELOPMENT_PENALTY
            reasons.append("developed too early—vulnerable to harassment")

    if not reasons:
        reasons.append(f"mobile with {mobility} moves")

    reason = "; ".join(reasons)
    return score, reason
```

## Complete Mobility Evaluation

```python
def evaluate_mobility(board: Board) -> Tuple[int, List[EvalTerm]]:
    """
    Full mobility evaluation for both sides.
    Returns (score, terms) where score is White-positive.
    """
    terms = []
    score = 0

    for color in [WHITE, BLACK]:
        sign = 1 if color == WHITE else -1
        color_terms = {}

        for square in range(64):
            piece = board.piece_at(square)
            if piece is None or piece.color != color:
                continue

            if piece.type == KNIGHT:
                val, reason = evaluate_knight_activity(board, square, color)
            elif piece.type == BISHOP:
                val, reason = evaluate_bishop_activity(board, square, color)
            elif piece.type == ROOK:
                val, reason = evaluate_rook_activity(board, square, color)
            elif piece.type == QUEEN:
                val, reason = evaluate_queen_activity(board, square, color, board.fullmove_number)
            else:
                continue  # Pawns and kings handled elsewhere

            # Aggregate by piece type for summary
            key = f"{'White' if color == WHITE else 'Black'} {piece.type.name}"
            if key not in color_terms:
                color_terms[key] = [0, []]
            color_terms[key][0] += val
            color_terms[key][1].append(f"{square_name(square)}: {reason}")

        for key, (val, details) in color_terms.items():
            if val != 0:
                score += sign * val
                terms.append(EvalTerm(
                    name=f"{key} Activity",
                    value=sign * val,
                    reason=details[0] if len(details) == 1 else f"{len(details)} pieces contributing",
                    priority=4
                ))

    return score, terms
```

## The Trade-Off: Accuracy vs. Speed

Mobility evaluation is the **most expensive** term in our evaluation function. Counting pseudo-legal moves for each piece requires traversing attack rays and generating move lists. On a position with 20 pieces, this means roughly 15-18 mobility calculations, each requiring ray traversal.

Optimization strategies:

1. **Incremental mobility**: When a move is made, only recalculate mobility for the moved piece and any pieces whose rays were affected.
2. **Approximate mobility**: Use precomputed attack tables to estimate mobility without full move generation.
3. **Skip in time trouble**: If the search time budget is running low, disable mobility evaluation and rely on cheaper terms.

```python
def should_evaluate_mobility(time_remaining_ms: int, depth: int) -> bool:
    """Decide whether to include mobility in evaluation based on time budget."""
    # At shallow depths or with ample time, always evaluate
    if depth <= 4 or time_remaining_ms > 5000:
        return True
    # At deep depths with tight time, skip for speed
    if time_remaining_ms < 1000:
        return False
    return True
```

## Summary

Mobility evaluation transforms the engine from a materialist into a **positionalist**. It understands that a well-placed knight on an outpost can be worth more than a poorly placed bishop, that a rook on an open file is a weapon, and that a bad bishop is a liability. Each of these insights is directly **explainable**: the engine can tell you *why* a piece is well-placed, not just that it is.

---

**See also:** [[Static Evaluation Overview]], [[Material Evaluation]], [[Piece-Square Tables]], [[King Safety Evaluation]], [[Threats and Tactical Patterns]], [[Bad Bishop]], [[Outpost]], [[Open File]], [[7th Rank]]
