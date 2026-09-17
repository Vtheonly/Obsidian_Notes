---
tags: [concept, jdbc, java, data-access, resultset]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
related:
  - [[13 - JDBC and Data Access/12 - RowMapper]]
  - [[13 - JDBC and Data Access/18 - try-with-resources]]
---

# ResultSet

## What it is

A **`ResultSet`** is the cursor over the rows returned by a query. You call `next()` to advance to the next row; `getXxx()` to read column values; `close()` (via try-with-resources) when done.

```java
try (PreparedStatement ps = conn.prepareStatement("SELECT * FROM intern");
     ResultSet rs = ps.executeQuery()) {
    while (rs.next()) {
        long id = rs.getLong("intern_id");
        String name = rs.getString("name");
        String status = rs.getString("is_accepted");
        Date start = rs.getDate("start_date");
    }
}
```

## Cursor types

JDBC defines three cursor types; Oracle supports two:

| Type | Scroll? | Updateable? | Notes |
|---|---|---|---|
| `TYPE_FORWARD_ONLY` | Forward only | No | Default; cheapest. |
| `TYPE_SCROLL_INSENSITIVE` | Both directions | No | Oracle supports via a temp copy. |
| `TYPE_SCROLL_SENSITIVE` | Both directions | Yes | Oracle: live updates from other txns. Limited. |

For 99% of queries, `TYPE_FORWARD_ONLY` is what you want. Scrollable cursors are expensive and rarely useful - if you need to revisit rows, materialize them into a `List`.

## Fetch size

`setFetchSize(n)` hints how many rows the driver should fetch per round-trip. Default is 10 for Oracle - tiny. For a query that returns 1000 rows, that's 100 round-trips. Set higher for bulk reads:

```java
ps.setFetchSize(500);
```

The driver may ignore the hint; Oracle's JDBC driver honors it.

## Reading columns

```java
// By index (1-based!) - slightly faster
String name = rs.getString(2);

// By name - more readable, robust to column reordering
String name = rs.getString("name");
```

JDBC column indices are **1-based**, not 0-based. This catches everyone.

For nullable NUMBER columns, use the `getObject` pattern to distinguish 0 from NULL:

```java
Object ageObj = rs.getObject("age");
Integer age = (ageObj == null) ? null : ((Number) ageObj).intValue();
```

`rs.getInt("age")` returns 0 for both NULL and actual 0 - you'd need `wasNull()` to tell them apart.

## NULL handling

```java
int age = rs.getInt("age");
if (rs.wasNull()) {
    age = -1;   // or use Integer instead of int
}
```

`wasNull()` must be called **immediately after** the `getXxx` for the nullable column; calling another `getXxx` clears the flag.

The cleaner pattern: use `getObject` and check for null.

## Streams for LOBs

For CLOB/BLOB columns, use the streaming getters to avoid loading the entire LOB into memory:

```java
try (Reader r = rs.getCharacterStream("payload")) {
    // stream the CLOB, e.g., to a file or JSON parser
}
```

## Why it matters

`ResultSet` is the lowest-level JDBC API - everything else (`RowMapper`, `JdbcTemplate`, JPA) builds on it. Understanding it tells you why `JdbcTemplate` exists: to handle the cursor lifecycle, the column extraction, and the try-with-resources boilerplate.

## Project Connection

The project uses `ResultSet` directly:

```java
ResultSet rs = stmt.executeQuery("SELECT * FROM "intern"");
while (rs.next()) {
    int deptId = rs.getInt("department_id");
    String deptName = oracleConnector.getNameById(...);   // N+1!
    HashMap<String, Object> row = new HashMap<>();
    row.put("id", rs.getInt("intern_id"));
    row.put("name", rs.getString("name"));
    row.put("department", deptName);
    results.add(row);
}
```

Issues:
- `SELECT *` - fragile; adding a column changes the result.
- Maps instead of typed objects - no compile-time checking.
- No fetch size set - 10-row fetches.
- N+1 - the per-row `getNameById` is a separate query.

The redesign uses `RowMapper` and `JdbcTemplate` to handle this cleanly. See [[13 - JDBC and Data Access/12 - RowMapper]].

## Common pitfalls

- Using `rs.getInt("age")` for a nullable column and not checking `wasNull()` - 0 leaks in for NULL.
- Forgetting to close the `ResultSet` (and the `Statement` it came from) - cursor leak.
- Calling `rs.getXxx` after `rs.next()` returns false - `SQLException: Exhausted ResultSet`.
- Using `rs.getString(1)` (index-based) after a schema change reorders columns - silent wrong data.

## Further reading

- Oracle Docs, "JDBC Developer's Guide", "ResultSet".
- [[13 - JDBC and Data Access/12 - RowMapper]]
