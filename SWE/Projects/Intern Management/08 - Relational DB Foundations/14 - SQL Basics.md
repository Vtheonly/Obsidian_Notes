---
tags: [concept, database, sql]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/13 - Relational Model (Codd)]]
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
---

# SQL Basics

## SQL sublanguages

| Sublanguage | Purpose | Example |
|---|---|---|
| **DDL** (Data Definition) | Define schema | `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` |
| **DML** (Data Manipulation) | Query and modify data | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **DCL** (Data Control) | Permissions | `GRANT`, `REVOKE` |
| **TCL** (Transaction Control) | Transactions | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

## CRUD mapping

| Operation | SQL |
|---|---|
| Create | `INSERT INTO t (cols) VALUES (vals)` |
| Read | `SELECT cols FROM t WHERE cond` |
| Update | `UPDATE t SET col=val WHERE cond` |
| Delete | `DELETE FROM t WHERE cond` |

## Important clauses (in execution order)

1. `FROM` (including JOINs) — load the source data.
2. `WHERE` — filter rows.
3. `GROUP BY` — group rows.
4. `HAVING` — filter groups.
5. `SELECT` — pick columns (after grouping).
6. `ORDER BY` — sort.
7. `OFFSET` / `FETCH` — paginate.

Note: `SELECT` happens *after* `WHERE`. You cannot use a column alias in `WHERE` (it doesn't exist yet).

## Project Connection

The project's SQL is basic: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, with `MAX()` and `COUNT(*)`. No `JOIN`s (causing N+1), no `GROUP BY`, no `HAVING`, no `ORDER BY`. The fix introduces JOINs for the N+1 problem and `GROUP BY` for the dashboard PieChart.

## Further reading

- *SQL in 10 Minutes* (Ben Forta).
- *SQL Antipatterns* (Karwin).
