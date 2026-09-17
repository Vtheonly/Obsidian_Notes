---
tags: [concept, database, iot, indexing]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# Index-Organized Tables (IOT)

## What it is

An **Index-Organized Table** stores the entire row inside a B-tree index, sorted by the primary key. There's no separate "table" — the index *is* the table.

```sql
CREATE TABLE roles (
    role_id NUMBER(10) PRIMARY KEY,
    role_name VARCHAR2(50),
    description VARCHAR2(255)
) ORGANIZATION INDEX;
```

## Difference from a regular table

**Regular table (heap-organized):**
- Table: rows stored in no particular order.
- PK index: (PK value, ROWID) → points to the row.

**IOT:**
- The entire row is stored in the B-tree, sorted by PK.
- No ROWID pointer — the row *is* in the index.

## Benefits

- **Faster PK lookups** — one read (the index) instead of two (index + table).
- **Smaller storage** — no separate table.
- **Range scans on PK are fast** — rows are sorted.

## Trade-offs

- **Slower inserts** — the B-tree must be kept sorted.
- **Secondary indexes are slower** — they point to PKs (logical ROWIDs), not physical ROWIDs, requiring an extra lookup.
- **No `ROWID` pseudo-column** — use `UROWID` instead.

## When to use

- **Lookup tables** — small, read-heavy, PK lookups. `roles`, `countries`, `currencies`.
- **Tables queried mostly by PK** — configuration tables.

## When NOT to use

- **Write-heavy tables** — B-tree maintenance is expensive.
- **Tables with many secondary indexes** — secondary index lookups are slower.
- **Tables without a natural PK order** — no benefit.

## Project Connection

The advanced redesign uses IOT for `roles` — a small, read-heavy lookup table:

```sql
CREATE TABLE roles (
    role_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR2(50) NOT NULL,
    description VARCHAR2(255)
) ORGANIZATION INDEX;
```

Role lookups (`JOIN users ON users.role_id = roles.role_id`) are now O(log n) without a table access.

## Further reading

- Oracle Database Administrator's Guide — Index-Organized Tables.
