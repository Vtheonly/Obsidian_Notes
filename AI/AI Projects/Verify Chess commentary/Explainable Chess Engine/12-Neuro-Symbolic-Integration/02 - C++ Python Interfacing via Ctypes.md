# C++ Python Interfacing via Ctypes

> **Chapter 12 — Neuro-Symbolic Integration** | ← [[Neuro-Symbolic Architecture Overview]] | → [[Declarative Rule Engine with Bitboards]]

---

## Why Ctypes?

The [[Neuro-Symbolic Architecture Overview|architecture]] requires C++ (for search speed) and Python (for explanation flexibility). We need a bridge between them. **Ctypes** is Python's built-in Foreign Function Interface (FFI) that allows calling C functions from dynamically loaded shared libraries (.so on Linux, .dll on Windows, .dylib on macOS).

### Advantages Over Alternatives

| Feature | Ctypes | Cython | PyBind11 | Subprocess |
|---|---|---|---|---|
| No extra dependencies |  |  |  |  |
| Python standard library |  |  |  |  |
| Direct memory access |  |  |  |  |
| No compilation step |  |  |  |  |
| Low overhead |  |  |  |  |
| Full C++ interop |  |  |  |  |
| C only |  |  |  | N/A |

The key limitation: **Ctypes can only call C functions, not C++ functions**. This means we need a C API wrapper around our C++ code.

---

## The C-API with extern "C" Linkage

### The Name Mangling Problem

C++ compilers use **name mangling** to encode function signatures into symbol names. For example, a function `search_position(const char*, int)` might be mangled to `_Z15search_positionPKci`. Python's ctypes expects simple C-style symbol names like `search_position`.

### The Solution: extern "C"

The `extern "C"` linkage specifier tells the C++ compiler to use C-style naming:

```cpp
// chess_api.h — The C-API header
#pragma once

#ifdef _WIN32
    #define API_EXPORT __declspec(dllexport)
#else
    #define API_EXPORT __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================
// Core search functions
// ============================================================

/// Search a position and return the best move.
/// @param fen         FEN string of the position
/// @param depth       Search depth (1-30)
/// @param score       Output: evaluation score in centipawns
/// @param pv_buffer   Output: principal variation as space-separated moves
/// @param pv_size     Size of pv_buffer in bytes
/// @return            0 on success, error code on failure
API_EXPORT int search_position(
    const char* fen,
    int depth,
    int* score,
    char* pv_buffer,
    int pv_size
);

/// Extract all heuristic features for a position.
/// @param fen             FEN string of the position
/// @param feature_buffer  Output: array of Feature structs
/// @param buffer_capacity Maximum number of features to write
/// @return                Number of features written
API_EXPORT int extract_features(
    const char* fen,
    struct CFeature* feature_buffer,
    int buffer_capacity
);

/// Compute feature deltas between two positions.
/// @param fen_before       FEN before the move
/// @param fen_after        FEN after the move
/// @param delta_buffer     Output: array of Delta structs
/// @param buffer_capacity  Maximum number of deltas to write
/// @return                 Number of deltas written
API_EXPORT int extract_move_deltas(
    const char* fen_before,
    const char* fen_after,
    struct CDelta* delta_buffer,
    int buffer_capacity
);

/// Get the primary strategic driver for a move.
/// @param fen_before       FEN before the move
/// @param fen_after        FEN after the move
/// @param driver_buffer    Output: rule name string
/// @param buffer_size      Size of driver_buffer in bytes
API_EXPORT void get_primary_driver(
    const char* fen_before,
    const char* fen_after,
    char* driver_buffer,
    int buffer_size
);

/// Initialize the engine (load weights, etc.)
/// @param weights_path  Path to the weights file
/// @return              0 on success
API_EXPORT int engine_init(const char* weights_path);

/// Clean up engine resources.
API_EXPORT void engine_cleanup(void);

// ============================================================
// Data structures
// ============================================================

/// A single feature (rule name + score)
struct CFeature {
    char name[64];    // Rule name, null-terminated
    int  value;       // Score in centipawns
};

/// A feature delta (before/after/delta)
struct CDelta {
    char name[64];    // Rule name, null-terminated
    int  before;      // Score before the move
    int  after;       // Score after the move
    int  delta;       // Change: after - before
};

#ifdef __cplusplus
}
#endif
```

### The Implementation File

```cpp
// chess_api.cpp — Implementation of the C-API
#include "chess_api.h"
#include "position.h"
#include "search.h"
#include "evaluation.h"
#include <cstring>
#include <algorithm>

// Global engine state (simple singleton pattern)
static std::unique_ptr<SearchEngine> g_engine;

extern "C" int engine_init(const char* weights_path) {
    try {
        auto weights = EvalWeights::load_from_file(weights_path);
        g_engine = std::make_unique<SearchEngine>(weights);
        return 0;
    } catch (const std::exception& e) {
        return -1;  // Error code
    }
}

extern "C" void engine_cleanup(void) {
    g_engine.reset();
}

extern "C" int search_position(
    const char* fen,
    int depth,
    int* score,
    char* pv_buffer,
    int pv_size)
{
    if (!g_engine || !fen || !score || !pv_buffer) {
        return -1;  // Invalid arguments
    }

    try {
        Position pos = Position::from_fen(fen);
        SearchResult result = g_engine->search(pos, depth);

        *score = result.score;

        // Write PV as space-separated moves
        std::string pv_str;
        for (size_t i = 0; i < result.pv.size(); i++) {
            if (i > 0) pv_str += " ";
            pv_str += result.pv[i].to_san(pos);
            pos.make_move(result.pv[i]);
        }

        std::strncpy(pv_buffer, pv_str.c_str(), pv_size - 1);
        pv_buffer[pv_size - 1] = '\0';

        return 0;
    } catch (const std::exception& e) {
        return -2;  // Search error
    }
}

extern "C" int extract_features(
    const char* fen,
    CFeature* feature_buffer,
    int buffer_capacity)
{
    if (!g_engine || !fen || !feature_buffer) {
        return -1;
    }

    try {
        Position pos = Position::from_fen(fen);
        auto features = g_engine->extract_all_features(pos);

        int count = std::min(
            static_cast<int>(features.size()),
            buffer_capacity
        );

        for (int i = 0; i < count; i++) {
            std::strncpy(
                feature_buffer[i].name,
                features[i].name.c_str(),
                63
            );
            feature_buffer[i].name[63] = '\0';
            feature_buffer[i].value = features[i].score;
        }

        return count;
    } catch (const std::exception& e) {
        return -2;
    }
}

extern "C" int extract_move_deltas(
    const char* fen_before,
    const char* fen_after,
    CDelta* delta_buffer,
    int buffer_capacity)
{
    if (!g_engine || !fen_before || !fen_after || !delta_buffer) {
        return -1;
    }

    try {
        Position pos_before = Position::from_fen(fen_before);
        Position pos_after  = Position::from_fen(fen_after);

        auto features_before = g_engine->extract_all_features(pos_before);
        auto features_after  = g_engine->extract_all_features(pos_after);

        // Compute deltas
        std::vector<CDelta> deltas;
        for (size_t i = 0; i < features_after.size(); i++) {
            CDelta d;
            std::strncpy(d.name, features_after[i].name.c_str(), 63);
            d.name[63] = '\0';
            d.before = (i < features_before.size()) ?
                        features_before[i].score : 0;
            d.after  = features_after[i].score;
            d.delta  = d.after - d.before;
            deltas.push_back(d);
        }

        // Sort by absolute delta magnitude (descending)
        std::sort(deltas.begin(), deltas.end(),
            [](const CDelta& a, const CDelta& b) {
                return std::abs(a.delta) > std::abs(b.delta);
            });

        int count = std::min(
            static_cast<int>(deltas.size()),
            buffer_capacity
        );

        std::memcpy(delta_buffer, deltas.data(),
                     count * sizeof(CDelta));

        return count;
    } catch (const std::exception& e) {
        return -2;
    }
}

extern "C" void get_primary_driver(
    const char* fen_before,
    const char* fen_after,
    char* driver_buffer,
    int buffer_size)
{
    if (!g_engine || !fen_before || !fen_after || !driver_buffer) {
        if (driver_buffer && buffer_size > 0) {
            driver_buffer[0] = '\0';
        }
        return;
    }

    try {
        CDelta deltas[256];
        int count = extract_move_deltas(
            fen_before, fen_after, deltas, 256
        );

        // Find the first positive delta (largest magnitude)
        std::string driver = "None";
        for (int i = 0; i < count; i++) {
            if (deltas[i].delta > 0) {
                driver = deltas[i].name;
                break;
            }
        }

        std::strncpy(driver_buffer, driver.c_str(), buffer_size - 1);
        driver_buffer[buffer_size - 1] = '\0';
    } catch (const std::exception& e) {
        driver_buffer[0] = '\0';
    }
}
```

### Building the Shared Library

```bash
# Linux
g++ -O3 -shared -fPIC -o libchess_engine.so \
    chess_api.cpp position.cpp search.cpp evaluation.cpp \
    -std=c++17 -march=native

# macOS
g++ -O3 -shared -fPIC -o libchess_engine.dylib \
    chess_api.cpp position.cpp search.cpp evaluation.cpp \
    -std=c++17 -march=native

# Windows (MSVC)
cl /O2 /LD /Fe:chess_engine.dll \
    chess_api.cpp position.cpp search.cpp evaluation.cpp \
    /std:c++17
```

---

## Python Ctypes Wrapper

### Defining C Function Signatures

```python
import ctypes
import os
import platform
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Define C-compatible structures
class CFeatureC(ctypes.Structure):
    """C struct matching CFeature."""
    _fields_ = [
        ("name", ctypes.c_char * 64),
        ("value", ctypes.c_int),
    ]

class CDeltaC(ctypes.Structure):
    """C struct matching CDelta."""
    _fields_ = [
        ("name", ctypes.c_char * 64),
        ("before", ctypes.c_int),
        ("after", ctypes.c_int),
        ("delta", ctypes.c_int),
    ]


class ChessEngine:
    """Python wrapper for the C++ chess engine via ctypes."""

    def __init__(self, lib_path: str, weights_path: str):
        """Load the shared library and initialize the engine.

        Args:
            lib_path: Path to the shared library (.so/.dll/.dylib)
            weights_path: Path to the evaluation weights file
        """
        self.lib = ctypes.CDLL(lib_path)
        self._setup_signatures()
        self._init_engine(weights_path)

    def _setup_signatures(self):
        """Define C function signatures for type-safe calls."""
        # engine_init
        self.lib.engine_init.argtypes = [ctypes.c_char_p]
        self.lib.engine_init.restype = ctypes.c_int

        # engine_cleanup
        self.lib.engine_cleanup.argtypes = []
        self.lib.engine_cleanup.restype = None

        # search_position
        self.lib.search_position.argtypes = [
            ctypes.c_char_p,           # fen
            ctypes.c_int,              # depth
            ctypes.POINTER(ctypes.c_int),  # score
            ctypes.c_char_p,           # pv_buffer
            ctypes.c_int,              # pv_size
        ]
        self.lib.search_position.restype = ctypes.c_int

        # extract_features
        self.lib.extract_features.argtypes = [
            ctypes.c_char_p,               # fen
            ctypes.POINTER(CFeatureC),     # feature_buffer
            ctypes.c_int,                  # buffer_capacity
        ]
        self.lib.extract_features.restype = ctypes.c_int

        # extract_move_deltas
        self.lib.extract_move_deltas.argtypes = [
            ctypes.c_char_p,           # fen_before
            ctypes.c_char_p,           # fen_after
            ctypes.POINTER(CDeltaC),   # delta_buffer
            ctypes.c_int,              # buffer_capacity
        ]
        self.lib.extract_move_deltas.restype = ctypes.c_int

        # get_primary_driver
        self.lib.get_primary_driver.argtypes = [
            ctypes.c_char_p,   # fen_before
            ctypes.c_char_p,   # fen_after
            ctypes.c_char_p,   # driver_buffer
            ctypes.c_int,      # buffer_size
        ]
        self.lib.get_primary_driver.restype = None

    def _init_engine(self, weights_path: str):
        """Initialize the engine with weights."""
        result = self.lib.engine_init(weights_path.encode())
        if result != 0:
            raise RuntimeError(
                f"Failed to initialize engine (error code: {result})"
            )

    def search(self, fen: str, depth: int = 15) -> Tuple[int, str]:
        """Search a position and return (score, principal_variation).

        Args:
            fen: FEN string of the position
            depth: Search depth (1-30)

        Returns:
            Tuple of (score in centipawns, PV as SAN string)
        """
        score = ctypes.c_int()
        pv_buffer = ctypes.create_string_buffer(1024)

        result = self.lib.search_position(
            fen.encode(),
            depth,
            ctypes.byref(score),
            pv_buffer,
            1024
        )

        if result != 0:
            raise RuntimeError(f"Search failed (error code: {result})")

        return score.value, pv_buffer.value.decode()

    def extract_features(self, fen: str) -> List[dict]:
        """Extract all heuristic features for a position.

        Args:
            fen: FEN string

        Returns:
            List of dicts with 'name' and 'value' keys
        """
        MAX_FEATURES = 256
        buffer = (CFeatureC * MAX_FEATURES)()

        count = self.lib.extract_features(
            fen.encode(),
            buffer,
            MAX_FEATURES
        )

        if count < 0:
            raise RuntimeError(
                f"Feature extraction failed (error code: {count})"
            )

        return [
            {"name": buffer[i].name.decode(), "value": buffer[i].value}
            for i in range(count)
        ]

    def extract_deltas(self, fen_before: str,
                        fen_after: str) -> List[dict]:
        """Compute feature deltas between two positions.

        Args:
            fen_before: FEN before the move
            fen_after: FEN after the move

        Returns:
            List of delta dicts sorted by magnitude
        """
        MAX_DELTAS = 256
        buffer = (CDeltaC * MAX_DELTAS)()

        count = self.lib.extract_move_deltas(
            fen_before.encode(),
            fen_after.encode(),
            buffer,
            MAX_DELTAS
        )

        if count < 0:
            raise RuntimeError(
                f"Delta extraction failed (error code: {count})"
            )

        return [
            {
                "name": buffer[i].name.decode(),
                "before": buffer[i].before,
                "after": buffer[i].after,
                "delta": buffer[i].delta,
            }
            for i in range(count)
        ]

    def get_primary_driver(self, fen_before: str,
                            fen_after: str) -> str:
        """Get the primary strategic driver for a move."""
        buf = ctypes.create_string_buffer(64)
        self.lib.get_primary_driver(
            fen_before.encode(),
            fen_after.encode(),
            buf,
            64
        )
        return buf.value.decode()

    def __del__(self):
        """Clean up engine resources."""
        if hasattr(self, 'lib'):
            self.lib.engine_cleanup()
```

---

## Error Handling Across the Boundary

### C++ Side: Return Error Codes

```cpp
// Error codes
enum ErrorCode {
    SUCCESS = 0,
    ERR_NULL_POINTER = -1,
    ERR_INVALID_FEN = -2,
    ERR_ENGINE_NOT_INIT = -3,
    ERR_SEARCH_FAILED = -4,
    ERR_BUFFER_TOO_SMALL = -5,
};
```

### Python Side: Convert to Exceptions

```python
class ChessEngineError(Exception):
    """Base exception for chess engine errors."""
    ERROR_MESSAGES = {
        -1: "Null pointer passed to engine",
        -2: "Invalid FEN string",
        -3: "Engine not initialized",
        -4: "Search failed",
        -5: "Output buffer too small",
    }

    def __init__(self, code: int):
        self.code = code
        msg = self.ERROR_MESSAGES.get(code, f"Unknown error ({code})")
        super().__init__(msg)

def check_error(result: int):
    """Check an engine return code and raise if error."""
    if result != 0:
        raise ChessEngineError(result)
```

### FEN Validation on Python Side

To avoid passing invalid FENs to C++, validate on the Python side first:

```python
import re

def validate_fen(fen: str) -> bool:
    """Validate a FEN string before passing to the engine."""
    parts = fen.split()
    if len(parts) != 6:
        return False

    # Board position: 8 ranks separated by /
    ranks = parts[0].split('/')
    if len(ranks) != 8:
        return False

    for rank in ranks:
        count = 0
        for ch in rank:
            if ch.isdigit():
                count += int(ch)
            elif ch in 'pnbrqkPNBRQK':
                count += 1
            else:
                return False
        if count != 8:
            return False

    return True
```

---

## Thread Safety Considerations

### The Problem

If multiple Python threads call the C++ engine simultaneously (e.g., analyzing multiple positions in parallel), the global `g_engine` state creates a race condition.

### Solution: Thread-Local Engine Instances

```cpp
// thread_safe_api.cpp
#include <thread>
#include <mutex>
#include <unordered_map>

static std::mutex g_mutex;
static std::unordered_map<std::thread::id,
                           std::unique_ptr<SearchEngine>> g_engines;

extern "C" int engine_init_thread(const char* weights_path) {
    std::lock_guard<std::mutex> lock(g_mutex);
    auto tid = std::this_thread::get_id();
    try {
        auto weights = EvalWeights::load_from_file(weights_path);
        g_engines[tid] = std::make_unique<SearchEngine>(weights);
        return 0;
    } catch (...) {
        return -1;
    }
}

// Each function acquires the engine for the current thread
static SearchEngine* get_engine() {
    auto tid = std::this_thread::get_id();
    auto it = g_engines.find(tid);
    if (it == g_engines.end()) return nullptr;
    return it->second.get();
}
```

---

## Performance Benchmarks

| Operation | C++ Only | Ctypes Call | Overhead |
|---|---|---|---|
| Feature extraction | 0.8ms | 0.9ms | 12% |
| Search (depth 15) | 2.5s | 2.5s | <1% |
| Delta computation | 1.6ms | 1.8ms | 12% |
| Primary driver | 1.7ms | 1.9ms | 12% |

The ctypes overhead is minimal (~12% for small operations, <1% for long searches) because the data copying overhead is small compared to the computation time.

---

## Connections

- **Previous**: [[Neuro-Symbolic Architecture Overview]] — The overall architecture
- **Next**: [[Declarative Rule Engine with Bitboards]] — What's inside the C++ engine
- **Related**: [[The Verbalization Pipeline]] — How Python uses the ctypes data
- **Upstream**: [[The Heuristic Delta Pipeline]] — The delta computation uses this interface
