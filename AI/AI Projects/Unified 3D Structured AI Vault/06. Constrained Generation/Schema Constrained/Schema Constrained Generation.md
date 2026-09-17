---
tags: [constrained-generation, schema]
---

# Schema-Constrained Generation

> **Definition.** *Schema-constrained generation* restricts output to satisfy a schema (JSON Schema, XML Schema, IFC schema, SQL schema).

## Difference from Grammar-Constrained

- **Grammar**: syntactic rules (e.g. JSON syntax).
- **Schema**: semantic rules on top of syntax (e.g. JSON Schema requiring `name` to be a string, `age` to be a positive integer).

A schema-constrained generator typically:

1. Uses grammar-constrained generation for syntax.
2. Adds schema-level masks (e.g. only allow property names defined in the schema).
3. Validates output against the schema at the end.

## Example: IFC

The IFC schema defines:

- entity types (`IfcWall`, `IfcSlab`, ...),
- attributes per entity,
- relationships (`IfcRelContainedInSpatialStructure`, ...),
- cardinalities (a wall must have a representation; a door must connect two spaces).

A schema-constrained BIM generator would:

- emit only valid entity types,
- require all mandatory attributes,
- enforce relationship cardinalities.

See [[BIM Validation]], [[Constrained BIM]].

## Strengths

- Hard guarantee on schema validity.
- Compatible with industrial schemas (JSON Schema, XSD, IFC).

## Limitations

- Only schema-level properties are guaranteed.
- Some schemas are very large; mask computation is expensive.
- Schema evolution (new versions) requires updating the constraint.

## Related Concepts

- [[Grammar Constrained Generation]]
- [[Constrained Decoding]]
- [[BIM Validation]]
- [[Constrained BIM]]
