---
tags: [concept, refactoring, enums]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/05 - Java Enums]]
related:
  - [[04 - OOD and SOLID/16 - Primitive Obsession]]
  - [[02 - CS Foundations/11 - State Machines]]
---

# Replace Magic Strings with Enums

## What it is

A **magic string** is a string literal used as a sentinel (e.g., `"Pending"`, `"Admin"`, `"ACCEPTED"`). Magic strings are bad because:
- **Typos not caught** — `"Pendin"` compiles, fails at runtime.
- **No autocomplete** — IDE can't suggest valid values.
- **No exhaustiveness checking** — switch statements can't verify all cases are handled.
- **Renaming is hard** — find-and-replace might miss some occurrences.

## The project's magic strings

```java
// Status
insertParameters.put("IS_ACCEPTED", "hold");  // violates CHECK constraint
// ...
case "Hold": // capitalized, doesn't match "hold"
case "Accepted":
case "Rejected":

// Roles
if (roleId == 4) { ... }  // admin
if (roleId == 5) { ... }  // chief

// Table names (in getIdByName switch)
case "intern":
case "theme":
case "department":
case "worker_user":
```

## The fix: enums

```java
public enum DecisionStatus {
    PENDING, ACCEPTED, REJECTED;

    public String dbValue() {
        return name().charAt(0) + name().substring(1).toLowerCase();
    }

    public static DecisionStatus fromDb(String dbValue) {
        return DecisionStatus.valueOf(dbValue.toUpperCase());
    }
}

public enum Role {
    USER(1), SECRETARY_BASIC(2), SECRETARY_ADVANCED(3), ADMIN(4), CHIEF(5);
    private final int id;
    Role(int id) { this.id = id; }
    public int getId() { return id; }
    public static Role fromId(int id) { ... }
}

public enum Entity {
    INTERN("intern", "intern_id"),
    THEME("theme", "theme_id"),
    DEPARTMENT("department", "department_id"),
    WORKER_USER("worker_user", "user_id");
    private final String tableName;
    private final String idColumn;
    // ...
}
```

Now:
```java
intern.status(DecisionStatus.PENDING);
if (user.getRole() == Role.ADMIN) { ... }
switch (entity) {
    case INTERN -> internRepo.findById(id);
    case THEME -> themeRepo.findById(id);
    // compile-time exhaustiveness check (with sealed switch)
}
```

## Why this is better

- **Typos caught at compile time** — `DecisionStatus.PENDIN` is a compile error.
- **IDE autocomplete** — type `DecisionStatus.` and the IDE shows the options.
- **Exhaustiveness** — switch over an enum can be checked for completeness.
- **Renaming** — refactor the enum constant, IDE updates all references.
- **Type safety** — `setStatus(DecisionStatus)` accepts only valid values.

## Common pitfalls

- **Storing enum names in the DB** — if you rename a constant, the DB has the old name. Store an explicit `id` or `dbValue` instead.
- **Forgetting to handle null** — `DecisionStatus.valueOf("Pendin")` throws. Use a safe `fromDb` method.
- **Mixing enums and strings** — `if (status.equals("Pending"))` when `status` is an enum. Use `status == DecisionStatus.PENDING`.

## Project Connection

The project's magic strings cause real bugs:
- `"hold"` violates the CHECK constraint (`'Accepted', 'Rejected', 'Pending'`).
- `"Hold"` in the display logic doesn't match `"hold"` in the insert.
- Role IDs 4 and 5 are scattered across multiple files with no single source of truth.

## Further reading

- *Refactoring* (Fowler), "Replace Magic Number with Symbolic Constant" and "Replace Type Code with Enum".
- *Effective Java* (Bloch), Item 34.
