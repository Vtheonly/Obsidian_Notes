---
tags: [hybrid, verifiable]
---

# Verifiable Generation

> **Definition.** Generation that produces outputs with a **formal proof** (or certificate) of correctness.

## Pattern

```
Input
  ↓
Neural generator: produce candidate output
  ↓
Formal verifier: check property P
  ↓
If P holds: emit output + certificate
If P fails: reject (or repair and retry)
```

## Why It Matters

For safety-critical applications (engineering, construction, medicine), "looks plausible" is not enough. We need **proof**.

Verifiable generation combines:

- Neural generation (flexibility, scalability).
- Formal verification (rigor, proof).

## Examples

- **Code generation with proofs**: generate code + proof of type safety.
- **BIM generation with structural proof**: generate BIM + proof of static equilibrium.
- **Layout generation with code compliance**: generate layout + proof of code compliance.

## Challenges

- Verifiers are slow.
- Properties must be expressible in the verifier's logic.
- Generating with a verifier in the loop is hard (verifier is non-differentiable).

## Hybrid Approaches

- **Generate-validate-repair**: see [[Generate Validate Repair]].
- **Guided search**: see [[Guided Search]].
- **Differentiable solvers**: see [[Differentiable Solvers]].

See [[Neural + Formal Hybrid Systems]], [[Formal Verification]], [[Verifiable Generation]].

## Related Concepts

- [[Neural + Formal Hybrid Systems]]
- [[Formal Verification]]
- [[Generate Validate Repair]]
- [[Guided Search]]
- [[Differentiable Solvers]]
