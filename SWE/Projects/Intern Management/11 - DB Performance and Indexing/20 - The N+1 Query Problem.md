---
tags: [concept, database, performance, anti-pattern, n-plus-1]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/06 - Joins]]
related:
  - [[11 - DB Performance and Indexing/03 - Batch Operations]]
  - [[12 - Advanced Database Features/06 - Materialized Views]]
---

# The N+1 Query Problem

## What it is

The **N+1 query problem** is executing **1 query to fetch a list of N rows, then N more queries to fetch a related row for each**. Total: N+1 round-trips where 1 would have sufficed.

## The classic example

```java
// 1 query: fetch all interns
List<Intern> interns = jdbc.query("SELECT * FROM intern", internRowMapper);

// N queries: fetch each intern's department
for (Intern i : interns) {
    Department d = jdbc.queryForObject(
        "SELECT * FROM department WHERE department_id = ?",
        deptRowMapper, i.getDepartmentId());
    i.setDepartment(d);
}
```

For 100 interns, that's 101 round-trips. Each round-trip is ~1ms minimum (network + parse + execute), so 100ms minimum - and that's optimistic. Under load, it's worse.

## Why it happens

- ORMs that lazy-load relations (Hibernate `@ManyToOne(fetch = LAZY)`). The first query loads interns; the department is loaded on first access - per row.
- Hand-written JDBC where the developer didn't think to JOIN.
- The "I'll just call my `getNameById` helper" pattern, applied in a loop.

## The fixes

### 1. JOIN

```sql
SELECT i.intern_id, i.name, d.department_name
FROM   intern i
LEFT   JOIN department d ON i.department_id = d.department_id;
```

One query. Done.

### 2. Batch fetch (when JOIN isn't possible)

If the relations are optional or you want to avoid a wide JOIN, fetch the related rows in one IN-clause query:

```java
List<Long> deptIds = interns.stream().map(Intern::getDepartmentId).distinct().toList();
List<Department> depts = jdbc.query(
    "SELECT * FROM department WHERE department_id IN (:ids)",
    Map.of("ids", deptIds),
    deptRowMapper);
Map<Long, Department> byId = depts.stream().collect(toMap(Department::getId, d -> d));
interns.forEach(i -> i.setDepartment(byId.get(i.getDepartmentId())));
```

Two queries total, regardless of N.

### 3. Hibernate `@Fetch(SUBSELECT)` or `@BatchSize`

```java
@ManyToOne(fetch = LAZY)
@Fetch(FetchMode.SUBSELECT)
private Department department;
```

Hibernate will issue a single `SELECT ... WHERE department_id IN (SELECT ... FROM intern)` for the whole batch.

## Why it matters

The N+1 is the #1 performance killer in CRUD apps. It scales linearly with the result set: a page that's fast at 10 rows is slow at 100 and unusable at 1000. The fix is mechanical - one JOIN - but the bug hides because each individual query is fast.

## Project Connection

`oracleConnector.searchIntern`:

```java
ResultSet rs = stmt.executeQuery("SELECT * FROM "intern"");
while (rs.next()) {
    int deptId = rs.getInt("department_id");
    String deptName = oracleConnector.getNameById("department", "department_id", deptId);
    // ...
}
```

This is a textbook N+1. The fix is one JOIN:

```sql
SELECT i.intern_id, i.name, i.is_accepted,
       d.department_name, t.theme_name
FROM   intern i
LEFT   JOIN department d ON i.department_id = d.department_id
LEFT   JOIN theme      t ON i.theme_id      = t.theme_id
WHERE  i.name LIKE '%' || ? || '%';
```

One query, three tables, one round-trip. The redesign proposes exactly this.

## Common pitfalls

- Fixing the N+1 with a JOIN but introducing a Cartesian product by missing a join condition.
- Using `SELECT *` across a JOIN - column-name collisions and wasted bandwidth.
- Fixing one N+1 and missing three others - profile with query logging.
- Using `EAGER` fetching everywhere to "avoid lazy-load issues" - that's just a 1+N problem in disguise (now the first query is huge).

## Detection

- Log every query with its timestamp. A burst of identical `SELECT ... WHERE id = ?` after a list query is the tell-tale sign.
- Hibernate's `org.hibernate.SQL=DEBUG` and `org.hibernate.stat=DEBUG` logs query counts.
- p6spy logs each query with timing.

## Further reading

- Fowler, P of EAA, "Lazy Load" and the N+1 discussion.
- [[08 - Relational DB Foundations/06 - Joins]]
- [[11 - DB Performance and Indexing/03 - Batch Operations]]
