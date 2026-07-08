---
tags:
  - search
  - iterative-deepening
  - time-management
  - move-ordering
chapter: "03"
---

# Iterative Deepening

## Overview

**Iterative Deepening** (ID) is a search strategy that performs a series of progressively deeper searches: first depth 1, then depth 2, then depth 3, and so on, until the time budget is exhausted. At first glance, this seems wasteful — why search depth 1 when you're going to search depth 2 anyway? The answer is profound: iterative deepening provides **near-perfect move ordering** for each subsequent depth, and the overhead of re-searching shallower depths is only about **3%**. It is one of the most counter-intuitive yet essential optimizations in chess programming.

---

## The Algorithm

### Basic Iterative Deepening

```python
def iterative_deepening(position, max_time_ms):
    best_move = None

    for depth in range(1, MAX_DEPTH):
        start_time = current_time_ms()

        move, score = search(position, depth)

        if current_time_ms() - start_time > max_time_ms:
            break  # Time's up — use the last completed result

        best_move = move

        print(f"depth {depth} score {score} move {move}")

    return best_move
```

At each depth, the search is started from scratch. The result from depth $d$ is used to inform the search at depth $d+1$ (via the [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|transposition table]] and [[03-Search-Accelerators/02 - Move Ordering|move ordering]]).

### Why It Seems Counter-Intuitive

The naive objection: "If you're going to search to depth 8, searching depths 1 through 7 first is wasted work."

The flaw in this reasoning: the work at depth 7 is **negligible** compared to the work at depth 8, and the move ordering information gained from depth 7 **dramatically reduces** the work at depth 8.

---

## The 3% Overhead Math

### Node Count at Each Depth

The total number of nodes at depth $D$ with branching factor $B$ is approximately:

$$N(D) = B^D$$

The total work of iterative deepening from depth 1 to depth $D$ is:

$$N_{\text{ID}}(D) = B^1 + B^2 + \ldots + B^D = \sum_{k=1}^{D} B^k$$

This is a geometric series. Since $B \gg 1$:

$$N_{\text{ID}}(D) = \frac{B^{D+1} - B}{B - 1} \approx \frac{B^{D+1}}{B - 1} \approx B^D \cdot \frac{B}{B-1}$$

The overhead compared to searching only depth $D$ directly:

$$\text{Overhead} = \frac{N_{\text{ID}}(D) - N(D)}{N(D)} = \frac{B}{B-1} - 1 = \frac{1}{B-1}$$

For $B = 35$:

$$\text{Overhead} = \frac{1}{34} \approx 2.9\%$$

**The overhead of iterative deepening is only ~3%!** The last depth dominates the total work so completely that all previous depths combined add less than 3% to the node count.

### Concrete Example

| Depth | Nodes at this depth | Cumulative ID nodes | Overhead vs. direct |
|-------|--------------------|--------------------|--------------------|
| 1 | 35 | 35 | +3,400% |
| 2 | 1,225 | 1,260 | +2.9% over direct depth 2 |
| 3 | 42,875 | 44,135 | +2.9% |
| 4 | 1,500,625 | 1,544,760 | +2.9% |
| 5 | 52,521,875 | 54,066,635 | +2.9% |

Even at depth 2, the overhead is already negligible. By depth 5, the first 4 depths combined add only 52 million nodes to the 52.5 million at depth 5 alone.

**With alpha-beta pruning**, the overhead is even lower because the effective branching factor is much smaller (see [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]]). With an effective $B' \approx 6$ (good move ordering), the overhead is $\frac{1}{5} = 20\%$ — still very acceptable.

---

## How Iterative Deepening Provides Move Ordering

### The Key Benefit

The primary benefit of iterative deepening is **not** the search results themselves — it's the **move ordering information** that each depth provides for the next.

At depth $d$, the search discovers:
1. The **best move** at the root (the PV move)
2. The **best move** at every internal position (stored in the [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|transposition table]])
3. The **principal variation** (the full line of best play)

When depth $d+1$ begins, this information is used to order moves:
- The TT move from depth $d$ is searched **first** at each node
- The PV from depth $d$ guides the initial search path
- History heuristic and killer moves from depth $d$ inform ordering

### The Move Ordering Cascade

Without iterative deepening, the first move tried at each node is essentially random. With iterative deepening, the first move is the **proven best move from the previous depth**:

```
Depth 1 search:  Finds best root move = e4
                 Stores in TT: position X → best move = Nf3

Depth 2 search:  Tries e4 first at root (from depth 1)
                 At position X, tries Nf3 first (from TT)
                 Finds best root move = d4

Depth 3 search:  Tries d4 first at root (from depth 2)
                 At position X, tries updated TT move
                 At position Y, tries the move from depth 2
                 Finds best root move = Nf3
```

Each depth's search benefits from the move ordering established by all previous depths. This creates a **virtuous cycle**: better move ordering → more pruning → faster search → deeper search → better move ordering.

---

## Time Management and Budgeting

### Why Time Management Matters

In tournament play, a chess engine has a **time budget** per move (e.g., 30 seconds). Iterative deepening provides the natural framework for time management: search deeper and deeper until time runs out, then return the result from the last completed depth.

### Time Controller Implementation

```cpp
class TimeManager {
    int64_t start_time_ms;
    int64_t allocated_time_ms;
    int64_t max_time_ms;

public:
    void init(int64_t time_remaining_ms, int64_t increment_ms, int moves_to_go) {
        start_time_ms = get_current_time_ms();

        // Allocate time based on remaining time and moves to go
        if (moves_to_go > 0) {
            allocated_time_ms = time_remaining_ms / moves_to_go
                              + increment_ms / 2;
        } else {
            // No moves-to-go information: use a fraction of remaining time
            allocated_time_ms = time_remaining_ms / 30
                              + increment_ms / 2;
        }

        // Safety margin: don't use more than 80% of remaining time
        max_time_ms = time_remaining_ms * 4 / 5;

        // Hard limit: never exceed this
        allocated_time_ms = std::min(allocated_time_ms, max_time_ms);
    }

    bool should_stop() const {
        return get_current_time_ms() - start_time_ms >= allocated_time_ms;
    }

    bool should_start_next_depth(int depth, int64_t estimated_time_ms) const {
        // Only start a new depth if we expect to finish it in time
        int64_t elapsed = get_current_time_ms() - start_time_ms;
        int64_t remaining = allocated_time_ms - elapsed;
        return remaining > estimated_time_ms;
    }

    int64_t elapsed() const {
        return get_current_time_ms() - start_time_ms;
    }
};
```

### Estimating Time for the Next Depth

The time for depth $d+1$ is approximately $B'$ times the time for depth $d$ (where $B'$ is the effective branching factor with pruning):

```cpp
bool should_start_next_depth(int depth, int64_t time_last_depth_ms) const {
    // Effective branching factor estimate
    double ebf = 1.5; // Conservative estimate with good pruning

    int64_t estimated_next_depth_ms = (int64_t)(time_last_depth_ms * ebf);
    int64_t remaining = allocated_time_ms - elapsed();

    return remaining > estimated_next_depth_ms * 2; // 2x safety margin
}
```

### The "Easy Move" Optimization

If the best move has been the same for several consecutive depths with a large margin, the engine can stop early:

```cpp
bool is_easy_move(const SearchInfo& info, int depth) {
    if (depth < 4) return false;

    // If the best move has been the same for 3+ depths
    // and the score margin is > 50 centipawns
    Move current_best = info.best_root_move;
    int same_count = 0;

    for (int d = depth - 3; d < depth; d++) {
        if (info.root_moves[d] == current_best) same_count++;
    }

    return same_count >= 3 && info.score_margin > 50;
}
```

---

## Iterative Deepening with PVS

Iterative deepening combines naturally with [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]]. The PV from depth $d$ provides the PV move for the PVS search at depth $d+1$:

```cpp
Move iterative_deepening(Position& pos, TimeManager& tm) {
    Move best_move = Move::none();
    int best_score = 0;
    SearchInfo info;

    tm.init(pos.time_remaining(), pos.increment(), pos.moves_to_go());

    for (int depth = 1; depth <= MAX_DEPTH; depth++) {
        int score = pvs(pos, depth, -INFINITY_SCORE, INFINITY_SCORE, info);

        if (tm.should_stop()) break; // Time expired mid-search

        best_move = info.pv_table[0][0];
        best_score = score;

        // Easy move check
        if (is_easy_move(info, depth) && depth >= 6) break;

        // Check if we have time for the next depth
        if (!tm.should_start_next_depth(depth, tm.elapsed())) break;

        // UCI output
        std::cout << "info depth " << depth
                  << " score cp " << best_score
                  << " nodes " << info.nodes_searched
                  << " nps " << (info.nodes_searched * 1000 / std::max(1LL, tm.elapsed()))
                  << " pv " << get_pv_string(info) << std::endl;
    }

    return best_move;
}
```

---

## Aspiration Windows with Iterative Deepening

A further optimization is to use **aspiration windows** — narrow search windows centered on the previous depth's score:

```cpp
for (int depth = 1; depth <= MAX_DEPTH; depth++) {
    int alpha, beta;

    if (depth <= 3) {
        // Low depths: full window
        alpha = -INFINITY_SCORE;
        beta  =  INFINITY_SCORE;
    } else {
        // Higher depths: aspiration window
        int window = 50; // 50 centipawns
        alpha = best_score - window;
        beta  = best_score + window;
    }

    int score = pvs(pos, depth, alpha, beta, info);

    // If score falls outside the aspiration window, re-search
    if (score <= alpha || score >= beta) {
        // Widen the window and re-search
        score = pvs(pos, depth, -INFINITY_SCORE, INFINITY_SCORE, info);
    }

    best_score = score;
    // ...
}
```

Aspiration windows work because the score rarely changes by more than 50 centipawns between depths. When it does, the re-search is a small cost compared to the savings from narrow windows at all other depths.

---

## Connection to Explainability

### Building the Reasoning Chain Progressively

Iterative deepening constructs the engine's **reasoning chain** one layer at a time:

- **Depth 1**: "I can see one move ahead. The best move captures a pawn."
- **Depth 2**: "After capturing, the opponent recaptures. It's still good."
- **Depth 3**: "But after recapturing, my knight is pinned! Maybe a different move..."
- **Depth 5**: "Actually, Nf3 develops and avoids the pin. This is best."

Each depth adds a layer of understanding. The explanation system can present this **progressive refinement** to the user:

```
Progressive analysis:
  Depth 1: Best move = Qxf7+ (captures pawn with check)
           Reason: Material gain (+100 centipawns)

  Depth 2: Best move = Qxf7+ ... Kd8
           Reason: Material gain holds up (+80 centipawns)

  Depth 3: Best move = Nf3 (changed!)
           Reason: After Qxf7+ Kd8, the queen is trapped!
                   Nf3 develops safely instead (+35 centipawns)

  Depth 5: Best move = Nf3 (confirmed)
           Reason: Nf3 develops, controls center, avoids traps
```

### The "Changed Mind" Event

When the best move changes between depths, this is a **critical event** for the explanation system. It indicates that deeper analysis revealed something the shallower search missed. These "changed mind" moments are often the most instructive:

```cpp
if (depth > 1 && info.best_root_move != previous_best_move) {
    info.explanation.add_event(
        "CHANGED_MIND",
        fmt::format("At depth {}, the best move changed from {} to {}. "
                    "Deeper analysis revealed that {} leads to {}",
                    depth, previous_best_move, info.best_root_move,
                    previous_best_move, info.why_previous_failed)
    );
}
```

### The PV as a Progressive Narrative

The PV at each depth tells a progressively longer "story":

```
Depth 1 PV: 1. e4
Depth 2 PV: 1. e4 e5
Depth 3 PV: 1. e4 e5 2. Nf3
Depth 5 PV: 1. e4 e5 2. Nf3 Nc6 3. Bb5
```

The explanation system can present this as "The engine's plan, as it sees deeper into the position."

---

## Key Takeaways

- **Iterative deepening** searches depth 1, then 2, then 3... until time runs out. The last completed depth's result is used.
- The overhead is only **~3%** because the deepest search dominates the total node count: $B^{D-1}$ is negligible compared to $B^D$.
- The real benefit is **move ordering**: each depth's results provide the TT move and PV for the next depth, creating a virtuous cycle of better ordering → more pruning → deeper search.
- **Time management** is natural with ID: stop when time runs out, return the last completed result.
- **Aspiration windows** further accelerate ID by using narrow search windows centered on the previous score.
- For explainability, ID builds a **progressive reasoning chain**, with "changed mind" events being particularly instructive.

## Cross-References

- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the search that iterative deepening calls at each depth
- [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — the search variant that benefits most from ID's move ordering
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — the critical optimization that ID feeds with TT/PV data
- [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|Transposition Tables]] — store results between ID iterations
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — how progressive reasoning supports explanation
