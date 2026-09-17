---
tags: [concept, jdbc, java, data-access, spring, jdbctemplate]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/12 - RowMapper]]
  - [[13 - JDBC and Data Access/18 - try-with-resources]]
related:
  - [[13 - JDBC and Data Access/08 - NamedParameterJdbcTemplate]]
  - [[13 - JDBC and Data Access/13 - SQLException Translation]]
  - [[05 - Software Architecture/14 - Repository Pattern]]
---

# Spring JdbcTemplate

## What it is

**`JdbcTemplate`** is Spring's central JDBC helper. It eliminates the boilerplate of `Connection` / `PreparedStatement` / `ResultSet` / try-with-resources / exception translation, leaving you to write only the SQL and the row mapping.

```java
@Repository
public class JdbcInternRepository implements InternRepository {
    private final JdbcTemplate jdbc;
    private final RowMapper<Intern> mapper = new InternRowMapper();

    public JdbcInternRepository(JdbcTemplate jdbc) { this.jdbc = jdbc; }

    public Optional<Intern> findById(long id) {
        try {
            return Optional.of(jdbc.queryForObject(
                "SELECT * FROM intern WHERE intern_id = ?",
                mapper, id));
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    public List<Intern> findByDepartment(long deptId) {
        return jdbc.query(
            "SELECT * FROM intern WHERE department_id = ?",
            mapper, deptId);
    }

    public long insert(Intern i) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(conn -> {
            PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO intern(name, is_accepted, department_id) VALUES (?, ?, ?)",
                new String[]{"intern_id"});
            ps.setString(1, i.getName());
            ps.setString(2, i.getStatus());
            ps.setLong(3, i.getDepartmentId());
            return ps;
        }, keyHolder);
        return keyHolder.getKey().longValue();
    }
}
```

## What JdbcTemplate does for you

- Opens a `Connection` from the `DataSource` (or uses the current transaction's connection).
- Creates the `PreparedStatement`.
- Sets the parameters.
- Executes the query.
- Iterates the `ResultSet`, calling your `RowMapper` per row.
- Closes everything (via try-with-resources internally).
- Translates `SQLException` to Spring's `DataAccessException` hierarchy. See [[13 - JDBC and Data Access/13 - SQLException Translation]].
- Logs SQL warnings.

You write: the SQL, the parameter array, and (for queries) a `RowMapper`.

## The main methods

| Method | Use |
|---|---|
| `query(sql, RowMapper, args...)` | SELECT returning a list |
| `queryForObject(sql, Class, args...)` | SELECT returning a single value |
| `queryForObject(sql, RowMapper, args...)` | SELECT returning a single object |
| `queryForList(sql, args...)` | SELECT returning `List<Map<String,Object>>` |
| `queryForMap(sql, args...)` | SELECT returning a single `Map` |
| `update(sql, args...)` | INSERT/UPDATE/DELETE |
| `update(PreparedStatementCreator, KeyHolder)` | INSERT with generated key |
| `batchUpdate(sql, BatchPreparedStatementSetter)` | Bulk INSERT/UPDATE |
| `execute(String)` | DDL |

## Why it matters

`JdbcTemplate` is the **modern, minimal** way to do JDBC in Java. It's lighter than JPA (no entity manager, no second-level cache, no N+1 surprises) and far safer than raw JDBC. For projects that don't need the object-graph magic of JPA, `JdbcTemplate` is the right choice.

The Spring Data JDBC project goes one step further: declare a `Repository` interface, get CRUD methods for free, with `JdbcTemplate` under the hood.

## Project Connection

The project's `oracleConnector` is essentially a hand-rolled, buggy `JdbcTemplate` - it has 25+ methods, each opening a `Statement`, running SQL, building a `HashMap`, and never closing. The redesign replaces all 25 methods with a `JdbcInternRepository` of ~5 methods, each a one-liner `jdbc.query(...)` or `jdbc.update(...)`.

The reduction in code is dramatic - 940 lines of `oracleConnector` becomes ~150 lines of repository code, with type safety, transaction support, exception translation, and no leaks.

## Common pitfalls

- Calling `queryForObject` for a query that might return 0 rows - throws `EmptyResultDataAccessException`. Catch it and return `Optional.empty()`, or use `query` and check `isEmpty()`.
- Calling `queryForObject` for a query that might return >1 row - throws `IncorrectResultSizeDataAccessException`. Add a `LIMIT 1` (or `FETCH FIRST 1 ROWS ONLY` in Oracle) to be safe.
- Using `queryForList` and treating the `Map<String, Object>` as typed - the values are `Object`; you cast and risk `ClassCastException`. Use a `RowMapper` instead.
- Forgetting that `JdbcTemplate` does **not** manage transactions by itself - wrap your repository methods in `@Transactional` (Spring handles the `setAutoCommit(false)` / `commit` / `rollback`).

## Trade-offs

- **`JdbcTemplate` vs JPA**: JdbcTemplate is simpler, more transparent (you see the SQL), and has no N+1 surprises. JPA handles object graphs, lazy loading, and caching - at the cost of complexity and "magic."
- **`JdbcTemplate` vs raw JDBC**: JdbcTemplate is strictly better for new code. The boilerplate it removes is exactly the boilerplate that introduces bugs.

## Further reading

- Spring Docs, "Data Access with JDBC".
- [[13 - JDBC and Data Access/08 - NamedParameterJdbcTemplate]]
- [[05 - Software Architecture/14 - Repository Pattern]]
