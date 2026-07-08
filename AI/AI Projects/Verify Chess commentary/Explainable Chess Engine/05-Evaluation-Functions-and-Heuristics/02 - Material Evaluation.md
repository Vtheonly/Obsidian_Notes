# Material Evaluation

> "In chess, material is the most important factor. The player with more material wins—eventually."
> — Wilhelm Steinitz

## The Foundation of All Evaluation

[[Material Evaluation]] is the single most important term in the [[Static Evaluation Overview|static evaluation function]]. It answers the simplest question in chess: **who has more stuff?** While positional factors can compensate for material deficits, material advantage is the most reliable predictor of game outcomes. Studies of master games show that a one-pawn advantage converts to a win approximately 80% of the time, and a two-pawn advantage over 95%.

Material evaluation is computed as the **difference in total piece values** between White and Black:

$$
M = \sum_{p \in \text{White pieces}} V(p) - \sum_{p \in \text{Black pieces}} V(p)
$$

where $V(p)$ is the standard value of piece $p$ in centipawns.

## Standard Piece Values

The conventional piece values in centipawns, as used in our engine:

| Piece | Symbol | Value (cp) | Relative to Pawn |
|-------|--------|------------|-------------------|
| Pawn | P | 100 | 1.00× |
| Knight | N | 320 | 3.20× |
| Bishop | B | 330 | 3.30× |
| Rook | R | 500 | 5.00× |
| Queen | Q | 900 | 9.00× |
| King | K | ∞ | — |

### Why These Specific Values?

These numbers are not arbitrary—they emerge from decades of statistical analysis of grandmaster games and computer self-play:

- **Pawn = 100**: By definition. The centipawn unit is 1/100th of a pawn, making it the natural base unit.
- **Knight = 320**: Knights are worth slightly more than 3 pawns. Their unique L-shaped movement makes them strong in closed positions but weak on open boards. The 320 value (vs. the older 300) reflects modern understanding that knights are slightly stronger than the traditional "3 pawns" estimate in typical positions.
- **Bishop = 330**: Bishops are marginally stronger than knights in most positions due to their long-range capabilities. The 10-centipawn difference (330 vs 320) is small but statistically significant. This difference grows in open positions and shrinks in closed ones.
- **Rook = 500**: The rook's value of 5 pawns reflects its power on open files and ranks. The **exchange** (rook for minor piece) is worth roughly 170-180 centipawns, a significant but not overwhelming advantage.
- **Queen = 900**: The queen combines the powers of rook and bishop. Its value (9 pawns) is less than rook + bishop + pawn (930), reflecting that a queen can sometimes be awkward against multiple pieces that cooperate.

The king has no finite value because losing the king ends the game. In implementation, we simply never include the king in material counts.

## Python Implementation

```python
from enum import IntEnum
from typing import Dict, List, Tuple

class PieceType(IntEnum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

# Standard piece values in centipawns
PIECE_VALUES: Dict[PieceType, int] = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 0,  # King is invaluable; not counted in material
}

def material_balance(white_pieces: List[PieceType], black_pieces: List[PieceType]) -> int:
    """
    Compute material balance in centipawns.
    Positive = White has more material.
    Negative = Black has more material.
    """
    white_total = sum(PIECE_VALUES[p] for p in white_pieces)
    black_total = sum(PIECE_VALUES[p] for p in black_pieces)
    return white_total - black_total

def material_count(pieces: List[PieceType]) -> int:
    """Total material value of a list of pieces (excluding kings)."""
    return sum(PIECE_VALUES[p] for p in pieces if p != PieceType.KING)
```

## The Bishop Pair Bonus

Having **both bishops** (the "bishop pair") is significantly stronger than having two bishops of different types would suggest individually. The bishop pair bonus is one of the most well-established evaluation terms in chess programming:

- Each bishop covers only half the squares (light or dark). Together, they cover the entire board.
- The bishop pair creates tactical threats that a single bishop cannot—especially long-range double attacks.
- Statistical analysis shows the bishop pair is worth approximately **50 centipawns** (half a pawn) above the sum of the two individual bishop values.

```python
BISHOP_PAIR_BONUS = 50  # centipawns

def bishop_pair_bonus(white_bishops: int, black_bishops: int) -> int:
    """
    Return bishop pair bonus.
    Only awarded if a side has BOTH bishops remaining.
    """
    bonus = 0
    if white_bishops >= 2:
        bonus += BISHOP_PAIR_BONUS
    if black_bishops >= 2:
        bonus -= BISHOP_PAIR_BONUS
    return bonus
```

**Explainability note**: When the bishop pair bonus fires, we generate the reason: *"White benefits from the bishop pair, covering both light and dark squares (+50 cp)."*

## Material Imbalance

Material imbalance goes beyond simple counting. The relative value of pieces **changes depending on what other pieces are on the board**. Key imbalance principles:

### 1. Two Minor Pieces vs. Rook + Pawns
Two minor pieces (N+B = 650 cp) are typically stronger than a rook and a pawn (600 cp). The minor pieces cooperate better and can dominate the rook in the middlegame.

### 2. Queen vs. Two Rooks
A queen (900 cp) is roughly equivalent to two rooks (1000 cp) in the middlegame, but the rooks gain an edge in the endgame when they can coordinate on open files.

### 3. Three Pawns vs. Minor Piece
Three pawns (300 cp) are roughly equivalent to a minor piece (320-330 cp) in the endgame, but in the middlegame the minor piece is almost always preferable.

### 4. Rook vs. Minor Piece + Two Pawns
This is the classic "exchange sacrifice" scenario. The rook (500) vs. minor piece + 2 pawns (520-530) is nearly balanced in material, but positional context determines the true value.

```python
# Imbalance table: (piece_type, opponent_piece_type) -> bonus/penalty
IMBALANCE_TABLE: Dict[Tuple[PieceType, PieceType], int] = {
    # Having knights when opponent has no bishops
    (PieceType.KNIGHT, PieceType.BISHOP): 10,
    # Having bishops when opponent has no knights
    (PieceType.BISHOP, PieceType.KNIGHT): 15,
    # Having rooks when opponent has queens (rooks gain value in Q+R vs 2R)
    (PieceType.ROOK, PieceType.QUEEN): 20,
    # Having queens when opponent has minor pieces only
    (PieceType.QUEEN, PieceType.KNIGHT): -10,
    (PieceType.QUEEN, PieceType.BISHOP): -10,
}

def material_imbalance(
    white_piece_counts: Dict[PieceType, int],
    black_piece_counts: Dict[PieceType, int]
) -> int:
    """
    Compute material imbalance bonus/penalty.
    This adjusts the raw material score based on the composition of forces.
    """
    imbalance = 0
    for w_piece, w_count in white_piece_counts.items():
        for b_piece, b_count in black_piece_counts.items():
            key = (w_piece, b_piece)
            if key in IMBALANCE_TABLE:
                imbalance += IMBALANCE_TABLE[key] * w_count * b_count
    return imbalance
```

## Endgame Material Scaling

In the endgame, material advantages become **more decisive**. A one-pawn advantage in a rook endgame is worth more than a one-pawn advantage in a middlegame with queens on the board, because there are fewer pieces to compensate. Our engine applies an **endgame scaling factor**:

$$
M_{\text{scaled}} = M \times \text{scale}(\text{phase})
$$

```python
def endgame_scale_factor(total_material: int) -> float:
    """
    Scale material advantage by game phase.
    In endgame (low material), advantages are more decisive.
    In middlegame (high material), advantages are less decisive.
    """
    # Maximum non-pawn, non-king material for both sides
    MAX_MATERIAL = 2 * (2 * 320 + 2 * 330 + 2 * 500 + 900)  # = 4900
    phase = total_material / MAX_MATERIAL  # 0.0 = endgame, 1.0 = opening
    # Scale: in endgame (phase→0), amplify material; in opening, don't
    return 1.0 + 0.3 * (1.0 - phase)  # ranges from 1.0 to 1.3
```

## Opposite-Colored Bishops

A special case in endgame evaluation: when each side has one bishop and they are on **opposite colors**, drawing chances increase dramatically, even with a pawn deficit. This is because the stronger side's bishop cannot attack the defender's pawns (or defend its own on the opposite color).

```python
def opposite_color_bishops(
    white_bishop_sq: int,
    black_bishop_sq: int,
    white_pawns: int,
    black_pawns: int
) -> int:
    """
    In opposite-colored bishop endgames, scale down the evaluation
    because drawing chances are much higher.
    Returns a scaling factor (0-100) applied to the total eval.
    """
    # Check if bishops are on opposite colors
    white_light = (white_bishop_sq + (white_bishop_sq // 8)) % 2 == 0
    black_light = (black_bishop_sq + (black_bishop_sq // 8)) % 2 == 0

    if white_light == black_light:
        return 100  # Same color bishops, no special scaling

    # Opposite colors: reduce eval sharply if few pawns
    total_pawns = white_pawns + black_pawns
    if total_pawns <= 4:
        return 30  # Very drawish
    elif total_pawns <= 6:
        return 50
    else:
        return 70
```

## Tracking Material for the Explanation Engine

Each material computation generates an [[EvalTerm]] with a human-readable reason:

```python
def evaluate_material(board) -> List[EvalTerm]:
    """Compute all material-related evaluation terms with explanations."""
    terms = []

    # Raw material balance
    balance = material_balance(board.white_pieces, board.black_pieces)
    if balance != 0:
        side = "White" if balance > 0 else "Black"
        abs_bal = abs(balance)
        pieces_ahead = "a pawn" if abs_bal == 100 else f"{abs_bal/100:.1f} pawns' worth"
        terms.append(EvalTerm(
            name="Material",
            value=balance,
            reason=f"{side} has an advantage of {pieces_ahead} of material",
            priority=1
        ))

    # Bishop pair bonus
    w_bishops = board.count_pieces(WHITE, BISHOP)
    b_bishops = board.count_pieces(BLACK, BISHOP)
    bp = bishop_pair_bonus(w_bishops, b_bishops)
    if bp != 0:
        side = "White" if bp > 0 else "Black"
        terms.append(EvalTerm(
            name="Bishop Pair",
            value=bp,
            reason=f"{side} has the bishop pair, controlling both color complexes",
            priority=5
        ))

    return terms
```

## Summary

Material evaluation is the anchor of the [[Static Evaluation Overview|evaluation function]]. While simple in concept—a weighted sum of piece counts—it requires careful handling of edge cases (bishop pair, imbalance, opposite-colored bishops, endgame scaling) to be accurate. In our explainable engine, every material adjustment carries a narrative: the engine doesn't just say "+150 cp"; it says "White has an extra pawn and the bishop pair." This is what makes the engine a **teacher**, not just a calculator.

---

**See also:** [[Static Evaluation Overview]], [[Piece-Square Tables]], [[Pawn Structure Evaluation]], [[King Safety Evaluation]], [[Mobility and Piece Activity]], [[Threats and Tactical Patterns]], [[Endgame Scaling]], [[Bishop Pair]]
