---
tags: [concept, jdbc, java, data-access, spring, named-parameter]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]]
related:
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
  - [[13 - JDBC and Data Access/01 - Batch Operations in JDBC]]
---

# NamedParameterJdbcTemplate

## What it is

**`NamedParameterJdbcTemplate`** is a wrapper around `JdbcTemplate` that lets you use **named parameters** (`:name`) instead of positional `?`. This makes complex SQL readable and lets you pass a `Map` or a `MapSqlParameterSource` of parameters.

```java
NamedParameterJdbcTemplate npjdbc = new NamedParameterJdbcTemplate(jdbc);

List<Intern> results = npjdbc.query(
    "SELECT * FROM intern WHERE name LIKE :name AND department_id = :deptId",
    Map.of("name", "%" + search + "%", "deptId", deptId),
    new InternRowMapper());
```

Compare to the positional version:

```java
jdbc.query(
    "SELECT * FROM intern WHERE name LIKE ? AND department_id = ?",
    new Object[]{"%" + search + "%", deptId},
    new InternRowMapper());
```

With 5+ parameters, the positional version becomes a "count the `?`s" puzzle. The named version is self-documenting.

## The IN-clause trick

The killer feature: `NamedParameterJdbcTemplate` expands a `List` parameter into an `IN (?, ?, ?)` list automatically:

```java
List<Intern> interns = npjdbc.query(
    "SELECT * FROM intern WHERE intern_id IN (:ids)",
    Map.of("ids", List.of(1L, 2L, 3L, 4L, 5L)),
    new InternRowMapper());
```

With plain `JdbcTemplate`, you'd have to build the SQL dynamically with the right number of `?`s. With `NamedParameterJdbcTemplate`, you just pass a `List`.

## MapSqlParameterSource

For more control (typed nulls, multi-value), use `MapSqlParameterSource`:

```java
SqlParameterSource params = new MapSqlParameterSource()
    .addValue("name", name)
    .addValue("age", age, Types.INTEGER)
    .addValue("ids", idList);

npjdbc.query(SQL, params, mapper);
```

## BeanPropertySqlParameterSource

Wrap a JavaBean and use its properties as parameters:

```java
Intern filter = new Intern();
filter.setName("Alice");
filter.setDepartmentId(5L);

npjdbc.query(
    "SELECT * FROM intern WHERE name = :name AND department_id = :departmentId",
    new BeanPropertySqlParameterSource(filter),
    mapper);
```

The parameter names (`name`, `departmentId`) come from the bean's property names. Convenient for "search by example" patterns.

## Wrapping

`NamedParameterJdbcTemplate` wraps a `JdbcTemplate` (or a `DataSource`). You typically declare both as beans:

```java
@Bean
public JdbcTemplate jdbcTemplate(DataSource ds) {
    return new JdbcTemplate(ds);
}

@Bean
public NamedParameterJdbcTemplate namedParameterJdbcTemplate(DataSource ds) {
    return new NamedParameterJdbcTemplate(ds);
}
```

Internally, `NamedParameterJdbcTemplate` translates `:name` to `?` and re-orders the parameters, then delegates to a `JdbcTemplate`.

## Why it matters

For any query with more than 2-3 parameters, named parameters are clearer. The IN-clause expansion alone is worth the wrapper. Most Spring JDBC code ends up using `NamedParameterJdbcTemplate` as the default.

## Project Connection

The project's `oracleConnector.searchIntern` builds SQL by string concatenation:

```java
String query = "SELECT * FROM "intern" WHERE " + field + " LIKE '%" + value + "%'";
```

This is SQL injection waiting to happen. The redesign with `NamedParameterJdbcTemplate`:

```java
public List<Intern> search(String field, String value) {
    // field is whitelisted to a known set, not interpolated
    String column = allowedColumns.get(field);
    if (column == null) throw new IllegalArgumentException();

    return npjdbc.query(
        "SELECT * FROM intern WHERE " + column + " LIKE :pattern",
        Map.of("pattern", "%" + value + "%"),
        mapper);
}
```

The column name must be whitelisted (you can't use a parameter for an identifier), but the value is safely parameterized.

## Common pitfalls

- Forgetting the `:` prefix - `WHERE name = name` is valid SQL (column = column), but `WHERE name = :name` is the named-parameter form.
- Mixing named and positional - `WHERE name = :name AND age = ?` doesn't work. Pick one per statement.
- Expecting the IN-clause expansion to work with arrays - it works with `List`s (and some other collections), but raw arrays may not expand correctly.
- Forgetting that `BeanPropertySqlParameterSource` uses **getter-derived** property names - `isActive` becomes `active`, not `isActive`.

## Further reading

- Spring Docs, "NamedParameterJdbcTemplate".
- [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]]
