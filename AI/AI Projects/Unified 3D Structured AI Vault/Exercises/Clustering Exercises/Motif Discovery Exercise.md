---
tags: [exercise, clustering, motifs]
---

# Exercise — Motif Discovery

## Problem

Consider a building with the following wall configurations (each wall is a sequence of elements):

```
Wall 1: [W, Wi, Wi, D]
Wall 2: [W, Wi, D]
Wall 3: [W, Wi, Wi, Wi, D]
Wall 4: [W, D]
Wall 5: [W, Wi, D, Wi]
```

Where W = wall segment, Wi = window, D = door.

(a) What is the most frequent motif?
(b) What motifs would MDL keep?
(c) Why might raw frequency mislead?

## Required Background

- A **motif** is a recurring structural pattern. See [[Structural Motif Discovery]].
- MDL: keep motifs that reduce total description length. See [[Minimum Description Length]].
- Raw frequency: count occurrences without considering complexity.

## Correct Answers

### (a) Most Frequent Motif (by Raw Frequency)

Let's count 2-grams:

- `[W, Wi]`: Wall 1 (×2), Wall 2 (×1), Wall 3 (×3), Wall 5 (×2) = 8 occurrences.
- `[Wi, D]`: Wall 1 (×1), Wall 2 (×1), Wall 3 (×1), Wall 5 (×1) = 4 occurrences.
- `[Wi, Wi]`: Wall 1 (×1), Wall 3 (×2) = 3 occurrences.
- `[D, Wi]`: Wall 5 (×1) = 1.
- `[W, D]`: Wall 4 (×1) = 1.

The most frequent 2-gram is `[W, Wi]` (8 occurrences).

### (b) What MDL Keeps

MDL would consider the *compression* benefit:

- `[W, Wi]` as a motif: encodes 8 occurrences with 1 motif definition. Saves description length.
- `[Wi, D]` as a motif: 4 occurrences. Saves less.
- `[Wi, Wi]` as a motif: 3 occurrences. Saves even less.

MDL would likely keep `[W, Wi]` and possibly `[Wi, D]`, depending on the cost of defining each motif.

But MDL would also consider longer motifs:

- `[W, Wi, D]` appears in Wall 2 and (almost) Wall 5. Defining this motif might save description length if it recurs enough.

### (c) Why Raw Frequency Misleads

- `[W, Wi]` is frequent because it's a common 2-gram, but it's not a meaningful architectural motif (it's just "a wall segment followed by a window", which is trivial).
- A meaningful motif might be `[W, Wi, Wi, D]` (a facade unit with two windows and a door), which appears only once in this small example but is structurally meaningful.
- Raw frequency biases toward short, common patterns. MDL balances frequency with complexity.

## Common Mistakes

- Counting only 2-grams (missing longer motifs).
- Treating all motifs equally (ignoring complexity).
- Forgetting that motif overlap matters (motifs can share elements).

## Edge Cases

- In real buildings, motifs may be approximate (window sizes vary slightly). Use approximate motif matching.
- Motifs may span hierarchy levels (a "kitchen" motif includes both elements and relations).

## Implementation Considerations

Use a frequent subgraph mining library (e.g. gSpan) for graph motifs, or a frequent subtree mining library for tree motifs.

## Related Concepts

- [[Structural Motif Discovery]]
- [[Minimum Description Length]]
- [[Frequency vs Meaning]]
- [[Subtree Discovery]]
- [[Subgraph Discovery]]
