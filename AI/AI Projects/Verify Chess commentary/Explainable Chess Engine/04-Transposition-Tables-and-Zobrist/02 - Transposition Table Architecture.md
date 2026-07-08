---
tags:
  - transposition-table
  - TT
  - caching
  - replacement-strategy
  - bounds
  - memory
chapter: "04"
---

# Transposition Table Architecture

## Overview

The **Transposition Table (TT)** is a large hash table that stores the results of previously searched positions, allowing the engine to **avoid re-searching** positions it has already encountered. Since different move orders can lead to the same position (a **transposition**), the TT dramatically reduces the search tree. It is the single largest data structure in a chess engine and one of the most impactful optimizations — without it, modern search depths would be impossible. This note covers why transpositions exist, the TT entry structure, bound types, lookup logic, replacement strategies, memory management, and the critical connection to explainability.

---

## Why Transpositions Exist

### Different Paths, Same Position

In chess, the **order** in which moves are played often doesn't matter for the final position. For example:

```
Path 1: 1. e4 e5 2. Nf3 Nc6
Path 2: 1. Nf3 Nc6 2. e4 e5
```

Both paths lead to **exactly the same position**: the Italian Game setup. The engine should not search this position twice — the second time, it should look up the result from the first search.

This is a **transposition**: reaching the same position through a different sequence of moves.

### How Common Are Transpositions?

In practice, transpositions are **extremely common**:
- In the opening, many move orders lead to the same position
- In the middlegame, piece exchanges and retreats create transpositions
- In the endgame, the king's circuitous path creates many transpositions

Studies show that **20-40%** of positions in a typical search are transpositions — positions that were already searched at equal or greater depth. The TT allows the engine to skip these positions entirely.

### The Savings

Without the TT, the engine would re-search every transposed position from scratch. With the TT, a single hash table lookup (O(1)) replaces an entire subtree search (potentially O($B^D$) nodes). The TT typically reduces the total nodes searched by **50-70%**.

---

## TT Entry Structure

### Fields

Each TT entry stores the information needed to determine whether the stored result is usable:

```cpp
struct TTEntry {
    uint64_t key;       // 8 bytes: Zobrist hash key (for verification)
    int32_t score;      // 4 bytes: Search score from the position
    int16_t depth;      // 2 bytes: Depth at which the position was searched
    uint8_t flag;       // 1 byte: Bound type (EXACT, LOWER, UPPER)
    uint8_t age;        // 1 byte: Search generation (for replacement)
    uint32_t best_move; // 4 bytes: Best move found (compact encoding)
};
// Total: 20 bytes per entry (often padded to 20 or 24 bytes)
```

### Field Descriptions

**Key (8 bytes)**: The full 64-bit [[04-Transposition-Tables-and-Zobrist/01 - Zobrist Hashing|Zobrist hash]] key. Used to verify that the stored entry corresponds to the current position. Since the hash key is used to compute the index into the TT, we only need to store the full key for verification (the index alone is not sufficient due to the modulo operation used in indexing).

**Score (4 bytes)**: The search score of the position, from the side-to-move's perspective (using the [[02-Search-Algorithms/02 - Negamax Formulation|Negamax]] convention). This score may be an exact value or a bound, depending on the flag.

**Depth (2 bytes)**: The depth at which the position was searched. Deeper searches are more reliable. Used to determine whether the stored result is usable (we only use results from searches at least as deep as our current depth) and for replacement decisions.

**Flag (1 byte)**: The bound type, indicating what kind of score is stored. This is critical for correct TT usage (see Bound Types below).

**Age (1 byte)**: The search generation number. Incremented at the start of each [[03-Search-Accelerators/01 - Iterative Deepening|iterative deepening]] iteration. Used for replacement decisions — old entries are preferred for replacement.

**Best Move (4 bytes)**: The best move found during the search. Even if the stored score cannot be used (insufficient depth), the best move can still be used for [[03-Search-Accelerators/02 - Move Ordering|move ordering]], which is extremely valuable.

---

## Bound Types

### The Three Bound Types

The flag field determines how to interpret the stored score:

#### 1. EXACT (Flag = 0)

The score is the **exact** minimax value of the position. This occurs when the alpha-beta search completed without any cutoff — all moves were searched, and the final score was between alpha and beta.

$$\text{Score}_{\text{exact}} = V(s)$$

Usage: The score can be used directly. If the stored depth ≥ current depth, the position does not need to be searched at all.

#### 2. LOWER_BOUND (Flag = 1)

The score is a **lower bound** on the true value. This occurs when a **beta cutoff** was triggered — we found a move so good that the search was cut short. The true value is at least as high as the stored score, but could be higher.

$$\text{Score}_{\text{lower}} \leq V(s)$$

Usage: If the stored score ≥ beta, we can cutoff (the position is at least as good as the lower bound, which is already above beta). If the stored score > alpha, we can tighten alpha (the position is at least this good).

#### 3. UPPER_BOUND (Flag = 2)

The score is an **upper bound** on the true value. This occurs when **all moves failed low** — no move was able to raise the score above alpha. The true value is at most as high as the stored score, but could be lower.

$$V(s) \leq \text{Score}_{\text{upper}}$$

Usage: If the stored score ≤ alpha, we can cutoff (the position is at most this good, which is already below alpha). If the stored score < beta, we can tighten beta.

### When Each Bound Is Stored

```cpp
// In the search function:
int best_score = -INFINITY;

for (int i = 0; i < moves.count; i++) {
    pos.make_move(moves[i]);
    int score = -search(pos, depth - 1, -beta, -alpha);
    pos.unmake_move(moves[i]);

    if (score > best_score) best_score = score;
    if (score >= beta) {
        // BETA CUTOFF: Store LOWER_BOUND
        // The true value is at least 'best_score', possibly higher
        tt.store(key, best_score, depth, LOWER_BOUND, moves[i]);
        return best_score;
    }
    if (score > alpha) alpha = score;
}

if (best_score > original_alpha) {
    // Score improved alpha but didn't cutoff: Store EXACT
    tt.store(key, best_score, depth, EXACT, best_move);
} else {
    // All moves failed low: Store UPPER_BOUND
    tt.store(key, best_score, depth, UPPER_BOUND, Move::none());
}

return best_score;
```

### Summary Table

| Condition | Flag Stored | Meaning |
|-----------|-----------|---------|
| Beta cutoff (`score ≥ beta`) | `LOWER_BOUND` | True value ≥ stored score |
| Alpha improved, no cutoff | `EXACT` | True value = stored score |
| All moves failed low | `UPPER_BOUND` | True value ≤ stored score |

---

## TT Lookup Decision Flow

### The Complete Logic

When we encounter a position during search, we look it up in the TT:

```cpp
bool tt_lookup(const Position& pos, int depth, int alpha, int beta,
               int& tt_score, Move& tt_move, bool& cutoff) {
    uint64_t key = pos.hash_key;
    TTEntry* entry = tt.probe(key);

    if (entry == nullptr) {
        tt_move = Move::none();
        cutoff = false;
        return false; // No entry found
    }

    // Verify the key matches (collision check)
    if (entry->key != key) {
        tt_move = Move::none();
        cutoff = false;
        return false; // Collision — wrong position
    }

    // Always extract the best move for move ordering
    tt_move = entry->best_move;

    // Can we use the score?
    if (entry->depth >= depth) {
        switch (entry->flag) {
            case EXACT:
                // Exact score — use directly
                tt_score = entry->score;
                cutoff = true;
                return true;

            case LOWER_BOUND:
                // Score is at least entry->score
                if (entry->score >= beta) {
                    // Lower bound is above beta — cutoff
                    tt_score = entry->score;
                    cutoff = true;
                    return true;
                }
                // Tighten alpha if possible
                if (entry->score > alpha) {
                    alpha = entry->score;
                }
                break;

            case UPPER_BOUND:
                // Score is at most entry->score
                if (entry->score <= alpha) {
                    // Upper bound is below alpha — cutoff
                    tt_score = entry->score;
                    cutoff = true;
                    return true;
                }
                // Tighten beta if possible
                if (entry->score < beta) {
                    beta = entry->score;
                }
                break;
        }
    }

    // Entry exists but can't be used for score (insufficient depth or bounds don't help)
    cutoff = false;
    return false;
}
```

### Visual Decision Flow

```
TT Lookup
  │
  ├─ No entry → Continue search (but use TT move for ordering if available)
  │
  ├─ Key mismatch → Collision → Continue search
  │
  ├─ depth < current_depth → Shallow entry → Continue search, but use TT move
  │
  └─ depth >= current_depth
       │
       ├─ EXACT → Return stored score (no search needed!)
       │
       ├─ LOWER_BOUND
       │    ├─ score >= beta → Cutoff! Return score
       │    └─ score < beta → Tighten alpha, continue search
       │
       └─ UPPER_BOUND
            ├─ score <= alpha → Cutoff! Return score
            └─ score > alpha → Tighten beta, continue search
```

---

## Replacement Strategies

### The Problem

The TT has a fixed size. When a new entry needs to be stored and the target bucket is full, an existing entry must be **replaced**. The choice of which entry to replace has a significant impact on search quality.

### Strategy 1: Depth-Preferred

**Rule**: Always replace the entry with the shallowest depth. If the new entry has a greater depth, it replaces the old one.

```cpp
bool should_replace_depth_preferred(const TTEntry& existing, const TTEntry& new_entry) {
    return new_entry.depth > existing.depth;
}
```

**Advantages**: Deeper searches are more valuable — they represent more computation and more reliable results. Keeping deep entries maximizes the TT's value.

**Disadvantages**: Old deep entries from previous searches may never be replaced, even if they're no longer relevant to the current search.

### Strategy 2: Age-Preferred

**Rule**: Always replace the oldest entry. Age is tracked by the search generation number.

```cpp
bool should_replace_age_preferred(const TTEntry& existing, const TTEntry& new_entry) {
    return new_entry.age > existing.age;
}
```

**Advantages**: Entries from the current search are always preferred, ensuring relevance.

**Disadvantages**: A shallow entry from the current search will replace a deep entry from a previous search, potentially losing valuable information.

### Strategy 3: Two-Tier (Buddy System)

**Rule**: Each TT slot stores TWO entries: one depth-preferred and one age-preferred. New entries go to the age-preferred slot; the deeper of the two entries stays in the depth-preferred slot.

```cpp
struct TTBucket {
    TTEntry depth_entry;  // Always the deeper of the two
    TTEntry age_entry;    // Always the most recent
};

void store_in_bucket(TTBucket& bucket, const TTEntry& new_entry) {
    if (new_entry.depth >= bucket.depth_entry.depth) {
        // New entry is deeper than the depth entry
        // Move old depth entry to age slot, put new in depth slot
        bucket.age_entry = bucket.depth_entry;
        bucket.depth_entry = new_entry;
    } else {
        // New entry goes to age slot regardless
        bucket.age_entry = new_entry;
    }
}
```

**Advantages**: Combines the best of both strategies — deep entries are preserved while current entries are always stored.

**Disadvantages**: Doubles the memory per slot (20 → 40 bytes per bucket).

### Strategy 4: Depth-Age Hybrid

**Rule**: Replace based on a combined score of depth and age:

$$\text{ReplaceScore} = \text{depth} + 4 \times \text{age\_difference}$$

```cpp
bool should_replace_hybrid(const TTEntry& existing, const TTEntry& new_entry) {
    int existing_score = existing.depth + 4 * (current_generation - existing.age);
    int new_score = new_entry.depth; // New entry has age = current_generation
    return new_score > existing_score;
}
```

This is the strategy used by Stockfish and many other top engines. The factor of 4 means that an entry from 4 generations ago is treated as 16 plies shallower for replacement purposes.

---

## Memory Management

### Sizing the TT

The TT must be large enough to store useful entries but small enough to fit in available memory and, ideally, in the CPU cache. Common sizes:

| TT Size | Number of Entries (20 bytes each) | Memory |
|---------|----------------------------------|--------|
| 64 MB | ~3.4 million | 64 MB |
| 128 MB | ~6.7 million | 128 MB |
| 256 MB | ~13.4 million | 256 MB |
| 512 MB | ~26.8 million | 512 MB |
| 1 GB | ~53.7 million | 1 GB |
| 4 GB | ~214.7 million | 4 GB |
| 16 GB | ~858.9 million | 16 GB |

### Index Calculation

The TT index is computed from the Zobrist hash key using modular arithmetic:

```cpp
size_t tt_index(uint64_t key, size_t tt_size) {
    return key % (tt_size / sizeof(TTEntry));
}
```

For power-of-two TT sizes, the modulo can be replaced with a bitwise AND:

```cpp
size_t tt_index(uint64_t key, size_t tt_mask) {
    return key & tt_mask; // tt_mask = (tt_size / sizeof(TTEntry)) - 1
}
```

This requires the number of entries to be a power of 2, which is standard practice.

### Cache Efficiency

The TT's performance depends heavily on **cache efficiency**. A cache miss (loading from main memory) costs ~100-300 CPU cycles, while a cache hit costs ~3-5 cycles. With millions of TT lookups per second, cache misses can be devastating.

Strategies for cache efficiency:
1. **Use power-of-two sizes** for fast index computation (bitwise AND vs. modulo)
2. **Align entries to cache lines** (64 bytes) to avoid false sharing
3. **Use smaller entries** (20 bytes vs. 24 or 32 bytes) to fit more entries per cache line
4. **Prefetch TT entries** before they're needed:

```cpp
void search(Position& pos, int depth, int alpha, int beta) {
    // Prefetch the TT entry for this position
    TTEntry* entry = tt.probe(pos.hash_key);
    __builtin_prefetch(entry); // Load into cache before we need it

    // ... rest of search ...
}
```

### TT Clearing

The TT is typically **not cleared** between moves during a game — entries from previous moves may still be useful (positions can recur). However, the TT is usually cleared at the start of a new game:

```cpp
void TranspositionTable::clear() {
    std::memset(table, 0, size_bytes);
}
```

At the start of each [[03-Search-Accelerators/01 - Iterative Deepening|iterative deepening]] iteration, the generation counter is incremented instead of clearing the table:

```cpp
void TranspositionTable::new_search() {
    generation++; // Old entries become "stale" but are not immediately removed
}
```

---

## TT and Alpha-Beta Integration

### Complete Search with TT

```cpp
int search(Position& pos, int depth, int alpha, int beta, SearchInfo& info) {
    // TT Lookup
    int original_alpha = alpha;
    Move tt_move = Move::none();
    TTEntry* tt_entry = tt.probe(pos.hash_key);

    if (tt_entry != nullptr && tt_entry->key == pos.hash_key) {
        tt_move = tt_entry->best_move;

        if (tt_entry->depth >= depth) {
            int tt_score = tt_entry->score;

            // Adjust mate scores for ply distance
            if (tt_score > MATE_SCORE - MAX_DEPTH) {
                tt_score -= pos.ply();
            } else if (tt_score < -MATE_SCORE + MAX_DEPTH) {
                tt_score += pos.ply();
            }

            switch (tt_entry->flag) {
                case EXACT:
                    return tt_score;
                case LOWER_BOUND:
                    if (tt_score >= beta) return tt_score;
                    alpha = std::max(alpha, tt_score);
                    break;
                case UPPER_BOUND:
                    if (tt_score <= alpha) return tt_score;
                    beta = std::min(beta, tt_score);
                    break;
            }
        }
    }

    // Terminal conditions
    if (depth <= 0) return quiescence(pos, alpha, beta, info);
    if (pos.is_draw()) return 0;

    // Generate and order moves (TT move searched first)
    MoveList moves = pos.generate_legal_moves();
    order_moves(pos, moves, tt_move);

    int best_score = -INFINITY_SCORE;
    Move best_move = Move::none();

    for (int i = 0; i < moves.count; i++) {
        pos.make_move(moves[i]);
        int score = -search(pos, depth - 1, -beta, -alpha, info);
        pos.unmake_move(moves[i]);

        if (score > best_score) {
            best_score = score;
            best_move = moves[i];
        }

        if (score >= beta) {
            // Store LOWER_BOUND
            tt.store(pos.hash_key, best_score, depth, LOWER_BOUND, best_move);
            update_killer_moves(info, pos.ply(), moves[i]);
            return best_score;
        }

        if (score > alpha) {
            alpha = score;
        }
    }

    // Store result
    uint8_t flag = (best_score > original_alpha) ? EXACT : UPPER_BOUND;
    tt.store(pos.hash_key, best_score, depth, flag, best_move);

    return best_score;
}
```

### Mate Score Adjustment

Mate scores must be adjusted relative to the root position. A "mate in 3" from ply 5 is different from "mate in 3" from ply 10:

```cpp
// When storing: adjust to be relative to this node
if (best_score > MATE_SCORE - MAX_DEPTH) {
    store_score = best_score + pos.ply(); // Distance from THIS node
}
if (best_score < -MATE_SCORE + MAX_DEPTH) {
    store_score = best_score - pos.ply();
}

// When reading: adjust back to be relative to the root
if (tt_score > MATE_SCORE - MAX_DEPTH) {
    use_score = tt_score - pos.ply();
}
if (tt_score < -MATE_SCORE + MAX_DEPTH) {
    use_score = tt_score + pos.ply();
}
```

---

## Connection to Explainability

### "The Engine Remembered This Position Was Good Because..."

The TT is the engine's **memory** — it stores the results of previous analysis. The explanation system can leverage this:

```
This position was previously analyzed at depth 15.
The engine determined that the best move is Nf3 with a score of +0.45.

This analysis was performed 3 moves ago in the game, and the
position has reoccurred due to a transposition. The stored
result is being reused rather than re-searched.

Key factors from the previous analysis:
  - Nf3 controls the center and develops toward an outpost
  - The evaluation is exact (not a bound), so the score is reliable
```

### TT Best Move as "Prior Knowledge"

Even when the TT score cannot be used (insufficient depth or unhelpful bounds), the **best move** from the TT entry provides valuable move ordering information. For the explanation system, this is "prior knowledge" — a hint about which move to examine first:

```
The engine's prior analysis (depth 12) suggested Nf3 as the best move.
Current search is at depth 18, so the score is being recomputed,
but Nf3 is being examined first based on the prior recommendation.
```

### Explaining Why a Position Was Not Re-Searched

When a TT hit allows the search to skip a subtree entirely, the explanation system can note:

```
Position after Nc3: This position was already searched at depth 20
during the analysis of move Nf3 (a transposition occurred). The
stored result (+0.30, EXACT) is being reused, saving approximately
5 million node evaluations.

The position is the same whether reached via 1. e4 Nc6 2. Nf3 e5 3. Nc3
or 1. e4 e5 2. Nc3 Nc6 3. Nf3 — the move order doesn't matter.
```

### TT Bounds and Confidence

The bound type provides **confidence information** for the explanation:

- **EXACT**: "The engine is certain about this score."
- **LOWER_BOUND**: "The engine knows this position is at least this good, but it may be better."
- **UPPER_BOUND**: "The engine knows this position is at most this good, but it may be worse."

This maps naturally to confidence levels in the explanation system.

---

## Key Takeaways

- **Transposition tables** store results of previously searched positions, avoiding redundant computation when the same position is reached via different move orders.
- Each TT entry stores: **key** (verification), **score**, **depth**, **flag** (bound type), **age** (generation), and **best move**.
- **Three bound types**: EXACT (precise value), LOWER_BOUND (score is at least this), UPPER_BOUND (score is at most this). Each is stored and used differently.
- The **lookup decision flow** checks depth sufficiency and bound type to determine whether the stored score can be used directly or can only tighten the search window.
- **Replacement strategies** (depth-preferred, age-preferred, two-tier, hybrid) determine which entries are evicted when the TT is full.
- **Memory management** focuses on cache efficiency: power-of-two sizes, entry alignment, prefetching, and generation-based aging.
- For explainability, the TT provides **"memory" of prior analysis**, **prior knowledge** via best moves, and **confidence information** via bound types.

## Cross-References

- [[04-Transposition-Tables-and-Zobrist/01 - Zobrist Hashing|Zobrist Hashing]] — the hash key that indexes the TT
- [[02-Search-Algorithms/03 - Alpha-Beta Pruning|Alpha-Beta Pruning]] — the search that generates and consumes TT entries
- [[03-Search-Accelerators/01 - Iterative Deepening|Iterative Deepening]] — the search strategy that benefits most from TT
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — TT move is the highest-priority ordering signal
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — how TT provides memory and confidence for explanations
