---
tags: [concept, database, deadlocks, concurrency]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/06 - Locking (Row, Table, TM, TX)]]
---

# Deadlocks

## What it is

A **deadlock** is when two transactions are each waiting for a lock the other holds. Neither can proceed.

```
Transaction A: locks row 1, wants row 2.
Transaction B: locks row 2, wants row 1.
→ Deadlock. Both wait forever.
```

## Oracle's detection

Oracle automatically detects deadlocks (within seconds) and resolves them by **killing one transaction** (the one that detected the deadlock). The killed transaction gets `ORA-00060: deadlock detected while waiting for resource`. The other transaction proceeds.

## Prevention

1. **Consistent lock ordering** — always lock resources in the same order. If A locks row 1 before row 2, B should too. No deadlock.
2. **Keep transactions short** — shorter transactions hold locks for less time, reducing deadlock window.
3. **Use the lowest isolation level that works** — higher isolation = more locking = more deadlock risk.
4. **Index FKs** — unindexed FKs cause table locks, which increase deadlock risk.

## Handling deadlocks in application code

```java
try {
    transaction.run(() -> {
        internRepository.update(...);
        assignmentRepository.update(...);
    });
} catch (DeadlockLoserDataAccessException e) {
    // Retry
    transaction.run(() -> { ... });
}
```

Spring's `DeadlockLoserDataAccessException` and Resilience4j's Retry can handle this.

## Project Connection

The project's `MAX(id)+1` is a deadlock-prone pattern: two concurrent inserts both scan the table for MAX, both try to insert the same ID, one fails. With IDENTITY columns, this doesn't happen — the DB generates IDs without contention.

## Further reading

- Oracle Database Concepts — Deadlocks.
- *Java Concurrency in Practice* (Goetz), Chapter 10.
