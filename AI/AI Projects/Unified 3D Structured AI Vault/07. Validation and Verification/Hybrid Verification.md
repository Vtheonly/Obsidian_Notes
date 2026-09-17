---
tags: [verification, hybrid]
---

# Hybrid Verification

> **Definition.** *Hybrid verification* combines formal, neural, and physics-based methods to get the strengths of each.

## Pattern

```
Output
  ↓
[Neural pre-check] — fast filter; rejects obvious failures.
  ↓ if passes
[Geometric/topological validation] — cheap rule checks.
  ↓ if passes
[Physics simulation] — expensive but accurate.
  ↓ if passes
[Formal verification] — proof of critical properties.
  ↓
Accept or reject with diagnosis.
```

## Why Hybrid

- Neural: fast, scalable, but no guarantee.
- Geometric/topological: cheap, exact, but limited scope.
- Physics: accurate, but expensive.
- Formal: proof, but expensive and limited expressivity.

Hybrid applies each at the right stage: cheap filters first, expensive provers last.

See [[Neural + Formal Hybrid Systems]], [[Verifiable Generation]].

## Related Concepts

- [[Formal Verification]]
- [[Neural Verification]]
- [[Physics Based Verification]]
- [[Neural + Formal Hybrid Systems]]
