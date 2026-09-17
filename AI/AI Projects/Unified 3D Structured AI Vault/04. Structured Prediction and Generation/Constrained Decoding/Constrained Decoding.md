---
tags: [structured-generation, constrained-decoding]
---

# Constrained Decoding

> **Definition.** *Constrained decoding* modifies the next-token distribution at generation time so that the output satisfies a given constraint (grammar, schema, type system, etc.).

## Mechanism

At each step $t$:

1. Compute the model's logits $\ell_t$ over the vocabulary.
2. Compute the set of valid next tokens $V_t$ based on the constraint and the partial output $y_{<t}$.
3. Mask logits: $\ell_t[i] = -\infty$ for $i \notin V_t$.
4. Softmax to get the constrained distribution.

## Types of Constraints

| Constraint type             | Source of valid next tokens                          |
| --------------------------- | ---------------------------------------------------- |
| Grammar                     | Parser state.                                        |
| Schema (JSON, XML, IFC)     | Schema validator.                                    |
| Type system                 | Type checker.                                        |
| Regex                       | DFA state.                                            |
| Logical constraints         | SAT/SMT solver.                                       |
| Geometric constraints       | Differentiable geometric solver.                     |

## Strengths

- Hard guarantee: output *always* satisfies the constraint.
- Cheap to apply (mask is computed once per step).
- Compatible with any autoregressive model.

## Limitations

- Only constraints *expressible* in the chosen formalism can be enforced.
- Some constraints are expensive to check (e.g. global graph properties).
- Over-constraining reduces diversity.

## Comparison to Generate-Validate-Repair

| Approach                | Hard guarantee?   | Cost per generation |
| ----------------------- | ----------------- | ------------------- |
| Constrained decoding    | Yes (per step)    | Higher per step     |
| Generate-validate-repair| Yes (after repair)| Higher per sample   |

See [[Generate Validate Repair]], [[Grammar Constrained Generation]], [[Schema Constrained Generation]].

## Related Concepts

- [[Grammar Constrained Generation]]
- [[Schema Constrained Generation]]
- [[Structural Constraints]]
- [[Generate Validate Repair]]
