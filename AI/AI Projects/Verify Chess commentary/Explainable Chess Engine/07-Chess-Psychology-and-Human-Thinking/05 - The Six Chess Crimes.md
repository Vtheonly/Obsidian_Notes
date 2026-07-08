---
tags:
  - chapter-07
  - psychology
  - chess-crimes
  - hope-chess
  - tunnel-vision
  - prophylaxis
  - engine-detection
  - explanation-system
  - common-errors
---

# 05 - The Six Chess Crimes

## What Are the Chess Crimes?

The "chess crimes" are a set of common thinking errors that plague players of all levels. They are called "crimes" because they are *systematic* violations of correct thinking—not random blunders, but predictable patterns of faulty reasoning that recur from game to game.

Understanding these crimes is essential for our engine for two reasons:
1. **Detection**: The engine must be able to detect when a human player is committing a chess crime, so it can explain *why* a move is wrong
2. **Avoidance**: The engine itself must not commit these crimes—its move selection and evaluation should be free of these systematic errors

The crimes are not equally severe—some are merely suboptimal habits, while others are fundamental failures of reasoning that lead to losses. Each one has a specific pattern, a specific remedy, and a specific way that our engine can detect and explain it.

## Crime 1: Ignoring the Opponent's Intent

### Definition

The most fundamental chess crime is **failing to consider what the opponent wants to do**. This is the opposite of [[07-Chess-Psychology-and-Human-Thinking/04 - Prophylaxis|prophylaxis]]—instead of asking "what does my opponent want?", the player only thinks about their own plans.

### Why It's Wrong

Chess is a two-player game. Every move the opponent makes has a purpose, and ignoring that purpose means you will be repeatedly surprised and outmaneuvered. The player who ignores opponent intent is like a driver who only looks at their own lane—they will inevitably crash.

### How the Engine Detects It

The engine detects this crime by comparing the move the player chose with the prophylactic moves the engine identified. If the engine flagged a dangerous opponent plan and the player's move does nothing to address it, the player has committed Crime 1.

```python
def detect_ignoring_opponent_intent(board: chess.Board, 
                                     player_move: chess.Move) -> tuple[bool, str]:
    """
    Detect if the player ignored a significant opponent threat/plan.
    """
    analyzer = ProphylacticAnalyzer(board)
    opponent_plans = analyzer.identify_opponent_plans()
    
    if not opponent_plans:
        return (False, "")
    
    # Check if the player's move addresses the top opponent plan
    top_plan_desc, top_desired_move, urgency = opponent_plans[0]
    
    if urgency < 80:  # Not urgent enough to be a crime
        return (False, "")
    
    # Check if the player's move prevents the top plan
    board.push(player_move)
    board.push(chess.Move.null())
    can_still_execute = top_desired_move in board.legal_moves
    board.pop()
    board.pop()
    
    if can_still_execute:
        return (True, f"Ignoring opponent's plan: {top_plan_desc}. "
                f"Consider addressing this threat instead.")
    
    return (False, "")
```

### Explanation System

When Crime 1 is detected, the explanation system generates:

> " **Chess Crime: Ignoring Opponent's Intent**. Your move doesn't address the opponent's plan to [plan]. If the opponent plays [move], they will [consequence]. Consider [prophylactic move] instead."

## Crime 2: Hope Chess

### Definition

**Hope chess** is playing a move and *hoping* the opponent doesn't find the refutation, rather than verifying that the move works against all reasonable responses. It's the chess equivalent of wishful thinking.

The term comes from Kotov's analysis: a player playing "hope chess" doesn't actually calculate the consequences of their move—they just make a move that looks good and hope the opponent doesn't find the defensive resource.

### Why It's Wrong

Hope chess is wrong because it outsources your success to your opponent's failure. If you're hoping the opponent misses something, you're relying on luck rather than skill. Against a strong opponent, hope chess consistently fails because they *will* find the refutation.

### How the Engine Detects It

The engine detects hope chess by analyzing whether the player's move has a refutation within the engine's search depth. If the engine finds a strong response for the opponent that the player apparently didn't consider, it flags hope chess.

```python
def detect_hope_chess(board: chess.Board, player_move: chess.Move,
                       engine_search_depth: int = 8) -> tuple[bool, str]:
    """
    Detect if the player is playing 'hope chess' — making a move
    that has a refutation the player apparently didn't consider.
    """
    board.push(player_move)
    
    # Search for the opponent's best response
    best_response, response_score = search_best_move(
        board, depth=engine_search_depth
    )
    
    board.pop()
    
    # If the opponent has a strong response, the player might be
    # playing hope chess
    if response_score < -100:  # Opponent can get +1.00 advantage
        # Check if this refutation is non-obvious
        if not is_obvious_move(best_response):
            return (True, f"After {board.san(player_move)}, the opponent has "
                    f"a strong response: {board.san(best_response)}. "
                    f"Did you consider this?")
    
    return (False, "")

def is_obvious_move(move: chess.Move) -> bool:
    """Check if a refutation is obvious (captures, checks, etc.)."""
    if board.is_capture(move):
        return True
    board.push(move)
    if board.is_check():
        board.pop()
        return True
    board.pop()
    return False
```

### Explanation System

> " **Chess Crime: Hope Chess**. Your move assumes the opponent won't find the best response, which is [response]. This response gives the opponent an advantage because [reason]. Always verify your moves against the opponent's best play."

## Crime 3: Tunnel Vision

### Definition

**Tunnel vision** is the tendency to focus on one part of the board or one plan to the exclusion of everything else. The player becomes so fixated on their chosen plan that they miss better alternatives on the other side of the board.

### Why It's Wrong

Tunnel vision violates Kotov's principle of generating *all* candidate moves before evaluating them. A player with tunnel vision might find the best move in their tunnel—but miss a clearly better move elsewhere.

### How the Engine Detects It

The engine detects tunnel vision by comparing the player's move with the engine's top choices. If the player's move is on a completely different part of the board from a much better alternative, tunnel vision is likely.

```python
def detect_tunnel_vision(board: chess.Board, player_move: chess.Move,
                          engine_top_moves: list[tuple[chess.Move, int]]) -> tuple[bool, str]:
    """
    Detect tunnel vision: the player focused on one area while
    a much better move exists elsewhere.
    """
    if not engine_top_moves:
        return (False, "")
    
    best_move, best_score = engine_top_moves[0]
    player_score = get_move_score(board, player_move)
    
    # If the player's move is significantly worse than the best
    if best_score - player_score > 100:  # More than 1 pawn worse
        
        # Check if the moves are on different parts of the board
        player_file = chess.square_file(player_move.from_square)
        best_file = chess.square_file(best_move.from_square)
        
        if abs(player_file - best_file) >= 3:
            return (True, f"Tunnel vision on the {'queenside' if player_file < 4 else 'kingside'}. "
                    f"Consider the {'kingside' if player_file < 4 else 'queenside'} move "
                    f"{board.san(best_move)} which is significantly better.")
    
    return (False, "")
```

### Explanation System

> " **Chess Crime: Tunnel Vision**. You're focused on the [queenside/kingside/center] but the best move is on the other side of the board: [best_move]. This move is better because [reason]. Remember to scan the entire board before deciding."

## Crime 4: Control Fallacy

### Definition

The **control fallacy** is the mistaken belief that because you *can* do something, you *should* do it. In chess, this manifests as playing an aggressive move simply because it's available, without considering whether it actually improves your position.

Common examples:
- Attacking a well-defended piece just because you can
- Advancing a pawn because the square in front is empty, without considering the weaknesses created
- Initiating a trade because it's available, even though the trade benefits the opponent

### Why It's Wrong

The control fallacy ignores the fundamental question: "Does this move *improve my position*?" The mere availability of a move does not make it good. In fact, aggressive moves that don't improve the position often make it *worse* by creating weaknesses, losing tempos, or activating the opponent's pieces.

### How the Engine Detects It

```python
def detect_control_fallacy(board: chess.Board, player_move: chess.Move) -> tuple[bool, str]:
    """
    Detect the control fallacy: making a move because it's available
    rather than because it's good.
    """
    # Evaluate the position before and after the move
    score_before = static_evaluation(board)
    board.push(player_move)
    score_after = static_evaluation(board)
    board.pop()
    
    # If the move makes the position worse, it might be a control fallacy
    if score_after < score_before - 30:  # At least 0.3 pawns worse
        
        # Check if the move was "tempting" (aggressive-looking)
        is_tempting = (
            board.is_capture(player_move) or
            gives_check(board, player_move) or
            attacks_valuable_piece(board, player_move)
        )
        
        if is_tempting:
            return (True, f"The move {board.san(player_move)} looks tempting but "
                    f"actually worsens your position by {score_before - score_after}cp. "
                    f"Just because you can make this move doesn't mean you should.")
    
    return (False, "")
```

### Explanation System

> " **Chess Crime: Control Fallacy**. This move is available but not good. Just because you can [attack/capture/advance] doesn't mean you should. This move actually worsens your position because [reason]. Look for moves that genuinely improve your position instead."

## Crime 5: Mindless Exchanges

### Definition

**Mindless exchanges** are trades made without strategic purpose—exchanging pieces simply because the opportunity exists, without considering whether the exchange benefits you or the opponent.

This crime is extremely common at amateur levels. Players exchange pieces reflexively, as if "trading" were an inherent good. But every exchange changes the character of the position, and some exchanges are deeply unfavorable.

### When Exchanges Are Good vs. Bad

| Exchange Is Good When... | Exchange Is Bad When... |
|--------------------------|------------------------|
| You're exchanging a bad piece for a good one | You're exchanging a good piece for a bad one |
| You're simplifying when ahead in material | You're simplifying when behind in material |
| The exchange opens lines for your attack | The exchange opens lines for the opponent's attack |
| You're removing the opponent's best piece | You're removing the opponent's worst piece |
| The resulting endgame favors you | The resulting endgame favors the opponent |
| You're eliminating a defender | You're eliminating an attacker needlessly |

### How the Engine Detects It

```python
def detect_mindless_exchange(board: chess.Board, player_move: chess.Move) -> tuple[bool, str]:
    """
    Detect mindless exchanges: trades that benefit the opponent.
    """
    if not board.is_capture(player_move):
        return (False, "")
    
    # Evaluate the pieces being exchanged
    attacker = board.piece_at(player_move.from_square)
    defender = board.piece_at(player_move.to_square)
    
    if attacker is None or defender is None:
        return (False, "")
    
    # Is the attacker a good piece for us?
    attacker_quality, _ = evaluate_piece_quality(board, player_move.from_square, attacker)
    
    # Is the defender a bad piece for the opponent?
    # (We'd want to exchange their GOOD piece, not their bad one)
    
    # After the exchange, will our position be worse?
    board.push(player_move)
    # The opponent might recapture
    recaptures = [m for m in board.legal_moves if board.is_capture(m) 
                  and m.to_square == player_move.to_square]
    
    if recaptures:
        board.push(recaptures[0])  # Assume the best recapture
        score_after = static_evaluation(board)
        board.pop()
    else:
        score_after = static_evaluation(board)
    
    board.pop()
    score_before = static_evaluation(board)
    
    # If the exchange makes us worse and the attacker was a good piece
    if score_after < score_before - 30 and attacker_quality > 0:
        return (True, f"Exchanging the {chess.piece_name(attacker.piece_type)} benefits "
                f"the opponent. This is a good {'white' if attacker.color else 'black'} "
                f"piece — consider keeping it on the board.")
    
    return (False, "")
```

### Explanation System

> " **Chess Crime: Mindless Exchange**. Trading your [piece] for the opponent's [piece] actually helps the opponent because [reason]. Your [piece] was well-placed [reason], while the opponent's [piece] was not a significant factor. Consider keeping your piece on the board."

## Crime 6: Defensive-Looking Moves That Aren't Defensive

### Definition

This crime is playing a move that *looks* defensive but doesn't actually solve the defensive problem. The player has the right instinct (they recognize they need to defend) but the wrong execution (their "defensive" move doesn't actually defend).

Common examples:
- Moving a piece to block a threat, but the threat can simply be renewed with tempo
- Moving the king to a square that looks safe but is actually vulnerable to a different attack
- Defending a piece that's about to be captured, but the defense can be overwhelmed

### Why It's Wrong

A defensive move that doesn't actually defend is worse than no defense at all, because it wastes a tempo and gives the illusion of safety. The player thinks they've addressed the threat and stops worrying about it, when in fact the threat is still present.

### How the Engine Detects It

```python
def detect_false_defense(board: chess.Board, player_move: chess.Move,
                          threat_before: tuple[chess.Move, str, int]) -> tuple[bool, str]:
    """
    Detect defensive-looking moves that don't actually solve the problem.
    """
    _, threat_type, threat_severity = threat_before
    
    if threat_severity < 50:
        return (False, "")
    
    # Check if the threat still exists after the player's move
    board.push(player_move)
    
    # Re-analyze threats
    threat_matrix_after = ThreatMatrix(board)
    threat_matrix_after.build()
    remaining_threats = threat_matrix_after.most_dangerous_threats()
    
    board.pop()
    
    # If significant threats still exist, the "defense" didn't work
    if remaining_threats and remaining_threats[0][2] >= threat_severity * 0.7:
        return (True, f"Your move looks defensive, but the threat of "
                f"{threat_type} still exists. {remaining_threats[0][1]} "
                f"is still a serious concern. Look for a more thorough defense.")
    
    return (False, "")
```

### Explanation System

> " **Chess Crime: False Defense**. Your move addresses the threat superficially but doesn't solve the underlying problem. The opponent can still [threat/plan] because [reason]. A better defense would be [alternative move], which fully addresses the threat."

## Crime 7: Knights on the Rim

### Definition

"A knight on the rim is dim" — placing a knight on the edge of the board (a-file, h-file, 1st rank, 8th rank) where it controls far fewer squares and has less influence on the game. This is a specific instance of the broader principle discussed in [[07-Chess-Psychology-and-Human-Thinking/02 - Feeling for the Pieces|Feeling for the Pieces]], but it's common enough and important enough to be listed as a separate crime.

### Why It's Wrong

The numbers speak for themselves:
- **Knight on a1/h1/a8/h8**: Controls 2 squares
- **Knight on b1/g1/b8/g8**: Controls 3-4 squares
- **Knight on c3/f3/c6/f6**: Controls 6-8 squares
- **Knight on d4/e4/d5/e5**: Controls 8 squares

A knight on the rim is roughly 3-4 times less powerful than a centralized knight. This is not a small difference—it's the difference between a dominant piece and a nearly useless one.

### How the Engine Detects It

```python
def detect_rim_knight(board: chess.Board, player_move: chess.Move) -> tuple[bool, str]:
    """
    Detect when a move places a knight on the rim.
    """
    piece = board.piece_at(player_move.from_square)
    if piece is None or piece.piece_type != chess.KNIGHT:
        return (False, "")
    
    to_file = chess.square_file(player_move.to_square)
    to_rank = chess.square_rank(player_move.to_square)
    
    is_on_rim = (to_file == 0 or to_file == 7 or to_rank == 0 or to_rank == 7)
    
    if is_on_rim:
        from_file = chess.square_file(player_move.from_square)
        from_rank = chess.square_rank(player_move.from_square)
        
        # Check if the knight was coming from a better position
        from_centrality = knight_centralization_score(player_move.from_square)
        to_centrality = knight_centralization_score(player_move.to_square)
        
        if from_centrality > to_centrality:
            return (True, f"Moving the knight to {chess.square_name(player_move.to_square)} "
                    f"places it on the rim where it controls fewer squares. "
                    f"'A knight on the rim is dim' — look for a centralized square instead.")
    
    return (False, "")
```

### Explanation System

> " **Chess Crime: Knight on the Rim**. Placing the knight on [square] puts it on the edge of the board where it controls only [N] squares, compared to [M] squares from a central position. Knights belong in the center—look for alternative squares like [central_square]."

## Summary: The Chess Crimes and Their Detection

| Crime | Core Error | Detection Method | Explanation Priority |
|-------|-----------|-----------------|---------------------|
| 1. Ignoring Opponent's Intent | Not asking "what does my opponent want?" | [[07-Chess-Psychology-and-Human-Thinking/04 - Prophylaxis|Prophylactic analyzer]] | High — critical thinking flaw |
| 2. Hope Chess | Not verifying against best response | [[02-Search-Algorithms/01 - Minimax Algorithm|Search-based refutation]] | High — leads to losses |
| 3. Tunnel Vision | Focusing on one area only | Move comparison | Medium — limits options |
| 4. Control Fallacy | Doing something because you can | [[05-Evaluation-Functions-and-Heuristics/01 - Static Evaluation Overview|Static evaluation delta]] | Medium — common amateur error |
| 5. Mindless Exchanges | Trading without purpose | [[07-Chess-Psychology-and-Human-Thinking/02 - Feeling for the Pieces|Piece quality comparison]] | Medium — very common |
| 6. False Defense | Defensive moves that don't defend | [[05-Evaluation-Functions-and-Heuristics/07 - Threats and Tactical Patterns|Threat matrix comparison]] | High — gives false security |
| 7. Knights on the Rim | Poor knight placement | [[07-Chess-Psychology-and-Human-Thinking/02 - Feeling for the Pieces|Centralization scoring]] | Low — specific positional error |

The chess crimes module is integrated into the [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|explanation pipeline]] as a post-hoc analysis: after the engine selects and explains its move, it also checks the player's move for chess crimes and generates warnings accordingly. This turns the engine from a pure move-recommender into a **chess teacher** that helps the player improve their thinking process.

---

*Previous: [[07-Chess-Psychology-and-Human-Thinking/04 - Prophylaxis|04 - Prophylaxis]] ←*
*Next: [[07-Chess-Psychology-and-Human-Thinking/06 - Tactical Blindness Patterns|06 - Tactical Blindness Patterns]] →*
*See also: [[07-Chess-Psychology-and-Human-Thinking/01 - Human Chess Thinking Models|Human Chess Thinking Models]] | [[07-Chess-Psychology-and-Human-Thinking/02 - Feeling for the Pieces|Feeling for the Pieces]] | [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]]*
