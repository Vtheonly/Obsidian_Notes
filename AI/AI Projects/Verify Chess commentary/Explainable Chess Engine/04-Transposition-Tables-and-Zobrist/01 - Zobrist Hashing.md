---
tags:
  - hashing
  - zobrist
  - incremental-update
  - bitboards
  - collision
chapter: "04"
---

# Zobrist Hashing

## Overview

**Zobrist Hashing** (also called Zobrist keys or Zobrist hashing) is a technique for representing the entire state of a chess position as a single 64-bit integer. It was invented by Albert Zobrist in 1970 and has become the standard hashing method for chess engines. Zobrist hashing enables **incremental updates** — when a move is made, the hash key can be updated with a few XOR operations rather than recomputing the entire hash from scratch. This is essential for [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|transposition table]] lookups, which occur at every node in the search tree.

---

## The Concept

### From Position to Key

A chess position is defined by:
- Which piece is on which square (up to 32 pieces on 64 squares)
- Which side is to move (White or Black)
- Castling rights (K, Q, k, q — 16 possible combinations)
- En passant target square (0-8 possible squares or none)

Zobrist hashing maps this complex state to a single 64-bit key $K \in [0, 2^{64})$. The key should satisfy:
1. **Deterministic**: The same position always produces the same key
2. **Uniform**: Keys are uniformly distributed across the 64-bit space
3. **Incrementally updatable**: Making a move changes the key in O(1) time
4. **Collision-resistant**: Different positions are extremely unlikely to produce the same key

### Random Number Tables

The foundation of Zobrist hashing is a table of **pre-generated random 64-bit numbers**:

```cpp
// 12 piece types (6 per color) × 64 squares
uint64_t piece_keys[12][64];

// 64 possible en passant squares (only ranks 3 and 6 are used, but we index by square)
uint64_t enpassant_keys[64];

// 16 possible castling right combinations (4 bits → 16 values)
uint64_t castle_keys[16];

// Side-to-move key (XOR'd when it's Black's turn)
uint64_t side_key;
```

The total number of random numbers is: $12 \times 64 + 64 + 16 + 1 = 849$.

---

## Initialization

### Generating the Random Numbers

The random numbers must be generated with a **high-quality PRNG** (pseudo-random number generator). A 64-bit Mersenne Twister or Xorshift generator is typically used:

```cpp
#include <random>

void init_zobrist_keys() {
    std::mt19937_64 rng(0x12345678); // Fixed seed for reproducibility

    // Piece-square keys
    for (int piece = 0; piece < 12; piece++) {
        for (int square = 0; square < 64; square++) {
            piece_keys[piece][square] = rng();
        }
    }

    // En passant keys
    for (int square = 0; square < 64; square++) {
        enpassant_keys[square] = rng();
    }

    // Castling keys
    for (int index = 0; index < 16; index++) {
        castle_keys[index] = rng();
    }

    // Side-to-move key
    side_key = rng();
}
```

**Important**: The seed must be **fixed** so that the same position always produces the same hash key across different runs of the engine. This is essential for [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|transposition table]] consistency.

### Piece Encoding

The piece index maps to the `piece_keys` array:

```cpp
enum PieceIndex {
    W_PAWN = 0,  W_KNIGHT = 1,  W_BISHOP = 2,  W_ROOK = 3,  W_QUEEN = 4,  W_KING = 5,
    B_PAWN = 6,  B_KNIGHT = 7,  B_BISHOP = 8,  B_ROOK = 9,  B_QUEEN = 10, B_KING = 11
};
```

---

## Computing the Hash Key

### Full Computation (From Scratch)

To compute the hash key for a position from scratch, XOR together all the random numbers that correspond to the current state:

```cpp
uint64_t compute_hash(const Position& pos) {
    uint64_t key = 0;

    // XOR in each piece on each square
    for (int square = 0; square < 64; square++) {
        Piece piece = pos.board[square];
        if (piece != EMPTY) {
            key ^= piece_keys[piece_index(piece)][square];
        }
    }

    // XOR in side to move
    if (pos.side_to_move == BLACK) {
        key ^= side_key;
    }

    // XOR in castling rights
    key ^= castle_keys[pos.castling_rights];

    // XOR in en passant square
    if (pos.en_passant_square >= 0) {
        key ^= enpassant_keys[pos.en_passant_square];
    }

    return key;
}
```

### Why XOR?

XOR (⊕) has three critical properties that make Zobrist hashing work:

#### 1. Identity: $A \oplus 0 = A$

XORing with zero leaves the value unchanged. This means we can simply skip squares with no piece.

#### 2. Self-Inverse: $A \oplus A = 0$

XORing a value with itself cancels out. This is the key to incremental updates: to **remove** a piece from the hash, we XOR in the same random number again.

#### 3. Commutativity: $A \oplus B = B \oplus A$

The order of XOR operations doesn't matter. We can add pieces to the hash in any order and get the same result.

These properties together mean:
- **Adding a piece**: `key ^= piece_keys[piece][square]`
- **Removing a piece**: `key ^= piece_keys[piece][square]` (same operation!)
- **Moving a piece**: Remove from old square, add to new square:
  `key ^= piece_keys[piece][from] ^ piece_keys[piece][to]`

---

## Incremental Update

### The Key Advantage

The full hash computation requires iterating over all 64 squares, which is O(64) — fast but not fast enough when called millions of times per second. The **incremental update** takes advantage of the XOR properties to update the hash in O(1) when a move is made.

### Update Formula

When a piece moves from square `from` to square `to`:

$$K_{\text{new}} = K_{\text{old}} \oplus \text{piece\_keys}[P][\text{from}] \oplus \text{piece\_keys}[P][\text{to}]$$

This simultaneously removes the piece from `from` (XOR cancels the old value) and adds it to `to`.

### Implementation for Regular Moves

```cpp
void Position::make_move(Move move) {
    // Save current hash key for unmake
    history[ply].hash_key = hash_key;

    int from = move.from();
    int to = move.to();
    Piece piece = board[from];
    PieceIndex pi = piece_index(piece);

    // Remove piece from source square, add to destination
    hash_key ^= piece_keys[pi][from] ^ piece_keys[pi][to];

    // Handle captures
    if (move.is_capture()) {
        Piece captured = board[to];
        PieceIndex ci = piece_index(captured);
        hash_key ^= piece_keys[ci][to]; // Remove captured piece
    }

    // Handle en passant: clear old EP square, set new if double pawn push
    if (en_passant_square >= 0) {
        hash_key ^= enpassant_keys[en_passant_square]; // Remove old EP
    }
    en_passant_square = -1; // Default: no EP
    if (type_of(piece) == PAWN && abs(to - from) == 16) {
        en_passant_square = (from + to) / 2;
        hash_key ^= enpassant_keys[en_passant_square]; // Add new EP
    }

    // Handle castling rights: XOR out old rights, XOR in new rights
    hash_key ^= castle_keys[castling_rights]; // Remove old
    castling_rights &= castling_rights_mask[from];
    castling_rights &= castling_rights_mask[to];
    hash_key ^= castle_keys[castling_rights]; // Add new

    // Switch side to move
    hash_key ^= side_key;

    // Update board, bitboards, etc.
    // ...

    ply++;
}

void Position::unmake_move(Move move) {
    ply--;

    // Simply restore the saved hash key
    hash_key = history[ply].hash_key;

    // Restore other state from history...
}
```

### The Castling Rights Mask

When a rook or king moves, or a rook is captured, the castling rights must be updated. The mask approach uses a precomputed table:

```cpp
// For each square, which castling rights are preserved
// (rights that are NOT removed when this square is involved)
const int castling_rights_mask[64] = {
    // a1: remove White Queenside
    13, 15, 15, 15, 12, 15, 15, 14,  // Rank 1 (12 = remove KQ, 13 = remove Q, 14 = remove K)
    15, 15, 15, 15, 15, 15, 15, 15,  // Rank 2
    // ... all 15s for ranks 2-7 ...
    7, 15, 15, 15, 3, 15, 15, 11,    // Rank 8 (3 = remove kq, 7 = remove q, 11 = remove k)
};

// castling_rights is a 4-bit value: K=1, Q=2, k=4, q=8
// When a piece moves from square X: castling_rights &= castling_rights_mask[X]
// This clears the relevant bits
```

### Special Move Hash Updates

**En passant capture**:

```cpp
// Remove the captured pawn (which is on a different square than 'to')
int ep_captured_square = (from < to) ? to - 8 : to + 8; // The pawn is on the same rank as 'from'
hash_key ^= piece_keys[piece_index(captured_pawn)][ep_captured_square];
```

**Castling**:

```cpp
// Move the king (already handled above)
// Also move the rook
if (move.is_castle()) {
    int rook_from, rook_to;
    if (to > from) { // Kingside
        rook_from = from + 3; // h1 or h8
        rook_to = from + 1;   // f1 or f8
    } else { // Queenside
        rook_from = from - 4; // a1 or a8
        rook_to = from - 1;   // d1 or d8
    }
    hash_key ^= piece_keys[ROOK_INDEX][rook_from] ^ piece_keys[ROOK_INDEX][rook_to];
}
```

**Promotion**:

```cpp
// Remove the pawn, add the promoted piece
hash_key ^= piece_keys[PAWN_INDEX][from];     // Remove pawn from 'from'
hash_key ^= piece_keys[promo_index][to];      // Add promoted piece to 'to'
// Note: we already XOR'd piece_keys[PAWN_INDEX][from] ^ piece_keys[PAWN_INDEX][to]
// above, but for promotion, the piece type changes, so we need to undo the pawn's
// contribution to 'to' and add the new piece instead.
hash_key ^= piece_keys[PAWN_INDEX][to];       // Undo pawn's 'to' contribution
hash_key ^= piece_keys[promo_index][to];      // Add promoted piece's 'to' contribution
```

---

## Why FEN Comparison Is Too Slow

### The Naive Approach

A FEN (Forsyth-Edwards Notation) string uniquely identifies a chess position. Comparing two positions could be done by comparing their FEN strings:

```python
if position1.fen() == position2.fen():
    # Same position!
```

**Why this is too slow**:
1. **FEN generation** requires iterating over all 64 squares: O(64)
2. **String comparison** requires comparing character by character: O(64+) for typical FEN strings
3. **Memory overhead**: FEN strings are ~60-80 bytes, while a Zobrist key is 8 bytes
4. **No incremental update**: FEN must be regenerated from scratch every time; there's no way to incrementally update a FEN string

In a search that evaluates millions of positions per second, FEN comparison would be a **catastrophic bottleneck**. Zobrist hashing replaces O(64) comparison with O(1) comparison (a single 64-bit integer comparison).

### Zobrist vs. FEN

| Operation | Zobrist | FEN |
|-----------|---------|-----|
| Initialize | O(64) | O(64) |
| Update (move) | O(1) | O(64) |
| Compare | O(1) | O(64+) |
| Memory per position | 8 bytes | ~70 bytes |
| Incremental |  Yes |  No |

---

## Hash Collision Handling

### The Collision Problem

Two different positions producing the same 64-bit hash key is called a **hash collision**. With 64-bit keys, the probability of a collision depends on the number of positions hashed, following the **birthday paradox**:

$$P(\text{collision among } n \text{ positions}) \approx 1 - e^{-n^2 / (2 \times 2^{64})}$$

For typical search sizes:

| Positions Hashed | Collision Probability |
|-----------------|----------------------|
| 10,000 | ~$2.7 \times 10^{-12}$ (essentially zero) |
| 1,000,000 | ~$2.7 \times 10^{-8}$ |
| 100,000,000 | ~$2.7 \times 10^{-4}$ (0.027%) |
| 10,000,000,000 | ~$2.7 \times 0^{-0}$ — actually $1 - e^{-10^{20}/(2 \times 1.8 \times 10^{19})} \approx 94\%$ |

Wait, let me recalculate. $n = 10^{10}$:

$$P \approx 1 - e^{-(10^{10})^2 / (2 \times 2^{64})} = 1 - e^{-10^{20} / (3.7 \times 10^{19})} = 1 - e^{-2.7} \approx 93\%$$

So with 10 billion positions (an extreme search), collisions become very likely. However:

1. **In practice**, the number of unique positions in a single search is much smaller than the total nodes (many nodes share the same position due to transpositions).
2. **The damage of a collision is limited**: the worst case is that the engine uses a wrong TT entry, which might cause it to miss the best move but won't crash or play an illegal move.
3. **Verification**: Some engines store part of the board state alongside the hash key and verify consistency before using a TT entry.

### Collision Mitigation Strategies

1. **Key verification**: Store additional bits of the hash key (or a separate verification hash) in the TT entry:

```cpp
struct TTEntry {
    uint64_t key;    // Full 64-bit Zobrist key
    int32_t score;
    int16_t depth;
    uint8_t flag;
    Move best_move;
};

bool is_valid_entry(const TTEntry& entry, uint64_t current_key) {
    return entry.key == current_key; // Full key comparison
}
```

2. **Dual hashing**: Use two independent Zobrist hashes (128 bits total) for extremely low collision probability:

```cpp
struct DualHash {
    uint64_t key1; // Primary Zobrist hash
    uint64_t key2; // Secondary Zobrist hash (different random table)
};
```

3. **Accept the risk**: Most engines simply accept the ~$10^{-8}$ collision probability per search, as the cost (an occasional wrong move) is negligible compared to the complexity of mitigation.

---

## Zobrist Hashing and Bitboards

### Natural Synergy

Zobrist hashing is a natural fit for [[01-Foundations/02 - Board Representation|bitboard]] representations. The piece_keys table maps directly to the piece-type indexing used by bitboards:

```cpp
uint64_t compute_hash_from_bitboards(const Position& pos) {
    uint64_t key = 0;

    // For each piece type and color
    for (int pt = PAWN; pt <= KING; pt++) {
        for (int color = WHITE; color <= BLACK; color++) {
            uint64_t pieces = pos.pieces[color][pt];
            while (pieces) {
                int square = __builtin_ctzll(pieces);
                key ^= piece_keys[piece_index(color, pt)][square];
                pieces &= pieces - 1;
            }
        }
    }

    if (pos.side_to_move == BLACK) key ^= side_key;
    key ^= castle_keys[pos.castling_rights];
    if (pos.en_passant_square >= 0) key ^= enpassant_keys[pos.en_passant_square];

    return key;
}
```

The bitscan-and-iterate pattern used to compute the hash from bitboards is the same pattern used throughout the engine for [[01-Foundations/03 - Move Generation|move generation]] and evaluation.

---

## Key Takeaways

- **Zobrist hashing** represents an entire chess position as a single 64-bit key, using a table of pre-generated random numbers.
- The key is computed by XORing together the random numbers for each piece-square combination, side to move, castling rights, and en passant square.
- **Incremental updates** are O(1) — making a move requires 3-5 XOR operations, not a full recomputation.
- The XOR properties (identity, self-inverse, commutativity) are the mathematical foundation that makes incremental updates possible.
- **FEN comparison** is O(64+) per comparison and cannot be incrementally updated — it is far too slow for use in search.
- **Hash collisions** are possible but extremely rare in practice (~$10^{-8}$ per million positions).
- Zobrist hashing is the foundation for [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|transposition tables]], which use the hash key to index and verify stored positions.

## Cross-References

- [[01-Foundations/02 - Board Representation|Board Representation]] — bitboard representation that Zobrist hashing operates on
- [[04-Transposition-Tables-and-Zobrist/02 - Transposition Table Architecture|Transposition Table Architecture]] — the primary consumer of Zobrist hash keys
- [[01-Foundations/03 - Move Generation|Move Generation]] — the make/unmake operations that update the hash key
- [[03-Search-Accelerators/01 - Iterative Deepening|Iterative Deepening]] — the search strategy that benefits from TT lookups via Zobrist keys
