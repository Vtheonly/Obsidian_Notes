---
tags: [bim-generation, constrained]
---

# Constrained BIM Generation

> **Definition.** BIM generation that enforces constraints (grammar, schema, geometric, topological, semantic) so the output is always valid.

## Constraints

- **IFC schema**: entity types, attributes, relationships.
- **Geometric**: walls vertical, floors horizontal, no overlaps, containment.
- **Topological**: every door connects 2 spaces; every room reachable.
- **Semantic**: kitchen has sink; bathroom has toilet.
- **Code**: corridor width, travel distance, fire rating.

## Mechanisms

- **Grammar-constrained decoding**: enforce IFC syntax at each step.
- **Schema validation**: reject outputs that violate IFC schema.
- **Geometric solver**: enforce geometric constraints with a solver.
- **Topological validator**: check connectivity graph.
- **Repair loop**: regenerate invalid parts.

## Strengths

- Output is always valid (or rejected).
- Compatible with regulatory requirements.
- Easier to deploy in real engineering.

## Limitations

- Constraints must be encoded.
- Over-constraining reduces diversity.
- Some constraints are expensive to check.

See [[BIM Generation]], [[Constrained Decoding]], [[BIM Validation]], [[Generate Validate Repair]].

## Related Concepts

- [[BIM Generation]]
- [[Constrained Decoding]]
- [[BIM Validation]]
- [[Generate Validate Repair]]
- [[Verifiable Generation]]
