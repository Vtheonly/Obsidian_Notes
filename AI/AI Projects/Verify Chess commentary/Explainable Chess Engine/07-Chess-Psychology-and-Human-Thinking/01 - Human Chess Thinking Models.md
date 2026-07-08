---
tags:
  - chapter-07
  - psychology
  - human-thinking
  - candidate-moves
  - kotov
  - intuition
  - pattern-recognition
  - calculation
  - im-gm-process
---

# 01 - Human Chess Thinking Models

## How Humans Actually Think About Chess

Understanding how humans think about chess is not merely an academic exercise—it is the **foundational prerequisite** for building an engine that can explain its moves in human terms. A chess engine that only speaks in terms of search trees, alpha-beta bounds, and centipawn scores might be strong, but it cannot teach, it cannot reason, and it cannot connect with the player sitting at the board. Our engine must bridge the gap between machine computation and human understanding, and that bridge starts with faithfully modeling how strong players actually think.

The human chess thinking process is fundamentally different from the brute-force search that computers use. While a computer evaluates millions of positions per second, a human evaluates only a handful—but each evaluation is far richer, incorporating pattern recognition, strategic understanding, emotional assessment, and intuitive weighting. This difference is not just quantitative; it is **qualitative**. A grandmaster's thought process involves layers of meaning that no raw search tree can capture.

Consider the difference in information density. When Stockfish evaluates a position at +1.5, it has compressed millions of leaf-node evaluations into a single number. When a grandmaster evaluates the same position as "slightly better for White due to the knight outpost and Black's weakened queenside pawns," the evaluation contains *explanatory structure*—it identifies the features that matter and names them. Our engine's goal is to produce the latter type of evaluation while maintaining the accuracy of the former.

## Candidate Move Generation: Kotov's Tree of Analysis

### The Concept

In his influential 1971 book *Think Like a Grandmaster*, Alexander Kotov proposed a structured thinking method that has become one of the most widely taught frameworks in chess pedagogy:

1. **Generate all candidate moves**: Look at the position and identify every move that could possibly be good
2. **Evaluate each candidate systematically**: Calculate the consequences of each candidate move, one at a time, without jumping between them
3. **Choose the best**: Based on the evaluation, select the move that leads to the best outcome

Kotov emphasized that the key mistake is **not** the failure to calculate deeply, but the failure to consider the right moves in the first place. A player who generates three strong candidates and evaluates them accurately will make a better decision than a player who generates one candidate and evaluates it perfectly. The candidate move generation step is where intuition and pattern recognition play their most critical role—they determine which branches of the enormous game tree are worth exploring.

```
Position Analysis
├── Candidate Move A (Nf5)
│   ├── Response A1 (gxh6) → Evaluate → +2.0
│   ├── Response A2 (Kh8)  → Evaluate → +1.5
│   └── Response A3 (Nd7)  → Evaluate → +1.8
├── Candidate Move B (Rae1)
│   ├── Response B1 (Rad8) → Evaluate → +0.5
│   └── Response B2 (b5)   → Evaluate → +0.3
└── Candidate Move C (a4)
    └── Response C1 (b4)   → Evaluate → +0.1
```

### The "Tree of Analysis" Problem

Kotov also identified the problem of **analytical drift**: players who start evaluating one candidate, get distracted by an interesting variation, and then jump to analyzing a different candidate without finishing the first. This leads to shallow, incomplete analysis of all candidates rather than thorough analysis of any. Kotov called this "playing hope chess"—hoping that the move works without actually verifying it through calculation.

The human tendency toward analytical drift explains why structured thinking methods are so important. Without discipline, the mind naturally wanders to the most tactically interesting line, leaving strategically important alternatives unexplored. This is one reason why computers, which never suffer from analytical drift, can find moves that humans miss—not because the human can't calculate them, but because the human never *considered* them.

### Engine Implementation of Kotov's Method

Our engine's [[06-Adaptive-Depth-Control/02 - Root-Level Selectivity|root-level selectivity]] directly implements Kotov's method: generate all legal moves, sort them by heuristic quality, and allocate search depth based on estimated importance. The move ordering ensures that the most promising candidates are evaluated first and most deeply:

```python
def generate_candidate_moves(board: chess.Board) -> list[chess.Move]:
    """
    Generate and rank candidate moves using Kotov's principle.
    
    Phase 1: Generate ALL legal moves (don't skip any candidate)
    Phase 2: Rank by heuristic promise (intuition)
    Phase 3: Allocate search depth by rank (calculation budget)
    """
    all_moves = list(board.legal_moves)
    
    # Phase 2: Rank by heuristic promise
    scored_moves = []
    for move in all_moves:
        score = heuristic_move_score(board, move)
        scored_moves.append((move, score))
    
    scored_moves.sort(key=lambda x: x[1], reverse=True)
    
    return [move for move, score in scored_moves]

def heuristic_move_score(board: chess.Board, move: chess.Move) -> float:
    """Quick heuristic scoring for move ordering (intuition phase)."""
    score = 0.0
    
    # Checks are always promising
    board.push(move)
    if board.is_check():
        score += 1000.0
    board.pop()
    
    # Captures scored by MVV-LVA
    if board.is_capture(move):
        score += mvv_lva_score(board, move)
    
    # Promotions
    if move.promotion:
        score += 800.0
    
    # Piece-Square Table improvement
    score += pst_delta(board, move)
    
    return score
```

## The "Checks, Captures, Threats" Priority System

### The CCT Method

A simplified and highly effective version of candidate move generation, popularized by chess coaches worldwide, is the **CCT** (Checks, Captures, Threats) method:

1. **Checks**: Always look at forcing moves first. A check demands a response and limits the opponent's options.
2. **Captures**: Material changes are the next most important. Look at captures, especially of undefended pieces and pieces defended by less valuable pieces.
3. **Threats**: Moves that create future threats (mate threats, piece attacks, pawn advances to promotion).

This priority order is not arbitrary—it follows the **principle of forcing**: a move that forces the opponent's response is always more valuable to consider than a move that allows the opponent freedom. Checks > Captures > Threats is the order of forcing intensity.

The CCT method is sometimes called "forced move analysis" because it prioritizes moves that *reduce* the opponent's options. A check typically has only 2-5 legal responses; a capture might alter the material balance decisively; a threat creates a future obligation for the opponent. By examining forcing moves first, the player maximizes the chance of finding a tactical solution while minimizing the computational burden.

### Formalizing CCT Priority

We can formalize CCT using the concept of **response constraint**—how many legal responses the opponent has after our move:

$$\text{Priority}(m) = \frac{1}{|\text{LegalResponses}(m)| + 1}$$

A check that allows only one response has priority $\frac{1}{2}$, while a quiet move that allows 30 responses has priority $\frac{1}{31}$. This mathematical formulation captures the intuition behind CCT: forcing moves are more important because they constrain the search tree.

### How Our Engine Implements CCT

```python
def order_moves_cct(board: chess.Board) -> list[chess.Move]:
    """
    Order moves using the Checks-Captures-Threats priority.
    This directly mirrors the human CCT thinking process.
    """
    checks = []
    captures = []
    threats = []
    quiet = []
    
    for move in board.legal_moves:
        board.push(move)
        
        if board.is_check():
            checks.append(move)
        elif board.is_capture(move):
            captures.append(move)
        else:
            if creates_significant_threat(board, move):
                threats.append(move)
            else:
                quiet.append(move)
        
        board.pop()
    
    # Sort captures by MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
    captures.sort(key=lambda m: mvv_lva_score(board, m), reverse=True)
    
    # Sort quiet moves by PST improvement
    quiet.sort(key=lambda m: pst_improvement(board, m), reverse=True)
    
    return checks + captures + threats + quiet

def creates_significant_threat(board: chess.Board, move: chess.Move) -> bool:
    """
    Heuristic: does this move create a significant threat?
    A threat is created when the moved piece attacks a valuable enemy piece.
    """
    piece = board.piece_at(move.to_square)
    if piece is None:
        return False
    
    attacks = board.attacks(move.to_square)
    for target_sq in attacks:
        target = board.piece_at(target_sq)
        if target and target.color != piece.color:
            if PIECE_VALUES.get(target.piece_type, 0) >= PIECE_VALUES.get(chess.ROOK, 0):
                return True
    return False
```

## Intuition vs. Calculation: The Dual-Process Model

### Two Modes of Thinking

Psychologists distinguish between two modes of cognitive processing, famously described by Daniel Kahneman in *Thinking, Fast and Slow*:

| Mode | Characteristics | Speed | Chess Example |
|------|----------------|-------|---------------|
| **System 1** (Intuition) | Fast, automatic, pattern-based, effortless | Milliseconds | "I know this position — the knight on f5 is dominant" |
| **System 2** (Calculation) | Slow, deliberate, analytical, effortful | Seconds to minutes | "If I play Nf5, then after gxh6, Bxh6, Kg7, Re1..." |

Strong players use both modes in a tightly integrated loop. They use **intuition** to generate candidate moves and assess positions, and **calculation** to verify specific tactical lines. The interaction between these modes is what makes human chess thinking powerful:

1. **Intuition generates candidates**: "This position feels like Nf5 should be considered"
2. **Calculation verifies**: "After Nf5, gxh6, Bxh6, the position is +2.0"
3. **Intuition reassesses**: "That feels right — the knight is dominant on f5 and the attack flows naturally"
4. **Calculation refines**: "But wait, what about Kh8 instead of gxh6? Let me check..."

This loop continues until the player reaches a decision they are confident in. The key insight is that **intuition narrows the search space** and **calculation verifies within that narrowed space**. Without intuition, calculation drowns in possibilities. Without calculation, intuition makes systematic errors.

### The Neuroscience of Chess Intuition

Brain imaging studies of chess players have revealed that pattern recognition in chess activates the **temporal lobe** (associated with object recognition and categorization), while calculation activates the **prefrontal cortex** (associated with working memory and logical reasoning). Expert players show stronger temporal lobe activation for pattern recognition, suggesting that years of study literally rewire the brain to recognize chess positions as "objects" with associated properties.

This neurological finding has direct implications for our engine: the rule-based evaluation system corresponds to the pattern-recognition system (temporal lobe), while the search algorithm corresponds to the calculation system (prefrontal cortex). The rules are the "patterns" that the engine recognizes, and the search is the "calculation" that verifies them.

### Why Our Engine Needs Both

Our engine needs both intuition (the static evaluation + rules) and calculation (the search algorithm). But it also needs to explain both types of reasoning:

- **Intuition explanations**: "The knight on f5 is on a powerful outpost, controlling key squares around the enemy king" — this is a pattern-based explanation grounded in [[07-Chess-Psychology-and-Human-Thinking/03 - Square Weakness and Outposts|square weakness and outpost]] concepts.
- **Calculation explanations**: "After Nf5 gxh6 Bxh6, the bishop pair dominates the open position" — this is a line-based explanation grounded in the [[02-Search-Algorithms/01 - Minimax Algorithm|search algorithm]].

The combination of both creates a rich, human-like explanation that addresses both *why the move was considered* (intuition) and *why it works* (calculation).

## Pattern Recognition as the Primary Human Strength

### What Is Pattern Recognition?

The primary cognitive strength of strong chess players is **pattern recognition**—the ability to recognize familiar configurations of pieces and recall the correct plans, tactics, and evaluations associated with them. A grandmaster doesn't calculate from scratch in every position; they recognize the position as belonging to a known class and apply the appropriate template.

This is the core insight from Adrian de Groot's seminal studies of chess players in the 1940s-60s. De Groot found that grandmasters and weaker players calculated roughly the same number of moves, but grandmasters consistently chose better moves. The difference was not in calculation depth or breadth, but in **perception**—grandmasters saw the right things first.

Examples of chess patterns and their recognition templates:

| Pattern | Recognition Cue | Associated Response |
|---------|----------------|-------------------|
| Back rank weakness | Enemy king on 1st/8th rank with no escape squares | Look for back rank mate |
| Opposite-colored bishops | Both sides have bishops on different color complexes | Attacking side has advantage; draw in endgame |
| Isolated queen pawn | White pawn on d4 with no c/e pawns | Space advantage but structural weakness |
| Bad bishop | Bishop blocked by own pawns on same color complex | Improve the bishop or exchange it |
| Knight outpost | Knight on rank 5, protected by pawn, no enemy pawn can attack | Fortify and use the knight dominantly |
| King-side attack | Open h- or g-file, queen + rook battery | Launch the attack with sacrifices |
| Pawn chain | Connected pawns on diagonal | Attack the base of the chain |

### Why Human Explanations Must Reference Patterns

When a grandmaster explains a move, they don't say "I calculated 12 ply and the evaluation was +1.5." They say "The knight on d5 is a monster—it controls the entire board and Black can't get rid of it." This is a pattern-based explanation, and it's what our engine must produce.

Our engine's [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|rule-based evaluation]] directly encodes these patterns:

- [[05-Evaluation-Functions-and-Heuristics/04 - Pawn Structure Evaluation|Pawn structure evaluation]] → "doubled pawns," "isolated pawn," "passed pawn"
- [[05-Evaluation-Functions-and-Heuristics/06 - Mobility and Piece Activity|Piece activity evaluation]] → "knight on outpost," "bad bishop," "rook on open file"
- [[07-Chess-Psychology-and-Human-Thinking/03 - Square Weakness and Outposts|Square weakness]] → "weak square," "outpost"
- [[07-Chess-Psychology-and-Human-Thinking/05 - The Six Chess Crimes|Chess crimes]] → "mindless exchange," "knight on the rim"

Each pattern has a name, a description, and an associated evaluation score. When a pattern is detected, the engine can explain the move in terms of the pattern, not in terms of the search tree.

## The IM/GM Thinking Process: Evaluate → Plan → Calculate → Blunder-Check

### The Four-Step Model

Studies of how International Masters and Grandmasters think—including de Groot's eye-tracking studies and Tisdall's further analysis—reveal a consistent four-step process:

1. **Evaluate the position**: Assess the static features (material, pawn structure, king safety, piece activity) to understand "who is better and why"
2. **Form a plan**: Based on the evaluation, determine the strategic direction (attack the king, improve the worst piece, create a passed pawn, exchange into a better endgame, etc.)
3. **Calculate specific variations**: For the chosen plan, calculate the key tactical lines to verify the plan works
4. **Blunder-check**: Before playing, double-check that the move doesn't hang a piece, allow a tactic, or miss a simple refutation

This four-step process is not always linear—players may cycle through steps, revising their evaluation after calculation reveals new information. But the overall structure is remarkably consistent across strong players.

### Step 1: Evaluate the Position

The evaluation step is where pattern recognition and intuition dominate. The player looks at the board and asks:
- Who has the material advantage?
- What are the pawn structure features? (isolated pawns, passed pawns, pawn chains)
- How active are the pieces? (bad bishops, knights on outposts, rooks on open files)
- How safe are the kings? (pawn shield, open files near king, attacking pieces nearby)

The result of this step is a *qualitative assessment*: "White is slightly better due to the strong knight on d5 and Black's weak c6-pawn." This assessment then guides the plan.

### Step 2: Form a Plan

Based on the evaluation, the player forms a plan. Common plans include:
- **Attack the king**: When the opponent's king is exposed
- **Improve the worst piece**: When a piece is passive (see [[07-Chess-Psychology-and-Human-Thinking/02 - Feeling for the Pieces|Feeling for the Pieces]])
- **Create a passed pawn**: When there's potential for pawn promotion
- **Exchange into a better endgame**: When we have a structural advantage that matters more with fewer pieces
- **Prophylaxis**: Prevent the opponent's plan (see [[07-Chess-Psychology-and-Human-Thinking/04 - Prophylaxis|Prophylaxis]])

### Step 3: Calculate Specific Variations

The player calculates the key tactical lines to verify the plan. This is where System 2 (calculation) takes over. The player calculates:

```
If I play Nf5:
  If gxh6: Bxh6, then Kg7: Re1! and the attack wins
  If Kh8:  Ng7! Rg8: Nf5 again with a winning position
  If Nd7:  Nxd7 Bxd7: and the knight dominates
```

### Step 4: Blunder-Check

The final step is a safety check: does the move hang anything? This is where many players fail—they find a beautiful plan and forget to check if it loses material. The blunder-check is the chess equivalent of "measure twice, cut once."

```python
def blunder_check(board: chess.Board, move: chess.Move) -> tuple[bool, str]:
    """
    Check if a move is a blunder.
    Returns (is_blunder, reason).
    """
    board.push(move)
    
    # Check if the moved piece is hanging
    if board.is_attacked_by(not board.turn, move.to_square):
        if not board.is_attacked_by(board.turn, move.to_square):
            piece = board.piece_at(move.to_square)
            return (True, f"The {piece.symbol()} on {chess.square_name(move.to_square)} is undefended")
    
    # Check if the move allows a simple tactic
    for opp_move in board.legal_moves:
        if board.is_capture(opp_move):
            # Check if the capture wins material
            if mvv_lva_score(board, opp_move) > 0:
                return (True, f"Allows {opp_move.uci()} which wins material")
    
    board.pop()
    return (False, "")
```

### How Our Engine Models This Process

| Human Step | Engine Component | Explanation Output |
|------------|-----------------|-------------------|
| Evaluate the position | [[05-Evaluation-Functions-and-Heuristics/01 - Static Evaluation Overview|Static evaluation]] | "White has a slight advantage due to..." |
| Form a plan | [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule engine]] | "The plan is to improve the knight..." |
| Calculate variations | [[06-Adaptive-Depth-Control/01 - The Depther Philosophy|Search with adaptive depth]] | "After Nf5 gxh6 Bxh6, the attack is decisive" |
| Blunder-check | [[05-Evaluation-Functions-and-Heuristics/07 - Threats and Tactical Patterns|Threat detection]] + quiescence | "No hanging pieces, no opponent tactics" |

## Why Search Trees Are Not Explanations

A common misconception in chess engine design is that showing the search tree *is* the explanation. It isn't. A search tree tells you *what* the engine calculated, but not *why*. The user doesn't want to see:

```
Nf5: depth 8, score +1.5
  gxh6: depth 7, score +1.2
    Bxh6: depth 6, score +2.0
      Kg7: depth 5, score +1.8
```

The user wants to see:

> "The knight sacrifice on f5 is strong because it opens the g-file for the rook and brings the bishop to h6, creating an unstoppable attack on the king. After gxh6 Bxh6, the bishop pair and open g-file give White a winning attack."

The difference is that the first version shows the **computation**, while the second shows the **reasoning**. Our engine is designed to produce the second version by connecting the search results to the rule-based evaluation, which provides the chess concepts (outpost knight, open file, bishop pair, attack on king) that make the explanation meaningful.

## Bridging Human and Machine Thinking

The ultimate goal of our chess psychology module is to **bridge** human and machine thinking. The engine should:

1. **Think like a machine** (search deeply, evaluate precisely) for quality
2. **Explain like a human** (reference patterns, use chess concepts) for understandability
3. **Connect the two** (show how the pattern-based reasoning led to the machine-level result) for trustworthiness

This bridge is built from the rule-based evaluation (which maps chess concepts to scores), the depth policy (which explains which lines were searched and why), and the explanation pipeline (which combines both into a coherent narrative). The result is an engine that is both strong and understandable—a rare combination in the world of chess AI, and one that directly addresses the [[01-Foundations/04 - The Explainability Problem|explainability problem]] at the core of this project.

---

*Next: [[07-Chess-Psychology-and-Human-Thinking/02 - Feeling for the Pieces|02 - Feeling for the Pieces]] →*
*See also: [[05-Evaluation-Functions-and-Heuristics/01 - Static Evaluation Overview|Static Evaluation Overview]] | [[06-Adaptive-Depth-Control/01 - The Depther Philosophy|The Depther Philosophy]] | [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]]*
