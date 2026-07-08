---
tags:
  - foundations
  - move-generation
  - legal-moves
  - special-moves
chapter: "01"
---

# Move Generation

## Overview

Move generation is the process of enumerating all legal moves available from a given position. It is the bridge between the [[01-Foundations/02 - Board Representation|board representation]] and the [[02-Search-Algorithms/01 - Minimax Algorithm|search algorithm]]. Every node in the search tree requires move generation, which means it is called **millions of times per second** in a competitive engine. Speed and correctness are both paramount — a single missed legal move can cause the engine to play an illegal move, and a single illegal move generated can crash the search.

This note covers the complete taxonomy of move generation: from pseudo-legal to legal, from pawn pushes to castling, and from representation to performance.

---

## Pseudo-Legal vs. Legal Move Generation

### Definitions

- **Pseudo-legal move**: A move that follows the movement rules of the piece, but may leave the king in check. For example, a bishop moving along a diagonal even if doing so would expose the king to a discovered check.
- **Legal move**: A pseudo-legal move that does NOT leave the king in check after it is made.

### The Two Approaches

**Approach 1: Generate Legal Directly**
Some engines try to generate only legal moves by incorporating king-safety checks into the generation logic. This is complex and often slower because every move must be checked during generation.

**Approach 2: Generate Pseudo-Legal, Then Filter**
Most modern engines generate pseudo-legal moves and then filter out the illegal ones:

```cpp
std::vector<Move> generate_legal_moves(const Position& pos) {
    std::vector<Move> moves = generate_pseudo_legal_moves(pos);
    moves.erase(std::remove_if(moves.begin(), moves.end(),
        [&](const Move& m) { return !is_legal(pos, m); }),
        moves.end());
    return moves;
}

bool is_legal(const Position& pos, Move move) {
    Position copy = pos;
    copy.make_move(move);
    // After making the move, is OUR king in check?
    // (Note: side_to_move has been switched, so we check the opponent's attack on our king)
    return !copy.is_in_check(~copy.side_to_move);
}
```

The advantage of Approach 2 is that the pseudo-legal generator is simpler and faster. The legality check is deferred, and in many cases (e.g., during [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta search]]), we don't even need to generate all legal moves — we just check legality of each move as we try it.

### The In-Check Optimization

When the king is in check, the number of legal moves is dramatically reduced (typically 1-5 instead of 30-40). Most engines detect check at the start of move generation and, if in check, use a specialized **evasion generator** that only produces moves that escape check:

1. **Capture the checking piece** (if only one attacker)
2. **Block the check** (interpose a piece on the checking line, if the checker is a sliding piece)
3. **Move the king** to a square not attacked by the opponent

This dramatically reduces the search tree in check positions.

---

## Move Generation by Piece Type

### Pawn Moves

Pawns are the most complex piece for move generation due to their asymmetric movement, special rules, and promotion.

**White Pawn Moves:**
- **Single push**: From rank $r$ to $r+1$ (if the target square is empty)
- **Double push**: From rank 2 to rank 4 (if both the intermediate and target squares are empty)
- **Capture left**: Diagonal from file $f$ to file $f-1$, rank $r+1$ (if enemy piece present)
- **Capture right**: Diagonal from file $f$ to file $f+1$, rank $r+1$ (if enemy piece present)
- **En passant capture**: Special capture of an adjacent enemy pawn that just double-pushed
- **Promotion**: When reaching rank 8, the pawn must promote to Q/R/B/N

**Bitboard implementation:**

```cpp
uint64_t white_single_pushes(uint64_t pawns, uint64_t empty) {
    return (pawns << 8) & empty;
}

uint64_t white_double_pushes(uint64_t pawns, uint64_t empty) {
    uint64_t rank2 = pawns & RANK_2;
    uint64_t single = (rank2 << 8) & empty;
    return (single << 8) & empty;
}

uint64_t white_pawn_captures(uint64_t pawns, uint64_t enemies) {
    uint64_t left  = (pawns << 7) & ~FILE_H & enemies;
    uint64_t right = (pawns << 9) & ~FILE_A & enemies;
    return left | right;
}
```

The elegance of bitboard pawn generation is that all pawn moves for the entire board are computed in **3-4 bitwise operations**, regardless of how many pawns exist.

### Knight Moves

Knights have a fixed set of up to 8 target squares from any position. As described in [[01-Foundations/02 - Board Representation|Board Representation]], these are precomputed in a lookup table:

```cpp
uint64_t knight_moves[64]; // Precomputed during initialization

void generate_knight_moves(const Position& pos, std::vector<Move>& moves) {
    uint64_t knights = pos.knights[pos.side_to_move];
    while (knights) {
        int from = __builtin_ctzll(knights);
        uint64_t targets = knight_moves[from] & ~pos.occupied[pos.side_to_move]; // Can't capture own pieces
        while (targets) {
            int to = __builtin_ctzll(targets);
            moves.push_back(Move(from, to));
            targets &= targets - 1;
        }
        knights &= knights - 1;
    }
}
```

### Bishop Moves

Bishops slide diagonally until blocked. Using magic bitboards:

```cpp
void generate_bishop_moves(const Position& pos, std::vector<Move>& moves) {
    uint64_t bishops = pos.bishops[pos.side_to_move];
    while (bishops) {
        int from = __builtin_ctzll(bishops);
        uint64_t targets = get_bishop_attacks(from, pos.all_occupied)
                         & ~pos.occupied[pos.side_to_move];
        while (targets) {
            int to = __builtin_ctzll(targets);
            moves.push_back(Move(from, to));
            targets &= targets - 1;
        }
        bishops &= bishops - 1;
    }
}
```

### Rook Moves

Identical pattern to bishops, using rook magic bitboards:

```cpp
uint64_t targets = get_rook_attacks(from, pos.all_occupied)
                 & ~pos.occupied[pos.side_to_move];
```

### Queen Moves

The queen combines bishop and rook movement:

```cpp
uint64_t targets = (get_bishop_attacks(from, pos.all_occupied)
                  | get_rook_attacks(from, pos.all_occupied))
                 & ~pos.occupied[pos.side_to_move];
```

### King Moves

The king has up to 8 adjacent target squares, precomputed like knight moves. However, the king has additional constraints:

1. Cannot move to a square attacked by the opponent
2. Can castle (see Special Moves below)

```cpp
void generate_king_moves(const Position& pos, std::vector<Move>& moves) {
    int from = __builtin_ctzll(pos.kings[pos.side_to_move]);
    uint64_t targets = king_moves[from]
                     & ~pos.occupied[pos.side_to_move]
                     & ~pos.attacked_by[~pos.side_to_move]; // Critical: exclude attacked squares
    while (targets) {
        int to = __builtin_ctzll(targets);
        moves.push_back(Move(from, to));
        targets &= targets - 1;
    }
}
```

---

## Special Moves

### Castling

Castling is the most complex move generation rule. The king moves two squares toward the rook, and the rook jumps to the other side of the king.

**Conditions (all must be true):**
1. The king has not moved from its starting square
2. The relevant rook has not moved from its starting square
3. No pieces between the king and the rook
4. The king is not in check
5. The king does not pass through a square attacked by the opponent
6. The king does not land on a square attacked by the opponent

```cpp
void generate_castling(const Position& pos, std::vector<Move>& moves) {
    if (pos.side_to_move == WHITE) {
        // White Kingside: e1 -> g1, rook h1 -> f1
        if ((pos.castling_rights & WK) &&
            !(pos.all_occupied & (SQ_F1 | SQ_G1)) &&
            !pos.is_attacked(SQ_E1, BLACK) &&
            !pos.is_attacked(SQ_F1, BLACK) &&
            !pos.is_attacked(SQ_G1, BLACK)) {
            moves.push_back(Move(SQ_E1, SQ_G1, CASTLE_FLAG));
        }
        // White Queenside: e1 -> c1, rook a1 -> d1
        if ((pos.castling_rights & WQ) &&
            !(pos.all_occupied & (SQ_B1 | SQ_C1 | SQ_D1)) &&
            !pos.is_attacked(SQ_E1, BLACK) &&
            !pos.is_attacked(SQ_D1, BLACK) &&
            !pos.is_attacked(SQ_C1, BLACK)) {
            moves.push_back(Move(SQ_E1, SQ_C1, CASTLE_FLAG));
        }
    }
    // Similar for BLACK with ranks shifted...
}
```

**Note for Queenside castling**: Even though the rook passes through b1, the king does NOT pass through b1, so b1 does not need to be unattacked — only unoccupied.

### En Passant

En passant allows a pawn to capture an enemy pawn that has just advanced two squares, as if it had only advanced one:

```cpp
void generate_en_passant(const Position& pos, std::vector<Move>& moves) {
    if (pos.en_passant_square == -1) return;

    uint64_t ep_bb = 1ULL << pos.en_passant_square;
    uint64_t pawns = pos.pawns[pos.side_to_move];

    if (pos.side_to_move == WHITE) {
        uint64_t attackers = ((ep_bb >> 7) & ~FILE_A | (ep_bb >> 9) & ~FILE_H) & pawns;
        while (attackers) {
            int from = __builtin_ctzll(attackers);
            moves.push_back(Move(from, pos.en_passant_square, EP_FLAG));
            attackers &= attackers - 1;
        }
    }
    // Similar for BLACK...
}
```

**Pitfall**: En passant can expose the king to a discovered check along the 4th/5th rank. For example, if both the capturing pawn and the captured pawn are on the same rank as the king, removing both pawns may open a rook attack. The legality filter catches this.

### Promotion

When a pawn reaches the last rank, it MUST promote to a queen, rook, bishop, or knight. This means each promotion square generates **4 moves** (one per promotion piece):

```cpp
void generate_promotions(uint64_t push_targets, uint64_t capture_targets,
                         std::vector<Move>& moves) {
    uint64_t promotions = push_targets & RANK_8;
    while (promotions) {
        int to = __builtin_ctzll(promotions);
        int from = to - 8; // For White pawns
        moves.push_back(Move(from, to, PROMO_QUEEN));
        moves.push_back(Move(from, to, PROMO_ROOK));
        moves.push_back(Move(from, to, PROMO_BISHOP));
        moves.push_back(Move(from, to, PROMO_KNIGHT));
        promotions &= promotions - 1;
    }
    // Same for capture promotions...
}
```

**Underpromotion** (promoting to anything other than queen) is important: a knight promotion can give check or fork, while a queen promotion might stalemate. The engine must consider all four options.

---

## Move Representation

### Compact Move Encoding

A move must encode: from-square (6 bits), to-square (6 bits), and flags for special moves. A common 16-bit encoding:

```
Bits 0-5:   From square (0-63)
Bits 6-11:  To square (0-63)
Bits 12-15: Flags (4 bits)
```

```cpp
enum MoveFlags : uint16_t {
    NONE        = 0,
    CASTLE      = 1,
    EN_PASSANT  = 2,
    PROMO_KNIGHT = 3,
    PROMO_BISHOP = 4,
    PROMO_ROOK   = 5,
    PROMO_QUEEN  = 6,
};

class Move {
    uint16_t data;
public:
    Move(int from, int to, MoveFlags flags = NONE)
        : data(from | (to << 6) | (flags << 12)) {}

    int from()  const { return data & 0x3F; }
    int to()    const { return (data >> 6) & 0x3F; }
    int flags() const { return (data >> 12) & 0xF; }

    bool is_capture() const; // Determined by checking the position, not the move itself
    bool is_castle()  const { return flags() == CASTLE; }
    bool is_ep()      const { return flags() == EN_PASSANT; }
    bool is_promo()   const { return flags() >= PROMO_KNIGHT; }
};
```

Some engines also include the captured piece or the moved piece in the move encoding to avoid re-reading the board during unmake. The tradeoff is larger move objects vs. faster unmake.

### Move Lists

Rather than using `std::vector<Move>` (which heap-allocates), high-performance engines use a stack-based move list:

```cpp
struct MoveList {
    Move moves[256]; // Maximum possible legal moves in any position is 218
    int count = 0;

    void add(Move m) { moves[count++] = m; }
    Move begin() { return moves[0]; }
    Move end() { return moves[count]; }
};
```

This avoids memory allocation entirely and keeps the move data in cache-friendly contiguous memory.

---

## Performance Considerations

### Why Move Generation Must Be Fast

In a typical search, the engine might evaluate **10-50 million positions per second**. Each position requires:
1. Move generation
2. Move ordering (see [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]])
3. Making/unmaking each move
4. Evaluating the resulting position

If move generation takes 1 microsecond per call and is called 10 million times, that's 10 seconds — a significant fraction of the time budget. Every nanosecond counts.

### Optimization Techniques

1. **Precomputed attack tables** (knight, king, pawn) — compute once at startup
2. **Magic bitboards** for sliding pieces — O(1) attack lookup
3. **Bulk piece iteration** using bitscan and bit traversal
4. **Avoid branches** in inner loops — use bitwise operations instead of if-statements
5. **Separate capture generation** for [[03-Search-Accelerators/05 - Quiescence Search|quiescence search]] — only generate captures, not quiet moves
6. **Lazy legality checking** — only verify legality when a move is actually played, not when generating

### Staged Move Generation

Rather than generating ALL moves and then sorting them, many engines use **staged generation** that produces moves in approximate order:

1. **TT Move** — return the best move from the transposition table
2. **Captures** — generate and sort by [[03-Search-Accelerators/02 - Move Ordering|MVV-LVA]]
3. **Killers** — return killer moves if they're pseudo-legal
4. **Quiets** — generate remaining quiet moves sorted by history heuristic

This integrates move generation with [[03-Search-Accelerators/02 - Move Ordering|move ordering]] for maximum efficiency.

---

## Connection to the Explainable Engine

Move generation is the **first step** before any rule-based evaluation can occur. The explainable engine's workflow is:

1. **Generate legal moves** — enumerate the candidate moves
2. **Search** — use [[02-Search-Algorithms/03 - Alpha-Beta Pruning|alpha-beta]] with pruning to find the best move
3. **Explain** — for the chosen move, evaluate which [[01-Foundations/04 - The Explainability Problem|principles and rules]] support it

The move generator feeds the search, and the search produces the candidate moves that the explanation system must analyze. If move generation is buggy, the entire system fails — the engine might miss the best move entirely, and the explanation would be for a suboptimal choice.

Furthermore, the **staged generation** approach maps naturally to explainability: the order in which moves are generated reflects the engine's "intuition" about which rules matter most. The TT move represents "prior knowledge," captures represent "tactical urgency," and quiet moves represent "strategic possibilities."

---

## Key Takeaways

- **Pseudo-legal generation + legality filtering** is the standard approach: generate moves that follow piece rules, then remove those that leave the king in check.
- **Bitboards** enable parallel move generation for all pieces of a type simultaneously.
- **Special moves** (castling, en passant, promotion) add significant complexity and are the source of many bugs.
- **Move representation** uses compact 16-bit or 32-bit encodings with flag bits for special moves.
- **Performance** is critical — move generation is called millions of times per second and must be as fast as possible.
- **Staged generation** integrates with move ordering for both performance and explainability.
- Move generation is the **input pipeline** for the explanation system — it determines which moves are even considered for explanation.

## Cross-References

- [[01-Foundations/02 - Board Representation|Board Representation]] — bitboards and attack tables that drive move generation
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — why the moves we generate matter for explanation
- [[02-Search-Algorithms/01 - Minimax Algorithm|Minimax Algorithm]] — the search that consumes generated moves
- [[03-Search-Accelerators/02 - Move Ordering|Move Ordering]] — how generated moves are prioritized
- [[03-Search-Accelerators/05 - Quiescence Search|Quiescence Search]] — capture-only move generation for tactical stability
