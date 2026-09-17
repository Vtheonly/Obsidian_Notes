---
tags: [concept, database, transactions, concurrency, pattern]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/07 - Locking and Lock Types]]
related:
  - [[10 - Transactions and Concurrency/04 - Deadlocks]]
  - [[05 - Software Architecture/18 - Unit of Work Pattern]]
---

# Optimistic vs Pessimistic Concurrency

## What it is

Two strategies for handling concurrent updates to the same row.

### Pessimistic

Assume conflicts will happen. **Lock the row when you read it; hold the lock until you commit.** No one else can update it during that window.

```sql
-- Load the intern for editing
SELECT intern_id, name, is_accepted
FROM   intern
WHERE  intern_id = 42
FOR UPDATE;     -- holds the lock until COMMIT/ROLLBACK

-- (user edits the form for 30 seconds)

UPDATE intern SET name = ?, is_accepted = ?
WHERE  intern_id = 42;
COMMIT;          -- releases the lock
```

### Optimistic

Assume conflicts are rare. **Don't lock when you read; check at update time that no one else changed the row.** If they did, fail and let the user retry.

```sql
-- Load the intern (no lock)
SELECT intern_id, name, is_accepted, version
FROM   intern
WHERE  intern_id = 42;
-- returns version = 7

-- (user edits for 30 seconds)

UPDATE intern
SET    name = ?, is_accepted = ?, version = version + 1
WHERE  intern_id = 42 AND version = 7;
-- if affected rows = 0, someone else updated; tell the user and refresh
COMMIT;
```

## Comparison

| Aspect | Pessimistic | Optimistic |
|---|---|---|
| Conflict assumption | Frequent | Rare |
| Lock duration | Whole transaction | None |
| Deadlock risk | Yes | No |
| Throughput under contention | Lower (waits) | Higher (retries) |
| User experience on conflict | Wait, then succeed | Fail, then must retry |
| Implementation complexity | Simpler (DB does it) | Needs a version column + retry logic |
| Holds locks across user input | Yes (dangerous) | No |

## When to use which

- **Pessimistic** when:
  - Conflicts are common (many users edit the same rows).
  - The cost of a retry is high (long transactions, expensive recomputation).
  - You can keep the transaction short (sub-second, not "across user think time").

- **Optimistic** when:
  - Conflicts are rare (most edits touch disjoint rows).
  - The transaction spans user think time (a user opens a form, goes to lunch, comes back, clicks Save).
  - You want to avoid deadlocks.

For most web/CRUD apps with human-in-the-loop editing, **optimistic is the default**.

## The version column

The standard implementation: add a `version NUMBER` column, increment it on every update, and include `WHERE version = ?` in the update. If the update affects zero rows, the row was changed by someone else.

```sql
ALTER TABLE intern ADD (version NUMBER DEFAULT 0 NOT NULL);

UPDATE intern
SET    name = :name, is_accepted = :status, version = version + 1
WHERE  intern_id = :id AND version = :expected_version;
```

An alternative is a `last_updated_at TIMESTAMP` column - same idea, compare the timestamp instead of a counter. The counter is simpler; the timestamp also gives you "when was this last changed."

## Hibernate / JPA support

```java
@Entity
public class Intern {
    @Id Long id;
    @Version Long version;   // JPA manages this automatically
    String name;
    ...
}
```

On update, JPA adds `WHERE version = ?` for you. If the row was changed, you get `OptimisticLockException`.

## Project Connection

The project does **neither**. Updates are:

```java
String sql = "UPDATE "intern" SET name=?, is_accepted=? WHERE intern_id=?";
```

No lock, no version check. Two users can open the same intern, both edit, both save - the second save silently overwrites the first. This is the **lost update** anomaly, and it's the most common concurrency bug in CRUD apps.

The fix in the redesign is a `version` column and optimistic locking:

```sql
ALTER TABLE intern ADD (version NUMBER DEFAULT 0 NOT NULL);

UPDATE intern
SET    name = ?, is_accepted = ?, version = version + 1
WHERE  intern_id = ? AND version = ?;
-- check affected rows; if 0, tell the user the row was changed by someone else
```

## Common pitfalls

- Using optimistic locking but **not checking the affected row count** - the update "succeeds" (no exception) but updated nothing, and the application proceeds as if it saved.
- Using pessimistic locking across user think time - locks held for minutes kill throughput and cause deadlocks.
- Forgetting that `@Version` in JPA requires a non-null initial value - insert with `version = 0` (or let the column default handle it).

## Further reading

- Fowler, P of EAA, "Optimistic Offline Lock" and "Pessimistic Offline Lock".
- [[10 - Transactions and Concurrency/07 - Locking and Lock Types]]
- [[10 - Transactions and Concurrency/04 - Deadlocks]]
