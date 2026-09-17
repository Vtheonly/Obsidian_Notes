---
tags: [structured-generation, scoring]
---

# Structural Scoring

> **Definition.** *Structural scoring* assigns a score to a candidate structured output based on how well it satisfies structural properties.

## What Is Scored

- **Validity**: is the structure well-formed? (binary)
- **Consistency**: do parts agree with each other? (continuous)
- **Plausibility**: does the structure match the data distribution? (continuous)
- **Constraint satisfaction**: how many hard constraints are satisfied? (count)

## Components

A typical structural score is:

$$S(\hat y) = \alpha \cdot \text{validity}(\hat y) + \beta \cdot \text{consistency}(\hat y) + \gamma \cdot \text{plausibility}(\hat y) + \delta \cdot \text{constraints}(\hat y)$$

where $\alpha, \beta, \gamma, \delta$ are weights.

## Use in Decoding

- **Reranking**: generate $k$ candidates, score each, pick the best.
- **Beam search**: prune beams with low structural scores.
- **MCTS**: use structural score as the rollout value.
- **Loss-augmented decoding**: in structured SVM, add $\Delta(\hat y, y)$ to the score to find the best wrong structure.

## Related Concepts

- [[Structured Loss]]
- [[Constrained Decoding]]
- [[Tree Search and Beam Search]]
