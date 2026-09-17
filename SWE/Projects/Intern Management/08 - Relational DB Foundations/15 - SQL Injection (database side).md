---
tags: [concept, database, security, sql-injection]
type: concept
status: complete
related:
  - [[17 - Application Security/08 - SQL Injection Prevention]]
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
---

# SQL Injection (Database Side)

> See [[17 - Application Security/08 - SQL Injection Prevention]] for the full treatment. This note covers the database-side perspective.

## What it is

SQL injection occurs when user input is concatenated into a SQL string, allowing the user to alter the query's meaning.

```java
// Vulnerable
String sql = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
// If username = "admin' --", the query becomes:
// SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
// The -- comments out the rest. Attacker logs in as admin without a password.
```

## Database-side defenses

### 1. Prepared statements (primary defense)
The database compiles the SQL once, with placeholders. User input is bound as data, not code.
```sql
-- Database sees: SELECT * FROM users WHERE username = ? AND password = ?
-- Then binds: username = 'admin'' --', password = '...'
-- The ' is escaped; the injection becomes a literal string.
```

### 2. Least-privilege database user
The application connects as a user with only the permissions it needs (`SELECT, INSERT, UPDATE, DELETE` on its tables). No `DROP`, no `GRANT`, no `SYSDBA`.

The project's `system/rootroot` connection is the opposite — `system` can do anything.

### 3. Stored procedures (when appropriate)
If queries are complex, encapsulate them in stored procedures. The app calls `CALL accept_intern(?, ?)` — no SQL string from the app.

### 4. Database firewalls
Some databases (Oracle Database Firewall) inspect SQL and block suspicious patterns.

## Why prepared statements work

The database parses the SQL template (`SELECT ... WHERE username = ?`) into a **parse tree**. The `?` is a parameter — it can only be a value, not a keyword. Binding `'admin'' --'` inserts the literal string `admin' --` as the username. No injection is possible because the parse tree is fixed.

## Identifier injection

Prepared statements don't protect **identifiers** (table names, column names). You can't do:
```java
String sql = "SELECT * FROM ? WHERE ? = ?";  // doesn't work
```

If you must parameterize identifiers, **whitelist** them:
```java
Set<String> allowedTables = Set.of("interns", "themes", "departments");
if (!allowedTables.contains(tableName)) {
    throw new IllegalArgumentException("Invalid table: " + tableName);
}
String sql = "SELECT * FROM " + tableName + " WHERE id = ?";
```

## Project Connection

The project's `getMaxId` uses `Statement` (not `PreparedStatement`) with string-concatenated table/column names:
```java
String sql = "SELECT MAX("" + columnName + "") FROM "" + tableName + """;
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(sql);
```

Today, callers pass hardcoded strings, so it's not directly exploitable. But the API is unsafe — a future caller passing user input becomes vulnerable.

The fix: replace `getMaxId` with per-entity `INSERT ... RETURNING` or Oracle IDENTITY columns. No dynamic SQL needed.

See [[17 - Application Security/08 - SQL Injection Prevention]] and [[13 - JDBC and Data Access/09 - PreparedStatement]].

## Further reading

- OWASP SQL Injection Prevention Cheat Sheet.
- *SQL Injection Attacks and Defense* (Clarke).
