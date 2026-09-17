---
tags: [concept, jdbc, resultset, rowmapper]
type: concept
status: complete
related:
  - [[13 - JDBC and Data Access/14 - Spring JDBC (JdbcTemplate)]]
---

# ResultSet and RowMapper

## ResultSet

A `ResultSet` is an iterator over query results. You call `next()` to advance to the next row, then `getXxx()` to read columns.

```java
try (PreparedStatement ps = conn.prepareStatement("SELECT intern_id, name, age FROM interns")) {
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
            long id = rs.getLong("intern_id");
            String name = rs.getString("name");
            int age = rs.getInt("age");
            // ...
        }
    }
}
```

## Column access

- By name: `rs.getString("name")` — preferred (readable, refactoring-safe).
- By index: `rs.getString(2)` — slightly faster, but fragile (column order changes).

## NULL handling

```java
int age = rs.getInt("age");  // returns 0 if NULL!
boolean wasNull = rs.wasNull();  // check after
```

Or use `getObject`:
```java
Integer age = (Integer) rs.getObject("age");  // returns null if NULL
```

## RowMapper (Spring JDBC)

A `RowMapper<T>` maps one row to an object:

```java
public class InternRowMapper implements RowMapper<Intern> {
    @Override
    public Intern mapRow(ResultSet rs, int rowNum) throws SQLException {
        return new Intern(
            rs.getLong("intern_id"),
            rs.getString("name"),
            rs.getInt("age"),
            rs.getString("email"),
            (Integer) rs.getObject("theme_id")  // nullable
        );
    }
}

// Usage
List<Intern> interns = jdbcTemplate.query("SELECT * FROM interns", new InternRowMapper());
```

The `RowMapper` centralizes the row-to-object mapping. Reused across queries.

## Project Connection

The project uses `Map<String, Object>` instead of typed objects — no RowMapper, no type safety. The fix: `InternRowMapper` that maps rows to `Intern` records.

## Further reading

- Spring JDBC `RowMapper` documentation.
