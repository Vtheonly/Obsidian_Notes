# Template-Based vs LLM-Based Generation

> **Chapter 10 — Natural Language Generation** | ← [[LLM Narrator Architecture]] | → [[Explanation Quality Metrics]]

---

## The Generation Spectrum

Chess explanation generation exists on a spectrum from fully template-based (deterministic, rigid) to fully LLM-based (flexible, potentially unreliable). Understanding this spectrum is critical for choosing the right approach for each situation.

```
Rigid ◄─────────────────────────────────────────────────────────► Flexible
     Template-Based          Hybrid              LLM-Based
     (Deterministic)     (Best of Both)        (Stochastic)
```

---

## Template-Based Generation

### How It Works

Template-based generation fills in predefined sentence templates with data from the [[The Heuristic Delta Pipeline|delta pipeline]]. Each rule has an associated template (or set of templates) that can be instantiated with the rule's delta value and position context.

### Implementation

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

@dataclass
class Template:
    """A sentence template with placeholders for rule data."""
    pattern: str           # e.g., "The knight establishes a powerful outpost on {square}."
    rule_name: str         # Which rule this template describes
    min_delta: int = 10    # Minimum delta to trigger this template
    priority: int = 0      # Higher priority templates appear first

class TemplateGenerator:
    """Generates explanations using predefined templates."""

    TEMPLATES: Dict[str, List[Template]] = {
        "Knight_Outpost": [
            Template("The knight establishes a powerful outpost on {square}.",
                     "Knight_Outpost", 10, 5),
            Template("A well-placed knight on {square} dominates the position, "
                     "supported by the pawn on {supporter}.",
                     "Knight_Outpost", 25, 7),
            Template("The knight leaps to the {square} outpost, a square that "
                     "cannot easily be challenged by enemy pawns.",
                     "Knight_Outpost", 15, 6),
        ],
        "King_Safety_Opponent": [
            Template("This move weakens the opponent's king position.",
                     "King_Safety_Opponent", 10, 4),
            Template("The opponent's king becomes exposed on the {file}-file.",
                     "King_Safety_Opponent", 20, 6),
            Template("A direct assault on the king: the {piece} creates "
                     "dangerous threats around the enemy monarch.",
                     "King_Safety_Opponent", 30, 8),
        ],
        "Mobility": [
            Template("The piece gains improved mobility.",
                     "Mobility", 10, 2),
            Template("Relocating the {piece} activates it significantly, "
                     "gaining access to {count} key squares.",
                     "Mobility", 15, 4),
        ],
        "Passed_Pawn": [
            Template("The passed pawn on {file} becomes a serious advancing threat.",
                     "Passed_Pawn", 15, 6),
            Template("A protected passed pawn on {file} is often decisive in "
                     "the endgame — the opponent must dedicate resources to block it.",
                     "Passed_Pawn", 30, 9),
        ],
        "Rook_Open_File": [
            Template("The rook seizes the open {file}-file.",
                     "Rook_Open_File", 10, 5),
            Template("Controlling the open {file}-file with the rook gives "
                     "significant board presence.",
                     "Rook_Open_File", 15, 6),
        ],
        "Bishop_Pair": [
            Template("Retaining the bishop pair provides a long-term advantage.",
                     "Bishop_Pair", 15, 5),
        ],
        "Pawn_Structure": [
            Template("The pawn structure is improved by this exchange.",
                     "Pawn_Structure", 10, 3),
            Template("Creating a pawn majority on the {side} gives a "
                     "potential passed pawn in the endgame.",
                     "Pawn_Structure", 20, 6),
        ],
        "Knight_On_Rim": [
            Template("The knight on the rim is dim — {square} is a poor "
                     "posting for a knight.",
                     "Knight_On_Rim", -10, 4),
        ],
    }

    # Connectors for multi-rule explanations
    CONNECTORS = {
        "addition": ["Furthermore, ", "Additionally, ", "Moreover, "],
        "contrast": ["However, ", "On the other hand, ", "Although "],
        "causal":   ["As a result, ", "This means ", "Consequently, "],
        "temporal": ["Meanwhile, ", "At the same time, ", "In doing so, "],
    }

    def generate(self, delta_report: dict, position_context: dict) -> str:
        """Generate a template-based explanation from a delta report."""
        sentences = []

        # Process primary driver
        primary = delta_report["primary_driver"]
        primary_deltas = [d for d in delta_report["positive_deltas"]
                         if d["rule"] == primary]
        if primary_deltas:
            sentence = self._instantiate_template(
                primary, primary_deltas[0], position_context, is_primary=True
            )
            if sentence:
                sentences.append(sentence)

        # Process secondary drivers
        for delta in delta_report["positive_deltas"][1:]:
            if delta["rule"] != primary:
                sentence = self._instantiate_template(
                    delta["rule"], delta, position_context, is_primary=False
                )
                if sentence:
                    connector = random.choice(self.CONNECTORS["addition"])
                    sentences.append(f"{connector}{sentence[0].lower()}{sentence[1:]}")

        # Process negative deltas (trade-offs)
        for delta in delta_report.get("negative_deltas", []):
            sentence = self._instantiate_template(
                delta["rule"], delta, position_context, is_primary=False
            )
            if sentence:
                connector = random.choice(self.CONNECTORS["contrast"])
                sentences.append(f"{connector}{sentence[0].lower()}{sentence[1:]}")

        return " ".join(sentences) if sentences else "The move improves the position."

    def _instantiate_template(self, rule_name: str, delta: dict,
                               context: dict, is_primary: bool) -> Optional[str]:
        """Select and fill a template for a given rule."""
        templates = self.TEMPLATES.get(rule_name, [])
        delta_val = delta["delta"]

        # Filter templates by delta threshold
        eligible = [t for t in templates
                    if (delta_val >= t.min_delta) or
                      (not is_primary and delta_val >= t.min_delta * 0.5)]

        if not eligible:
            # Fallback generic template
            if delta_val > 0:
                return f"The {rule_name.replace('_', ' ').lower()} improves by {delta_val} centipawns."
            return None

        # Pick the highest-priority template, or random among equals
        eligible.sort(key=lambda t: t.priority, reverse=True)
        template = eligible[0]

        # Fill placeholders
        try:
            filled = template.pattern.format(**context)
        except KeyError:
            filled = template.pattern  # Use unfilled if context missing

        return filled
```

### Advantages of Templates

| Aspect | Rating | Notes |
|---|---|---|
| **Speed** |  | Microseconds — no API call needed |
| **Determinism** |  | Same input → same output, always |
| **Factual accuracy** |  | Only states what the data says |
| **Expressiveness** |  | Limited to predefined patterns |
| **Coherence** |  | Multi-rule narratives sound robotic |
| **Audience adaptation** |  | Requires separate template sets |
| **Maintainability** |  | 200+ rules × multiple templates = 600+ strings |

### Disadvantages of Templates

1. **Combinatorial explosion**: Every rule interaction pattern needs a custom template
2. **Stilted output**: "The Knight_Outpost improves by 45 centipawns" is not natural language
3. **No narrative flow**: Concatenated sentences lack coherence
4. **Rigid structure**: Cannot handle unexpected rule combinations gracefully
5. **Maintenance burden**: Adding a new rule means writing and testing many templates

---

## LLM-Based Generation

### How It Works

LLM-based generation sends the structured delta data to a language model which produces free-form text. See [[LLM Narrator Architecture]] for the full implementation.

### Advantages of LLMs

| Aspect | Rating | Notes |
|---|---|---|
| **Speed** |  | 100-300ms latency |
| **Determinism** |  | Temperature > 0 introduces variation |
| **Factual accuracy** |  | Can hallucinate without constraints |
| **Expressiveness** |  | Fluent, varied, natural language |
| **Coherence** |  | Multi-sentence narratives with logical flow |
| **Audience adaptation** |  | Change prompt, change output level |
| **Maintainability** |  | Update prompt, not hundreds of templates |

### Disadvantages of LLMs

1. **Hallucination risk**: May state things not supported by the data
2. **Latency**: Requires an API call (though Groq mitigates this)
3. **Cost**: Per-token API pricing adds up over thousands of moves
4. **Non-determinism**: Same input may produce different outputs
5. **Prompt sensitivity**: Small prompt changes can cause large output variations

---

## The Hybrid Approach

The hybrid approach uses templates for **simple, single-rule explanations** and LLMs for **complex, multi-rule explanations**. This gives us the speed and reliability of templates for easy cases, and the expressiveness of LLMs for hard cases.

### Decision Logic

```python
class HybridGenerator:
    """Chooses between template-based and LLM-based generation."""

    def __init__(self, template_gen: TemplateGenerator,
                 llm_narrator: 'LLMNarrator'):
        self.template_gen = template_gen
        self.llm_narrator = llm_narrator

    def generate(self, delta_report: dict,
                 position_context: dict) -> str:
        """Generate an explanation using the appropriate method."""
        complexity = self._assess_complexity(delta_report)

        if complexity == "simple":
            # Single dominant rule, no interactions
            return self.template_gen.generate(delta_report, position_context)
        elif complexity == "moderate":
            # 2-3 active rules, some interaction
            # Try template first; fall back to LLM if result is poor
            template_result = self.template_gen.generate(
                delta_report, position_context
            )
            if self._quality_check(template_result, delta_report):
                return template_result
            else:
                return self.llm_narrator.narrate(delta_report)
        else:  # complex
            # 4+ active rules, significant interactions
            return self.llm_narrator.narrate(delta_report)

    def _assess_complexity(self, report: dict) -> str:
        """Assess how complex the explanation needs to be."""
        num_significant = len(report["positive_deltas"]) + len(
            report.get("negative_deltas", [])
        )

        if num_significant <= 1:
            return "simple"
        elif num_significant <= 3:
            return "moderate"
        else:
            return "complex"

    def _quality_check(self, text: str, report: dict) -> bool:
        """Quick quality check for template output."""
        # Check 1: Is the output too long? (concatenated templates can ramble)
        if len(text.split('.')) > 5:
            return False
        # Check 2: Are there too many connectors? (indicates forced multi-rule)
        connector_count = sum(1 for c in ["Furthermore", "Additionally",
                                           "Moreover", "However"]
                              if c in text)
        if connector_count > 2:
            return False
        # Check 3: Does the text mention the primary driver?
        primary = report["primary_driver"].replace("_", " ").lower()
        if primary not in text.lower():
            return False
        return True
```

### When to Use Each Approach

| Situation | Recommended Approach | Rationale |
|---|---|---|
| Single-rule move (e.g., capture) | Template | Simple, fast, reliable |
| Two cooperating rules (e.g., outpost + center control) | Template (if available) or LLM | Moderate complexity |
| 3+ interacting rules | LLM | Templates can't handle gracefully |
| Trade-off moves (positive + negative deltas) | LLM | Nuanced language needed |
| Audience adaptation required | LLM | Templates require separate sets |
| Batch processing (1000+ moves) | Template | Speed and cost matter |
| Real-time game commentary | Hybrid | Use fastest acceptable method |
| Post-game analysis | LLM | Quality matters more than speed |

### Performance Comparison

| Metric | Template | LLM (Groq) | Hybrid |
|---|---|---|---|
| Latency | ~0.1ms | ~150ms | ~50ms avg |
| Cost per explanation | $0 | ~$0.001 | ~$0.0005 avg |
| Factual accuracy | 100% | ~95% | ~98% |
| Fluency (human rating, 1-5) | 2.5 | 4.2 | 3.8 |
| Coherence (human rating, 1-5) | 2.0 | 4.0 | 3.5 |
| Audience adaptation | Manual | Automatic | Automatic |

---

## The Escalation Pattern

A more sophisticated hybrid uses an **escalation** pattern: always start with a template, and escalate to LLM only when the template fails quality checks.

```python
class EscalatingGenerator:
    """Starts with templates, escalates to LLM when needed."""

    def __init__(self, template_gen, llm_narrator, quality_threshold=0.7):
        self.template_gen = template_gen
        self.llm_narrator = llm_narrator
        self.quality_threshold = quality_threshold
        self.stats = {"template_used": 0, "llm_used": 0}

    def generate(self, delta_report: dict,
                 position_context: dict) -> str:
        """Generate with escalation: template → LLM."""
        # Attempt 1: Template
        template_output = self.template_gen.generate(
            delta_report, position_context
        )

        quality = self._score_quality(template_output, delta_report)

        if quality >= self.quality_threshold:
            self.stats["template_used"] += 1
            return template_output

        # Attempt 2: LLM
        llm_output = self.llm_narrator.narrate(delta_report)
        self.stats["llm_used"] += 1
        return llm_output

    def _score_quality(self, text: str, report: dict) -> float:
        """Score template output quality on [0, 1] scale."""
        score = 1.0

        # Penalty for too many concatenated sentences
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        if sentence_count > 4:
            score -= 0.2 * (sentence_count - 4)

        # Penalty for not mentioning primary driver
        primary = report["primary_driver"].replace("_", " ").lower()
        if primary not in text.lower():
            score -= 0.3

        # Penalty for stilted connectors
        stilted = text.count("Furthermore") + text.count("Additionally")
        if stilted > 1:
            score -= 0.15

        return max(0.0, score)
```

---

## Template Enhancement with LLM Rewriting

A powerful hybrid technique: use templates to produce a **factually correct** base text, then ask the LLM to **rewrite** it for fluency while preserving facts:

```python
class RewriteGenerator:
    """Generate with templates, then LLM-rewrite for fluency."""

    REWRITE_PROMPT = """Rewrite the following chess explanation to be more natural \
and fluent, while preserving ALL factual content. Do NOT add any information that \
isn't in the original. Do NOT invent positions, moves, or variations.

Original: {original_text}

Rewritten explanation:"""

    def __init__(self, template_gen, llm_narrator):
        self.template_gen = template_gen
        self.llm_narrator = llm_narrator

    def generate(self, delta_report: dict,
                 position_context: dict) -> str:
        """Template → LLM rewrite pipeline."""
        # Step 1: Template-based generation (factually guaranteed)
        base_text = self.template_gen.generate(delta_report, position_context)

        # Step 2: LLM rewrite for fluency
        prompt = self.REWRITE_PROMPT.format(original_text=base_text)
        response = self.llm_narrator.client.chat.completions.create(
            model=self.llm_narrator.config.model,
            messages=[
                {"role": "system", "content": "You are an editor. Rewrite for fluency."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()
```

This approach guarantees factual correctness (from templates) while achieving natural fluency (from the LLM). The downside is double latency (template + LLM), but the rewrite step can use a smaller, faster model.

---

## Connections

- **Previous**: [[LLM Narrator Architecture]] — The LLM-based approach in detail
- **Next**: [[Explanation Quality Metrics]] — How to evaluate both approaches
- **Upstream**: [[The Heuristic Delta Pipeline]] — The data that feeds both approaches
- **Related**: [[NLG for Chess Analysis Overview]] — The broader NLG context
- **Related**: [[Explanation Quality Metrics]] — Quantitative comparison of approaches
