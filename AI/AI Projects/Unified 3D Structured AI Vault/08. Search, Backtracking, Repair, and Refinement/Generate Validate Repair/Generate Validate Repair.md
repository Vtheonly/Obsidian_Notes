---
tags: [repair, generate-validate-repair]
---

# Generate → Validate → Repair

> **Definition.** An architecture that **generates** an output, **validates** it, and if invalid, **locates** the error and **repairs** it, then re-validates.

## Pattern

```
Generate(output)
  ↓
Validate(output)
  ↓
Valid?
    - Yes → return output
    - No  → Locate error
            ↓
            Diagnose cause
            ↓
            Plan fix
            ↓
            Apply fix → regenerated output
            ↓
            Validate again (loop)
```

## When to Use

- When constrained generation is too restrictive (kills diversity).
- When validation is cheap but constraints are hard to express at decode time.
- When localized errors are common (most of the output is fine; small parts are wrong).

## When Not to Use

- When the error rate is high (each generation needs many repair rounds).
- When errors are global (whole output is wrong; localized repair doesn't help).
- When latency matters (each round adds delay).

## Comparison to Constrained Generation

| Approach                | Hard guarantee?    | Diversity          | Latency          |
| ----------------------- | ------------------ | ------------------ | ---------------- |
| Constrained generation  | Yes (per step)     | Lower (constrained)| Lower (per step) |
| Generate-validate-repair| Yes (after repair) | Higher (free gen)  | Higher (rounds)  |

See [[Constrained Decoding]], [[Hard Guarantees vs Statistical Preferences]].

## Repair Strategies

- **Resample**: regenerate the whole output (cheap but destroys good parts).
- **Localized rewrite**: regenerate only the failing subtree/segment.
- **Constraint projection**: project the output onto the nearest valid output.
- **Solver-based fix**: solve for the minimal change that satisfies the constraint.

See [[Backtracking Search]], [[Iterative Refinement]].

## Related Concepts

- [[Backtracking Search]]
- [[Iterative Refinement]]
- [[Constrained Decoding]]
- [[Validating vs Verifying vs Repairing Structure]]
