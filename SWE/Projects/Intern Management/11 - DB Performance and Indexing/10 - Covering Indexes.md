---
tags: [concept, database, performance, indexing, covering-index]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/07 - Composite Indexes]]
related:
  - [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
  - [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
---

# Covering Indexes

## What it is

A **covering index** is a composite index that includes **every column** a query needs. The database can satisfy the query entirely from the index, without visiting the table. This is called an **index-only scan**.

## The problem it solves

Without a covering index, a query like:

```sql
SELECT name, is_accepted FROM intern WHERE department_id = 5;
```

does two IOs per matching row:

1. Read the index entry to find the ROWID.
2. Read the table block at that ROWID to get `name` and `is_accepted`.

For 100 matching rows, that's 100 random table-block reads - slow.

## The covering fix

Add the queried columns to the index:

```sql
CREATE INDEX idx_intern_dept_covering
    ON intern(department_id, name, is_accepted);
```

Now the query reads the index leaves (which are sorted by `department_id`) and gets `name` and `is_accepted` from the same leaf - **no table lookup**. One sequential read of a contiguous chunk of the index.

## Including extra columns without sorting by them

In some databases (SQL Server, PostgreSQL with `INCLUDE`), you can add non-key columns to an index - they're stored in the leaf but not used for sorting. Oracle doesn't have `INCLUDE`, but you can simulate it: just add the columns to the end of the composite. They won't help with `ORDER BY` or range scans, but they will be in the leaf for the covering scan.

```sql
-- "Covering" index for SELECT name, is_accepted WHERE department_id = ?
CREATE INDEX idx_intern_dept_covering
    ON intern(department_id, name, is_accepted);
```

## When to use a covering index

- A query runs **very frequently** (a hot path).
- The query touches **few columns** (one or two beyond the predicate).
- The table is **wide** (so the table-block read is expensive - many columns to skip).
- The query returns **many rows** (so the per-row table lookup dominates).

## When NOT to use a covering index

- The query changes often - you'd have to keep adding columns to the index.
- The table is narrow - the table lookup is cheap.
- The query returns few rows - one table lookup per row is fine.
- The covering index would be wider than the table - you've made storage worse, not better.

## Project Connection

The project's `searchIntern` does `SELECT *` and then per-row `getNameById`. The redesign proposes either:

1. A JOIN (no index trickery needed - just rewrite the query).
2. A covering index on `intern(department_id, name, is_accepted)` so the dashboard query "list pending interns in department X" is a single index range scan with no table lookup.

## Common pitfalls

- Adding every column to the index "just in case" - the index becomes wider than the table, writes become slow.
- Forgetting that covering indexes still need maintenance - every UPDATE to a covered column updates the index too.
- Expecting covering scans to be free - they're faster than table lookups, but the index still has to be scanned.

## Trade-offs

- **Read speed vs write cost**: covering indexes dramatically speed up specific reads but slow every write to the covered columns.
- **Index size vs table-block reads**: a covering index trades storage for IO.

## Further reading

- Oracle Docs, "Index Fast Full Scan", "Index Range Scan".
- [[11 - DB Performance and Indexing/07 - Composite Indexes]]
