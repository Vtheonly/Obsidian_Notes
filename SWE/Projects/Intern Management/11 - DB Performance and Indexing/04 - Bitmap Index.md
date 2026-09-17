---
tags: [concept, database, indexing, bitmap]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# Bitmap Index

## What it is

A **bitmap index** stores a bitmap (bit array) for each distinct value. Bit `i` is 1 if row `i` has that value, 0 otherwise.

```
Column: status (values: 'Pending', 'Accepted', 'Rejected')

Bitmap for 'Pending':  10100010...
Bitmap for 'Accepted': 01010100...
Bitmap for 'Rejected': 00001001...
```

## When to use

- **Low cardinality** columns (few distinct values): `status`, `gender`, `is_active`.
- **Read-heavy** tables (bitmaps are slow to update).
- **Data warehouse** queries with many AND/OR conditions (bitmaps can be combined with bitwise operations).

## When NOT to use

- **High cardinality** columns (use B-tree).
- **Write-heavy** tables (every update locks the entire bitmap — severe contention).
- **OLTP** (online transaction processing) — too much write contention.

## Combining bitmaps

```sql
SELECT * FROM interns WHERE status = 'Pending' AND department_id = 5;
```

Oracle can AND the bitmaps for `status='Pending'` and `department_id=5` (bitwise AND), then read only the matching rows. Very fast for low-cardinality combinations.

## Project Connection

The advanced redesign uses bitmap indexes on `interns.status` and `users.status` — both low-cardinality columns. Combined with interval partitioning, this makes "find all pending interns" very fast.

```sql
CREATE BITMAP INDEX bmp_interns_status ON interns(status) LOCAL;
```

`LOCAL` means the index is partitioned to match the table (one bitmap per partition).

## Further reading

- Oracle Database Data Warehousing Guide — Bitmap Indexes.
