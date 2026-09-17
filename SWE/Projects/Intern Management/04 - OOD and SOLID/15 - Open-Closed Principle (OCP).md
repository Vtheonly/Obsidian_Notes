---
tags: [concept, solid, ocp]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/19 - Single Responsibility Principle (SRP)]]
  - [[06 - Design Patterns/17 - Strategy Pattern]]
  - [[06 - Design Patterns/18 - Template Method Pattern]]
---

# Open-Closed Principle (OCP)

> "Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification." — Bertrand Meyer, 1988

## What it means

You should be able to **extend** a class's behavior (add new functionality) without **modifying** its source code.

## The project's OCP violation

```java
public static int getIdByName(String tableName, String name) {
    switch (tableName) {
        case "intern": // ...
        case "theme": // ...
        case "department": // ...
        case "worker_user": // ...
        case "worker_user_super": // ...
        case "worker_user_user": // ...
        case "responsible": // ...
        default: throw new IllegalArgumentException("Unknown table: " + tableName);
    }
}
```

Adding a new entity (e.g., `InternshipApplication`) requires editing this method to add a new `case`. This is **closed for extension** — you must modify existing code to add new functionality.

## The fix: polymorphism

```java
public interface Repository<T, ID> {
    Optional<T> findByName(String name);
}

// Each entity has its own repository:
public class InternRepository implements Repository<Intern, Long> { ... }
public class ThemeRepository implements Repository<Theme, Long> { ... }
// Adding a new entity: write a new class. No modification of existing code.
```

The dispatch is now polymorphic — the caller holds a `Repository<T, ID>` reference, and the right method is called based on the actual type.

## OCP via Strategy Pattern

```java
public interface PasswordEncoder {
    String encode(String raw);
    boolean matches(String raw, String encoded);
}

public class Argon2PasswordEncoder implements PasswordEncoder { ... }
public class BCryptPasswordEncoder implements PasswordEncoder { ... }
// Adding a new encoder: write a new class. No modification of existing code.
```

## OCP via Template Method

```java
public abstract class AbstractJdbcRepository<T, ID> {
    public Optional<T> findById(ID id) {
        // shared algorithm: prepare, execute, map
        try (PreparedStatement ps = conn.prepareStatement("SELECT * FROM " + tableName() + " WHERE " + idColumn() + " = ?")) {
            ps.setObject(1, id);
            ResultSet rs = ps.executeQuery();
            return rs.next() ? Optional.of(mapRow(rs)) : Optional.empty();
        }
    }
    protected abstract String tableName();
    protected abstract String idColumn();
    protected abstract T mapRow(ResultSet rs);
}
```

The base class is **closed** (you don't modify it). Each subclass **extends** it by providing the abstract methods.

## Common pitfalls

- **Switch statements on type** — almost always an OCP violation. Replace with polymorphism.
- **If/else chains on type strings** — same as switch. Replace with a `Map<String, Strategy>`.
- **Abstract classes with too many abstract methods** — subclasses have to implement too much. Split into smaller interfaces (ISP).

## Project Connection

The project's `getIdByName` switch and the 4 copy-pasted CRUD methods are OCP violations. Adding a 5th entity requires editing `oracleConnector`.

### Fix

Replace with a `Repository<T, ID>` interface + `AbstractJdbcRepository<T, ID>` template + per-entity subclasses. See [[06 - Design Patterns/18 - Template Method Pattern]] and [[05 - Software Architecture/14 - Repository Pattern]].

## Further reading

- *Clean Architecture* (Martin), Chapter 8 (OCP).
- *Object-Oriented Software Construction* (Meyer).
