# Neuro-Symbolic Architecture Overview

> **Chapter 12 — Neuro-Symbolic Integration** | → [[C++ Python Interfacing via Ctypes]] → [[Declarative Rule Engine with Bitboards]] → [[The Verbalization Pipeline]] → [[Combining Stockfish with Explanations]]

---

## The Two-World Problem

Building an explainable chess engine forces us to confront a fundamental tension between two worlds:

| World | Speed | Flexibility | Expressiveness | Explainability |
|---|---|---|---|---|
| **C++ (Systems)** |  |  |  |  |
| **Python (ML/NLP)** |  |  |  |  |

C++ is essential for **search speed** — a competitive chess engine must evaluate millions of positions per second. Python is essential for **explanation generation** — the NLG pipeline, LLM integration, and delta computation are all natural Python tasks.

We need **both**. The neuro-symbolic architecture is the solution.

---

## What is Neuro-Symbolic Integration?

**Neuro-symbolic integration** combines neural (learned, flexible, approximate) and symbolic (rule-based, rigid, exact) approaches into a single system. In our context:

- **Symbolic**: The C++ rule engine with hand-crafted, interpretable heuristic rules. Each rule produces a human-understandable centipawn score. The search is alpha-beta with these rules.
- **Neural**: The Python LLM narrator that converts structured rule data into natural language. The LLM's "neural" knowledge of chess language provides fluency that rules alone cannot.
- **Integration**: The ctypes boundary that connects C++ speed with Python flexibility.

### Why Not Pure Symbolic?

A pure symbolic system (C++ only) produces correct but incomprehensible output:

```
Move: e2e4
Eval: +35
Rules: Center_Control=+12, Development=+8, Space=+7, Mobility=+5, King_Safety=+3
```

This is accurate but not an "explanation." It requires the reader to already understand what each rule means and how the numbers combine.

### Why Not Pure Neural?

A pure neural system (Python + LLM only) produces fluent but unreliable output:

```
"e4 stakes a claim in the center and opens lines for the bishop and queen,
setting up potential kingside attacks."
```

This sounds great, but the LLM has no actual evaluation data. It might claim "kingside attacks" when the position doesn't support one. It hallucinates.

### The Hybrid: Symbolic Truth + Neural Fluency

```
"e4 controls the center (gaining +12cp from central influence) and develops
the king's bishop to active diagonals (+8cp), creating space for future
piece activity."
```

This is both **faithful** (grounded in rule data) and **fluent** (natural language). This is the neuro-symbolic promise.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Explainable Chess Engine                         │
│                                                                         │
│  ┌──────────────────────────────────┐  ┌─────────────────────────────┐ │
│  │         C++ CORE (Symbolic)       │  │    PYTHON LAYER (Neural)    │ │
│  │                                   │  │                             │ │
│  │  ┌─────────────┐  ┌───────────┐  │  │  ┌──────────────────────┐  │ │
│  │  │  Alpha-Beta  │  │  Rule     │  │  │  │  Delta Pipeline      │  │ │
│  │  │  Search      │  │  Engine   │  │  │  │  (Before/After       │  │ │
│  │  │  Engine      │  │  (200+    │  │  │  │   Feature Deltas)    │  │ │
│  │  │             │  │   Rules)  │  │  │  └──────────┬───────────┘  │ │
│  │  └──────┬──────┘  └─────┬─────┘  │  │             │              │ │
│  │         │               │        │  │  ┌──────────▼───────────┐  │ │
│  │         │               │        │  │  │  JSON Report Builder │  │ │
│  │         ▼               ▼        │  │  │  (Structured Data)   │  │ │
│  │  ┌──────────────────────────┐    │  │  └──────────┬───────────┘  │ │
│  │  │  Feature Extraction API  │    │  │             │              │ │
│  │  │  (extern "C" exports)    │────┼──┼─────────────┤              │ │
│  │  │                          │    │  │  ┌──────────▼───────────┐  │ │
│  │  │  • extract_features()    │    │  │  │  LLM Narrator       │  │ │
│  │  │  • search_position()     │    │  │  │  (Groq API)         │  │ │
│  │  │  • extract_move_deltas() │    │  │  │                     │  │ │
│  │  └──────────────────────────┘    │  │  └──────────┬───────────┘  │ │
│  │                                   │  │             │              │ │
│  └──────────────────────────────────┘  │  ┌──────────▼───────────┐  │ │
│                                         │  │  Natural Language    │  │ │
│          CTypes / ABI Boundary          │  │  Explanation         │  │ │
│                                         │  └──────────────────────┘  │ │
│                                         └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The C++ Core: Fast Search

### Why C++ Is Non-Negotiable

Chess search is fundamentally a performance problem. A competitive engine evaluates:

- **Alpha-beta search**: 1-10 million positions per second
- **Quiescence search**: Additional captures and checks
- **Move ordering**: Sort moves for maximum pruning
- **Transposition table**: Hash table with millions of entries

Python is 50-200x slower than C++ for these tasks. A pure Python engine would evaluate perhaps 50,000 positions per second—roughly the speed of a 1980s chess program. This is not competitive.

### What Lives in C++

| Component | Purpose | Speed Requirement |
|---|---|---|
| Board representation | Bitboards for fast move generation | Millions of ops/sec |
| Move generation | Legal move enumeration | Millions of moves/sec |
| Alpha-beta search | Position evaluation with pruning | Millions of nodes/sec |
| Quiescence search | Tactical resolution | Hundreds of thousands/sec |
| Transposition table | Position memoization | Hash lookups in nanoseconds |
| Rule evaluation | [[Declarative Rule Engine with Bitboards]] | Hundreds of rules per eval |
| Feature extraction | Expose rule scores for Python | On-demand, per-move |

### The Rule Engine in C++

The rule engine is the heart of the symbolic component. Each rule is a function that takes a position and returns a centipawn score:

```cpp
// Each rule is a pure function: Position → int (centipawns)
int eval_knight_outpost(const Position& pos);
int eval_pawn_structure(const Position& pos);
int eval_king_safety(const Position& pos);
int eval_mobility(const Position& pos);
// ... 200+ rules
```

See [[Declarative Rule Engine with Bitboards]] for how these are implemented with 64-bit integers and bitwise operations for maximum speed.

---

## The Python Layer: Flexible Explanation

### What Lives in Python

| Component | Purpose | Why Python |
|---|---|---|
| Delta pipeline | Compute rule score changes | List processing, JSON |
| JSON report builder | Structure data for LLM | Dict manipulation |
| LLM narrator | Generate natural language | API calls, string processing |
| Quality metrics | Evaluate explanations | NumPy, statistical tests |
| Texel tuning | Optimize weights | PyTorch, gradient descent |
| Orthogonality audit | Check rule overlaps | Pandas, correlation analysis |

### Why Python for These Tasks

1. **LLM APIs**: All major LLM providers (Groq, OpenAI, Anthropic) have Python SDKs
2. **Data processing**: Pandas and NumPy make delta computation and statistical analysis trivial
3. **Rapid prototyping**: Adjusting prompts, testing templates, iterating on quality metrics
4. **PyTorch**: The [[Texel Tuning Method]] implementation uses PyTorch
5. **Ecosystem**: JSON, dataclasses, type hints, testing frameworks

---

## The Interface: CTypes / ABI Boundary

### The Contract

The C++ and Python layers communicate through a strict **ABI (Application Binary Interface)** boundary:

```cpp
// C++ side: extern "C" functions
extern "C" {
    int search_position(const char* fen, int depth,
                         int* score, char* pv_buffer);
    int extract_features(const char* fen, Feature* buffer, int capacity);
    int extract_move_deltas(const char* fen_before, const char* fen_after,
                             Delta* buffer, int capacity);
}
```

```python
# Python side: ctypes wrappers
import ctypes
lib = ctypes.CDLL("./libchess_engine.so")
lib.search_position.argtypes = [ctypes.c_char_p, ctypes.c_int,
                                 ctypes.POINTER(ctypes.c_int),
                                 ctypes.c_char_p]
```

See [[C++ Python Interfacing via Ctypes]] for the complete implementation.

### Design Principles for the Interface

1. **Minimal surface area**: Only expose what Python needs (search, feature extraction, delta computation)
2. **Simple data types**: Use C primitives (int, char*) not C++ objects (std::string, std::vector)
3. **Ownership clarity**: C++ owns memory for the board; Python owns memory for reports and API calls
4. **Error handling**: Return error codes from C++, not exceptions (which can't cross the boundary)
5. **Thread safety**: The C++ functions must be reentrant for parallel analysis

---

## The Data Flow

### End-to-End: Position → Explanation

```
1. User provides FEN string
   │
   ▼
2. Python calls C++ search_position(fen, depth=15)
   │  Returns: best_move="Ne5", score=+89, PV="Ne5 Nfd7 Nxd7"
   │
   ▼
3. Python calls C++ extract_features(fen_before)
   │  Returns: {Knight_Outpost: 0, King_Safety: -20, Mobility: 15, ...}
   │
   ▼
4. Python applies the move to get fen_after
   │
   ▼
5. Python calls C++ extract_features(fen_after)
   │  Returns: {Knight_Outpost: 45, King_Safety: -55, Mobility: 28, ...}
   │
   ▼
6. Python computes deltas: {Knight_Outpost: +45, King_Safety: -35, Mobility: +13, ...}
   │
   ▼
7. Python builds JSON report with primary/secondary drivers
   │
   ▼
8. Python sends JSON to LLM via Groq API
   │  System prompt: "You are a Grandmaster chess commentator..."
   │
   ▼
9. LLM returns: "Ne5 plants the knight on a powerful outpost..."
   │
   ▼
10. Python validates explanation against delta data (optional)
    │
    ▼
11. Return explanation to user
```

Total latency: ~160ms (1ms C++ + 5ms Python + 150ms LLM + 4ms validation)

---

## Why Not Other Integration Approaches?

| Approach | Pros | Cons | Verdict |
|---|---|---|---|
| **Ctypes** | Simple, no build deps, fast | Manual type mapping |  Best for our case |
| **Cython** | Python-like syntax, fast | Build complexity, version coupling | Overkill |
| **PyBind11** | Full C++ interop | Build complexity, ABI fragility | Overkill |
| **gRPC** | Language-agnostic, scalable | Network overhead, complexity | Overkill |
| **Subprocess** | Simple | IPC overhead (pipe/JSON), slow | Too slow |
| **Shared memory** | Fast | Complex synchronization | Only for large data |

Ctypes is the sweet spot: simple enough to implement in a day, fast enough for our latency requirements, and stable across C++ compiler versions.

---

## Extending the Architecture

### Adding New Rules

1. Write the rule in C++ (see [[Declarative Rule Engine with Bitboards]])
2. Add it to the feature extraction function
3. The Python delta pipeline automatically picks it up (it processes all features)
4. Update the LLM system prompt with the new rule's description

### Adding New NLG Methods

1. Implement in Python (no C++ changes needed)
2. The JSON report format is stable—any NLG method can consume it
3. See [[Template-Based vs LLM-Based Generation]] for options

### Adding New Training Methods

1. The PyTorch tuning framework is pure Python
2. Weights are exported to C++ via a header file
3. No ABI changes needed—just recompile the C++ engine with new weights

---

## Connections

- **Next**: [[C++ Python Interfacing via Ctypes]] — The ABI boundary in detail
- **Related**: [[Declarative Rule Engine with Bitboards]] — The C++ rule engine
- **Related**: [[The Verbalization Pipeline]] — The complete data flow
- **Upstream**: [[NLG for Chess Analysis Overview]] — Why we need Python
- **Upstream**: [[The Tuning Problem]] — Why we need C++ speed
- **Downstream**: [[Combining Stockfish with Explanations]] — Alternative architecture
