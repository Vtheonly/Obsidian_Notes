---
tags: [concept, architecture, clean-architecture]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[05 - Software Architecture/08 - Hexagonal Architecture (Ports and Adapters)]]
  - [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]]
---

# Clean Architecture (Uncle Bob)

> "The dependency rule: source code dependencies must point only inward, toward higher-level policies." — Robert C. Martin, *Clean Architecture*

## What it is

Clean Architecture (Robert C. Martin, 2017) organizes a system into concentric circles:

```
┌─────────────────────────────────────┐
│  Frameworks & Drivers               │  Web, DB, UI frameworks
│  ┌─────────────────────────────┐    │
│  │  Interface Adapters         │  │  Controllers, Presenters, Gateways
│  │  ┌─────────────────────┐    │  │
│  │  │  Use Cases          │    │  │  Application business rules
│  │  │  ┌─────────────┐    │    │  │
│  │  │  │  Entities    │    │    │  │  Enterprise business rules
│  │  │  └─────────────┘    │    │  │
│  │  └─────────────────────┘    │  │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## The Dependency Rule

**Dependencies point inward.** The inner circles are policies (what the system does); the outer circles are mechanisms (how it does it). The inner circles cannot know anything about the outer circles.

- **Entities** — domain objects with enterprise-wide rules. Pure Java, no framework.
- **Use Cases** — application-specific business rules. Orchestrates entities. Pure Java.
- **Interface Adapters** — controllers, presenters, gateways. Translate data between use cases and external interfaces.
- **Frameworks & Drivers** — the outermost layer. Spring, JavaFX, JDBC, Oracle. This is where the "details" live.

## Why it's better than naive layering

In a naive 3-layer architecture:
- The service layer depends on the repository (interface), good.
- The repository depends on JDBC (a framework), unavoidable.
- But the repository *interface* lives in the data access layer, so the service depends on data access.

In Clean Architecture:
- The repository *interface* lives in the use case layer.
- The repository *implementation* lives in the frameworks layer.
- The use case depends on the interface (inner → inner), not the implementation (which is outer).

This inverts the dependency: the outer layer depends on the inner, never the reverse.

## The Dependency Inversion Principle in action

```java
// Use case layer (inner)
public interface InternRepository {
    Optional<Intern> findById(long id);
    void save(Intern intern);
}

public class AcceptInternUseCase {
    private final InternRepository repository;
    public AcceptInternUseCase(InternRepository repository) { ... }
    public void execute(long id, User chief) { ... }
}

// Frameworks layer (outer)
public class OracleInternRepository implements InternRepository {
    // Oracle JDBC implementation
}
```

The use case (inner) defines the interface. The repository (outer) implements it. The dependency direction is outer → inner, satisfying the dependency rule.

## Project Connection

The project is the opposite of Clean Architecture. `oracleConnector` (outer — DB access) is called directly by controllers (outer — UI). There are no use cases, no entities, no interfaces. The dependency direction is sideways (controller ↔ DAO) instead of inward.

## When Clean Architecture is overkill

For a CRUD app with no complex business rules, a simpler 3-layer architecture is sufficient. Clean Architecture shines when:
- The domain is complex (lots of business rules).
- You want to swap the UI, DB, or framework.
- You want to test the domain in complete isolation.

## Common pitfalls

- **Cargo-culting the circles** — drawing the diagram without understanding the dependency rule.
- **Putting entities in the outer layer** — JPA `@Entity` annotations leak the framework into the domain. Use plain POJOs or records in the entity layer, and a separate JPA mapping.
- **Too many layers for a simple app** — 4 circles for a CRUD app is overkill.

## Further reading

- *Clean Architecture* (Martin), the book.
- blog.cleancoder.com — Uncle Bob's blog.
