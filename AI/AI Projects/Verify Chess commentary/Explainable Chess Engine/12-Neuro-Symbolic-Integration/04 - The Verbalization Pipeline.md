# The Verbalization Pipeline

> **Chapter 12 — Neuro-Symbolic Integration** | ← [[Declarative Rule Engine with Bitboards]] | → [[Combining Stockfish with Explanations]]

---

## The Complete Flow

The verbalization pipeline is the end-to-end system that takes a chess position and produces a natural language explanation for the engine's chosen move. It stitches together every component from the [[Neuro-Symbolic Architecture Overview|architecture]]:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  C++     │    │  C++     │    │  Python  │    │  Python  │    │  LLM     │
│  Engine  │───│  Feature │───│  Delta   │───│  JSON    │───│  Natural │
│  Search  │    │  Extract │    │  Compute │    │  Report  │    │  Language│
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
   Step 1          Step 2          Step 3          Step 4          Step 5
```

Each stage has a specific responsibility and produces a well-defined output. Let's examine each in detail.

---

## Stage 1: C++ Engine Selects Best Move

The C++ search engine performs alpha-beta search with the [[Declarative Rule Engine with Bitboards|rule-based evaluation]] and selects the best move.

### C++ Code

```cpp
// In the C++ search engine
SearchResult SearchEngine::search(const Position& root_pos, int depth) {
    SearchResult best;

    // Alpha-beta search with move ordering
    for (int d = 1; d <= depth; d++) {
        auto result = alpha_beta(root_pos, d,
                                  -INF_SCORE, INF_SCORE, root_pos.side_to_move);

        if (result.score != TIMEOUT_SCORE) {
            best = result;
        }

        // Time management: stop if we've used too much time
        if (clock.elapsed() > time_limit / 2) break;
    }

    return best;  // Contains: move, score, PV
}
```

### Output

```cpp
struct SearchResult {
    Move best_move;       // e.g., "Ne5" in internal representation
    int score;            // e.g., +89 centipawns
    std::vector<Move> pv; // Principal variation
};
```

---

## Stage 2: C++ Extracts Features (Before and After Move)

Before and after applying the best move, the engine extracts all heuristic features using the [[Declarative Rule Engine with Bitboards|bitboard rule engine]].

### C++ Feature Extraction Function

```cpp
// The main feature extraction function called from Python
extern "C" int extract_features(const char* fen,
                                 CFeature* buffer,
                                 int capacity) {
    Position pos = Position::from_fen(fen);
    auto features = g_engine->get_rule_engine().extract_all(pos);

    int count = std::min((int)features.size(), capacity);
    for (int i = 0; i < count; i++) {
        std::strncpy(buffer[i].name, features[i].name.c_str(), 63);
        buffer[i].name[63] = '\0';
        buffer[i].value = features[i].score;
    }

    return count;
}
```

### Combined Search + Feature Extraction

For efficiency, we combine the search and feature extraction into a single Python-callable function:

```cpp
extern "C" int search_and_extract(
    const char* fen,
    int depth,
    char* best_move_san,    // Output: best move in SAN
    int* score,             // Output: evaluation score
    char* pv_buffer,        // Output: principal variation
    int pv_size,
    CFeature* features_before,  // Output: features before move
    CFeature* features_after,   // Output: features after move
    int feature_capacity
) {
    Position pos = Position::from_fen(fen);

    // Step 1: Extract features BEFORE
    auto before = g_engine->get_rule_engine().extract_all(pos);

    // Step 2: Search
    auto result = g_engine->search(pos, depth);
    *score = result.score;

    // Step 3: Apply best move and extract features AFTER
    Position pos_after = pos;
    pos_after.make_move(result.best_move);
    auto after = g_engine->get_rule_engine().extract_all(pos_after);

    // Write outputs
    std::string san = result.best_move.to_san(pos);
    std::strncpy(best_move_san, san.c_str(), 7);
    best_move_san[7] = '\0';

    // Write PV
    std::string pv_str;
    Position pv_pos = pos;
    for (size_t i = 0; i < result.pv.size(); i++) {
        if (i > 0) pv_str += " ";
        pv_str += result.pv[i].to_san(pv_pos);
        pv_pos.make_move(result.pv[i]);
    }
    std::strncpy(pv_buffer, pv_str.c_str(), pv_size - 1);
    pv_buffer[pv_size - 1] = '\0';

    // Write features before
    int count_before = std::min((int)before.size(), feature_capacity);
    for (int i = 0; i < count_before; i++) {
        std::strncpy(features_before[i].name, before[i].name.c_str(), 63);
        features_before[i].name[63] = '\0';
        features_before[i].value = before[i].score;
    }

    // Write features after
    int count_after = std::min((int)after.size(), feature_capacity);
    for (int i = 0; i < count_after; i++) {
        std::strncpy(features_after[i].name, after[i].name.c_str(), 63);
        features_after[i].name[63] = '\0';
        features_after[i].value = after[i].score;
    }

    return count_after;
}
```

---

## Stage 3: Python Computes Deltas

The Python layer receives the feature vectors and computes the deltas as described in [[The Heuristic Delta Pipeline]].

### Python Delta Computation

```python
class VerbalizationPipeline:
    """Complete pipeline from position to natural language explanation."""

    SIGNIFICANCE_THRESHOLD = 10  # centipawns

    def __init__(self, engine_lib_path: str, weights_path: str):
        self.engine = ChessEngine(engine_lib_path, weights_path)

    def compute_deltas(self, features_before: list,
                        features_after: list) -> list:
        """Compute rule deltas from before/after feature vectors.

        Args:
            features_before: List of {name, value} dicts
            features_after: List of {name, value} dicts

        Returns:
            List of delta dicts sorted by magnitude
        """
        # Create lookup for fast access
        before_map = {f["name"]: f["value"] for f in features_before}
        after_map  = {f["name"]: f["value"] for f in features_after}

        # Compute deltas for all rules
        deltas = []
        all_rules = set(before_map.keys()) | set(after_map.keys())

        for rule in all_rules:
            before_val = before_map.get(rule, 0)
            after_val = after_map.get(rule, 0)
            delta = after_val - before_val

            deltas.append({
                "rule": rule,
                "before": before_val,
                "after": after_val,
                "delta": delta,
                "magnitude": abs(delta),
                "is_significant": abs(delta) >= self.SIGNIFICANCE_THRESHOLD,
                "is_positive": delta > 0,
                "is_negative": delta < 0,
            })

        # Sort by magnitude (descending)
        deltas.sort(key=lambda d: d["magnitude"], reverse=True)

        return deltas
```

---

## Stage 4: Python Constructs JSON Report

The deltas are structured into a JSON report that the LLM can consume.

### Python Report Construction

```python
    def build_report(self, fen: str, best_move: str, score: int,
                      pv: str, deltas: list) -> dict:
        """Build the structured JSON report for the LLM.

        Args:
            fen: Position FEN before the move
            best_move: Best move in SAN notation
            score: Evaluation score in centipawns
            pv: Principal variation as string
            deltas: Computed rule deltas

        Returns:
            Structured report dict
        """
        # Separate significant deltas
        significant = [d for d in deltas if d["is_significant"]]
        positive = [d for d in significant if d["is_positive"]]
        negative = [d for d in significant if d["is_negative"]]

        # Identify primary and secondary drivers
        primary_driver = "None"
        if positive:
            primary_driver = positive[0]["rule"]

        secondary_drivers = [d["rule"] for d in positive[1:4]]  # Top 3

        # Classify the move intent
        intent = self._classify_intent(positive, negative)

        # Determine game phase
        phase = self._determine_phase(fen)

        # Rule descriptions for the LLM
        rule_descriptions = self._get_rule_descriptions(
            significant
        )

        report = {
            "move": best_move,
            "evaluation": {
                "score_cp": score,
                "score_pawns": round(score / 100, 2),
                "principal_variation": pv,
            },
            "position": {
                "fen_before": fen,
                "phase": phase,
            },
            "strategic_analysis": {
                "primary_driver": primary_driver,
                "primary_driver_delta": (
                    positive[0]["delta"] if positive else 0
                ),
                "secondary_drivers": secondary_drivers,
                "move_intent": intent,
            },
            "positive_deltas": [
                {
                    "rule": d["rule"],
                    "delta": d["delta"],
                    "before": d["before"],
                    "after": d["after"],
                    "description": rule_descriptions.get(d["rule"], ""),
                }
                for d in positive[:6]  # Limit to top 6
            ],
            "negative_deltas": [
                {
                    "rule": d["rule"],
                    "delta": d["delta"],
                    "before": d["before"],
                    "after": d["after"],
                    "description": rule_descriptions.get(d["rule"], ""),
                }
                for d in negative[:3]  # Limit to top 3
            ],
        }

        return report

    def _classify_intent(self, positive: list,
                          negative: list) -> str:
        """Classify the strategic intent of the move."""
        if not positive and not negative:
            return "neutral"
        if not positive and negative:
            return "defensive"
        if positive and negative:
            return "trade_off"
        return "improving"

    def _determine_phase(self, fen: str) -> str:
        """Determine the game phase from the FEN."""
        parts = fen.split()
        board = parts[0]

        # Count pieces
        queens = board.count('q') + board.count('Q')
        rooks = board.count('r') + board.count('R')
        minors = (board.count('b') + board.count('B') +
                  board.count('n') + board.count('N'))

        if queens == 0 and rooks <= 1:
            return "endgame"
        elif queens > 0 or (rooks >= 2 and minors >= 2):
            return "middlegame"
        else:
            return "opening"

    def _get_rule_descriptions(self, deltas: list) -> dict:
        """Get human-readable descriptions for active rules."""
        DESCRIPTIONS = {
            "Knight_Outpost": (
                "Knight occupies a square that cannot be attacked by "
                "enemy pawns, typically supported by a friendly pawn"
            ),
            "King_Safety": (
                "The overall safety of the king, considering pawn "
                "shield, open files, and attacking pieces nearby"
            ),
            "King_Safety_Opponent": (
                "The safety of the opponent's king — negative delta "
                "means their king became less safe"
            ),
            "Mobility": (
                "The number of legal moves available, indicating "
                "piece activity and freedom"
            ),
            "Center_Control": (
                "Influence over the central squares d4, d5, e4, e5"
            ),
            "Passed_Pawn": (
                "A pawn with no enemy pawns ahead on the same or "
                "adjacent files, threatening promotion"
            ),
            "Rook_Open_File": (
                "A rook positioned on a file with no pawns, giving "
                "it maximum activity along that file"
            ),
            "Bishop_Pair": (
                "Having both bishops, which complement each other "
                "by covering both light and dark squares"
            ),
            "Pawn_Structure": (
                "The overall quality of the pawn formation, "
                "including chains, islands, and weaknesses"
            ),
            "Knight_On_Rim": (
                "A knight on the edge of the board (a/h file or "
                "1st/8th rank), where it controls fewer squares"
            ),
        }
        return DESCRIPTIONS
```

---

## Stage 5: LLM Generates Natural Language

The final stage sends the JSON report to the LLM using the [[LLM Narrator Architecture]].

### Python Prompt Construction and LLM Call

```python
    def generate_explanation(self, report: dict,
                              audience: str = "intermediate",
                              model: str = "llama-3.1-70b-versatile"
                              ) -> str:
        """Generate a natural language explanation using the LLM.

        Args:
            report: The structured delta report
            audience: Target audience level
            model: LLM model to use

        Returns:
            Natural language explanation
        """
        narrator = LLMNarrator(NarrationConfig(
            model=model,
            audience=audience,
            temperature=0.3,
            max_tokens=300,
        ))

        return narrator.narrate(report)
```

---

## Complete Pipeline: Putting It All Together

```python
class VerbalizationPipeline:
    """Complete pipeline: Position → Natural Language Explanation."""

    def __init__(self, engine_lib_path: str, weights_path: str,
                 audience: str = "intermediate"):
        self.engine = ChessEngine(engine_lib_path, weights_path)
        self.audience = audience
        self.narrator = LLMNarrator(NarrationConfig(audience=audience))

    def analyze(self, fen: str, depth: int = 15) -> dict:
        """Analyze a position and generate a full explanation.

        Args:
            fen: FEN string of the position to analyze
            depth: Search depth

        Returns:
            Complete analysis with explanation
        """
        # Step 1: Search + Feature Extraction (C++)
        score, pv = self.engine.search(fen, depth)
        features_before = self.engine.extract_features(fen)

        # Step 2: Determine the best move and apply it
        # (The PV gives us the best move)
        best_move = pv.split()[0] if pv else "???"
        fen_after = self._apply_move(fen, best_move)
        features_after = self.engine.extract_features(fen_after)

        # Step 3: Compute deltas (Python)
        deltas = self.compute_deltas(features_before, features_after)

        # Step 4: Build JSON report (Python)
        report = self.build_report(fen, best_move, score, pv, deltas)

        # Step 5: Generate explanation (LLM)
        explanation = self.narrator.narrate(report)

        # Step 6: Validate explanation (Python)
        validation = self._validate_explanation(explanation, report)

        return {
            "fen": fen,
            "best_move": best_move,
            "score_cp": score,
            "score_pawns": round(score / 100, 2),
            "pv": pv,
            "primary_driver": report["strategic_analysis"]["primary_driver"],
            "secondary_drivers": report["strategic_analysis"]["secondary_drivers"],
            "explanation": explanation,
            "validation": validation,
            "delta_report": report,
        }

    def analyze_game(self, pgn_path: str, depth: int = 15
                      ) -> list:
        """Analyze every move in a game.

        Args:
            pgn_path: Path to a PGN file
            depth: Search depth for each position

        Returns:
            List of analysis results, one per move
        """
        import chess.pgn

        results = []
        with open(pgn_path) as f:
            game = chess.pgn.read_game(f)

        board = game.board()
        for move in game.mainline_moves():
            fen = board.fen()
            analysis = self.analyze(fen, depth)
            analysis["actual_move"] = move.uci()
            results.append(analysis)
            board.push(move)

        return results

    def _apply_move(self, fen: str, move_san: str) -> str:
        """Apply a move to a position and return the new FEN."""
        import chess
        board = chess.Board(fen)
        move = board.parse_san(move_san)
        board.push(move)
        return board.fen()

    def _validate_explanation(self, explanation: str,
                               report: dict) -> dict:
        """Quick validation of the generated explanation."""
        from explanation_quality import ExplanationFactChecker

        checker = ExplanationFactChecker()
        result = checker.check(explanation, report)

        return {
            "accuracy_score": result.accuracy_score,
            "verified_claims": result.verified_claims,
            "contradicted_claims": result.contradicted_claims,
            "unverifiable_claims": result.unverifiable_claims,
        }
```

---

## Performance Profile

### Latency Breakdown

| Stage | Component | Time | Percentage |
|---|---|---|---|
| 1 | C++ search (depth 15) | 2,000ms | 92.6% |
| 2 | C++ feature extraction (2×) | 2ms | 0.1% |
| 3 | Python delta computation | 5ms | 0.2% |
| 4 | Python JSON construction | 1ms | 0.0% |
| 5 | LLM generation (Groq) | 150ms | 7.0% |
| **Total** | | **2,158ms** | **100%** |

The search dominates. The verbalization overhead is only ~160ms (7.3%), which is negligible compared to the search time.

### Optimization Opportunities

1. **Parallel search + feature extraction**: Extract features for the root position while searching
2. **Cache feature vectors**: If the same position appears again (transposition), reuse features
3. **Streaming LLM output**: Start displaying the explanation as it's generated
4. **Batch LLM calls**: For game analysis, batch multiple moves into a single LLM call

---

## Error Handling

```python
class VerbalizationError(Exception):
    """Base exception for verbalization pipeline errors."""

class SearchError(VerbalizationError):
    """The C++ search failed."""

class FeatureExtractionError(VerbalizationError):
    """Feature extraction failed."""

class LLMError(VerbalizationError):
    """The LLM call failed."""

class Pipeline:
    """Pipeline with robust error handling."""

    def analyze(self, fen: str, depth: int = 15) -> dict:
        """Analyze with fallback on errors."""
        try:
            score, pv = self.engine.search(fen, depth)
        except Exception as e:
            raise SearchError(f"Search failed: {e}")

        try:
            features_before = self.engine.extract_features(fen)
        except Exception as e:
            raise FeatureExtractionError(
                f"Feature extraction (before) failed: {e}"
            )

        # ... rest of pipeline with try/except at each stage

        try:
            explanation = self.narrator.narrate(report)
        except Exception as e:
            # Fallback to template-based explanation
            explanation = self.template_gen.generate(report, {})
            explanation += f" [Note: LLM unavailable, using template]"

        return {
            # ... results with explanation
        }
```

---

## Connections

- **Previous**: [[Declarative Rule Engine with Bitboards]] — Stage 2 implementation
- **Next**: [[Combining Stockfish with Explanations]] — Using Stockfish instead of our engine
- **Upstream**: [[The Heuristic Delta Pipeline]] — Stage 3 in detail
- **Upstream**: [[LLM Narrator Architecture]] — Stage 5 in detail
- **Upstream**: [[C++ Python Interfacing via Ctypes]] — The interface between stages
- **Related**: [[Explanation Quality Metrics]] — Validating the final output
