---
tags:
  - foundations
  - board-representation
  - bitboards
  - performance
chapter: "01"
---

# Board Representation

## Overview

Before a chess engine can search, evaluate, or explain anything, it must first **represent** the board in computer memory. The choice of board representation affects every subsequent subsystem: move generation speed, evaluation function complexity, search algorithm efficiency, and — critically for our project — the ability to perform fast declarative rule checking for explanations.

This note covers every major board representation method, with deep emphasis on **bitboards**, the representation used by virtually all modern high-performance engines.

---

## The 8×8 Array Representation

### Concept

The simplest board representation uses an 8×8 array where each element stores the piece occupying that square. Typically, integers encode piece types:

```cpp
// Piece encoding
enum Piece : int8_t {
    EMPTY  = 0,
    W_PAWN = 1, W_KNIGHT = 2, W_BISHOP = 3, W_ROOK = 4, W_QUEEN = 5, W_KING = 6,
    B_PAWN = 7, B_KNIGHT = 8, B_BISHOP = 9, B_ROOK = 10, B_QUEEN = 11, B_KING = 12
};

// Board state
Piece board[8][8];

// Example: starting position
board[0][0] = W_ROOK;   // a1
board[0][1] = W_KNIGHT; // b1
board[0][2] = W_BISHOP; // c1
board[0][3] = W_QUEEN;  // d1
board[0][4] = W_KING;   // e1
// ... etc.
board[6][0] = W_PAWN;   // a2
```

### Square Mapping

Squares are typically mapped as `(rank, file)` where rank 0 = rank 1 (White's first rank) and file 0 = a-file. Alternatively, a single index `0..63` can be used:

$$\text{index} = \text{rank} \times 8 + \text{file}$$

```
  a  b  c  d  e  f  g  h
8 56 57 58 59 60 61 62 63
7 48 49 50 51 52 53 54 55
6 40 41 42 43 44 45 46 47
5 32 33 34 35 36 37 38 39
4 24 25 26 27 28 29 30 31
3 16 17 18 19 20 21 22 23
2  8  9 10 11 12 13 14 15
1  0  1  2  3  4  5  6  7
```

### Pros and Cons

**Advantages:**
- Trivially simple to understand and implement
- O(1) piece-at-square lookup: `board[rank][file]`
- Easy to iterate over all squares
- Natural for human-readable output

**Disadvantages:**
- No spatial parallelism — checking "are there any White pawns on the kingside?" requires iterating over 32 squares
- Slow attack generation — computing knight moves requires looking up 8 individual squares
- No efficient set operations — cannot intersect piece sets with bitwise AND
- Each move requires two array writes (clear source, set destination)
- Checking patterns (e.g., "is the f7-square weak?") requires multiple individual lookups

The array representation is pedagogically valuable but **insufficient for competitive engines**.

---

## Bitboard Representation

### Core Concept

A **bitboard** is a 64-bit unsigned integer where each bit corresponds to one square on the chess board. If bit $i$ is set (1), the property associated with that bitboard holds on square $i$; if clear (0), it does not.

Since a standard chess board has exactly **64 squares**, and modern processors have native **64-bit integers**, this mapping is perfect:

$$\text{bitboard}[i] = \begin{cases} 1 & \text{if the property holds on square } i \\ 0 & \text{otherwise} \end{cases}$$

### Multiple Bitboards Per Position

A single bitboard can only represent one binary property. A chess position requires **multiple bitboards**:

```cpp
struct Position {
    // Piece bitboards (one per piece type per color)
    uint64_t pawns[2];      // [WHITE], [BLACK]
    uint64_t knights[2];
    uint64_t bishops[2];
    uint64_t rooks[2];
    uint64_t queens[2];
    uint64_t kings[2];

    // Aggregate bitboards
    uint64_t occupied[2];   // All pieces for each color
    uint64_t all_occupied;  // All pieces on the board

    // Game state
    int side_to_move;       // WHITE or BLACK
    int castling_rights;    // 4-bit flag: KQkq
    int en_passant_square;  // -1 or square index
    int halfmove_clock;     // For 50-move rule
    int fullmove_number;

    // Piece-on-square array (for reverse lookup)
    Piece board[64];
};
```

### The Power of Bitwise Operations

The true power of bitboards comes from **bitwise operations** that the CPU executes on all 64 bits simultaneously — achieving **data-level parallelism**.

#### 1. Aggregation (OR)

"All White pieces" = White pawns ∪ White knights ∪ ... ∪ White king:

```cpp
occupied[WHITE] = pawns[WHITE] | knights[WHITE] | bishops[WHITE]
               | rooks[WHITE]  | queens[WHITE]  | kings[WHITE];
```

#### 2. Intersection (AND)

"White pieces under attack by Black pawns":

```cpp
uint64_t attacked_whites = occupied[WHITE] & black_pawn_attacks;
```

#### 3. Complement (NOT)

"Empty squares":

```cpp
uint64_t empty = ~all_occupied;
```

#### 4. Shift (Pattern Generation)

Shifts generate attack patterns. A White pawn on square $i$ attacks squares $i+7$ and $i+9$ (with file-wrapping handled by masking):

```cpp
// White pawn attacks (shift left by 7 and 9)
uint64_t white_pawn_attacks(uint64_t pawns) {
    uint64_t attacks = 0;
    attacks |= (pawns << 7) & ~FILE_H;  // Attack up-left (exclude wrap)
    attacks |= (pawns << 9) & ~FILE_A;  // Attack up-right (exclude wrap)
    return attacks;
}
```

**Notice:** This generates attacks for **ALL white pawns simultaneously**. Whether there is 1 pawn or 8, the operation takes exactly one CPU instruction per shift. This is the fundamental advantage of bitboards.

#### 5. Population Count (POPCOUNT)

Count the number of set bits — i.e., the number of pieces of a type, or the number of attacked squares:

```cpp
int white_pawn_count = __builtin_popcountll(pawns[WHITE]); // GCC/Clang
int num_attacked_squares = std::popcount(attacks);          // C++20
```

#### 6. Bitscan (Find First Set Bit)

Find the index of the least significant set bit — i.e., the square of a piece:

```cpp
int square = __builtin_ctzll(knights[WHITE]); // Count trailing zeros
```

### Attack Generation with Bitboards

#### Knight Attacks

Knight moves are non-sliding and can be precomputed as a lookup table:

```cpp
uint64_t knight_attacks[64]; // Precomputed attack bitboard for each square

void init_knight_attacks() {
    for (int sq = 0; sq < 64; sq++) {
        uint64_t b = 1ULL << sq;
        knight_attacks[sq] = 0;
        knight_attacks[sq] |= (b << 17) & ~FILE_A;        // Up 2, right 1
        knight_attacks[sq] |= (b << 15) & ~FILE_H;        // Up 2, left 1
        knight_attacks[sq] |= (b << 10) & ~(FILE_A | FILE_B); // Up 1, right 2
        knight_attacks[sq] |= (b << 6)  & ~(FILE_G | FILE_H); // Up 1, left 2
        knight_attacks[sq] |= (b >> 17) & ~FILE_H;        // Down 2, left 1
        knight_attacks[sq] |= (b >> 15) & ~FILE_A;        // Down 2, right 1
        knight_attacks[sq] |= (b >> 10) & ~(FILE_G | FILE_H); // Down 1, left 2
        knight_attacks[sq] |= (b >> 6)  & ~(FILE_A | FILE_B); // Down 1, right 2
    }
}

// Usage: attacks for ALL knights of one color
uint64_t all_knight_attacks(uint64_t knights) {
    uint64_t attacks = 0;
    while (knights) {
        int sq = __builtin_ctzll(knights);
        attacks |= knight_attacks[sq];
        knights &= knights - 1; // Clear LSB (efficient iteration)
    }
    return attacks;
}
```

#### Sliding Piece Attacks (Magic Bitboards)

Sliding pieces (bishops, rooks, queens) are more complex because their attacks are **blocked** by other pieces. The state-of-the-art approach is **Magic Bitboards**:

1. For each square, identify the **relevant occupancy mask** (squares that can block the slider)
2. Use a **magic number** to index a precomputed attack table
3. The formula: `attack_index = ((occupancy & mask) * magic) >> shift`

```cpp
struct Magic {
    uint64_t mask;      // Relevant occupancy mask
    uint64_t magic;     // Magic multiplication constant
    int shift;          // Shift amount (64 - number of relevant bits)
    uint64_t* attacks;  // Pointer to attack table
};

Magic rook_magics[64];
Magic bishop_magics[64];

// Lookup rook attacks for a square given current occupancy
uint64_t get_rook_attacks(int square, uint64_t occupancy) {
    Magic& m = rook_magics[square];
    occupancy &= m.mask;
    occupancy *= m.magic;
    occupancy >>= m.shift;
    return m.attacks[occupancy];
}
```

The magic numbers are found through trial-and-error during initialization. This technique provides O(1) sliding piece attack lookup with minimal memory.

### Move Execution with Bitboards

Making a move on a bitboard representation involves:

```cpp
void make_move(Position& pos, Move move) {
    int from = move.from();
    int to   = move.to();
    Piece piece = pos.board[from];
    Color side = pos.side_to_move;

    // Clear the from-square in the piece bitboard
    pos.pieces(side, type_of(piece)) ^= (1ULL << from);
    // Set the to-square in the piece bitboard
    pos.pieces(side, type_of(piece)) ^= (1ULL << to);

    // Update the piece-on-square array
    pos.board[from] = EMPTY;
    pos.board[to] = piece;

    // Handle captures: clear captured piece from opponent's bitboard
    if (move.is_capture()) {
        Piece captured = pos.board[to]; // Read before overwriting
        Color opp = ~side;
        pos.pieces(opp, type_of(captured)) ^= (1ULL << to);
    }

    // Update aggregate bitboards
    pos.occupied[side] = pos.pawns[side] | pos.knights[side] | ...;
    pos.all_occupied = pos.occupied[WHITE] | pos.occupied[BLACK];

    // Switch side to move
    pos.side_to_move = ~pos.side_to_move;
}
```

The XOR operation (`^=`) is used because toggling a bit works for both setting and clearing: `bit ^= (1ULL << sq)` sets the bit if it was 0, clears it if it was 1.

---

## Mailbox Representation

### Concept

The **mailbox** representation uses a 10×12 (or 8×10) array with **sentinel values** around the edges. This makes off-board detection trivial: instead of checking if a square is within [0,63], you simply check if the array value is a sentinel.

```cpp
// 10x12 mailbox
// -1 = off-board sentinel
int mailbox[120] = {
    -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
    -1, 0, 1, 2, 3, 4, 5, 6, 7,-1,
    -1, 8, 9,10,11,12,13,14,15,-1,
    -1,16,17,18,19,20,21,22,23,-1,
    -1,24,25,26,27,28,29,30,31,-1,
    -1,32,33,34,35,36,37,38,39,-1,
    -1,40,41,42,43,44,45,46,47,-1,
    -1,48,49,50,51,52,53,54,55,-1,
    -1,56,57,58,59,60,61,62,63,-1,
    -1,-1,-1,-1,-1,-1,-1,-1,-1,-1
};

// Direction offsets for knight
int knight_dirs[8] = {-21, -19, -12, -8, 8, 12, 19, 21};
```

When generating knight moves, adding the direction offset to the current mailbox index and checking for -1 handles off-board detection in a single comparison. This was popular in early engines but has been superseded by bitboards.

### Why Mailbox Is Obsolete

- No parallel operations — each square must be checked individually
- No efficient set operations — cannot intersect piece sets
- Slower attack generation compared to magic bitboards
- The only advantage (simple off-board detection) is easily handled in bitboards with file masking

---

## Why Bitboards Are Preferred

The convergence of virtually all competitive engines on bitboards is not coincidental:

| Feature | Array | Mailbox | Bitboard |
|---------|-------|---------|----------|
| Piece-at-square lookup | O(1) | O(1) | O(1) (via board[] array) |
| All-pawns-of-color | O(64) | O(64) | O(1) (single read) |
| Attack generation (non-sliding) | Per-square | Per-square | All-at-once (parallel) |
| Attack generation (sliding) | Per-square | Per-square | O(1) via magic |
| Set operations (intersection) | O(64) loop | O(64) loop | O(1) bitwise AND |
| Population count | Loop | Loop | O(1) POPCOUNT |
| Cache efficiency | Moderate | Poor | Excellent (64-byte cache line = 8 bitboards) |

The bitboard advantage compounds: every subsystem — move generation, evaluation, search, and the explanation engine — benefits from the parallelism and speed.

---

## Connection to Explainability

Bitboards are not just a performance optimization — they are an **enabler for explainability**. Here's why:

### Fast Declarative Rule Checking

When the explanation engine asks "Does this move control the center?", it needs to check whether the moved piece attacks center squares (d4, d5, e4, e5). With bitboards:

```cpp
const uint64_t CENTER = (1ULL << D4) | (1ULL << D5) | (1ULL << E4) | (1ULL << E5);

bool controls_center(int square, uint64_t attacks) {
    return (attacks & CENTER) != 0;
}

// How MANY center squares does this piece control?
int center_control_count(uint64_t attacks) {
    return __builtin_popcountll(attacks & CENTER);
}
```

This is a **constant-time operation** — regardless of how many pieces are on the board, checking center control is a single bitwise AND plus a population count. This means the explanation engine can evaluate dozens of principles per move with negligible overhead.

### Pattern Matching for Strategic Concepts

Many chess principles are naturally expressed as spatial patterns:

- **Outpost**: A square on the 4th-6th rank, protected by a friendly pawn, not attackable by enemy pawns
- **Open file**: A file with no pawns of either color
- **Back rank weakness**: Enemy rook/queen can access the 1st/8th rank near the king

Each of these is a **bitboard intersection**:

```cpp
// Is square an outpost for a knight?
bool is_outpost(int sq, Color side, const Position& pos) {
    uint64_t sq_bb = 1ULL << sq;
    // Must be on ranks 4-6 (relative to side)
    if (!(sq_bb & outpost_ranks[side])) return false;
    // Must be protected by a friendly pawn
    if (!(pawn_attacks[~side][sq] & pos.pawns[side])) return false;
    // Must NOT be attackable by enemy pawns
    if (pawn_attacks[side][sq] & pos.pawns[~side]) return false;
    return true;
}
```

### Efficient "What-If" Analysis

When explaining a move, we often need to compare the position **before** and **after** the move. Bitboards make this comparison trivial:

```cpp
// Which squares changed attack coverage?
uint64_t new_attacks = get_attacks(after_move);
uint64_t old_attacks = get_attacks(before_move);
uint64_t gained_attacks = new_attacks & ~old_attacks;
uint64_t lost_attacks  = ~new_attacks & old_attacks;

int gained_center = __builtin_popcountll(gained_attacks & CENTER);
int lost_center   = __builtin_popcountll(lost_attacks & CENTER);
```

This "delta" approach is the foundation for explaining moves in terms of what improved and what was sacrificed.

---

## Key Takeaways

- **Bitboards** map the 64 squares of a chess board to the 64 bits of a native integer, enabling **parallel computation** across all squares simultaneously.
- Bitwise operations (AND, OR, XOR, shift, NOT) replace loops, providing massive speedups for attack generation, pattern matching, and set operations.
- **Magic bitboards** solve the sliding-piece problem with O(1) lookup using carefully chosen multiplication constants.
- The 8×8 array is simple but slow; the mailbox is obsolete; **bitboards are the standard** for all competitive engines.
- For explainability, bitboards enable **constant-time rule checking**, **pattern matching**, and **before/after delta analysis** — all essential for real-time move explanation.

## Cross-References

- [[01-Foundations/01 - Chess as a Zero-Sum Game|Chess as a Zero-Sum Game]] — the theoretical foundation
- [[01-Foundations/03 - Move Generation|Move Generation]] — how moves are generated from bitboard attack data
- [[01-Foundations/04 - The Explainability Problem|The Explainability Problem]] — why fast rule checking matters
- [[04-Transposition-Tables-and-Zobrist/01 - Zobrist Hashing|Zobrist Hashing]] — how bitboards enable incremental hash updates
