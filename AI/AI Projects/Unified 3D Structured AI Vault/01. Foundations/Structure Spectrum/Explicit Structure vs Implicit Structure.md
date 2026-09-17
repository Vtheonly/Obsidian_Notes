---
tags: [foundations, spectrum, explicit, implicit]
---

# Explicit Structure vs Implicit Structure

> **Definition.** Structure is *explicit* if it is represented as a data structure in the model (edges, masks, parent pointers). Structure is *implicit* if it is only present in the data distribution or in the model's learned behaviour.

## Explicit Structure

Examples:
- An AST stored as a tree of node objects.
- An edge list of a scene graph.
- A tree-structured attention mask.
- A grammar used to constrain decoding.
- An IFC file's spatial containment hierarchy.

Explicit structure is **inspectable**, **editable**, **validatable**, and **verifiable**.

## Implicit Structure

Examples:
- A language model's latent representation of LaTeX syntax.
- A diffusion model's preference for watertight meshes (learned from data).
- An embedding space in which similar structures cluster together.

Implicit structure is **cheaper** (no annotation needed) but **opaque** — you cannot inspect, edit, validate, or verify it directly.

## Why This Matters

- You can only **constrain** what is explicit.
- You can only **validate** what is explicit.
- You can only **verify** what is explicit.
- You can only **repair** what is explicit.

Implicit structure can be *made* explicit by parsing or by an auxiliary predictor, but that introduces its own errors.

## Hybrid Strategy

Many strong systems use *both*:

1. Train an auxiliary predictor to extract explicit structure from raw data.
2. Use the explicit structure to constrain, validate, and repair.
3. Use the implicit representation to handle ambiguity and missing data.

See [[Neural + Formal Hybrid Systems]], [[Verifiable Generation]].

## Related Concepts

- [[The Awareness Spectrum]]
- [[Learning vs Representing vs Using vs Constraining Structure]]
- [[Hard Guarantees vs Statistical Preferences]]
