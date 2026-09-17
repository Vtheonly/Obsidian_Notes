---
tags: [pattern, creational, builder]
type: concept
status: complete
related:
  - [[06 - Design Patterns/08 - Factory Pattern]]
---

# Builder Pattern

## What it is

> "Separate the construction of a complex object from its representation so that the same construction process can create various representations." — GoF

A **builder** constructs a complex object step by step. Instead of a constructor with 10 parameters, you call methods that set each field, then call `build()` to get the object.

```java
InternSearchCriteria criteria = InternSearchCriteria.builder()
    .name("Alice")
    .university("MIT")
    .status(DecisionStatus.PENDING)
    .themeId(5L)
    .build();
```

## Why it exists

- **Readable** — `builder().name("Alice").age(22)` is clearer than `new Intern(null, "Alice", 22, null, null, ...)`.
- **Optional fields** — you only set what you need. No telescope constructor.
- **Immutability** — the built object can be immutable; the builder is mutable.
- **Validation** — the `build()` method validates all fields before constructing.

## The "telescope constructor" anti-pattern

```java
public Intern(Long id, String name) { this(id, name, null); }
public Intern(Long id, String name, Integer age) { this(id, name, age, null); }
public Intern(Long id, String name, Integer age, String email) { this(id, name, age, email, null); }
public Intern(Long id, String name, Integer age, String email, String university) { ... }
// ... 7 more overloads
```

Each new field adds another overload. The constructor list grows like a telescope. The builder pattern fixes this.

## Implementation

```java
public final class InternSearchCriteria {
    private final String name;
    private final String university;
    private final DecisionStatus status;
    private final Long themeId;

    private InternSearchCriteria(Builder b) {
        this.name = b.name;
        this.university = b.university;
        this.status = b.status;
        this.themeId = b.themeId;
    }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private String name;
        private String university;
        private DecisionStatus status;
        private Long themeId;

        public Builder name(String name) { this.name = name; return this; }
        public Builder university(String u) { this.university = u; return this; }
        public Builder status(DecisionStatus s) { this.status = s; return this; }
        public Builder themeId(Long id) { this.themeId = id; return this; }

        public InternSearchCriteria build() {
            // validate
            return new InternSearchCriteria(this);
        }
    }
}
```

## Java records + builder

For immutable data, records + a builder is common:

```java
public record InternSearchCriteria(String name, String university, DecisionStatus status, Long themeId) {
    public static Builder builder() { return new Builder(); }

    public static class Builder {
        // ... same as above
        public InternSearchCriteria build() { return new InternSearchCriteria(name, university, status, themeId); }
    }
}
```

Or use Lombok's `@Builder` annotation to generate it automatically.

## When to use

- Objects with many optional fields (> 4).
- Objects that are immutable.
- Construction that requires validation across multiple fields.

## When NOT to use

- Objects with 2-3 required fields — use a constructor.
- Mutable objects — use setters.

## Project Connection

The project builds `HashMap<String, Object>` for search filters — no type safety, no validation. The fix: `InternSearchCriteria` with a builder.

## Further reading

- *Effective Java* (Bloch), Item 2 (builder).
- *Design Patterns* (GoF), Builder.
