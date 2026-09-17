---
tags: [repair, refinement]
---

# Iterative Refinement

> **Definition.** *Iterative refinement* starts from a rough draft and progressively improves it through small edits.

## Pattern

```
Draft = generate_rough(input)
for k iterations:
    Score = critique(Draft)
    Edits = propose_edits(Draft, Score)
    Draft = apply(Draft, Edits)
return Draft
```

## Why It Works

- Each iteration makes a small, localized improvement.
- The model can recover from early mistakes.
- The output gradually converges to a valid structure.

## Examples

- **Diffusion models**: iteratively denoise a random sample.
- **Refinement networks** for image-to-image tasks.
- **Self-refine** LLMs: ask the model to critique and revise its own output.
- **Iterative mesh refinement**: start from a coarse mesh, subdivide and refine.

## Comparison to Generate-Validate-Repair

| Approach                  | Trigger              | Granularity           |
| ------------------------- | -------------------- | --------------------- |
| Generate-validate-repair  | Validator signal     | Targeted at failures. |
| Iterative refinement      | Always (k iterations)| Whole output.         |

Iterative refinement is more general (always runs) but less targeted.

## Comparison to Constrained Generation

Constrained generation prevents errors; iterative refinement fixes them. They compose well: constrain during generation, refine after.

See [[Generate Validate Repair]], [[Constrained Decoding]].

## Related Concepts

- [[Generate Validate Repair]]
- [[Constrained Decoding]]
- [[Backtracking Search]]
