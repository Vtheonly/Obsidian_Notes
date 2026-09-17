---
tags: [concept, principles, tell-dont-ask]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/13 - Law of Demeter]]
  - [[04 - OOD and SOLID/08 - Encapsulation]]
---

# Tell-Don't-Ask

## What it means

Tell objects what to do. Don't ask them for data and then decide what to do.

## Anti-pattern (Ask)

```java
if (intern.getStatus().equals("Pending")) {
    intern.setStatus("Accepted");
    intern.setDecidedBy(currentUser);
    intern.setDecidedAt(Instant.now());
    repository.save(intern);
}
```

The caller asks `intern` for its status, decides what to do, then mutates `intern`. The `Intern` class is a passive data bag.

## Better (Tell)

```java
intern.accept(currentUser);  // Intern decides if it can accept, mutates itself, returns events
repository.save(intern);
```

`Intern.accept()` checks the status, validates, mutates fields, and (if needed) returns a domain event. The caller doesn't know the rules — the `Intern` enforces them.

## Why it matters

- **Encapsulation** — the rules live with the data they govern.
- **Single source of truth** — the accept logic is in one place (`Intern.accept`), not scattered across controllers.
- **Testability** — you can unit-test `Intern.accept()` in isolation.

## When Ask is OK

- **Reading data for display** — `intern.getName()` is fine; the UI needs to display the name.
- **DTOs** — data transfer objects are meant to be data bags.
- **Functional style** — immutable data + pure functions is a valid alternative to OOP.

## Project Connection

The project is 100% "Ask" — every controller asks `oracleConnector` for `Map<String, Object>`, then asks the map for individual values, then asks `oracleConnector` to update.

The fix: introduce behavior-rich domain objects (`Intern.accept()`, `Intern.reject()`) and let them enforce their own rules.

See [[04 - OOD and SOLID/01 - Anemic Domain Model]] and [[04 - OOD and SOLID/08 - Encapsulation]].

## Further reading

- *Clean Code* (Martin), Chapter 6.
- "Tell, Don't Ask" (ThoughtWorks).
