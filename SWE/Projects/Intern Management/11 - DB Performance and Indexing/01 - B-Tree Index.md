---
tags: [concept, database, indexing, b-tree]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/04 - Complexity Theory (Big-O)]]
  - [[02 - CS Foundations/05 - Data Structures Overview]]
related:
  - [[11 - DB Performance and Indexing/04 - Bitmap Index]]
  - [[11 - DB Performance and Indexing/08 - Composite and Covering Indexes]]
---

# B-Tree Index

## What it is

A **B-tree** (Balanced Tree) is the default index type in Oracle (and most databases). It's a self-balancing tree with high fan-out (many children per node), keeping the tree shallow.

```
            [Root]
           /  |   \
       [Leaf] [Leaf] [Leaf]
       ↓       ↓      ↓
     (data)  (data)  (data)
```

## Why it's fast

- **Lookup**: O(log_f n), where `f` is the fan-out (typically 100-1000).
- For 1 billion rows with fan-out 100: log_100(10^9) ≈ 4.5 page reads.
- For comparison, a full table scan reads all 1 billion rows.

## Structure

Oracle's B-tree index leaf nodes contain:
- The indexed column value.
- The ROWID of the table row.

To find a row by indexed column:
1. Traverse the B-tree (4-5 reads) to find the leaf.
2. Get the ROWID.
3. Read the table row by ROWID (1 read).

Total: 5-6 reads vs. 1 billion for a full scan.

## When to use

- Columns used in `WHERE` clauses.
- Columns used in `JOIN` conditions.
- Columns used in `ORDER BY` (index is pre-sorted).
- Foreign keys (see [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]]).

## When NOT to use

- Small tables (full scan is faster).
- Columns with low cardinality (use bitmap).
- Columns rarely queried.
- Tables with heavy writes (every index slows writes).

## Project Connection

The project's schema has **no secondary indexes** — only the implicit PK index. Adding indexes on FK columns and frequently-filtered columns is the #1 performance fix:

```sql
CREATE INDEX idx_interns_theme ON interns(theme_id);
CREATE INDEX idx_interns_email ON interns(email);
CREATE INDEX idx_interns_status ON interns(status);
CREATE INDEX idx_users_username ON users(username);
```

## Further reading

- Oracle Database Concepts — Indexes.
- *Database Internals* (Petrov).
