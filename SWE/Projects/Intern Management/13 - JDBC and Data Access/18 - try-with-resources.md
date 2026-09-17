---
tags: [concept, jdbc, java, data-access, try-with-resources]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
related:
  - [[03 - Java Foundations/16 - try-with-resources Deep Dive]]
  - [[13 - JDBC and Data Access/03 - Connection Pooling]]
---

# try-with-resources

## What it is

**try-with-resources** (Java 7+) is a `try` block that declares one or more `AutoCloseable` resources. The compiler guarantees each is closed at the end of the block, even if an exception is thrown. No `finally`, no leaked resources, no "did I close the Statement or not?" mental overhead.

```java
try (Connection c = dataSource.getConnection();
     PreparedStatement ps = c.prepareStatement("SELECT name FROM intern WHERE intern_id = ?")) {
    ps.setLong(1, id);
    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) {
            return rs.getString("name");
        }
    }
    return null;
}   // rs.close(), ps.close(), c.close() all called automatically, in reverse order
```

## Why it matters for JDBC

Every JDBC object - `Connection`, `Statement`, `PreparedStatement`, `CallableStatement`, `ResultSet` - is `AutoCloseable`. If you don't close them, you leak:

- **Connections** - the pool runs dry; new requests block.
- **Statements** - the server-side cursor stays open; `ORA-01000: maximum open cursors exceeded`.
- **ResultSets** - the underlying fetch cursor stays open; same as above.

The pre-Java-7 pattern was verbose and error-prone:

```java
Connection c = null;
PreparedStatement ps = null;
ResultSet rs = null;
try {
    c = dataSource.getConnection();
    ps = c.prepareStatement(SQL);
    rs = ps.executeQuery();
    ...
} catch (SQLException e) {
    ...
} finally {
    if (rs != null) try { rs.close(); } catch (SQLException ignored) {}
    if (ps != null) try { ps.close(); } catch (SQLException ignored) {}
    if (c  != null) try { c.close();  } catch (SQLException ignored) {}
}
```

Every `close()` can throw, every `close()` must be in its own try, and forgetting one leaks. The try-with-resources version is shorter, correct, and the compiler checks it.

## Suppressed exceptions

If both the `try` body and the `close()` throw, the body's exception is primary; the close's exception is **suppressed** (attached via `addSuppressed`). You see both in the stack trace. This is better than the old pattern, where the close's exception silently replaced the body's.

## Resource ordering

Resources are closed in **reverse order of declaration** - innermost first. So `ResultSet` closes before `PreparedStatement` before `Connection`. This is the correct order: closing a `Connection` implicitly closes its statements, but explicit closing is clearer and works with pools.

## Effectively final

The resource variable is **effectively final** within the try block - you can't reassign it. This is a feature: it guarantees the compiler can close the original resource, not whatever you reassigned it to.

```java
try (Connection c = ds.getConnection()) {
    c = anotherConnection;   // compile error
}
```

## Spring's `JdbcTemplate` does this for you

`JdbcTemplate.query`, `update`, `execute` all open and close resources internally. You write a `RowMapper` or a `PreparedStatementCallback`; Spring handles the rest:

```java
String name = jdbc.queryForObject(
    "SELECT name FROM intern WHERE intern_id = ?",
    String.class, id);
```

No `Connection`, no `PreparedStatement`, no `ResultSet` to manage. See [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]].

## Project Connection

The project's `oracleConnector` does **not** use try-with-resources. Connections are static and never closed; statements are local but only sometimes closed:

```java
public static void insertIntern(...) {
    Statement stmt = connection.createStatement();   // never closed
    stmt.executeUpdate("INSERT INTO ...");
    // stmt leaks; cursor count grows; eventually ORA-01000
}
```

Even worse, the static `connection` is never closed, so when the DB restarts, the connection is stale and every query fails until the JVM restarts.

The redesign uses try-with-resources everywhere, or - better - `JdbcTemplate` which handles it.

## Common pitfalls

- Declaring the resource **outside** the try - the compiler can't close it:

  ```java
  Connection c = ds.getConnection();
  try { ... } finally { c.close(); }   // pre-Java-7 style; still works, but no suppressed exceptions
  ```

  Move the declaration **inside** the try header.

- Forgetting that closing a `Connection` returned from a pool **returns it to the pool**, not closes the physical connection. (This is what you want - but it confuses people who expect the physical connection to close.)

- Using try-with-resources on a `ResultSet` returned from a method - the `Statement` that produced it is closed at method return; the `ResultSet` is now invalid.

## Further reading

- [[03 - Java Foundations/16 - try-with-resources Deep Dive]]
- [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]]
