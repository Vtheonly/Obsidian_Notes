---
tags: [concept, database, jdbc, thread-safety]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/10 - Processes and Threads (OS view)]]
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
related:
  - [[11 - DB Performance and Indexing/09 - Connection Pooling]]
  - [[11 - DB Performance and Indexing/15 - HikariCP]]
---

# Connection Is Not Thread-Safe

## The rule

> JDBC `Connection` objects are **not thread-safe**. A `Connection` may only be used by one transaction (and effectively one thread) at a time. — JDBC 4.3 §9.5

## Why

A `Connection` holds:
- A socket to the DB.
- Server-side session state (timezone, NLS settings).
- Transaction state (in-progress transaction, isolation level).
- Statement cache.

If two threads use the same connection simultaneously:
- Thread A starts a transaction.
- Thread B autocommits its own update — which silently commits A's transaction.
- Thread A's rollback fails — nothing to roll back.
- The connection's transaction state is corrupted.

Oracle's driver serializes execution on a single connection (it locks internally), so you don't get *corruption* — you get *mysterious transaction bugs*. Other drivers may corrupt.

## The project's bug

```java
public class oracleConnector {
    private static Connection connection;  // ONE connection, shared across all threads
    static {
        connection = DriverManager.getConnection(...);
    }
}
```

Every controller calls `oracleConnector.searchIntern(...)` etc. All on the JavaFX Application Thread today — so it "works." But:

1. The moment any background work is added (which the fix does — see [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]]), two threads share the connection → corruption.
2. The connection is never validated. If it dies (network blip, DB restart), every subsequent operation fails.
3. No pooling — every operation serializes through one connection.

## The fix: connection pool

Use HikariCP to maintain a pool of connections. Each operation borrows a connection, uses it, returns it.

```java
public class OracleInternRepository implements InternRepository {
    private final HikariDataSource dataSource;

    public void save(Intern intern) throws SQLException {
        try (Connection conn = dataSource.getConnection()) {  // borrow
            try (PreparedStatement ps = conn.prepareStatement(sql)) {
                // ...
                ps.executeUpdate();
            }
        }  // return to pool (try-with-resources)
    }
}
```

Each thread gets its own connection. No sharing. No corruption.

## Why not synchronize?

```java
public synchronized void save(Intern intern) { ... }  // bad
```

This serializes all DB access — one operation at a time. Defeats the purpose of concurrency. A pool allows parallel operations.

## Further reading

- JDBC 4.3 Specification, §9.5.
- HikariCP wiki — About Pool Sizing.
