---
tags: [pattern, creational, factory]
type: concept
status: complete
related:
  - [[06 - Design Patterns/01 - Abstract Factory Pattern]]
  - [[06 - Design Patterns/03 - Builder Pattern]]
---

# Factory Pattern (Factory Method)

## What it is

> "Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses." — GoF

A **factory method** is a method that creates objects. Instead of calling `new` directly, you call a method that returns the object. This decouples the caller from the concrete class.

```java
// Without factory
Connection conn = new OracleConnection(url, user, pass);  // hard dependency on OracleConnection

// With factory
Connection conn = connectionFactory.create();  // factory decides the implementation
```

## Why it exists

- **Decoupling** — the caller doesn't know the concrete class.
- **Testability** — inject a mock factory that returns mock objects.
- **Encapsulation** — complex construction logic lives in one place.
- **Naming** — `ConnectionFactory.create()` is more readable than `new HikariDataSource(config)`.

## Static factory methods (Effective Java Item 1)

Not all factories are the GoF pattern. A **static factory method** is a static method that returns an instance:

```java
public class List {
    public static <E> List<E> of(E... elements) { ... }  // static factory
    public static <E> List<E> copyOf(Collection<E> coll) { ... }
}

List<String> names = List.of("Alice", "Bob");  // returns ImmutableCollections.ListN
```

Pros over constructors:
- Has a name (`List.of` vs `new ArrayList`).
- Can return a subtype (immutable list, synchronized list).
- Can cache instances (`Boolean.valueOf(true)` returns a cached `Boolean.TRUE`).

## Factory examples in the project's fix

### ConnectionFactory
```java
public interface ConnectionFactory {
    Connection getConnection() throws SQLException;
}

public class HikariConnectionFactory implements ConnectionFactory {
    private final HikariDataSource dataSource;
    public HikariConnectionFactory(HikariDataSource dataSource) { ... }
    @Override public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
}
```

### AlertFactory
```java
public class AlertFactory {
    public static Alert error(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        return alert;
    }
    public static Alert confirmation(String title, String message) { ... }
    public static Alert information(String title, String message) { ... }
}
```

## When to use

- When the construction logic is non-trivial (validation, configuration, caching).
- When the caller shouldn't know the concrete class.
- When you want to return different subtypes based on input.

## When NOT to use

- When `new` is simpler. `new Intern(name, age)` doesn't need a factory.
- When there's only one implementation and construction is trivial.

## Common pitfalls

- **Factory for everything** — over-engineering. Use factories when they add value.
- **Factory that just delegates to `new`** — useless. The factory must add something (validation, caching, polymorphism).
- **God factory** — one factory that creates everything. Split per concern.

## Further reading

- *Effective Java* (Bloch), Item 1 (static factory methods).
- *Design Patterns* (GoF), Factory Method.
