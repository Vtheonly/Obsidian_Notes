---
tags: [hybrid, search]
---

# Guided Search

> **Definition.** Use a neural network to guide a formal search procedure (e.g. MCTS, branch-and-bound).

## Pattern

```
Search state
  ↓
Neural network: predict value + policy (which action to try first)
  ↓
Search procedure: expand using neural guidance
  ↓
Formal checker: verify
  ↓
Update neural network from search results
```

## Examples

- **AlphaGo / AlphaZero**: neural-guided MCTS for games.
- **AlphaCode**: neural-guided search for program synthesis.
- **Neural theorem proving**: neural-guided proof search.

## Strengths

- Combines neural pattern recognition with formal correctness.
- Scales to large search spaces.
- Provides formal guarantees (via the checker).

## Limitations

- Expensive (many search iterations).
- Requires a good neural guide.
- Requires a formal checker.

See [[Neural + Formal Hybrid Systems]], [[Verifiable Generation]].

## Related Concepts

- [[Neural + Formal Hybrid Systems]]
- [[Verifiable Generation]]
- [[Differentiable Solvers]]
