# Piece-Square Tables

> "A knight on the rim is dim." — Chess proverb

## What Are Piece-Square Tables?

[[Piece-Square Tables]] (PSTs) are the simplest form of **positional knowledge** encoded in a chess engine. A PST assigns a bonus or penalty to every piece on every square, capturing the heuristic that "some squares are better than others for certain pieces." A knight in the center is powerful; a knight on the edge is often wasted. A rook on an open file is valuable; a rook buried behind its own pawns is not.

Formally, for a piece $p$ on square $s$, the PST value is:

$$
PST(p, s) \in [-50, +50] \text{ centipawns}
$$

PSTs are the **most cost-effective** evaluation term: a single array lookup ($O(1)$) encodes a significant amount of positional wisdom. They are also the most **explainable** positional feature: we can directly tell the user "the knight on d4 gets a +30 bonus because centralized knights are strong."

## Design Philosophy

PSTs encode the following principles:

1. **Centralization**: Pieces in the center control more squares and are more flexible.
2. **Advancement**: Pawns are worth more as they advance toward promotion.
3. **King Safety**: In the middlegame, the king should shelter behind pawns; in the endgame, it should activate.
4. **Development**: Pieces on their starting squares get penalties to encourage development.

Each PST is an 8×8 matrix indexed by square (a1=0 to h8=63). The values are hand-tuned based on chess theory and refined through self-play testing.

## Full Piece-Square Tables

### Pawn PST

Pawns gain value as they advance. Center pawns (d, e) are more valuable than wing pawns (a, h). Rank 7 pawns (about to promote) get the largest bonus.

```python
PAWN_PST_MG = [
    #   a    b    c    d    e    f    g    h
      [   0,   0,   0,   0,   0,   0,   0,   0],  # rank 1 (impossible)
      [   5,  10,  10, -20, -20,  10,  10,   5],  # rank 2 (starting)
      [   5,  -5, -10,   0,   0, -10,  -5,   5],  # rank 3
      [   0,   0,   0,  20,  20,   0,   0,   0],  # rank 4
      [   5,   5,  10,  25,  25,  10,   5,   5],  # rank 5
      [  10,  10,  20,  30,  30,  20,  10,  10],  # rank 6
      [  50,  50,  50,  50,  50,  50,  50,  50],  # rank 7 (one step from promo)
      [   0,   0,   0,   0,   0,   0,   0,   0],  # rank 8 (promoted)
]
```

**Explanation**: The d4/e4 squares get +20 at rank 4 because central pawns control key squares. The -20 at rank 2 for d/e reflects the cost of pushing center pawns prematurely without development.

### Knight PST

Knights are at their best in the center and on outposts (rank 5, c4-c6, f4-f6). On the rim, they control fewer squares and are vulnerable.

```python
KNIGHT_PST_MG = [
    #   a    b    c    d    e    f    g    h
      [ -50, -40, -30, -30, -30, -30, -40, -50],  # rank 1
      [ -40, -20,   0,   5,   5,   0, -20, -40],  # rank 2
      [ -30,   5,  10,  15,  15,  10,   5, -30],  # rank 3
      [ -30,   0,  15,  20,  20,  15,   0, -30],  # rank 4
      [ -30,   5,  15,  20,  20,  15,   5, -30],  # rank 5
      [ -30,   0,  10,  15,  15,  10,   0, -30],  # rank 6
      [ -40, -20,   0,   0,   0,   0, -20, -40],  # rank 7
      [ -50, -40, -30, -30, -30, -30, -40, -50],  # rank 8
]
```

**Explanation**: The knight on d4/d5/e4/e5 gets +20, reflecting the proverb "a knight on the rim is dim" with -50 for corner knights.

### Bishop PST

Bishops want open diagonals. They prefer central squares that give them the most diagonal reach. Fianchetto positions (b2/g2 for White) also receive bonuses.

```python
BISHOP_PST_MG = [
    #   a    b    c    d    e    f    g    h
      [ -20, -10, -10, -10, -10, -10, -10, -20],  # rank 1
      [ -10,   5,   0,   0,   0,   0,   5, -10],  # rank 2
      [ -10,  10,  10,  10,  10,  10,  10, -10],  # rank 3
      [ -10,   0,  10,  10,  10,  10,   0, -10],  # rank 4
      [ -10,   5,   5,  10,  10,   5,   5, -10],  # rank 5
      [ -10,   0,   5,  10,  10,   5,   0, -10],  # rank 6
      [ -10,   0,   0,   0,   0,   0,   0, -10],  # rank 7
      [ -20, -10, -10, -10, -10, -10, -10, -20],  # rank 8
]
```

### Rook PST

Rooks want to be on open files and on the 7th rank (rank 7 for White). They are neutral about horizontal position since their power depends on file openness, which PSTs don't capture directly (that's handled by [[Mobility and Piece Activity|mobility]] evaluation).

```python
ROOK_PST_MG = [
    #   a    b    c    d    e    f    g    h
      [   0,   0,   0,   5,   5,   0,   0,   0],  # rank 1
      [  -5,   0,   0,   0,   0,   0,   0,  -5],  # rank 2
      [  -5,   0,   0,   0,   0,   0,   0,  -5],  # rank 3
      [  -5,   0,   0,   0,   0,   0,   0,  -5],  # rank 4
      [  -5,   0,   0,   0,   0,   0,   0,  -5],  # rank 5
      [  -5,   0,   0,   0,   0,   0,   0,  -5],  # rank 6
      [   5,  10,  10,  10,  10,  10,  10,   5],  # rank 7 (7th rank!)
      [   0,   0,   0,   0,   0,   0,   0,   0],  # rank 8
]
```

### Queen PST

The queen is powerful everywhere but is discouraged from advancing too early (common beginner mistake). She belongs behind her pieces in the early game.

```python
QUEEN_PST_MG = [
    #   a    b    c    d    e    f    g    h
      [ -20, -10, -10,  -5,  -5, -10, -10, -20],  # rank 1
      [ -10,   0,   5,   0,   0,   0,   0, -10],  # rank 2
      [ -10,   5,   5,   5,   5,   5,   0, -10],  # rank 3
      [   0,   0,   5,   5,   5,   5,   0,  -5],  # rank 4
      [  -5,   0,   5,   5,   5,   5,   0,  -5],  # rank 5
      [ -10,   0,   5,   5,   5,   5,   0, -10],  # rank 6
      [ -10,   0,   0,   0,   0,   0,   0, -10],  # rank 7
      [ -20, -10, -10,  -5,  -5, -10, -10, -20],  # rank 8
]
```

### King Middlegame PST

The king should shelter in the corner, behind pawns. The classic castled position (g1 for White) gets a bonus.

```python
KING_PST_MG = [
    #   a    b    c    d    e    f    g    h
      [  20,  30,  10,   0,   0,  10,  30,  20],  # rank 1
      [  20,  20,   0,   0,   0,   0,  20,  20],  # rank 2
      [ -10, -20, -20, -20, -20, -20, -20, -10],  # rank 3
      [ -20, -30, -30, -40, -40, -30, -30, -20],  # rank 4
      [ -30, -40, -40, -50, -50, -40, -40, -30],  # rank 5
      [ -30, -40, -40, -50, -50, -40, -40, -30],  # rank 6
      [ -30, -40, -40, -50, -50, -40, -40, -30],  # rank 7
      [ -30, -40, -40, -50, -50, -40, -40, -30],  # rank 8
]
```

### King Endgame PST

In the endgame, the king must activate! Centralized kings are powerful, both for attack and defense.

```python
KING_PST_EG = [
    #   a    b    c    d    e    f    g    h
      [ -50, -30, -30, -30, -30, -30, -30, -50],  # rank 1
      [ -30, -30,   0,   0,   0,   0, -30, -30],  # rank 2
      [ -30, -10,  20,  30,  30,  20, -10, -30],  # rank 3
      [ -30, -10,  30,  40,  40,  30, -10, -30],  # rank 4
      [ -30, -10,  30,  40,  40,  30, -10, -30],  # rank 5
      [ -30, -10,  20,  30,  30,  20, -10, -30],  # rank 6
      [ -30, -20, -10,   0,   0, -10, -20, -30],  # rank 7
      [ -50, -30, -30, -30, -30, -30, -30, -50],  # rank 8
]
```

## The Mirror Trick for Black

All PSTs above are defined from White's perspective (rank 1 at bottom). For Black, we **mirror vertically**: a Black pawn on e7 uses the same table as a White pawn on e2. This works because chess is symmetric—what's good for White on rank $r$ is good for Black on rank $(9 - r)$.

```python
def pst_value(piece_type: PieceType, square: int, color: Color, phase: float) -> int:
    """
    Look up PST value for a piece on a given square.
    For Black, mirror the square vertically.
    Interpolate between middlegame and endgame tables.
    """
    rank = square // 8  # 0-7
    file = square % 8   # 0-7

    # Mirror for Black: rank 0 → rank 7, etc.
    if color == BLACK:
        rank = 7 - rank

    # Get middlegame and endgame tables
    mg_table = PST_MG[piece_type]
    eg_table = PST_EG.get(piece_type, mg_table)  # most pieces share MG/EG

    mg_value = mg_table[rank][file]
    eg_value = eg_table[rank][file]

    # Interpolate based on game phase
    return int(mg_value * phase + eg_value * (1.0 - phase))
```

## PST Evaluation for All Pieces

```python
def evaluate_pst(board: Board, phase: float) -> Tuple[int, List[EvalTerm]]:
    """
    Sum PST values for all pieces on the board.
    Returns total score (White-positive) and list of EvalTerms.
    """
    score = 0
    terms = []

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None:
            continue

        value = pst_value(piece.type, square, piece.color, phase)
        if piece.color == WHITE:
            score += value
        else:
            score -= value

    # Generate summary terms (not per-piece, for brevity)
    if score != 0:
        side = "White" if score > 0 else "Black"
        terms.append(EvalTerm(
            name="Piece Positioning",
            value=score,
            reason=f"{side}'s pieces are better positioned (+{abs(score)} cp from piece-square tables)",
            priority=3
        ))

    return score, terms
```

## PSTs as Explainable Knowledge

The key insight for our [[Explainable Chess Engine]] project: **PSTs are the simplest form of explainable positional knowledge.** Each table entry corresponds to a chess principle:

- "Knights belong in the center" → `KNIGHT_PST_MG[3][3] = +20` (d4)
- "Rooks belong on the 7th rank" → `ROOK_PST_MG[6][x] = +10`
- "The king should castle" → `KING_PST_MG[0][6] = +30` (g1)
- "Pawns gain value as they advance" → `PAWN_PST_MG[6][x] = +50`

When the engine explains a move, it can reference these principles:

> "The knight moves to d4 because centralized knights control more squares and are harder to dislodge. This improves the position by +20 centipawns according to piece-square tables."

This is far more informative than a neural network's opaque score adjustment.

## Tuning PSTs

While hand-tuned PSTs work well, modern engines use **automated tuning** methods:

1. **Texel Tuning**: Optimize PST values by minimizing prediction error on a dataset of game outcomes.
2. **SPSA (Simultaneous Perturbation Stochastic Approximation)**: A gradient-free optimization method that perturbs parameters and measures performance.
3. **Genetic Algorithms**: Evolve PST populations toward better evaluation accuracy.

Our engine uses hand-tuned values as a starting point, with plans for Texel Tuning integration. The tuning process itself must remain explainable—we log which values changed and by how much.

---

**See also:** [[Static Evaluation Overview]], [[Material Evaluation]], [[Pawn Structure Evaluation]], [[King Safety Evaluation]], [[Mobility and Piece Activity]], [[Threats and Tactical Patterns]], [[Endgame Scaling]], [[Texel Tuning]]
