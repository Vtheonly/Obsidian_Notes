---
tags: [bim, connectivity]
---

# Connectivity Relationships

> Two elements are **connected** if they touch, share, or are linked by a passage. This is a graph relation.

## Examples

- A door connects two rooms.
- A staircase connects two storeys.
- A beam connects two columns.
- A pipe connects two fixtures.

## IFC Encoding

- `IfcRelConnectsElements` for generic connections.
- `IfcRelConnectsPathElements` for path elements (pipes, ducts, cables).
- `IfcRelConnectsStructuralActivity` for structural connections (beam-to-column).

## Why It Matters

Connectivity enables:

- Route planning (how to get from A to B).
- Structural analysis (load paths).
- MEP routing (pipe networks).
- Code compliance (egress paths).

## Validation

- A door must connect exactly two spaces.
- A staircase must connect exactly two storeys.
- Connectivity graph must be connected (no isolated parts).

See [[BIM Relationships]], [[Topological Validation]].

## Related Concepts

- [[BIM Relationships]]
- [[Spatial Adjacency]]
- [[Topological Validation]]
