---
tags: [concept, database, schema-evolution, migrations, zero-downtime]
type: concept
status: complete
prerequisites:
  - [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
  - [[14 - Schema Evolution/02 - Backfill Migrations]]
related:
  - [[14 - Schema Evolution/05 - Flyway]]
  - [[14 - Schema Evolution/04 - Database Refactoring]]
---

# Zero-Downtime Migrations

## What it is

A **zero-downtime migration** is a schema change that's applied while the application is running, with no user-visible interruption. It combines [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract|expand-and-contract]], [[14 - Schema Evolution/02 - Backfill Migrations|chunked backfills]], and a few specific techniques for the operations that are inherently blocking.

## The blocking operations

Some schema operations lock the table in Oracle:

- **`ALTER TABLE ... ADD column NOT NULL`** with a default - locks the table briefly to update metadata. Fast on 11g+ (metadata-only default), but verify.
- **`ALTER TABLE ... MODIFY column type`** - rewrites every row. Locks the table.
- **`ALTER TABLE ... DROP column`** - marks the column unused (fast) but the physical drop (`DROP COLUMN`) locks.
- **`CREATE INDEX`** - locks the table for writes. Use `CREATE INDEX ... ONLINE` to allow concurrent writes.
- **`ALTER TABLE ... ADD CONSTRAINT`** - validates the constraint, which requires a full scan. Use `ENABLE NOVALIDATE` to skip validation, then `ENABLE VALIDATE` later.

## The non-blocking alternatives

| Blocking | Non-blocking |
|---|---|
| `ADD column NOT NULL DEFAULT x` | `ADD column NULL`, backfill, add `NOT NULL` |
| `MODIFY column type` | Add new column, backfill, switch code, drop old |
| `DROP column` | `SET UNUSED column` (fast), `DROP UNUSED COLUMNS` later |
| `CREATE INDEX` | `CREATE INDEX ... ONLINE` (allows writes, slower) |
| `ADD CONSTRAINT ... VALIDATE` | `ADD CONSTRAINT ... ENABLE NOVALIDATE`, validate later |
| `DROP TABLE` | Rename to `_old`, drop later |

## `CREATE INDEX ... ONLINE`

```sql
CREATE INDEX idx_intern_department ON intern(department_id) ONLINE;
```

`ONLINE` allows DML during the index build (it uses a journal table to capture changes and merge them at the end). The build takes longer, but the table stays writable. Essential for production indexes on live tables.

In Oracle Enterprise Edition, `ONLINE` is fully supported. In XE, `ONLINE` is **not available** - you have to schedule a maintenance window for index creation on large tables.

## `ALTER TABLE ... ADD CONSTRAINT ... ENABLE NOVALIDATE`

```sql
-- Phase 1: add the constraint without validating existing rows
ALTER TABLE intern
ADD CONSTRAINT chk_is_accepted
CHECK (is_accepted IN ('Accepted','Rejected','Pending'))
ENABLE NOVALIDATE;

-- Phase 2: validate in chunks (or one statement, if the table is small)
ALTER TABLE intern ENABLE VALIDATE CONSTRAINT chk_is_accepted;
```

`ENABLE NOVALIDATE` adds the constraint to the data dictionary but doesn't check existing rows - so the constraint applies to **future** writes, but existing bad data is allowed. `ENABLE VALIDATE` checks existing rows; if any fail, it errors.

This pattern lets you add a constraint to a large table without a long table scan blocking writes.

## `DBMS_REDEFINITION` for table rewrites

For changes that fundamentally rewrite a table (change column types, split/merge, reorganize), Oracle's `DBMS_REDEFINITION` package does it online:

1. Create an "interim" table with the new shape.
2. `DBMS_REDEFINITION.START_REDEF_TABLE` begins a snapshot-based sync.
3. The package keeps the interim table in sync with the live table via a materialized view log.
4. `DBMS_REDEFINITION.FINISH_REDEF_TABLE` swaps the names in a brief exclusive lock.

Available in Enterprise Edition only.

## The full zero-downtime playbook

For a "rename column `name` to `full_name`" on a 10M-row live table:

1. **V1 (expand)**: `ALTER TABLE intern ADD (full_name VARCHAR2(100));` - nullable, fast.
2. **V2 (backfill)**: chunked UPDATE setting `full_name = name`. See [[14 - Schema Evolution/02 - Backfill Migrations]].
3. **V3 (sync trigger)**: create a trigger that keeps `full_name` in sync with `name` on INSERT/UPDATE.
4. **Deploy new code** that reads and writes `full_name`.
5. **V4 (drop sync)**: drop the trigger.
6. **V5 (contract)**: `ALTER TABLE intern SET UNUSED COLUMN name;` (fast).
7. **V6 (cleanup)**: `ALTER TABLE intern DROP UNUSED COLUMNS;` - schedule in a low-traffic window.

At no point is the table locked for more than a fraction of a second.

## Why it matters

For 24/7 systems, downtime is revenue lost. For systems with maintenance windows, zero-downtime migrations let you deploy more frequently (no coordination overhead). The discipline of zero-downtime migrations also makes rollbacks possible - each phase is independently revertible.

## Project Connection

The project is small enough that zero-downtime isn't strictly necessary - a brief downtime during the migration is acceptable. But the **principle** matters: the reviews' redesign proposes migrations that follow expand-and-contract, so even if the project grows to 24/7, the same patterns apply.

For example, the migration from `MAX(id)+1` to IDENTITY columns follows the pattern:

1. Add `intern_id_new NUMBER GENERATED ALWAYS AS IDENTITY`.
2. Backfill `intern_id_new` (with `GENERATED BY DEFAULT` to accept explicit values from the old `intern_id`).
3. Switch the code to use `intern_id_new`.
4. Drop `intern_id`, rename `intern_id_new` to `intern_id`.

## Common pitfalls

- Forgetting that `ONLINE` index builds aren't available on XE - schedule a maintenance window.
- Adding a `NOT NULL` constraint before the backfill completes - fails on un-backfilled rows.
- Running a backfill and a deploy at the same time - the backfill's UPDATEs lock rows the deploy is trying to write.
- Skipping the deprecation period - old code that hasn't been updated breaks when the contract phase runs.

## Trade-offs

- **Complexity vs. downtime**: zero-downtime migrations are more complex (more steps, triggers, transitional structures) but eliminate downtime.
- **Time vs. safety**: chunked backfills are slower than single-statement updates but safer.

## Further reading

- [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
- [[14 - Schema Evolution/02 - Backfill Migrations]]
- Oracle Docs, "DBMS_REDEFINITION".
