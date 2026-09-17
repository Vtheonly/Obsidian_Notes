---
tags: [bim, containment]
---

# Containment Relationships

> A spatial element contains another element. This forms the spatial hierarchy tree.

## Examples

- Site contains Building.
- Building contains Storey.
- Storey contains Space.
- Space contains Element (wall, door, furniture).

## IFC Encoding

- `IfcRelAggregates` for site → building → storey → space.
- `IfcRelContainedInSpatialStructure` for space → element.

## Properties

- **Tree**: each element has exactly one parent (single containment).
- **Closure**: if A contains B and B contains C, then A contains C.
- **Disjointness**: siblings do not contain each other.

## Validation

- Every element must be contained in exactly one space (or storey, building, site).
- Containment must be consistent with geometry (element's geometry inside parent's geometry).

See [[BIM Relationships]], [[IFC Spatial Structure]], [[Topological Validation]].

## Related Concepts

- [[BIM Relationships]]
- [[IFC Spatial Structure]]
- [[Spatial Adjacency]]
- [[Topological Validation]]
