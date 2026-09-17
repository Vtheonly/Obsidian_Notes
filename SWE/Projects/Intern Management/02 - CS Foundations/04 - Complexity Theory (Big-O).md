---
tags: [concept, cs-foundations, complexity, performance]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
  - [[11 - DB Performance and Indexing/18 - N+1 Query Problem]]
---

# Complexity Theory (Big-O)

## What it is

Big-O notation describes how runtime (or memory) grows as input size grows. It answers: "if I double the input, how much longer does this take?"

`O(f(n))` means: worst case, the runtime grows proportional to `f(n)`. We ignore constants and lower-order terms.

## Common classes

| Class | Name | Example | If you double `n`… |
|---|---|---|---|
| `O(1)` | Constant | Hash table lookup | Same time |
| `O(log n)` | Logarithmic | Binary search, B-tree lookup | Adds one step |
| `O(n)` | Linear | Scanning an array | Doubles |
| `O(n log n)` | Linearithmic | Sort (merge, quick) | Slightly more than doubles |
| `O(n^2)` | Quadratic | Nested loop | Quadruples |
| `O(2^n)` | Exponential | Naive recursive Fibonacci | Catastrophic |

## How to compute

1. Count the dominant operation.
2. Express as a function of `n`.
3. Drop constants and lower-order terms.

```java
for (int i = 0; i < arr.length; i++) {        // O(n) — one pass
    if (arr[i].equals(target)) return i;
}
```

```java
while (low <= high) {                          // O(log n) — halves each iteration
    int mid = (low + high) / 2;
    ...
}
```

## The B-tree insight

A database B-tree index has a high fan-out (typically 100–1000 children per node). Looking up a row by indexed column takes `O(log_f n)` where `f` is the fan-out. For 1 billion rows and `f=100`, that's `log_100(10^9) ≈ 4.5` page reads. **Five disk reads vs. a billion.** That's why indexes matter.

## Common pitfalls

- Confusing worst-case with average-case. Hash tables are `O(1)` average, `O(n)` worst case.
- Forgetting that `O(1)` doesn't mean "fast." Hashing a 1 GB file is `O(1)` in input size but takes minutes.
- Ignoring constants when `n` is small. Insertion sort (`O(n^2)`) beats merge sort (`O(n log n)`) for `n < ~12`.

## Trade-offs

Big-O guides algorithm selection but doesn't capture:
- Constant factors (a hash map has a bigger constant than an array).
- Cache locality (an array is faster to scan than a linked list, even though both are `O(n)`).
- Memory usage (a B-tree uses more memory than a sorted array).
- Worst-case latency (a hash table's worst case is much worse than average).

Always combine Big-O reasoning with measurement. Big-O is the theory; profiling is the practice.

## Project Connection

- `MAX(id)+1` for primary keys: `O(log n)` with a PK index, `O(n)` without. The `requstes.sql` schema has no PK index. Fix: Oracle IDENTITY (see [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]]).
- N+1 in `searchIntern`: `O(n)` round-trips for `n` results. Fix: single JOIN, `O(1)` round-trips.
- TitledPane-in-VBox: `O(n)` memory + layout time for `n` rows. Fix: virtualized TableView, `O(1)` regardless of `n`.

## Further reading

- *Introduction to Algorithms* (CLRS), Chapters 1–3.
- bigocheatsheet.com.
