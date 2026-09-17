---
tags: [concept, jdbc, try-with-resources]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/16 - try-with-resources Deep Dive]]
---

# try-with-resources for JDBC

## What it is

Every JDBC resource (`Connection`, `Statement`, `ResultSet`) implements `AutoCloseable`. Use try-with-resources to ensure they're closed.

## The pattern

```java
String sql = "SELECT * FROM interns WHERE department_id = ?";
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setLong(1, deptId);
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
            // ...
        }
    }
}
// conn, ps, rs are all closed automatically
```

## Why it matters

- **Resource leaks** — unclosed connections exhaust the pool. Unclosed statements exhaust the DB's cursor cache (ORA-01000: maximum open cursors exceeded).
- **Exception safety** — try-with-resources closes even if an exception occurs, with suppressed exceptions preserved.
- **Clean code** — no `finally` block needed.

## Project Connection

The project uses try-with-resources in some methods (`isAdmin`, `searchIntern`) but try-finally in others (`insertIntern`, `deleteIntern`, `getMaxId`). The fix: use try-with-resources everywhere.

## Further reading

- See [[03 - Java Foundations/16 - try-with-resources Deep Dive]] for the deep treatment.
