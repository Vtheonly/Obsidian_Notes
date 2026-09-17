---
tags: [concept, jdbc, java, data-access]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]
related:
  - [[13 - JDBC and Data Access/03 - Connection Pooling]]
  - [[11 - DB Performance and Indexing/14 - HikariCP Connection Pooling]]
  - [[08 - Relational DB Foundations/17 - Schemas and Users in Oracle]]
---

# DataSource vs DriverManager

## What it is

**`DriverManager`** is the original JDBC API (JDBC 1.0, 1997) for obtaining a connection. You call `DriverManager.getConnection(url, user, password)`; it loads the driver, opens a TCP socket, authenticates, and returns a fresh `Connection`.

**`DataSource`** is the newer API (JDBC 2.0 Optional Package, 1999). It's an interface; the implementation can be a pool, a JNDI lookup, a mock for tests. You ask the `DataSource` for a connection; what you get is up to the implementation.

```java
// DriverManager - 1990s style
Connection c = DriverManager.getConnection(
    "jdbc:oracle:thin:@//localhost:1521/XEPDB1",
    "app_user", "password");

// DataSource - modern style
HikariDataSource ds = new HikariDataSource(hikariConfig);
Connection c = ds.getConnection();
```

## Why DataSource is better

| Aspect | DriverManager | DataSource |
|---|---|---|
| Pooling | None | Built-in (or wrap with HikariCP) |
| JNDI lookup | No | Yes (app server managed) |
| Configuration | Hardcoded URL | Configurable, can be JNDI-bound |
| Hot-swap driver | No | Yes (replace the DataSource bean) |
| Testability | Hard (real DB required) | Easy (mock the DataSource) |
| Connection caching | None | The pool's job |

`DriverManager` opens a new physical connection every call - 50-200ms each. `DataSource` (when backed by a pool) lends a pre-opened connection - microseconds. For any production app, the choice is not "DataSource or DriverManager" but "which DataSource implementation".

## The JNDI pattern

In a Java EE / Jakarta EE app server (Tomcat, WildFly, WebLogic), the app server configures a `DataSource` and binds it to JNDI. The app looks it up:

```java
Context ctx = new InitialContext();
DataSource ds = (DataSource) ctx.lookup("java:comp/env/jdbc/internDS");
```

This decouples the app from the connection details - the same WAR runs in dev (pointing at a dev DB) and prod (pointing at a prod DB) without recompilation.

In Spring Boot, you skip JNDI and configure the `DataSource` as a bean:

```java
@Bean
@ConfigurationProperties("spring.datasource")
public DataSource dataSource() {
    return DataSourceBuilder.create().type(HikariDataSource.class).build();
}
```

```yaml
spring:
  datasource:
    url: jdbc:oracle:thin:@//localhost:1521/XEPDB1
    username: app_user
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 10
```

## The `DataSource` interface

```java
public interface DataSource extends CommonDataSource, Wrapper {
    Connection getConnection() throws SQLException;
    Connection getConnection(String username, String password) throws SQLException;
}
```

That's it. Two methods. The complexity is in the implementation - HikariDataSource, OracleDataSource, UCPDataSource, etc.

## Why it matters

Every modern JDBC tutorial, every Spring Boot app, every Jakarta EE app uses `DataSource`. `DriverManager` survives only in legacy code and quick-and-dirty scripts. If you see `DriverManager.getConnection` in production code, it's a code smell - the code was written pre-2000 or by someone who didn't know better.

## Project Connection

The project uses `DriverManager`:

```java
private static Connection connection;
static {
    try {
        Class.forName("oracle.jdbc.driver.OracleDriver");
        connection = DriverManager.getConnection(url, user, pass);
    } catch (Exception e) { ... }
}
```

Three problems:

1. **No pool** - one connection, no concurrency. See [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]].
2. **Static initialization** - if the DB is down at startup, the class fails to load and the whole app crashes. No retry, no fallback.
3. **Hardcoded credentials** - the URL, user, and password are in the source. Use environment variables or a secrets manager.

The redesign replaces this with a Spring Boot-configured HikariCP `DataSource`. See [[11 - DB Performance and Indexing/14 - HikariCP Connection Pooling]].

## Common pitfalls

- Using `DriverManager` and then wrapping it in a custom "pool" of `static Connection` references - that's not a pool, it's a leak waiting to happen.
- Calling `Class.forName("oracle.jdbc.driver.OracleDriver")` - not needed since JDBC 4.0 (Java 6); the driver auto-registers via `ServiceLoader`.
- Holding a `DataSource` reference and never closing it - the pool's threads and connections leak.

## Further reading

- Oracle Docs, "JDBC Developer's Guide", "DataSource".
- [[11 - DB Performance and Indexing/14 - HikariCP Connection Pooling]]
