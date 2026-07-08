# King Safety Evaluation

> "Chess is a game of king-hunting." — Gerald Abrahams

## The Paramount Importance of King Safety

Of all the [[Static Evaluation Overview|evaluation terms]], king safety is the most **urgent**. A material advantage of +500 centipawns is meaningless if the king gets checkmated. King safety evaluation is fundamentally asymmetric: a slight material deficit is acceptable if the king is safe, but even a large material advantage cannot compensate for an exposed king under attack.

King safety is also the most **difficult** evaluation term to get right. It requires assessing:
1. The **pawn shield** in front of the king
2. **Open files** near the king that enemy rooks can exploit
3. **Attack units** — how many enemy pieces are targeting the king zone
4. **King tropism** — how close enemy pieces are to the king

Unlike [[Material Evaluation]] (which is additive and stable) or [[Piece-Square Tables]] (which are static and local), king safety is **dynamic and combinatorial** — the danger comes from the *combination* of weaknesses, not from any single factor alone.

## The King Zone

The **king zone** is defined as the 3×3 area centered on the king's square. If the king is on g1, the king zone includes f1, g1, h1, f2, g2, h2, f3, g3, h3 (within the board boundaries).

```python
def king_zone(king_square: int) -> List[int]:
    """
    Return the squares in the king zone (3x3 area around the king).
    These are the squares whose safety matters most.
    """
    rank = king_square // 8
    file = king_square % 8
    zone = []

    for dr in [-1, 0, 1]:
        for df in [-1, 0, 1]:
            r = rank + dr
            f = file + df
            if 0 <= r <= 7 and 0 <= f <= 7:
                zone.append(r * 8 + f)

    return zone
```

## 1. Pawn Shield Evaluation

The most important component of king safety is the **pawn shield** — the three pawns directly in front of the castled king. For a White king on g1, the ideal shield consists of f2, g2, h2. Missing pawns from this shield create open lines for attack.

### Shield Scoring

```python
# Pawn shield penalties (per missing shield pawn)
SHIELD_PENALTY = {
    # (missing_count) → penalty in centipawns
    0: 0,     # Perfect shield
    1: -30,   # One pawn missing
    2: -60,   # Two pawns missing
    3: -100,  # No shield at all (king is naked!)
}

def evaluate_pawn_shield(board: Board, king_square: int, color: Color) -> Tuple[int, str]:
    """
    Evaluate the pawn shield in front of the king.
    For White: check the rank directly below the king's file and adjacent files.
    For Black: check the rank directly above.
    """
    rank = king_square // 8
    file = king_square % 8

    # Determine shield rank and direction
    if color == WHITE:
        shield_rank = rank + 1  # Pawns should be one rank in front
        if rank > 1:
            # King not on back rank, shield is less relevant
            return 0, "King not on back rank, pawn shield less relevant"
    else:
        shield_rank = rank - 1
        if rank < 6:
            return 0, "King not on back rank, pawn shield less relevant"

    if shield_rank < 0 or shield_rank > 7:
        return 0, "King on edge, no shield possible"

    # Check for pawns on the three shield files
    shield_files = [max(0, file - 1), file, min(7, file + 1)]
    missing = 0
    missing_files = []

    for f in shield_files:
        shield_sq = shield_rank * 8 + f
        piece = board.piece_at(shield_sq)
        if piece is None or piece.type != PAWN or piece.color != color:
            missing += 1
            missing_files.append(chr(ord('a') + f))

    penalty = SHIELD_PENALTY.get(missing, -100)

    reason = ""
    if missing == 0:
        reason = "King has a complete pawn shield"
    else:
        files_str = ", ".join(missing_files)
        reason = f"King's pawn shield is missing pawns on the {files_str} file(s)"

    return penalty, reason
```

### Storm Shields

An additional danger: **enemy pawns advancing toward the king** (a "pawn storm"). Even with a complete shield, if enemy pawns are on adjacent files and advancing, the shield will be broken soon.

```python
def evaluate_pawn_storm(board: Board, king_square: int, color: Color) -> int:
    """
    Evaluate enemy pawn storms approaching the king.
    Enemy pawns on adjacent files heading toward our king are dangerous.
    """
    king_rank = king_square // 8
    king_file = king_square % 8
    enemy_color = BLACK if color == WHITE else WHITE

    storm_penalty = 0
    for df in [-1, 0, 1]:
        f = king_file + df
        if f < 0 or f > 7:
            continue

        # Check enemy pawns on this file
        enemy_pawns_on_file = board.get_pawns_on_file(enemy_color, f)
        for pawn_rank in enemy_pawns_on_file:
            # Is this pawn advancing toward our king?
            if color == WHITE and pawn_rank > king_rank:
                distance = pawn_rank - king_rank
                storm_penalty -= (4 - distance) * 10  # Closer = more dangerous
            elif color == BLACK and pawn_rank < king_rank:
                distance = king_rank - pawn_rank
                storm_penalty -= (4 - distance) * 10

    return storm_penalty
```

## 2. Open Files Near the King

An **open file** (no pawns of either color) or **semi-open file** (only enemy pawns) near the king is an invitation for enemy rooks to attack. Rooks on open files near the king are among the most dangerous attacking pieces.

```python
def evaluate_open_files_near_king(board: Board, king_square: int, color: Color) -> int:
    """
    Penalize open or semi-open files near the king.
    Open files allow enemy rooks direct access to the king.
    """
    king_file = king_square % 8
    penalty = 0

    for df in [-1, 0, 1]:
        f = king_file + df
        if f < 0 or f > 7:
            continue

        own_pawns = board.count_pawns_on_file(color, f)
        enemy_pawns = board.count_pawns_on_file(
            BLACK if color == WHITE else WHITE, f
        )

        if own_pawns == 0 and enemy_pawns == 0:
            # Fully open file near king: very dangerous
            penalty -= 40
        elif own_pawns == 0 and enemy_pawns > 0:
            # Semi-open file (enemy has pawns): moderately dangerous
            penalty -= 15

    return penalty
```

**Explanation**: *"The f-file is open near White's king, giving Black's rooks a direct avenue of attack (-40 cp)."*

## 3. Attack Units

This is the most sophisticated king safety metric. We count **attack units** — the number of enemy pieces that can reach the king zone — and apply a **non-linear** penalty. The non-linearity is critical: one attacker is a nuisance, two are a threat, three are dangerous, and four or more can be devastating.

### Attack Weight Table

Each type of attacker contributes a different weight:

| Piece | Attack Weight |
|-------|---------------|
| Queen | 4 |
| Rook | 3 |
| Bishop | 2 |
| Knight | 2 |

### Non-Linear Penalty Function

The penalty scales quadratically with the total attack weight:

$$
KS_{\text{attack}} = -\text{attack\_weight}^2 \times 2
$$

This means:
- 1 attacker (weight 2): penalty = -8 cp
- 2 attackers (weight 4): penalty = -32 cp
- 3 attackers (weight 6): penalty = -72 cp
- 4 attackers (weight 8): penalty = -128 cp
- 5 attackers (weight 10): penalty = -200 cp

```python
ATTACK_WEIGHTS = {
    QUEEN: 4,
    ROOK: 3,
    BISHOP: 2,
    KNIGHT: 2,
}

def evaluate_attack_units(board: Board, king_square: int, color: Color) -> Tuple[int, str]:
    """
    Count attack units targeting the king zone.
    Apply a quadratic penalty for increasing attack pressure.
    """
    enemy_color = BLACK if color == WHITE else WHITE
    zone = king_zone(king_square)
    zone_set = set(zone)

    total_attack_weight = 0
    attackers = []

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None or piece.color != enemy_color:
            continue
        if piece.type == PAWN or piece.type == KING:
            continue

        # Does this piece attack any square in the king zone?
        attacks = board.attacks_from(square)
        if attacks & zone_set:
            weight = ATTACK_WEIGHTS.get(piece.type, 0)
            total_attack_weight += weight
            attackers.append(f"{piece.symbol()}{square_name(square)}")

    # Quadratic penalty
    penalty = -(total_attack_weight ** 2) * 2

    # Generate explanation
    if total_attack_weight == 0:
        reason = "No enemy pieces are targeting the king zone"
    else:
        attacker_str = ", ".join(attackers)
        reason = f"Enemy pieces ({attacker_str}) are targeting the king zone with {total_attack_weight} attack units"

    return penalty, reason
```

## 4. King Tropism

**King tropism** measures how close enemy pieces (especially queens and rooks) are to the king. The closer they are, the more dangerous. This is a simpler metric than attack units but captures the "looming threat" of nearby heavy pieces.

```python
def evaluate_king_tropism(board: Board, king_square: int, color: Color) -> int:
    """
    Penalize enemy pieces that are close to the king.
    Distance is measured in Chebyshev (chess king) distance.
    """
    enemy_color = BLACK if color == WHITE else WHITE
    king_rank = king_square // 8
    king_file = king_square % 8

    tropism_penalty = 0
    TROPISM_WEIGHTS = {
        QUEEN: 6,
        ROOK: 4,
        BISHOP: 3,
        KNIGHT: 3,
    }

    for square in range(64):
        piece = board.piece_at(square)
        if piece is None or piece.color != enemy_color:
            continue

        weight = TROPISM_WEIGHTS.get(piece.type, 0)
        if weight == 0:
            continue

        # Chebyshev distance
        pr = square // 8
        pf = square % 8
        distance = max(abs(pr - king_rank), abs(pf - king_file))

        # Penalty is inverse of distance, weighted by piece importance
        if distance > 0:
            tropism_penalty -= weight * (7 - distance)  # Closer = bigger penalty

    return tropism_penalty
```

## Complete King Safety Evaluation

```python
def evaluate_king_safety(board: Board) -> Tuple[int, List[EvalTerm]]:
    """
    Full king safety evaluation for both sides.
    Returns (score, terms) where score is White-positive.
    """
    terms = []
    score = 0

    for color in [WHITE, BLACK]:
        king_sq = board.king_square(color)
        sign = 1 if color == WHITE else -1

        # Pawn shield
        shield_val, shield_reason = evaluate_pawn_shield(board, king_sq, color)
        if shield_val != 0:
            score += sign * shield_val
            terms.append(EvalTerm(
                name=f"{'White' if color == WHITE else 'Black'} King Shield",
                value=sign * shield_val,
                reason=shield_reason,
                priority=2
            ))

        # Open files near king
        open_files = evaluate_open_files_near_king(board, king_sq, color)
        if open_files != 0:
            score += sign * open_files
            terms.append(EvalTerm(
                name=f"{'White' if color == WHITE else 'Black'} King Open Files",
                value=sign * open_files,
                reason=f"Open files near the {'White' if color == WHITE else 'Black'} king allow rook attacks",
                priority=3
            ))

        # Attack units
        attack_val, attack_reason = evaluate_attack_units(board, king_sq, color)
        if attack_val != 0:
            score += sign * attack_val
            terms.append(EvalTerm(
                name=f"{'White' if color == WHITE else 'Black'} King Attack",
                value=sign * attack_val,
                reason=attack_reason,
                priority=1  # Very important to report
            ))

        # King tropism
        tropism = evaluate_king_tropism(board, king_sq, color)
        if tropism != 0:
            score += sign * tropism
            terms.append(EvalTerm(
                name=f"{'White' if color == WHITE else 'Black'} King Tropism",
                value=sign * tropism,
                reason=f"Enemy pieces are near the {'White' if color == WHITE else 'Black'} king",
                priority=3
            ))

    return score, terms
```

## Endgame Transition

King safety evaluation must **diminish in the endgame**. With few pieces on the board, the risk of checkmate drops dramatically, and the king should transition from hiding to activating. Our engine uses the [[Game Phase|game phase]] parameter to scale king safety terms:

```python
def scale_king_safety(king_safety_score: int, phase: float) -> int:
    """
    Scale king safety by game phase.
    phase: 1.0 = full middlegame, 0.0 = pure endgame.
    In endgame, king safety is much less important.
    """
    return int(king_safety_score * phase)
```

In the endgame, the king's [[Piece-Square Tables|PST]] naturally encourages centralization, complementing the reduced safety penalties.

## The Narrative of Danger

The most powerful aspect of explainable king safety is the **narrative of danger**. Instead of reporting a cryptic score, the engine can say:

> "White's king is in serious danger. The pawn shield is broken (missing the g-pawn, -30 cp). Black's queen on h5 and rook on f1 are attacking the king zone with 7 attack units (-98 cp). The f-file is open, giving Black's rook direct access (-40 cp). White must prioritize king safety over material gains."

This kind of explanation transforms the engine from a black box into a chess coach.

---

**See also:** [[Static Evaluation Overview]], [[Pawn Structure Evaluation]], [[Mobility and Piece Activity]], [[Piece-Square Tables]], [[Attack Units]], [[King Tropism]], [[Pawn Shield]], [[Quiescence Search]]
