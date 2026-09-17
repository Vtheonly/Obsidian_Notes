---
tags: [concept, pattern, repository]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[05 - Software Architecture/05 - Domain-Driven Design]]
  - [[13 - JDBC and Data Access/00 - MOC - JDBC]]
---

# Repository Pattern

> "Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects." — Martin Fowler, P of EAA

## What it is

A **repository** is an object that provides a collection-like interface for accessing domain objects. It hides the persistence details (SQL, JDBC, ORM) behind a clean interface.

```java
public interface InternRepository {
    Optional<Intern> findById(long id);
    List<Intern> findAll();
    List<Intern> findByFilters(InternSearchCriteria criteria);
    void save(Intern intern);
    void delete(long id);
}
```

The service layer calls `repository.findById(123)` — it doesn't know (or care) whether the data comes from Oracle, PostgreSQL, a file, or memory.

## Why it exists

1. **Decoupling** — the service layer doesn't know about JDBC, SQL, or Oracle.
2. **Testability** — in tests, inject an `InMemoryInternRepository` (a fake) instead of the real `OracleInternRepository`.
3. **Clarity** — the interface documents what queries are possible. No scattered SQL strings.
4. **Consistency** — all persistence goes through the same interface. Easy to add caching, logging, transactions.

## The collection-like interface

A repository should feel like an in-memory collection:
- `findById(id)` — like `map.get(key)`.
- `findAll()` — like `map.values()`.
- `save(entity)` — like `map.put(id, entity)`.
- `delete(id)` — like `map.remove(key)`.

The fact that there's a database behind it is an implementation detail.

## Generic vs specific repositories

### Generic
```java
public interface Repository<T, ID> {
    Optional<T> findById(ID id);
    List<T> findAll();
    void save(T entity);
    void delete(ID id);
}

public class InternRepository extends Repository<Intern, Long> { ... }
```

Pro: less duplication. Con: leaks the abstraction (callers can do anything).

### Specific
```java
public interface InternRepository {
    Optional<Intern> findById(long id);
    List<Intern> findPendingByDepartment(long deptId);
    void save(Intern intern);
    void markAccepted(long id, long chiefId);
}
```

Pro: documents the actual use cases. Con: more code per entity.

Fowler recommends **specific repositories** — they document what the app actually does. Generic repositories are a starting point but tend to become "anything goes" dumping grounds.

## The generic abstract base

A common pattern: a generic interface for the basics, plus a specific interface for custom queries:

```java
public interface CrudRepository<T, ID> {
    Optional<T> findById(ID id);
    List<T> findAll();
    void save(T entity);
    void delete(ID id);
}

public interface InternRepository extends CrudRepository<Intern, Long> {
    List<Intern> findPendingByDepartment(long deptId);
    List<Intern> findByFilters(InternSearchCriteria criteria);
}
```

## The project's (lack of) repository

```java
public class oracleConnector {
    public static void insertIntern(HashMap<String, Object> internData) { ... }
    public static List<Map<String, Object>> searchIntern(Map<String, Object> filters) { ... }
    public static void deleteIntern(int id, String name) { ... }
    public static void updateInter(Map<String, String> idNamePrimaryKey, Map<String, String> newUpdateParams) { ... }
    // ... 25 more methods
}
```

No interface. No type safety. No separation. Every controller calls `oracleConnector` directly.

## The fix

```java
public interface InternRepository {
    void save(Intern intern) throws SQLException;
    Optional<Intern> findById(long id) throws SQLException;
    List<Intern> findByFilters(InternSearchCriteria criteria) throws SQLException;
    void delete(long id) throws SQLException;
}

public class OracleInternRepository implements InternRepository {
    private final DataSource dataSource;
    public OracleInternRepository(DataSource dataSource) { this.dataSource = dataSource; }

    @Override
    public void save(Intern intern) throws SQLException {
        String sql = "INSERT INTO interns (name, age, email, ...) VALUES (?, ?, ?, ...)";
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, intern.getName());
            ps.setInt(2, intern.getAge());
            // ...
            ps.executeUpdate();
        }
    }
    // ...
}
```

Now:
- `InternService` depends on `InternRepository` (interface), not `OracleInternRepository` (concrete).
- In tests, inject `MockInternRepository` or `InMemoryInternRepository`.
- To migrate to PostgreSQL, write `PostgresInternRepository`. No service changes.

## Common pitfalls

- **Repository returning DTOs** — repositories should return domain objects, not DTOs. The mapping to DTOs happens in the service or controller.
- **Repository with business logic** — repositories do CRUD, not business rules. Put logic in the service or domain.
- **One repository per table** — repositories are per aggregate, not per table. If `Intern` and `InternAssignment` are one aggregate, one repository.
- **`findById` returning `null`** — return `Optional<T>`. See [[03 - Java Foundations/10 - Optional]].

## Further reading

- *Patterns of Enterprise Application Architecture* (Fowler), Repository pattern.
- *Domain-Driven Design* (Evans), Repositories.
