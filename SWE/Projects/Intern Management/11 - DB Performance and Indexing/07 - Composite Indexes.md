---
tags: [concept, database, performance, indexing, composite-index]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
related:
  - [[11 - DB Performance and Indexing/10 - Covering Indexes]]
  - [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
---

# Composite Indexes

## What it is

A **composite index** (also called a concatenated or multi-column index) indexes more than one column. The columns are stored in the order you declare them, so the index is sorted by `(col1, col2, col3)`.

```sql
CREATE INDEX idx_intern_dept_status ON intern(department_id, is_accepted);
```

The index is sorted first by `department_id`, then within each `department_id` by `is_accepted`. Think of a phone book sorted by `(last_name, first_name)`.

## The leftmost-prefix rule

A composite index can be used for any **leftmost prefix** of its columns:

| Query | Uses the index? |
|---|---|
| `WHERE department_id = 5 AND is_accepted = 'Pending'` | Yes (full index) |
| `WHERE department_id = 5` | Yes (first column) |
| `WHERE is_accepted = 'Pending'` | **No** (skips the first column) |
| `WHERE department_id = 5 AND name = 'Alice'` | Yes (uses `department_id`; `name` is not in the index) |

The third query is the classic footgun. If you need both `WHERE department_id = ?` and `WHERE is_accepted = ?` independently, you need **two** single-column indexes (or a skip-scan, which Oracle can do but is slower).

## Choosing column order

The general rules:

1. **Equality columns first**. `WHERE department_id = ? AND is_accepted = ?` - both are equality, so either order works for this query.
2. **Range columns last**. `WHERE department_id = ? AND start_date BETWEEN ? AND ?` - put `department_id` first; the range on `start_date` walks a contiguous chunk of the index.
3. **Sort columns to match `ORDER BY`**. If you always `ORDER BY department_id, is_accepted`, the index in that order serves the sort for free.

But: the more queries you support, the harder it is to find one order that fits them all. **Measure** with `EXPLAIN PLAN`. See [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]].

## Index skip scan

Oracle can sometimes use a composite index even when you skip the first column - the "skip scan." It works when the first column has few distinct values: Oracle walks each distinct value and probes the index. For `idx_intern_dept_status` with 5 departments and `WHERE is_accepted = 'Pending'`, Oracle does 5 probes - cheaper than a full scan, but not as cheap as a dedicated index.

## Project Connection

The project has no composite indexes (it has no non-PK indexes at all). The redesign proposes:

```sql
CREATE INDEX idx_intern_dept_status ON intern(department_id, is_accepted);
```

This serves the common dashboard query "show me pending interns in department X" in one index range scan, no table lookup needed if you add the queried columns to the index (covering - see [[11 - DB Performance and Indexing/10 - Covering Indexes]]).

## Common pitfalls

- Wrong column order - the index is useless for the queries you actually run.
- Adding too many columns - the index grows, the write cost grows, the optimizer gets confused.
- Duplicating single-column indexes - if you have `(a, b)`, you don't need a separate `(a)`. (But you might need `(b)`.)
- Forgetting that `ORDER BY` only uses the index if the order matches exactly - reversed order forces a sort.

## Trade-offs

- **Index count vs query speed**: more indexes = faster reads, slower writes.
- **Index width vs covering**: a wider index can be covering (no table lookup) but uses more storage and is slower to update.

## Further reading

- Oracle Docs, "Composite Indexes".
- [[11 - DB Performance and Indexing/10 - Covering Indexes]]
