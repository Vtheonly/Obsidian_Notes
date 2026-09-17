---
tags: [concept, spring, jdbc, jdbctemplate]
type: concept
status: complete
related:
  - [[13 - JDBC and Data Access/10 - ResultSet and RowMapper]]
  - [[13 - JDBC and Data Access/13 - SQLException Translation]]
---

# Spring JDBC (JdbcTemplate)

## What it is

`JdbcTemplate` is Spring's wrapper around JDBC. It eliminates boilerplate (connection management, statement creation, result set iteration, exception translation) while keeping you in control of SQL.

## Without JdbcTemplate

```java
public Intern findById(long id) {
    String sql = "SELECT * FROM interns WHERE intern_id = ?";
    try (Connection conn = dataSource.getConnection();
         PreparedStatement ps = conn.prepareStatement(sql)) {
        ps.setLong(1, id);
        try (ResultSet rs = ps.executeQuery()) {
            if (rs.next()) {
                return new Intern(rs.getLong("intern_id"), rs.getString("name"), ...);
            }
            return null;
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
```

## With JdbcTemplate

```java
public class InternRepository {
    private final JdbcTemplate jdbc;

    public Intern findById(long id) {
        return jdbc.queryForObject(
            "SELECT * FROM interns WHERE intern_id = ?",
            new InternRowMapper(),
            id
        );
    }

    public void save(Intern intern) {
        jdbc.update(
            "INSERT INTO interns (name, age, email) VALUES (?, ?, ?)",
            intern.getName(), intern.getAge(), intern.getEmail()
        );
    }
}
```

JdbcTemplate handles connection borrowing, statement creation, parameter binding, ResultSet iteration, and exception translation.

## Key methods

| Method | Purpose |
|---|---|
| `query(sql, rowMapper, args)` | Query for a list. |
| `queryForObject(sql, rowMapper, args)` | Query for one object. |
| `queryForList(sql, elementType, args)` | Query for a list of primitives. |
| `update(sql, args)` | INSERT/UPDATE/DELETE. |
| `batchUpdate(sql, batchSetter)` | Batch operations. |
| `execute(sql)` | DDL. |

## NamedParameterJdbcTemplate

Uses named parameters instead of `?`:
```java
Map<String, Object> params = Map.of("name", "Alice", "age", 22);
namedJdbc.update(
    "INSERT INTO interns (name, age) VALUES (:name, :age)",
    params
);
```

More readable for many parameters.

## SQLException translation

JdbcTemplate translates `SQLException` to Spring's `DataAccessException` hierarchy:
- `DuplicateKeyException` (ORA-00001)
- `DataIntegrityViolationException` (ORA-02291 FK violation)
- `DataAccessException` (root)

Your code catches `DataAccessException`, not `SQLException`. Vendor-agnostic.

## Project Connection

The project's `oracleConnector` is manual JDBC — verbose, error-prone, no exception translation. The fix: Spring `JdbcTemplate` or manual repository classes with `RowMapper`.

## Further reading

- Spring Framework documentation — JDBC.
