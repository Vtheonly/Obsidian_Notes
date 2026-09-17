---
tags: [pattern, behavioral, template-method]
type: concept
status: complete
related:
  - [[06 - Design Patterns/17 - Strategy Pattern]]
  - [[05 - Software Architecture/14 - Repository Pattern]]
---

# Template Method Pattern

> "Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure." — GoF

## What it is

A **template method** is a method in a base class that defines the algorithm skeleton, calling abstract methods that subclasses implement.

```java
public abstract class AbstractJdbcRepository<T, ID> implements Repository<T, ID> {
    protected final DataSource dataSource;

    public AbstractJdbcRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    // Template method: defines the algorithm
    @Override
    public Optional<T> findById(ID id) {
        String sql = "SELECT * FROM " + tableName() + " WHERE " + idColumn() + " = ?";
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setObject(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? Optional.of(mapRow(rs)) : Optional.empty();
            }
        } catch (SQLException e) {
            throw new DataAccessException("findById failed", e);
        }
    }

    // Abstract methods: subclasses provide these
    protected abstract String tableName();
    protected abstract String idColumn();
    protected abstract T mapRow(ResultSet rs) throws SQLException;
}

public class OracleInternRepository extends AbstractJdbcRepository<Intern, Long> {
    public OracleInternRepository(DataSource ds) { super(ds); }

    @Override protected String tableName() { return "interns"; }
    @Override protected String idColumn() { return "intern_id"; }

    @Override protected Intern mapRow(ResultSet rs) throws SQLException {
        return new Intern(
            rs.getLong("intern_id"),
            rs.getString("name"),
            // ...
        );
    }
}
```

The base class defines `findById` — the algorithm is fixed. Each subclass provides `tableName()`, `idColumn()`, and `mapRow()` — the steps that vary.

## Why it exists

- **DRY** — the algorithm lives in one place (the base class).
- **Customization** — subclasses provide only the varying parts.
- **Control** — the base class controls the algorithm; subclasses can't change the structure.

## Template Method vs Strategy

- **Template Method** — inheritance. Subclasses override steps.
- **Strategy** — composition. Client injects a strategy.

Template Method is more rigid (the algorithm structure is fixed). Strategy is more flexible (any algorithm can be plugged in).

## When to use

- When you have several classes with similar algorithms but varying details.
- When the algorithm structure should be controlled by the base class.
- When subclasses should only override specific steps, not the whole algorithm.

## Project Connection

The project's 4 copy-pasted CRUD methods are the textbook case for Template Method. The fix: `AbstractJdbcRepository<T, ID>` with `save`, `findById`, `findAll`, `delete` as template methods. Each entity repository subclasses and provides `tableName()`, `idColumn()`, `mapRow()`, and `setInsertParams()`.

This collapses ~600 lines of duplicated CRUD to ~80 lines of generic code.

## Common pitfalls

- **Too many abstract methods** — subclasses have to implement too much. Split into smaller interfaces (ISP).
- **Hooks that nobody overrides** — if the template method has `hook()` that's always empty, remove it.
- **Final template method** — make the template method `final` so subclasses can't change the structure.

## Further reading

- *Design Patterns* (GoF), Template Method.
