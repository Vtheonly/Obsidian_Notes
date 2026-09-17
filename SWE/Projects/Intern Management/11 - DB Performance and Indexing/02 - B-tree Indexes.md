---
tags: [concept, database, performance, indexing, b-tree]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
related:
  - [[11 - DB Performance and Indexing/07 - Composite Indexes]]
  - [[11 - DB Performance and Indexing/05 - Bitmap Indexes]]
  - [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
---

# B-tree Indexes

## What it is

A **B-tree index** (technically a B+ tree in Oracle) is a balanced tree of index entries. The leaf level stores `(indexed_value, ROWID)` pairs sorted by value; branch levels speed the search. Lookup is `O(log N)` - for a 10-million-row table, that's about 4 levels of tree traversal.

```
                [ Branch: M ]
               /             \
        [ A..L ]              [ N..Z ]
        /     \               /      \
  [A,B,C] [D,E,F] ...    [N,O,P] [Q..Z]    <- leaves: (value, ROWID)
```

Each leaf also has a pointer to the next leaf (a doubly-linked list), enabling fast range scans: `WHERE id BETWEEN 100 AND 200` walks the leaves from 100 to 200.

## Creating a B-tree index

```sql
CREATE INDEX idx_intern_name        ON intern(name);
CREATE INDEX idx_intern_start_date  ON intern(start_date);
CREATE UNIQUE INDEX uq_intern_email ON intern(email);   -- PK and UNIQUE create B-tree indexes implicitly
```

## When the optimizer uses a B-tree

- **Equality** (`WHERE id = 42`) - direct leaf lookup.
- **Range** (`WHERE id BETWEEN 100 AND 200`) - leaf walk.
- **Prefix** (`WHERE name LIKE 'A%'`) - leaf walk from the first 'A'.
- **Sort** (`ORDER BY name`) - if the index order matches, no sort needed.

A `LIKE '%A%'` (leading wildcard) **cannot** use the index - the tree is sorted from the left, so a leading wildcard forces a full scan. Use a function-based index or Oracle Text for that.

## When the optimizer ignores a B-tree

- The table is small (a few blocks) - a full scan is faster.
- The predicate matches too many rows (typically >5% of the table) - a full scan is cheaper than bouncing between index and table.
- Statistics are stale - the optimizer guesses wrong.

Refresh statistics:

```sql
EXEC DBMS_STATS.GATHER_TABLE_STATS('APP_OWNER', 'INTERN');
```

## Why it matters

Without an index, every `WHERE` clause is a full table scan. On a 10-million-row intern table, a name lookup reads 10M rows. With an index, it reads ~4 blocks. The difference between "users complain" and "users don't notice."

## Project Connection

`insertion.sql` creates **no indexes** beyond the implicit PK indexes. Foreign-key columns like `intern.theme_id`, `intern.department_id`, and `worker_user.department_id` are unindexed. This means:

- `WHERE department_id = 5` does a full table scan on `intern`.
- Joining `intern` to `department` does a full scan of one side (or a hash join with a full scan of both).
- Deleting a `department` row locks the entire `intern` table (Oracle's unindexed-FK behavior). See [[11 - DB Performance and Indexing/17 - Missing Indexes on Foreign Keys]].

The redesign adds:

```sql
CREATE INDEX idx_intern_department ON intern(department_id);
CREATE INDEX idx_intern_theme      ON intern(theme_id);
CREATE INDEX idx_intern_status     ON intern(is_accepted);
CREATE INDEX idx_user_department   ON worker_user(department_id);
```

## Common pitfalls

- Indexing every column - each index costs writes (the index must be maintained on every INSERT/UPDATE/DELETE) and storage. Index selectively.
- Indexing low-cardinality columns (e.g., `is_accepted` with 3 values) with a B-tree - use [[11 - DB Performance and Indexing/05 - Bitmap Indexes]] instead.
- Indexing a column that's frequently updated - the index bloats from splits; consider rebuilding periodically.
- Forgetting to gather stats after a big load - the optimizer thinks the table is empty and chooses bad plans.

## Trade-offs

- **Read speed vs write cost**: every index speeds some reads and slows every write.
- **Storage**: an index is roughly 1.5x the size of the indexed column.
- **Plan stability**: too many indexes can make the optimizer flip between plans unpredictably.

## Further reading

- Oracle Docs, "Index Skip Scan", "Index Range Scan".
- [[11 - DB Performance and Indexing/07 - Composite Indexes]]
- [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
