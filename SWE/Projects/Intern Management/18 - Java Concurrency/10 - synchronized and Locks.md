---
tags: [concept, concurrency, synchronized, locks]
type: concept
status: complete
prerequisites:
  - [[18 - Java Concurrency/05 - Java Memory Model]]
---

# synchronized and Locks

## synchronized

```java
// Method-level
public synchronized void increment() { count++; }

// Block-level
private final Object lock = new Object();
public void increment() {
    synchronized (lock) {
        count++;
    }
}
```

`synchronized` provides:
- **Mutual exclusion** — only one thread holds the lock at a time.
- **Memory barrier** — writes inside are visible to the next thread that acquires the lock.

## ReentrantLock

```java
private final ReentrantLock lock = new ReentrantLock();

public void increment() {
    lock.lock();
    try {
        count++;
    } finally {
        lock.unlock();
    }
}
```

More flexible than `synchronized`:
- `tryLock()` — non-blocking attempt.
- `tryLock(timeout)` — timed attempt.
- `lockInterruptibly()` — can be interrupted.
- Fairness — `new ReentrantLock(true)` serves the longest-waiting thread first.

## ReadWriteLock

```java
private final ReadWriteLock rwLock = new ReentrantReadWriteLock();

public Intern read(long id) {
    rwLock.readLock().lock();
    try { return cache.get(id); }
    finally { rwLock.readLock().unlock(); }
}

public void write(Intern intern) {
    rwLock.writeLock().lock();
    try { cache.put(intern.getId(), intern); }
    finally { rwLock.writeLock().unlock(); }
}
```

Multiple readers, one writer. Good for read-heavy caches.

## StampedLock (Java 8+)

Optimistic reads:
```java
private final StampedLock lock = new StampedLock();

public Intern read(long id) {
    long stamp = lock.tryOptimisticRead();
    Intern intern = cache.get(id);
    if (lock.validate(stamp)) return intern;  // no writer occurred
    stamp = lock.readLock();
    try { return cache.get(id); }
    finally { lock.unlockRead(stamp); }
}
```

Faster than ReadWriteLock for read-heavy workloads.

## When to use which

- **`synchronized`** — simple, sufficient for most cases.
- **`ReentrantLock`** — need `tryLock`, interruptibility, or fairness.
- **`ReadWriteLock`** — read-heavy data with occasional writes.
- **`StampedLock`** — extreme read-heavy performance.

## Common pitfalls

- **Forgetting to unlock** — always use try-finally.
- **Locking on the wrong object** — don't lock on a string literal or `this` (other code may lock on the same).
- **Deadlock** — acquiring locks in different orders. See [[10 - Transactions and Concurrency/04 - Deadlocks]].
- **Holding a lock too long** — do I/O outside the lock.

## Project Connection

The project doesn't use `synchronized` at all — shared state (`static Connection`, `static labelText`) is unprotected. The fix: avoid shared state (connection pool, controller injection). Where shared state is unavoidable, use `synchronized` or `java.util.concurrent` utilities.

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapters 4-5.
