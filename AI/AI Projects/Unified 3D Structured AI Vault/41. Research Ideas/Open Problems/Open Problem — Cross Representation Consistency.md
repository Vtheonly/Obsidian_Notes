---
tags: [research, open-problem, consistency]
---

# Open Problem — Cross-Representation Consistency

> **Problem.** When a building is simultaneously represented as a mesh, scene graph, tree, BIM, and point cloud, how do all representations stay synchronized under edits?

## Why It's Open

- Each representation captures different aspects.
- Edits in one must propagate to all others.
- Conflicts arise (e.g. mesh says wall is 0.20 m thick, BIM says 0.15 m).
- No unified differentiable representation exists.

## Sub-Problems

1. **Single source of truth**: which representation is canonical?
2. **Propagation**: how to propagate changes to all representations?
3. **Conflict detection**: how to detect when representations disagree?
4. **Conflict resolution**: how to resolve disagreements?
5. **Unified representation**: can one representation capture all aspects?

See [[Cross Representation Consistency]], [[Hybrid Representations]].

## Related Concepts

- [[Cross Representation Consistency]]
- [[Hybrid Representations]]
- [[Combining Trees Graphs and Geometry]]
