# Pawn Structure Evaluation

> "Pawns are the soul of chess." — François-André Danican Philidor

## Why Pawn Structure Matters

Of all the [[Static Evaluation Overview|evaluation terms]], pawn structure is the most **strategically significant** and the most **durable**. Unlike piece placement (which can change in a single move), pawn structures persist for many moves and shape the entire character of the position. A doubled pawn created on move 8 may remain doubled for 30 moves, creating permanent weaknesses.

Pawn structure evaluation answers: **Is the pawn skeleton healthy or compromised?** A healthy pawn structure provides:
- **Mobility** for pieces behind it
- **Control** of key squares
- **Safety** for the king
- **Potential** for breakthrough and promotion

A compromised pawn structure creates permanent liabilities that the opponent can exploit.

## The Five Pawn Structure Defects

Our engine evaluates five major pawn structure defects, each with a centipawn penalty and an explainable reason.

### 1. Doubled Pawns

**Definition**: Two pawns of the same color on the same file. This occurs when one pawn captures diagonally onto a file already occupied by a friendly pawn.

**Why it's bad**:
- The rear pawn is **blocked** and cannot advance.
- The pawns cannot defend each other.
- They create a **static weakness** that can be blockaded.
- They reduce the number of pawns controlling adjacent squares.

**Penalty**: -15 centipawns per doubled pawn group.

```python
def find_doubled_pawns(pawn_files: Dict[int, List[int]]) -> List[Tuple[int, int]]:
    """
    Find all doubled pawn groups.
    pawn_files: mapping from file (0-7) to list of pawn ranks on that file.
    Returns list of (file, count) for files with more than one pawn.
    """
    doubled = []
    for file, ranks in pawn_files.items():
        if len(ranks) > 1:
            doubled.append((file, len(ranks)))
    return doubled

def evaluate_doubled_pawns(white_pawn_files: Dict[int, List[int]],
                           black_pawn_files: Dict[int, List[int]]) -> int:
    """Return penalty for doubled pawns (White-positive convention)."""
    DOUBLED_PENALTY = -15  # per extra pawn on same file

    score = 0
    for file, ranks in white_pawn_files.items():
        if len(ranks) > 1:
            score += DOUBLED_PENALTY * (len(ranks) - 1)

    for file, ranks in black_pawn_files.items():
        if len(ranks) > 1:
            score -= DOUBLED_PENALTY * (len(ranks) - 1)

    return score
```

**Explanation**: *"White has doubled pawns on the e-file, limiting their mobility and creating a static weakness (-15 cp)."*

### 2. Isolated Pawns

**Definition**: A pawn with no friendly pawns on adjacent files. It cannot be defended by another pawn and becomes a target.

**Why it's bad**:
- It must be defended by pieces, tying them down.
- The opponent can blockade it with a piece (especially a knight).
- The squares in front of an isolated pawn become outposts for enemy pieces.
- In endgames, isolated pawns are vulnerable because fewer pieces can defend them.

**Penalty**: -20 centipawns per isolated pawn.

```python
def is_isolated_pawn(file: int, own_pawn_files: Set[int]) -> bool:
    """
    Check if a pawn on the given file is isolated.
    A pawn is isolated if there are no friendly pawns on adjacent files.
    """
    adjacent_files = set()
    if file > 0:
        adjacent_files.add(file - 1)
    if file < 7:
        adjacent_files.add(file + 1)
    return len(adjacent_files & own_pawn_files) == 0

def evaluate_isolated_pawns(white_pawn_files: Dict[int, List[int]],
                            black_pawn_files: Dict[int, List[int]]) -> int:
    """Return penalty for isolated pawns."""
    ISOLATED_PENALTY = -20

    score = 0
    white_file_set = set(white_pawn_files.keys())
    black_file_set = set(black_pawn_files.keys())

    for file in white_pawn_files:
        if is_isolated_pawn(file, white_file_set):
            score += ISOLATED_PENALTY * len(white_pawn_files[file])

    for file in black_pawn_files:
        if is_isolated_pawn(file, black_file_set):
            score -= ISOLATED_PENALTY * len(black_pawn_files[file])

    return score
```

**Explanation**: *"White's d-pawn is isolated—it has no pawns on the c or e files to protect it, making it a target for Black's pieces (-20 cp)."*

### 3. Backward Pawns

**Definition**: A pawn that cannot advance because the square in front of it is controlled by an enemy pawn, AND it cannot be defended by a friendly pawn advancing.

**Why it's bad**:
- It is a permanent weakness—stuck in place.
- The square in front of it is a strong outpost for the opponent.
- It requires piece defense, reducing piece activity.
- It can be attacked repeatedly (the "weakling" pawn).

**Penalty**: -25 centipawns per backward pawn.

```python
def is_backward_pawn(file: int, rank: int, own_pawn_files: Dict[int, List[int]],
                     enemy_pawn_files: Dict[int, List[int]], color: Color) -> bool:
    """
    Check if a pawn is backward.
    A pawn is backward if:
    1. The square directly in front is controlled by an enemy pawn.
    2. No friendly pawn on an adjacent file can advance to defend it.
    """
    # Direction of advancement
    advance_rank = rank + 1 if color == WHITE else rank - 1
    if advance_rank < 0 or advance_rank > 7:
        return False  # Can't advance (already on last rank)

    # Check if the square in front is controlled by an enemy pawn
    front_controlled = False
    for adj_file in [file - 1, file + 1]:
        if 0 <= adj_file <= 7:
            enemy_ranks = enemy_pawn_files.get(adj_file, [])
            for er in enemy_ranks:
                # Enemy pawn controls the advance square?
                enemy_advance = er + 1 if color == WHITE else er - 1
                if enemy_advance == advance_rank:
                    front_controlled = True
                    break

    if not front_controlled:
        return False  # The square in front is not contested

    # Check if a friendly pawn on an adjacent file can advance to defend
    can_be_defended = False
    for adj_file in [file - 1, file + 1]:
        if 0 <= adj_file <= 7:
            own_ranks = own_pawn_files.get(adj_file, [])
            for own_rank in own_ranks:
                # Can this friendly pawn advance to the defense square?
                if color == WHITE and own_rank <= rank:
                    can_be_defended = True
                elif color == BLACK and own_rank >= rank:
                    can_be_defended = True

    return not can_be_defended
```

**Explanation**: *"White's d2 pawn is backward—the d3 square is controlled by Black's e4 pawn, and no White pawn can advance to defend it (-25 cp)."*

### 4. Passed Pawns

**Definition**: A pawn with no enemy pawns on its file or on adjacent files between it and the promotion square. It can advance to promotion without being blocked or captured by an enemy pawn.

**Why it's valuable**:
- It is a direct **promotion threat** that demands attention.
- It ties down enemy pieces to blockade it.
- Its value increases as it advances (the "passed pawn races" principle).
- Connected passed pawns (two or more on adjacent files) are nearly unstoppable.

**Bonus**: +20 to +100 centipawns, increasing with rank advancement.

```python
def is_passed_pawn(file: int, rank: int, enemy_pawn_files: Dict[int, List[int]],
                   color: Color) -> bool:
    """
    Check if a pawn is passed.
    A pawn is passed if no enemy pawn can block or capture it on its
    march to promotion.
    """
    if color == WHITE:
        # Check from rank+1 to rank 7 on same file and adjacent files
        for check_file in [file - 1, file, file + 1]:
            if 0 <= check_file <= 7:
                enemy_ranks = enemy_pawn_files.get(check_file, [])
                for er in enemy_ranks:
                    if er > rank:  # Enemy pawn ahead
                        return False
    else:
        # Check from rank-1 down to rank 0
        for check_file in [file - 1, file, file + 1]:
            if 0 <= check_file <= 7:
                enemy_ranks = enemy_pawn_files.get(check_file, [])
                for er in enemy_ranks:
                    if er < rank:  # Enemy pawn ahead (toward rank 0)
                        return False
    return True

PASSED_PAWN_BONUS_BY_RANK = {
    # Rank → bonus in centipawns (from the perspective of the advancing side)
    2: 10,   # Just created, distant
    3: 20,
    4: 30,
    5: 50,
    6: 80,   # One step from promotion, extremely dangerous
    7: 120,  # About to promote (though this is rare as promotion would occur)
}

def evaluate_passed_pawns(white_pawns: List[Tuple[int, int]],
                          black_pawns: List[Tuple[int, int]],
                          white_pawn_files: Dict[int, List[int]],
                          black_pawn_files: Dict[int, List[int]]) -> int:
    """Evaluate passed pawns for both sides."""
    score = 0
    for file, rank in white_pawns:
        if is_passed_pawn(file, rank, black_pawn_files, WHITE):
            score += PASSED_PAWN_BONUS_BY_RANK.get(rank, 0)

    for file, rank in black_pawns:
        if is_passed_pawn(file, rank, white_pawn_files, BLACK):
            # Mirror the rank for Black (rank 2 for Black ≈ rank 6 for White)
            mirrored = 7 - rank
            score -= PASSED_PAWN_BONUS_BY_RANK.get(mirrored, 0)

    return score
```

**Explanation**: *"White has a passed pawn on e5—a dangerous weapon that threatens to promote and demands constant attention from Black's pieces (+50 cp)."*

### 5. Connected Passed Pawns

**Definition**: Two or more passed pawns on adjacent files that can mutually support each other's advance. They are among the most powerful positional advantages in chess.

**Why they're devastating**:
- If the opponent blockades one, the other advances.
- A single piece cannot stop two connected passed pawns.
- They can create a "roll" where one pawn sacrifices to promote the other.

**Bonus**: +40 centipawns on top of individual passed pawn bonuses.

```python
CONNECTED_PASSED_BONUS = 40

def evaluate_connected_passed_pawns(passed_pawns: List[Tuple[int, int]]) -> int:
    """
    Check for connected passed pawns (adjacent files).
    Only counts unique connections (not per-pawn).
    """
    if len(passed_pawns) < 2:
        return 0

    files = sorted(set(f for f, r in passed_pawns))
    connections = 0
    for i in range(len(files) - 1):
        if files[i + 1] - files[i] == 1:
            connections += 1

    return CONNECTED_PASSED_BONUS * connections
```

## Pawn Chains

A **pawn chain** is a diagonal line of pawns where each pawn defends the next. The base of the chain (the pawn defended by no other pawn) is the weak point.

```python
def pawn_chain_base(pawns: List[Tuple[int, int]], color: Color) -> List[Tuple[int, int]]:
    """
    Find the base(s) of pawn chains.
    A pawn chain base is a pawn that is not defended by another pawn.
    These are structural weaknesses the opponent should target.
    """
    pawn_set = set(pawns)
    defended = set()

    for file, rank in pawns:
        # A pawn on (file, rank) defends pawns on (file-1, rank+1) and (file+1, rank+1)
        # for White; mirror for Black
        if color == WHITE:
            for df in [-1, 1]:
                nf = file + df
                nr = rank + 1
                if (nf, nr) in pawn_set:
                    defended.add((nf, nr))
        else:
            for df in [-1, 1]:
                nf = file + df
                nr = rank - 1
                if (nf, nr) in pawn_set:
                    defended.add((nf, nr))

    # Bases are pawns NOT defended by another pawn
    bases = [p for p in pawns if p not in defended]
    return bases

CHAIN_BASE_PENALTY = -10

def evaluate_pawn_chains(white_pawns, black_pawns):
    """Penalize pawn chain bases as they are targets."""
    score = 0
    white_bases = pawn_chain_base(white_pawns, WHITE)
    black_bases = pawn_chain_base(black_pawns, BLACK)
    score += CHAIN_BASE_PENALTY * len(white_bases)
    score -= CHAIN_BASE_PENALTY * len(black_bases)
    return score
```

**Explanation**: *"The base of White's pawn chain on d3 is a target—if it falls, the entire chain collapses (-10 cp)."*

## Complete Pawn Structure Evaluation

```python
def evaluate_pawn_structure(board: Board) -> Tuple[int, List[EvalTerm]]:
    """
    Full pawn structure evaluation.
    Returns (score, terms) where score is White-positive.
    """
    # Gather pawn data
    white_pawns = board.get_pawns(WHITE)
    black_pawns = board.get_pawns(BLACK)
    white_pawn_files = board.get_pawn_files(WHITE)
    black_pawn_files = board.get_pawn_files(BLACK)

    terms = []
    total = 0

    # Doubled pawns
    doubled = evaluate_doubled_pawns(white_pawn_files, black_pawn_files)
    if doubled != 0:
        side = "White" if doubled < 0 else "Black"
        total += doubled
        terms.append(EvalTerm(
            name="Doubled Pawns", value=doubled,
            reason=f"{side} has doubled pawns, reducing mobility",
            priority=4
        ))

    # Isolated pawns
    isolated = evaluate_isolated_pawns(white_pawn_files, black_pawn_files)
    if isolated != 0:
        side = "White" if isolated < 0 else "Black"
        total += isolated
        terms.append(EvalTerm(
            name="Isolated Pawns", value=isolated,
            reason=f"{side} has isolated pawns vulnerable to attack",
            priority=4
        ))

    # Backward pawns
    backward = evaluate_backward_pawns_full(board)
    if backward != 0:
        side = "White" if backward < 0 else "Black"
        total += backward
        terms.append(EvalTerm(
            name="Backward Pawns", value=backward,
            reason=f"{side} has backward pawns that cannot advance safely",
            priority=4
        ))

    # Passed pawns
    passed = evaluate_passed_pawns(white_pawns, black_pawns,
                                    white_pawn_files, black_pawn_files)
    if passed != 0:
        side = "White" if passed > 0 else "Black"
        total += passed
        terms.append(EvalTerm(
            name="Passed Pawns", value=passed,
            reason=f"{side} has passed pawn(s) threatening promotion",
            priority=3
        ))

    # Connected passed pawns
    # (additional bonus on top of individual passed pawn bonuses)
    # Pawn chains
    chains = evaluate_pawn_chains(white_pawns, black_pawns)
    if chains != 0:
        total += chains
        terms.append(EvalTerm(
            name="Pawn Chain", value=chains,
            reason="Pawn chain bases are potential targets",
            priority=5
        ))

    return total, terms
```

## Summary

Pawn structure is the **strategic backbone** of a position. While [[Material Evaluation]] tells you who has more stuff, and [[Piece-Square Tables]] tell you where pieces prefer to be, pawn structure tells you whether the **foundation** of the position is sound. Each defect (doubled, isolated, backward) is a permanent liability; each asset (passed, connected) is a long-term weapon. In our explainable engine, every pawn structure term carries a clear narrative, making the engine a genuine chess teacher.

---

**See also:** [[Static Evaluation Overview]], [[Material Evaluation]], [[Piece-Square Tables]], [[King Safety Evaluation]], [[Mobility and Piece Activity]], [[Passed Pawns]], [[Pawn Chains]], [[Philidor Defense]]
