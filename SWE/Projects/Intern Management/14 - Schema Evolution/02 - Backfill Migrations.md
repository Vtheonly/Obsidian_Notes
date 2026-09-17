---
tags: [concept, database, schema-evolution, migrations, backfill]
type: concept
status: complete
prerequisites:
  - [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
related:
  - [[14 - Schema Evolution/05 - Flyway]]
  - [[14 - Schema Evolution/14 - Zero-Downtime Migrations]]
---

# Backfill Migrations

## What it is

A **backfill migration** populates data for a new column (or table) from existing data. It's the "Migrate" phase of [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract|expand-and-contract]] - the work of getting existing rows into the new shape.

## The pattern

```sql
-- Phase 1 (expand): add the new column, nullable
ALTER TABLE intern ADD (full_name VARCHAR2(100));

-- Phase 1.5 (backfill): populate it from existing data
UPDATE intern SET full_name = name WHERE full_name IS NULL;
COMMIT;

-- Phase 1.6: add NOT NULL constraint, now that every row has a value
ALTER TABLE intern MODIFY (full_name VARCHAR2(100) NOT NULL);
```

## The problem with a single UPDATE

For a 10-million-row table, a single `UPDATE intern SET full_name = name` is:

- **Slow** - one transaction, full scan, lots of undo and redo.
- **Blocking** - locks every row for the duration.
- **All-or-nothing** - if it fails at row 9,999,999, the whole thing rolls back.

## Chunked backfill

Run the UPDATE in chunks, committing each chunk:

```sql
-- Backfill in chunks of 10,000 rows
DECLARE
    CURSOR c IS SELECT intern_id, name FROM intern WHERE full_name IS NULL;
    TYPE id_t IS TABLE OF intern.intern_id%TYPE;
    TYPE name_t IS TABLE OF intern.name%TYPE;
    l_ids id_t;
    l_names name_t;
BEGIN
    OPEN c;
    LOOP
        FETCH c BULK COLLECT INTO l_ids, l_names LIMIT 10000;
        EXIT WHEN l_ids.COUNT = 0;

        FORALL i IN 1..l_ids.COUNT
            UPDATE intern SET full_name = l_names(i) WHERE intern_id = l_ids(i);

        COMMIT;
    END LOOP;
    CLOSE c;
END;
/
```

Each chunk is a separate transaction; locks release between chunks; failure resumes from the last committed chunk.

## Chunked backfill in Java

```java
public void backfillFullName(JdbcTemplate jdbc) {
    int chunkSize = 10_000;
    long lastId = 0;
    while (true) {
        List<Long> ids = jdbc.queryForList(
            "SELECT intern_id FROM intern WHERE full_name IS NULL AND intern_id > ? ORDER BY intern_id FETCH FIRST ? ROWS ONLY",
            Long.class, lastId, chunkSize);
        if (ids.isEmpty()) break;

        jdbc.batchUpdate(
            "UPDATE intern SET full_name = name WHERE intern_id = ?",
            ids, chunkSize,
            (ps, id) -> ps.setLong(1, id));

        lastId = ids.get(ids.size() - 1);
    }
}
```

## The "online" backfill

For tables that can't afford any lock contention, use the **online redefinition** pattern:

1. Create a new table (`intern_new`) with the new schema.
2. Backfill `intern_new` from `intern` in chunks (as above).
3. Keep `intern_new` in sync with `intern` via a materialized view log or trigger.
4. In a final, brief switchover, rename `intern` to `intern_old`, rename `intern_new` to `intern`.

This is the gold-standard pattern for large tables; it's what `DBMS_REDEFINITION` automates.

## Why it matters

The backfill is the most error-prone part of a schema migration. A naive `UPDATE` on a large table can:

- Lock the table for hours.
- Exhaust the undo tablespace.
- Fail at 99% and roll back everything.

A chunked backfill avoids all three. It's slower (more commits) but safer and resumable.

## Project Connection

The project's `insertion.sql` has sample data that stores plaintext `'rootroot'` as `password_hash`. The redesign migrates to Argon2id hashes - a backfill:

```sql
-- V10__hash_sample_passwords.sql
-- Backfill: hash the plaintext passwords.
-- (In production, this would be a Java migration that uses the Argon2 library.)
DECLARE
    CURSOR c IS SELECT user_id, password_hash FROM worker_user;
BEGIN
    FOR r IN c LOOP
        -- In real life, call a Java stored procedure or external script
        -- to compute the Argon2 hash of r.password_hash.
        UPDATE worker_user
        SET    password_hash = compute_argon2(r.password_hash)
        WHERE  user_id = r.user_id;
        COMMIT;
    END LOOP;
END;
/
```

(For a small sample dataset, the loop is fine. For a million users, chunk it.)

## Common pitfalls

- Running a backfill as a single transaction - exhausts undo, locks everything.
- Forgetting to commit between chunks - same as a single transaction.
- Backfilling while the app is writing - the backfill misses new rows (or worse, races with them). Use a trigger to capture changes during the backfill, or schedule a maintenance window.
- Adding a NOT NULL constraint before the backfill completes - fails on rows that haven't been backfilled.

## Trade-offs

- **Chunk size vs. commit overhead**: smaller chunks = more commits = slower, but less undo and shorter locks. 10,000 is a reasonable default.
- **Online vs. offline**: online backfill (with triggers) is more complex but allows the app to keep running. Offline is simpler but requires downtime.

## Further reading

- [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
- [[14 - Schema Evolution/14 - Zero-Downtime Migrations]]
- Oracle Docs, "DBMS_REDEFINITION".
