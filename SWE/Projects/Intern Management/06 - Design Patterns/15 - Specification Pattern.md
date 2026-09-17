---
tags: [pattern, enterprise, specification]
type: concept
status: complete
related:
  - [[05 - Software Architecture/14 - Repository Pattern]]
  - [[06 - Design Patterns/17 - Strategy Pattern]]
---

# Specification Pattern

> A way to encapsulate business rules as composable predicates. — Eric Evans, DDD

## What it is

A **specification** is a boolean predicate that can be combined with other specifications using AND, OR, NOT.

```java
public interface Specification<T> {
    boolean isSatisfiedBy(T candidate);
    default Specification<T> and(Specification<T> other) {
        return c -> this.isSatisfiedBy(c) && other.isSatisfiedBy(c);
    }
    default Specification<T> or(Specification<T> other) {
        return c -> this.isSatisfiedBy(c) || other.isSatisfiedBy(c);
    }
    default Specification<T> not() {
        return c -> !this.isSatisfiedBy(c);
    }
}

// Usage
Specification<Intern> pending = intern -> intern.getStatus() == DecisionStatus.PENDING;
Specification<Intern> inDept = intern -> intern.getDepartmentId() == 5;
Specification<Intern> pendingInDept = pending.and(inDept);

List<Intern> results = allInterns.stream()
    .filter(pendingInDept::isSatisfiedBy)
    .collect(Collectors.toList());
```

## Why it exists

- **Composable** — combine simple rules into complex ones.
- **Reusable** — a specification can be used in memory, in SQL (via translation), or for validation.
- **Testable** — each specification is a small, testable unit.

## Project Connection

The project's search uses `Map<String, Object>` filters — no composition, no type safety. The fix: `InternSearchCriteria` as a specification, composable.

## Common pitfalls

- **Specifications that don't translate to SQL** — if you can't translate the spec to SQL, you're loading everything into memory. Design specs to be SQL-translatable.
- **Too many specifications** — one per query is overkill. Group related queries.

## Further reading

- *Domain-Driven Design* (Evans), Specifications.
- *Specifications* (Mark Seemann, blog).
