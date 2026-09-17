---
tags: [concept, java, exceptions]
type: concept
status: complete
related:
  - [[03 - Java Foundations/16 - try-with-resources Deep Dive]]
  - [[27 - Testing/00 - MOC - Testing]]
---

# Exception Handling

## What it is

Java exceptions are objects that represent error conditions. The exception mechanism:
1. **Throw** — `throw new SQLException("...")` creates an exception object and unwinds the stack.
2. **Catch** — `try { ... } catch (SQLException e) { ... }` handles it.
3. **Propagate** — if not caught, the exception propagates up the call stack.

## Checked vs unchecked

| Type | Extends | Must declare? | Example |
|---|---|---|---|
| Checked | `Exception` | Yes (`throws` clause) | `SQLException`, `IOException` |
| Unchecked | `RuntimeException` | No | `NullPointerException`, `IllegalArgumentException` |
| Error | `Error` | No | `StackOverflowError`, `OutOfMemoryError` |

Checked exceptions are for **recoverable** conditions the caller should handle. Unchecked exceptions are for **programming errors** (bugs).

## try-catch-finally

```java
try {
    // code that may throw
} catch (SQLException e) {
    // handle
} catch (IOException e) {
    // handle
} finally {
    // always runs (even if try/catch returns)
}
```

Java 7+ multi-catch:
```java
try { ... }
catch (SQLException | IOException e) { ... }
```

## try-with-resources (Java 7+)

```java
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    // use conn and ps
}  // conn and ps are auto-closed, even if an exception occurs
```

Any object implementing `AutoCloseable` can be used. Resources are closed in reverse order of declaration. **Always prefer this over try-finally.**

## The project's inconsistent resource management

`oracleConnector` uses try-with-resources in some methods (login, isAdmin, searchIntern) and try-finally in others (insertIntern, deleteIntern, getMaxId, getUserAccessLevel). This inconsistency signals the author didn't understand when to use which.

### The bug with try-finally

```java
Connection conn = null;
PreparedStatement ps = null;
try {
    conn = dataSource.getConnection();
    ps = conn.prepareStatement(sql);
    // ...
} finally {
    if (ps != null) ps.close();     // may throw SQLException
    if (conn != null) conn.close(); // may throw SQLException
}
```

If `ps.close()` throws, `conn.close()` is never called — connection leak. try-with-resources handles this correctly (it uses suppressed exceptions).

## Common pitfalls

- Catching `Exception` (too broad) — catches everything including `NullPointerException`. Catch the most specific exception.
- Swallowing exceptions (`catch (Exception e) {}`) — hides bugs. At minimum, log.
- `e.printStackTrace()` — not logging. Use a logger.
- Throwing in a `finally` block — masks the original exception.
- Returning in a `finally` block — masks the original exception.
- Catching `NullPointerException` — fix the null instead.
- Using checked exceptions for programming errors — use unchecked.

## Project Connection

- `oracleConnector` mixes try-with-resources and try-finally inconsistently.
- ~30 catch blocks do `e.printStackTrace()` — not logging.
- `oracleConnector.insertWorkerUser` declares `throws SQLException` (the only method that does) — inconsistent.
- `isColumnExist` and `getSelectableOptions` wrap `SQLException` in `RuntimeException` — loses the original exception type.
- `makePDF` uses multi-catch `catch (DocumentException | IOException e)` — correct.

### Fix

```java
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    // ...
} catch (SQLException e) {
    log.error("Failed to insert intern", e);
    throw new DataAccessException("Database error", e);  // wrap in domain exception
}
```

See [[28 - Observability/07 - SLF4J and Logback]] and [[05 - Software Architecture/06 - Exception Translation]].

## Further reading

- *Effective Java* (Bloch), Items 69-77 (Exceptions).
- JLS §11 (Exceptions).
