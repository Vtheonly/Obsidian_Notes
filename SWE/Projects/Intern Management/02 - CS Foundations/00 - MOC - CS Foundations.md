---
tags: [moc, cs-foundations]
type: moc
status: complete
---

# MOC — Computer Science Foundations

> Before reasoning about *why* an algorithm is slow or *why* a race condition
> occurs, you need the vocabulary. This chapter gives you that vocabulary.

## Notes (read in order)

1. [[02 - CS Foundations/09 - Number Systems and Binary]] — integer overflow, two's complement.
2. [[02 - CS Foundations/02 - Boolean Logic]] — the algebra behind every `if` and SQL `WHERE`.
3. [[02 - CS Foundations/04 - Complexity Theory (Big-O)]] — the language engineers use to talk about performance.
4. [[02 - CS Foundations/05 - Data Structures Overview]] — arrays, lists, maps, sets, trees, hash tables.
5. [[02 - CS Foundations/01 - Algorithms Overview]] — sorting, searching, recursion. The B-tree is a self-balancing tree.
6. [[02 - CS Foundations/08 - Memory and Pointers]] — stack vs heap. Why Java's `==` is reference equality.
7. [[02 - CS Foundations/10 - Processes and Threads (OS view)]] — what a thread *actually is* before JavaFX threading.
8. [[02 - CS Foundations/06 - Floating Point and Numeric Precision]] — why `NUMBER(10)` ≠ `int` and why phone numbers are strings.
9. [[02 - CS Foundations/03 - Character Encoding (Unicode, UTF-8)]] — why `getBytes()` without a charset is a bug.
10. [[02 - CS Foundations/11 - State Machines]] — the conceptual basis for the UI State Machine pattern.
11. [[02 - CS Foundations/07 - Information Theory (Entropy, Compression)]] — why column compression works, why hashes are one-way.

## Why this chapter matters

- Big-O is required to understand why `MAX(id)+1` is `O(N)` and indexed lookups are `O(log N)`.
- OS threads are required to understand the JavaFX Application Thread.
- Hash tables are required to understand the `HashMap` iteration order bug.
- Memory/pointers is required to understand the `value == ""` bug.
