# Data Pipeline Architecture

> **Chapter 13.01** | [[02 - Feature Extraction in C++|Next: Feature Extraction in C++]] | [[03 - Python PyTorch Optimization Engine|PyTorch Optimization]] | [[04 - The Puzzle Database System|Puzzle Database]]
> **Related**: [[01 - The Slav Defense Philosophy|Slav Defense]], [[04 - Puzzle Training Integration|Puzzle Training]], [[05 - Android Puzzle App Architecture|Android App]]

---

## Overview

The data pipeline is the backbone of the [[Explainable Chess Engine]]. It transforms raw chess data — millions of games in PGN format — into structured, engine-ready feature vectors that can be consumed by both the C++ evaluation engine and the PyTorch training pipeline. Every rule in the [[Rules Engine]] depends on correctly extracted features, and every explanation the engine generates traces back to data that flowed through this pipeline.

The pipeline has five major stages:

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐    ┌──────────────┐
│  Raw PGN     │───│  Position     │───│  Feature      │───│  Training     │───│  Weight      │
│  Files       │    │  Extractor    │    │  Extractor    │    │  Pipeline     │    │  Export       │
│  (millions)  │    │  (C++)        │    │  (C++)        │    │  (Python)     │    │  (JSON)       │
└─────────────┘    └──────────────┘    └───────────────┘    └──────────────┘    └──────────────┘
       │                   │                    │                    │                   │
       ▼                   ▼                    ▼                    ▼                   ▼
  .pgn files         SQLite DB           Binary Feature       PyTorch Tensors      weights.json
  ~100GB             positions.db         Vectors (.bin)       .pt datasets         → C++ engine
```

---

## Stage 1: Parsing PGN Files into Structured Position Data

### The PGN Format

PGN (Portable Game Notation) is the standard format for recording chess games. A single game looks like:

```pgn
[Event "F/S Return Match"]
[Site "Belgrade, Serbia JUG"]
[Date "1992.11.04"]
[Round "29"]
[White "Fischer, Robert J."]
[Black "Spassky, Boris V."]
[Result "1/2-1/2"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 {The Ruy Lopez.} 4. Ba4 Nf6 5. O-O 1/2-1/2
```

The parser must handle:
- **Move text** in Standard Algebraic Notation (SAN)
- **Variations** enclosed in parentheses: `(3... d5 4. exd5)`
- **Comments** enclosed in braces: `{best move}`
- **NAGs** (Numeric Annotation Glyphs): `$1` for good move, `$2` for mistake
- **Results**: `1-0`, `0-1`, `1/2-1/2`, `*`

### The C++ PGN Parser

We use a high-performance C++ parser built on top of a [[Bitboard Engine]]:

```cpp
// pgn_parser.h
#pragma once
#include <string>
#include <vector>
#include <optional>
#include "chess_board.h"

struct PgnGame {
    std::map<std::string, std::string> headers;
    struct MoveRecord {
        std::string san;           // "Nf3"
        std::string comment;       // "developing the knight"
        int nag = 0;              // annotation glyph
        uint16_t move_data;       // packed move for engine use
        std::string fen_before;   // FEN before this move
        std::string fen_after;    // FEN after this move
    };
    std::vector<MoveRecord> moves;
    std::string result;           // "1-0", "0-1", "1/2-1/2"
};

class PgnParser {
public:
    // Parse a single game from a PGN string
    std::optional<PgnGame> parse_game(const std::string& pgn_text);

    // Parse an entire PGN file (potentially millions of games)
    // Uses streaming to handle files > 100GB
    std::vector<PgnGame> parse_file(const std::string& filepath);

    // Streaming parser for massive files — calls callback per game
    using GameCallback = std::function<void(const PgnGame&)>;
    void parse_file_streaming(
        const std::string& filepath,
        GameCallback callback,
        size_t max_games = 0  // 0 = unlimited
    );

private:
    ChessBoard board_;  // Current board state during parsing

    std::string parse_header_line(const std::string& line);
    std::optional<uint16_t> parse_san_move(const std::string& san);
    std::string extract_comment(const std::string& text, size_t& pos);
};
```

### The Streaming Parser Implementation

For datasets like the Lichess database (~100 million games), we cannot load everything into memory. The streaming parser processes one game at a time:

```cpp
void PgnParser::parse_file_streaming(
    const std::string& filepath,
    GameCallback callback,
    size_t max_games)
{
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open PGN file: " + filepath);
    }

    std::string line;
    std::string current_game_text;
    size_t games_parsed = 0;

    while (std::getline(file, line)) {
        // A blank line after move text signals end of game
        if (line.empty() && !current_game_text.empty()) {
            // Check if we have both headers and moves
            if (current_game_text.find('1.') != std::string::npos) {
                auto game = parse_game(current_game_text);
                if (game.has_value()) {
                    callback(game.value());
                    games_parsed++;
                    if (max_games > 0 && games_parsed >= max_games) {
                        return;  // Limit reached
                    }
                }
            }
            current_game_text.clear();
        } else {
            current_game_text += line + "\n";
        }
    }

    // Handle last game (file may not end with blank line)
    if (!current_game_text.empty()) {
        auto game = parse_game(current_game_text);
        if (game.has_value()) {
            callback(game.value());
        }
    }
}
```

---

## Stage 2: Converting Positions to Feature Vectors

Each position in a game is converted into a structured record containing:

1. **The FEN string** — canonical position representation
2. **The move played** — in UCI format (e.g., `e2e4`)
3. **The game result** — `1.0`, `0.0`, or `0.5` from the perspective of the side to move
4. **The feature vector** — 200+ binary and numeric features extracted by the [[02 - Feature Extraction in C++|C++ Feature Extractor]]

### The Training Record Format

```cpp
// training_record.h
#pragma once
#include <string>
#include <vector>
#include <cstdint>

struct TrainingRecord {
    // Position identifiers
    std::string fen;           // Full FEN: "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    std::string move_uci;      // UCI move: "e7e5"
    float result;              // 1.0 (win), 0.0 (loss), 0.5 (draw) from mover's perspective

    // Metadata
    uint16_t elo_white;        // White player's ELO
    uint16_t elo_black;        // Black player's ELO
    uint32_t game_id;          // Links back to source game

    // Feature vector: binary flags + numeric values
    // Binary features: rule_active (1) or rule_inactive (0)
    // Numeric features: material count, mobility, king safety score, etc.
    std::vector<float> features;

    // Serialization for efficient binary storage
    void serialize(std::ostream& out) const;
    static TrainingRecord deserialize(std::istream& in);

    // CSV export for inspection
    std::string to_csv_line() const;
    static TrainingRecord from_csv_line(const std::string& line);
};
```

### Result from Mover's Perspective

This is a crucial detail. The `result` field is always from the perspective of the side making the move:

```cpp
float result_from_mover_perspective(const PgnGame& game, size_t move_index) {
    bool white_won = (game.result == "1-0");
    bool black_won = (game.result == "0-1");
    bool is_draw = (game.result == "1/2-1/2");

    // Even move indices (0, 2, 4...) are White's moves
    bool is_white_move = (move_index % 2 == 0);

    if (is_draw) return 0.5f;
    if (is_white_move) {
        return white_won ? 1.0f : 0.0f;
    } else {
        return black_won ? 1.0f : 0.0f;
    }
}
```

---

## Stage 3: Batch Processing of Large Datasets

### The Pipeline Orchestrator

Processing millions of positions requires careful orchestration of parallelism, memory, and I/O:

```cpp
// pipeline_orchestrator.h
#pragma once
#include "pgn_parser.h"
#include "feature_extractor.h"
#include "training_record.h"
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>

class PipelineOrchestrator {
public:
    struct Config {
        std::string input_pgn_path;     // "/data/lichess_2023.pgn"
        std::string output_db_path;      // "/data/training.db"
        int num_threads = 8;
        size_t batch_size = 10000;       // Records per DB transaction
        size_t max_positions = 0;        // 0 = unlimited
        int min_elo = 2000;             // Filter low-quality games
        int max_elo = 4000;
        bool include_clock = false;      // Include time control info
    };

    void run(const Config& config);

private:
    // Thread-safe queue of parsed games
    std::queue<PgnGame> game_queue_;
    std::mutex queue_mutex_;
    std::condition_variable queue_cv_;
    bool parsing_done_ = false;

    void parser_thread(const Config& config);
    void extractor_thread(int thread_id, const Config& config);
};
```

### The Multi-Threaded Pipeline

```cpp
void PipelineOrchestrator::run(const Config& config) {
    // Phase 1: Initialize output database
    sqlite3* db;
    sqlite3_open(config.output_db_path.c_str(), &db);
    create_training_table(db);  // CREATE TABLE IF NOT EXISTS ...

    // Phase 2: Start parser thread (single producer)
    std::thread parser(&PipelineOrchestrator::parser_thread, this, std::cref(config));

    // Phase 3: Start extractor threads (multiple consumers)
    std::vector<std::thread> extractors;
    for (int i = 0; i < config.num_threads; ++i) {
        extractors.emplace_back(
            &PipelineOrchestrator::extractor_thread, this, i, std::cref(config)
        );
    }

    // Phase 4: Wait for completion
    parser.join();
    for (auto& t : extractors) {
        t.join();
    }

    // Phase 5: Create indices for fast querying
    create_indices(db);
    sqlite3_close(db);
}

void PipelineOrchestrator::extractor_thread(int thread_id, const Config& config) {
    FeatureExtractor extractor;  // Each thread has its own extractor
    sqlite3* db;
    sqlite3_open(config.output_db_path.c_str(), &db);

    std::vector<TrainingRecord> batch;
    batch.reserve(config.batch_size);

    while (true) {
        PgnGame game;

        // Get next game from queue
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            queue_cv_.wait(lock, [this] {
                return !game_queue_.empty() || parsing_done_;
            });

            if (game_queue_.empty() && parsing_done_) {
                break;  // No more games
            }

            game = game_queue_.front();
            game_queue_.pop();
        }

        // Process all positions in this game
        ChessBoard board;
        for (size_t i = 0; i < game.moves.size(); ++i) {
            const auto& move_record = game.moves[i];

            // Extract features from current position
            auto features = extractor.extract(board);

            // Build training record
            TrainingRecord record;
            record.fen = move_record.fen_before;
            record.move_uci = board.move_to_uci(move_record.move_data);
            record.result = result_from_mover_perspective(game, i);
            record.elo_white = std::stoi(game.headers.at("WhiteElo"));
            record.elo_black = std::stoi(game.headers.at("BlackElo"));
            record.features = features;

            batch.push_back(record);

            // Flush batch to DB
            if (batch.size() >= config.batch_size) {
                insert_batch(db, batch);
                batch.clear();
            }

            // Apply move to advance board
            board.make_move(move_record.move_data);
        }
    }

    // Flush remaining records
    if (!batch.empty()) {
        insert_batch(db, batch);
    }

    sqlite3_close(db);
}
```

---

## Stage 4: Data Storage Formats

### SQLite Database Schema

The primary storage format is SQLite, which provides atomic transactions, efficient querying, and single-file portability:

```sql
-- Core training positions table
CREATE TABLE IF NOT EXISTS training_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fen TEXT NOT NULL,
    move_uci TEXT NOT NULL,
    result REAL NOT NULL,           -- 0.0, 0.5, or 1.0
    elo_white INTEGER,
    elo_black INTEGER,
    game_id INTEGER,
    feature_vector BLOB,            -- Packed binary float array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast FEN lookups
CREATE INDEX IF NOT EXISTS idx_fen ON training_positions(fen);

-- Index for filtering by ELO range
CREATE INDEX IF NOT EXISTS idx_elo ON training_positions(elo_white, elo_black);

-- Source games table (for traceability)
CREATE TABLE IF NOT EXISTS source_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    white TEXT,
    black TEXT,
    result TEXT,
    white_elo INTEGER,
    black_elo INTEGER,
    opening_eco TEXT,
    opening_name TEXT,
    pgn_text TEXT,
    import_batch TEXT
);
```

### Binary Feature Vector Format

For the highest throughput, feature vectors are stored as packed binary blobs:

```cpp
void TrainingRecord::serialize(std::ostream& out) const {
    // Write FEN length + FEN string
    uint16_t fen_len = fen.size();
    out.write(reinterpret_cast<const char*>(&fen_len), sizeof(fen_len));
    out.write(fen.data(), fen_len);

    // Write UCI move (always 4 bytes: e2e4, or 5 for promotion: e7e8q)
    uint8_t move_len = move_uci.size();
    out.write(reinterpret_cast<const char*>(&move_len), sizeof(move_len));
    out.write(move_uci.data(), move_len);

    // Write result
    out.write(reinterpret_cast<const char*>(&result), sizeof(result));

    // Write feature vector
    uint16_t num_features = features.size();
    out.write(reinterpret_cast<const char*>(&num_features), sizeof(num_features));
    out.write(reinterpret_cast<const char*>(features.data()),
              num_features * sizeof(float));
}
```

### CSV Format for Interoperability

For debugging and Python interop, we also support CSV export:

```csv
fen,move_uci,result,elo_white,elo_black,feat_0,feat_1,feat_2,...,feat_219
rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1,e7e5,0.5,2510,2480,1.0,0.0,38.0,...,0.0
```

### Performance Comparison of Storage Formats

| Format | Read Speed | Write Speed | File Size (10M positions) | Query Support |
|--------|-----------|-------------|--------------------------|---------------|
| SQLite | 50k rows/s | 100k rows/s (batched) | ~8 GB | Full SQL |
| CSV | 100k rows/s | 200k rows/s | ~15 GB | None (sequential) |
| Binary | 500k rows/s | 1M rows/s | ~4 GB | None (sequential) |
| Parquet | 200k rows/s | 150k rows/s | ~3 GB | Columnar |

For the [[Explainable Chess Engine]], we use **SQLite** as the primary format because:
1. We need to query by FEN, ELO range, and opening
2. Atomic transactions prevent data corruption during large imports
3. The PyTorch [[03 - Python PyTorch Optimization Engine|training pipeline]] can read SQLite directly

---

## Stage 5: End-to-End Pipeline Script

The complete pipeline is orchestrated by a single script:

```python
#!/usr/bin/env python3
"""
run_pipeline.py — End-to-end data pipeline for the Explainable Chess Engine

Usage:
    python run_pipeline.py --input /data/lichess.pgn --output /data/training.db --threads 8
"""

import subprocess
import argparse
import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def compile_cpp_extractor():
    """Compile the C++ feature extractor with optimizations."""
    logger.info("Compiling C++ feature extractor...")
    result = subprocess.run([
        "g++", "-O3", "-std=c++17", "-pthread",
        "-I", "src/include",
        "src/pipeline/pgn_parser.cpp",
        "src/pipeline/feature_extractor.cpp",
        "src/pipeline/pipeline_orchestrator.cpp",
        "src/pipeline/main.cpp",
        "-o", "build/pipeline",
        "-lsqlite3"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Compilation failed:\n{result.stderr}")
        raise RuntimeError("C++ compilation failed")
    logger.info("Compilation successful.")

def run_cpp_pipeline(input_pgn: str, output_db: str, threads: int, min_elo: int):
    """Run the C++ pipeline to parse PGN and extract features."""
    logger.info(f"Running C++ pipeline: {input_pgn} → {output_db}")
    result = subprocess.run([
        "./build/pipeline",
        "--input", input_pgn,
        "--output", output_db,
        "--threads", str(threads),
        "--min-elo", str(min_elo),
        "--batch-size", "10000"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Pipeline failed:\n{result.stderr}")
        raise RuntimeError("Pipeline execution failed")
    logger.info("C++ pipeline completed.")

def validate_output(db_path: str):
    """Validate the output database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM training_positions")
    count = cursor.fetchone()[0]
    logger.info(f"Total positions in database: {count:,}")

    cursor.execute("SELECT AVG(result) FROM training_positions")
    avg_result = cursor.fetchone()[0]
    logger.info(f"Average result (from mover's perspective): {avg_result:.3f}")

    cursor.execute("""
        SELECT MIN(elo_white), MAX(elo_white),
               MIN(elo_black), MAX(elo_black)
        FROM training_positions
    """)
    row = cursor.fetchone()
    logger.info(f"ELO range: White [{row[0]}-{row[1]}], Black [{row[2]}-{row[3]}]")

    # Spot-check a few records
    cursor.execute("SELECT fen, move_uci, result FROM training_positions LIMIT 5")
    for fen, move, result in cursor.fetchall():
        logger.info(f"  Sample: {fen[:50]}... {move} result={result}")

    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Explainable Chess Engine Data Pipeline")
    parser.add_argument("--input", required=True, help="Input PGN file path")
    parser.add_argument("--output", required=True, help="Output SQLite database path")
    parser.add_argument("--threads", type=int, default=8, help="Number of extraction threads")
    parser.add_argument("--min-elo", type=int, default=2000, help="Minimum ELO filter")
    parser.add_argument("--skip-compile", action="store_true", help="Skip C++ compilation")
    args = parser.parse_args()

    if not args.skip_compile:
        compile_cpp_extractor()

    run_cpp_pipeline(args.input, args.output, args.threads, args.min_elo)
    validate_output(args.output)

    logger.info("Pipeline complete! Next step: python train.py --data %s", args.output)

if __name__ == "__main__":
    main()
```

---

## Data Quality and Filtering

Not all positions are equally valuable for training. We apply several filters:

### ELO Filtering
Only games between players rated 2000+ are used. Below this threshold, moves often don't reflect correct evaluation:

```cpp
bool should_include_game(const PgnGame& game, int min_elo) {
    try {
        int white_elo = std::stoi(game.headers.at("WhiteElo"));
        int black_elo = std::stoi(game.headers.at("BlackElo"));
        return white_elo >= min_elo && black_elo >= min_elo;
    } catch (...) {
        return false;  // Missing ELO data → exclude
    }
}
```

### Position Filtering
We exclude certain positions that would corrupt training:

- **Opening positions** (book moves): Skip the first 8-10 moves to avoid biasing the dataset toward opening theory rather than evaluation accuracy
- **Time trouble blunders**: If available, positions where the clock is below 5 seconds
- **Resignation positions**: The move after a blunder is often immediate resignation — these are misleading

```cpp
bool should_include_position(const TrainingRecord& record, int ply) {
    // Skip opening book positions
    if (ply < 16) return false;  // First 8 full moves

    // Skip positions with extreme material imbalance (already decided)
    int material = compute_material(record.fen);
    if (abs(material) > 1500) return false;  // More than a queen advantage

    return true;
}
```

### De-duplication

The same position can appear in thousands of games. We keep at most N copies:

```sql
-- Keep at most 10 records per unique FEN
DELETE FROM training_positions
WHERE id NOT IN (
    SELECT id FROM (
        SELECT id, ROW_NUMBER() OVER (PARTITION BY fen ORDER BY RANDOM()) as rn
        FROM training_positions
    ) WHERE rn <= 10
);
```

---

## Pipeline Metrics and Monitoring

During processing, we track key metrics:

| Metric | Target | Purpose |
|--------|--------|---------|
| Positions/second | > 50k | Overall throughput |
| Feature extraction time | < 10μs/position | [[02 - Feature Extraction in C++\|C++ extractor]] performance |
| DB write throughput | > 100k rows/s | Batch insert efficiency |
| Memory usage | < 4 GB | Prevent OOM on large datasets |
| Duplicate rate | < 5% | De-duplication effectiveness |

```python
class PipelineMetrics:
    def __init__(self):
        self.positions_processed = 0
        self.games_processed = 0
        self.games_filtered = 0
        self.positions_filtered = 0
        self.start_time = time.time()

    def report(self):
        elapsed = time.time() - self.start_time
        pos_rate = self.positions_processed / elapsed
        game_rate = self.games_processed / elapsed
        logger.info(
            f"Progress: {self.positions_processed:,} positions "
            f"({pos_rate:,.0f}/s) | "
            f"{self.games_processed:,} games ({game_rate:,.0f}/s) | "
            f"Filtered: {self.games_filtered:,} games, "
            f"{self.positions_filtered:,} positions"
        )
```

---

## Summary

The data pipeline transforms raw chess game data into the structured format needed for training and evaluation:

1. **Parse** millions of PGN games into structured position data
2. **Convert** each position into a feature vector using the [[02 - Feature Extraction in C++|C++ Feature Extractor]]
3. **Store** training records in SQLite with efficient binary blobs
4. **Filter** for quality: ELO thresholds, position de-duplication, opening exclusion
5. **Export** to the [[03 - Python PyTorch Optimization Engine|PyTorch training pipeline]]

The pipeline processes at 50,000+ positions per second on a modern 8-core machine, meaning the full Lichess database (~4 billion positions) can be processed in approximately 24 hours.
