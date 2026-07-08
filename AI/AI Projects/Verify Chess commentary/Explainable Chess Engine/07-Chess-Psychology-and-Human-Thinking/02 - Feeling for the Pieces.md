---
tags:
  - chapter-07
  - psychology
  - piece-quality
  - bad-bishop
  - bad-knight
  - piece-activity
  - improvement-algorithm
  - positional-chess
---

# 02 - Feeling for the Pieces

## The Concept of Piece Quality

Not all pieces are created equal. A knight on a central outpost dominating the board is worth far more than its nominal 3 points, while a bishop trapped behind its own pawns might be worth barely more than a pawn. This concept—**piece quality** or **piece activity**—is one of the most important ideas in positional chess, and it is central to how humans evaluate positions.

The phrase "feeling for the pieces" comes from the intuitive sense that strong players develop: they can *feel* when a piece is well-placed or poorly placed. This feeling is not mystical—it is the result of pattern recognition, accumulated through thousands of games and studies, that associates piece placement with positional outcomes. Our engine must codify this feeling into measurable, explainable rules.

## Good Pieces vs. Bad Pieces

### The Spectrum of Piece Quality

Piece quality exists on a spectrum from **dominant** to **pathetic**. Here is the scale for each piece type:

| Quality Level | Knight | Bishop | Rook | Queen |
|--------------|--------|--------|------|-------|
| **Dominant** | Outpost on rank 5, no enemy pawn can attack | Open diagonal aiming at enemy king | 7th rank with trapped enemy king | Active in center with targets |
| **Good** | Central with multiple targets | Open diagonal, good pawn structure | Open file, active | Coordinated with other pieces |
| **Neutral** | Average central position | Average position | Undeveloped but not blocked | Not yet developed |
| **Bad** | On the rim, no targets | Blocked by own pawns on same color | Blocked by pawns, no open file | Chased by lesser pieces |
| **Pathetic** | Trapped, no moves | Entirely locked by pawn chain | Completely passive, no prospects | Trapped, about to be exchanged for rook |

### The Bad Bishop

The **bad bishop** is perhaps the most classic example of a poorly placed piece. A bishop is "bad" when it is on the same color complex as its own central pawns, because those pawns block the bishop's diagonals and limit its scope.

```python
def is_bad_bishop(board: chess.Board, square: chess.Square, color: chess.Color) -> bool:
    """
    Determine if a bishop is 'bad' — blocked by its own pawns
    on the same color complex.
    """
    piece = board.piece_at(square)
    if piece is None or piece.piece_type != chess.BISHOP:
        return False
    
    bishop_color = chess.square_color(square)  # True = light, False = dark
    own_pawns_on_color = 0
    total_own_pawns = 0
    
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.piece_type == chess.PAWN and p.color == color:
            total_own_pawns += 1
            if chess.square_color(sq) == bishop_color:
                own_pawns_on_color += 1
    
    # Bishop is bad if most own pawns are on its color complex
    if total_own_pawns == 0:
        return False
    
    ratio = own_pawns_on_color / total_own_pawns
    return ratio >= 0.5 and own_pawns_on_color >= 3
```

**Why the bad bishop matters for explanation**: When our engine recommends a move that improves a bad bishop (e.g., by moving the blocking pawns or exchanging the bishop), it can explain: "This move improves the bad bishop on c8 by advancing the d-pawn, giving the bishop the d7-a4 diagonal." Without the concept of piece quality, this explanation would be impossible.

### The Bad Knight ("A Knight on the Rim Is Dim")

A knight on the edge of the board (a-file, h-file, 1st rank, 8th rank) controls far fewer squares than a central knight. The math is stark:

- **Knight on a1**: Controls 2 squares
- **Knight on d4**: Controls 8 squares
- **Knight on e5**: Controls 8 squares

This is why the chess proverb says "A knight on the rim is dim." Our engine must detect when a knight is poorly placed and explain moves that improve it:

```python
def knight_centralization_score(square: chess.Square) -> float:
    """
    Score how centralized a knight is. Central knights control more squares
    and are more influential.
    
    Returns a value from 0.0 (corner) to 1.0 (center).
    """
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    
    # Distance from center (d4, d5, e4, e5)
    file_dist = abs(file - 3.5)
    rank_dist = abs(rank - 3.5)
    max_dist = 3.5  # Maximum possible distance from center
    
    # Normalize to [0, 1]
    centrality = 1.0 - (file_dist + rank_dist) / (2 * max_dist)
    return centrality
```

### The Bad Rook (Without an Open File)

A rook is most powerful on an **open file** (no pawns on the file) or a **semi-open file** (only enemy pawns). A rook trapped behind its own pawns on a closed file is a bad rook—one of the most common positional weaknesses in amateur play.

```python
def rook_file_quality(board: chess.Board, square: chess.Square, 
                       color: chess.Color) -> str:
    """
    Classify a rook's file quality.
    Returns: 'open', 'semi-open', or 'closed'
    """
    file = chess.square_file(square)
    
    own_pawns_on_file = 0
    enemy_pawns_on_file = 0
    
    for rank in range(8):
        sq = chess.square(file, rank)
        piece = board.piece_at(sq)
        if piece and piece.piece_type == chess.PAWN:
            if piece.color == color:
                own_pawns_on_file += 1
            else:
                enemy_pawns_on_file += 1
    
    if own_pawns_on_file == 0 and enemy_pawns_on_file == 0:
        return "open"
    elif own_pawns_on_file == 0 and enemy_pawns_on_file > 0:
        return "semi-open"
    else:
        return "closed"
```

## Activity vs. Passivity

### The Activity Principle

The fundamental principle of positional chess is that **active pieces are better than passive pieces**. An active piece:
- Controls important squares
- Threatens the opponent's position
- Has multiple options and moves available
- Works in coordination with other pieces

A passive piece:
- Is blocked by its own or opponent's pawns
- Controls few important squares
- Has limited mobility
- Serves only a defensive function

The difference between activity and passivity is measurable through **mobility**—the number of legal moves available to each piece. Our engine's [[05-Evaluation-Functions-and-Heuristics/06 - Mobility and Piece Activity|mobility evaluation]] directly quantifies this:

```python
def piece_activity_score(board: chess.Board, color: chess.Color) -> dict[chess.PieceType, float]:
    """
    Calculate the activity score for each piece type of the given color.
    Activity = number of squares attacked / maximum possible attacks.
    """
    activity = {}
    
    for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        total_attacks = 0
        piece_count = 0
        
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece and piece.piece_type == piece_type and piece.color == color:
                attacks = len(board.attacks(sq))
                total_attacks += attacks
                piece_count += 1
        
        if piece_count > 0:
            # Normalize by maximum possible attacks for the piece type
            max_attacks = {
                chess.KNIGHT: 8,
                chess.BISHOP: 13,
                chess.ROOK: 14,
                chess.QUEEN: 27
            }
            activity[piece_type] = total_attacks / (piece_count * max_attacks[piece_type])
        else:
            activity[piece_type] = 0.0
    
    return activity
```

### The Activity-Passivity Scale in Practice

Consider a typical middlegame position where White has:
- A knight on d5 (outpost, controlling 8 squares) → **Highly active**
- A bishop on c1 (blocked by d2 and e3 pawns) → **Passive**
- A rook on e1 (semi-open e-file) → **Moderately active**
- A rook on a1 (closed a-file) → **Passive**

The total activity profile tells a story: White's strength lies in the dominant knight and the semi-open file, while the weakness lies in the bad bishop and the passive a-rook. The plan should be to improve the passive pieces.

## The Improvement Algorithm

### Find Your Worst Piece and Improve It

This is perhaps the single most useful heuristic for positional play: **look at your pieces, identify the worst one, and find a way to improve it**. This "improvement algorithm" was formalized by chess trainers but has been practiced intuitively by strong players for centuries.

The algorithm works because:
1. It focuses attention on the *weakest link* in the position
2. Improving a piece rarely makes the position worse (unlike aggressive play, which can backfire)
3. The opponent's best piece is often the one exploiting your worst piece
4. Systematic improvement of all pieces eventually creates a dominant position

```python
def find_worst_piece(board: chess.Board, color: chess.Color) -> tuple[chess.Square, float, str]:
    """
    Find the worst-placed piece for the given color.
    Returns (square, score, reason).
    
    The score is negative, with more negative = worse piece.
    """
    worst_sq = None
    worst_score = float('inf')
    worst_reason = ""
    
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is None or piece.color != color:
            continue
        if piece.piece_type == chess.KING:
            continue  # King is evaluated separately
        
        score, reason = evaluate_piece_quality(board, sq, piece)
        if score < worst_score:
            worst_score = score
            worst_sq = sq
            worst_reason = reason
    
    return (worst_sq, worst_score, worst_reason)

def evaluate_piece_quality(board: chess.Board, square: chess.Square, 
                           piece: chess.Piece) -> tuple[float, str]:
    """
    Evaluate how well a piece is placed.
    Returns (score, reason) where score is in centipawns.
    """
    score = 0
    reasons = []
    
    # Mobility
    attacks = len(board.attacks(square))
    max_attacks = {chess.KNIGHT: 8, chess.BISHOP: 13, 
                   chess.ROOK: 14, chess.QUEEN: 27, chess.PAWN: 2}
    mobility_ratio = attacks / max_attacks.get(piece.piece_type, 10)
    score += mobility_ratio * 30  # Up to 30cp for full mobility
    reasons.append(f"{mobility_ratio:.0%} mobility")
    
    # Centralization (especially for knights)
    if piece.piece_type == chess.KNIGHT:
        centrality = knight_centralization_score(square)
        score += centrality * 40
        if centrality < 0.3:
            reasons.append("poorly centralized (rim)")
    
    # For bishops: same-color pawn blocking
    if piece.piece_type == chess.BISHOP:
        if is_bad_bishop(board, square, piece.color):
            score -= 40
            reasons.append("bad bishop (blocked by own pawns)")
    
    # For rooks: file quality
    if piece.piece_type == chess.ROOK:
        file_quality = rook_file_quality(board, square, piece.color)
        if file_quality == "open":
            score += 35
            reasons.append("on open file")
        elif file_quality == "semi-open":
            score += 20
            reasons.append("on semi-open file")
        elif file_quality == "closed":
            score -= 15
            reasons.append("on closed file (passive)")
    
    # Piece protection
    if not board.is_attacked_by(piece.color, square):
        if board.is_attacked_by(not piece.color, square):
            score -= 25
            reasons.append("undefended and attacked")
    
    return (score, "; ".join(reasons) if reasons else "adequate placement")
```

### The Improvement Algorithm in Action

Consider this position: White has a knight on a3, a bishop on c1, and rooks on a1 and f1. The improvement algorithm identifies:

1. **Knight on a3**: Centrality = 0.14 (very poor). This is the worst piece.
2. **Improvement plan**: Nc2-e3 or Nb5 to bring the knight to a better square
3. **After Nc2**: Centrality improves to 0.43. The knight now eyes d4 and e3.

The engine can explain: "The knight on a3 is the worst-placed piece (only 14% centralized). The move Nc2 improves the knight by bringing it closer to the center, where it will control d4 and e3."

## Piece Coordination

### More Than Individual Quality

Piece quality is not just about individual pieces—it's about **coordination**. Two well-coordinated pieces are worth more than the sum of their individual values. Examples of coordination:

- **Battery**: Rook + queen on the same file or bishop + queen on the same diagonal
- **Knight + bishop pair**: The two minor pieces complement each other, attacking squares of both colors
- **Rook doubling**: Two rooks on the same file create overwhelming pressure
- **Pawn chain + bishop**: A bishop supporting a pawn chain from behind

```python
def coordination_bonus(board: chess.Board, color: chess.Color) -> tuple[int, str]:
    """
    Calculate bonus for piece coordination.
    Returns (bonus, reason).
    """
    bonus = 0
    reasons = []
    
    # Check for battery (queen + rook on same file)
    for file_idx in range(8):
        pieces_on_file = []
        for rank in range(8):
            sq = chess.square(file_idx, rank)
            piece = board.piece_at(sq)
            if piece and piece.color == color and piece.piece_type in [chess.QUEEN, chess.ROOK]:
                pieces_on_file.append((piece, sq))
        
        if len(pieces_on_file) >= 2:
            has_queen = any(p.piece_type == chess.QUEEN for p, _ in pieces_on_file)
            has_rook = any(p.piece_type == chess.ROOK for p, _ in pieces_on_file)
            if has_queen and has_rook:
                bonus += 30
                file_name = chess.file_name(chess.square(file_idx, 0))
                reasons.append(f"battery on {file_name}-file")
    
    # Check for bishop pair
    bishops = [sq for sq in chess.SQUARES 
               if board.piece_at(sq) and 
               board.piece_at(sq).piece_type == chess.BISHOP and 
               board.piece_at(sq).color == color]
    
    if len(bishops) >= 2:
        colors = set(chess.square_color(sq) for sq in bishops)
        if len(colors) >= 2:
            bonus += 45
            reasons.append("bishop pair")
    
    return (bonus, "; ".join(reasons) if reasons else "no coordination bonus")
```

## Connecting Piece Quality to the Explanation Pipeline

The piece quality evaluation feeds directly into the [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|explanation architecture]]:

1. **Before the move**: Identify the worst piece and its quality score
2. **After the move**: Re-evaluate piece quality
3. **Delta**: If the move significantly improves the worst piece, the explanation references piece improvement
4. **Template**: "This move improves the [piece] on [square] by [how it improves]"

This creates explanations like:
- "This move improves the bad bishop on c8 by advancing the d-pawn, opening the b7-h1 diagonal"
- "The knight retreats from a3 to c2, centralizing it and giving it access to d4, e3, and b4"
- "The rook maneuvers from a1 to c1, placing it on the semi-open c-file where it can pressure c7"

These are exactly the kind of explanations a chess teacher would give—because they are grounded in the same [[07-Chess-Psychology-and-Human-Thinking/01 - Human Chess Thinking Models|human thinking models]] that guide strong play.

---

*Previous: [[07-Chess-Psychology-and-Human-Thinking/01 - Human Chess Thinking Models|01 - Human Chess Thinking Models]] ←*
*Next: [[07-Chess-Psychology-and-Human-Thinking/03 - Square Weakness and Outposts|03 - Square Weakness and Outposts]] →*
*See also: [[05-Evaluation-Functions-and-Heuristics/06 - Mobility and Piece Activity|Mobility and Piece Activity]] | [[05-Evaluation-Functions-and-Heuristics/03 - Piece-Square Tables|Piece-Square Tables]] | [[07-Chess-Psychology-and-Human-Thinking/04 - Prophylaxis|Prophylaxis]]*
