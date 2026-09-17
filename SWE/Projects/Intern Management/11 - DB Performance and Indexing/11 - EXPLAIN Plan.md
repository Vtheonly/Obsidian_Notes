---
tags: [concept, database, performance, explain-plan]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# EXPLAIN Plan

## What it is

`EXPLAIN PLAN` shows how the database will execute a query — which indexes it uses, which join strategy, the estimated cost.

## Oracle

```sql
EXPLAIN PLAN FOR
SELECT * FROM interns WHERE name LIKE 'A%';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY());
```

Output:
```
--------------------------------------------------------------------------
| Id | Operation         | Name         | Rows | Bytes | Cost  |
--------------------------------------------------------------------------
|  0 | SELECT STATEMENT  |              |   10 |  500  |    3  |
|* 1 |  TABLE ACCESS FULL| INTERNS      |   10 |  500  |    3  |
--------------------------------------------------------------------------
```

`TABLE ACCESS FULL` = full table scan (no index used). Bad for large tables.

`TABLE ACCESS BY INDEX ROWID` = index used. Good.

## Reading the plan

- **Operation** — what the DB does (scan, join, sort).
- **Options** — how (FULL, BY INDEX ROWID, RANGE SCAN).
- **Object** — which table/index.
- **Rows** — estimated rows returned.
- **Cost** — relative cost (lower is better).
- **Time** — estimated time (Oracle 10g+).

## Common operations

| Operation | Meaning |
|---|---|
| `TABLE ACCESS FULL` | Full scan — bad (unless the table is small). |
| `TABLE ACCESS BY INDEX ROWID` | Index lookup — good. |
| `INDEX RANGE SCAN` | Index range — good. |
| `INDEX UNIQUE SCAN` | Index equality on PK/unique — best. |
| `HASH JOIN` | Hash join — good for large joins. |
| `NESTED LOOPS` | Nested loop join — good for small joins. |
| `SORT ORDER BY` | Sort — needed for ORDER BY. |
| `FILTER` | Apply a predicate. |

## Identifying problems

1. **`TABLE ACCESS FULL` on a large table** — missing index.
2. **`TABLE ACCESS FULL` when you have an index** — the query doesn't use the index (function on column, type mismatch, etc.).
3. **High cost** — relative measure; compare to other queries.
4. **Unexpected rows** — stale statistics. Run `DBMS_STATS.GATHER_TABLE_STATS`.

## Project Connection

The project has no indexes, so every query is `TABLE ACCESS FULL`. The fix: add indexes, then verify with EXPLAIN that they're used.

## Further reading

- Oracle Database SQL Tuning Guide.
- *SQL Performance Explained* (Winand).
