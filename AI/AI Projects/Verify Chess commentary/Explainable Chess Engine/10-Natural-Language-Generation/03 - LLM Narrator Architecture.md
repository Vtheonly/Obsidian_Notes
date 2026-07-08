# LLM Narrator Architecture

> **Chapter 10 — Natural Language Generation** | ← [[The Heuristic Delta Pipeline]] | → [[Template-Based vs LLM-Based Generation]]

---

## Why LLMs for Chess Narration?

The [[The Heuristic Delta Pipeline|delta pipeline]] produces structured, numerical data. But numbers are not explanations. We need a system that can:

1. **Weave multiple rule deltas into a coherent narrative** — not just list them
2. **Adjust language complexity** for different audiences
3. **Handle the combinatorial explosion** of rule interactions (see [[NLG for Chess Analysis Overview]])
4. **Use chess-specific idioms** ("light-square weakness," "pawn roller," "king in a box")

Large Language Models (LLMs) are uniquely suited for this because they have been trained on millions of pages of chess commentary, books, and analysis. They already *know* how chess experts talk. What they don't know is the **ground truth** of what the engine actually computed—which is exactly what our delta pipeline provides.

---

## The Hybrid Principle: Rules Provide Truth, LLMs Provide Language

### Why LLMs Alone Are Insufficient

If you give an LLM a FEN string and ask "why is Ne5 the best move?", it will often:

- **Hallucinate board positions**: Claim a piece is on a square where it isn't
- **Invent tactical lines**: Describe continuations that don't exist
- **Miss strategic nuances**: Overlook subtle positional factors the engine detected
- **Produce plausible but wrong explanations**: Sound confident while being incorrect

This is the fundamental problem with pure LLM chess analysis: **fluency without fidelity**.

### Why Rules Alone Are Insufficient

If you use only the rule deltas with templates (see [[Template-Based vs LLM-Based Generation]]), you get:

- **Factual accuracy**: Every statement is grounded in engine data
- **Stilted language**: "Knight_Outpost delta is +45 centipawns" is not how humans talk
- **No narrative flow**: A list of deltas doesn't form a coherent paragraph
- **No audience adaptation**: Templates produce the same output regardless of reader

This is the problem with pure symbolic generation: **fidelity without fluency**.

### The Hybrid Solution

Our architecture combines the best of both:

| Component | Provides | Guarantees |
|---|---|---|
| Rule Engine (Symbolic) | Factual deltas | Fidelity |
| LLM (Neural) | Natural language | Fluency |
| JSON Payload (Interface) | Structured context | Faithfulness |

The rule engine constrains the LLM's output to only state things that are true according to the deltas. The LLM's job is **translation**, not **reasoning**.

---

## The JSON Payload

The LLM receives a carefully structured JSON payload that contains everything it needs and nothing it doesn't:

```json
{
  "move": "Ne5",
  "position_before": {
    "fen": "r1bqkbnr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq",
    "material_balance": 0,
    "phase": "opening"
  },
  "position_after": {
    "fen": "r1bqkbnr/pppp1ppp/2n5/2b1p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq",
    "material_balance": 0,
    "phase": "opening"
  },
  "primary_driver": {
    "rule": "Knight_Outpost",
    "delta": 45,
    "description": "Knight occupies a supported outpost on e5, protected by the d4 pawn"
  },
  "secondary_drivers": [
    {
      "rule": "King_Safety_Opponent",
      "delta": -35,
      "description": "Opponent king safety decreased: knight attacks f7 near the king"
    },
    {
      "rule": "Mobility",
      "delta": 13,
      "description": "Knight on e5 controls 8 squares vs 5 squares on f3"
    },
    {
      "rule": "Center_Control",
      "delta": 12,
      "description": "e5 is a central outpost increasing center influence"
    }
  ],
  "negative_deltas": [],
  "move_classification": "improving",
  "evaluation_before": "+0.35",
  "evaluation_after": "+0.89"
}
```

### Payload Design Principles

1. **Include descriptions, not just names**: The `"description"` field gives the LLM semantic context about what each rule means, reducing the chance of misinterpretation.
2. **Include evaluation context**: The eval before/after helps the LLM understand the move's overall impact.
3. **Include position phase**: Opening, middlegame, and endgame explanations use very different language.
4. **Omit irrelevant data**: Only significant deltas are included (above the threshold from [[The Heuristic Delta Pipeline]]).

---

## System Prompt Design

The system prompt is the most critical component. It must:

1. Establish the LLM's **role** as a chess commentator
2. Constrain it to **only use provided data**
3. Define the **output format**
4. Set the **audience level**

```python
SYSTEM_PROMPT = """You are a Grandmaster-level chess commentator providing analysis for \
an explainable chess engine. Your job is to convert structured engine data into clear, \
insightful chess commentary.

CRITICAL RULES:
1. ONLY state facts that are supported by the provided delta data. Do NOT invent, \
   speculate, or hallucinate any board positions, piece placements, or tactical lines.
2. Every claim you make must be traceable to a specific rule delta in the payload.
3. Do NOT describe continuations or variations unless they are explicitly included \
   in the payload.
4. Use standard chess terminology: outpost, weak square, open file, pawn chain, \
   kingside attack, etc.
5. Weave the primary driver and secondary drivers into a coherent narrative — do NOT \
   simply list them.
6. If there are negative deltas (trade-offs), mention them honestly.
7. Keep the explanation to 2-4 sentences unless the position is complex.
8. Do NOT begin with "The move" or "This move" — start directly with the strategic content.

AUDIENCE: Intermediate chess players (rating ~1500-1800 Elo). Use chess terminology \
but explain non-obvious concepts.

EXAMPLE OUTPUT:
"Ne5 plants the knight on a powerful outpost, protected by the d4 pawn. From e5, \
the knight dominates the center and pressures the vulnerable f7 square near Black's \
king, creating the foundation for a kingside attack."
"""
```

### Prompt Engineering for Different Audiences

```python
AUDIENCE_PROMPTS = {
    "beginner": """AUDIENCE: Beginner chess players (rating ~800-1200 Elo). Avoid jargon. \
Explain every concept in plain language. Use analogies where helpful. For example, say \
"the knight is in a strong position that can't easily be attacked" instead of "outpost." """,

    "intermediate": """AUDIENCE: Intermediate chess players (rating ~1500-1800 Elo). \
Use standard chess terminology but explain non-obvious concepts.""",

    "advanced": """AUDIENCE: Advanced chess players (rating ~2000+ Elo). Use precise \
chess terminology freely. Be concise. Mention subtle positional nuances.""",

    "grandmaster": """AUDIENCE: Grandmaster level. Be extremely concise (1-2 sentences). \
Use shorthand: "e5 outpost," "dark-square weakness," "pawn break." No explanations \
of basic concepts."""
}
```

---

## Full Python Code Using Groq API

Groq provides ultra-fast LLM inference, which is essential for real-time chess commentary:

```python
import json
import os
from groq import Groq
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NarrationConfig:
    """Configuration for the LLM narrator."""
    model: str = "llama-3.1-70b-versatile"
    max_tokens: int = 300
    temperature: float = 0.3  # Low temperature for factual consistency
    audience: str = "intermediate"  # beginner, intermediate, advanced, grandmaster
    include_negative_deltas: bool = True
    max_sentences: int = 4


class LLMNarrator:
    """Converts structured delta reports into natural language using an LLM."""

    def __init__(self, config: Optional[NarrationConfig] = None):
        self.config = config or NarrationConfig()
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Assemble the system prompt with audience-specific instructions."""
        base = SYSTEM_PROMPT  # defined above
        audience_addition = AUDIENCE_PROMPTS.get(
            self.config.audience, AUDIENCE_PROMPTS["intermediate"]
        )
        return f"{base}\n\n{audience_addition}"

    def narrate(self, delta_report: dict) -> str:
        """Generate a natural language explanation for a chess move.

        Args:
            delta_report: The structured report from DeltaPipeline.build_delta_report()

        Returns:
            A natural language explanation string.
        """
        user_prompt = self._build_user_prompt(delta_report)

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
        )

        return response.choices[0].message.content.strip()

    def _build_user_prompt(self, report: dict) -> str:
        """Build the user prompt from the delta report."""
        payload_json = json.dumps(report, indent=2)

        prompt = f"""Explain the chess move {report['move']} using ONLY the data below.

PRIMARY STRATEGIC DRIVER: {report['primary_driver']}

STRUCTURED DATA:
{payload_json}

Provide a clear, insightful explanation in 2-4 sentences."""

        if not self.config.include_negative_deltas:
            prompt += "\n\nFocus only on the positive aspects of the move."

        return prompt

    def narrate_with_alternatives(self, delta_report: dict,
                                   alternative_moves: List[dict]) -> str:
        """Generate an explanation that also discusses why alternatives were rejected.

        Args:
            delta_report: The main move's delta report
            alternative_moves: List of delta reports for alternative moves

        Returns:
            A more detailed explanation comparing the chosen move with alternatives.
        """
        main_explanation = self.narrate(delta_report)

        alt_descriptions = []
        for alt in alternative_moves[:2]:  # Limit to top 2 alternatives
            alt_driver = alt["primary_driver"]
            alt_eval = alt.get("evaluation_after", "unknown")
            alt_descriptions.append(
                f"- {alt['move']}: primary driver is {alt_driver}, "
                f"evaluation {alt_eval}"
            )

        comparison_prompt = f"""The engine chose {delta_report['move']} over these alternatives:
{chr(10).join(alt_descriptions)}

The explanation for the chosen move is: {main_explanation}

In 1-2 additional sentences, briefly explain why the chosen move is better than \
the alternatives, based on the data."""

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": comparison_prompt}
            ],
            max_tokens=200,
            temperature=0.3,
        )

        comparison = response.choices[0].message.content.strip()
        return f"{main_explanation} {comparison}"


# --- Usage Example ---

def main():
    from delta_pipeline import DeltaPipeline  # from [[The Heuristic Delta Pipeline]]

    pipeline = DeltaPipeline("./libchess_engine.so")
    narrator = LLMNarrator(NarrationConfig(audience="intermediate"))

    fen_before = "r1bqkbnr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
    fen_after  = "r1bqkbnr/pppp1ppp/2n5/2b1p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4"

    report = pipeline.build_delta_report(fen_before, fen_after, "Ne5")
    explanation = narrator.narrate(report)

    print(f"Move: {report['move']}")
    print(f"Primary driver: {report['primary_driver']}")
    print(f"Explanation: {explanation}")


if __name__ == "__main__":
    main()
```

---

## Handling Edge Cases

### Prophylactic Moves (No Positive Deltas)

When a move has no significant positive deltas, the LLM prompt is modified:

```python
def _build_user_prompt(self, report: dict) -> str:
    if report["primary_driver"] == "None":
        return f"""Explain the chess move {report['move']}. This appears to be a \
defensive or prophylactic move — there are no significant positive rule deltas. \
The move likely prevents an opponent threat or maintains the position.

NEGATIVE DELTAS AVOIDED (opponent threats neutralized):
{json.dumps(report.get('negative_deltas', []), indent=2)}

Provide a brief explanation (1-2 sentences)."""
    # ... normal prompt building
```

### Positions with Many Active Rules

For complex middlegame positions with 8+ significant deltas, we truncate the payload:

```python
def _truncate_report(self, report: dict, max_drivers: int = 5) -> dict:
    """Limit the report to the most significant drivers to avoid LLM confusion."""
    truncated = report.copy()
    truncated["positive_deltas"] = report["positive_deltas"][:max_drivers]
    truncated["secondary_drivers"] = report["secondary_drivers"][:max_drivers - 1]
    return truncated
```

### Hallucination Detection

We can post-process the LLM's output to check for potential hallucinations:

```python
def validate_explanation(explanation: str, delta_report: dict) -> dict:
    """Check if the explanation is consistent with the delta data."""
    mentioned_rules = []
    for delta in delta_report["positive_deltas"] + delta_report["negative_deltas"]:
        # Check if the rule name or its description keywords appear
        keywords = delta["rule"].lower().replace("_", " ").split()
        if any(kw in explanation.lower() for kw in keywords):
            mentioned_rules.append(delta["rule"])

    significant_rules = [
        d["rule"] for d in delta_report["positive_deltas"] + delta_report["negative_deltas"]
    ]

    return {
        "mentioned_rules": mentioned_rules,
        "missing_rules": [r for r in significant_rules if r not in mentioned_rules],
        "faithfulness_score": len(mentioned_rules) / max(len(significant_rules), 1)
    }
```

---

## Performance Considerations

| Component | Latency | Notes |
|---|---|---|
| C++ feature extraction | ~1ms | Negligible |
| Python delta computation | ~5ms | List processing |
| Groq LLM inference (Llama 3.1 70B) | ~150ms | Fast inference |
| Total pipeline | ~160ms | Real-time capable |

For comparison, a typical chess engine search takes 1-10 seconds, so the narration adds minimal overhead. See [[The Verbalization Pipeline]] for the complete end-to-end flow.

---

## Connections

- **Previous**: [[The Heuristic Delta Pipeline]] — Produces the data fed to the LLM
- **Next**: [[Template-Based vs LLM-Based Generation]] — When to use templates vs LLMs
- **Related**: [[Explanation Quality Metrics]] — Evaluating LLM output quality
- **Architecture**: [[Neuro-Symbolic Architecture Overview]] — The broader hybrid design
- **Related**: [[The Verbalization Pipeline]] — The complete end-to-end flow
