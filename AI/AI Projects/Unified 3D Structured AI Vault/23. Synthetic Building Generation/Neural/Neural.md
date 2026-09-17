---
tags: [synthetic, neural]
---

# Neural Generation (Buildings)

> **Definition.** Generate building content with neural networks (diffusion, autoregressive, GAN, VAE).

## Variants

- **Image-based**: generate building images (then optionally lift to 3D).
- **Voxel-based**: generate building as a voxel grid.
- **Mesh-based**: generate building as a mesh.
- **Latent 3D**: generate in a 3D latent space.
- **Tree-based**: generate the building hierarchy as a tree.
- **Scene-graph-based**: generate the building as a scene graph.

## Strengths

- Learns from data (real buildings).
- Produces diverse outputs.
- Can be conditioned (text, image, partial building).

## Limitations

- **Hallucination**: can produce implausible buildings.
- **No hard guarantees**: structural, semantic, code compliance not guaranteed.
- **Data hungry**: needs large training set.
- **Hard to edit**: latent representations are opaque.

## Hybrid Approach

Combine neural generation with rules / constraints / validation:

1. Neural network generates a draft.
2. Validator checks geometric, topological, semantic, code constraints.
3. Repair loop fixes violations.
4. Final output is plausible + valid.

See [[BIM Generation]], [[Diffusion 3D]], [[Autoregressive 3D]], [[Constrained BIM]].

## Related Concepts

- [[BIM Generation]]
- [[Diffusion 3D]]
- [[Autoregressive 3D]]
- [[Constrained BIM]]
- [[Generate Validate Repair]]
