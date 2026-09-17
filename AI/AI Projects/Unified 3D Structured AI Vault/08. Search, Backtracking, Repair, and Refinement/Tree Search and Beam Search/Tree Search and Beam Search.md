---
tags: [repair, search, beam]
---

# Tree Search and Beam Search

> **Definition.** Decoding strategies that maintain multiple partial outputs and explore them in parallel.

## Beam Search

Maintain a beam of $k$ partial sequences:

1. Start with one empty sequence.
2. At each step, expand each sequence with each possible next token.
3. Keep the top $k$ by score.
4. Stop when all sequences emit EOS.

Variants:

- **Diverse beam search**: penalize similar sequences in the beam.
- **Constrained beam search**: only expand sequences that satisfy constraints.
- **Top-$p$ / top-$k$ sampling**: stochastic alternatives.

## Tree Search (MCTS)

Monte Carlo Tree Search:

1. **Selection**: traverse the tree using UCB.
2. **Expansion**: add a new child.
3. **Rollout**: simulate to the end (cheap policy).
4. **Backprop**: update node values.

Used in:

- Game playing (AlphaGo).
- Program synthesis (AlphaCode).
- Code generation with tests.

## Comparison

| Approach        | Memory               | Diversity            | Optimality            |
| --------------- | -------------------- | -------------------- | --------------------- |
| Greedy          | Minimal              | Lowest               | Lowest                |
| Beam search     | $O(k \cdot T)$       | Medium               | Approximate           |
| MCTS            | Grows with tree      | High                 | Bounded by rollouts   |
| Backtracking    | Linear in depth      | High (with heuristics)| Optimal if complete  |

## In Structured Generation

- Beam search is the default for sequence generation.
- Constrained beam search enforces grammar/schema at each step.
- MCTS is used when a verifier (rollout value) is available, e.g. unit tests for code.

See [[Constrained Decoding]], [[Backtracking Search]].

## Related Concepts

- [[Constrained Decoding]]
- [[Backtracking Search]]
- [[Generate Validate Repair]]
