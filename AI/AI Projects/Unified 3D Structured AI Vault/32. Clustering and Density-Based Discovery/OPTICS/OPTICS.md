---
tags: [clustering, optics]
---

# OPTICS

> **Definition.** *Ordering Points To Identify the Clustering Structure*. Produces a cluster ordering rather than explicit clusters.

## Algorithm

1. For each point, compute its **core distance** (distance to the $\text{minPts}$-th nearest neighbor).
2. Compute **reachability distance** between pairs.
3. Produce an ordering of points by reachability.
4. The reachability plot reveals cluster structure (valleys = clusters).

## Strengths

- Handles varying density.
- Produces a hierarchy (extract clusters at multiple granularities).
- Less sensitive to $\epsilon$ than DBSCAN.

## Limitations

- More complex than DBSCAN.
- Slower.

## In Buildings

OPTICS for:

- Multi-scale analysis of point cloud density.
- Discovering clusters at different granularities (rooms vs. walls vs. furniture).

See [[DBSCAN]], [[HDBSCAN]].

## Related Concepts

- [[DBSCAN]]
- [[HDBSCAN]]
    