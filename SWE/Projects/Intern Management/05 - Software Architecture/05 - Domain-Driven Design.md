---
tags: [concept, architecture, ddd]
type: concept
status: complete
related:
  - [[05 - Software Architecture/02 - Clean Architecture (Uncle Bob)]]
  - [[04 - OOD and SOLID/01 - Anemic Domain Model]]
  - [[04 - OOD and SOLID/16 - Primitive Obsession]]
---

# Domain-Driven Design (DDD)

> "Domain-Driven Design is an approach to software development that centers the development on programming a rich domain model that expresses the true nature of the business." — Eric Evans, *Domain-Driven Design*, 2003

## What it is

DDD (Evans, 2003) is a methodology for designing complex software by deeply modeling the business domain. It's not an architecture pattern — it's a way of thinking about the domain that *informs* the architecture.

## Strategic design

### Ubiquitous Language
The same vocabulary used by domain experts is used in code. If the business says "internship application," the code has an `InternshipApplication` class. If the business says "chief of department," the code has a `ChiefOfDepartment` role. No translation between business and code.

### Bounded Contexts
A large system is divided into contexts, each with its own model. The `User` in the HR context is different from the `User` in the Auth context. They may share an ID but have different fields and behavior.

```
[ HR Context ]  ←→  [ Auth Context ]  ←→  [ Notifications Context ]
   User              User                  Recipient
   Department        Role                  Channel
   Manager
```

### Context Mapping
How contexts relate: shared kernel, customer/supplier, conformist, anti-corruption layer, etc.

## Tactical design (building blocks)

### Entity
An object defined by its identity (not its attributes). Two `Intern`s with the same `id` are the same intern, even if their names differ.

```java
public class Intern {  // Entity
    private final InternId id;  // identity
    private String name;
    // ...
}
```

### Value Object
An object defined by its attributes. Two `Email("alice@example.com")` are the same email. Immutable.

```java
public record Email(String value) {  // Value Object
    public Email {
        if (!value.contains("@")) throw new IllegalArgumentException();
    }
}
```

### Aggregate
A cluster of entities and value objects treated as a single unit. The `Aggregate Root` is the only entry point — external code can only hold references to the root, not to internal entities.

```java
public class Intern extends AggregateRoot<InternId> {  // Aggregate root
    private List<Assignment> assignments;  // internal entities, accessed only via Intern
    public void addAssignment(Assignment a) { ... }  // the only way to add
}
```

### Repository
An interface for retrieving and saving aggregates. Hides persistence details.

```java
public interface InternRepository {
    Optional<Intern> findById(InternId id);
    void save(Intern intern);
}
```

### Domain Service
A stateless operation that doesn't fit on any entity or value object.

```java
public class InternAssignmentService {  // Domain Service
    public void assignToInternship(Intern intern, Theme theme) { ... }
}
```

### Domain Event
Something that happened in the domain. Other parts of the system can react.

```java
public record InternAccepted(InternId id, UserId chiefId, Instant at) {}
```

## Why DDD matters

- **Shared understanding** — developers and domain experts speak the same language.
- **Rich domain model** — behavior lives on the objects that own the data.
- **Clear boundaries** — bounded contexts prevent "one giant model" syndrome.
- **Testable** — domain logic is isolated from infrastructure.

## When to use DDD

- The domain is complex (lots of business rules).
- The team has access to domain experts.
- The system will be maintained for years.

**Don't use DDD for:**
- CRUD apps with no business rules.
- Internal tools with simple workflows.
- Prototypes or throwaways.

## The project's (lack of) DDD

The project has no domain model — just `Map<String, Object>`. There's no `Intern` entity, no `Email` value object, no `InternRepository` interface, no `InternAccepted` event. The fix introduces all of these, but for a CRUD app, full DDD is overkill. A pragmatic approach:
- Use entities (records) and value objects (records with validation).
- Use repositories (interfaces).
- Skip aggregates, domain events, bounded contexts (until the domain grows).

## Common pitfalls

- **DDD cargo-cult** — aggregates, value objects, domain events everywhere, for a CRUD app. Overkill.
- **Anemic domain model** — entities with only getters/setters. DDD requires rich domain objects.
- **Ubiquitous language violations** — `WorkerUser` in code, "employee" in conversation. Pick one.
- **One giant context** — everything in one bounded context. Split when contexts emerge.

## Further reading

- *Domain-Driven Design* (Evans, 2003) — the blue book.
- *Implementing Domain-Driven Design* (Vaughn Vernon, 2013) — the red book.
- *Domain-Driven Design Distilled* (Vernon, 2016) — the short version.
