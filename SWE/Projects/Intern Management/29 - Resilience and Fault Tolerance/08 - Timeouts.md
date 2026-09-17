---
tags: [concept, resilience, timeout]
type: concept
status: complete
---

# Timeouts

## What it is

A **timeout** is the maximum time to wait for an operation. After the timeout, the operation fails.

## Why

- **Don't wait forever** — a hung DB shouldn't freeze the app.
- **Resource release** — a timed-out call releases its resources.
- **User experience** — show an error after 5 seconds, not 5 minutes.

## Types

### Connect timeout
How long to wait for the TCP connection. Default 0 (infinite) in many libraries — **always set this**.

### Read timeout
How long to wait for data after connecting. Default 0 (infinite) — **always set this**.

### Query timeout (JDBC)
```java
PreparedStatement ps = conn.prepareStatement(sql);
ps.setQueryTimeout(5);  // 5 seconds
```

## HikariCP timeouts

```java
config.setConnectionTimeout(30_000);  // 30 sec to get a connection from pool
config.setValidationTimeout(5_000);   // 5 sec for connection validation
```

## Setting the right timeout

- **Local network** — 1-5 sec.
- **Cross-region** — 5-30 sec.
- **User-facing** — 30 sec max (users won't wait longer).

Too short → spurious failures. Too long → user waits forever.

## Project Connection

The project has no timeouts. A slow query blocks forever. The fix:
- HikariCP: `connectionTimeout=30s`, `maxLifetime=30min`.
- JDBC: `setQueryTimeout(5)` on every statement.
- JavaFX `Task`: cancel after 30 sec.

## Further reading

- *Release It!* (Nygard).
