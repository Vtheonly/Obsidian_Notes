# The Puzzle Database System

> **Chapter 13.04** | [[03 - Python PyTorch Optimization Engine|Prev: PyTorch Optimization]] | [[01 - The Slav Defense Philosophy|Next: Slav Defense]]
> **Related**: [[04 - Puzzle Training Integration|Puzzle Training]], [[05 - Android Puzzle App Architecture|Android App]], [[02 - Defense and Swindling|Defense & Swindling]]

---

## Overview

Puzzle databases are the testing ground for the [[Explainable Chess Engine]]. Each puzzle presents a position where a specific tactical theme is active, and the engine must not only find the correct move but also **explain why** it's correct using its rule-based system. The Lichess puzzle database, with over 2 million curated puzzles, provides an enormous corpus for both training and evaluation.

This note covers the Lichess puzzle database format, the subtle but critical details of how FEN and moves are encoded, and the complete system for importing, storing, and querying puzzles.

---

## The Lichess Puzzle Database Format

### CSV Schema

The Lichess puzzle database is distributed as a CSV file with the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `PuzzleId` | string | Unique identifier | `"00H1s"` |
| `FEN` | string | Board position **before the opponent's move** | `"rnbqkbnr/pppp1ppp/4p3/8/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"` |
| `Moves` | string | Sequence of UCI moves | `"e2e5 d2d5 e5d5"` |
| `Rating` | int | Puzzle difficulty (ELO-based) | `1750` |
| `RatingDeviation` | int | Uncertainty in rating | `78` |
| `Popularity` | int | Community approval (-100 to 100) | `92` |
| `NbPlays` | int | Number of times played | `4521` |
| `Themes` | string | Comma-separated tactical themes | `"fork middlegame short"` |
| `GameUrl` | string | Link to source game | `"https://lichess.org/xxxxxx#y"` |
| `OpeningTags` | string | Associated opening names | `"Sicilian_Defense"` |

### The Critical FEN Detail

The most important and commonly misunderstood aspect of the puzzle format is:

> **The FEN represents the position BEFORE the opponent makes their move. The first move in the Moves sequence is the opponent's move, which is applied automatically. The SECOND move is the start of the solution.**

Let's break this down with a concrete example:

```
FEN:   r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 4 4
Moves: f7f5 Qxf7# (in UCI: f7f5 h5f7)
```

**Step-by-step:**
1. The FEN shows the position with **Black to move**
2. The first move `f7f5` is Black's move (the opponent's move, applied automatically)
3. After `f7f5`, it's White's turn — this is where the puzzle begins
4. The second move `h5f7` is White's correct response: **Qxf7#** — checkmate!

This is critical for the [[Explainable Chess Engine]] because:
- The engine must evaluate the position **after** the opponent's move
- The explanation system must describe why the opponent's move created a weakness
- The solution move's explanation must reference the tactical theme

### UCI Move Format

Moves in the puzzle database use UCI (Universal Chess Interface) format:

| Move Type | SAN | UCI | Description |
|-----------|-----|-----|-------------|
| Normal | `e4` | `e2e4` | From-square to-square |
| Capture | `Qxf7` | `h5f7` | Queen from h5 takes f7 |
| Castling | `O-O` | `e1g1` | King from e1 to g1 |
| Promotion | `e8=Q` | `e7e8q` | Pawn promotes, lowercase piece letter |
| En passant | `exd6` | `e5d6` | Pawn captures en passant |

Note the promotion format: the piece letter is always **lowercase** in UCI: `q` for queen, `r` for rook, `b` for bishop, `n` for knight.

---

## Tactical Themes

The `Themes` field contains one or more tags from a controlled vocabulary. These are essential for the [[Explainable Chess Engine]] because they define what the engine's explanation should capture:

### Core Tactical Themes

| Theme | Description | Engine Explanation Pattern |
|-------|-------------|---------------------------|
| `fork` | One piece attacks two or more targets | "The knight on d5 forks the king on e7 and the rook on c7" |
| `pin` | A piece cannot move without exposing a more valuable piece | "The bishop on g5 pins the knight on f6 against the queen on d8" |
| `skewer` | A valuable piece is attacked and must move, exposing a less valuable piece | "The rook on d1 skewers the king on d8 and the queen on d5" |
| `discoveredAttack` | Moving one piece reveals an attack by another | "Moving the bishop reveals a rook attack on the queen" |
| `doubleCheck` | Two pieces give check simultaneously | "Both the knight and bishop deliver check — the king must move" |
| `deflection` | A defending piece is lured away from its defensive duties | "The rook sacrifice deflects the knight from defending e7" |
| `decoy` | A piece is lured to a bad square | "The queen sacrifice decoys the king to d2 where it's mated" |
| `sacrifice` | Material is given up for a greater advantage | "The bishop sacrifice on h7 destroys the king's pawn shield" |
| `backRankMate` | Checkmate on the back rank | "The rook delivers checkmate — the king is trapped by its own pawns" |
| `smotheredMate` | Checkmate by a knight with the king surrounded by its own pieces | "The knight delivers smothered mate — the king is entombed" |
| `attraction` | A piece is forced to a square where it can be attacked | "The rook check forces the king to g8, setting up the queen mate" |
| `interference` | A piece is placed between two defending pieces | "The knight on e6 cuts off communication between the rooks" |
| `clearance` | A square or line is cleared for tactical use | "The pawn advance clears the e-file for the rook" |
| `xRayAttack` | A piece "sees through" another piece | "The rook on d1 x-rays through the queen to the king" |
| `overloading` | A piece has too many defensive tasks | "The queen must defend both f7 and the back rank — it's overloaded" |
| `trappedPiece` | A piece has no safe squares | "The bishop on b7 is trapped — it has no escape squares" |
| `mateIn1` | Checkmate in one move | "White can deliver checkmate in one move" |
| `mateIn2` | Checkmate in two moves | "White can force checkmate in two moves" |
| `mateIn3` | Checkmate in three moves | "White can force checkmate in three moves" |

### Positional Themes

| Theme | Description | Engine Explanation Pattern |
|-------|-------------|---------------------------|
| `advantage` | Converting an advantage | "White has a material advantage that can be converted" |
| `crushing` | Finding the winning move in a dominant position | "Black is already winning — find the most efficient continuation" |
| `equality` | Finding the equalizing move | "White must find the only move to equalize the position" |
| `defensiveMove` | Finding the best defensive resource | "The only move that avoids losing material" |
| `quietMove` | A non-forcing but strong move | "This quiet move improves the position without threats" |
| `zugzwang` | Any move worsens the position | "Black is in zugzwang — any move loses" |

### Game Phase Themes

| Theme | Description |
|-------|-------------|
| `opening` | Puzzle from the opening phase |
| `middlegame` | Puzzle from the middlegame |
| `endgame` | Puzzle from the endgame |

### Length Themes

| Theme | Description |
|-------|-------------|
| `short` | 1-2 move solution |
| `long` | 3+ move solution |
| `veryLong` | 5+ move solution |

---

## Building the SQLite Puzzle Database

### Database Schema

```sql
-- Puzzle database schema
CREATE TABLE IF NOT EXISTS puzzles (
    puzzle_id TEXT PRIMARY KEY,
    fen TEXT NOT NULL,                -- Position BEFORE opponent's move
    moves TEXT NOT NULL,              -- UCI move sequence (space-separated)
    rating INTEGER NOT NULL,
    rating_deviation INTEGER NOT NULL,
    popularity INTEGER NOT NULL,
    nb_plays INTEGER NOT NULL,
    themes TEXT,                      -- Comma-separated theme tags
    game_url TEXT,
    opening_tags TEXT,

    -- Computed fields (populated during import)
    solution_move TEXT,               -- First move of the solution (2nd in sequence)
    opponent_move TEXT,               -- First move in sequence (applied automatically)
    fen_after_opponent TEXT,          -- FEN after opponent's move (the puzzle position)
    side_to_solve TEXT,               -- 'white' or 'black'
    num_solution_moves INTEGER,       -- Length of the solution
    is_mate_puzzle INTEGER DEFAULT 0, -- 1 if themes contain 'mateIn'
    primary_theme TEXT,               -- First theme listed
    difficulty_tier TEXT              -- 'beginner', 'intermediate', 'advanced', 'expert'
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_puzzle_rating ON puzzles(rating);
CREATE INDEX IF NOT EXISTS idx_puzzle_theme ON puzzles(primary_theme);
CREATE INDEX IF NOT EXISTS idx_puzzle_themes ON puzzles(themes);
CREATE INDEX IF NOT EXISTS idx_puzzle_opening ON puzzles(opening_tags);
CREATE INDEX IF NOT EXISTS idx_puzzle_difficulty ON puzzles(difficulty_tier);
CREATE INDEX IF NOT EXISTS idx_puzzle_side ON puzzles(side_to_solve);

-- Puzzle themes junction table (for many-to-many queries)
CREATE TABLE IF NOT EXISTS puzzle_themes (
    puzzle_id TEXT NOT NULL,
    theme TEXT NOT NULL,
    PRIMARY KEY (puzzle_id, theme),
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(puzzle_id)
);

CREATE INDEX IF NOT EXISTS idx_theme ON puzzle_themes(theme);
```

### Import Script

```python
#!/usr/bin/env python3
"""
import_puzzles.py — Import Lichess puzzle database into SQLite

Usage:
    python import_puzzles.py --input lichess_db_puzzle.csv --output puzzles.db

Download the CSV from: https://database.lichess.org/#puzzles
"""

import csv
import sqlite3
import argparse
import logging
from typing import List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Puzzle:
    puzzle_id: str
    fen: str
    moves: str
    rating: int
    rating_deviation: int
    popularity: int
    nb_plays: int
    themes: str
    game_url: str
    opening_tags: str

    @property
    def move_list(self) -> List[str]:
        """Parse the UCI move string into a list."""
        return self.moves.split()

    @property
    def opponent_move(self) -> str:
        """The first move in the sequence (applied automatically)."""
        return self.move_list[0]

    @property
    def solution_moves(self) -> List[str]:
        """All moves after the opponent's first move."""
        return self.move_list[1:]

    @property
    def solution_move(self) -> str:
        """The first move of the solution."""
        return self.move_list[1]

    @property
    def side_to_solve(self) -> str:
        """Which side must find the solution?"""
        # The FEN tells us who moves first (the opponent)
        fen_parts = self.fen.split()
        opponent_side = fen_parts[1]  # 'w' or 'b'
        # The solver plays the opposite side
        return 'black' if opponent_side == 'w' else 'white'

    @property
    def primary_theme(self) -> str:
        """The first (most important) theme."""
        return self.themes.split()[0] if self.themes else ''

    @property
    def is_mate_puzzle(self) -> bool:
        """Whether the puzzle involves checkmate."""
        return any(t.startswith('mateIn') for t in self.themes.split())

    @property
    def difficulty_tier(self) -> str:
        """Classify puzzle difficulty into tiers."""
        if self.rating < 1000:
            return 'beginner'
        elif self.rating < 1500:
            return 'intermediate'
        elif self.rating < 2000:
            return 'advanced'
        else:
            return 'expert'


def compute_fen_after_move(fen: str, uci_move: str) -> str:
    """
    Apply a UCI move to a FEN and return the new FEN.
    Uses python-chess for accurate FEN manipulation.
    """
    import chess

    board = chess.Board(fen)
    move = chess.Move.from_uci(uci_move)

    if move not in board.legal_moves:
        logger.warning(f"Illegal move {uci_move} in position {fen}")
        return fen

    board.push(move)
    return board.fen()


def import_puzzles(csv_path: str, db_path: str, batch_size: int = 50000):
    """Import puzzles from Lichess CSV into SQLite database."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript(SCHEMA)
    conn.commit()

    # Import CSV
    logger.info(f"Importing puzzles from {csv_path}...")
    puzzle_count = 0
    batch = []

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)

        # Skip header row
        next(reader)

        for row in reader:
            try:
                puzzle = Puzzle(
                    puzzle_id=row[0],
                    fen=row[1],
                    moves=row[2],
                    rating=int(row[3]),
                    rating_deviation=int(row[4]),
                    popularity=int(row[5]),
                    nb_plays=int(row[6]),
                    themes=row[7],
                    game_url=row[8],
                    opening_tags=row[9] if len(row) > 9 else ''
                )

                # Compute derived fields
                fen_after_opponent = compute_fen_after_move(puzzle.fen, puzzle.opponent_move)

                # Insert into puzzles table
                batch.append((
                    puzzle.puzzle_id,
                    puzzle.fen,
                    puzzle.moves,
                    puzzle.rating,
                    puzzle.rating_deviation,
                    puzzle.popularity,
                    puzzle.nb_plays,
                    puzzle.themes,
                    puzzle.game_url,
                    puzzle.opening_tags,
                    puzzle.solution_move,
                    puzzle.opponent_move,
                    fen_after_opponent,
                    puzzle.side_to_solve,
                    len(puzzle.solution_moves),
                    1 if puzzle.is_mate_puzzle else 0,
                    puzzle.primary_theme,
                    puzzle.difficulty_tier
                ))

                # Insert theme associations
                for theme in puzzle.themes.split():
                    cursor.execute(
                        "INSERT OR IGNORE INTO puzzle_themes (puzzle_id, theme) VALUES (?, ?)",
                        (puzzle.puzzle_id, theme)
                    )

                puzzle_count += 1

                # Batch insert
                if len(batch) >= batch_size:
                    cursor.executemany(INSERT_PUZZLE_SQL, batch)
                    conn.commit()
                    batch.clear()
                    logger.info(f"  Imported {puzzle_count:,} puzzles...")

            except Exception as e:
                logger.error(f"Error importing puzzle {row[0]}: {e}")
                continue

    # Flush remaining
    if batch:
        cursor.executemany(INSERT_PUZZLE_SQL, batch)
        conn.commit()

    # Create indices
    logger.info("Creating indices...")
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_puzzle_rating ON puzzles(rating);
        CREATE INDEX IF NOT EXISTS idx_puzzle_theme ON puzzles(primary_theme);
        CREATE INDEX IF NOT EXISTS idx_theme ON puzzle_themes(theme);
        CREATE INDEX IF NOT EXISTS idx_puzzle_opening ON puzzles(opening_tags);
        CREATE INDEX IF NOT EXISTS idx_puzzle_difficulty ON puzzles(difficulty_tier);
    """)
    conn.commit()

    conn.close()
    logger.info(f"Import complete! {puzzle_count:,} puzzles imported to {db_path}")


# SQL for inserting a puzzle
INSERT_PUZZLE_SQL = """
INSERT OR REPLACE INTO puzzles (
    puzzle_id, fen, moves, rating, rating_deviation, popularity, nb_plays,
    themes, game_url, opening_tags, solution_move, opponent_move,
    fen_after_opponent, side_to_solve, num_solution_moves,
    is_mate_puzzle, primary_theme, difficulty_tier
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SCHEMA = """
CREATE TABLE IF NOT EXISTS puzzles (
    puzzle_id TEXT PRIMARY KEY,
    fen TEXT NOT NULL,
    moves TEXT NOT NULL,
    rating INTEGER NOT NULL,
    rating_deviation INTEGER NOT NULL,
    popularity INTEGER NOT NULL,
    nb_plays INTEGER NOT NULL,
    themes TEXT,
    game_url TEXT,
    opening_tags TEXT,
    solution_move TEXT,
    opponent_move TEXT,
    fen_after_opponent TEXT,
    side_to_solve TEXT,
    num_solution_moves INTEGER,
    is_mate_puzzle INTEGER DEFAULT 0,
    primary_theme TEXT,
    difficulty_tier TEXT
);

CREATE TABLE IF NOT EXISTS puzzle_themes (
    puzzle_id TEXT NOT NULL,
    theme TEXT NOT NULL,
    PRIMARY KEY (puzzle_id, theme)
);
"""


def main():
    parser = argparse.ArgumentParser(description="Import Lichess puzzle database")
    parser.add_argument("--input", required=True, help="Path to lichess puzzle CSV")
    parser.add_argument("--output", required=True, help="Output SQLite database path")
    parser.add_argument("--batch-size", type=int, default=50000, help="Insert batch size")
    args = parser.parse_args()

    import_puzzles(args.input, args.output, args.batch_size)


if __name__ == "__main__":
    main()
```

---

## Querying the Puzzle Database

### Query by Theme

```python
def query_by_theme(db_path: str, theme: str, limit: int = 10) -> List[Puzzle]:
    """Find puzzles that test a specific tactical theme."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.* FROM puzzles p
        JOIN puzzle_themes pt ON p.puzzle_id = pt.puzzle_id
        WHERE pt.theme = ?
        AND p.popularity > 80       -- Only well-regarded puzzles
        AND p.rating_deviation < 100 -- Reliable rating
        ORDER BY p.nb_plays DESC
        LIMIT ?
    """, (theme, limit))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
```

### Query by Rating Range

```python
def query_by_rating(db_path: str, min_rating: int, max_rating: int,
                    limit: int = 10) -> List[dict]:
    """Find puzzles appropriate for a specific skill level."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM puzzles
        WHERE rating BETWEEN ? AND ?
        AND popularity > 80
        AND rating_deviation < 100
        ORDER BY RANDOM()
        LIMIT ?
    """, (min_rating, max_rating, limit))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
```

### Query by Opening

```python
def query_by_opening(db_path: str, opening_tag: str, limit: int = 10) -> List[dict]:
    """Find puzzles from a specific opening. Useful for opening study."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM puzzles
        WHERE opening_tags LIKE ?
        AND popularity > 80
        ORDER BY rating ASC
        LIMIT ?
    """, (f'%{opening_tag}%', limit))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
```

---

## Connecting Puzzles to Engine Explanations

The most powerful aspect of the puzzle database for the [[Explainable Chess Engine]] is the ability to verify that the engine's explanations match the tactical theme:

```python
def verify_engine_explanation(puzzle: dict, engine: 'ExplainableEngine') -> dict:
    """
    Verify that the engine's explanation for a puzzle solution
    matches the puzzle's designated tactical theme.

    Returns a comparison report.
    """
    import chess

    # Set up the puzzle position (after opponent's first move)
    board = chess.Board(puzzle['fen_after_opponent'])

    # Get engine's evaluation and explanation
    result = engine.evaluate_and_explain(board)

    # Check if engine found the correct move
    correct_move = puzzle['solution_move']
    engine_move = result['best_move_uci']
    move_correct = (engine_move == correct_move)

    # Check if engine's explanation mentions the puzzle's themes
    explanation_text = result['explanation'].lower()
    themes = puzzle['themes'].split()

    theme_coverage = {}
    for theme in themes:
        # Map Lichess theme names to engine explanation keywords
        theme_keywords = {
            'fork': ['fork', 'attacks two', 'simultaneous attack'],
            'pin': ['pin', 'pinned', 'cannot move'],
            'skewer': ['skewer', 'forced to move', 'exposes'],
            'backRankMate': ['back rank', 'trapped by own pawns', 'mated on back rank'],
            'sacrifice': ['sacrifice', 'giving up material', 'material investment'],
            'deflection': ['deflect', 'lure away', 'removing defender'],
            'discoveredAttack': ['discovered attack', 'reveals attack', 'unmasked'],
            'doubleCheck': ['double check', 'two pieces check'],
            'overloading': ['overloaded', 'too many tasks', 'defending both'],
            'trappedPiece': ['trapped', 'no escape', 'no safe square'],
            'mateIn1': ['checkmate', 'mate in one', 'mated'],
            'mateIn2': ['mate in two', 'force mate'],
            'endgame': ['endgame', 'king and pawn', 'opposition'],
            'advantage': ['advantage', 'better position', 'converting'],
            'defensiveMove': ['defensive', 'only move', 'saving move'],
            'quietMove': ['quiet move', 'improving position', 'non-forcing'],
            'zugzwang': ['zugzwang', 'any move loses', 'forced to worsen'],
        }

        keywords = theme_keywords.get(theme, [theme.lower()])
        found = any(kw in explanation_text for kw in keywords)
        theme_coverage[theme] = found

    return {
        'puzzle_id': puzzle['puzzle_id'],
        'correct_move_found': move_correct,
        'engine_move': engine_move,
        'expected_move': correct_move,
        'engine_evaluation': result['evaluation'],
        'engine_explanation': result['explanation'],
        'theme_coverage': theme_coverage,
        'all_themes_explained': all(theme_coverage.values()),
        'active_rules': result['active_rules']
    }
```

### Batch Verification

```python
def batch_verify(db_path: str, engine: 'ExplainableEngine',
                 theme: str = None, limit: int = 100) -> dict:
    """Run verification across many puzzles and compute statistics."""

    if theme:
        puzzles = query_by_theme(db_path, theme, limit)
    else:
        puzzles = query_by_rating(db_path, 1200, 1800, limit)

    results = []
    for puzzle in puzzles:
        report = verify_engine_explanation(puzzle, engine)
        results.append(report)

    # Aggregate statistics
    move_accuracy = sum(1 for r in results if r['correct_move_found']) / len(results)
    theme_explanation_rate = sum(
        1 for r in results if r['all_themes_explained']
    ) / len(results)

    # Per-theme breakdown
    theme_stats = {}
    for r in results:
        for theme, covered in r['theme_coverage'].items():
            if theme not in theme_stats:
                theme_stats[theme] = {'total': 0, 'explained': 0}
            theme_stats[theme]['total'] += 1
            if covered:
                theme_stats[theme]['explained'] += 1

    for theme in theme_stats:
        theme_stats[theme]['rate'] = (
            theme_stats[theme]['explained'] / theme_stats[theme]['total']
        )

    return {
        'total_puzzles': len(results),
        'move_accuracy': move_accuracy,
        'theme_explanation_rate': theme_explanation_rate,
        'theme_breakdown': theme_stats
    }
```

---

## Summary

The Puzzle Database System provides:

1. **2 million+ curated positions** from the Lichess database, each tagged with tactical themes
2. **Critical format understanding**: the FEN is before the opponent's move; the first move in the sequence is applied automatically
3. **SQLite storage** with precomputed fields (solution move, difficulty tier, FEN after opponent's move)
4. **Rich querying** by theme, rating, opening, and difficulty
5. **Explanation verification** — the engine's explanations are checked against the puzzle's designated themes
6. **Theme-keyword mapping** that connects abstract tactical concepts to natural language explanations

This system directly feeds into the [[04 - Puzzle Training Integration|Puzzle Training]] module and the [[05 - Android Puzzle App Architecture|Android Puzzle App]], creating a complete loop from database to user-facing explanation.
