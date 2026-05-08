---
tags: [queue, deque, fifo, lifo]
aliases: [queue, deque, fifo, lifo]
keywords: [queue, deque, fifo, lifo]
---


## Queue and Deque [[044 Interfaces|Interfaces]]

These interfaces are used for holding elements prior to processing.

### 1. Queue (`java.util.Queue`)
Follows **FIFO** (First-In-First-Out). Like a line at a supermarket.
*   `offer(e)`: Add to back.
*   `poll()`: Remove from front.
*   `peek()`: Look at front without removing.

### 2. Deque (`java.util.Deque`)
Pronounced "Deck". Stands for **Double Ended Queue**.
Supports insertion and removal at **both** ends.
*   Can function as a Queue (FIFO).
*   Can function as a Stack (LIFO - Last-In-First-Out).

### Implementations

#### A. ArrayDeque
*   "Resizing [[051 Arrays|array]]" implementation of Deque.
*   **Faster than `Stack`** for stack operations.
*   **Faster than `LinkedList`** for queue operations.
*   No null elements allowed.

#### B. PriorityQueue
*   Does not follow FIFO.
*   Orders elements based on **priority** (Sorted).
*   When you call `poll()`, you always get the "smallest" (or highest priority) element, not the oldest one.
*   Useful for scheduling tasks (e.g., "Process critical bug before UI fix").

#### C. [[054 List Interface|LinkedList]] (Again)
*   `LinkedList` implements `Deque`!
*   It can be used as a Queue or a Stack.


---
**Keywords:** #queue, #deque, #fifo, #lifo
