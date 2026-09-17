---
tags: [concept, java, records, immutability]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/01 - Anemic Domain Model]]
  - [[04 - OOD and SOLID/08 - Encapsulation]]
---

# Java Records

## What it is

Java 16+ introduced **records** — immutable data carriers with auto-generated constructors, accessors, `equals`, `hashCode`, and `toString`.

```java
public record Intern(
    Long internId,
    String name,
    Integer age,
    String email,
    String university,
    String phoneNumber,
    LocalDate startDate,
    DecisionStatus status,
    Long themeId
) {}
```

The compiler generates:
- A canonical constructor taking all fields.
- Accessor methods: `internId()`, `name()`, etc. (not `getInternId()`).
- `equals` and `hashCode` based on all fields.
- `toString` like `Intern[internId=1, name=Alice, ...]`.

## Why records exist

Before records, writing a simple data class required ~60 lines of boilerplate:
```java
public class Intern {
    private final Long internId;
    private final String name;
    // ... 7 more fields
    public Intern(Long internId, String name, ...) { ... }
    public Long getInternId() { return internId; }
    public String getName() { return name; }
    // ... 7 more getters
    @Override public boolean equals(Object o) { ... }
    @Override public int hashCode() { ... }
    @Override public String toString() { ... }
}
```

Records reduce this to ~10 lines.

## Compact constructors

If you need validation:
```java
public record Email(String value) {
    public Email {
        Objects.requireNonNull(value);
        if (!value.contains("@")) throw new IllegalArgumentException("Invalid email");
    }
}
```

The compact constructor runs before field assignment. Modify the parameters (e.g., normalize), not the fields.

## When to use records

- **DTOs** (Data Transfer Objects) — immutable data passed between layers.
- **Domain value objects** — `EmailAddress`, `Money`, `Coordinates`.
- **Method return types** — multiple values without a full class.
- **Configuration** — immutable settings.

## When NOT to use records

- **JPA entities** — JPA requires a no-arg constructor and mutable fields. Records don't work. (Use a class with `@Entity`.)
- **When you need inheritance** — records cannot extend other classes (they implicitly extend `java.lang.Record`). They can implement interfaces.
- **When you need mutable fields** — records are immutable by design.

## Common pitfalls

- Forgetting that accessors are `name()` not `getName()` — breaks JavaFX `PropertyValueFactory` which expects `getName()`. Workaround: use `TableColumn.cellValueFactory` with a lambda, or add `getName()` to a wrapper class.
- Trying to use records as JPA entities — doesn't work. Use a class.
- Modifying fields in the compact constructor — modify the parameters, not the fields (which haven't been assigned yet).

## Project Connection

The project has no domain classes at all — everything is `Map<String, Object>`. Replacing with records:

```java
public record Intern(
    Long internId,
    String name,
    Integer age,
    String email,
    String university,
    String phoneNumber,
    LocalDate startDate,
    DecisionStatus status,
    Long themeId
) {}

public enum DecisionStatus { PENDING, ACCEPTED, REJECTED }
```

This:
- Gives compile-time type safety (typos caught at compile time).
- Makes the code self-documenting (the `Intern` record documents the intern entity).
- Enables IDE autocomplete.
- Makes refactoring safe (rename a field, IDE updates all references).

See [[04 - OOD and SOLID/01 - Anemic Domain Model]].

## Further reading

- JEP 395 (Records).
- *Modern Java in Action* (Urma, Fusco, Mycroft).
