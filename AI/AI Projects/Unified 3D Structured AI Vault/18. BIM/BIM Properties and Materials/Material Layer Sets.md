---
tags: [bim, materials]
---

# Material Layer Sets

> A *material layer set* defines the material composition of a layered element (typically a wall, slab, or roof).

## Structure

```
IfcMaterialLayerSet
  - IfcMaterialLayer "Brick" (thickness 0.10 m)
  - IfcMaterialLayer "Insulation" (thickness 0.08 m)
  - IfcMaterialLayer "Air gap" (thickness 0.04 m)
  - IfcMaterialLayer "Drywall" (thickness 0.013 m)
```

Attached to the element via `IfcRelAssociatesMaterial`.

## Why It Matters

- **Thermal analysis**: compute U-value from layer conductivities.
- **Acoustic analysis**: compute sound transmission class.
- **Cost estimation**: material quantities × unit cost.
- **Structural analysis**: material strengths.
- **Sustainability**: embodied carbon.

## Common Wall Layer Sets

- **Brick cavity wall**: brick + cavity + insulation + brick.
- **Stud wall**: drywall + stud + insulation + drywall.
- **Concrete wall**: concrete (single layer).

## In AI

Material layer sets are node attributes. A generator must predict:

- how many layers,
- what material per layer,
- what thickness per layer.

A validator must check:

- total thickness matches the wall's geometry,
- materials are valid,
- thermal properties are reasonable.

See [[Property Sets]], [[Quantity Sets]], [[IFC Property Sets]].

## Related Concepts

- [[Property Sets]]
- [[Quantity Sets]]
- [[IFC Property Sets]]
