---
tags: [concept, database, performance, indexing, bitmap]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
related:
  - [[11 - DB Performance and Indexing/13 - Function-Based Indexes]]
  - [[11 - DB Performance and Indexing/07 - Composite Indexes]]
---

# Bitmap Indexes

## What it is

A **bitmap index** stores, for each distinct value, a bitmap with one bit per row in the table. A `1` means "this row has this value"; a `0` means "this row does not."

```
Value  Bitmask (one bit per row)
'Accepted'  1 0 0 1 0 1 0 0 1   <-- rows 1, 4, 6, 9 are Accepted
'Rejected'  0 1 0 0 1 0 0 1 0
'Pending'   0 0 1 0 0 0 1 0 0
```

For a column with 3 values, that's 3 bitmaps of N bits each. For low-cardinality columns (gender, status, yes/no flags, region), bitmap indexes are tiny and fast.

## Creating a bitmap index

```sql
CREATE BITMAP INDEX bm_intern_status ON intern(is_accepted);
CREATE BITMAP INDEX bm_intern_active ON intern(is_active);
```

## Bitmap vs B-tree

| Aspect | B-tree | Bitmap |
|---|---|---|
| Cardinality | High (unique-ish) | Low (< 100 distinct values) |
| Storage | Moderate | Tiny for low-cardinality |
| Read speed | Fast single-row lookup | Fast for "WHERE status = 'Pending'" |
| Combine predicates | One index at a time, then filter | Bitmap AND/OR is super fast |
| Write cost | Moderate (split a leaf) | **Very high** (rewrite the whole bitmap) |

The killer feature of bitmap indexes is **bitmap AND/OR**: combining two predicates is a bitwise operation, which is CPU-cheap and vectorizes beautifully. `WHERE status = 'Pending' AND region = 'West'` becomes `(bitmap_status_pending) AND (bitmap_region_west)` - one instruction per bit.

## When to use a bitmap index

- **Low-cardinality columns** with few distinct values (status, gender, boolean flags, region codes).
- **Read-mostly tables** - data warehouses, dimension tables, reporting.
- **Multi-predicate queries** - the bitmap AND/OR shines.

## When NOT to use a bitmap index

- **OLTP with frequent writes** - every INSERT/UPDATE/DELETE to the column rewrites the entire bitmap. Two concurrent writes lock each other out (bitmap locks are at the segment level, not the row level). This is a known severe limitation.
- **High-cardinality columns** - the bitmaps become sparse and waste space. Use a B-tree.
- **Columns that change often** - even in a read-mostly table, an "update this status" batch job will be slow.

## Project Connection

`intern.is_accepted` has three values (`Accepted`, `Rejected`, `Pending`), and the project queries it (`WHERE is_accepted = 'Pending'`) far more than it updates it. A bitmap index is ideal:

```sql
CREATE BITMAP INDEX bm_intern_status ON intern(is_accepted);
```

The redesign recommends this. Note that the CHECK constraint on `is_accepted` (see [[08 - Relational DB Foundations/02 - Constraints]]) makes the cardinality stable - no surprise fourth value.

## Common pitfalls

- Using bitmap indexes on a high-write OLTP table - throughput collapses.
- Forgetting that bitmap indexes lock at the segment level, not the row level - two concurrent updates to the same bitmap-protected column serialize.
- Indexing a column with 1000 distinct values - too high for a bitmap; use a B-tree.

## Trade-offs

- **Bitmap read speed vs write lock granularity**: bitmaps are great for reads but bad for writes.
- **Bitmap storage vs B-tree storage**: bitmaps are smaller for low-cardinality, larger for high-cardinality.

## Further reading

- Oracle Docs, "Bitmap Indexes".
- [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
