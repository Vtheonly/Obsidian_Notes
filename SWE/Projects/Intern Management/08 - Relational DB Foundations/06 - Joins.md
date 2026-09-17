---
tags: [concept, database, joins, sql]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
related:
  - [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
  - [[11 - DB Performance and Indexing/20 - The N+1 Query Problem]]
---

# Joins

## What it is

A **join** combines rows from two or more tables based on a predicate. The two tables are inputs; the result is a new (virtual) table.

## The five join types

```sql
-- INNER JOIN: rows that match in BOTH tables
SELECT i.name, d.name AS department
FROM   intern i
INNER  JOIN department d ON i.department_id = d.department_id;

-- LEFT [OUTER] JOIN: all left rows, NULLs where right doesn't match
SELECT i.name, d.name AS department
FROM   intern i
LEFT   JOIN department d ON i.department_id = d.department_id;

-- RIGHT [OUTER] JOIN: all right rows, NULLs where left doesn't match
--   (same as LEFT JOIN with tables swapped; rarely used)

-- FULL [OUTER] JOIN: all rows from both; NULLs where either side misses
SELECT i.name, d.name AS department
FROM   intern i
FULL   JOIN department d ON i.department_id = d.department_id;

-- CROSS JOIN: Cartesian product (every left x every right)
SELECT i.name, d.name AS department
FROM   intern i
CROSS  JOIN department d;  -- 10 interns x 5 depts = 50 rows
```

There's also `NATURAL JOIN` (joins on all same-named columns) - **avoid it**; rename a column and the query silently changes meaning.

## How Oracle executes joins

- **Nested loop** - for each left row, probe the right table via index. Good when left is small and right is indexed.
- **Hash join** - hash the smaller side into memory, scan the larger. Good for large/large equi-joins.
- **Sort-merge** - sort both sides, merge. Used when the join predicate is not an equality or memory is tight.

You can hint with `/*+ USE_HASH(i d) */` but usually the optimizer gets it right - **if statistics are fresh**.

## Why it matters

Joins are the reason the relational model scales to complex questions. A normalized schema has many small tables; joins recombine them on demand. The alternative - a giant denormalized table - is fast to query but impossible to maintain. See [[09 - Normalization/10 - When to Denormalize]].

## Project Connection

The project's `searchIntern` **deliberately avoids joins** in favor of per-row lookups:

```java
ResultSet rs = stmt.executeQuery("SELECT * FROM "intern"");
while (rs.next()) {
    int deptId = rs.getInt("department_id");
    String deptName = oracleConnector.getNameById("department", "department_id", deptId);
    // ... one round-trip per intern row
}
```

This is the **N+1 query problem** - see [[11 - DB Performance and Indexing/20 - The N+1 Query Problem]]. The fix is a single `INNER JOIN`:

```sql
SELECT i.intern_id, i.name, d.name AS department_name
FROM   intern i
LEFT   JOIN department d ON i.department_id = d.department_id
WHERE  i.name LIKE '%' || ? || '%';
```

## Common pitfalls

- Forgetting that `LEFT JOIN` rows with no match have NULL in right columns - `WHERE d.name = 'X'` silently converts it to an inner join.
- Joining on the wrong column (e.g., `i.department_id = i.department_id`) - returns a cross join with one row per intern.
- `SELECT *` across a join - column-name collisions (both have `name`) force you to alias.

## Further reading

- Oracle Docs, "Joins".
- [[11 - DB Performance and Indexing/20 - The N+1 Query Problem]]
