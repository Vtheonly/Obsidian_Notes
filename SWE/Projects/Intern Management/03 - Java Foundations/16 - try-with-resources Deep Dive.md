---
tags: [concept, java, exceptions, resources]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/02 - Exception Handling]]
related:
  - [[13 - JDBC and Data Access/00 - MOC - JDBC]]
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
---

# try-with-resources Deep Dive

## What it is

`try-with-resources` (Java 7+) automatically closes resources that implement `AutoCloseable`. Resources are closed in reverse order of declaration, even if an exception occurs.

```java
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql);
     ResultSet rs = ps.executeQuery()) {
    // use conn, ps, rs
}  // rs.close(), then ps.close(), then conn.close() — all automatic
```

## Why it's better than try-finally

```java
// Old way (buggy)
Connection conn = null;
PreparedStatement ps = null;
try {
    conn = dataSource.getConnection();
    ps = conn.prepareStatement(sql);
    // ...
} finally {
    if (ps != null) ps.close();     // if this throws, conn.close() is skipped!
    if (conn != null) conn.close(); // leak
}
```

If `ps.close()` throws, `conn.close()` is never called — connection leak. try-with-resources handles this:

```java
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    // ...
} catch (SQLException e) {
    // ...
}
```

The compiler generates the equivalent of:
```java
Connection conn = null;
PreparedStatement ps = null;
Throwable primary = null;
try {
    conn = dataSource.getConnection();
    ps = conn.prepareStatement(sql);
    // ...
} catch (Throwable t) {
    primary = t;
    throw t;
} finally {
    if (ps != null) {
        if (primary != null) {
            try { ps.close(); } catch (Throwable suppressed) {
                primary.addSuppressed(suppressed);
            }
        } else {
            ps.close();
        }
    }
    // same for conn
}
```

Suppressed exceptions are attached to the primary exception and accessible via `getSuppressed()`.

## AutoCloseable vs Closeable

- `AutoCloseable` (Java 7+) — `close()` can throw any `Exception`.
- `Closeable` (Java 5, `java.io`) — `close()` throws `IOException`. `Closeable` extends `AutoCloseable`. Idempotent (calling `close()` twice is safe).

## Custom AutoCloseable

```java
public class Timer implements AutoCloseable {
    private final long start = System.nanoTime();
    private final String name;
    public Timer(String name) { this.name = name; }
    @Override public void close() {
        System.out.println(name + " took " + (System.nanoTime() - start) / 1_000_000 + "ms");
    }
}

try (Timer t = new Timer("search")) {
    // do work
}
```

## Common pitfalls

- **Not using it** — the project's `oracleConnector` uses try-finally in half its methods, risking resource leaks.
- **Declaring resources outside the try** — defeats the purpose.
- **Closing manually inside the try** — double-close (usually harmless but confusing).
- **Using try-with-resources for non-resources** — only use it for `AutoCloseable` objects.

## Project Connection

The project uses try-with-resources correctly in:
- `isAdmin`, `isChief`, `login` (nested PreparedStatement + ResultSet).
- `searchIntern`, `searchWorkerUser`.
- `getIdByName`, `getNameById`, `getSelectableOptions`.
- `updateInter`, `updateWorkerUser`, `updateChiefDecision`.
- `setAllInternsAccepted`, `setAllInternsRejected`.
- `isColumnExist`.

But uses try-finally (or nothing) in:
- `insertIntern`, `insertTheme`, `insertDepartment`, `insertWorkerUser`.
- `searchTheme`, `searchDepartment`.
- All `deleteX` methods.
- `getMaxId`.
- `getUserAccessLevel`.

The fix: convert all try-finally to try-with-resources.

## Further reading

- *Effective Java* (Bloch), Item 9 (prefer try-with-resources).
- JLS §14.20.3 (try-with-resources).
