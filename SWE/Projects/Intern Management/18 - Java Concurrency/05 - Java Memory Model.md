---
tags: [concept, concurrency, jmm, memory-model]
type: concept
status: complete
related:
  - [[18 - Java Concurrency/06 - Race Conditions]]
  - [[18 - Java Concurrency/10 - synchronized and Locks]]
---

# Java Memory Model (JMM)

## What it is

The **Java Memory Model** (JLS §17) defines how threads interact through memory. It specifies:
- When a write by one thread is visible to another.
- The ordering of reads and writes.
- What guarantees you have without synchronization.

## The problem

Without synchronization, threads can see stale or inconsistent values:

```java
class Counter {
    private int count = 0;
    public void increment() { count++; }
    public int get() { return count; }
}
```

If two threads call `increment()` 10,000 times each, the final count is often less than 20,000. Why?
1. `count++` is not atomic — it's read, add, write.
2. Without synchronization, threads can read stale values.
3. Writes can be reordered by the CPU or compiler.

## Visibility

A write by thread A is not immediately visible to thread B. The CPU caches values; the compiler reorders instructions. Without a **happens-before** relationship, B may never see A's write.

## Happens-before

A write `W` happens-before a read `R` if:
- `W` and `R` are in the same thread, and `W` comes first.
- `W` is in thread A, `R` is in thread B, and there's a synchronization action (lock, volatile, thread start, thread join) connecting them.

If `W` happens-before `R`, then `R` sees `W` (and all writes before `W`).

## `volatile`

```java
private volatile boolean running = true;

// Thread A
while (running) { ... }

// Thread B
running = false;  // visible to A immediately
```

`volatile` ensures:
- **Visibility** — writes are immediately visible to other threads.
- **Prevents reordering** — the compiler/CPU can't reorder volatile accesses.

But `volatile` does **not** make `count++` atomic. Use `AtomicInteger` for that.

## `synchronized`

```java
public synchronized void increment() { count++; }
```

- Mutual exclusion — only one thread can execute this method at a time.
- Memory barrier — all writes inside the synchronized block are visible to the next thread that acquires the lock.

## The project's JMM bugs

1. `static Connection connection` — shared across threads. Without synchronization, two threads can corrupt the connection's state.
2. `static String labelText` — shared between controllers. Two clicks can race.
3. `oracleConnector` has no synchronization — every method is a race waiting to happen.

## The fix

- Use a connection pool (each thread has its own connection).
- Don't share mutable state via `static` fields.
- Use `ExecutorService` for background work.
- Use `synchronized`, `volatile`, or `java.util.concurrent` for shared state.

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapter 3.
- JLS §17.
