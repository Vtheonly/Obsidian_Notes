---
tags: [constraints, solvers]
---

# Constraint Solvers

> **Definition.** Algorithms that find assignments of variables satisfying a set of constraints.

## Types

- **SAT solvers**: Boolean satisfiability (MiniSAT, CaDiCaL).
- **SMT solvers**: Satisfiability Modulo Theories (Z3, CVC4).
- **CP solvers**: Constraint Programming (OR-Tools, Gecode).
- **ILP solvers**: Integer Linear Programming (Gurobi, CPLEX).

## In BIM

- Enforce geometric constraints (parallelism, orthogonality, alignment).
- Enforce topological constraints (connectivity, containment).
- Enforce code compliance (corridor width, travel distance).

## Integration with Generation

- **Pre-check**: before adding a node/edge, query solver to see if feasible.
- **Post-check**: after generation, query solver to verify.
- **Repair**: use solver to find minimal fix.

See [[Hard Constraints]], [[Constrained Decoding]], [[Differentiable Solvers]].

## Related Concepts

- [[Hard Constraints]]
- [[Constrained Decoding]]
- [[Differentiable Solvers]]
- [[Formal Verification]]
