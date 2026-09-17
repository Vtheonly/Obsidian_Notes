---
tags: [case-study, code-walkthrough, god-class, dao]
type: case-study
status: complete
related:
  - "[[05 - Software Architecture/17 - Smart UI Anti-Pattern]]"
  - "[[04 - OOD and SOLID/19 - Single Responsibility Principle (SRP)]]"
---

# oracleConnector.java (the God Class)

> 940 lines. Six distinct responsibilities. The single biggest architectural problem
> in the project.

## Responsibilities (all in one class)

1. **Connection lifecycle** — static `Connection` field, static initializer that opens it.
2. **Authentication queries** — `login`, `isAdmin`, `isChief`, `getUserAccessLevel`.
3. **CRUD for 4 entities** — `insertIntern`, `insertTheme`, `insertWorkerUser`, `insertDepartment`, plus search/update/delete for each.
4. **SQL string construction** — by `HashMap` iteration and `StringBuilder` surgery (`setLength(-2)` to strip trailing `, `).
5. **UI feedback** — ~30 calls to `JOptionPane.showMessageDialog` directly from the DAO.
6. **ID generation** — `getMaxId(table, col) + 1` for every insert (race condition).

## The static initializer

```java
private static final String URL = "jdbc:oracle:thin:@localhost:1521:XE";
private static final String USERNAME = "system";
private static final String PASSWORD = "rootroot";

private static Connection connection;

static {
    try {
        connection = getConnection(URL, USERNAME, PASSWORD);
        System.out.println("Connected!");
    } catch (SQLException e) {
        System.out.println("Failed to establish a connection to the Oracle database.");
        e.printStackTrace();
    }
}
```

### What's wrong
1. **Hardcoded `system` credentials** — `system` is SYSDBA-privileged, can `DROP DATABASE`. Should be a least-privilege app user.
2. **Static initializer with side effects** — opens a DB connection at class-load time, before the user has even seen the login screen. The class is loaded transitively when `loginController` is loaded, so the connection opens at app startup. If the DB is down, the app silently fails.
3. **`System.out.println("Connected!")`** — logging via stdout. No log level, no structure, no rotation.
4. **`e.printStackTrace()`** — leaks stack trace to stderr, not a logging strategy.
5. **Single static Connection** — JDBC `Connection` is not thread-safe (JDBC 4.3 §9.5). Once any background work is added, it breaks.
6. **No connection validation** — if the connection dies (network blip, DB restart), every subsequent operation fails. No retry, no recovery.
7. **No connection pool** — every thread competes for one connection.

## The login flow (3–4 round-trips)

```java
public static boolean login(String username, String password) {
    String query = "SELECT COUNT(*) FROM "worker_user" WHERE "username" = ? AND "password_hash" = ?";
    // returns count == 1
}
public static boolean isAdmin(String username, String password) {
    String query = "SELECT "role_id" FROM "worker_user" WHERE "username" = ? AND "password_hash" = ?";
    // returns roleId == 4
}
public static boolean isChief(String username, String password) { ... returns roleId == 5 }
public static int getUserAccessLevel(String username, String password) { ... returns roleId or -1 }
```

### What's wrong
1. **Sending the password hash to the DB for comparison** — the hash travels over the wire. If DB is remote and Oracle Net encryption isn't configured, it's plaintext on the network.
2. **4 separate round-trips for one login** — should be 1 query that returns the user row.
3. **Magic role IDs 4 and 5** — hardcoded. If the DBA renumbers roles, the app breaks.
4. **Username-exists oracle** — `login` returns false differently for "wrong password" vs. "no such user" (one returns 0 rows, the other returns count=0 — same result, but the role queries silently return falsey).
5. **`String.equals` for hash comparison** (in `toolkit.isHashEqual`, never called) — vulnerable to timing attacks. Should be `MessageDigest.isEqual()` (constant-time).

## Dynamic SQL by HashMap iteration

```java
public static void insertIntern(HashMap<String, Object> internData) {
    StringBuilder columns = new StringBuilder();
    StringBuilder placeholders = new StringBuilder();
    for (String key : internData.keySet()) {
        columns.append(""").append(key).append("", ");
        placeholders.append("?, ");
    }
    columns.setLength(columns.length() - 2);
    placeholders.setLength(placeholders.length() - 2);
    String sql = "INSERT INTO "intern" (" + columns + ") VALUES (" + placeholders + ")";
    // ... PreparedStatement, setObject per value in internData.values()
}
```

### What's wrong
1. **`HashMap.keySet()` and `values()` may diverge** — HashMap iteration order is undefined. Today it works by accident (both backed by the same map), but if anyone switches to `ConcurrentHashMap`, columns and values may desync → silent data corruption. See [[02 - CS Foundations/05 - Data Structures Overview]].
2. **No type safety** — `Map<String, Object>` accepts any value. `setObject` may or may not convert correctly.
3. **Quoted identifiers `"col"`** — forces case-sensitivity in Oracle. If the schema was created with unquoted identifiers (the default), this fails with `ORA-00904: invalid identifier`.
4. **String concatenation for column names** — `internData` keys come from the controller; if a user input ever ends up as a key, it's SQL injection. (Currently not exploitable because keys are hardcoded, but the API is unsafe.)
5. **No transaction** — `connection.commit()` is commented out. Auto-commit is on. Multi-step operations are not atomic.

## `getMaxId` race condition

```java
public static int getMaxId(String tableName, String columnName) {
    Statement stmt = connection.createStatement();
    ResultSet rs = stmt.executeQuery("SELECT MAX("" + columnName + "") FROM "" + tableName + """);
    rs.next();
    return rs.getInt(1);
}
```

Then in the controller: `int newId = oracleConnector.getMaxId("intern", "intern_id") + 1;`

### What's wrong
1. **Race condition** — two concurrent inserts both read MAX=100, both compute 101, both insert 101 → primary key violation. See [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]].
2. **`Statement` (not `PreparedStatement`)** — table/column names are concatenated. SQL injection vector if caller-controlled. (Currently hardcoded, but the API is unsafe.)
3. **`rs.getInt(1)`** — returns `0` if the table is empty (NULL → 0 via JDBC). Then `+1` = 1. Probably fine, but fragile.
4. **No try-with-resources** — `stmt` and `rs` leak if an exception occurs.
5. **O(N) scan** on every insert (or O(log N) if PK indexed). Should be O(1) amortized via Oracle IDENTITY.

## `JOptionPane` in the DAO

```java
} catch (SQLException e) {
    JOptionPane.showMessageDialog(null, "Failed to insert intern.", "Error", JOptionPane.ERROR_MESSAGE);
}
```

### What's wrong
1. **UI in the data layer** — catastrophic layering violation. The DAO cannot complete its operation without a graphical desktop session.
2. **Cannot run headless** — `java.awt.headless=true` throws `HeadlessException`. The DAO is untestable in CI.
3. **Swing + JavaFX on different event threads** — focus stealing, deadlocks on macOS, broken on Linux/Wayland.
4. **`null` parent** — the dialog appears at screen center, not over the JavaFX stage.
5. **`e.getMessage()` passed to user** — leaks internal Oracle error messages (table names, constraint names, ORA codes).

## The fix

Split into:
- `ConnectionManager` — HikariCP pool, lifecycle, validation.
- `CrudRepository<T, ID>` interface + `AbstractJdbcRepository<T, ID>` template.
- Per-entity repositories: `InternRepository`, `WorkerUserRepository`, `ThemeRepository`, `DepartmentRepository`.
- Service layer: `AuthService`, `InternService`, `ChiefDecisionService`.
- Throw typed exceptions (`DuplicateEmailException`, `NotFoundException`) from the DAO. Controllers translate to JavaFX `Alert`.

See [[05 - Software Architecture/14 - Repository Pattern]] and [[13 - JDBC and Data Access/00 - MOC - JDBC]].
