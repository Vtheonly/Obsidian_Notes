---
tags: [concept, ood, encapsulation]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/24 - The Four Pillars of OOP]]
  - [[04 - OOD and SOLID/01 - Anemic Domain Model]]
---

# Encapsulation

## What it is

Encapsulation is the bundling of data with the methods that operate on it, and the hiding of internal state. The class exposes a **public API** (methods) and hides its **private implementation** (fields, helper methods).

## Why it matters

Without encapsulation:
- Any code can mutate any field, breaking invariants.
- Changing the internal representation breaks every caller.
- The class cannot enforce its contracts (e.g., "age must be 16–100").

With encapsulation:
- The class controls how its state changes (validation in setters or methods).
- The internal representation can change (e.g., `int age` → `LocalDate birthDate`) without breaking callers.
- Bugs are localized — if `age` is wrong, you look at `Intern.setAge()`, not every line that touches `intern.age`.

## Levels of access

| Modifier | Same class | Same package | Subclass | World |
|---|---|---|---|---|
| `public` | ✓ | ✓ | ✓ | ✓ |
| `protected` | ✓ | ✓ | ✓ | ✗ |
| (package-private, default) | ✓ | ✓ | ✗ | ✗ |
| `private` | ✓ | ✗ | ✗ | ✗ |

**Default to `private`.** Expose only what callers need. Use `package-private` for testing access within the same package. Use `public` only for the class's published API.

## Getters and setters (use carefully)

```java
public class Intern {
    private int age;
    public int getAge() { return age; }
    public void setAge(int age) {
        if (age < 16 || age > 100) throw new IllegalArgumentException();
        this.age = age;
    }
}
```

The setter validates. Callers cannot set an invalid age. This is encapsulation working.

**But** — if a class has getters and setters for every field, it's a "data bag" with no real encapsulation. The class enforces no invariants. This is the [[04 - OOD and SOLID/01 - Anemic Domain Model|Anemic Domain Model]] anti-pattern.

## Better: behavior-rich domain objects

```java
public class Intern {
    private DecisionStatus status;
    private final Long decidedBy;

    public void accept(User chief) {
        if (status != DecisionStatus.PENDING) {
            throw new IllegalStateException("Cannot accept: status is " + status);
        }
        this.status = DecisionStatus.ACCEPTED;
        this.decidedBy = chief.getId();
    }

    public void reject(User chief) {
        if (status != DecisionStatus.PENDING) { ... }
        this.status = DecisionStatus.REJECTED;
        this.decidedBy = chief.getId();
    }
}
```

The `Intern` enforces its own invariants: you can't accept an already-accepted intern, and only a `User` with chief privileges can call `accept` (the method enforces this). No setter for `status` — it can only change via `accept`/`reject`.

## Common pitfalls

- **Public fields** — no encapsulation at all.
- **Getter/setter for every field** — encapsulation in name only.
- **No validation in setters** — the field can be set to anything.
- **Mutable collections exposed** — `getList()` returns the internal list; callers can mutate it. Return an unmodifiable view.

## Project Connection

The project has no encapsulation:
- `oracleConnector.connection` is `static` (effectively public, since every method accesses it).
- `Map<String, Object>` — no validation, no invariants, no behavior.
- Controllers access `intern.get("name")`, `intern.get("age")` — raw data, no encapsulation.

The fix: replace `Map<String, Object>` with `Intern` records (immutable) or `Intern` classes (mutable but with behavior). See [[04 - OOD and SOLID/01 - Anemic Domain Model]].

## Further reading

- *Clean Code* (Martin), Chapter 6 (Objects and Data Structures).
- *Effective Java* (Bloch), Item 16 (minimize accessibility).
