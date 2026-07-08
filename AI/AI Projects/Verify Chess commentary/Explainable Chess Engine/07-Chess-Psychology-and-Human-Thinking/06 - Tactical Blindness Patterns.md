---
tags:
  - chapter-07
  - psychology
  - tactical-blindness
  - sniper-blindness
  - lpdo
  - discovered-attack
  - alignment
  - extension-rules
  - search-extensions
---

# 06 - Tactical Blindness Patterns

## Why Humans Miss Tactics

Even strong players miss tactics. It's not because they can't calculate—it's because they don't *look*. Tactical blindness is a failure of **perception**, not calculation. The player's search algorithm works correctly, but it searches the wrong part of the game tree because the critical move doesn't register as a candidate.

Understanding tactical blindness patterns is essential for our engine because:
1. **Extension rules**: The engine should search *deeper* in positions where humans are likely to be blind
2. **Explanation**: The engine should specifically warn about patterns that cause blindness
3. **Move ordering**: Moves that exploit blindness patterns should be ordered higher

This note catalogs the major patterns of tactical blindness and describes how our engine's [[06-Adaptive-Depth-Control/03 - Depth Extension Rules|depth extension rules]] counter each one.

## Sniper Blindness: Long-Range Corner Pieces

### The Pattern

**Sniper blindness** is the failure to notice a long-range piece (bishop, rook, queen) positioned in a distant corner of the board that has a clear line of attack. The name comes from the image of a "sniper" hidden in the corner, whose attack is invisible until it's too late.

This is one of the most common and devastating forms of tactical blindness. The human visual system naturally focuses on the center of the board and the area around the kings. A bishop on h1 or a rook on a8 that has a clear diagonal/file to a critical square often goes unnoticed because the player simply doesn't "see" that far.

### Why It Happens

1. **Peripheral neglect**: Players don't look at the corners of the board regularly
2. **Distance discounting**: The farther a piece is from the action, the less likely a player is to consider its influence
3. **Visual field limitation**: The board's geometry makes it hard to trace long diagonal/file lines visually
4. **Pattern rarity**: Sniper attacks are less common than central tactics, so players don't have strong patterns for them

### Formal Definition

A **sniper attack** occurs when:

$$\text{Sniper}(B, s_{\text{target}}) \iff \text{Piece}(B, s_{\text{sniper}}) \in \{\text{Bishop}, \text{Rook}, \text{Queen}\} \wedge \text{Line}(s_{\text{sniper}}, s_{\text{target}}) \wedge \text{ClearPath}(B, s_{\text{sniper}}, s_{\text{target}}) \wedge \text{Distance}(s_{\text{sniper}}, s_{\text{target}}) \geq 4$$

Where:
- $B$ is the board state
- $s_{\text{sniper}}$ is the square of the attacking piece
- $s_{\text{target}}$ is the target square
- $\text{Line}$ means the squares are on the same rank, file, or diagonal
- $\text{ClearPath}$ means no pieces block the line of attack
- $\text{Distance} \geq 4$ means the attack crosses at least 4 squares

### Detection Code

```python
def detect_sniper_threats(board: chess.Board, color: chess.Color) -> list[tuple[chess.Square, chess.Square, str]]:
    """
    Detect all sniper threats — long-range pieces in corners/far edges
    with clear lines to critical squares.
    
    Returns list of (sniper_square, target_square, piece_type).
    """
    snipers = []
    
    # Corner and edge squares where snipers hide
    corner_squares = [chess.A1, chess.H1, chess.A8, chess.H8]
    edge_squares = [sq for sq in chess.SQUARES 
                    if chess.square_file(sq) in [0, 7] or chess.square_rank(sq) in [0, 7]]
    
    for sniper_sq in edge_squares:
        piece = board.piece_at(sniper_sq)
        if piece is None or piece.color != color:
            continue
        
        if piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            continue
        
        # Find all squares this piece attacks
        attacks = board.attacks(sniper_sq)
        
        for target_sq in attacks:
            distance = chess.square_distance(sniper_sq, target_sq)
            if distance < 4:
                continue
            
            # Check if the target is significant (enemy piece, near enemy king)
            target_piece = board.piece_at(target_sq)
            enemy_king = board.king(not color)
            
            is_significant = (
                (target_piece and target_piece.color != color) or
                (enemy_king and chess.square_distance(target_sq, enemy_king) <= 1) or
                target_sq in [chess.D4, chess.E4, chess.D5, chess.E5]  # Center
            )
            
            if is_significant:
                snipers.append((sniper_sq, target_sq, chess.piece_name(piece.piece_type)))
    
    return snipers
```

### How Extension Rules Counter Sniper Blindness

When a sniper threat is detected, the engine applies a **sniper extension** to ensure the threat is fully explored:

```python
class SniperExtensionRule(DepthRule):
    """
    Extend search depth when a sniper piece has a clear line
    to a critical square.
    """
    name = "Sniper Extension"
    description = "Extends depth when long-range corner pieces threaten critical squares"
    
    def evaluate(self, board: chess.Board, move: chess.Move) -> tuple[int, str]:
        sniper_threats = detect_sniper_threats(board, not board.turn)
        
        if sniper_threats:
            # Extend by 1 ply for each significant sniper threat
            extension = min(len(sniper_threats), 2)  # Cap at 2 extra plies
            descriptions = [f"{pt} on {chess.square_name(sq)} targeting "
                          f"{chess.square_name(tsq)}" for sq, tsq, pt in sniper_threats[:2]]
            reason = f"Sniper threat: {'; '.join(descriptions)}"
            return (extension, reason)
        
        return (0, "")
```

## LPDO: Loose Pieces Drop Off

### The Pattern

**LPDO** (Loose Pieces Drop Off) is one of the most important tactical principles: **undefended pieces are tactical targets**. If a piece is not defended by another piece, it can be captured, attacked, or used as the basis for a fork, pin, or skewer.

The LPDO principle is simple but devastatingly effective. At amateur levels, the majority of tactical losses come from leaving pieces undefended. Even at master level, a momentary LPDO can be exploited.

### Why Humans Miss LPDOs

1. **Defensive neglect**: Players focus on their own plans and forget to check if their pieces are defended
2. **Recapture assumption**: "Even if it's attacked, I can recapture" — but what if the recapture hangs another piece?
3. **Complex positions**: In positions with many pieces, it's hard to verify that every piece is defended
4. **Focusing on attackers**: Players notice what their pieces attack, but not what's attacking their pieces

### Formal Definition

A piece is **loose** (LPDO) if:

$$\text{LPDO}(B, s) \iff \text{Piece}(B, s) \wedge \neg\text{Defended}(B, s) \wedge \text{AttackedBy}(B, s, \text{opponent})$$

The LPDO score for a position counts the number and value of loose pieces:

$$\text{LPDO\_Score}(B, \text{color}) = \sum_{s \in \text{Loose}(B, \text{color})} \text{Value}(\text{Piece}(B, s))$$

### Detection Code

```python
def find_loose_pieces(board: chess.Board, color: chess.Color) -> list[tuple[chess.Square, chess.Piece, int]]:
    """
    Find all loose (undefended) pieces for the given color.
    Returns list of (square, piece, value).
    """
    loose = []
    
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is None or piece.color != color:
            continue
        
        # Skip pawns and king for LPDO purposes
        if piece.piece_type in [chess.PAWN, chess.KING]:
            continue
        
        # Check if the piece is defended
        is_defended = board.is_attacked_by(color, sq)
        is_attacked = board.is_attacked_by(not color, sq)
        
        if not is_defended and is_attacked:
            value = PIECE_VALUES.get(piece.piece_type, 0)
            loose.append((sq, piece, value))
    
    return loose

def lpdo_score(board: chess.Board, color: chess.Color) -> tuple[int, str]:
    """
    Calculate the LPDO vulnerability score for the given color.
    """
    loose = find_loose_pieces(board, color)
    
    if not loose:
        return (0, "No loose pieces")
    
    total_value = sum(v for _, _, v in loose)
    
    descriptions = []
    for sq, piece, value in loose:
        descriptions.append(
            f"undefended {chess.piece_name(piece.piece_type)} on {chess.square_name(sq)} "
            f"(value: {value}cp)"
        )
    
    reason = "Loose pieces: " + "; ".join(descriptions)
    return (total_value, reason)
```

### LPDO as an Extension Trigger

When LPDO pieces exist, the engine extends search depth because the position is tactically volatile:

```python
class LPDOExtensionRule(DepthRule):
    """
    Extend search depth when there are loose pieces that could
    drop off (be captured or exploited tactically).
    """
    name = "LPDO Extension"
    description = "Extends depth when undefended pieces are present"
    
    def evaluate(self, board: chess.Board, move: chess.Move) -> tuple[int, str]:
        # Check LPDO for both sides
        our_loose = find_loose_pieces(board, board.turn)
        their_loose = find_loose_pieces(board, not board.turn)
        
        total_loose_value = (sum(v for _, _, v in our_loose) + 
                           sum(v for _, _, v in their_loose))
        
        if total_loose_value > 0:
            # Extend by 1 ply for significant LPDO situations
            extension = 1 if total_loose_value >= 300 else 0
            reason = f"LPDO: {len(our_loose) + len(their_loose)} undefended pieces (total value: {total_loose_value}cp)"
            return (extension, reason)
        
        return (0, "")
```

## Discovered Attack Pattern

### The Pattern

A **discovered attack** occurs when moving one piece reveals an attack by another piece behind it. This is one of the most dangerous tactical motifs because:

1. The move that creates the discovery often has its own purpose (making it doubly dangerous)
2. The discovered attack was not visible before the move, so the opponent doesn't prepare for it
3. The "screen" piece (the one that moves) can go anywhere useful, creating multiple threats

### Why Humans Miss Discovered Attacks

1. **Invisible before the move**: The attack literally doesn't exist until the screen piece moves
2. **Cognitive load**: The player must think about TWO threats simultaneously (the screen piece's destination and the revealed attack)
3. **Pattern rarity at amateur level**: Discovered attacks are less common than direct attacks, so the pattern is less ingrained

### Detection Code

```python
def detect_discovered_attack_potential(board: chess.Board, 
                                        color: chess.Color) -> list[tuple[chess.Square, chess.Square, chess.SquareSet]]:
    """
    Detect potential discovered attacks.
    A discovered attack exists when a piece can move to reveal
    an attack by a piece behind it.
    
    Returns list of (screen_square, attacker_square, attack_squares).
    """
    discoveries = []
    
    for screen_sq in chess.SQUARES:
        screen_piece = board.piece_at(screen_sq)
        if screen_piece is None or screen_piece.color != color:
            continue
        
        # Check if removing the screen piece would reveal an attack
        # along any line (rank, file, diagonal)
        
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0),  # Rook directions
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Bishop directions
            # Look behind the screen piece in this direction
            df, dr = direction
            file = chess.square_file(screen_sq) + df
            rank = chess.square_rank(screen_sq) + dr
            
            while 0 <= file <= 7 and 0 <= rank <= 7:
                behind_sq = chess.square(file, rank)
                behind_piece = board.piece_at(behind_sq)
                
                if behind_piece is not None:
                    if behind_piece.color == color and behind_piece.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                        # Found a potential attacker behind the screen
                        # Check what it would attack if the screen moved
                        # (This is simplified; full implementation would check
                        # specific screen piece moves)
                        discoveries.append((screen_sq, behind_sq, 
                                          board.attacks(behind_sq) if screen_sq not in chess.SquareSet(board.attacks(behind_sq)) else chess.SquareSet()))
                    break  # Blocked by this piece
                
                file += df
                rank += dr
    
    return discoveries
```

### Discovered Attack Extension

```python
class DiscoveredAttackExtensionRule(DepthRule):
    """
    Extend search when a discovered attack is possible.
    """
    name = "Discovered Attack Extension"
    description = "Extends depth when a discovered attack pattern exists"
    
    def evaluate(self, board: chess.Board, move: chess.Move) -> tuple[int, str]:
        discoveries = detect_discovered_attack_potential(board, board.turn)
        
        if discoveries:
            # Check if the actual move IS a discovery
            screen_sq = move.from_square
            is_discovery = any(sq == screen_sq for sq, _, _ in discoveries)
            
            if is_discovery:
                return (1, "Discovered attack: moving this piece reveals an attack")
        
        return (0, "")
```

## Alignment Sensitivity

### The Pattern

**Alignment** refers to pieces (of the same color or different colors) that are arranged on the same rank, file, or diagonal. Alignments are the raw material for pins, skewers, x-rays, and discovered attacks. A player who is "alignment-sensitive" sees these tactical possibilities naturally; a player who isn't will miss them.

### Why Humans Miss Alignments

1. **Visual scanning**: Tracing long diagonals and files across the entire board is cognitively expensive
2. **Attention focus**: Players focus on the area around the kings and the center, missing alignments on the periphery
3. **Color blindness**: Players who don't regularly check "are my pieces on the same diagonal?" will miss bishop alignments
4. **Recency bias**: Players are more likely to notice alignments created by their last move than alignments that have existed for several moves

### Alignment Detection

```python
def detect_alignments(board: chess.Board) -> list[tuple[str, list[chess.Square]]]:
    """
    Detect all significant alignments on the board.
    An alignment is a set of pieces on the same rank, file, or diagonal.
    
    Returns list of (alignment_type, squares) tuples.
    """
    alignments = []
    
    # Check files
    for file_idx in range(8):
        pieces_on_file = []
        for rank_idx in range(8):
            sq = chess.square(file_idx, rank_idx)
            piece = board.piece_at(sq)
            if piece:
                pieces_on_file.append(sq)
        
        if len(pieces_on_file) >= 3:  # 3+ pieces on same file = potential pin/skewer
            alignments.append(("file", pieces_on_file))
    
    # Check ranks
    for rank_idx in range(8):
        pieces_on_rank = []
        for file_idx in range(8):
            sq = chess.square(file_idx, rank_idx)
            piece = board.piece_at(sq)
            if piece:
                pieces_on_rank.append(sq)
        
        if len(pieces_on_rank) >= 3:
            alignments.append(("rank", pieces_on_rank))
    
    # Check diagonals
    for diag_idx in range(-7, 8):
        pieces_on_diag = []
        for i in range(8):
            file_idx = i
            rank_idx = i + diag_idx
            if 0 <= file_idx <= 7 and 0 <= rank_idx <= 7:
                sq = chess.square(file_idx, rank_idx)
                piece = board.piece_at(sq)
                if piece:
                    pieces_on_diag.append(sq)
        
        if len(pieces_on_diag) >= 3:
            alignments.append(("diagonal", pieces_on_diag))
    
    # Anti-diagonals
    for diag_idx in range(-7, 8):
        pieces_on_diag = []
        for i in range(8):
            file_idx = i
            rank_idx = 7 - i + diag_idx
            if 0 <= file_idx <= 7 and 0 <= rank_idx <= 7:
                sq = chess.square(file_idx, rank_idx)
                piece = board.piece_at(sq)
                if piece:
                    pieces_on_diag.append(sq)
        
        if len(pieces_on_diag) >= 3:
            alignments.append(("anti-diagonal", pieces_on_diag))
    
    return alignments

def alignment_threat_score(board: chess.Board) -> tuple[int, str]:
    """
    Score the tactical danger from piece alignments.
    Higher score = more alignment-based tactical opportunities.
    """
    alignments = detect_alignments(board)
    score = 0
    threats = []
    
    for align_type, squares in alignments:
        # Check for pins: same-color pieces lined up with enemy slider
        # Check for skewers: same pattern from the other direction
        # Check for x-rays: piece attacking through another piece
        
        for i, sq1 in enumerate(squares):
            for sq2 in squares[i+1:]:
                piece1 = board.piece_at(sq1)
                piece2 = board.piece_at(sq2)
                
                if piece1.color != piece2.color:
                    # Different colors on same line = potential pin/skewer
                    if piece1.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                        # piece1 is attacking piece2 (or through it)
                        score += 15
                        threats.append(
                            f"{chess.piece_name(piece1.piece_type)} on {chess.square_name(sq1)} "
                            f"pins/x-rays {chess.piece_name(piece2.piece_type)} on {chess.square_name(sq2)}"
                        )
    
    return (score, "; ".join(threats[:3]) if threats else "No alignment threats")
```

## The Extension Rule Hierarchy

### How Blindness Patterns Drive Search Depth

The various blindness patterns feed into the [[06-Adaptive-Depth-Control/03 - Depth Extension Rules|depth extension system]] as a coordinated set. When multiple blindness patterns are present, the extensions compound, ensuring that the engine searches deeply in positions where humans are most likely to err:

```python
def compute_blindness_extensions(board: chess.Board, move: chess.Move) -> tuple[int, list[str]]:
    """
    Compute total depth extension from tactical blindness patterns.
    """
    total_extension = 0
    all_reasons = []
    
    # Sniper extension
    sniper_ext, sniper_reason = SniperExtensionRule().evaluate(board, move)
    if sniper_ext > 0:
        total_extension += sniper_ext
        all_reasons.append(sniper_reason)
    
    # LPDO extension
    lpdo_ext, lpdo_reason = LPDOExtensionRule().evaluate(board, move)
    if lpdo_ext > 0:
        total_extension += lpdo_ext
        all_reasons.append(lpdo_reason)
    
    # Discovered attack extension
    disc_ext, disc_reason = DiscoveredAttackExtensionRule().evaluate(board, move)
    if disc_ext > 0:
        total_extension += disc_ext
        all_reasons.append(disc_reason)
    
    # Cap total extension
    total_extension = min(total_extension, 4)  # Maximum 4 extra plies
    
    return (total_extension, all_reasons)
```

## Connecting Blindness Patterns to Explanations

When the engine explains a move, it can reference the blindness pattern as part of the explanation:

- **Sniper**: "Watch out for the bishop on h3 — it has a clear diagonal to your king. This move blocks the diagonal and prevents the sniper threat."
- **LPDO**: "Your knight on c3 was undefended and could be captured. This move defends it by placing the bishop on d2."
- **Discovered attack**: "This move creates a discovered attack: moving the knight reveals the rook's attack on the queen."
- **Alignment**: "Your queen and rook are on the same file, creating a potential pin. This move breaks the alignment."

These explanations serve a dual purpose: they explain why the engine chose a move, and they help the player recognize the pattern in future positions. This is the core of the engine's educational value—turning tactical blindness into tactical awareness.

---

*Previous: [[07-Chess-Psychology-and-Human-Thinking/05 - The Six Chess Crimes|05 - The Six Chess Crimes]] ←*
*Next: [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|08 - Rule Engine Architecture]] →*
*See also: [[05-Evaluation-Functions-and-Heuristics/07 - Threats and Tactical Patterns|Threats and Tactical Patterns]] | [[06-Adaptive-Depth-Control/03 - Depth Extension Rules|Depth Extension Rules]] | [[07-Chess-Psychology-and-Human-Thinking/01 - Human Chess Thinking Models|Human Chess Thinking Models]]*
