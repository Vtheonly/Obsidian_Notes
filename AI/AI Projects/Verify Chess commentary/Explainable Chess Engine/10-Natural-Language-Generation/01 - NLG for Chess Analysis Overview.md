# NLG for Chess Analysis Overview

> **Chapter 10 — Natural Language Generation** | [[The Heuristic Delta Pipeline]] → [[LLM Narrator Architecture]] → [[Template-Based vs LLM-Based Generation]] → [[Explanation Quality Metrics]]

---

## The Communication Gap

A chess engine that outputs `+1.73` tells you *what* the evaluation is, but it tells you nothing about *why*. The score is a single scalar—a lossy compression of hundreds of positional and tactical factors into one number. For a human to understand the engine's reasoning, we must decompose that scalar back into the factors that produced it and then translate those factors into language.

This is the **Natural Language Generation (NLG)** problem for chess: converting structured, numerical reasoning into fluent, human-readable explanations.

### The Fundamental Tension

| What the Engine Knows | What the Human Needs |
|---|---|
| `Material score: +127cp` | "White has an extra pawn" |
| `King safety: -45cp` | "Black's king is exposed on the open g-file" |
| `Mobility delta: +23cp` | "The knight relocation gains access to five key squares" |
| `Passed pawn: +89cp` | "The protected passed pawn on d6 is decisive" |

The engine thinks in **centipawns and bitboards**. The human thinks in **plans, threats, and pawn structures**. NLG is the bridge between these two worlds.

---

## What is NLG in the Context of Chess?

Natural Language Generation is a subfield of computational linguistics concerned with producing coherent text from non-linguistic data. In our chess context, NLG takes the following inputs:

1. **Rule activation scores** — numerical values for each heuristic rule (material, king safety, pawn structure, etc.)
2. **Delta scores** — the *change* in each rule's value caused by a specific move
3. **Position context** — the board state before and after the move
4. **Strategic classification** — which rules are dominant, which are secondary

And produces:

> *"Ne5! forces the exchange of the dark-squared bishop, weakening Black's king on the dark squares. The knight now controls d7 and f7, and the weakened dark-square complex around Black's king creates lasting strategic problems."*

### Why NLG is Hard for Chess

Chess explanations are not simple one-to-one mappings from scores to text. Consider:

- **Rule interactions**: A knight move might simultaneously improve mobility, attack the king, and create an outpost. The explanation must weave these together coherently.
- **Negation**: Sometimes the most important fact is what a move *prevents* (prophylaxis). "Preventing ...c5" is harder to generate than "Playing ...c5."
- **Audience calibration**: A 1200-rated player needs different language than a 2400-rated player. "Double attack on f7 and h7" vs. "The queen creates a mating net."
- **Anaphora and coherence**: Multi-sentence explanations need pronoun resolution, logical connectors ("therefore," "however," "moreover"), and narrative flow.

---

## The Gap Between Rule Scores and Human Language

### The Score → Language Mapping Problem

Each rule in our [[Declarative Rule Engine with Bitboards|rule engine]] produces a centipawn score. But centipawns are not meaning. Consider three scenarios where the **King Safety** rule outputs `-60cp`:

| Scenario | Board Context | Human Explanation |
|---|---|---|
| A | Open file, rook aiming at king | "The open f-file gives White a devastating attack" |
| B | Diagonal, bishop aiming at king | "The dark-square weaknesses around the king are terminal" |
| C | Pawn storm, pawns advancing | "The pawn avalanche is unstoppable" |

Same score, three completely different explanations. The score alone is insufficient; we need the **structural context** that produced it.

### The Combinatorial Explosion

With 200+ rules and many possible interaction patterns, template-based approaches face a combinatorial explosion. If we have $n$ active rules per move, the number of possible combinations is:

$$C = \sum_{k=1}^{n} \binom{n}{k} = 2^n - 1$$

For $n = 10$ active rules (typical for a complex middlegame position), that's $2^{10} - 1 = 1023$ possible combinations. Writing templates for each is infeasible. This is why we need a **generation** approach, not a **template lookup** approach.

---

## The NLG Pipeline: Rules → Deltas → JSON → LLM → Language

Our pipeline transforms raw engine data into natural language through five stages:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  C++ Engine  │────│   Feature    │────│    Delta     │────│  JSON Report │────│  LLM/NLG     │
│  Evaluates   │     │  Extraction  │     │  Computation │     │  Constructor │     │  Generator   │
│  Position    │     │  (Before/    │     │  After-      │     │  (Structured │     │  (Natural    │
│              │     │   After)     │     │  Before      │     │   Payload)   │     │   Language)  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Stage 1: C++ Engine Evaluates Position

The engine performs its search and selects the best move. During evaluation, each heuristic rule fires and produces a centipawn contribution. See [[Declarative Rule Engine with Bitboards]] for implementation details.

### Stage 2: Feature Extraction (Before/After)

Before the move is applied, we snapshot all rule scores. After the move is applied, we snapshot again. This gives us two vectors:

$$\mathbf{S}_{before} = [s_1^{before}, s_2^{before}, \ldots, s_n^{before}]$$
$$\mathbf{S}_{after} = [s_1^{after}, s_2^{after}, \ldots, s_n^{after}]$$

### Stage 3: Delta Computation

The delta vector captures the *change* caused by the move:

$$\Delta = \mathbf{S}_{after} - \mathbf{S}_{before} = [\Delta_1, \Delta_2, \ldots, \Delta_n]$$

Where $\Delta_i = s_i^{after} - s_i^{before}$ for each rule $i$.

The dominant positive delta identifies the **primary strategic driver** of the move. See [[The Heuristic Delta Pipeline]] for full implementation.

### Stage 4: JSON Report Construction

The deltas are packaged into a structured JSON payload containing:

```json
{
  "move": "Ne5",
  "position_fen_before": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
  "position_fen_after": "r1bqk2r/pppp1ppp/2n2n2/2b1p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4",
  "deltas": [
    {"rule": "Knight_Outpost", "before": 0, "after": 45, "delta": 45},
    {"rule": "King_Safety_Opponent", "before": -20, "after": -55, "delta": -35},
    {"rule": "Mobility", "before": 15, "after": 28, "delta": 13}
  ],
  "primary_driver": "Knight_Outpost",
  "secondary_drivers": ["King_Safety_Opponent", "Mobility"]
}
```

### Stage 5: LLM/NLG Generation

The JSON payload is sent to a language model with a carefully designed system prompt. The LLM converts the structured data into fluent, natural language. See [[LLM Narrator Architecture]] for the full implementation.

---

## Why This Architecture Works

### Ground Truth from Rules

The rule engine provides **ground truth**. Every statement in the generated explanation can be traced back to a specific rule delta. This prevents hallucination—unlike asking an LLM to "explain this chess move" with only a FEN string, our system gives the LLM verified data.

### Flexibility from Language Models

The LLM provides **flexibility**. It can handle the combinatorial explosion of rule combinations, adjust language for different audiences, and produce coherent multi-sentence narratives. This is something rigid templates cannot do.

### The Hybrid Advantage

This architecture represents a **neuro-symbolic hybrid**:

- The **symbolic** component (rule engine) guarantees factual correctness
- The **neural** component (LLM) guarantees linguistic fluency
- The **interface** (JSON deltas) connects them

Neither component alone can produce faithful, fluent explanations. Together, they can. See [[Neuro-Symbolic Architecture Overview]] for the broader architectural vision.

---

## Historical Context

Traditional chess engines (Fritz, Houdini, early Stockfish) provided only numerical evaluations. The first major attempt at chess explanation was the **"Natural Language"** feature in ChessBase, which used simple templates like "White stands better due to the pawn on d5." These were often stilted and incomplete.

The explainability problem became *worse* with NNUE and deep learning engines, because the neural network is fundamentally opaque. Our approach—building a symbolic rule engine *alongside* the search—represents a return to interpretable evaluation, but enhanced with modern NLG techniques.

---

## Connections

- **Next**: [[The Heuristic Delta Pipeline]] — Full implementation of the delta computation pipeline
- **Related**: [[LLM Narrator Architecture]] — How LLMs convert deltas to language
- **Related**: [[Template-Based vs LLM-Based Generation]] — Trade-offs between approaches
- **Related**: [[Explanation Quality Metrics]] — How to evaluate generated explanations
- **Upstream**: [[Declarative Rule Engine with Bitboards]] — The rule engine that produces the scores
- **Architecture**: [[Neuro-Symbolic Architecture Overview]] — The overall system design
