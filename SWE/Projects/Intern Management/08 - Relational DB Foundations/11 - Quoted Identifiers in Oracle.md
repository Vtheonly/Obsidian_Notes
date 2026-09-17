---
tags: [concept, database, oracle, identifiers]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
---

# Quoted Identifiers in Oracle

## The rule

In Oracle:
- **Unquoted identifiers** are stored UPPERCASE. `CREATE TABLE interns` → stored as `INTERNS`.
- **Quoted identifiers** (`"interns"`) are stored exactly as written, case-sensitive.

```sql
CREATE TABLE interns (...);     -- stored as INTERNS
CREATE TABLE "interns" (...);   -- stored as interns (lowercase!)
CREATE TABLE "Interns" (...);   -- stored as Interns (mixed case)
```

To query:
```sql
SELECT * FROM interns;          -- works (Oracle uppercases to INTERNS, matches)
SELECT * FROM INTERNS;          -- works
SELECT * FROM "interns";        -- works (matches the lowercase stored name)
SELECT * FROM "INTERNS";        -- fails (no table named "INTERNS" in uppercase quotes)
```

## The project's bug

`insertion.sql` creates tables with unquoted identifiers (stored uppercase):
```sql
CREATE TABLE intern (...);       -- stored as INTERN
CREATE TABLE worker_user (...);  -- stored as WORKER_USER
```

But `oracleConnector.java` queries with quoted identifiers (lowercase):
```java
String query = "SELECT * FROM "intern" WHERE ...";
```

`"intern"` (lowercase, quoted) ≠ `INTERN` (uppercase, unquoted). This should fail with `ORA-00942: table or view does not exist`.

**The fact that the app works at all** means someone manually created the tables with quoted lowercase names that match the queries — which is not what the schema files do. The schema files and the runtime schema diverge.

## The fix

**Pick one convention: never quote identifiers.** Oracle uppercases them automatically. All table and column names should be lowercase in the SQL file (Oracle stores them uppercase; case-insensitive to query).

Update every query in `oracleConnector` to drop the quotes:
```java
// Before
String query = "SELECT * FROM "intern" WHERE "intern_id" = ?";

// After
String query = "SELECT * FROM intern WHERE intern_id = ?";
```

Re-create the schema from a single Flyway migration with no quotes.

## Common pitfalls

- **Mixing quoted and unquoted** — the most common Oracle schema bug. Pick one.
- **Quoting to preserve case** — sometimes useful (e.g., `CREATE TABLE "My Table"`) but creates fragile queries.
- **Tools that auto-quote** — some ORMs quote all identifiers. Be consistent.

## Further reading

- Oracle Database SQL Language Reference — Schema Object Naming Rules.
