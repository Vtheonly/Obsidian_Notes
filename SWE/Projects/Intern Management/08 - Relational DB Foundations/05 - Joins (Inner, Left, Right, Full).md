---
tags: [concept, database, sql, joins]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/18 - N+1 Query Problem]]
---

# Joins (Inner, Left, Right, Full)

## What it is

A **JOIN** combines rows from two tables based on a related column.

## Types

### INNER JOIN (default)
Returns rows where the join condition matches in both tables.
```sql
SELECT i.name, t.theme_name
FROM interns i
INNER JOIN themes t ON i.theme_id = t.theme_id;
```
Interns without a theme are excluded. Themes without interns are excluded.

### LEFT OUTER JOIN
Returns all rows from the left table, plus matching rows from the right. Unmatched right columns are NULL.
```sql
SELECT i.name, t.theme_name
FROM interns i
LEFT JOIN themes t ON i.theme_id = t.theme_id;
```
All interns are returned, even those without a theme (theme_name is NULL).

### RIGHT OUTER JOIN
Same as LEFT, but reversed. Rarely used (just swap tables and use LEFT).

### FULL OUTER JOIN
Returns all rows from both tables. Unmatched columns are NULL.
```sql
SELECT i.name, t.theme_name
FROM interns i
FULL JOIN themes t ON i.theme_id = t.theme_id;
```

### CROSS JOIN
Cartesian product — every row in A paired with every row in B. Rarely useful.
```sql
SELECT * FROM interns CROSS JOIN themes;  -- N × M rows
```

### NATURAL JOIN
Joins on columns with the same name. Avoid — fragile (adding a column can break it).

### SELF JOIN
A table joined to itself.
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

## JOIN syntax

```sql
-- ANSI-92 (preferred)
SELECT ... FROM a JOIN b ON a.id = b.a_id;

-- ANSI-89 (legacy, avoid)
SELECT ... FROM a, b WHERE a.id = b.a_id;
```

ANSI-92 is clearer (separates join condition from filter) and supports OUTER joins.

## Project Connection

The project has **zero JOINs**. `searchIntern` does:
```java
List<Map<String,Object>> interns = oracleConnector.searchIntern(filters);
for (Map<String,Object> intern : interns) {
    String themeName = oracleConnector.getNameById(intern.get("theme_id"), "theme", ...);
}
```
N+1 queries. The fix:
```sql
SELECT i.intern_id, i.name, i.email, t.theme_name
FROM interns i
LEFT JOIN themes t ON i.theme_id = t.theme_id
WHERE i.name LIKE ?
```
One query, one round-trip.

## Further reading

- *SQL in 10 Minutes* (Forta), Lesson on Joins.
- Visual JOIN (SQL-Bolt interactive tutorial).
