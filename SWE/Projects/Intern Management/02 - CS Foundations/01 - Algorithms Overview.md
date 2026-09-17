---
tags: [concept, cs-foundations, algorithms]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/04 - Complexity Theory (Big-O)]]
  - [[02 - CS Foundations/05 - Data Structures Overview]]
related:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# Algorithms Overview

## What it is

An algorithm is a step-by-step procedure for solving a problem. The choice of algorithm determines Big-O complexity. Choice of data structure and choice of algorithm are intertwined — binary search requires a sorted array (or balanced tree).

## Core algorithmic concepts

### Sorting
- **Quicksort** — average `O(n log n)`, worst `O(n^2)`. In-place. Default in many languages.
- **Merge sort** — guaranteed `O(n log n)`. Stable. Needs `O(n)` extra space.
- **Heapsort** — guaranteed `O(n log n)`, in-place, not stable.
- **Insertion sort** — `O(n^2)` but fast for tiny `n` (used as the base case in quicksort).

### Searching
- **Linear search** — `O(n)`. Works on any collection.
- **Binary search** — `O(log n)`. Requires sorted collection.
- **Hash lookup** — `O(1)` average. Requires hash table.

### Recursion
A function that calls itself. Required for tree traversal, divide-and-conquer (merge sort, quick sort). Risk: stack overflow if recursion is too deep. Tail recursion can be optimized to a loop by the compiler (Java does *not* do tail-call optimization).

### Tree traversal
- **In-order** (left, root, right) — visits BST in sorted order.
- **Pre-order** (root, left, right) — useful for copying.
- **Post-order** (left, right, root) — useful for deleting.
- **Level-order** (BFS) — useful for shortest path.

### Graph algorithms
- **BFS** — shortest path in unweighted graphs.
- **DFS** — cycle detection, topological sort.
- **Dijkstra** — shortest path in weighted graphs (no negative edges).
- **A\*** — shortest path with heuristic.

## Why this matters for databases

A B-tree index is a self-balancing tree with high fan-out. The database uses B-tree traversal (`O(log_f n)`) to find rows by indexed columns. Without an index, the database falls back to linear search (`O(n)` full table scan).

The query optimizer picks the algorithm: index range scan vs. full table scan vs. hash join vs. nested loop join vs. merge join. These are all classic algorithms applied to disk-resident data.

## Common pitfalls

- Using a `O(n^2)` algorithm when `O(n log n)` is available (bubble sort vs. quicksort).
- Using recursion where iteration would do (Python recursion limit; Java stack overflow).
- Re-implementing a sort algorithm — use `Arrays.sort()` or `Collections.sort()`.
- Not recognizing dynamic programming opportunities (Fibonacci, longest common subsequence).

## Project Connection

- `MAX(id)+1` does a linear scan of the table (or B-tree scan if PK indexed) on every insert. Replacing with IDENTITY/sequence reduces to `O(1)` amortized.
- `searchIntern` + `getNameById` per row is `O(n)` round-trips. JOIN collapses to `O(1)` round-trips + `O(n log n)` join (if both sides indexed).
- The HashMap iteration is `O(n)` in the number of columns (small), but the bug is the order, not the speed.

## Further reading

- *Introduction to Algorithms* (CLRS).
- *The Algorithm Design Manual* (Skiena).
