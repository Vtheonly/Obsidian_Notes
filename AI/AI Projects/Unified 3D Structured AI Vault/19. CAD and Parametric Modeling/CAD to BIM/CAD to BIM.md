---
tags: [cad, bim, conversion]
---

# CAD-to-BIM

> Converting a CAD model (geometry) into a BIM model (geometry + semantics + properties + relationships + hierarchy).

## Why It's Hard

CAD has geometry but lacks:

- element types (wall, slab, door),
- properties (fire rating, U-value),
- relationships (containment, connectivity),
- hierarchy (site → building → storey → space).

Conversion requires **inference**:

1. **Segment** CAD geometry into elements.
2. **Classify** each element (is this a wall? a slab? a column?).
3. **Infer** spatial containment (which floor? which room?).
4. **Infer** relationships (which doors connect which rooms?).
5. **Assign** properties (default fire rating, default material).
6. **Build** the IFC structure.

## Approaches

- **Manual**: human annotates (slow, accurate).
- **Rule-based**: geometric heuristics (vertical thin objects → walls; horizontal flat objects → slabs).
- **Learned**: train a classifier on labeled CAD → BIM pairs.
- **Hybrid**: rules + ML.

## In AI

CAD-to-BIM is a structured prediction problem:

- Input: CAD geometry.
- Output: BIM model (tree + graph + properties).

Tree-aware and structure-aware methods apply naturally. See [[Tree Generation]], [[Structure-Aware AI]].

See [[CAD Fundamentals]], [[BIM Fundamentals]], [[Tree Generation]].

## Related Concepts

- [[CAD Fundamentals]]
- [[BIM Fundamentals]]
- [[Tree Generation]]
- [[Structure-Aware AI]]
