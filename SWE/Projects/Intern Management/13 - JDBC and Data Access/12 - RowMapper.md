---
tags: [concept, jdbc, java, data-access, rowmapper, spring]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/11 - ResultSet]]
related:
  - [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]]
  - [[07 - Refactoring Techniques/09 - Replace Data Value with Object]]
---

# RowMapper

## What it is

A **`RowMapper<T>`** is a Spring JDBC interface that maps one row of a `ResultSet` to one object of type `T`. You implement it once per table; `JdbcTemplate` calls it for each row.

```java
public class InternRowMapper implements RowMapper<Intern> {
    @Override
    public Intern mapRow(ResultSet rs, int rowNum) throws SQLException {
        return new Intern(
            rs.getLong("intern_id"),
            rs.getString("name"),
            rs.getString("is_accepted"),
            rs.getDate("start_date").toLocalDate(),
            rs.getLong("department_id"),
            rs.getLong("theme_id")
        );
    }
}
```

Usage:

```java
List<Intern> interns = jdbc.query(
    "SELECT intern_id, name, is_accepted, start_date, department_id, theme_id FROM intern",
    new InternRowMapper());
```

`JdbcTemplate` handles the `Connection`, `PreparedStatement`, `ResultSet`, the `while (rs.next())` loop, the try-with-resources, the exception translation - you just write the per-row mapping.

## Why it exists

The raw JDBC pattern is verbose and repetitive:

```java
List<Intern> interns = new ArrayList<>();
try (PreparedStatement ps = conn.prepareStatement(SQL);
     ResultSet rs = ps.executeQuery()) {
    while (rs.next()) {
        interns.add(new Intern(
            rs.getLong("intern_id"),
            rs.getString("name"),
            // ... 6 more columns ...
        ));
    }
} catch (SQLException e) {
    throw new RuntimeException(e);
}
return interns;
```

Every query has the same boilerplate (open, loop, close, translate). `RowMapper` extracts the only varying part - the per-row mapping - and lets `JdbcTemplate` own the rest.

## RowMapper vs ResultSetExtractor

- **`RowMapper<T>`** - maps one row to one object. Use for `SELECT` queries that return a list.
- **`ResultSetExtractor<T>`** - processes the whole `ResultSet` yourself. Use for queries that produce a non-list result (e.g., a single aggregate, a parent-children tree from a join).
- **`RowCallbackHandler`** - processes each row without returning a value. Use for streaming (write each row to a file).

## Mapping to records (Java 16+)

```java
public record InternRow(Long id, String name, String status) {}

public class InternRowMapper implements RowMapper<InternRow> {
    public InternRow mapRow(ResultSet rs, int rowNum) throws SQLException {
        return new InternRow(rs.getLong("intern_id"), rs.getString("name"), rs.getString("is_accepted"));
    }
}
```

Records are immutable and concise - ideal for row mappers.

## BeanPropertyRowMapper

For trivial cases (column names match field names), Spring's `BeanPropertyRowMapper` does the mapping by convention:

```java
List<Intern> interns = jdbc.query(
    "SELECT intern_id AS id, is_accepted AS status FROM intern",
    new BeanPropertyRowMapper<>(Intern.class));
```

Underscores in column names map to camelCase field names (`intern_id` -> `internId`). It uses reflection, so it's slower than a hand-written mapper, but for low-volume queries it's fine.

## Why it matters

`RowMapper` is the workhorse of Spring JDBC. It replaces the boilerplate of raw JDBC with a one-method interface that's easy to test (just pass a mock `ResultSet`), easy to reuse (one mapper per table), and easy to read.

## Project Connection

The project doesn't use `RowMapper` (it doesn't use Spring JDBC at all). Each query in `oracleConnector` manually builds a `HashMap<String, Object>` from the `ResultSet` - untyped, error-prone, and duplicated across 25 methods.

The redesign moves to `RowMapper`:

```java
@Repository
public class JdbcInternRepository implements InternRepository {
    private final JdbcTemplate jdbc;
    private final InternRowMapper mapper = new InternRowMapper();

    public List<Intern> findByDepartment(long deptId) {
        return jdbc.query(
            "SELECT * FROM intern WHERE department_id = ?",
            mapper, deptId);
    }
}
```

The mapper is one place; the SQL is in one place; the boilerplate is gone.

## Common pitfalls

- Using `SELECT *` and a mapper that reads by column name - adding a column doesn't break the mapper, but removing one does. Prefer explicit column lists.
- Forgetting that column-name lookups are case-insensitive in JDBC - `rs.getString("NAME")` and `rs.getString("name")` both work. Use the casing that matches your schema.
- Mapping NULL to a primitive - `rs.getLong` returns 0 for NULL. Use `Long` (object) and check for null, or use `rs.getObject`.

## Further reading

- Spring Docs, "Data Access with JDBC", "RowMapper".
- [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]]
- [[07 - Refactoring Techniques/09 - Replace Data Value with Object]]
