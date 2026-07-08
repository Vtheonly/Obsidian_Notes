# The Depther Philosophy

> "The depth of search is not the depth of understanding." — Chess Programming Aphorism

## Depth Is a Budget, Not a Fixed Number

In classical chess engines, the search depth is a fixed parameter: "search to depth 8" or "search to depth 12." Every move at every position gets the same depth allocation, regardless of whether the position is a quiet positional maneuver or a wild tactical melee. This is like giving every patient the same dose of medicine regardless of their condition.

The [[Depther]] philosophy rejects this uniformity. **Depth is a budget**, and like any budget, it should be allocated where it matters most. A quiet position with no tactics does not need depth 12—it needs depth 4. A position with forced checkmate needs depth 20+. The Depther's job is to **distribute search depth intelligently**, spending more on important lines and less on irrelevant ones.

Formally, let $D$ be the base search depth. For each move $m$ at each node, the Depther computes a **depth delta** $\delta(m)$:

$$
D_{\text{effective}}(m) = D + \delta(m)
$$

where $\delta(m) > 0$ is an **extension** (spending more budget on this line) and $\delta(m) < 0$ is a **reduction** (saving budget from this line). The total depth budget across the tree is approximately conserved: extensions on important lines are paid for by reductions on unimportant ones.

## Why Fixed Depth Doesn't Scale

Consider two scenarios:

### Scenario A: The Quiet Position
```
rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1
```
After 1.e4, Black has 20 legal moves. Most are roughly equivalent in evaluation. Searching all 20 moves to depth 12 wastes enormous computation on positions that are essentially equal. A depth-6 search would yield the same conclusion in 1/64th the time.

### Scenario B: The Tactical Melee
```
r1b1k2r/ppppqppp/2n2n2/2b5/3NP3/2P1B3/PP3PPP/RN1QKB1R w KQkq - 0 1
```
This position is a tactical knife-fight. Every move matters. A forced sequence might require depth 15+ to resolve. A fixed depth-8 search might miss the winning combination entirely.

**The problem**: Fixed depth over-searches quiet positions and under-searches tactical ones. The Depther solves this by making depth **adaptive**.

## Prove Importance Before Granting Depth

The core principle of the Depther is: **prove importance before granting depth**. A move must earn its extra search depth by exhibiting one or more of the following properties:

1. **It gives check** — forcing the opponent to respond.
2. **It captures a piece** — directly changing the material balance.
3. **It threatens promotion** — a pawn is one step from queening.
4. **It creates a tactical threat** — fork, pin, discovered attack.
5. **It is the only legal move** — the position is forced.
6. **It recaptures** — maintaining material balance in a specific line.

Conversely, moves that are **quiet, positionally neutral, and historically poor** should have their depth **reduced**:

1. **Late moves in move ordering** — unlikely to be best.
2. **Quiet moves with no tactical significance** — positional only.
3. **Mindless exchanges** — trading pieces without purpose.
4. **Rim knights** — edge-of-board knight moves are rarely best.
5. **Historically failed moves** — this move has been tried and rejected before.

This philosophy directly mirrors how strong human players think: they spend more time on critical positions and less on obvious ones. A grandmaster doesn't spend 5 minutes on every move—they spend 20 minutes on one critical move and 10 seconds on ten routine moves.

## The Vision of Explainable Depth

In a traditional engine, the depth delta is an invisible implementation detail. The engine searches to depth 10 with various extensions and reductions, but the user never knows *why* certain lines were explored more deeply than others.

In our [[Explainable Chess Engine]], **every depth adjustment carries a reason**. When the engine extends a line by 1 ply, it can explain:

> "Extending this line by 1 ply because: the move Bxf7+ gives check, which forces the opponent's response and may lead to a tactical sequence."

When it reduces a line by 1 ply:

> "Reducing this line by 1 ply because: the move a3 is a quiet pawn move with no tactical significance, and similar moves have historically been poor in this position."

This transforms the search from a black box into a **transparent decision-making process**. The user can understand not just *what* the engine found, but *where it looked* and *why it looked there*.

## Depth Rules as a Rule Engine

The Depther is implemented as a **rule engine**—a collection of independent rules, each of which can propose a depth delta (positive or negative) with an associated reason string. The final depth delta is the sum of all applicable rules:

$$
\delta(m) = \sum_{r \in \text{Rules}} r(m)
$$

Each rule $r$ examines the current position and the move $m$ and returns:

```python
@dataclass
class DepthDelta:
    delta: int        # +1 for extension, -1 for reduction
    reason: str       # Human-readable explanation
    rule_name: str    # Identifier for the rule
    priority: int     # Higher = more important (for conflict resolution)
```

This architecture is:
- **Extensible**: New rules can be added without modifying existing ones.
- **Explainable**: Each rule provides its own reason string.
- **Composable**: Rules can be combined; their effects are additive.
- **Debuggable**: We can inspect which rules fired and why.

## The Depth Budget Analogy

Think of the Depther as a financial advisor managing a search budget:

| Concept | Financial Analogy | Chess Analogy |
|---------|-------------------|---------------|
| Base depth | Monthly salary | Default search depth |
| Extensions | Investments | Additional depth on promising lines |
| Reductions | Savings | Less depth on unpromising lines |
| Max cap | Credit limit | Maximum allowed depth to prevent runaway |
| Quiescence | Emergency fund | Continue searching tactical moves at depth 0 |

Just as a financial advisor allocates more money to high-return investments and less to low-return savings accounts, the Depther allocates more depth to tactically rich lines and less to quiet positional lines.

## Historical Context

The idea of adaptive depth is not new. The key milestones:

1. **Deep Blue (1997)**: Used singular extensions—extending lines where one move was clearly best.
2. **Stockfish (2010s)**: Pioneered Late Move Reductions (LMR), reducing depth on later moves in the move order.
3. **Komodo (2010s)**: Developed sophisticated extension/reduction heuristics.
4. **Our engine (2024)**: Makes every extension and reduction **explainable**, with human-readable reasons.

The difference is not in the *mechanism* (extensions and reductions are standard) but in the **transparency**. Our engine doesn't just extend or reduce—it tells you *why*.

## The Depther in the Search Pipeline

The Depther operates at two points in the search:

1. **Root-level selectivity**: At the root, not all moves are searched at full depth. The top $K$ moves (by heuristic score) get full depth; the rest get reduced depth. See [[Root-Level Selectivity]].

2. **Node-level adjustment**: At every internal node, each move is evaluated by the rule engine to determine its depth delta. See [[Depth Extension Rules]] and [[Depth Reduction Rules]].

```
┌──────────────────────────┐
│     Root Level           │
│  Sort moves by heuristic │
│  Top K → full depth      │
│  Others → reduced depth  │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│     Each Internal Node   │
│  For each move m:        │
│    δ = 0                 │
│    For each rule r:      │
│      δ += r(m)           │
│    D_eff = D + δ         │
│    Search m to D_eff     │
└──────────────────────────┘
```

## The Cost of Explainability

Generating reason strings and `DepthDelta` objects adds overhead. Our benchmarks show approximately 5-10% performance cost compared to a traditional engine without explainability. We consider this acceptable because:

1. The rule engine itself is fast ($O(1)$ per rule per move).
2. The main cost is string construction, which we can optimize with lazy evaluation.
3. The benefit—transparent, teachable search decisions—far outweighs the cost.

```python
# Optimization: only generate reason strings when needed
class LazyDepthDelta:
    def __init__(self, delta, rule_name, reason_fn):
        self._delta = delta
        self._rule_name = rule_name
        self._reason_fn = reason_fn  # Callable, evaluated lazily
        self._reason = None

    @property
    def delta(self):
        return self._delta

    @property
    def reason(self):
        if self._reason is None:
            self._reason = self._reason_fn()
        return self._reason
```

## Summary

The Depther philosophy is simple: **treat depth as a scarce resource and allocate it where it matters most**. This is not just an optimization—it is a design principle that aligns with how humans think about chess and enables the engine to **explain** its search decisions. Every extension says "this line is promising"; every reduction says "this line is probably not worth exploring." Together, they form a coherent, transparent search strategy.

---

**See also:** [[Root-Level Selectivity]], [[Depth Extension Rules]], [[Depth Reduction Rules]], [[Quiescence Termination Rules]], [[Safety and Control Rules]], [[The Depth Rules Module (Code Architecture)]], [[Alpha-Beta Search]], [[LMR]], [[Singular Extensions]]
