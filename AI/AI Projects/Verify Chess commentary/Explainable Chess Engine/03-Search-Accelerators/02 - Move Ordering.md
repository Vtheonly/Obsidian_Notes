---
tags:
  - search
  - move-ordering
  - MVV-LVA
  - killer-moves
  - history-heuristic
  - critical-optimization
chapter: "03"
---

# Move Ordering

## Overview

**Move ordering** is the single most critical optimization in a chess engine. The efficiency of [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta pruning]] depends almost entirely on the quality of move ordering — with perfect ordering, the effective branching factor drops from $B$ to $\sqrt{B}$, enabling search depths 2× deeper. With poor ordering, alpha-beta degrades to full Minimax. This note covers the complete move ordering hierarchy, from the TT move through MVV-LVA captures, killer moves, and the history heuristic.

---

## Why Move Ordering Matters

### The Mathematical Argument

As established in [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]], the number of nodes evaluated with alpha-beta depends on move ordering:

| Ordering | Effective BF | Depth-10 Nodes | vs. No Pruning |
|----------|-------------|----------------|----------------|
| None | 35 | 2.76 × 10¹⁵ | 1× |
| Poor | 25 | 9.77 × 10¹³ | 28× |
| Good | 10 | 10¹⁰ | 276,000× |
| Perfect | √35 ≈ 5.9 | 5.1 × 10⁷ | 54,000,000× |

Each improvement in move ordering translates directly into deeper search within the same time budget. Since each additional ply is worth ~80-100 Elo (see [[01-Foundations/01 - Chess as a Zero-Sum Game|Chess as a Zero-Sum Game]]), move ordering improvements have an **enormous** impact on playing strength.

### The Intuition

Alpha-beta pruning cuts off branches where the current move cannot beat the best move already found. **If the best move is searched first, all remaining moves can be pruned maximally.** If the best move is searched last, no pruning occurs until the final move.

The goal of move ordering is to **search the best move first** as often as possible.

---

## The Move Ordering Hierarchy

Moves are ordered using a priority score. Higher scores are searched first. The hierarchy, from highest to lowest priority:

### 1. TT Move (Priority: +10000)

The **Transposition Table move** — the best move found when this position was previously searched (at a shallower depth during [[03-Search-Accelerators/01 - Iterative Deepening|iterative deepening]]). This is the single most important ordering signal.

**Why it works**: If a move was best at depth $d-1$, it is very likely to be best at depth $d$ as well. Statistics show that the TT move is the best move in **85-95%** of positions.

**Implementation**:

```cpp
int score_move(const Position& pos, Move move, const SearchInfo& info) {
    // TT move gets highest priority
    if (move == info.tt_move) {
        return 10000;
    }

    // ... other scoring below
}
```

The TT move is checked first, before any other scoring. If the move matches the TT move, it immediately gets the highest score and is searched first.

### 2. Captures via MVV-LVA (Priority: +1000 to +1900)

**MVV-LVA** stands for **Most Valuable Victim – Least Valuable Attacker**. Captures are scored based on the value of the captured piece (victim) minus a fraction of the attacker's value.

**Why it works**: Capturing a queen with a pawn (QxP, but from the attacker's perspective, PxQ) is almost always a good move. Capturing a pawn with a queen (QxP) is often a bad trade. MVV-LVA prioritizes the former.

**The MVV-LVA Formula**:

$$\text{Priority} = 1000 + \text{Value}(\text{Victim}) \times 10 - \text{Value}(\text{Attacker})$$

Using standard piece values (Pawn=100, Knight=320, Bishop=330, Rook=500, Queen=900):

| Capture | Victim Value | Attacker Value | Priority |
|---------|-------------|---------------|----------|
| PxQ | 900 | 100 | 1000 + 9000 - 100 = 9900 |
| NxQ | 900 | 320 | 1000 + 9000 - 320 = 9680 |
| BxQ | 900 | 330 | 1000 + 9000 - 330 = 9670 |
| RxQ | 900 | 500 | 1000 + 9000 - 500 = 9500 |
| PxR | 500 | 100 | 1000 + 5000 - 100 = 5900 |
| NxR | 500 | 320 | 1000 + 5000 - 320 = 5680 |
| PxN | 320 | 100 | 1000 + 3200 - 100 = 4100 |
| PxP | 100 | 100 | 1000 + 1000 - 100 = 1900 |
| QxP | 100 | 900 | 1000 + 1000 - 900 = 1100 |

**Implementation**:

```cpp
// Piece values for MVV-LVA
constexpr int piece_value[7] = {
    0,    // EMPTY
    100,  // PAWN
    320,  // KNIGHT
    330,  // BISHOP
    500,  // ROOK
    900,  // QUEEN
    0     // KING (not capturable)
};

int score_capture(const Position& pos, Move move) {
    Piece victim = pos.piece_on(move.to());
    Piece attacker = pos.piece_on(move.from());
    return 1000 + piece_value[type_of(victim)] * 10 - piece_value[type_of(attacker)];
}
```

**Why multiply victim by 10?**: The victim value dominates the ordering. We want PxQ before NxQ (both capture the queen, but the pawn capture is "cheaper"). The ×10 multiplier ensures that the victim's value overwhelms the attacker's value:

$$\text{PxQ}: 1000 + 9000 - 100 = 9900$$
$$\text{NxP}: 1000 + 1000 - 320 = 1680$$

Without the ×10 multiplier, PxQ would score 1800 and NxP would score 780 — still correct ordering, but with less separation. The multiplier creates clear tiers: queen captures first, then rook captures, then minor piece captures, then pawn captures.

### 3. Killer Moves (Priority: +900)

**Killer moves** are quiet (non-capture) moves that caused a **beta cutoff** at the same ply (depth from root) in a sibling node. The idea: if a move was good enough to cause a cutoff in a similar position at the same depth, it's likely to cause a cutoff here too.

**Why it works**: Sibling nodes share many properties — the same pieces are on the board, just with one move's difference. A move that refutes one position often refutes similar positions.

**Killer Move Storage**:

Each ply maintains **2 killer move slots**:

```cpp
struct SearchInfo {
    Move killer_moves[MAX_DEPTH][2]; // 2 killers per ply
    // ...
};
```

**Killer Move Update**:

When a quiet move causes a beta cutoff, it replaces one of the killers:

```cpp
void update_killer_moves(SearchInfo& info, int ply, Move move) {
    // Don't add if it's already the first killer
    if (info.killer_moves[ply][0] != move) {
        // Shift: old first killer becomes second
        info.killer_moves[ply][1] = info.killer_moves[ply][0];
        info.killer_moves[ply][0] = move;
    }
}
```

**Killer Move Scoring**:

```cpp
int score_killer(const SearchInfo& info, int ply, Move move) {
    if (move == info.killer_moves[ply][0]) return 900;
    if (move == info.killer_moves[ply][1]) return 800;
    return 0;
}
```

**Why ply-indexed, not position-indexed?**: Killer moves are indexed by ply (distance from root) rather than by position hash. This is because the killer heuristic exploits the **locality** of the search tree — nearby positions in the search tree are similar. Position-indexed killers would require a hash table and lose this locality.

### 4. History Heuristic (Priority: +0 to +800)

The **history heuristic** is a global counter that tracks how often each move (from-square, to-square pair) has caused a beta cutoff throughout the entire search. Unlike killer moves (ply-local), the history heuristic is **global** across all positions.

**Why it works**: Some from-to move patterns are inherently good in many positions — e.g., Nf3 (knight to f3) is frequently a strong move. The history heuristic captures these patterns.

**History Score Update**:

When a quiet move causes a beta cutoff, its history score is increased:

```cpp
void update_history(int history[64][64], int from, int to, int depth) {
    history[from][to] += depth * depth;
}
```

The `depth * depth` weighting means that cutoffs at deeper levels contribute more — they represent stronger evidence that the move is good.

**History Score Decay**:

Over time, history scores can grow very large, causing the heuristic to become overly biased toward old data. Periodic decay prevents this:

```cpp
void decay_history(int history[64][64]) {
    for (int from = 0; from < 64; from++) {
        for (int to = 0; to < 64; to++) {
            history[from][to] /= 2; // Halve all scores
        }
    }
}
```

Decay is typically applied at the start of each new [[03-Search-Accelerators/01 - Iterative Deepening|iterative deepening]] iteration.

**History Score as Move Priority**:

```cpp
int score_history(const int history[64][64], Move move) {
    int raw = history[move.from()][move.to()];
    // Clamp to [0, 800] to keep below killer move priority
    return std::min(raw, 800);
}
```

---

## Complete Move Scoring Function

Combining all four levels into a single scoring function:

```cpp
int score_move(const Position& pos, Move move, int ply, const SearchInfo& info) {
    // Level 1: TT Move
    if (move == info.tt_move) {
        return 10000;
    }

    // Level 2: Captures (MVV-LVA)
    if (move.is_capture()) {
        Piece victim = pos.piece_on(move.to());
        Piece attacker = pos.piece_on(move.from());
        return 1000 + piece_value[type_of(victim)] * 10 - piece_value[type_of(attacker)];
    }

    // Level 3: Killer Moves
    if (move == info.killer_moves[ply][0]) return 900;
    if (move == info.killer_moves[ply][1]) return 800;

    // Level 4: History Heuristic
    return std::min(info.history[move.from()][move.to()], 800);
}
```

**Priority tiers**:
- TT Move: 10000
- Captures: 1000-9900 (MVV-LVA)
- Killer 1: 900
- Killer 2: 800
- History: 0-800

This ensures captures are always tried before quiet moves, and the TT move is always tried first.

---

## Move Sorting Implementation

### Incremental Selection (Pick Best)

Rather than sorting the entire move list, which is $O(n \log n)$, we use **incremental selection** — pick the best remaining move just before it's needed. This is $O(n)$ total for the entire search at a node:

```cpp
void pick_best_move(MoveList& moves, int* scores, int start_index) {
    int best_index = start_index;
    int best_score = scores[start_index];

    for (int i = start_index + 1; i < moves.count; i++) {
        if (scores[i] > best_score) {
            best_score = scores[i];
            best_index = i;
        }
    }

    // Swap the best move to the current position
    std::swap(moves[start_index], moves[best_index]);
    std::swap(scores[start_index], scores[best_index]);
}
```

Usage in the search loop:

```cpp
for (int i = 0; i < moves.count; i++) {
    pick_best_move(moves, scores, i);
    Move move = moves[i];
    // ... search this move
}
```

**Why incremental selection?**: Because of beta cutoffs, we often don't need to examine all moves. If a cutoff occurs after 3 moves, we've only paid for 3 selections ($O(3n)$) instead of a full sort ($O(n \log n)$). With a branching factor of 35 and typical cutoffs after 5-10 moves, incremental selection is significantly faster.

---

## Advanced Move Ordering Techniques

### Countermove Heuristic

The **countermove** is the move that refuted the previous move. If the last move was Nc3 and the refutation was Bb4, then Bb4 is the countermove to Nc3. This is stored as:

```cpp
Move countermove[12][64]; // [piece_that_moved][to_square]
```

When ordering moves, if the current move matches the countermove of the previous ply's move, it gets a bonus:

```cpp
if (move == info.countermove[prev_piece][prev_to]) {
    score += 600; // Between killer and history
}
```

### Continuation Heuristic

An extension of the countermove concept: track which piece-to-square combinations have historically followed other piece-to-square combinations. This creates a **piece-square continuation table**:

```cpp
int continuation_history[12][64][12][64]; // [prev_piece][prev_to][curr_piece][curr_to]
```

This is memory-intensive but provides strong move ordering for quiet moves.

### SEE (Static Exchange Evaluation)

For captures, SEE estimates the outcome of a series of recaptures on the same square. This distinguishes "winning captures" (QxP is winning if the pawn is undefended) from "losing captures" (QxP is losing if the pawn is defended by a pawn):

```cpp
int see(const Position& pos, Move move) {
    // Simulate the exchange sequence on the target square
    int gain[32]; // Gain at each depth of the exchange
    int depth = 0;
    int target = move.to();
    PieceType attacker = type_of(pos.piece_on(move.from()));

    gain[0] = piece_value[type_of(pos.piece_on(target))];

    // Iteratively find the least valuable attacker and add to the exchange
    while (true) {
        depth++;
        gain[depth] = piece_value[attacker] - gain[depth - 1];

        // Find the least valuable attacker of the target square
        attacker = least_valuable_attacker(pos, target);
        if (attacker == NONE) break;
    }

    // Negamax the gain array
    while (--depth > 0) {
        gain[depth - 1] = -std::max(-gain[depth - 1], gain[depth]);
    }

    return gain[0];
}
```

SEE is used to prune obviously losing captures (SEE < 0) during [[03-Search-Accelerators/03 - Late Move Reductions (LMR)|LMR]] and [[03-Search-Accelerators/05 - Quiescence Search|quiescence search]].

---

## Connection to Explainability

### Move Ordering IS the Engine's "Intuition"

The move ordering hierarchy reflects the engine's **priorities** — its implicit understanding of which chess principles matter most:

1. **TT Move** → "Prior knowledge" — "I've seen this position before, and this move was best."
2. **MVV-LVA Captures** → "Tactical urgency" — "Capture the most valuable piece with the cheapest attacker."
3. **Killer Moves** → "Local refutations" — "This move refuted a similar position at the same depth."
4. **History Heuristic** → "Global patterns" — "This from-to pair has been good across many positions."

The explanation system can leverage this: "The engine tried Nf3 first because it was the best move found at a shallower depth (TT move). Among the remaining moves, Bc4 was tried next because it captures the e6 pawn (MVV-LVA capture)."

### Explaining Why Moves Were Searched in a Particular Order

```
Move ordering at root:
  1. Nf3 (TT move from depth 7, score: +0.45) — searched first
  2. Bc4 (capture, MVV-LVA: 1550) — winning capture
  3. d4 (killer move, ply 0 slot 1) — caused cutoffs in sibling nodes
  4. Nc3 (history score: 450) — frequently good in similar positions
  5. Be2 (history score: 120) — occasionally good
  ... remaining moves ...
```

This ordering tells a story: the engine's "intuition" says Nf3 is best, but it verifies by searching alternatives in order of decreasing expected strength.

---

## Key Takeaways

- **Move ordering is the most important optimization** in a chess engine — it determines the efficiency of alpha-beta pruning.
- The **four-level hierarchy**: TT Move (+10000) → MVV-LVA Captures (+1000 to +1900) → Killer Moves (+900/+800) → History Heuristic (+0 to +800).
- **MVV-LVA** prioritizes capturing valuable pieces with cheap attackers: `Priority = 1000 + VictimValue×10 - AttackerValue`.
- **Killer moves** are quiet moves that caused cutoffs at the same ply — 2 slots per ply.
- **History heuristic** is a global counter of from-to pairs that caused cutoffs, with depth² weighting and periodic halving.
- **Incremental selection** (pick-best) is preferred over full sorting because cutoffs often occur early.
- For explainability, **move ordering reflects the engine's priorities** — its "intuition" about which principles matter most.

## Cross-References

- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the algorithm whose efficiency depends on move ordering
- [[02-Search-Algorithms/04 - Principal Variation Search (PVS)|PVS]] — benefits from TT move as the PV move
- [[03-Search-Accelerators/01 - Iterative Deepening|Iterative Deepening]] — provides TT moves for the next depth
- [[03-Search-Accelerators/03 - Late Move Reductions (LMR)|LMR]] — depends on good move ordering to be safe
- [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|Transposition Tables]] — source of TT moves
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — move ordering as the engine's "intuition"
