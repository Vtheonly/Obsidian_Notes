---
tags: [3d, generation, autoregressive]
---

# Autoregressive 3D Generation

> **Definition.** Generate 3D content token by token, similar to language models.

## Tokenization

3D content must be tokenized:

- **Voxel tokens**: each voxel is a token (occupied / empty / class).
- **Quantized latents**: VQ-VAE on 3D, then transformer over latent codes.
- **Mesh tokens**: vertices / faces encoded as sequences.
- **Scene graph tokens**: objects + relations as a sequence.

## Architectures

- **Transformer decoder** over 3D tokens.
- **Tree decoder** for hierarchical 3D (e.g. building → storeys → rooms).
- **Graph decoder** for scene graphs.

## Strengths

- Sequential generation enables conditioning on partial output.
- Natural fit for hierarchical / structured outputs.
- Compatible with tree and graph constraints.

## Limitations

- Slow (sequential).
- Error accumulation (early mistakes propagate).
- Long sequences for high resolution.

## Connection to BIM

Tree-structured autoregressive generation is the most direct path to BIM:

```
Predict building node
  → predict storeys
    → predict rooms per storey
      → predict walls/doors/windows per room
        → predict geometry per element
```

See [[Tree Based BIM]], [[BIM Generation]], [[Hierarchical Decoders]].

## Related Concepts

- [[3D Generative Models]]
- [[Tree Based BIM]]
- [[BIM Generation]]
- [[Hierarchical Decoders]]
