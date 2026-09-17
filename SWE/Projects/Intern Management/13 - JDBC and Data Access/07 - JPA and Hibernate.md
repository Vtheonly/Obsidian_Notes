---
tags: [concept, jpa, hibernate, orm]
type: concept
status: complete
related:
  - [[13 - JDBC and Data Access/14 - Spring JDBC (JdbcTemplate)]]
---

# JPA and Hibernate

## What it is

**JPA** (Jakarta Persistence API, formerly Java Persistence API) is the standard ORM (Object-Relational Mapping) specification for Java. **Hibernate** is the most popular JPA implementation.

## What ORM does

Maps Java objects to database tables:
```java
@Entity
@Table(name = "interns")
public class Intern {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long internId;

    private String name;
    private Integer age;
    private String email;

    @ManyToOne
    @JoinColumn(name = "theme_id")
    private Theme theme;

    // getters/setters
}
```

JPA generates the SQL:
```java
// Find by ID
Intern intern = entityManager.find(Intern.class, 123L);
// JPA executes: SELECT * FROM interns WHERE intern_id = ?

// Save
entityManager.persist(intern);
// JPA executes: INSERT INTO interns (name, age, ...) VALUES (?, ?, ...)

// Query
List<Intern> interns = entityManager.createQuery("SELECT i FROM Intern i WHERE i.age > :age", Intern.class)
    .setParameter("age", 18)
    .getResultList();
```

## Benefits

- **No SQL** — for simple CRUD, JPA generates the SQL.
- **Type safety** — JPQL is checked at compile time (with criteria API).
- **Lazy loading** — related entities are loaded on demand.
- **Caching** — first-level (session) and second-level (cross-session) caches.
- **Portability** — switch databases by changing the dialect.

## Drawbacks

- **N+1 problem** — lazy loading can cause N+1 queries if you're not careful.
- **Performance** — generated SQL may be suboptimal.
- **Complexity** — JPA has a steep learning curve.
- **Leaky abstraction** — you still need to understand SQL to debug.

## When to use JPA

- **Complex domain** — many entities, relationships, inheritance.
- **CRUD-heavy apps** — JPA shines for simple persistence.
- **Spring Boot** — JPA is the default.

## When NOT to use JPA

- **Simple apps** — JdbcTemplate is simpler.
- **Performance-critical** — hand-tuned SQL wins.
- **Reporting** — SQL queries are clearer.

## Project Connection

The project uses raw JDBC (via `oracleConnector`). For a portfolio-grade refactor, JPA is an option — but JdbcTemplate is simpler and gives more control. The reviews recommend JdbcTemplate + RowMapper over JPA for this project's scope.

## Common pitfalls

- **N+1** — `intern.getTheme().getName()` triggers a query per intern. Use `JOIN FETCH`.
- **Open Session in View** — anti-pattern where the session stays open during view rendering, hiding N+1.
- **Ignoring SQL** — if you don't understand the generated SQL, you can't optimize it.

## Further reading

- *Java Persistence with Hibernate* (Bauer, King, Gregory).
