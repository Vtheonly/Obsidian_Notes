---
tags: [datasets, domain-randomization]
---

# Domain Randomization

> **Definition.** Vary the synthetic data's appearance (textures, lighting, colors, object placements) to make models robust to real-world variations.

## Why It Works

A model trained on a single synthetic appearance may overfit to that appearance. Training on many randomized appearances forces the model to learn the *structure*, not the appearance.

## What to Randomize

- **Textures**: random colors, patterns.
- **Lighting**: random direction, intensity, color.
- **Camera**: random pose, focal length.
- **Object placement**: random positions, orientations, scales.
- **Background**: random scenes.

## In Buildings

- Random wall colors, floor textures, ceiling textures.
- Random furniture placement.
- Random lighting conditions.
- Random camera poses.

## Result

A model trained on randomized synthetic data:

- generalizes better to real data,
- is more robust to lighting / texture variations,
- focuses on structure (not appearance).

See [[Synthetic Generators]], [[Sim to Real]].

## Related Concepts

- [[Synthetic Generators]]
- [[Sim to Real]]
