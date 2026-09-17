---
tags: [foundations, awareness, structure-aware]
---

# What Is Structure-Aware AI

> **Definition.** A model is *structure-aware* if it explicitly represents or exploits the relationships and organization among the components of whatever it is processing, instead of treating them as an unstructured collection or a flat sequence.

## What "Aware" Means

When a paper says a model is *X-aware*, it does **not** mean the model is conscious of X. It means:

> The model takes information about X into account during prediction, generation, or reasoning.

So *structure-aware* means the model takes information about how the output (or input) is *organized* into account.

## Structure vs Content

Suppose the data is:

```
A
  - B
      - D
      - E
  - C
```

There are two kinds of information here:

- **Content information**: the five elements `A, B, C, D, E`.
- **Structural information**: `parent(A, B)`, `parent(A, C)`, `parent(B, D)`, `parent(B, E)`, `sibling(D, E)`, `depth(B) = 1`.

A non-structure-aware model can know all five elements while *ignoring* their relationships. A structure-aware model preserves or exploits those relationships.

## Where It Appears

- **NLP**: parse trees, dependency graphs, ASTs of code.
- **Tables**: rows and columns, not just cells.
- **HTML / XML**: DOM hierarchy, not just text tokens.
- **SQL**: clause hierarchy (`SELECT / FROM / WHERE / AND`), not just keywords.
- **LaTeX**: mathematical hierarchy (fractions, superscripts, radicals).
- **BIM**: spatial containment and connectivity, not just meshes.
- **3D scenes**: scene graphs (objects and relations), not just points.

See [[Structure vs Content]], [[Awareness vs Consciousness]].

## How Structure Can Enter a Model

A paper that claims structure-awareness could mean any of:

1. **Structural embeddings** — augment each token embedding with positional/relational info.
2. **Structural attention** — bias attention toward parent / child / sibling.
3. **Structural constraints** — restrict the decoder so it cannot emit invalid structures.
4. **Generate-structure-first** — predict the skeleton, then fill it.
5. **Tree or graph decoder** — emit a tree or graph directly rather than a sequence.
6. **Grammar-guided decoding** — restrict next tokens by a grammar.
7. **Schema validation in the loop** — reject and resample invalid candidates.

See [[How Structure Enters Models]] for the full enumeration.

## Critical Distinction

The phrase "structure-aware" describes the **principle**, not a specific implementation. Two papers can both call themselves structure-aware while doing very different things mechanically.

You must always ask:

- Is the structure learned or explicitly defined?
- Is it injected as embeddings, attention, constraints, or decoder shape?
- Does it create a *hard guarantee* or merely a *statistical preference*?

See [[Learning vs Representing vs Using vs Constraining Structure]] and [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[What Is Tree Aware AI]]
- [[What Is 3D Aware AI]]
- [[What Is Hierarchy Aware AI]]
- [[What Is Graph Aware AI]]
- [[What Is Spatially Aware AI]]
- [[What Is Geometry Aware AI]]
- [[What Is Semantic Aware AI]]
- [[What Is Topology Aware AI]]
- [[The Awareness Spectrum]]
