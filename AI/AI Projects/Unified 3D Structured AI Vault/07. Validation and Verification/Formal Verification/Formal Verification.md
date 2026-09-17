---
tags: [verification, formal]
---

# Formal Verification

> **Definition.** *Formal verification* uses mathematical methods to **prove** that a system satisfies a property.

Unlike validation (which checks), verification **proves**. The output is a proof certificate or a counter-example.

## Methods

| Method                | Mechanism                                                            |
| --------------------- | ------------------------------------------------------------------- |
| Theorem proving       | Interactive (Coq, Isabelle, Lean) or automated (ACL2).              |
| SMT solving           | Decide satisfiability of formulas with theories (Z3, CVC4).          |
| Model checking        | Exhaustive state-space exploration (SPIN, NuSMV).                   |
| Abstract interpretation| Approximate program semantics (Astree, Polyspace).                  |
| Type checking         | Prove absence of type errors (for code generation).                 |

## Application to BIM

- Prove that every load has a path to the foundation.
- Prove that travel distance to exit is bounded.
- Prove that every door connects exactly two spaces.
- Prove that no two structural elements clash.

The property is encoded as a logical formula; the model is encoded as axioms; the solver decides.

## Strengths

- **Proof**, not just check.
- Counter-examples are diagnostic.

## Limitations

- Expensive (computationally and in human time for interactive provers).
- Properties must be expressible in the chosen logic.
- Scalability: large models can blow up the solver.

See [[BIM Validation]], [[Verifiable Generation]], [[Neural + Formal Hybrid Systems]].

## Related Concepts

- [[BIM Validation]]
- [[Verifiable Generation]]
- [[Neural Verification]]
- [[Physics Based Verification]]
