# Declarative Rule Engine with Bitboards

> **Chapter 12 — Neuro-Symbolic Integration** | ← [[C++ Python Interfacing via Ctypes]] | → [[The Verbalization Pipeline]]

---

## The Performance Challenge

The [[Neuro-Symbolic Architecture Overview|architecture]] requires evaluating 200+ heuristic rules on millions of positions during search. If each rule takes even 10 microseconds, evaluating all rules takes 2 milliseconds per position—far too slow when we need to evaluate millions of positions per second.

The solution: **bitboard-based rule evaluation** that processes all 64 squares simultaneously using 64-bit integer operations.

---

## Bitboard Fundamentals

### What is a Bitboard?

A bitboard is a **64-bit integer** where each bit represents one square on the chess board:

```
Bit layout (MSB = a8, LSB = h1):

  63 62 61 60 59 58 57 56    a8 b8 c8 d8 e8 f8 g8 h8
  55 54 53 52 51 50 49 48    a7 b7 c7 d7 e7 f7 g7 h7
  47 46 45 44 43 42 41 40    a6 b6 c6 d6 e6 f6 g6 h6
  39 38 37 36 35 34 33 32    a5 b5 c5 d5 e5 f5 g5 h5
  31 30 29 28 27 26 25 24    a4 b4 c4 d4 e4 f4 g4 h4
  23 22 21 20 19 18 17 16    a3 b3 c3 d3 e3 f3 g3 h3
  15 14 13 12 11 10  9  8    a2 b2 c2 d2 e2 f2 g2 h2
   7  6  5  4  3  2  1  0    a1 b1 c1 d1 e1 f1 g1 h1
```

### Core Bitboard Types

```cpp
#include <cstdint>
#include <bit>

using Bitboard = uint64_t;

// Empty bitboard
constexpr Bitboard BB_EMPTY = 0ULL;

// Full bitboard
constexpr Bitboard BB_ALL = ~0ULL;

// Single square bitboard
constexpr Bitboard sq_bb(int sq) {
    return 1ULL << sq;
}

// Square indices
enum Square : int {
    SQ_A1=0,  SQ_B1,  SQ_C1,  SQ_D1,  SQ_E1,  SQ_F1,  SQ_G1,  SQ_H1,
    SQ_A2,    SQ_B2,  SQ_C2,  SQ_D2,  SQ_E2,  SQ_F2,  SQ_G2,  SQ_H2,
    SQ_A3,    SQ_B3,  SQ_C3,  SQ_D3,  SQ_E3,  SQ_F3,  SQ_G3,  SQ_H3,
    SQ_A4,    SQ_B4,  SQ_C4,  SQ_D4,  SQ_E4,  SQ_F4,  SQ_G4,  SQ_H4,
    SQ_A5,    SQ_B5,  SQ_C5,  SQ_D5,  SQ_E5,  SQ_F5,  SQ_G5,  SQ_H5,
    SQ_A6,    SQ_B6,  SQ_C6,  SQ_D6,  SQ_E6,  SQ_F6,  SQ_G6,  SQ_H6,
    SQ_A7,    SQ_B7,  SQ_C7,  SQ_D7,  SQ_E7,  SQ_F7,  SQ_G7,  SQ_H7,
    SQ_A8,    SQ_B8,  SQ_C8,  SQ_D8,  SQ_E8,  SQ_F8,  SQ_G8,  SQ_H8,
    SQ_NONE = 64
};
```

### Position Representation

```cpp
struct Position {
    // Piece bitboards (one per piece type per color)
    Bitboard pawns[2];      // [WHITE, BLACK]
    Bitboard knights[2];
    Bitboard bishops[2];
    Bitboard rooks[2];
    Bitboard queens[2];
    Bitboard kings[2];

    // Aggregate bitboards
    Bitboard occupied[2];   // All pieces per color
    Bitboard all_occupied;  // All pieces on the board

    // Side to move, castling rights, en passant, etc.
    Color side_to_move;
    int castling_rights;
    Square en_passant;
    int halfmove;
    int fullmove;

    // Fast piece-type queries
    Piece piece_on(Square sq) const;
    bool is_square_occupied(Square sq) const { return all_occupied & sq_bb(sq); }
};
```

---

## Bitwise Operations for Rule Checking

### The Power of Bitwise Masking

The key insight: **bitwise operations on 64-bit integers process all 64 squares simultaneously**. A single AND, OR, or NOT operation replaces a loop over 64 squares.

| Operation | Meaning | Example |
|---|---|---|
| `A & B` | Squares in both A and B | Squares with both a knight AND pawn support |
| `A \| B` | Squares in A or B | All attacked squares |
| `A ^ B` | Squares in A or B but not both | Changed squares |
| `~A` | Squares NOT in A | Unoccupied squares |
| `A & ~B` | Squares in A but not B | Pawn squares without adjacent pawns |

### Popcount: Counting Set Bits

```cpp
#include <bit>

// Count the number of set bits (1s) in a bitboard
inline int popcount(Bitboard bb) {
    return std::popcount(bb);  // C++20, compiles to POPCNT instruction
}
```

The `POPCNT` instruction is a single CPU instruction (on modern x86/ARM) that counts set bits in a 64-bit integer. This is incredibly fast: **1 clock cycle** vs. a loop that would take 64 iterations.

---

## Rule Implementation Examples

### Example 1: Knight on Rim Detection

The classic rule: "A knight on the rim is dim." Knights on the a- and h-files or 1st and 8th ranks have fewer squares to jump to.

```cpp
// Precomputed masks for edge squares
constexpr Bitboard BB_FILE_A = 0x0101010101010101ULL;
constexpr Bitboard BB_FILE_H = 0x8080808080808080ULL;
constexpr Bitboard BB_RANK_1 = 0x00000000000000FFULL;
constexpr Bitboard BB_RANK_8 = 0xFF00000000000000ULL;
constexpr Bitboard BB_RIM = BB_FILE_A | BB_FILE_H | BB_RANK_1 | BB_RANK_8;

int eval_knight_on_rim(const Position& pos) {
    // Get all knights for the side to move
    Bitboard knights = pos.knights[pos.side_to_move];

    // Find knights on the rim: knights AND rim squares
    Bitboard rim_knights = knights & BB_RIM;

    // Count them and apply penalty
    int count = popcount(rim_knights);
    return count * EvalWeights::W_KNIGHT_ON_RIM;  // Typically -30cp each
}
```

**What this does in one operation**: Instead of checking each of 64 squares individually ("Is there a knight here? Is this square on the rim?"), we AND the knight bitboard with the rim mask and count the result. **No loops.**

### Example 2: Pawn Outpost

A pawn outpost is a square on the opponent's half of the board where:
1. A friendly knight stands
2. No enemy pawn can attack the square

```cpp
// Precomputed: squares that can be attacked by enemy pawns
// For each square, which pawns could attack it?
Bitboard pawn_attack_mask(Color c, Square sq) {
    // White pawns attack diagonally up-left and up-right
    // Black pawns attack diagonally down-left and down-right
    Bitboard bb = sq_bb(sq);
    if (c == WHITE) {
        return ((bb & ~BB_FILE_A) << 7) | ((bb & ~BB_FILE_H) << 9);
    } else {
        return ((bb & ~BB_FILE_A) >> 9) | ((bb & ~BB_FILE_H) >> 7);
    }
}

int eval_knight_outpost(const Position& pos) {
    Color us = pos.side_to_move;
    Color them = ~us;
    int score = 0;

    Bitboard our_knights = pos.knights[us];
    Bitboard their_pawns = pos.pawns[them];
    Bitboard our_pawns = pos.pawns[us];

    // Iterate over each knight (typically 0-2)
    while (our_knights) {
        Square sq = static_cast<Square>(
            std::countr_zero(our_knights)  // Find first set bit
        );
        our_knights &= our_knights - 1;  // Clear LSB

        // Check 1: Is this square on the opponent's side?
        if (us == WHITE && sq < SQ_A5) continue;
        if (us == BLACK && sq > SQ_H4) continue;

        // Check 2: Can any enemy pawn attack this square?
        Bitboard enemy_pawn_attacks = pawn_attack_mask(them, sq);
        bool can_be_challenged = (their_pawns & enemy_pawn_attacks) != 0;

        if (!can_be_challenged) {
            // This is an outpost!

            // Bonus for being protected by our own pawn
            Bitboard our_pawn_attacks = pawn_attack_mask(us, sq);
            bool is_protected = (our_pawns & our_pawn_attacks) != 0;

            int bonus = is_protected ?
                EvalWeights::W_KNIGHT_OUTPOST_PROTECTED :
                EvalWeights::W_KNIGHT_OUTPOST_UNPROTECTED;

            score += bonus;
        }
    }

    return score;
}
```

### Example 3: Open Files for Rooks

A file is "open" if it contains no pawns. A rook on an open file is very strong.

```cpp
// Precomputed masks for each file
constexpr Bitboard BB_FILES[8] = {
    0x0101010101010101ULL,  // a-file
    0x0202020202020202ULL,  // b-file
    0x0404040404040404ULL,  // c-file
    0x0808080808080808ULL,  // d-file
    0x1010101010101010ULL,  // e-file
    0x2020202020202020ULL,  // f-file
    0x4040404040404040ULL,  // g-file
    0x8080808080808080ULL,  // h-file
};

int eval_rook_open_file(const Position& pos) {
    Color us = pos.side_to_move;
    Color them = ~us;
    int score = 0;

    Bitboard our_rooks = pos.rooks[us];
    Bitboard all_pawns = pos.pawns[WHITE] | pos.pawns[BLACK];
    Bitboard our_pawns = pos.pawns[us];
    Bitboard their_pawns = pos.pawns[them];

    while (our_rooks) {
        Square sq = static_cast<Square>(std::countr_zero(our_rooks));
        our_rooks &= our_rooks - 1;

        int file = sq % 8;
        Bitboard file_mask = BB_FILES[file];

        // Check if the file has any pawns at all
        bool has_any_pawn = (all_pawns & file_mask) != 0;

        if (!has_any_pawn) {
            // Open file! Big bonus.
            score += EvalWeights::W_ROOK_OPEN_FILE;
        } else {
            // Semi-open file: no friendly pawns
            bool has_our_pawn = (our_pawns & file_mask) != 0;
            if (!has_our_pawn) {
                score += EvalWeights::W_ROOK_SEMI_OPEN_FILE;
            }
        }
    }

    return score;
}
```

### Example 4: Passed Pawn

A passed pawn has no enemy pawn on the same or adjacent files ahead of it.

```cpp
int eval_passed_pawn(const Position& pos) {
    Color us = pos.side_to_move;
    Color them = ~us;
    int score = 0;

    Bitboard our_pawns = pos.pawns[us];
    Bitboard their_pawns = pos.pawns[them];

    while (our_pawns) {
        Square sq = static_cast<Square>(std::countr_zero(our_pawns));
        our_pawns &= our_pawns - 1;

        int file = sq % 8;
        int rank = sq / 8;

        // Compute the "front span" of this pawn:
        // All squares ahead on the same and adjacent files
        Bitboard front_span = compute_front_span(sq, us);

        // A passed pawn: no enemy pawns in the front span
        bool is_passed = (their_pawns & front_span) == 0;

        if (is_passed) {
            // Bonus increases with rank (closer to promotion)
            int rank_bonus = (us == WHITE) ? (rank - 1) : (6 - rank);
            score += EvalWeights::W_PASSED_PAWN[rank_bonus];

            // Extra bonus if the pawn is protected
            Bitboard our_pawn_attacks = pawn_attack_mask(us, sq);
            bool is_protected = (our_pawns & our_pawn_attacks) != 0;
            if (is_protected) {
                score += EvalWeights::W_PASSED_PAWN_PROTECTED[rank_bonus];
            }
        }
    }

    return score;
}

Bitboard compute_front_span(Square sq, Color c) {
    int file = sq % 8;
    int rank = sq / 8;

    Bitboard span = BB_EMPTY;

    if (c == WHITE) {
        // All squares ahead on files file-1, file, file+1
        for (int r = rank + 1; r <= 7; r++) {
            for (int f = std::max(0, file - 1); f <= std::min(7, file + 1); f++) {
                span |= sq_bb(r * 8 + f);
            }
        }
    } else {
        for (int r = rank - 1; r >= 0; r--) {
            for (int f = std::max(0, file - 1); f <= std::min(7, file + 1); f++) {
                span |= sq_bb(r * 8 + f);
            }
        }
    }

    return span;
}
```

### Example 5: King Safety

King safety evaluates how protected the king is, considering pawn shield, open files near the king, and attacking pieces.

```cpp
int eval_king_safety(const Position& pos) {
    Color us = pos.side_to_move;
    Color them = ~us;
    int score = 0;

    // Find our king
    Square king_sq = static_cast<Square>(
        std::countr_zero(pos.kings[us])
    );

    int king_file = king_sq % 8;
    int king_rank = king_sq / 8;

    // Pawn shield: pawns directly in front of the king
    Bitboard shield_zone = compute_king_shield_zone(king_sq, us);
    Bitboard our_pawns = pos.pawns[us];
    int shield_pawns = popcount(shield_zone & our_pawns);

    // Penalty for missing shield pawns (3 is ideal)
    score += EvalWeights::W_KING_SHIELD[shield_pawns];

    // Open files near the king
    for (int f = std::max(0, king_file - 1);
         f <= std::min(7, king_file + 1); f++) {
        Bitboard file_mask = BB_FILES[f];
        bool has_our_pawn = (our_pawns & file_mask) != 0;
        bool has_their_pawn = (pos.pawns[them] & file_mask) != 0;

        if (!has_our_pawn && !has_their_pawn) {
            // Fully open file near king — dangerous!
            score += EvalWeights::W_OPEN_FILE_NEAR_KING;
        } else if (!has_our_pawn) {
            // Semi-open file near king
            score += EvalWeights::W_SEMI_OPEN_FILE_NEAR_KING;
        }
    }

    // Enemy piece attacks near king
    Bitboard king_zone = compute_king_zone(king_sq);
    Bitboard enemy_attacks = pos.get_all_attacks(them);
    int attack_units = popcount(king_zone & enemy_attacks);

    score -= attack_units * EvalWeights::W_KING_ATTACK_PER_UNIT;

    return score;
}
```

---

## Why Bitboards Guarantee Speed

### The Loop Elimination Principle

Traditional (array-based) evaluation:
```cpp
// SLOW: Loop over all 64 squares
int count = 0;
for (int sq = 0; sq < 64; sq++) {
    if (board[sq] == KNIGHT && is_on_rim(sq)) {
        count++;
    }
}
```

Bitboard evaluation:
```cpp
// FAST: Single AND + popcount
int count = popcount(knights & BB_RIM);
```

### Operation Comparison

| Operation | Array-Based | Bitboard |
|---|---|---|
| Count pieces on rim | Loop + 64 comparisons | AND + POPCNT (2 instructions) |
| Find open files | Loop over files | AND per file (8 operations) |
| Check pawn shield | Loop over 3-5 squares | AND + POPCNT |
| Count attacks on zone | Nested loops | AND + POPCNT |

### Typical Performance

| Task | Array-Based | Bitboard | Speedup |
|---|---|---|---|
| Full evaluation (200 rules) | ~500μs | ~5μs | 100x |
| Knight on rim | ~2μs | ~0.02μs | 100x |
| Passed pawn detection | ~5μs | ~0.3μs | 17x |
| King safety | ~10μs | ~0.5μs | 20x |

At 5μs per full evaluation, we can evaluate **200,000 positions per second** — enough for competitive search.

---

## The Rule Registration System

### Declarative Rule Definition

```cpp
#include <functional>
#include <vector>
#include <string>

struct Rule {
    std::string name;
    std::function<int(const Position&)> evaluate;
    int weight_index;  // Index into the weight array
    bool is_phase_dependent;  // Has MG/EG split
};

class RuleEngine {
    std::vector<Rule> rules;

public:
    void register_rule(const std::string& name,
                        std::function<int(const Position&)> evaluator,
                        int weight_idx,
                        bool phase_dependent = false) {
        rules.push_back({name, evaluator, weight_idx, phase_dependent});
    }

    std::vector<Feature> extract_all(const Position& pos) const {
        std::vector<Feature> features;
        for (const auto& rule : rules) {
            Feature f;
            f.name = rule.name;
            f.score = rule.evaluate(pos);
            features.push_back(f);
        }
        return features;
    }
};

// Register all rules (done once at initialization)
RuleEngine create_rule_engine() {
    RuleEngine engine;
    engine.register_rule("Knight_On_Rim", eval_knight_on_rim, 0);
    engine.register_rule("Knight_Outpost", eval_knight_outpost, 1);
    engine.register_rule("Pawn_Outpost_Support", eval_pawn_outpost_support, 2);
    engine.register_rule("Rook_Open_File", eval_rook_open_file, 3);
    engine.register_rule("Rook_Semi_Open_File", eval_rook_semi_open_file, 4);
    engine.register_rule("Passed_Pawn", eval_passed_pawn, 5, true);
    engine.register_rule("King_Safety", eval_king_safety, 7, true);
    engine.register_rule("Mobility", eval_mobility, 9);
    // ... 200+ rules
    return engine;
}
```

This declarative system makes it easy to add, remove, or modify rules without changing the core evaluation loop—supporting the [[Feature Orthogonality Design]] methodology.

---

## Connections

- **Previous**: [[C++ Python Interfacing via Ctypes]] — How Python calls these functions
- **Next**: [[The Verbalization Pipeline]] — How rule data becomes explanations
- **Upstream**: [[Feature Orthogonality Design]] — Designing rules that don't overlap
- **Upstream**: [[Constrained Optimization]] — Weight constraints for these rules
- **Related**: [[The Heuristic Delta Pipeline]] — How feature extraction feeds the delta pipeline
