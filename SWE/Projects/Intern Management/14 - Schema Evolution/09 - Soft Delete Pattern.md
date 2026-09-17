---
tags: [concept, database, soft-delete, pattern]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/01 - Audit Columns]]
---

# Soft Delete Pattern

## What it is

Instead of `DELETE FROM interns WHERE intern_id = 123` (hard delete — row gone forever), soft delete marks the row as deleted:

```sql
UPDATE interns SET deleted_at = SYSTIMESTAMP WHERE intern_id = 123;
```

Queries filter out deleted rows:
```sql
SELECT * FROM interns WHERE deleted_at IS NULL;
```

## Why

- **Recovery** — accidental deletes can be undone.
- **Audit** — know that a record existed, even after deletion.
- **Referential integrity** — child rows don't lose their parent.
- **Compliance** — GDPR may require retention periods before deletion.

## Trade-offs

- **Storage** — deleted rows still take space.
- **Query complexity** — every query must include `WHERE deleted_at IS NULL`.
- **Unique constraints** — `UNIQUE(email)` prevents reusing a deleted user's email. Workaround: `UNIQUE(email, deleted_at)` (NULL is treated as unique in Oracle).
- **Performance** — the table grows; indexes must include the filter.

## When to use

- **Regulated industries** — finance, healthcare, where deletion requires retention.
- **User accounts** — allow "deactivate" instead of hard delete.
- **Anything auditable**.

## When NOT to use

- **Truly ephemeral data** — session tokens, cache entries.
- **GDPR right to erasure** — sometimes you must hard-delete (after the retention period).

## Project Connection

The project's `deleteIntern` / `deleteWorkerUser` / `deleteTheme` / `deleteDepartment` all do hard DELETE. The fix: add `deleted_at TIMESTAMP` to every table, change DELETE to UPDATE, and add `WHERE deleted_at IS NULL` to all queries.

The advanced redesign includes `deleted_at` on `departments`, `users`, `themes`, `interns`.

## Further reading

- *SQL Antipatterns* (Karwin), "Phantom Files" (soft delete).
