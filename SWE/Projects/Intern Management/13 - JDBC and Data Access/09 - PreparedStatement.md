---
tags: [concept, jdbc, prepared-statement, security]
type: concept
status: complete
related:
  - [[17 - Application Security/08 - SQL Injection Prevention]]
  - [[08 - Relational DB Foundations/15 - SQL Injection (database side)]]
---

# PreparedStatement

## What it is

A `PreparedStatement` is a pre-compiled SQL statement with parameter placeholders (`?`). Parameters are bound separately, preventing SQL injection.

```java
String sql = "SELECT * FROM interns WHERE name = ? AND age > ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, "Alice");
    ps.setInt(2, 18);
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) { ... }
    }
}
```

## Why it's better than Statement

### 1. SQL injection prevention
```java
// Vulnerable (Statement)
String sql = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);
// If username = "admin' --", the query is compromised.

// Safe (PreparedStatement)
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, username);
// The ' is escaped; username is treated as data, not code.
```

### 2. Performance (statement caching)
The DB parses and compiles the SQL once. Subsequent executions with different parameters reuse the plan.

### 3. Type safety
`setString`, `setInt`, `setLong`, `setDate` — the right type is bound. No string conversion errors.

### 4. Readability
No string concatenation, no quoting.

## Parameter binding methods

| Method | SQL type |
|---|---|
| `setString` | VARCHAR, CHAR, CLOB |
| `setInt` / `setLong` | NUMBER (integer) |
| `setDouble` / `setFloat` | NUMBER (floating) |
| `setBigDecimal` | NUMBER (decimal) |
| `setBoolean` | NUMBER(1) or BOOLEAN |
| `setDate` | DATE |
| `setTimestamp` | TIMESTAMP |
| `setBytes` | RAW, BLOB |
| `setObject` | Any (let JDBC figure it out) |
| `setNull` | NULL |

## What PreparedStatement does NOT protect

- **Identifiers** — table names, column names. `SELECT * FROM ?` doesn't work.
- **Lists** — `IN (?, ?, ?)` requires knowing the list size. Use dynamic SQL or a table-valued parameter.

## Project Connection

The project uses `PreparedStatement` for most queries (good), but `Statement` for `getMaxId` (bad — table/column names are concatenated). The fix: remove `getMaxId`, use IDENTITY columns.

## Further reading

- OWASP SQL Injection Prevention Cheat Sheet.
