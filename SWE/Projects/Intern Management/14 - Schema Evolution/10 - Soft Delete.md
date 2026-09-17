---
tags: [concept, database, schema-evolution, soft-delete]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/02 - Constraints]]
related:
  - [[14 - Schema Evolution/01 - Audit Columns]]
  - [[14 - Schema Evolution/12 - Temporal Tables]]
  - [[12 - Advanced Database Features/01 - Audit Logs]]
---

# Soft Delete

## What it is

**Soft delete** is the pattern of marking a row as deleted instead of physically deleting it. A `deleted_at TIMESTAMP` column (NULL = not deleted) is the canonical implementation; queries add `WHERE deleted_at IS NULL` to filter out deleted rows.

```sql
ALTER TABLE intern ADD (deleted_at TIMESTAMP);

-- "Delete" an intern
UPDATE intern SET deleted_at = SYSTIMESTAMP WHERE intern_id = 42;

-- Query only active interns
SELECT * FROM intern WHERE deleted_at IS NULL;
```

## Why it exists

Physical `DELETE` is **irreversible**. Once the row is gone:

- You can't recover from a mistake ("I deleted the wrong intern").
- You can't audit ("when did intern 42 leave, and who did it?").
- You can't undo a bug ("the script deleted 1000 interns by accident").
- Foreign keys cascade - deleting a department might cascade-delete its interns, losing data forever.

Soft delete keeps the row around. The data is recoverable; the audit log is complete; the FK cascades can be deferred or undone.

## Implementation choices

### 1. `deleted_at TIMESTAMP` (NULL = active)

The standard. The timestamp records **when** the row was soft-deleted.

```sql
SELECT * FROM intern WHERE deleted_at IS NULL;
```

### 2. `is_deleted CHAR(1)` flag

Simpler but loses the "when". Use only if you never need the deletion time.

### 3. `deleted_at` + `deleted_by`

Tracks who deleted the row, in addition to when.

```sql
ALTER TABLE intern ADD (deleted_at TIMESTAMP, deleted_by VARCHAR2(100));

UPDATE intern
SET    deleted_at = SYSTIMESTAMP,
       deleted_by = SYS_CONTEXT('USERENV','SESSION_USER')
WHERE  intern_id = 42;
```

### 4. Move to a `_deleted` table

Move the soft-deleted row to a separate `intern_deleted` table, leaving the main table clean. Trades query complexity (no `WHERE deleted_at IS NULL` needed) for storage complexity (two tables to maintain).

## Query-level filtering

Every query must remember `WHERE deleted_at IS NULL`. Forgetting it leaks deleted rows into the result. Options to enforce:

- **Application discipline** - every repository method adds the filter. Brittle.
- **View** - create a view `intern_active AS SELECT * FROM intern WHERE deleted_at IS NULL`; query the view, not the table.
- **VPD policy** - automatically append `deleted_at IS NULL` to every query on `intern`. See [[12 - Advanced Database Features/16 - VPD - Virtual Private Database]]. The most robust option.
- **Hibernate `@Where` annotation** - `@Where(clause = "deleted_at IS NULL")` on the entity. ORM-level enforcement.

## Trade-offs

- **Storage**: soft-deleted rows stay in the table. For high-churn tables, the dead rows accumulate. Periodically purge (or archive) old soft-deleted rows.
- **Index size**: indexes include the dead rows. Query plans may degrade. Periodically rebuild.
- **Constraint complexity**: a UNIQUE constraint on `email` would prevent re-creating a soft-deleted user's email. Solutions: include `deleted_at` in the unique constraint (`UNIQUE (email, deleted_at)`), or use a partial index (Oracle doesn't have partial indexes directly; use a function-based index with `DECODE`).
- **Query complexity**: every query has `WHERE deleted_at IS NULL`. Easy to forget; VPD or views mitigate.

## Project Connection

The project does **hard delete**:

```java
String sql = "DELETE FROM "intern" WHERE intern_id = " + id;
```

Once executed, the intern is gone - no audit trail, no recovery. The reviews' redesign proposes:

```sql
ALTER TABLE intern ADD (
    deleted_at TIMESTAMP,
    deleted_by VARCHAR2(100)
);
```

And a VPD policy (or application discipline) that filters `deleted_at IS NULL` from every query.

## Common pitfalls

- Forgetting `WHERE deleted_at IS NULL` in one query - deleted rows leak in.
- Using `UNIQUE (email)` and then being unable to re-register with a soft-deleted email.
- Soft-deleting and never purging - the table grows without bound.
- Soft-deleting a parent without soft-deleting children - orphans appear.

## Further reading

- Fowler, P of EAA, "Soft Delete".
- [[14 - Schema Evolution/01 - Audit Columns]]
- [[12 - Advanced Database Features/16 - VPD - Virtual Private Database]]
