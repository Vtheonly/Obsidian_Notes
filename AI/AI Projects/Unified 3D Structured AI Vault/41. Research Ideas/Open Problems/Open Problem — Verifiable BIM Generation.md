---
tags: [research, open-problem, bim]
---

# Open Problem — Verifiable BIM Generation

> **Problem.** Generate BIM models that are *verifiably* valid: every geometric, topological, structural, semantic, and code-compliance property holds with a formal certificate.

## Why It's Open

- Existing BIM generators produce plausible but not verifiable models.
- Formal verifiers are slow and hard to integrate into generation loops.
- Expressing all relevant properties in a single formalism is hard.

## Sub-Problems

1. **Property specification**: how to formally state all properties a BIM must satisfy?
2. **Verifiable generator**: how to generate BIM such that a certificate is produced alongside?
3. **Repair with proof**: when a property fails, how to repair while maintaining provability?
4. **Scalability**: how to make verification scale to large buildings?

## Approaches

- [[Constrained BIM]] with formal constraints.
- [[Verifiable Generation]] with formal verifiers.
- [[Guided Search]] with neural guidance + formal checking.
- [[Differentiable Solvers]] for end-to-end training.

See [[Open Problem — Neural Formal Hybrid Generation]], [[Verifiable Generation]].

## Related Concepts

- [[Verifiable Generation]]
- [[Constrained BIM]]
- [[Open Problem — Neural Formal Hybrid Generation]]
