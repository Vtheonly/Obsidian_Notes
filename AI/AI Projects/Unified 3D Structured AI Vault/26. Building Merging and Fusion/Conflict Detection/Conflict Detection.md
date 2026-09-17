---
tags: [merging, conflict-detection]
---

# Conflict Detection

> **Definition.** Detect conflicts between two BIM models that are being merged.

## Types of Conflicts

| Conflict type   | Description                                                    |
| --------------- | -------------------------------------------------------------- |
| Geometric       | Two elements overlap when they shouldn't.                      |
| Semantic        | Two corresponding elements have different types or attributes. |
| Topological     | Connectivity / adjacency relations disagree.                   |
| Metadata        | Different property values (fire rating, material, etc.).       |
| Hierarchy       | Different containment structure (A says room in floor 1, B says floor 2). |

## Geometric Conflicts

- Clash detection: do two elements' geometries intersect?
- Tolerance: small overlaps may be acceptable.
- Severity: hard clash (physical intersection) vs soft clash (clearance violation).

## Semantic Conflicts

- Element type mismatch (wall vs slab).
- Property mismatch (fire rating F60 vs F90).
- Material mismatch.

## Topological Conflicts

- Door connects different rooms in A and B.
- Room adjacency differs.

## Hierarchy Conflicts

- Element assigned to different storeys.
- Building has different number of storeys.

See [[BIM Merging]], [[Conflict Resolution]].

## Related Concepts

- [[BIM Merging]]
- [[Semantic Alignment]]
- [[Conflict Resolution]]
