---
tags: [concept, database, oracle, pseudocolumns]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
---

# DUAL and Oracle Pseudocolumns

## DUAL

`DUAL` is a special one-row, one-column table in Oracle. Used to evaluate expressions that don't need a real table.

```sql
SELECT 1 FROM DUAL;                    -- returns 1
SELECT SYSDATE FROM DUAL;              -- current date
SELECT SYSTIMESTAMP FROM DUAL;         -- current timestamp
SELECT 1+1 FROM DUAL;                  -- arithmetic
SELECT 'hello' FROM DUAL;              -- string literal
SELECT my_sequence.NEXTVAL FROM DUAL;  -- get next sequence value
```

In standard SQL (and Oracle 23c+), `SELECT 1` without `FROM` works. But for Oracle ≤ 21c, `FROM DUAL` is required.

## Pseudocolumns

Pseudocolumns behave like columns but aren't real.

### ROWNUM
The row's position in the result set (1-based). Assigned before `ORDER BY`.
```sql
SELECT ROWNUM, name FROM interns WHERE ROWNUM <= 10;  -- first 10 rows
```
⚠️ `ROWNUM <= 10` returns 10 rows, but `ROWNUM > 10` returns 0 rows (ROWNUM is assigned before the filter). Use a subquery.

### ROWID
The physical address of a row. Unique within a table.
```sql
SELECT ROWID, name FROM interns;
```
Use for fast access (`WHERE ROWID = '...'`), but it can change (table rebuild, partition move).

### NEXTVAL and CURRVAL (sequences)
```sql
SELECT my_seq.NEXTVAL FROM DUAL;  -- advance and return next value
SELECT my_seq.CURRVAL FROM DUAL;  -- current value (same session, after NEXTVAL)
```

### LEVEL (hierarchical queries)
```sql
SELECT LEVEL, employee_name FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id;
```

### ROW_NUMBER() (analytic function)
```sql
SELECT ROW_NUMBER() OVER (ORDER BY name) AS rn, name FROM interns;
```
Better than ROWNUM for pagination.

## Project Connection

The project uses `SELECT MAX(intern_id) FROM intern` to generate IDs — this is what `DUAL` + `NEXTVAL` (sequences) or IDENTITY columns are for. The fix:
```sql
-- IDENTITY column (Oracle 12c+)
CREATE TABLE interns (
    intern_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ...
);
-- INSERT without the ID; JDBC returns it via getGeneratedKeys()
```

Or with a sequence:
```sql
CREATE SEQUENCE intern_seq START WITH 1 INCREMENT BY 1;
INSERT INTO interns (intern_id, ...) VALUES (intern_seq.NEXTVAL, ...);
```

The advanced redesign uses IDENTITY columns. See [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]].

## Further reading

- Oracle Database SQL Language Reference — Pseudocolumns.
