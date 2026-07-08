# The Heuristic Delta Pipeline

> **Chapter 10 — Natural Language Generation** | ← [[NLG for Chess Analysis Overview]] | → [[LLM Narrator Architecture]]

---

## The Core Insight

A chess move's *purpose* is best understood not by the absolute scores it produces, but by the **changes** it causes. A knight on e5 might contribute +45cp to the position, but what matters for explanation is: *how did the position change when the knight moved there?* Was the knight previously on f3 contributing only +5cp? Then the delta is +40cp, and "occupying the outpost" is a dominant explanation.

The **Heuristic Delta Pipeline** is the mechanism that computes these changes systematically for every rule, producing a ranked list of strategic drivers that can be fed into the [[LLM Narrator Architecture|narration layer]].

---

## The Delta Formula

For each heuristic rule $R$, the delta is:

$$\Delta_R = \text{Score}_{\text{After}}(R) - \text{Score}_{\text{Before}}(R)$$

Where:
- $\text{Score}_{\text{Before}}(R)$ = the centipawn contribution of rule $R$ evaluated on the position **before** the move
- $\text{Score}_{\text{After}}(R)$ = the centipawn contribution of rule $R$ evaluated on the position **after** the move

A **positive delta** means the move improved the position according to that rule. A **negative delta** means the move worsened it. The **magnitude** of the delta indicates how important that rule was in motivating the move.

### Identifying the Primary Strategic Driver

The primary strategic driver is the rule with the largest positive delta:

$$R_{\text{primary}} = \arg\max_{R} \Delta_R \quad \text{subject to} \quad \Delta_R > 0$$

Secondary drivers are rules with positive deltas sorted in descending order, typically including all rules with $\Delta_R$ above a significance threshold (e.g., $\Delta_R > 10$ centipawns).

### Handling Negative Deltas

Negative deltas are equally important for explanation. If $\Delta_{\text{King Safety}} = -35$cp, this means the move weakened the king's position—a critical trade-off that any good explanation must mention:

> *"Ne5 occupies a powerful outpost, but it comes at the cost of momentarily weakening the f3 square, which could be exploited by ...Ng4."*

---

## The Five-Step Pipeline

### Step 1: Calculate All Heuristics BEFORE the Move

Before the move is applied, the engine evaluates the current position through every heuristic rule:

```cpp
// C++ Feature Extraction — BEFORE the move
struct HeuristicSnapshot {
    std::unordered_map<std::string, int> scores;
};

HeuristicSnapshot capture_before(const Position& pos) {
    HeuristicSnapshot snap;
    snap.scores["Material"]             = eval_material(pos);
    snap.scores["Pawn_Structure"]       = eval_pawn_structure(pos);
    snap.scores["King_Safety"]          = eval_king_safety(pos);
    snap.scores["Mobility"]             = eval_mobility(pos);
    snap.scores["Knight_Outpost"]       = eval_knight_outpost(pos);
    snap.scores["Bishop_Pair"]          = eval_bishop_pair(pos);
    snap.scores["Rook_Open_File"]       = eval_rook_open_file(pos);
    snap.scores["Passed_Pawn"]          = eval_passed_pawn(pos);
    snap.scores["Space"]                = eval_space(pos);
    snap.scores["Threats"]             = eval_threats(pos);
    snap.scores["Connectivity"]         = eval_connectivity(pos);
    snap.scores["Knight_On_Rim"]        = eval_knight_on_rim(pos);
    snap.scores["Bad_Bishop"]           = eval_bad_bishop(pos);
    snap.scores["Weak_Squares"]         = eval_weak_squares(pos);
    snap.scores["King_Protection"]      = eval_king_protection(pos);
    // ... 200+ rules total
    return snap;
}
```

Each function like `eval_knight_outpost()` returns a centipawn score for that specific rule. See [[Declarative Rule Engine with Bitboards]] for how these are implemented efficiently with bitboards.

### Step 2: Apply the Move

The move is applied to the position, producing a new board state:

```cpp
Position pos_after = pos_before;
pos_after.make_move(best_move);
```

### Step 3: Calculate All Heuristics AFTER the Move

The same evaluation functions are called on the new position:

```cpp
HeuristicSnapshot capture_after(const Position& pos) {
    // Same function as capture_before, but called on the post-move position
    HeuristicSnapshot snap;
    snap.scores["Material"]             = eval_material(pos);
    snap.scores["Pawn_Structure"]       = eval_pawn_structure(pos);
    snap.scores["King_Safety"]          = eval_king_safety(pos);
    // ... all 200+ rules
    return snap;
}
```

### Step 4: Compute Deltas

The delta for each rule is simply the difference:

```cpp
std::vector<RuleDelta> compute_deltas(
    const HeuristicSnapshot& before,
    const HeuristicSnapshot& after)
{
    std::vector<RuleDelta> deltas;

    for (const auto& [rule_name, score_after] : after.scores) {
        int score_before = before.scores.at(rule_name);
        int delta = score_after - score_before;

        deltas.push_back({
            .rule_name  = rule_name,
            .before     = score_before,
            .after      = score_after,
            .delta      = delta
        });
    }

    return deltas;
}
```

### Step 5: Sort and Identify Dominant Drivers

The deltas are sorted by magnitude, and the primary driver is identified:

```cpp
std::vector<RuleDelta> rank_deltas(std::vector<RuleDelta>& deltas) {
    // Sort by absolute delta magnitude, descending
    std::sort(deltas.begin(), deltas.end(),
        [](const RuleDelta& a, const RuleDelta& b) {
            return std::abs(a.delta) > std::abs(b.delta);
        });

    return deltas;
}

std::string identify_primary_driver(const std::vector<RuleDelta>& deltas) {
    // Find the rule with the largest positive delta
    for (const auto& d : deltas) {
        if (d.delta > 0) return d.rule_name;
    }
    return "None"; // defensive move, no positive deltas
}

std::vector<std::string> identify_secondary_drivers(
    const std::vector<RuleDelta>& deltas,
    int threshold_cp = 10)
{
    std::vector<std::string> drivers;
    bool skip_first = true; // skip primary driver

    for (const auto& d : deltas) {
        if (skip_first && d.delta > 0) { skip_first = false; continue; }
        if (d.delta > threshold_cp) {
            drivers.push_back(d.rule_name);
        }
    }
    return drivers;
}
```

---

## Full C++ Feature Extraction and Output

The engine needs to export the delta data across the ABI boundary to Python. Here's the complete C++ function:

```cpp
// feature_extractor.h
#pragma once
#include <vector>
#include <string>

extern "C" {
    // Opaque structure for passing delta data
    struct CDelta {
        char rule_name[64];
        int before;
        int after;
        int delta;
    };

    // Main extraction function
    // Returns number of deltas written to the buffer
    int extract_move_deltas(
        const char* fen_before,      // FEN string before the move
        const char* fen_after,       // FEN string after the move
        CDelta* delta_buffer,        // Output buffer for deltas
        int buffer_capacity          // Max number of deltas
    );

    // Convenience: also returns the primary driver
    void get_primary_driver(
        const char* fen_before,
        const char* fen_after,
        char* driver_buffer,         // Output: rule name
        int buffer_size
    );
}
```

```cpp
// feature_extractor.cpp
#include "feature_extractor.h"
#include "position.h"
#include "evaluation.h"
#include <cstring>
#include <algorithm>

extern "C" int extract_move_deltas(
    const char* fen_before,
    const char* fen_after,
    CDelta* delta_buffer,
    int buffer_capacity)
{
    Position pos_before = Position::from_fen(fen_before);
    Position pos_after  = Position::from_fen(fen_after);

    HeuristicSnapshot snap_before = capture_before(pos_before);
    HeuristicSnapshot snap_after  = capture_after(pos_after);

    std::vector<RuleDelta> deltas = compute_deltas(snap_before, snap_after);
    auto ranked = rank_deltas(deltas);

    int count = std::min((int)ranked.size(), buffer_capacity);
    for (int i = 0; i < count; i++) {
        std::strncpy(delta_buffer[i].rule_name,
                     ranked[i].rule_name.c_str(), 63);
        delta_buffer[i].rule_name[63] = '\0';
        delta_buffer[i].before = ranked[i].before;
        delta_buffer[i].after  = ranked[i].after;
        delta_buffer[i].delta  = ranked[i].delta;
    }

    return count;
}

extern "C" void get_primary_driver(
    const char* fen_before,
    const char* fen_after,
    char* driver_buffer,
    int buffer_size)
{
    Position pos_before = Position::from_fen(fen_before);
    Position pos_after  = Position::from_fen(fen_after);

    HeuristicSnapshot snap_before = capture_before(pos_before);
    HeuristicSnapshot snap_after  = capture_after(pos_after);

    std::vector<RuleDelta> deltas = compute_deltas(snap_before, snap_after);
    auto ranked = rank_deltas(deltas);

    std::string primary = identify_primary_driver(ranked);
    std::strncpy(driver_buffer, primary.c_str(), buffer_size - 1);
    driver_buffer[buffer_size - 1] = '\0';
}
```

---

## Full Python Delta Computation Code

On the Python side, we receive the C++ data and perform additional processing:

```python
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
import ctypes

@dataclass
class RuleDelta:
    """Represents the change in a single rule's score after a move."""
    rule_name: str
    before: int
    after: int
    delta: int

    @property
    def is_positive(self) -> bool:
        return self.delta > 0

    @property
    def is_negative(self) -> bool:
        return self.delta < 0

    @property
    def magnitude(self) -> int:
        return abs(self.delta)

    @property
    def is_significant(self, threshold: int = 10) -> bool:
        """A delta is significant if it exceeds the threshold in centipawns."""
        return self.magnitude >= threshold


class DeltaPipeline:
    """Computes heuristic deltas for a chess move using the C++ engine."""

    def __init__(self, engine_lib_path: str):
        self.lib = ctypes.CDLL(engine_lib_path)
        self._setup_signatures()

    def _setup_signatures(self):
        """Define C function signatures for ctypes."""
        self.lib.extract_move_deltas.argtypes = [
            ctypes.c_char_p,   # fen_before
            ctypes.c_char_p,   # fen_after
            ctypes.POINTER(CDeltaC),  # delta_buffer
            ctypes.c_int        # buffer_capacity
        ]
        self.lib.extract_move_deltas.restype = ctypes.c_int

        self.lib.get_primary_driver.argtypes = [
            ctypes.c_char_p,   # fen_before
            ctypes.c_char_p,   # fen_after
            ctypes.c_char_p,   # driver_buffer
            ctypes.c_int        # buffer_size
        ]
        self.lib.get_primary_driver.restype = None

    def compute_deltas(self, fen_before: str, fen_after: str,
                       significance_threshold: int = 10) -> List[RuleDelta]:
        """Compute all rule deltas for a move."""
        MAX_RULES = 256
        buffer = (CDeltaC * MAX_RULES)()

        count = self.lib.extract_move_deltas(
            fen_before.encode(),
            fen_after.encode(),
            buffer,
            MAX_RULES
        )

        deltas = []
        for i in range(count):
            delta = RuleDelta(
                rule_name=buffer[i].rule_name.decode(),
                before=buffer[i].before,
                after=buffer[i].after,
                delta=buffer[i].delta
            )
            deltas.append(delta)

        return deltas

    def get_primary_driver(self, fen_before: str, fen_after: str) -> str:
        """Get the primary strategic driver for a move."""
        buf = ctypes.create_string_buffer(64)
        self.lib.get_primary_driver(
            fen_before.encode(),
            fen_after.encode(),
            buf,
            64
        )
        return buf.value.decode()

    def build_delta_report(self, fen_before: str, fen_after: str,
                           move_san: str) -> dict:
        """Build a complete delta report for the LLM narrator."""
        deltas = self.compute_deltas(fen_before, fen_after)
        primary = self.get_primary_driver(fen_before, fen_after)

        # Filter to significant deltas only
        significant = [d for d in deltas if d.is_significant]

        # Separate positive and negative
        positive = [d for d in significant if d.is_positive]
        negative = [d for d in significant if d.is_negative]

        # Sort by magnitude
        positive.sort(key=lambda d: d.delta, reverse=True)
        negative.sort(key=lambda d: d.delta)  # most negative first

        secondary = [d.rule_name for d in positive[1:]]

        report = {
            "move": move_san,
            "position_fen_before": fen_before,
            "position_fen_after": fen_after,
            "primary_driver": primary,
            "secondary_drivers": secondary,
            "positive_deltas": [
                {"rule": d.rule_name, "delta": d.delta,
                 "before": d.before, "after": d.after}
                for d in positive
            ],
            "negative_deltas": [
                {"rule": d.rule_name, "delta": d.delta,
                 "before": d.before, "after": d.after}
                for d in negative
            ],
            "all_deltas": [
                {"rule": d.rule_name, "delta": d.delta,
                 "before": d.before, "after": d.after}
                for d in deltas
            ]
        }

        return report

    def to_json(self, report: dict) -> str:
        """Serialize the delta report to JSON for the LLM."""
        return json.dumps(report, indent=2)
```

The ctypes structure definition:

```python
class CDeltaC(ctypes.Structure):
    """C struct matching the C++ CDelta definition."""
    _fields_ = [
        ("rule_name", ctypes.c_char * 64),
        ("before", ctypes.c_int),
        ("after", ctypes.c_int),
        ("delta", ctypes.c_int),
    ]
```

---

## Example: Computing Deltas for Nf3 → Ne5

Given the Italian Game position:

```
Before: r1bqkbnr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4
After:  r1bqkbnr/pppp1ppp/2n5/2b1p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4
Move:   Ne5
```

The delta computation yields:

| Rule | Before | After | Delta | Category |
|---|---|---|---|---|
| Knight_Outpost | 0 | +45 | **+45** | Primary |
| King_Safety_Opponent | -20 | -55 | **-35** | Secondary |
| Mobility | +15 | +28 | **+13** | Secondary |
| Knight_On_Rim | 0 | 0 | 0 | — |
| Material | 0 | 0 | 0 | — |
| Center_Control | +10 | +22 | **+12** | Secondary |
| Piece_Activity | +5 | +18 | **+13** | Secondary |
| Pawn_Structure | 0 | 0 | 0 | — |

**Primary Driver**: `Knight_Outpost` (Δ = +45cp)
**Secondary Drivers**: `King_Safety_Opponent`, `Mobility`, `Piece_Activity`, `Center_Control`

This structured data is exactly what the [[LLM Narrator Architecture]] needs to generate an explanation like:

> *"Ne5 plants the knight on a powerful outpost supported by the d4 pawn. It simultaneously pressures f7 and tightens the grip on the center, while making Black's king uncomfortable."*

---

## Edge Cases

### Zero Deltas (Prophylactic Moves)

Some moves produce no positive deltas—they are purely defensive. For example, **h3** to prevent **Bg4**. The delta pipeline handles this:

```python
def classify_move_intent(report: dict) -> str:
    """Classify the move's strategic intent."""
    if not report["positive_deltas"] and report["negative_deltas"]:
        return "defensive"
    elif report["positive_deltas"] and report["negative_deltas"]:
        return "trade_off"
    elif report["positive_deltas"]:
        return "improving"
    else:
        return "neutral"  # likely prophylaxis
```

### Equal Primary Deltas

When two rules tie for the largest positive delta, we use the [[Feature Orthogonality Design|orthogonality hierarchy]] to break ties: rules higher in the taxonomy (e.g., material, king safety) take precedence over lower rules (e.g., minor piece placement).

---

## Connections

- **Previous**: [[NLG for Chess Analysis Overview]] — The broader NLG context
- **Next**: [[LLM Narrator Architecture]] — How deltas become language
- **Upstream**: [[Declarative Rule Engine with Bitboards]] — How rules are computed
- **Related**: [[C++ Python Interfacing via Ctypes]] — The ABI boundary
- **Related**: [[Explanation Quality Metrics]] — Evaluating delta-based explanations
