---
tags:
  - search
  - negamax
  - zero-sum
  - simplification
chapter: "02"
---

# Negamax Formulation

## Overview

The **Negamax** algorithm is a reformulation of [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax]] that exploits the **zero-sum property** of chess to eliminate the alternating max/min distinction. Instead of separate maximizing and minimizing branches, Negamax uses a single consistent rule: **always maximize, but negate the score from the child's perspective**. This halves the code, reduces bugs, and provides an elegant foundation for [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta pruning]].

---

## The Mathematical Insight

### Zero-Sum Implies Score Negation

In a zero-sum game, if White's evaluation of a position is $+3$, then Black's evaluation of the same position is $-3$. This is because:

$$V_{\text{White}}(s) = -V_{\text{Black}}(s)$$

Therefore, when we compute the value of a child node from the **opponent's perspective** and then negate it, we get the value from **our perspective**.

### The Key Identity

The Minimax algorithm alternates between:

$$\text{Max node: } V = \max(V_1, V_2, \ldots, V_n)$$
$$\text{Min node: } V = \min(V_1, V_2, \ldots, V_n)$$

Using the zero-sum property, we can transform the min node:

$$\min(a, b) = -\max(-a, -b)$$

**Proof:**
- If $a \leq b$, then $\min(a,b) = a$ and $-\max(-a, -b) = -(-a) = a$ 
- If $a > b$, then $\min(a,b) = b$ and $-\max(-a, -b) = -(-b) = b$ 

This means we can replace every min node with a max node by negating the scores:

$$\min(V_1, V_2, \ldots, V_n) = -\max(-V_1, -V_2, \ldots, -V_n)$$

### The Negamax Rule

In Negamax, the score is **always from the perspective of the side to move**. The recursive rule is:

$$V(s) = \max_{a \in \text{actions}(s)} (-V(\text{result}(s, a)))$$

In words: the value of a position is the maximum of the **negated** values of all child positions. The negation handles the perspective switch (the child is evaluated from the opponent's point of view).

---

## Negamax Algorithm

### Pseudocode

```python
def negamax(position, depth):
    if depth == 0 or position.is_terminal():
        return evaluate_for_side(position)  # Always from side-to-move perspective

    max_score = -INFINITY

    for move in position.generate_legal_moves():
        position.make_move(move)
        # Child is from opponent's perspective, so negate
        score = -negamax(position, depth - 1)
        position.unmake_move(move)

        max_score = max(max_score, score)

    return max_score
```

Notice: there is **no `if is_maximizing` branch**. The algorithm is the same at every level. The perspective switch is handled entirely by the negation.

### Finding the Best Move

```python
def find_best_move_negamax(position, depth):
    best_move = None
    best_score = -INFINITY

    for move in position.generate_legal_moves():
        position.make_move(move)
        score = -negamax(position, depth - 1)
        position.unmake_move(move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score
```

### The Evaluation Function

The critical requirement is that `evaluate_for_side()` returns the evaluation from the **side to move's** perspective:

```python
def evaluate_for_side(position):
    raw_score = evaluate(position)  # e.g., positive = White is better
    if position.side_to_move == BLACK:
        return -raw_score  # Negate for Black's perspective
    return raw_score
```

---

## Complete Code Trace: Minimax vs. Negamax

Consider the same simplified game tree:

```
Minimax perspective (scores from White's view):
          MAX=3 (root, White)
         /          \
      MIN=3        MIN=2
     /   \         /   \
    3      5      2      9
```

### Minimax Trace

| Node | Type | Children | Computation | Value |
|------|------|----------|-------------|-------|
| Leaf A | - | - | eval = 3 | 3 |
| Leaf B | - | - | eval = 5 | 5 |
| Leaf C | - | - | eval = 2 | 2 |
| Leaf D | - | - | eval = 9 | 9 |
| Node L | MIN | A(3), B(5) | min(3, 5) | 3 |
| Node R | MIN | C(2), D(9) | min(2, 9) | 2 |
| Root | MAX | L(3), R(2) | max(3, 2) | 3 |

### Negamax Trace

In Negamax, scores are **always from the side to move's perspective**. We need to track perspective at each level:

| Node | Side | Child eval (opp. view) | Negated | max(-child) | Value |
|------|------|----------------------|---------|-------------|-------|
| Leaf A | Black | -3 | — | — | -3 |
| Leaf B | Black | -5 | — | — | -5 |
| Leaf C | Black | -2 | — | — | -2 |
| Leaf D | Black | -9 | — | — | -9 |
| Node L | White | A=-3, B=-5 | 3, 5 | max(3,5) | 5→3* |

Wait — let me redo this more carefully. The key is that the evaluation at leaf nodes must be from the side to move at that leaf.

**Corrected trace:**

The tree alternates: White → Black → (evaluate).

- **Root** (White to move): Try moves → get score = -negamax(child, depth-1)
- **Children** (Black to move): Try moves → get score = -negamax(grandchild, depth-1)
- **Grandchildren** (White to move): At depth 0, evaluate from White's perspective

Let's use concrete values. Assume all evaluations are from White's perspective:
- Position after White move 1, Black move 1a: eval = +3 (White better)
- Position after White move 1, Black move 1b: eval = +5 (White better)
- Position after White move 2, Black move 2a: eval = +2 (White better)
- Position after White move 2, Black move 2b: eval = +9 (White better)

**Negamax trace (all scores from side-to-move perspective):**

| Level | Node | Side | Computation | Value |
|-------|------|------|-------------|-------|
| 2 | Leaf 1a | White | eval = +3 | +3 |
| 2 | Leaf 1b | White | eval = +5 | +5 |
| 2 | Leaf 2a | White | eval = +2 | +2 |
| 2 | Leaf 2b | White | eval = +9 | +9 |
| 1 | Node 1 | Black | max(-3, -5) = max(-3, -5) = -3 | -3 |
| 1 | Node 2 | Black | max(-2, -9) = max(-2, -9) = -2 | -2 |
| 0 | Root | White | max(-(-3), -(-2)) = max(3, 2) = 3 | +3 |

**Result: +3** — identical to Minimax! 

The beauty is that the computation at every level follows the **same pattern**: maximize the negated child scores. No branching on who's turn it is.

---

## Why Negamax Is Preferred

### 1. 50% Less Code

Minimax requires two separate branches (max and min), effectively duplicating the logic:

```python
# Minimax: 2 branches
if is_maximizing:
    for move in moves:
        score = minimax(child, depth-1, False)
        best = max(best, score)
else:
    for move in moves:
        score = minimax(child, depth-1, True)
        best = min(best, score)
```

Negamax has one unified branch:

```python
# Negamax: 1 branch
for move in moves:
    score = -negamax(child, depth-1)
    best = max(best, score)
```

### 2. Fewer Bugs

Every `if` branch is an opportunity for a bug. Negamax eliminates the max/min branch entirely. The most common Minimax bug — forgetting to switch the maximizing flag on a recursive call — is impossible in Negamax.

### 3. Elegant Integration with Alpha-Beta

[[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta pruning]] integrates naturally with Negamax. The alpha-beta window is maintained symmetrically: passing `-beta, -alpha` to the child. This is far cleaner than the Minimax version, which requires different logic for max and min nodes.

### 4. Uniform Score Convention

In Negamax, **positive always means good for the side to move**. This eliminates confusion about "whose perspective is this score from?" that plagues Minimax implementations.

---

## Negamax with Alpha-Beta (Preview)

The full integration with alpha-beta pruning:

```python
def negamax_ab(position, depth, alpha, beta):
    if depth == 0 or position.is_terminal():
        return evaluate_for_side(position)

    for move in position.generate_legal_moves():
        position.make_move(move)
        # Key: negate AND swap alpha/beta
        score = -negamax_ab(position, depth - 1, -beta, -alpha)
        position.unmake_move(move)

        if score >= beta:
            return beta  # Beta cutoff
        if score > alpha:
            alpha = score

    return alpha
```

Notice how the alpha-beta window is **negated and swapped** in the recursive call: `-beta, -alpha`. This is the elegant consequence of the zero-sum property — the opponent's beta is our negated alpha, and vice versa.

---

## Common Pitfalls

### 1. Forgetting to Negate

The most common mistake:

```python
# WRONG: forgot to negate
score = negamax(position, depth - 1)  # Missing the minus sign!

# CORRECT:
score = -negamax(position, depth - 1)
```

### 2. Evaluation Function Not From Side-to-Move

If the evaluation function always returns White's perspective without negation for Black:

```python
# WRONG:
def evaluate_for_side(position):
    return evaluate(position)  # Always White's view!

# CORRECT:
def evaluate_for_side(position):
    score = evaluate(position)
    if position.side_to_move == BLACK:
        return -score
    return score
```

### 3. Mate Score Adjustment

When returning mate scores, the distance to mate must be adjusted:

```python
MATE_SCORE = 100000

def evaluate_for_side(position):
    if position.is_checkmate():
        # The side to move is checkmated — return a very negative score
        # adjusted by depth so shorter mates are preferred
        return -MATE_SCORE + position.ply_from_root
    if position.is_stalemate():
        return 0
    # ... normal evaluation
```

The `+ position.ply_from_root` ensures that a mate in 1 (closer) is scored higher than a mate in 3 (further away), even though both are "checkmate."

---

## Full Python Implementation

```python
import chess

MATE_SCORE = 100000

def evaluate_for_side(board):
    """Evaluate position from the side-to-move's perspective."""
    if board.is_checkmate():
        return -MATE_SCORE  # Side to move is mated
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Material evaluation (centipawns)
    piece_values = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0
    }

    score = 0
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    # Negate if Black to move
    if board.turn == chess.BLACK:
        score = -score

    return score

def negamax(board, depth):
    """Negamax search without alpha-beta pruning."""
    if depth == 0:
        return evaluate_for_side(board)

    if board.is_game_over():
        return evaluate_for_side(board)

    max_score = -MATE_SCORE - 1

    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1)
        board.pop()

        if score > max_score:
            max_score = score

    return max_score

def find_best_move(board, depth):
    """Find the best move using Negamax."""
    best_move = None
    best_score = -MATE_SCORE - 1

    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1)
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score
```

---

## Connection to Explainability

Negamax's uniform score convention — **positive = good for the side to move** — is a natural fit for the explanation system. Every score has an unambiguous meaning:

- "+2.50" means the side to move has a decisive advantage
- "-1.00" means the side to move is worse
- "+0.15" means the side to move has a slight edge

When the explanation system says "This move improves your position by 0.35 pawns," it's using the Negamax convention: the improvement is from *your* perspective. There's no need to translate between White and Black views — the perspective is always the current player.

This convention also simplifies **comparative explanations**: "Move A scores +0.50, while Move B scores +0.20. Move A is better because it gains 0.30 pawns more, primarily due to [principle X]."

---

## Key Takeaways

- **Negamax** exploits the zero-sum property to unify the max/min branches into a single **always-maximize** algorithm.
- The key identity: $\min(a, b) = -\max(-a, -b)$ means every min node becomes a max node with negated scores.
- Scores are **always from the side-to-move's perspective**, eliminating ambiguity.
- Negamax requires **50% less code**, has **fewer bugs**, and integrates **elegantly with alpha-beta pruning**.
- The alpha-beta window is passed as `-beta, -alpha` to children, maintaining the zero-sum symmetry.
- The uniform score convention is a natural foundation for the explanation system.

## Cross-References

- [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax Algorithm]] — the algorithm that Negamax simplifies
- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the essential optimization built on Negamax
- [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — further optimization using the Negamax framework
- [[01-Foundations/01 - Chess as a Zero-Sum Game|Chess as a Zero-Sum Game]] — the zero-sum property that makes Negamax possible
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — how the uniform score convention aids explanation
