---
tags: [scene-graph, construction]
---

# Spatial Graph Construction

> **Definition.** Building a spatial graph (nodes = objects, edges = spatial relations) from a scene.

## Steps

1. **Detect objects**: from images, point clouds, or BIM.
2. **Compute pairwise features**: distance, relative position, contact area, relative orientation.
3. **Predict relations**: classify each pair as one of {`adjacent`, `supports`, `connects`, `none`, ...}.
4. **Filter**: keep only high-confidence edges.
5. **Refine**: enforce constraints (symmetric adjacency, transitive containment).

## Pairwise Features

- Euclidean distance between centroids.
- Distance between surfaces (closest point).
- Bounding box overlap (IoU).
- Bounding box containment.
- Relative orientation (dot product of normals).

## Relation Classifiers

- **Rule-based**: threshold distances and overlaps.
- **MLP**: pairwise features → relation class.
- **GNN**: message passing between objects.
- **Transformer**: attention over object pairs.

## Constraints

- **Symmetric**: `adjacent-to(A, B)` ⟺ `adjacent-to(B, A)`.
- **Asymmetric**: `supports(A, B)` ≠ `supports(B, A)`.
- **Transitive**: `contains(A, B) ∧ contains(B, C) → contains(A, C)`.

Enforce with rule-based post-processing or constrained decoding.

See [[Scene Graph Fundamentals]], [[Scene Graph Generation]].

## Related Concepts

- [[Scene Graph Fundamentals]]
- [[Scene Graph Generation]]
- [[Spatial Relations]]
- [[Adjacency and Containment]]
