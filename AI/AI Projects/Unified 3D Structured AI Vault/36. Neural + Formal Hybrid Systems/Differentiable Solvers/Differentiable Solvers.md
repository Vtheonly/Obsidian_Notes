---
tags: [hybrid, differentiable, solvers]
---

# Differentiable Solvers

> **Definition.** Solvers (constraint, optimization, physics) that are differentiable, allowing gradients to flow back to a neural network.

## Why It Matters

A neural network can predict parameters; a solver checks feasibility. If the solver is differentiable, the network can be trained end-to-end:

```
Neural network → predict parameters → solver checks → loss → gradient → update network
```

## Examples

- **Differentiable physics** (Brax, PhysX-diff): differentiable rigid body simulation.
- **Differentiable rendering** (SoftRas, PyTorch3D): differentiable mesh rendering.
- **Differentiable SMT**: convert SAT/SMT solving into continuous optimization.
- **Differentiable optimization** (cvxpylayers): differentiable convex optimization.

## Strengths

- End-to-end training.
- Combines neural flexibility with solver rigor.

## Limitations

- Differentiable solvers are often slower.
- Gradients can be noisy or uninformative.
- Some constraints are hard to make differentiable (e.g. integer constraints).

See [[Neural + Formal Hybrid Systems]], [[Guided Search]], [[Verifiable Generation]].

## Related Concepts

- [[Neural + Formal Hybrid Systems]]
- [[Guided Search]]
- [[Verifiable Generation]]
