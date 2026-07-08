# Combining Stockfish with Explanations

> **Chapter 12 — Neuro-Symbolic Integration** | ← [[The Verbalization Pipeline]] | Return to [[Neuro-Symbolic Architecture Overview]]

---

## The Stockfish Problem

Stockfish is the strongest chess engine in the world. It consistently dominates the Top Chess Engine Championship (TCEC) and is the engine used by virtually all online chess platforms. It would be ideal to provide explanations for Stockfish's moves—but Stockfish uses **NNUE** (Efficiently Updatable Neural Network), which is fundamentally opaque.

### Why Stockfish Can't Explain Itself

| Aspect | Stockfish (NNUE) | Our Rule Engine |
|---|---|---|
| Evaluation method | Neural network inference | Heuristic rule scoring |
| Interpretability |  Opaque |  Transparent |
| Strength | 3600+ Elo | ~2500 Elo |
| Speed | ~100M nps | ~2M nps |
| Explainability |  Impossible |  Built-in |

The NNUE network takes a position encoding as input and outputs a single scalar. There is no way to decompose this scalar into human-meaningful components. You can't ask "how much did king safety contribute?" because the answer is distributed across millions of neural network weights in a way that defies human interpretation.

This is the central paradox: **the strongest engine is the least explainable**.

---

## The Solution: Explanation Layer ON TOP of Stockfish

Instead of trying to make Stockfish explain itself, we build an **explanation layer** that sits on top of Stockfish:

```
┌─────────────────────────────────────────────────────────┐
│                  Explanation Layer                       │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ Rule Engine  │  │  Delta       │  │  LLM          │ │
│  │ (Surrogate)  │  │  Pipeline    │  │  Narrator     │ │
│  └──────┬──────┘  └──────┬───────┘  └───────┬───────┘ │
│         │                │                   │         │
└─────────┼────────────────┼───────────────────┼─────────┘
          │                │                   │
          ▼                ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│                    Stockfish                             │
│                                                         │
│  Provides: best move, evaluation, PV, multi-PV lines    │
│  Does NOT provide: why that move is best                │
└─────────────────────────────────────────────────────────┘
```

Stockfish provides **what** to play. Our explanation layer provides **why**.

---

## The Surrogate Model Approach

### Concept

A **surrogate model** is a simpler, interpretable model that approximates the behavior of a complex, opaque model. In our case:

- **Complex model**: Stockfish's NNUE evaluation
- **Surrogate model**: Our rule-based evaluation
- **Goal**: The surrogate should produce the same *move selections* as Stockfish, even if the absolute evaluations differ

### The Key Insight

We don't need the surrogate to produce the same numerical evaluation as Stockfish. We only need it to **agree on the best move**. If Stockfish says Ne5 is best, and our rule engine also says Ne5 is best (possibly for different numerical reasons), then our rule engine's explanation is a valid explanation for why Ne5 is good.

### Mathematical Formulation

Given a position $P$ and a set of candidate moves $\{m_1, m_2, \ldots, m_k\}$:

- Stockfish selects: $m^* = \arg\max_{m} \text{Eval}_{\text{SF}}(P, m)$
- Surrogate selects: $\hat{m} = \arg\max_{m} \text{Eval}_{\text{Rule}}(P, m)$
- **Agreement**: $\hat{m} = m^*$

The **surrogate fidelity** is the fraction of positions where the surrogate agrees with Stockfish:

$$F_{\text{surrogate}} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\hat{m}_i = m_i^*]$$

A fidelity of 0.80 means the surrogate agrees with Stockfish on 80% of positions. The explanations for those 80% are trustworthy; the 20% where they disagree require additional care.

---

## Implementation: Post-Hoc Rationalization Architecture

### The Architecture

```python
import chess
import chess.engine
from typing import List, Optional, Tuple

class StockfishExplainer:
    """Explains Stockfish's moves using a surrogate rule engine."""

    def __init__(self, stockfish_path: str, engine_lib_path: str,
                 weights_path: str):
        """Initialize with both Stockfish and our rule engine.

        Args:
            stockfish_path: Path to Stockfish binary
            engine_lib_path: Path to our rule engine shared library
            weights_path: Path to rule engine weights
        """
        # Start Stockfish process
        self.sf = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.sf.configure({"Threads": 4, "Hash": 1024})

        # Load our rule engine
        self.rule_engine = ChessEngine(engine_lib_path, weights_path)

        # Narrator for NLG
        self.narrator = LLMNarrator()

    def explain_move(self, fen: str, depth: int = 20,
                      multipv: int = 3) -> dict:
        """Get Stockfish's move and explain it using the rule engine.

        Args:
            fen: Position FEN string
            depth: Stockfish search depth
            multipv: Number of alternative moves to analyze

        Returns:
            Explanation dict
        """
        board = chess.Board(fen)

        # Step 1: Get Stockfish's analysis (multi-PV)
        sf_analysis = self.sf.analyse(
            board,
            chess.engine.Limit(depth=depth),
            multipv=multipv
        )

        best_move = sf_analysis[0]["move"].san()
        best_score = sf_analysis[0]["score"].white().score()

        # Step 2: Apply the best move and get FEN after
        board_after = board.copy()
        board_after.push(sf_analysis[0]["move"])
        fen_after = board_after.fen()

        # Step 3: Extract features using our rule engine
        features_before = self.rule_engine.extract_features(fen)
        features_after = self.rule_engine.extract_features(fen_after)

        # Step 4: Compute deltas
        deltas = self._compute_deltas(features_before, features_after)

        # Step 5: Check surrogate agreement
        rule_best_move = self._get_rule_engine_best_move(fen)
        agrees_with_sf = (rule_best_move == sf_analysis[0]["move"].uci())

        # Step 6: Build report with agreement metadata
        report = self._build_report(
            fen, best_move, best_score, deltas,
            agrees_with_sf=agrees_with_sf,
            alternatives=sf_analysis[1:]
        )

        # Step 7: Generate explanation
        if agrees_with_sf:
            explanation = self.narrator.narrate(report)
        else:
            # Surrogate disagrees — use caution in explanation
            explanation = self._generate_cautious_explanation(
                report, rule_best_move
            )

        return {
            "move": best_move,
            "score_cp": best_score,
            "explanation": explanation,
            "surrogate_agrees": agrees_with_sf,
            "rule_engine_choice": rule_best_move,
            "stockfish_analysis": [
                {
                    "move": info["move"].san(),
                    "score": info["score"].white().score(),
                }
                for info in sf_analysis
            ],
            "delta_report": report,
        }

    def _get_rule_engine_best_move(self, fen: str) -> str:
        """Get our rule engine's best move for a position."""
        try:
            score, pv = self.rule_engine.search(fen, depth=10)
            return pv.split()[0] if pv else "none"
        except Exception:
            return "error"

    def _generate_cautious_explanation(self, report: dict,
                                        rule_choice: str) -> str:
        """Generate an explanation when surrogate and Stockfish disagree.

        This produces a more hedged explanation, acknowledging that
        our rule engine might not capture Stockfish's reasoning.
        """
        sf_move = report["move"]

        prompt = f"""Stockfish recommends {sf_move}, but the rule-based
engine would have preferred {rule_choice}. The rule engine identifies the
following factors for {sf_move}:

{json.dumps(report['positive_deltas'][:4], indent=2)}

However, since the rule engine disagrees with Stockfish, there may be
important tactical or strategic factors that the rules don't capture.

Based on the available data, provide a cautious explanation for {sf_move}
that acknowledges the limitations of the rule-based analysis. Use phrases
like "appears to" and "may be related to" rather than definitive statements.
Keep it to 2-3 sentences."""

        return self.narrator.narrate_with_custom_prompt(prompt)
```

---

## Mapping Stockfish's Evaluation to Human Concepts

### The Evaluation Decomposition Challenge

Stockfish outputs a single score like `+1.73`. We can try to decompose this into human concepts by comparing how the evaluation changes across different positions:

```python
class EvaluationMapper:
    """Maps Stockfish evaluation changes to human concepts."""

    def decompose_evaluation(self, fen: str, move_san: str,
                              sf_engine) -> dict:
        """Decompose Stockfish's evaluation change into conceptual components.

        Instead of reading Stockfish's internal representation (which is opaque),
        we observe how the evaluation changes when we modify the position
        in conceptually meaningful ways.
        """
        board = chess.Board(fen)
        eval_before = self._sf_eval(board, sf_engine)

        # Apply the move
        move = board.parse_san(move_san)
        board.push(move)
        eval_after = self._sf_eval(board, sf_engine)

        total_delta = eval_after - eval_before

        # Concept probing: remove specific features and see how eval changes
        components = {}

        # Material component
        board_no_material_change = chess.Board(fen)
        # (This is a simplified example; actual implementation would
        #  need to carefully construct control positions)
        material_delta = self._probe_material(fen, move_san, sf_engine)
        components["material"] = material_delta

        # King safety component (remove pieces near the king)
        king_delta = self._probe_king_safety(fen, move_san, sf_engine)
        components["king_safety"] = king_delta

        # Mobility component (count legal moves before/after)
        mobility_before = len(list(board_no_material_change.legal_moves))
        mobility_after = len(list(board.legal_moves))
        components["mobility_change"] = mobility_after - mobility_before

        return {
            "total_delta": total_delta,
            "components": components,
            "unexplained": total_delta - sum(
                v for v in components.values()
                if isinstance(v, (int, float))
            )
        }
```

### The Limitation

This probing approach is **approximate** and **expensive** (multiple Stockfish evaluations per move). It's a research direction, not a production solution. The surrogate model approach (using our rule engine) is more practical because it provides exact decompositions by construction.

---

## Training the Surrogate to Match Stockfish

### The Alignment Problem

Our rule engine was trained on human game outcomes via [[Texel Tuning Method]]. But Stockfish doesn't play like a human—it plays much better. The rule engine's move selection might disagree with Stockfish's on 30-40% of positions.

### Improving Agreement

We can **fine-tune** the rule engine's weights to maximize agreement with Stockfish:

```python
class SurrogateTrainer:
    """Train the rule engine to agree with Stockfish on move selection."""

    def __init__(self, rule_engine, stockfish_engine):
        self.rule_engine = rule_engine
        self.sf = stockfish_engine

    def generate_training_data(self, positions: List[str],
                                depth: int = 15) -> List[dict]:
        """Generate training pairs: position → Stockfish's best move."""
        training_data = []

        for fen in positions:
            board = chess.Board(fen)

            # Get Stockfish's evaluation for all legal moves
            move_evals = []
            for move in board.legal_moves:
                board.push(move)
                score = self._sf_eval(board, depth)
                board.pop()
                move_evals.append({
                    "move": move.uci(),
                    "score": score,
                })

            # The best move is the target
            best = max(move_evals, key=lambda x: x["score"])

            # Extract features for the position
            features = self.rule_engine.extract_features(fen)

            training_data.append({
                "fen": fen,
                "features": features,
                "best_move": best["move"],
                "move_evals": move_evals,
            })

        return training_data

    def train_with_pairwise_loss(self, training_data, n_epochs=50):
        """Train using pairwise ranking loss.

        For each position, we want the rule engine to score the
        Stockfish-preferred move higher than all alternatives.
        """
        # Pairwise hinge loss:
        # Loss = max(0, margin - (S(best) - S(alternative)))
        MARGIN = 25  # centipawns

        for epoch in range(n_epochs):
            total_loss = 0.0
            correct = 0

            for sample in training_data:
                fen = sample["fen"]
                best_move = sample["best_move"]

                # Get rule engine's evaluation for each candidate move
                move_scores = {}
                board = chess.Board(fen)
                for move in board.legal_moves:
                    board.push(move)
                    fen_after = board.fen()
                    features_after = self.rule_engine.extract_features(
                        fen_after
                    )
                    score = self._compute_eval(features_after)
                    move_scores[move.uci()] = score
                    board.pop()

                # Check agreement
                rule_best = max(move_scores, key=move_scores.get)
                if rule_best == best_move:
                    correct += 1

                # Compute pairwise loss
                best_score = move_scores[best_move]
                for alt_move, alt_score in move_scores.items():
                    if alt_move == best_move:
                        continue
                    loss = max(0, MARGIN - (best_score - alt_score))
                    total_loss += loss

            agreement = correct / len(training_data)
            print(f"Epoch {epoch}: agreement={agreement:.1%}, "
                  f"loss={total_loss:.0f}")
```

---

## The Confidence Framework

When the surrogate agrees with Stockfish, we can be confident in the explanation. When it disagrees, we must be honest about the limitation.

### Confidence Levels

```python
class ExplanationConfidence:
    """Assigns confidence levels to explanations based on surrogate agreement."""

    @staticmethod
    def assess(surrogate_agrees: bool,
               surrogate_score_gap: int,
               stockfish_score_gap: int) -> dict:
        """Assess confidence in the explanation.

        Args:
            surrogate_agrees: Whether rule engine agrees with Stockfish
            surrogate_score_gap: How much better the chosen move is
                                  according to the rule engine (cp)
            stockfish_score_gap: How much better the chosen move is
                                  according to Stockfish (cp)

        Returns:
            Confidence assessment
        """
        if surrogate_agrees:
            if surrogate_score_gap > 50:
                level = "HIGH"
                description = "The rule engine strongly agrees with Stockfish"
            elif surrogate_score_gap > 20:
                level = "MEDIUM-HIGH"
                description = "The rule engine agrees with Stockfish"
            else:
                level = "MEDIUM"
                description = (
                    "The rule engine agrees but the margin is thin; "
                    "other factors may be involved"
                )
        else:
            if stockfish_score_gap > 100:
                level = "LOW"
                description = (
                    "Stockfish sees something the rules don't capture; "
                    "likely a tactical nuance"
                )
            else:
                level = "MEDIUM-LOW"
                description = (
                    "The rule engine disagrees, but Stockfish's "
                    "preference is marginal"
                )

        return {
            "level": level,
            "description": description,
            "surrogate_agrees": surrogate_agrees,
            "surrogate_gap_cp": surrogate_score_gap,
            "stockfish_gap_cp": stockfish_score_gap,
        }
```

### Adding Confidence to Explanations

```python
def format_explanation_with_confidence(explanation: str,
                                        confidence: dict) -> str:
    """Add confidence metadata to the explanation."""
    if confidence["level"] in ("HIGH", "MEDIUM-HIGH"):
        return explanation
    elif confidence["level"] == "MEDIUM":
        return f"{explanation} (The engine's analysis suggests this, though other factors may also be relevant.)"
    elif confidence["level"] == "MEDIUM-LOW":
        return f"The position suggests that {explanation.lower()} However, the strongest engine sees additional subtleties beyond what the rules capture."
    else:  # LOW
        return f"While positional factors suggest {explanation.lower()}, there appears to be a tactical element that the rule-based analysis doesn't fully capture. Stockfish's choice may be based on concrete variations rather than general principles."
```

---

## Future Directions

### 1. NNUE Feature Attribution

Recent research in neural network interpretability (Integrated Gradients, SHAP values) could potentially be applied to NNUE. If we can identify which input features (piece placements) contribute most to the NNUE output, we can map those back to human concepts.

### 2. Hybrid NNUE + Rules Evaluation

A modified Stockfish could use NNUE for the primary evaluation but also compute rule-based features in parallel. This would give us both the strength of NNUE and the explainability of rules, at the cost of some additional computation.

### 3. Move-Level Surrogate Training

Instead of training on game outcomes, train the surrogate to predict Stockfish's move rankings directly. This maximizes agreement but may sacrifice the independence of the rule-based evaluation.

### 4. Interactive Explanations

Allow the user to ask follow-up questions: "Why not Nf3 instead?" "What about the kingside attack?" The LLM can answer these using both the rule engine data and Stockfish's multi-PV analysis.

### 5. Explanation Databases

Pre-compute explanations for all common opening positions and store them in a database. This eliminates latency for the most common use case and allows human expert review of explanations before they're shown.

---

## Connections

- **Previous**: [[The Verbalization Pipeline]] — The pipeline this extends
- **Upstream**: [[Neuro-Symbolic Architecture Overview]] — The overall architecture
- **Related**: [[Texel Tuning Method]] — How the surrogate's weights are trained
- **Related**: [[Explanation Quality Metrics]] — Especially the faithfulness metric
- **Related**: [[LLM Narrator Architecture]] — The LLM that generates explanations
- **Related**: [[C++ Python Interfacing via Ctypes]] — The interface used to communicate with both engines
