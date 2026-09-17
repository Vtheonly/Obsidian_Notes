---
tags: [bim, quantities]
---

# Quantity Sets

> A *quantity set* stores measurable quantities of an element: area, volume, length, weight, count.

## IFC Encoding

- `IfcElementQuantity`: container.
- `IfcQuantityArea`, `IfcQuantityVolume`, `IfcQuantityLength`, `IfcQuantityWeight`, `IfcQuantityCount`: individual quantities.

## Examples

For a wall:
- Net area (excluding openings).
- Gross area (including openings).
- Volume.
- Length, height, thickness.

For a slab:
- Net area, gross area.
- Volume.
- Perimeter.

## Why It Matters

- **Cost estimation**: quantities × unit cost.
- **Construction planning**: quantities drive time estimates.
- **Validation**: check that predicted quantities match expected (e.g. wall area is reasonable for a wall of this length and height).

## In AI

Quantity sets are derivable from geometry. A generator that produces geometry can compute quantities; a validator can check that they make sense.

See [[Property Sets]], [[Material Layer Sets]], [[IFC Property Sets]].

## Related Concepts

- [[Property Sets]]
- [[Material Layer Sets]]
- [[IFC Property Sets]]
