---
tags: [concept, anti-pattern, anemic-model]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/08 - Encapsulation]]
  - [[04 - OOD and SOLID/23 - Tell-Dont-Ask]]
  - [[05 - Software Architecture/10 - Layered Architecture]]
---

# Anemic Domain Model

> "The basic symptom of an Anemic Domain Model is that at first blush it looks like the real thing. There are objects, many named after the nouns in the domain space, and these objects are connected with the rich relationships and structure that true domain models have. The catch comes when you look at the behavior, and you realize that there is hardly any behavior on these objects, making them little more than bags of getters and setters. Indeed often these models come with design rules that say that you are not to put any domain logic in the domain objects. ... The horror comes when you realize that all this logic is scattered across many service objects." — Martin Fowler

## What it is

An **anemic domain model** has domain objects (e.g., `Intern`, `User`) with fields and getters/setters, but **no behavior**. The business logic lives in services that operate on the data bags.

## The project's anemia

The project doesn't even have anemic domain objects — it has **no domain objects at all**. Everything is `Map<String, Object>`:

```java
HashMap<String, Object> internData = new HashMap<>();
internData.put("name", "Alice");
internData.put("age", 22);
// ...
oracleConnector.insertIntern(internData);
```

This is anemia taken to its extreme. There's no `Intern` class at all — just a map of strings to objects.

## Why it's bad

- **No type safety** — `internData.get("naem")` returns null silently (typo).
- **No validation** — the map accepts any garbage.
- **No behavior** — the `Intern` cannot answer `isPending()` or `accept()`. The caller has to know the string `"Pending"` means pending.
- **No refactoring safety** — rename a field, and the string keys break at runtime.
- **No IDE support** — no autocomplete, no "find usages."

## The fix: rich domain objects

```java
public final class Intern {
    private final long id;
    private String name;
    private int age;
    private String email;
    private DecisionStatus status;
    private User decidedBy;
    private Instant decidedAt;
    // ... other fields

    // Constructor, getters (no setters for derived state)

    public void accept(User chief) {
        if (status != DecisionStatus.PENDING) {
            throw new IllegalStateException("Cannot accept: status is " + status);
        }
        this.status = DecisionStatus.ACCEPTED;
        this.decidedBy = chief;
        this.decidedAt = Instant.now();
    }

    public void reject(User chief) {
        if (status != DecisionStatus.PENDING) {
            throw new IllegalStateException("Cannot reject: status is " + status);
        }
        this.status = DecisionStatus.REJECTED;
        this.decidedBy = chief;
        this.decidedAt = Instant.now();
    }

    public boolean isPending() { return status == DecisionStatus.PENDING; }
}
```

The `Intern` enforces its own invariants: you can't accept an already-accepted intern. The caller just calls `intern.accept(chief)` — no need to know the rules.

## When anemia is OK

- **DTOs** (Data Transfer Objects) — objects passed between layers for serialization. No behavior, just data.
- **Database entities** (JPA `@Entity`) — sometimes anemic is acceptable; the service layer holds the logic. (Fowler disagrees, but it's a common pattern.)
- **View models** — objects for UI display. Anemia is fine.

The key question: is the anemia **at the domain layer**? If yes, that's the anti-pattern. If it's at the DTO/entity layer, it may be acceptable.

## Common pitfalls

- **"Anemic" used as a blanket insult** — sometimes anemia is the right choice (DTOs, view models). Don't over-correct.
- **Rich domain model with no service layer** — sometimes you still need services for cross-entity coordination. Don't try to put everything in domain objects.
- **DDD cargo-cult** — aggregates, value objects, repositories everywhere. Use DDD when the domain is complex enough to justify it.

## Project Connection

The project has no domain objects at all — just `Map<String, Object>`. The fix: introduce `Intern`, `WorkerUser`, `Theme`, `Department`, `Role` (enum), `DecisionStatus` (enum) with behavior. See [[03 - Java Foundations/07 - Java Records]] and [[03 - Java Foundations/05 - Java Enums]].

## Further reading

- *Domain-Driven Design* (Evans).
- Fowler, "Anemic Domain Model" (martinfowler.com).
