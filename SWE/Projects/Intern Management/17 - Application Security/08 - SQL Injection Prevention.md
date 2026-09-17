---
tags: [concept, security, sql-injection]
type: concept
status: complete
related:
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
  - [[08 - Relational DB Foundations/15 - SQL Injection (database side)]]
---

# SQL Injection Prevention

## The project's vulnerability

```java
// oracleConnector.getMaxId
public static int getMaxId(String tableName, String columnName) {
    String sql = "SELECT MAX("" + columnName + "") FROM "" + tableName + """;
    Statement stmt = connection.createStatement();  // Statement, not PreparedStatement
    ResultSet rs = stmt.executeQuery(sql);
    // ...
}
```

Table and column names are concatenated into the SQL. If a caller passes user input, it's SQL injection.

Today, callers pass hardcoded strings, so it's not directly exploitable. But the API is unsafe — a future refactor that passes user input becomes vulnerable.

## Prevention techniques

### 1. PreparedStatement (primary defense)
```java
String sql = "SELECT * FROM interns WHERE name = ? AND age > ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setString(1, name);
ps.setInt(2, age);
```
The `?` is a parameter — bound as data, not code. SQL injection is impossible.

### 2. Whitelist identifiers
If you must parameterize table/column names, whitelist:
```java
Set<String> ALLOWED_TABLES = Set.of("interns", "themes", "departments", "users");
if (!ALLOWED_TABLES.contains(tableName)) {
    throw new IllegalArgumentException("Invalid table: " + tableName);
}
String sql = "SELECT MAX(" + columnName + ") FROM " + tableName;
```

### 3. Stored procedures
Encapsulate SQL in procedures; the app calls `CALL my_proc(?, ?)`. No SQL string from the app.

### 4. ORM
JPA/Hibernate use prepared statements under the hood. But beware of JPQL injection:
```java
// Vulnerable
em.createQuery("SELECT i FROM Intern i WHERE i.name = '" + name + "'");
// Safe
em.createQuery("SELECT i FROM Intern i WHERE i.name = :name").setParameter("name", name);
```

## Project Connection

The fix: remove `getMaxId`, use IDENTITY columns. Remove `getIdByName`/`getNameById`/`getSelectableOptions` (generic methods), replace with per-entity repository methods with hardcoded SQL.

## Further reading

- OWASP SQL Injection Prevention Cheat Sheet.
