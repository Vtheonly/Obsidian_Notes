# Root-Level Selectivity

> "You don't need to search bad moves deeply to know they're bad." — Chess Programming Wisdom

## The Problem with Searching Everything

At the root of the search tree, the engine typically faces 30-40 legal moves. Searching all of them to full depth is wasteful because:

1. **Most moves are clearly inferior** — in most positions, only 3-5 moves are competitive.
2. **The cost of searching is exponential** — each additional ply multiplies the node count by the branching factor.
3. **Time is limited** — in tournament conditions, the engine must return a move within a time budget.

Consider the math: with branching factor 35 and depth 10, the full tree has $35^{10} \approx 2.8 \times 10^{15}$ nodes. Even with [[Alpha-Beta Search]] reducing this to roughly $35^5 \approx 52$ million nodes, searching all 35 root moves to depth 10 takes far too long. If we can reduce the number of root moves that get full depth from 35 to 5, we save 85% of the computation.

[[Root-Level Selectivity]] is the strategy of **not searching all root moves equally**. The best moves get full depth; the rest get reduced depth or are pruned entirely.

## Heuristic Sort

The first step is to **sort root moves by heuristic quality**. Moves that are likely to be best should be searched first (for [[Alpha-Beta Search|alpha-beta pruning]] efficiency) and to full depth. Moves that are likely to be poor can be searched at reduced depth.

Our heuristic sort considers multiple factors:

```python
def root_move_heuristic(board: Board, move: Move) -> int:
    """
    Compute a heuristic score for a root move.
    Higher score = more promising = should be searched deeper.
    """
    score = 0

    # 1. Captures are usually good
    if board.is_capture(move):
        # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
        victim = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        if victim:
            score += 10 * PIECE_VALUES[victim.type] - PIECE_VALUES[attacker.type]

    # 2. Checks are forcing and often strong
    if board.gives_check(move):
        score += 5000

    # 3. Promotions are almost always worth checking
    if move.promotion:
        score += 4000

    # 4. Killer moves (moves that were best in sibling nodes)
    if move in killer_moves:
        score += 3000

    # 5. History heuristic (moves that have been good in similar positions)
    score += history_table[move.from_square][move.to_square]

    # 6. Piece-square table improvement
    piece = board.piece_at(move.from_square)
    if piece:
        from_pst = pst_value(piece.type, move.from_square, piece.color, phase)
        to_pst = pst_value(piece.type, move.to_square, piece.color, phase)
        score += (to_pst - from_pst) * 10

    # 7. Castling is usually good
    if board.is_castling(move):
        score += 2000

    # 8. Threats created by this move
    if creates_threat(board, move):
        score += 1500

    return score

def sort_root_moves(board: Board, moves: List[Move]) -> List[Move]:
    """
    Sort root moves by heuristic quality (best first).
    """
    scored_moves = [(root_move_heuristic(board, m), m) for m in moves]
    scored_moves.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored_moves]
```

## Top-K Selection

After sorting, we select the **top K moves** for full-depth search. The value of K depends on the time budget and position complexity:

```python
def compute_root_k(num_moves: int, time_budget_ms: int, position_complexity: float) -> int:
    """
    Determine how many root moves to search at full depth.
    - time_budget_ms: remaining time
    - position_complexity: 0.0 (simple) to 1.0 (complex)

    More time and more complex positions → search more root moves.
    """
    # Base: search top 4 moves at full depth
    base_k = 4

    # Time adjustment: with more time, we can afford to search more
    if time_budget_ms > 30000:
        base_k += 2
    elif time_budget_ms > 10000:
        base_k += 1

    # Complexity adjustment: complex positions need more exploration
    base_k += int(position_complexity * 3)

    # Never search fewer than 3 or more than all moves
    return max(3, min(num_moves, base_k))
```

The remaining moves (moves ranked K+1 through N) are searched at **reduced depth**, typically depth - 2 or depth - 3. If any of them produce a surprisingly good score (better than the alpha bound), they are **re-searched** at full depth.

## Asymmetric Budgeting

Root-level selectivity is fundamentally **asymmetric**: the top move might get searched to depth 14 while the 10th-best move only gets depth 8. This is not unfair—it is efficient. The top move is most likely to be the best, so it deserves the most computational investment.

```
Move Ranking    Full Depth    Actual Depth
──────────────  ────────────  ────────────
1st (best)      D             D + extensions
2nd             D             D
3rd             D             D
4th             D             D - 1 (slight reduction)
5th             D             D - 2
6th–10th        D             D - 3
11th+           D             D - 4 or pruned
```

### Python Implementation

```python
@dataclass
class RootSearchPlan:
    """Plan for searching root moves with asymmetric depth allocation."""
    move: Move
    depth: int
    is_full_depth: bool
    reason: str

def plan_root_search(board: Board, moves: List[Move], base_depth: int,
                     time_budget_ms: int) -> List[RootSearchPlan]:
    """
    Create a search plan for all root moves.
    Top K moves get full depth; others get reduced depth.
    """
    sorted_moves = sort_root_moves(board, moves)
    k = compute_root_k(len(sorted_moves), time_budget_ms,
                       estimate_complexity(board))

    plans = []
    for i, move in enumerate(sorted_moves):
        if i < k:
            # Top K: full depth search
            plans.append(RootSearchPlan(
                move=move,
                depth=base_depth,
                is_full_depth=True,
                reason=f"Top-{i+1} move by heuristic, searched at full depth {base_depth}"
            ))
        elif i < k + 5:
            # Near-cutoff: slight reduction
            reduced = max(1, base_depth - 2)
            plans.append(RootSearchPlan(
                move=move,
                depth=reduced,
                is_full_depth=False,
                reason=f"Move ranked {i+1}, searched at reduced depth {reduced} (heuristic suggests it's unlikely to be best)"
            ))
        else:
            # Deep cuts: significant reduction
            reduced = max(1, base_depth - 4)
            plans.append(RootSearchPlan(
                move=move,
                depth=reduced,
                is_full_depth=False,
                reason=f"Move ranked {i+1}, searched at depth {reduced} (low heuristic score)"
            ))

    return plans
```

## Re-Search on Surprise

If a reduced-depth search returns a score **above the current alpha bound**, the move might actually be better than the top-K moves predicted. In this case, we **re-search at full depth**:

```python
def search_root(board: Board, base_depth: int, time_budget_ms: int) -> SearchResult:
    """
    Root search with asymmetric depth allocation and re-search.
    """
    moves = board.legal_moves()
    plans = plan_root_search(board, moves, base_depth, time_budget_ms)

    best_result = None
    alpha = -INFINITY

    for plan in plans:
        board.push(plan.move)

        if plan.is_full_depth:
            # Full depth search
            score = -negamax(board, plan.depth - 1, -BETA, -alpha)
        else:
            # Reduced depth search
            score = -negamax(board, plan.depth - 1, -BETA, -alpha)

            # Re-search if this move is surprisingly good
            if score > alpha and plan.depth < base_depth:
                score = -negamax(board, base_depth - 1, -BETA, -alpha)
                plan.reason += " [RE-SEARCHED at full depth due to surprising score]"

        board.pop()

        if score > alpha:
            alpha = score
            best_result = SearchResult(
                move=plan.move,
                score=score,
                depth=plan.depth,
                reason=plan.reason
            )

    return best_result
```

## Estimating Position Complexity

How do we know whether a position is "complex" and deserves more root-level exploration? We estimate complexity based on:

1. **Number of legal moves**: More moves = more to consider.
2. **Tactical density**: Number of captures, checks, and threats available.
3. **King safety imbalance**: If one king is exposed, the position is tactical.
4. **Evaluation volatility**: How much the evaluation changes between iterations.

```python
def estimate_complexity(board: Board) -> float:
    """
    Estimate position complexity on a scale of 0.0 (simple) to 1.0 (very complex).
    """
    complexity = 0.0

    # Number of legal moves
    num_moves = len(list(board.legal_moves()))
    complexity += min(1.0, num_moves / 40) * 0.2

    # Tactical density
    captures = sum(1 for m in board.legal_moves() if board.is_capture(m))
    checks = sum(1 for m in board.legal_moves() if board.gives_check(m))
    complexity += min(1.0, (captures + checks) / 10) * 0.3

    # King safety imbalance
    w_ks = evaluate_king_safety_for_side(board, WHITE)
    b_ks = evaluate_king_safety_for_side(board, BLACK)
    king_imbalance = abs(w_ks - b_ks)
    complexity += min(1.0, king_imbalance / 200) * 0.3

    # Material imbalance (tactical positions often have material imbalance)
    mat = material_balance(board.white_pieces, board.black_pieces)
    complexity += min(1.0, abs(mat) / 300) * 0.2

    return min(1.0, complexity)
```

## Explainability at the Root

Root-level selectivity is one of the most visible decisions the engine makes, and therefore one of the most important to explain. When the engine recommends a move, it can now say:

> "I searched 5 moves at full depth (depth 10) and 12 moves at reduced depth (depth 7-8). The top move by heuristic was Nxe5, which I searched first. The 8th-ranked move, Qd2, surprisingly scored better at reduced depth, so I re-searched it at full depth and confirmed it was inferior."

This transparency builds trust and helps the user understand the engine's decision-making process.

## Summary

Root-level selectivity ensures that the engine's computational budget is spent where it matters most. By sorting moves heuristically, searching the top K at full depth, and re-searching surprising results, we achieve both **efficiency** and **accuracy**. And by attaching explanations to every depth allocation decision, we make the search process **transparent and teachable**.

---

**See also:** [[The Depther Philosophy]], [[Depth Extension Rules]], [[Depth Reduction Rules]], [[Alpha-Beta Search]], [[Move Ordering]], [[History Heuristic]], [[Killer Moves]], [[MVV-LVA]]
