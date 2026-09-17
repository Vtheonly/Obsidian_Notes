---
tags: [concept, database, performance, n-plus-1]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/05 - Joins (Inner, Left, Right, Full)]]
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
---

# N+1 Query Problem

## What it is

The **N+1 problem** is executing 1 query to fetch N rows, then N more queries to fetch related data for each row. Total: N+1 queries instead of 1.

## The project's N+1

```java
// insertionInternController.searchIntern
List<Map<String, Object>> interns = oracleConnector.searchIntern(filters);  // query 1
for (Map<String, Object> intern : interns) {
    String themeName = oracleConnector.getNameById(                          // query 2, 3, 4, ...
        Integer.parseInt((String) intern.get("theme_id")),
        "theme", "theme_id", "theme_name"
    );
    addToPool(...);
}
```

100 interns = 101 queries.

## Why it's bad

Each query has a round-trip cost:
- Localhost: ~1 ms.
- LAN: ~10 ms.
- Cross-region: ~50 ms.

100 interns:
- Local: 101 × 1 ms = 101 ms.
- LAN: 101 × 10 ms = 1.01 sec.
- Cross-region: 101 × 50 ms = 5.05 sec.

Plus the query execution time per query.

## The fix: JOIN

```sql
SELECT i.intern_id, i.name, i.email, t.theme_name
FROM interns i
LEFT JOIN themes t ON i.theme_id = t.theme_id
WHERE i.name LIKE ?;
```

One query, one round-trip. 100 interns:
- Local: 1 × 1 ms = 1 ms.
- LAN: 1 × 10 ms = 10 ms.
- Cross-region: 1 × 50 ms = 50 ms.

100x-1000x faster.

## The fix: batch fetching

If you can't use a JOIN (e.g., the related data is in a different service), use `IN`:
```sql
-- Step 1: fetch interns
SELECT intern_id, name, theme_id FROM interns WHERE ...;
-- Returns theme_ids: [1, 5, 7, 9]

-- Step 2: fetch all themes in one query
SELECT theme_id, theme_name FROM themes WHERE theme_id IN (1, 5, 7, 9);
```

2 queries instead of N+1.

## ORM N+1

ORMs (Hibernate, JPA) are notorious for N+1:
```java
List<Intern> interns = internRepository.findAll();  // 1 query
for (Intern i : interns) {
    System.out.println(i.getTheme().getName());  // N queries (lazy loading)
}
```

Fix with `JOIN FETCH`:
```java
@Query("SELECT i FROM Intern i JOIN FETCH i.theme")
List<Intern> findAllWithTheme();
```

## Project Connection

The project has N+1 in:
- `insertionInternController.searchIntern` (fetches theme_name per intern).
- `chiefDecisionController.searchIntern` (same).
- `insertionUserController` (fetches supervisor name per user, etc.).

The fix: JOIN queries in the repository layer.

## Further reading

- Fowler, *Patterns of Enterprise Application Architecture* — Lazy Load and Eager Load.
