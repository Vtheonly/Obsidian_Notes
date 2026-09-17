---
tags: [bim-generation, autoregressive]
---

# Autoregressive BIM Generation

> **Definition.** Generate a BIM model token by token (or node by node), each step conditioned on the previous.

## Tokenization

A BIM model is serialized:

- **Sequence**: `(building, storey, room, wall, ...)` with brackets.
- **Tree**: each node has a parent pointer.
- **Graph**: nodes + edges as a sequence.

## Architecture

- Transformer decoder over the serialized BIM.
- Tree decoder that emits nodes one at a time, attaching to parents.
- Graph decoder that emits nodes + edges.

## Strengths

- Sequential conditioning enables complex dependencies.
- Natural fit for hierarchical BIM.
- Compatible with constrained decoding (grammar / schema).

## Limitations

- Slow (sequential).
- Error accumulation.
- Long sequences for large buildings.

See [[BIM Generation]], [[Tree Based BIM]], [[Constrained BIM]].

## Related Concepts

- [[BIM Generation]]
- [[Tree Based BIM]]
- [[Constrained BIM]]
- [[Autoregressive 3D]]
