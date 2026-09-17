---
tags: [concept, database, locking, optimistic, pessimistic]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/06 - Locking (Row, Table, TM, TX)]]
---

# Optimistic vs Pessimistic Locking

## Pessimistic locking
Assume conflicts will happen. Lock the row when you read it; hold the lock until you commit.

```sql
-- Oracle
SELECT * FROM interns WHERE intern_id = 123 FOR UPDATE;
-- Row is locked. Other transactions must wait to update.
```

Pro: no conflicts possible.
Con: locks held for the whole transaction; reduces concurrency; risk of deadlocks.

## Optimistic locking
Assume conflicts are rare. Don't lock. When updating, check that the row hasn't changed since you read it.

```sql
-- Add a version column
ALTER TABLE interns ADD COLUMN version NUMBER DEFAULT 0;

-- Read
SELECT intern_id, name, version FROM interns WHERE intern_id = 123;
-- Returns version = 5

-- Update (check version)
UPDATE interns SET name = 'Alice', version = version + 1
WHERE intern_id = 123 AND version = 5;
-- If 0 rows updated, someone else changed it. Retry or fail.
```

Pro: no locks held; high concurrency.
Con: retries needed on conflict; wasted work on conflict.

## When to use which

- **Pessimistic** — high contention (many transactions on the same row), short transactions, must-not-fail updates.
- **Optimistic** — low contention, long transactions (don't want to hold locks), read-heavy with occasional writes.

Most web/desktop apps use **optimistic locking** — conflicts are rare, and the version check is cheap.

## JPA optimistic locking

```java
@Entity
public class Intern {
    @Id Long id;
    @Version Long version;  // JPA manages this
    String name;
}
```

JPA automatically adds `AND version = ?` to UPDATE. If the version changed, throws `OptimisticLockException`.

## Project Connection

The project has no locking strategy — it uses auto-commit, last-write-wins. If two users edit the same intern simultaneously, the second overwrites the first silently.

The fix: add a `version` column to every table; use optimistic locking in the repository.

## Further reading

- *Patterns of Enterprise Application Architecture* (Fowler), "Optimistic Offline Lock" and "Pessimistic Offline Lock".
