---
tags: [concept, cs-foundations, data-structures]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/04 - Complexity Theory (Big-O)]]
  - [[02 - CS Foundations/08 - Memory and Pointers]]
related:
  - [[03 - Java Foundations/01 - Collections Framework]]
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# Data Structures Overview

## What it is

A data structure is a particular way of organizing data in memory so it can be used efficiently. The choice determines which operations are fast and which are slow. Every choice is a trade-off.

## The fundamental data structures

### Array
Contiguous block of `n` same-typed elements.
- Access by index: `O(1)`.
- Search (unsorted): `O(n)`.
- Insert/delete in middle: `O(n)` (shift elements).

### Linked List
Each node holds a value + reference to next. Non-contiguous.
- Access by index: `O(n)`.
- Insert/delete at known position: `O(1)`.

### Hash Table (HashMap)
Key-value pairs stored in an array. The key is hashed to compute the index.
- Get/Put (average): `O(1)`.
- Get/Put (worst case): `O(n)` (all keys collide).
- **Iteration order: undefined in `HashMap`.** Insertion order in `LinkedHashMap`. Sorted by key in `TreeMap`.

The "undefined iteration order" is a real property of `HashMap` and is the source of a real bug in the project — see Project Connection below.

### Binary Search Tree / B-tree
Tree where left subtree keys < node key < right subtree keys.
- Search/Insert/Delete: `O(log n)` if balanced, `O(n)` if degenerate.
- B-tree (database index): high fan-out, shallow tree, `O(log_f n)`.

### Stack (LIFO)
Push/pop in `O(1)`. The JVM call stack is a stack.

### Queue (FIFO)
Enqueue/dequeue in `O(1)`. Used for task scheduling, producer-consumer.

### Set
Collection with no duplicates. `HashSet` `O(1)`, `TreeSet` `O(log n)`.

### Graph
Nodes + edges. Directed/undirected, weighted/unweighted.

### Heap
Binary tree where parent > children (max-heap) or < children (min-heap). Priority queues.

## The HashMap iteration order bug

The project's `insertIntern` builds an INSERT by iterating `HashMap.keySet()` for columns and `HashMap.values()` for parameters. This works *today* because both are backed by the same internal map. But:

1. The Java spec does **not** guarantee iteration order for `HashMap`. It can change between JVM versions or even between runs.
2. If someone switches to `ConcurrentHashMap` for thread safety, the two iterations may diverge — and the INSERT will put `phone_number` in the `email` column. Silent data corruption.

The fix: use a typed domain object (`Intern`) with a hardcoded SQL string `INSERT INTO interns (name, age, ...) VALUES (?, ?, ...)` where the column order is fixed by the SQL. Or use `LinkedHashMap` (preserves insertion order). Or iterate `entrySet()` in a single loop. Best: use a typed record.

## Common pitfalls

- Using `HashMap` when order matters → `LinkedHashMap` (insertion) or `TreeMap` (sorted).
- Using a List when you need fast lookup → Set (`O(1)` contains vs List's `O(n)`).
- Using an array when you need dynamic sizing → `ArrayList`.
- Modifying a collection while iterating → `ConcurrentModificationException`. Use `Iterator.remove()` or streams.
- Assuming `ArrayList` and `LinkedList` are interchangeable → `LinkedList.get(i)` is `O(n)`.

## Project Connection

- `HashMap` iteration order bug in `oracleConnector.insertIntern/insertTheme/insertDepartment`. See [[04 - OOD and SOLID/01 - Anemic Domain Model]] and [[03 - Java Foundations/01 - Collections Framework]].
- `List<Map<String,Object>>` instead of `List<Intern>` — see [[04 - OOD and SOLID/01 - Anemic Domain Model]].
- Missing B-tree indexes on foreign keys — the database analog of "your list scans are O(n)." See [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]].

## Further reading

- *Introduction to Algorithms* (CLRS), Parts III and V.
- *Java Generics and Collections* (Naftalin & Wadler).
