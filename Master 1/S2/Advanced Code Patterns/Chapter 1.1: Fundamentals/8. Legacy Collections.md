
## Legacy Collections (The History Lesson)

Java 1.0 (1996) had a few container classes. When Java 1.2 introduced the Collections Framework (1998), these old classes were "retrofitted" to work with the new interfaces, but they carry historical baggage.

### 1. Vector
*   **What it is**: An old version of `ArrayList`.
*   **The Problem**: It is **Synchronized** (Thread-Safe).
*   **Why that's bad**: Synchronization adds significant performance overhead. In 99% of cases, you are working on a single thread, so you pay a "speed tax" for safety you don't need.
*   **Replacement**: Use `ArrayList`. If you strictly need thread safety, use `CopyOnWriteArrayList` or `Collections.synchronizedList()`.

### 2. Stack
*   **What it is**: An extension of `Vector` representing LIFO (Last-In-First-Out).
*   **The Problem**: It inherits from Vector, so it is also slow/synchronized. It also breaks OOP principles (since it inherits methods like `add(index)` which shouldn't exist in a stack).
*   **Replacement**: Use `ArrayDeque` for stacks.

### 3. Hashtable
*   **What it is**: An old version of `HashMap`.
*   **The Problem**: Synchronized (Slow). Does not allow null keys/values.
*   **Replacement**: Use `HashMap` (or `ConcurrentHashMap` for multi-threading).

> [!SUMMARY]
> **Legacy Rule**
> If you see `Vector`, `Stack`, or `Hashtable` in code, it is likely code written before 1998 or by someone who learned Java from very old tutorials. **Avoid them.**
