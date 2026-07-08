---
tags:
  - search
  - minimax
  - game-theory
  - foundation-algorithm
chapter: "02"
---

# Minimax Algorithm

## Overview

The **Minimax algorithm** is the theoretical foundation of all two-player zero-sum game-playing programs. It defines the optimal strategy: assume your opponent plays perfectly, and choose the move that maximizes your worst-case outcome. While pure Minimax is far too slow for practical chess engines, it is the conceptual bedrock upon which [[02-Search-Algorithms/02 - Negamax Formulation|Negamax]], [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta]], and every subsequent optimization is built.

---

## The Minimax Principle

### Intuition

Imagine you are White, and it is your turn. You want to choose the move that leads to the best possible outcome for you. But you know that after your move, Black will choose the move that leads to the **worst possible outcome for you** (best for Black). And after Black's move, you again maximize, and so on.

This alternating maximization and minimization is the core of Minimax. The algorithm assumes **perfect play** from both sides — it is a worst-case analysis.

### Mathematical Formulation

Let $V(s)$ be the Minimax value of position $s$. Then:

$$V(s) = \begin{cases} \text{eval}(s) & \text{if } s \text{ is a terminal/leaf node} \\ \displaystyle\max_{a \in \text{actions}(s)} V(\text{result}(s, a)) & \text{if it is the maximizer's turn (White)} \\ \displaystyle\min_{a \in \text{actions}(s)} V(\text{result}(s, a)) & \text{if it is the minimizer's turn (Black)} \end{cases}$$

Where:
- $\text{actions}(s)$ is the set of legal moves from position $s$
- $\text{result}(s, a)$ is the position resulting from taking action $a$ in position $s$
- $\text{eval}(s)$ is the static evaluation function that estimates the position's value

### Game Tree Interpretation

In the game tree:
- **Max nodes** (White's turn): the node's value is the maximum of its children's values
- **Min nodes** (Black's turn): the node's value is the minimum of its children's values
- **Leaf nodes**: the value is the static evaluation

The optimal move at the root is the one leading to the child with the highest value (since the root is a max node for White).

---

## Complete Algorithm

### Pseudocode

```python
def minimax(position, depth, is_maximizing):
    if depth == 0 or position.is_terminal():
        return evaluate(position)

    if is_maximizing:
        max_eval = -INFINITY
        for move in position.generate_legal_moves():
            position.make_move(move)
            eval = minimax(position, depth - 1, False)
            position.unmake_move(move)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = +INFINITY
        for move in position.generate_legal_moves():
            position.make_move(move)
            eval = minimax(position, depth - 1, True)
            position.unmake_move(move)
            min_eval = min(min_eval, eval)
        return min_eval
```

### Finding the Best Move

At the root, we need not just the value but the **move** that achieves it:

```python
def find_best_move(position, depth):
    best_move = None
    best_value = -INFINITY

    for move in position.generate_legal_moves():
        position.make_move(move)
        value = minimax(position, depth - 1, False)  # Next is minimizer
        position.unmake_move(move)

        if value > best_value:
            best_value = value
            best_move = move

    return best_move, best_value
```

---

## Complete Code Trace Example

Consider a simplified game tree with depth 2 and branching factor 2:

```
          MAX (root, White)
         /          \
        /            \
      MIN            MIN
     /   \          /   \
   LEAF  LEAF    LEAF  LEAF
    3      5       2     9
```

**Step-by-step trace:**

1. **Root (MAX)**: Try left child first
2. **Left MIN node**: Try its children
   - Left leaf: eval = 3
   - Right leaf: eval = 5
   - MIN chooses: min(3, 5) = **3**
3. **Root (MAX)**: Left child value = 3. Try right child
4. **Right MIN node**: Try its children
   - Left leaf: eval = 2
   - Right leaf: eval = 9
   - MIN chooses: min(2, 9) = **2**
5. **Root (MAX)**: max(3, 2) = **3**
6. **Best move**: The left child (which led to value 3)

Notice that even though the right subtree contains a leaf with value 9, Black would never allow White to reach it — Black would choose the move leading to value 2 instead. **Minimax assumes the opponent plays optimally.**

---

## Complexity Analysis

### Time Complexity

The time complexity of Minimax is:

$$T(D) = O(B^D)$$

Where:
- $B$ = average branching factor (~35 in chess)
- $D$ = search depth in plies

### Space Complexity

The space complexity is $O(B \times D)$ for the recursive call stack and move lists at each level. Since $D$ is typically much smaller than $B^D$, the space requirement is manageable.

### Concrete Numbers for Chess

| Depth | Nodes ($35^D$) | Time at 10M nps |
|-------|----------------|-------------------|
| 4 | 1,500,625 | 0.15s |
| 5 | 52,521,875 | 5.3s |
| 6 | 1,838,265,625 | 3.1 min |
| 7 | 64,339,296,875 | 1.8 hrs |
| 8 | 2.25 × 10¹² | 2.6 days |

Even at depth 6, Minimax takes minutes. At depth 8, it takes days. Modern competitive engines search to depth 25-35+, which is only possible because of pruning (see [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]]) and other [[03-Search-Accelerators/01 - Iterative Deepening|acceleration techniques]]).

### Why Brute Force Fails

The exponential growth means that each additional ply multiplies the search time by ~35. Going from depth 6 to depth 7 is a 35× increase. Going from depth 10 to depth 15 is a $35^5 \approx 52$ million × increase. No hardware improvement can overcome this — we need **algorithmic** improvements.

---

## The Minimax Theorem

### John von Neumann (1928)

The **Minimax Theorem**, proved by John von Neumann in 1928, states:

> For any finite two-player zero-sum game, there exists a value $V$ and optimal mixed strategies for both players such that:
> - The maximizer can guarantee a payoff of at least $V$
> - The minimizer can guarantee a payoff of at most $V$

In chess (a game of perfect information), the optimal strategies are **pure** (deterministic), not mixed. The theorem guarantees that an optimal move exists for every position, but finding it requires searching the entire game tree.

### Implications for Chess

1. **Chess is solvable in principle**: There exists an optimal strategy that guarantees the best possible outcome.
2. **Chess is not solvable in practice**: The game tree is too large for exhaustive search.
3. **Minimax with limited depth is a heuristic approximation**: We search as deep as we can and use a static evaluation function to estimate the value of non-terminal positions.

---

## Properties of Minimax

### Optimality

Minimax is **optimal** against an optimal opponent. If the opponent plays perfectly, Minimax guarantees the best possible result. If the opponent makes a mistake, Minimax may not exploit it optimally (it assumes worst-case play), but it will never be worse than the Minimax value.

### Completeness

Minimax is **complete**: given enough time, it will find the optimal move. The limitation is purely computational.

### Depth-Limited Minimax

In practice, we cannot search to terminal positions. Instead, we use **depth-limited Minimax** with a **static evaluation function**:

$$V(s, d) = \begin{cases} \text{eval}(s) & \text{if } d = 0 \\ \max_a V(\text{result}(s, a), d-1) & \text{if maximizer's turn} \\ \min_a V(\text{result}(s, a), d-1) & \text{if minimizer's turn} \end{cases}$$

The quality of the move depends critically on both the **search depth** and the **evaluation function**. A deep search with a poor evaluation may be worse than a shallow search with a good evaluation, though in practice, depth is more important.

### The Horizon Effect

Depth-limited Minimax suffers from the **Horizon Effect**: a catastrophic sequence of moves may exist just beyond the search horizon. The engine cannot see it, so it evaluates the position as good when it is actually bad.

For example, if a queen is about to be trapped, but the trap requires 7 moves to execute and the engine only searches to depth 6, it will not see the trap and may evaluate the position as favorable. This is addressed by [[03-Search-Accelerators/05 - Quiescence Search|Quiescence Search]].

---

## Why Minimax Is the Foundation But Not the Solution

Minimax is:
-  **Theoretically optimal** — guarantees the best move against perfect play
-  **Simple to understand and implement**
-  **The basis for all subsequent algorithms** — every improvement is a modification of Minimax
-  **Exponentially slow** — $O(35^D)$ makes it impractical beyond depth 5-6
-  **Wastes computation** — explores branches that can never affect the result
-  **No pruning** — every node at every depth is fully evaluated

The transition from Minimax to practical chess engines involves:
1. [[02-Search-Algorithms/02 - Negamax Formulation|Negamax]] — simplification using the zero-sum property
2. [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — cutting branches that cannot affect the result
3. [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — further pruning based on the assumption of a best-first ordering
4. [[03-Search-Accelerators/01 - Iterative Deepening|Iterative Deepening]], [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]], [[03-Search-Accelerators/03 - Late Move Reductions (LMR)|LMR]], [[03-Search-Accelerators/04 - Null Move Pruning (NMP)|NMP]] — practical acceleration

---

## Connection to Explainability

Minimax provides the **theoretical guarantee** that a best move exists. The explainability challenge is to decompose *why* that move is best into human-understandable principles.

In Minimax, the best move is "the one that maximizes the minimum evaluation across all opponent responses." The explanation system must translate this into: "This move was chosen because even in the opponent's best response, our position remains favorable due to [principle A] and [principle B]."

Furthermore, Minimax's assumption of optimal opponent play means that the explanation should address: "What if the opponent doesn't play optimally? What opportunities does that create?" This is an extension beyond standard Minimax into **exploitability analysis** — identifying not just the best move against perfect play, but the best move against a specific opponent's tendencies.

---

## Key Takeaways

- **Minimax** is the optimal algorithm for two-player zero-sum games: it assumes perfect play and chooses the move that maximizes the worst-case outcome.
- The algorithm alternates between **maximization** (White) and **minimization** (Black) at each level of the game tree.
- Time complexity is $O(B^D) \approx O(35^D)$, which is **impractical** for chess beyond depth 5-6.
- **Depth-limited Minimax** uses a static evaluation function for non-terminal positions, introducing the **Horizon Effect**.
- Minimax is the **foundation** upon which all practical search algorithms are built — every optimization is a modification of Minimax.
- For explainability, Minimax provides the theoretical basis: "the best move maximizes the worst case," which the explanation system must translate into human principles.

## Cross-References

- [[01-Foundations/01 - Chess as a Zero-Sum Game|Chess as a Zero-Sum Game]] — the game-theoretic context for Minimax
- [[02-Search-Algorithms/02 - Negamax Formulation|Negamax Formulation]] — the simplified version using the zero-sum property
- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the essential pruning optimization
- [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — further optimization based on best-first ordering
- [[03-Search-Accelerators/05 - Quiescence Search|Quiescence Search]] — addressing the Horizon Effect
