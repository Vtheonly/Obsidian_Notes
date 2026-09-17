---
tags: [concept, concurrency, collections, atomic]
type: concept
status: complete
prerequisites:
  - [[18 - Java Concurrency/05 - Java Memory Model]]
---

# Concurrent Collections

## The problem

`ArrayList`, `HashMap`, etc. are not thread-safe. Concurrent access can corrupt them.

```java
Map<String, Integer> map = new HashMap<>();
// Thread A: map.put("a", 1);
// Thread B: map.put("b", 2);
// Both resize the internal array simultaneously → corruption
```

## Solutions

### synchronized wrappers (legacy)
```java
Map<String, Integer> map = Collections.synchronizedMap(new HashMap<>());
```
Wraps every method in `synchronized`. Slow (locks on every operation).

### ConcurrentHashMap (preferred)
```java
ConcurrentMap<String, Integer> map = new ConcurrentHashMap<>();
```
- Lock-striping (Java 7) or CAS (Java 8+) — multiple threads can read/write different buckets simultaneously.
- Weakly consistent iterators — don't throw `ConcurrentModificationException`, but may not reflect concurrent modifications.
- No null keys or values.

### CopyOnWriteArrayList
```java
List<String> list = new CopyOnWriteArrayList<>();
```
- Every write creates a new copy of the array.
- Reads are lock-free.
- Best for read-heavy lists with infrequent writes (e.g., listener lists).

## Atomics

```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();  // atomic, lock-free
counter.compareAndSet(0, 1);  // CAS

AtomicLong, AtomicBoolean, AtomicReference
LongAdder, LongAccumulator  // high-throughput counters
```

Use instead of `synchronized` for single-variable operations.

## When to use which

| Need | Use |
|---|---|
| Concurrent map | `ConcurrentHashMap` |
| Concurrent list (read-heavy) | `CopyOnWriteArrayList` |
| Concurrent queue | `ConcurrentLinkedQueue` (unbounded) or `LinkedBlockingQueue` (bounded) |
| Counter | `AtomicInteger` / `LongAdder` |
| Single reference | `AtomicReference` |

## Project Connection

The project doesn't use concurrent collections (it's single-threaded). The fix, when adding concurrency, should use:
- `ConcurrentHashMap` for a session cache.
- `CopyOnWriteArrayList` for event listeners.
- `AtomicInteger` for metrics counters.

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapter 5.
