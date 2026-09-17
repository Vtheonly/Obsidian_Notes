---
tags: [synthetic, procedural]
---

# Procedural Generation

> **Definition.** Generate content algorithmically from rules, parameters, and randomness.

## In Buildings

Procedural building generation uses:

- **Shape grammars** (see [[Shape Grammars]]).
- **CGA shape** (Computer Generated Architecture).
- **L-systems** (for branching structures like cities).
- **Wave function collapse** (constraint-based tiling).

## Pipeline

```
Start shape
  ↓
Apply rule R1 (e.g. split building into floors)
  ↓
Apply rule R2 to each floor (split into rooms)
  ↓
Apply rule R3 to each wall (add windows)
  ↓
...
  ↓
Final building
```

## Strengths

- **Compact**: small rule set generates large variety.
- **Controllable**: parameters and rules can be tweaked.
- **Deterministic** (given seed): reproducible.
- **Fast**: no neural network inference.

## Limitations

- Rules must be authored manually (or learned — see [[Grammar Induction]]).
- Limited to what rules can express.
- Hard to learn from data without grammar induction.

## Use Cases

- Synthetic datasets for training (e.g. synthetic interiors).
- Video game cities.
- Quick massing studies in architecture.

See [[Shape Grammars]], [[Rule Based]], [[Grammar Induction]].

## Related Concepts

- [[Shape Grammars]]
- [[Rule Based]]
- [[Grammar Induction]]
- [[Synthetic RGB Depth BIM]]
