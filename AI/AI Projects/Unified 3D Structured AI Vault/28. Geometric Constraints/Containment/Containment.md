---
tags: [constraints, geometric, containment]
---

# Containment Constraints

> **Definition.** Constraints that one element's geometry is inside another's.

## Examples

- Window's geometry inside its wall's geometry.
- Door's geometry inside its wall's geometry.
- Furniture's geometry inside its room's geometry.
- Room's geometry inside its storey's geometry.

## Enforcement

- Point-in-mesh test for centroid.
- Surface containment test for boundary.
- Volume containment test for full geometry.

## Why It Matters

Containment constraints enforce the spatial hierarchy. A window outside its wall violates the containment tree.

See [[Geometric Constraints]], [[Spatial Validation]], [[Containment Relationships]].

## Related Concepts

- [[Geometric Constraints]]
- [[Spatial Validation]]
- [[Containment Relationships]]
