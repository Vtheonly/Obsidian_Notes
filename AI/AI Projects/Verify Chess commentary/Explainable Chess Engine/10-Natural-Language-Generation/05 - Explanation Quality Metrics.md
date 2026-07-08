# Explanation Quality Metrics

> **Chapter 10 — Natural Language Generation** | ← [[Template-Based vs LLM-Based Generation]] | Return to [[NLG for Chess Analysis Overview]]

---

## Why Measure Explanation Quality?

An explainable chess engine is only as good as its explanations. A system that produces verbose but inaccurate commentary is worse than one that says nothing. We need rigorous, quantitative metrics to evaluate whether our generated explanations actually explain the engine's reasoning.

The challenge is that "explanation quality" is multi-dimensional. A good explanation must be:

1. **Factually accurate** — it tells the truth about the position
2. **Complete** — it mentions all significant factors
3. **Concise** — it doesn't ramble
4. **Faithful** — it reflects the engine's actual reasoning, not a post-hoc rationalization
5. **Audience-appropriate** — it uses language the reader can understand

Each dimension requires different evaluation methods.

---

## Dimension 1: Factual Accuracy

### Definition

**Factual accuracy** measures whether every statement in the explanation is consistent with the actual board state and the rule deltas from the [[The Heuristic Delta Pipeline|delta pipeline]].

### The Fact-Checking Pipeline

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class FactCheckResult:
    """Result of fact-checking an explanation against engine data."""
    total_claims: int
    verified_claims: int
    contradicted_claims: int
    unverifiable_claims: int
    accuracy_score: float  # verified / (verified + contradicted)
    details: List[dict]


class ExplanationFactChecker:
    """Verifies factual accuracy of generated explanations."""

    # Mapping from rule names to keywords that should appear in explanations
    RULE_KEYWORDS = {
        "Knight_Outpost": ["outpost", "knight", "supported", "protected"],
        "King_Safety": ["king safety", "exposed king", "king position",
                        "shelter", "king attack"],
        "King_Safety_Opponent": ["opponent king", "attack", "threat",
                                  "exposed"],
        "Mobility": ["mobility", "activity", "active", "squares",
                     "piece activity"],
        "Passed_Pawn": ["passed pawn", "advance", "promotion",
                        "queening"],
        "Rook_Open_File": ["open file", "rook", "file control",
                           "rook lift"],
        "Bishop_Pair": ["bishop pair", "two bishops", "bishop advantage"],
        "Pawn_Structure": ["pawn structure", "pawn chain", "pawn island",
                           "pawn weakness"],
        "Center_Control": ["center", "central", "center control",
                           "central squares"],
        "Material": ["material", "piece advantage", "extra piece",
                     "exchange"],
        "Knight_On_Rim": ["rim", "edge", "side", "knight on the rim"],
        "Bad_Bishop": ["bad bishop", "blocked bishop", "hemmed in"],
        "Weak_Squares": ["weak square", "hole", "outpost for opponent"],
        "Space": ["space", "space advantage", "territory"],
        "Threats": ["threat", "attack", "target", "pressure"],
        "Connectivity": ["coordination", "pieces work together",
                         "harmony"],
        "King_Protection": ["king protection", "shield", "pawn cover"],
    }

    # Claims that would be UNVERIFIABLE from delta data alone
    UNVERIFIABLE_PATTERNS = [
        "will", "could", "might", "threatens to",
        "plans to", "intends to", "next move"
    ]

    def check(self, explanation: str,
              delta_report: dict) -> FactCheckResult:
        """Check an explanation against engine data for factual accuracy."""
        claims = self._extract_claims(explanation)
        verified = 0
        contradicted = 0
        unverifiable = 0
        details = []

        significant_rules = self._get_significant_rules(delta_report)

        for claim in claims:
            result = self._verify_claim(claim, significant_rules)
            details.append(result)

            if result["status"] == "verified":
                verified += 1
            elif result["status"] == "contradicted":
                contradicted += 1
            else:
                unverifiable += 1

        denom = max(verified + contradicted, 1)
        accuracy = verified / denom

        return FactCheckResult(
            total_claims=len(claims),
            verified_claims=verified,
            contradicted_claims=contradicted,
            unverifiable_claims=unverifiable,
            accuracy_score=accuracy,
            details=details
        )

    def _extract_claims(self, text: str) -> List[str]:
        """Split explanation into individual claims (sentences)."""
        sentences = [s.strip() for s in text.split('.')
                     if s.strip()]
        return sentences

    def _verify_claim(self, claim: str,
                      significant_rules: dict) -> dict:
        """Verify a single claim against the delta data."""
        claim_lower = claim.lower()

        # Check for unverifiable claims (future predictions)
        for pattern in self.UNVERIFIABLE_PATTERNS:
            if pattern in claim_lower:
                return {
                    "claim": claim,
                    "status": "unverifiable",
                    "reason": f"Contains future prediction: '{pattern}'"
                }

        # Check if claim matches any significant rule
        matched_rules = []
        for rule, delta_info in significant_rules.items():
            keywords = self.RULE_KEYWORDS.get(rule, [rule.lower()])
            if any(kw in claim_lower for kw in keywords):
                matched_rules.append((rule, delta_info))

        if matched_rules:
            # Verify the claim's direction matches the delta
            for rule, delta_info in matched_rules:
                delta = delta_info["delta"]
                # Positive claim about a negative delta = contradiction
                if delta < 0 and any(w in claim_lower
                                      for w in ["improves", "strengthens",
                                                "powerful", "strong"]):
                    return {
                        "claim": claim,
                        "status": "contradicted",
                        "reason": f"Positive language about {rule} but delta is {delta}"
                    }
                # Negative claim about a positive delta = contradiction
                if delta > 0 and any(w in claim_lower
                                      for w in ["weakens", "worsens",
                                                "poor", "bad"]):
                    return {
                        "claim": claim,
                        "status": "contradicted",
                        "reason": f"Negative language about {rule} but delta is +{delta}"
                    }

            return {
                "claim": claim,
                "status": "verified",
                "matched_rules": [r[0] for r in matched_rules]
            }

        # No matching rule found — could be a hallucinated claim
        return {
            "claim": claim,
            "status": "unverifiable",
            "reason": "No matching rule delta found for this claim"
        }

    def _get_significant_rules(self, report: dict) -> dict:
        """Get all rules with significant deltas."""
        rules = {}
        for delta in report.get("positive_deltas", []):
            rules[delta["rule"]] = delta
        for delta in report.get("negative_deltas", []):
            rules[delta["rule"]] = delta
        return rules
```

---

## Dimension 2: Completeness

### Definition

**Completeness** measures whether the explanation mentions all significant rule deltas. A complete explanation should cover every rule with a delta above the significance threshold.

### Completeness Score

$$\text{Completeness} = \frac{|\{R : R \in \text{Significant} \land R \in \text{Mentioned}\}|}{|\{R : R \in \text{Significant}\}|}$$

Where:
- $\text{Significant}$ = set of rules with $|\Delta_R| > \theta$ (threshold, typically 10cp)
- $\text{Mentioned}$ = set of rules whose keywords appear in the explanation

```python
class CompletenessEvaluator:
    """Evaluates how complete an explanation is."""

    def __init__(self, significance_threshold: int = 10):
        self.threshold = significance_threshold

    def evaluate(self, explanation: str, delta_report: dict) -> dict:
        """Compute completeness metrics."""
        significant_rules = [
            d for d in delta_report["positive_deltas"] + delta_report.get("negative_deltas", [])
            if abs(d["delta"]) >= self.threshold
        ]

        mentioned = []
        missed = []

        for delta in significant_rules:
            rule_name = delta["rule"]
            keywords = ExplanationFactChecker.RULE_KEYWORDS.get(
                rule_name, [rule_name.replace("_", " ").lower()]
            )

            if any(kw in explanation.lower() for kw in keywords):
                mentioned.append(rule_name)
            else:
                missed.append({
                    "rule": rule_name,
                    "delta": delta["delta"]
                })

        completeness = len(mentioned) / max(len(significant_rules), 1)

        # Weighted completeness: weight by delta magnitude
        total_magnitude = sum(abs(d["delta"]) for d in significant_rules)
        mentioned_magnitude = sum(
            abs(d["delta"]) for d in significant_rules
            if d["rule"] in mentioned
        )
        weighted_completeness = mentioned_magnitude / max(total_magnitude, 1)

        return {
            "completeness": completeness,
            "weighted_completeness": weighted_completeness,
            "mentioned_rules": mentioned,
            "missed_rules": missed,
            "significant_rule_count": len(significant_rules)
        }
```

---

## Dimension 3: Conciseness

### Definition

**Conciseness** measures whether the explanation is appropriately brief. Overly long explanations are as bad as overly terse ones.

### The Conciseness Curve

There's a **Goldilocks zone** for explanation length:

- Too short (< 1 sentence): Insufficient detail
- Just right (2-4 sentences): Optimal for most audiences
- Too long (> 6 sentences): Rambling, loses the reader

```python
class ConcisenessEvaluator:
    """Evaluates explanation conciseness."""

    OPTIMAL_SENTENCES = {
        "beginner": (2, 5),     # Beginners need more context
        "intermediate": (2, 4),  # Standard
        "advanced": (1, 3),     # Advanced players want brevity
        "grandmaster": (1, 2),  # Maximum conciseness
    }

    def evaluate(self, explanation: str,
                 audience: str = "intermediate") -> dict:
        """Score conciseness."""
        sentence_count = self._count_sentences(explanation)
        word_count = len(explanation.split())
        optimal_min, optimal_max = self.OPTIMAL_SENTENCES.get(
            audience, (2, 4)
        )

        # Conciseness score based on distance from optimal range
        if optimal_min <= sentence_count <= optimal_max:
            score = 1.0
        elif sentence_count < optimal_min:
            score = sentence_count / optimal_min
        else:
            # Penalty increases with distance from optimal max
            overshoot = sentence_count - optimal_max
            score = max(0.0, 1.0 - 0.2 * overshoot)

        # Information density: words per significant rule
        # (populated externally with rule count)

        return {
            "conciseness_score": score,
            "sentence_count": sentence_count,
            "word_count": word_count,
            "optimal_range": (optimal_min, optimal_max),
            "in_range": optimal_min <= sentence_count <= optimal_max
        }

    def _count_sentences(self, text: str) -> int:
        """Count sentences in text."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])
```

---

## Dimension 4: Audience Appropriateness

### Definition

**Audience appropriateness** measures whether the explanation uses language and complexity suitable for the target reader.

```python
class AudienceEvaluator:
    """Evaluates whether explanations match the target audience."""

    JARGON_LEVELS = {
        "beginner": ["check", "capture", "attack", "defend", "piece",
                      "pawn", "king", "queen", "rook", "bishop", "knight"],
        "intermediate": ["outpost", "open file", "pawn chain", "king safety",
                          "mobility", "passed pawn", "bishop pair",
                          "weak square", "double attack", "pin",
                          "skewer", "discovered attack"],
        "advanced": ["prophylaxis", "minority attack", "pawn break",
                      "opposition", "zugzwang", "reciprocal zugzwang",
                      "fortress", "shouldering", "Lucena position",
                      "Philidor position", "hyperbola", "retrograde"],
        "grandmaster": ["NNUE", "tablebase", "DPT", "scaled eval",
                          "horizon effect", "search explosion",
                          "null move pruning", "late move reduction"]
    }

    def evaluate(self, explanation: str,
                 target_audience: str = "intermediate") -> dict:
        """Check if explanation vocabulary matches audience."""
        words = explanation.lower().split()
        target_level = self._audience_to_level(target_audience)

        # Find jargon used that's above the target level
        inappropriate_jargon = []
        for level in range(target_level + 1, 4):
            level_name = ["beginner", "intermediate", "advanced",
                          "grandmaster"][level]
            for term in self.JARGON_LEVELS[level_name]:
                if term.lower() in explanation.lower():
                    inappropriate_jargon.append({
                        "term": term,
                        "level": level_name
                    })

        # Find if the explanation is too simple for the audience
        target_terms = self.JARGON_LEVELS[target_audience]
        used_target_terms = [
            t for t in target_terms if t.lower() in explanation.lower()
        ]

        appropriateness = 1.0 - (0.1 * len(inappropriate_jargon))

        return {
            "appropriateness_score": max(0.0, appropriateness),
            "inappropriate_jargon": inappropriate_jargon,
            "target_terms_used": used_target_terms,
            "target_audience": target_audience
        }

    def _audience_to_level(self, audience: str) -> int:
        mapping = {"beginner": 0, "intermediate": 1,
                   "advanced": 2, "grandmaster": 3}
        return mapping.get(audience, 1)
```

---

## Dimension 5: Explanation Faithfulness

### Definition

**Faithfulness** is the most important and most subtle metric. It measures whether the explanation reflects the engine's *actual reasoning process*, not just a plausible-sounding post-hoc rationalization.

### The Faithfulness Problem

Consider: the engine plays **Ne5**. The delta pipeline reports `Knight_Outpost: +45`. The explanation says "The knight occupies a powerful outpost." This is **faithful** if the outpost score was actually the *reason* the engine chose Ne5—that is, if removing the outpost evaluation would change the engine's choice.

But what if the engine would have chosen Ne5 *even without the outpost bonus*, because the tactical threats alone justify it? Then the explanation is **unfaithful**—it attributes the move to the outpost, but the engine's true reason was tactical.

### Faithfulness Test: Ablation

```python
class FaithfulnessEvaluator:
    """Tests whether explanations faithfully reflect engine reasoning."""

    def __init__(self, engine_lib_path: str):
        self.engine_lib = ctypes.CDLL(engine_lib_path)

    def evaluate_faithfulness(self, move: str, fen: str,
                               delta_report: dict,
                               primary_rule: str) -> dict:
        """Test faithfulness via rule ablation.

        If we remove the primary rule from the evaluation,
        does the engine still choose the same move?
        """
        # Baseline: engine's choice with all rules
        baseline_move = self._get_best_move(fen, disabled_rules=[])

        # Ablation: remove the primary rule
        ablated_move = self._get_best_move(fen, disabled_rules=[primary_rule])

        is_faithful = (baseline_move != ablated_move)

        # Also test secondary rules
        secondary_ablations = {}
        for driver in delta_report.get("secondary_drivers", []):
            ablated = self._get_best_move(fen, disabled_rules=[driver])
            secondary_ablations[driver] = (baseline_move != ablated)

        return {
            "primary_rule": primary_rule,
            "is_faithful": is_faithful,
            "baseline_move": baseline_move,
            "ablated_move": ablated_move,
            "faithfulness_score": 1.0 if is_faithful else 0.0,
            "secondary_faithfulness": secondary_ablations,
            "interpretation": (
                f"The primary rule '{primary_rule}' is "
                f"{'causally responsible' if is_faithful else 'not causally responsible'} "
                f"for the engine's choice of {move}."
            )
        }

    def _get_best_move(self, fen: str,
                        disabled_rules: List[str]) -> str:
        """Get the engine's best move with optional rule ablation."""
        # Convert disabled rules to C-compatible format
        rules_buf = (ctypes.c_char_p * len(disabled_rules))()
        for i, rule in enumerate(disabled_rules):
            rules_buf[i] = rule.encode()

        move_buf = ctypes.create_string_buffer(8)
        self.engine_lib.get_best_move_ablated(
            fen.encode(),
            rules_buf,
            len(disabled_rules),
            move_buf,
            8
        )
        return move_buf.value.decode()
```

### The Faithfulness Score

For a complete game analysis, the overall faithfulness is:

$$F = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\text{Ablating } R_{\text{primary}}^{(i)} \text{ changes the engine's choice}]$$

Where $N$ is the total number of moves analyzed and $R_{\text{primary}}^{(i)}$ is the primary driver for move $i$.

A faithfulness score of 1.0 means every explanation correctly identifies the engine's true reason. A score of 0.5 means half the explanations are post-hoc rationalizations.

---

## Composite Quality Score

All five dimensions combine into a single quality metric:

$$Q = \alpha \cdot \text{Accuracy} + \beta \cdot \text{Completeness} + \gamma \cdot \text{Conciseness} + \delta \cdot \text{Appropriateness} + \epsilon \cdot \text{Faithfulness}$$

With recommended weights:

$$\alpha = 0.30, \quad \beta = 0.20, \quad \gamma = 0.10, \quad \delta = 0.10, \quad \epsilon = 0.30$$

Note that **accuracy** and **faithfulness** receive the highest weights because they are the most critical for an explainable system.

```python
class CompositeQualityEvaluator:
    """Combines all quality dimensions into a single score."""

    WEIGHTS = {
        "accuracy": 0.30,
        "completeness": 0.20,
        "conciseness": 0.10,
        "appropriateness": 0.10,
        "faithfulness": 0.30,
    }

    def evaluate(self, explanation: str, delta_report: dict,
                 target_audience: str = "intermediate",
                 fen: str = None) -> dict:
        """Compute the composite quality score."""
        results = {}

        # Factual accuracy
        fact_checker = ExplanationFactChecker()
        accuracy_result = fact_checker.check(explanation, delta_report)
        results["accuracy"] = accuracy_result.accuracy_score

        # Completeness
        completeness_eval = CompletenessEvaluator()
        completeness_result = completeness_eval.evaluate(
            explanation, delta_report
        )
        results["completeness"] = completeness_result["completeness"]

        # Conciseness
        conciseness_eval = ConcisenessEvaluator()
        conciseness_result = conciseness_eval.evaluate(
            explanation, target_audience
        )
        results["conciseness"] = conciseness_result["conciseness_score"]

        # Audience appropriateness
        audience_eval = AudienceEvaluator()
        audience_result = audience_eval.evaluate(
            explanation, target_audience
        )
        results["appropriateness"] = audience_result["appropriateness_score"]

        # Faithfulness (requires engine ablation — may be None)
        if fen:
            faithfulness_eval = FaithfulnessEvaluator("./libchess_engine.so")
            faithfulness_result = faithfulness_eval.evaluate_faithfulness(
                delta_report["move"], fen, delta_report,
                delta_report["primary_driver"]
            )
            results["faithfulness"] = faithfulness_result["faithfulness_score"]
        else:
            results["faithfulness"] = 0.5  # Default: unknown

        # Composite score
        composite = sum(
            self.WEIGHTS[dim] * score
            for dim, score in results.items()
        )

        return {
            "composite_score": composite,
            "dimension_scores": results,
            "grade": self._score_to_grade(composite),
            "details": {
                "accuracy": accuracy_result,
                "completeness": completeness_result,
                "conciseness": conciseness_result,
                "appropriateness": audience_result,
            }
        }

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """Convert a 0-1 score to a letter grade."""
        if score >= 0.9: return "A"
        if score >= 0.8: return "B"
        if score >= 0.7: return "C"
        if score >= 0.6: return "D"
        return "F"
```

---

## Benchmarking Results

### Expected Scores by Generation Method

| Method | Accuracy | Completeness | Conciseness | Appropriateness | Faithfulness | Composite |
|---|---|---|---|---|---|---|
| Template | 1.00 | 0.75 | 0.60 | 0.50 | 0.80 | 0.79 |
| LLM (unconstrained) | 0.85 | 0.90 | 0.85 | 0.90 | 0.70 | 0.82 |
| LLM (with delta constraints) | 0.95 | 0.90 | 0.85 | 0.90 | 0.75 | 0.87 |
| Hybrid (escalation) | 0.97 | 0.88 | 0.80 | 0.85 | 0.78 | 0.86 |

The constrained LLM approach achieves the highest composite score, validating the [[LLM Narrator Architecture|hybrid architecture]] design.

---

## Connections

- **Previous**: [[Template-Based vs LLM-Based Generation]] — The methods we're evaluating
- **Related**: [[NLG for Chess Analysis Overview]] — The broader NLG context
- **Related**: [[The Heuristic Delta Pipeline]] — The data used for fact-checking
- **Related**: [[LLM Narrator Architecture]] — The LLM system being evaluated
- **Upstream**: [[The Tuning Problem]] — Rule weights affect explanation quality
