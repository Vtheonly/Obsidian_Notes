---
tags: [foundations, spectrum, verification, repair]
---

# Validating vs Verifying vs Repairing Structure

Three closely related but distinct operations:

| Term         | Question answered                              | Output                            |
| ------------ | ---------------------------------------------- | --------------------------------- |
| Validate     | "Is this output well-formed?"                  | `yes / no` (with reasons).        |
| Verify       | "Does this output satisfy property P?"         | `proof / counterexample`.         |
| Repair       | "Given an invalid output, how do we fix it?"   | `revised output + diagnosis`.     |

## Validate

A validator is a checker that tests well-formedness. Examples:

- A LaTeX parser checking that every `{` has a matching `}`.
- An IFC schema validator checking that every `IfcWall` has a `Representation`.
- A mesh validator checking that the mesh is watertight.

Validation is **algorithmic** and **binary**: the output either passes or fails.

See [[Geometric Validation]], [[Topological Validation]], [[BIM Validation]].

## Verify

A verifier is stronger: it provides a *certificate* that a property holds (or a counter-example that it does not). Examples:

- An SMT solver proving that a wall's endpoints are colinear with the floor slab's edge.
- A type checker proving that a generated program is well-typed.
- A static equilibrium solver proving that a generated structure stands.

Verification is **formal** and **property-specific**. You must state the property explicitly.

See [[Formal Verification]], [[Physics Based Verification]].

## Repair

A repair system takes an invalid output and produces a valid one. It must:

1. **Localize** the error (which node, which edge, which subtree).
2. **Diagnose** the cause (missing child, wrong type, conflicting geometry).
3. **Plan** a fix (regenerate subtree, adjust attribute, add missing edge).
4. **Apply** the fix.
5. **Re-validate** (or re-verify).

See [[Generate Validate Repair]], [[Backtracking Search]], [[Iterative Refinement]].

## Why Distinctions Matter

A system can validate without verifying (most BIM checkers), verify without repairing (formal provers), and repair without verifying (LLMs that hallucinate fixes). The strongest systems do all three in a loop.

## Related Concepts

- [[Learning vs Representing vs Using vs Constraining Structure]]
- [[Generate Validate Repair]]
- [[Formal Verification]]
- [[BIM Validation]]
- [[Backtracking Search]]
