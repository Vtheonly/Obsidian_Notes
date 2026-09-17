---
tags: [structured-generation, prediction]
---

# Structured Prediction

> **Definition.** *Structured prediction* is the task of predicting an output that has internal structure (a tree, graph, sequence with constraints, etc.) rather than a single label or a flat vector.

## Examples

| Task                          | Output structure                  |
| ----------------------------- | --------------------------------- |
| Image-to-LaTeX                | Expression tree → LaTeX string.   |
| Image-to-markup               | DOM tree → HTML/XML string.       |
| Code generation               | AST → source string.              |
| Scene graph generation        | Scene graph (nodes + edges).      |
| BIM generation                | Spatial hierarchy + relations.    |
| Layout generation             | List of rectangles with relations.|
| Program synthesis             | AST → program.                    |

## Why It Is Hard

The output space is exponentially large (or infinite), so:

- You cannot enumerate and score all candidates.
- You need a tractable decoding strategy (greedy, beam, search).
- The loss must capture structure, not just element-wise accuracy.

## Key Questions

1. **What is the output structure?** (tree, graph, sequence, hybrid)
2. **How is it represented?** (sequence with brackets, edge list, tree object)
3. **How is it generated?** (autoregressive, tree decoder, graph decoder)
4. **How is it scored?** (per-element loss, structural loss, validator-based)
5. **How is it constrained?** (grammar, schema, hard mask, soft bias)
6. **How is it validated?** (parser, schema, formal verifier)
7. **How is it repaired?** (resample, localized rewrite, backtracking)

See [[Structured Output Spaces]], [[Structured Loss]], [[Constrained Decoding]].

## Related Concepts

- [[Structured Output Spaces]]
- [[Structured Loss]]
- [[Constrained Decoding]]
- [[Tree Generation]]
- [[Generate Validate Repair]]
