---
tags: [research, open-problem, hybrid]
---

# Open Problem — Neural + Formal Hybrid Generation

> **Problem.** Build a generator that combines neural flexibility with formal rigor, producing outputs that are both plausible and verifiably valid.

## Why It's Open

- Neural and formal methods have different strengths.
- Integrating them requires either differentiable solvers or guided search.
- Both are expensive and hard to scale.

## Sub-Problems

1. **Integration architecture**: how to combine neural and formal components?
2. **Training**: how to train end-to-end with a non-differentiable verifier?
3. **Scalability**: how to scale to large outputs (whole buildings)?
4. **Expressivity**: what properties can be formally verified?

See [[Neural + Formal Hybrid Systems]], [[Verifiable Generation]], [[Guided Search]].

## Related Concepts

- [[Neural + Formal Hybrid Systems]]
- [[Verifiable Generation]]
- [[Guided Search]]
- [[Differentiable Solvers]]
