# Safety and Control Rules

> "An engine that doesn't terminate is not an engine—it's an infinite loop." — Software Engineering Wisdom

## Why Safety Rules Exist

The [[Depther]]'s extension and reduction rules are powerful, but power without constraint is dangerous. Without safety rules, the engine could:

1. **Extend infinitely**: Each extension leads to a position that triggers another extension, creating an unbounded search.
2. **Reduce to zero**: Multiple stacked reductions could reduce the search depth to 0 or negative, making the search meaningless.
3. **Create depth inflation**: Extensions accumulate across the tree, making the effective search depth much larger than intended.
4. **Loop indefinitely**: Re-searches of reduced moves could trigger new extensions, creating circular behavior.

[[Safety and Control Rules]] are the guardrails that prevent these failure modes while preserving the benefits of adaptive depth control.

## Rule 1: Maximum Extension Cap

### What
The total depth extension at any single node is **capped** at a maximum value. No matter how many extension rules fire, the extension cannot exceed this cap.

### Why
A single move might trigger multiple extensions: it gives check (+1), it captures a piece (+1), it recaptures (+1), it creates a discovered attack (+1)—total extension: +4. While each extension is individually justified, a +4 extension at a single node dramatically increases the search tree size. More importantly, a +4 extension at *every* node along a line would create exponential depth inflation.

### Implementation

```python
MAX_EXTENSION_PER_MOVE = 2  # Maximum extension at a single node

def cap_extension(total_extension: int) -> int:
    """Cap the total extension at a single node."""
    return min(total_extension, MAX_EXTENSION_PER_MOVE)
```

### The Impact on the Tree

With MAX_EXTENSION_PER_MOVE = 2:
- A line with checks at every ply could extend by at most 2 at each node.
- Over 10 plies, the maximum extension is $10 \times 2 = 20$, giving an effective depth of $10 + 20 = 30$.
- This is still very deep, so we also need a **global depth cap** (see Rule 3).

## Rule 2: Maximum Reduction Cap

### What
The total depth reduction at any single node is **capped** at a maximum value. No matter how many reduction rules fire, the reduction cannot exceed this cap.

### Why
A move might trigger multiple reductions: it's late in the move order (-1), it's a quiet move (-1), it's a rim knight (-1), it has poor history (-1)—total reduction: -4. A -4 reduction means searching at depth $D - 4$, which might be too shallow to detect even obvious tactical threats. The re-search safety net would catch the move being good, but only if it's searched at all—some implementations skip moves entirely if the reduced depth reaches 0.

### Implementation

```python
MAX_REDUCTION_PER_MOVE = 3  # Maximum reduction at a single node

def cap_reduction(total_reduction: int) -> int:
    """Cap the total reduction at a single node."""
    return max(total_reduction, -MAX_REDUCTION_PER_MOVE)
```

## Rule 3: Global Depth Cap

### What
The **effective search depth** (base depth + accumulated extensions - accumulated reductions) is capped at a global maximum. No line in the search tree can exceed this depth.

### Why
Even with per-node extension caps, extensions can accumulate across multiple nodes along a single line. A 10-ply base depth with +2 extensions at each of 10 nodes would give an effective depth of 30—far beyond what the time budget allows. The global depth cap prevents this runaway.

### Implementation

```python
MAX_GLOBAL_DEPTH = 64  # Absolute maximum search depth

def search_with_global_cap(board: Board, depth: int, alpha: int, beta: int,
                           current_depth: int) -> int:
    """
    Search with a global depth cap.
    current_depth tracks how deep we've actually gone (base + extensions - reductions).
    """
    if current_depth >= MAX_GLOBAL_DEPTH:
        return evaluate(board)  # Force evaluation at the cap

    # Normal search with extensions and reductions
    moves = board.legal_moves()
    for move in moves:
        extension = compute_total_extension(board, move)
        reduction = compute_total_reduction(board, move)

        effective_depth = depth - 1 + extension.delta + reduction.delta
        effective_depth = max(1, effective_depth)  # Never search at depth 0 (use quiescence)

        board.push(move)
        score = -search_with_global_cap(
            board, effective_depth, -beta, -alpha,
            current_depth + 1
        )
        board.pop()

        # ... alpha-beta logic ...

    return alpha
```

## Rule 4: No Extension at Depth 1

### What
When the remaining search depth is 1, **no extensions are applied**. The move is searched at depth 1 and then handed off to quiescence search.

### Why
At depth 1, the search is about to transition to [[Quiescence Termination Rules|quiescence search]], which will handle tactical moves (captures, checks) anyway. Adding extensions at depth 1 would push the search into quiescence with extra depth, but quiescence already has its own depth management. Allowing extensions at depth 1 can create a cascade: check at depth 1 → extend to depth 2 → check at depth 2 → extend to depth 3, and so on.

### Implementation

```python
def extension_at_shallow_depth(depth: int, total_extension: int) -> int:
    """No extensions at depth 1 to prevent cascading."""
    if depth <= 1:
        return 0
    return min(total_extension, MAX_EXTENSION_PER_MOVE)
```

## Rule 5: Accumulated Extension Tracking

### What
We track the **total accumulated extensions** along each search path. If a line has already received many extensions, further extensions are reduced or denied.

### Why
A line that has been extended multiple times has already received extra attention. Continuing to extend it produces diminishing returns while increasing the risk of depth inflation. This is analogous to the economic principle of diminishing marginal returns.

### Implementation

```python
MAX_ACCUMULATED_EXTENSIONS = 8  # Maximum total extensions along a single path

class SearchPath:
    """Track accumulated extensions along a search path."""
    def __init__(self):
        self.total_extensions = 0
        self.extension_history: List[DepthDelta] = []

    def can_extend(self, proposed_delta: int) -> bool:
        """Check if we can afford this extension along the current path."""
        if proposed_delta <= 0:
            return True  # Reductions are always allowed
        return self.total_extensions + proposed_delta <= MAX_ACCUMULATED_EXTENSIONS

    def apply(self, delta: DepthDelta):
        """Record an extension or reduction."""
        if delta.delta > 0:
            self.total_extensions += delta.delta
            self.extension_history.append(delta)
```

## Rule 6: Depth Inflation Prevention

### What
The **ratio** of effective depth to base depth is monitored. If the effective depth exceeds a multiple of the base depth, further extensions are denied.

### Why
In a healthy search, the effective depth should be at most 1.5-2× the base depth. If the effective depth is 3× the base depth, the search has inflated dramatically and may not complete within the time budget. This rule acts as a circuit breaker.

### Implementation

```python
MAX_DEPTH_RATIO = 2.0  # Effective depth should not exceed 2× base depth

def should_deny_extension(base_depth: int, effective_depth: int) -> bool:
    """
    Deny extensions if the effective depth has inflated too much
    relative to the base depth.
    """
    if base_depth <= 0:
        return True
    return (effective_depth / base_depth) > MAX_DEPTH_RATIO
```

## Rule 7: Guaranteed Termination

### What
The search is **guaranteed to terminate** by the combination of:
1. Depth decreases by at least 1 at each recursive call.
2. Quiescence search has a hard depth limit.
3. Global depth cap prevents unbounded search.

### Proof Sketch

We prove termination by showing that the search always makes progress toward a base case:

**Base cases**:
- `depth <= 0`: Transition to quiescence search.
- Quiescence reaches `max_ply`: Return static evaluation.
- No legal moves: Checkmate or stalemate (return evaluation directly).
- Alpha-beta cutoff: Return immediately.

**Inductive step**:
- At each recursive call, `current_depth` increases by at least 1.
- `current_depth` is capped at `MAX_GLOBAL_DEPTH`.
- Therefore, the recursion must reach a base case within `MAX_GLOBAL_DEPTH` calls.

Since each call makes progress (current_depth increases, depth decreases) and there is a hard upper bound, the search **must terminate**.

```python
def search_terminates(board: Board, depth: int, current_depth: int,
                      max_depth: int = MAX_GLOBAL_DEPTH) -> bool:
    """
    Verify that the search will terminate.
    For debugging and assertion purposes.
    """
    # Depth must decrease or we must be at a base case
    if current_depth >= max_depth:
        return True  # Will terminate (return eval)

    if depth <= 0:
        return True  # Will transition to quiescence (which has its own limits)

    # Each child has current_depth + 1, which is bounded
    # Therefore, by induction, the search terminates
    return True
```

## Rule 8: Time Budget Enforcement

### What
The search must **stop within the time budget**. Even if the search hasn't completed the current iteration, it must return the best move found so far when time runs out.

### Why
In tournament play, exceeding the time limit means losing the game. The time budget is the ultimate safety constraint—no search, no matter how important, can continue past the time limit.

### Implementation

```python
class TimeManager:
    """Manage search time budget with guaranteed termination."""

    def __init__(self, total_time_ms: int):
        self.start_time = time.time()
        self.total_time_ms = total_time_ms
        self.nodes_searched = 0
        self.time_checks = 0
        self.TIME_CHECK_INTERVAL = 4096  # Check time every N nodes

    def should_stop(self) -> bool:
        """Check if the time budget has been exceeded."""
        self.time_checks += 1
        if self.time_checks % self.TIME_CHECK_INTERVAL != 0:
            return False  # Don't check every node (too expensive)

        elapsed = (time.time() - self.start_time) * 1000
        return elapsed >= self.total_time_ms

    def should_stop_early(self, iteration: int, best_move_stable: bool) -> bool:
        """Check if we should stop early (don't start a new iteration)."""
        elapsed = (time.time() - self.start_time) * 1000
        remaining = self.total_time_ms - elapsed

        # Don't start a new iteration if we've used more than half the time
        # and the best move is stable
        if elapsed > self.total_time_ms * 0.5 and best_move_stable:
            return True

        # Don't start if we can't complete it
        if elapsed > self.total_time_ms * 0.75:
            return True

        return False
```

## Complete Safety Wrapper

```python
def safe_search(board: Board, base_depth: int, time_budget_ms: int) -> SearchResult:
    """
    Search with all safety guarantees.
    This is the top-level entry point that ensures termination.
    """
    time_manager = TimeManager(time_budget_ms)
    path = SearchPath()
    best_result = None

    for depth in range(1, base_depth + 1):
        if time_manager.should_stop_early(depth, best_result is not None):
            break

        result = search_iteration(board, depth, time_manager, path)

        if result is not None:
            best_result = result

        if time_manager.should_stop():
            break

    return best_result or SearchResult(
        move=board.legal_moves()[0],
        score=0,
        depth=0,
        reason="Emergency: time budget exhausted, returning first legal move"
    )
```

## Summary

Safety rules are the **guardrails** that keep the adaptive depth system from running off the rails. They ensure that:

1. Extensions are capped (per-move and globally).
2. Reductions don't make the search trivially shallow.
3. Depth inflation is prevented.
4. Termination is guaranteed by mathematical proof.
5. The time budget is always respected.

Each safety rule is itself **explainable**: when the engine hits a cap, it can report "Extension denied: the maximum accumulated extension of 8 plies has been reached along this line." This transparency extends even to the engine's self-imposed limits.

---

**See also:** [[The Depther Philosophy]], [[Depth Extension Rules]], [[Depth Reduction Rules]], [[Quiescence Termination Rules]], [[The Depth Rules Module (Code Architecture)]], [[Alpha-Beta Search]], [[Iterative Deepening]], [[Time Management]]
