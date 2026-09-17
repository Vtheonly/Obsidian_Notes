---
tags: [scene-graph, generation]
---

# Scene Graph Generation (SGG)

> **Definition.** Generating a scene graph from an image (or images, point cloud, etc.).

## Pipeline

```
Image
  ↓
Object detector (e.g. Faster R-CNN)
  ↓
Object features + bounding boxes
  ↓
Pairwise relation predictor
  ↓
Scene graph (nodes + edges)
```

## Variants

- **Predicate classification**: given object pairs, classify the relation.
- **Scene graph classification**: given objects (with labels), predict all relations.
- **Scene graph detection**: detect objects from scratch, then predict relations.

## Architectures

- **IMP** (Inference Motifs): chain-based relation prediction.
- **NeuralMotif**: bi-directional LSTM over objects.
- **RelDN**: relation detection network.
- **Transformer-based**: attention over object pairs.

## Challenges

- **Long-tailed relations**: rare relations are hard to predict.
- **Context**: relations depend on more than pairs (e.g. "person sitting on chair" depends on room context).
- **Ambiguity**: multiple relations can be plausible.

## In Buildings

SGG for buildings:

- Detect walls, doors, windows, slabs, columns, beams.
- Predict relations: `adjacent-to`, `connects`, `supports`, `contains`.
- Output: building scene graph → can be converted to BIM.

See [[Scene Graph Fundamentals]], [[Spatial Graph Construction]].

## Related Concepts

- [[Scene Graph Fundamentals]]
- [[Spatial Graph Construction]]
- [[Feature Extraction]]
- [[Instance and Panoptic]]
