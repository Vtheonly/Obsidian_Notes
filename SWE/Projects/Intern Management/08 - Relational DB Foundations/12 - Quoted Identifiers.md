---
tags: [concept, database, oracle, identifiers]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/08 - Oracle Data Types]]
related:
  - [[03 - Java Foundations/06 - Java Naming Conventions]]
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
---

# Quoted Identifiers

## What it is

Oracle has two modes for identifiers (table and column names):

- **Unquoted**: folded to **UPPERCASE** before storage. `intern`, `Intern`, `INTERN` all become `INTERN` in the data dictionary.
- **Quoted** (`"..."`): stored **exactly as written**, **case-sensitive**. `"intern"` becomes `intern` (lowercase) - a different identifier from `INTERN`.

```sql
CREATE TABLE intern (...);   -- stored as INTERN
CREATE TABLE "intern" (...); -- stored as intern  -- DIFFERENT TABLE
```

You now have **two tables**. `SELECT * FROM intern` looks for `INTERN` (uppercase) - it will find the first, not the second. To query the second, you must **always** quote: `SELECT * FROM "intern"`.

## Why it matters

Mixing quoted and unquoted identifiers is the source of countless "table does not exist" errors. The convention is universal: **never quote**. Pick a casing (Oracle's default uppercase) and use it everywhere. The schema metadata in `USER_TABLES` will always show uppercase; JDBC's `ResultSetMetaData.getTableName()` returns uppercase; tools assume uppercase.

The only legitimate use of quoting is to use a reserved word (`"DATE"`, `"LEVEL"`, `"COMMENT"`) or to preserve mixed case for a migration from another engine.

## Example of the trap

```sql
-- Day 1: dev creates the table quoted
CREATE TABLE "intern" (intern_id NUMBER, ...);

-- Day 2: someone tries
SELECT * FROM intern;             -- ORA-00942: table or view does not exist
SELECT * FROM "INTERN";           -- ORA-00942: case mismatch
SELECT * FROM "intern";           -- works -- you must quote forever
```

## Project Connection

The project quotes `"intern"` everywhere in Java:

```java
String query = "SELECT * FROM "intern" WHERE ...";
```

This works only because `insertion.sql` happened to declare the table unquoted (so it's stored as `INTERN`), and Oracle's quoted lookup of `"intern"` resolves to... actually, no - `"intern"` (lowercase) does NOT match `INTERN` (uppercase). Let me be precise.

The reason the project "works" (when it does) is that the Java code uses `"IS_ACCEPTED"` (uppercase quoted), which **does** match the unquoted-declared `is_accepted` column (stored as `IS_ACCEPTED`). And `"intern"` (lowercase quoted) would NOT match `INTERN`. The fact that it ever works at all is a series of lucky coincidences - this is exactly the kind of fragility quoted identifiers introduce.

The fix: drop the quotes, use unquoted identifiers everywhere, rely on Oracle's default uppercasing.

## Common pitfalls

- Creating a table `"MyTable"` and then trying `SELECT * FROM mytable` - fails.
- Tooling that lowercases identifiers (Hibernate's legacy naming strategy) forcing you to quote everything to compensate.
- Quoting on day 1 means you must quote on day 1,000 - there is no escape hatch.

## Trade-offs

| Choice | Pro | Con |
|---|---|---|
| Always unquoted | Simple, matches Oracle defaults, tools "just work" | Can't use reserved words as names |
| Always quoted | Preserves any casing | Every SQL statement must quote, forever |
| Mixed | - | Worst of both; constant surprises |

Pick "always unquoted." If you must use a reserved word, pick a different name.

## Further reading

- Oracle Docs, "Schema Object Naming Rules".
- [[03 - Java Foundations/06 - Java Naming Conventions]]
