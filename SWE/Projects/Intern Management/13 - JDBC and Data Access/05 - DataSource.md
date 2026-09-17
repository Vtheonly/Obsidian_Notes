---
tags: [concept, jdbc, datasource]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/09 - Connection Pooling]]
  - [[11 - DB Performance and Indexing/15 - HikariCP]]
---

# DataSource

## What it is

`javax.sql.DataSource` is the JDBC interface for obtaining connections. It replaces `DriverManager` for production code.

## DataSource vs DriverManager

| | DriverManager | DataSource |
|---|---|---|
| Connection creation | Opens a new connection each time | Can pool connections |
| Configuration | Hardcoded URL/user/pass | Configurable, JNDI-bindable |
| Logging | None | Can log |
| XA (distributed transactions) | No | Yes (XADataSource) |

## Usage

```java
// DriverManager (avoid)
Connection conn = DriverManager.getConnection("jdbc:oracle:thin:@localhost:1521:XE", "user", "pass");

// DataSource (preferred)
DataSource ds = new HikariDataSource(config);
Connection conn = ds.getConnection();
```

## Why DataSource

- **Pooling** — `DataSource` implementations (HikariCP, Oracle UCP) pool connections.
- **JNDI** — in an app server, the DataSource is registered in JNDI; the app looks it up. Decouples config from code.
- **Testing** — inject a `DataSource` mock in tests.
- **XA** — `XADataSource` supports distributed transactions (two-phase commit).

## Project Connection

The project uses `DriverManager.getConnection` in a static initializer. The fix: HikariCP `DataSource`, injected via constructor.

## Further reading

- JDBC `javax.sql.DataSource` documentation.
