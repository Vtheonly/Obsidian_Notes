---
tags: [structured-generation, output-space]
---

# Structured Output Spaces

> **Definition.** The *structured output space* is the set of all valid outputs for a structured prediction task. It is typically much smaller than the set of all possible token sequences.

## Example

For the task "generate a syntactically valid JSON object", the structured output space is the set of all strings parseable as JSON. The set of all token sequences is much larger — most sequences are not valid JSON.

## Why It Matters

- A model that ignores the structure can produce outputs *outside* the structured space (invalid JSON, invalid AST, invalid BIM).
- A model that respects the structure produces only outputs *inside* the space.

## Mechanisms for Respecting Structure

- **Soft**: loss shaping to penalize invalid outputs.
- **Constraint**: grammar mask, schema validator.
- **Architecture**: tree/graph decoder that emits only valid structures.
- **Post-hoc**: validator that rejects invalid outputs.

See [[Constrained Decoding]], [[Structural Constraints]], [[Hard Guarantees vs Statistical Preferences]].

## Tractability

Even when the structured space is much smaller than the full sequence space, it is usually still exponentially large. Decoding requires heuristics:

- greedy,
- beam search,
- constrained beam search,
- Monte Carlo tree search (MCTS),
- branch-and-bound.

See [[Tree Search and Beam Search]], [[Backtracking Search]].

## Related Concepts

- [[Structured Prediction]]
- [[Constrained Decoding]]
- [[Hard Guarantees vs Statistical Preferences]]
