---
tags: [concept, java, enums]
type: concept
status: complete
related:
  - [[02 - CS Foundations/11 - State Machines]]
  - [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]]
---

# Java Enums

## What it is

An `enum` is a type-safe enumeration — a fixed set of named constants. Java enums are full classes (unlike C/C++ enums which are just integers).

```java
public enum DecisionStatus {
    PENDING,
    ACCEPTED,
    REJECTED
}
```

## Why enums exist

Before enums, developers used `int` constants:
```java
public static final int STATUS_PENDING = 1;
public static final int STATUS_ACCEPTED = 2;
public static final int STATUS_REJECTED = 3;

public void setStatus(int status) { ... }  // accepts ANY int, no type safety
setStatus(99);  // compiles, breaks at runtime
```

Enums give compile-time safety:
```java
public void setStatus(DecisionStatus status) { ... }
setStatus(DecisionStatus.PENDING);  // OK
setStatus(99);                       // compile error
setStatus("Pending");                // compile error
```

## Enums as classes

Java enums can have fields, methods, and constructors:
```java
public enum Role {
    USER(1, "User"),
    SECRETARY_BASIC(2, "Secretary (Basic)"),
    SECRETARY_ADVANCED(3, "Secretary (Advanced)"),
    ADMIN(4, "Administrator"),
    CHIEF(5, "Chief of Department");

    private final int id;
    private final String displayName;

    Role(int id, String displayName) {
        this.id = id;
        this.displayName = displayName;
    }

    public int getId() { return id; }
    public String getDisplayName() { return displayName; }

    public static Role fromId(int id) {
        for (Role r : values()) {
            if (r.id == id) return r;
        }
        throw new IllegalArgumentException("Unknown role ID: " + id);
    }
}
```

## Enums with abstract methods (State Pattern in miniature)

```java
public enum Operation {
    PLUS { public int apply(int a, int b) { return a + b; } },
    MINUS { public int apply(int a, int b) { return a - b; } },
    TIMES { public int apply(int a, int b) { return a * b; } };

    public abstract int apply(int a, int b);
}
```

Each constant provides its own implementation. This is the State Pattern without the boilerplate.

## EnumSet and EnumMap

`EnumSet` and `EnumMap` are highly optimized collections for enums (bitset-backed):
```java
EnumSet<Role> adminRoles = EnumSet.of(Role.ADMIN, Role.CHIEF);
EnumMap<Role, String> descriptions = new EnumMap<>(Role.class);
```

## Common pitfalls

- Using `int` constants instead of enums — no type safety.
- Using string literals instead of enums — typos not caught at compile time.
- Forgetting that `enum` values are singletons — `==` works, but use `.equals()` for consistency.
- Serializing enums by name (default) — if you rename a constant, deserialization breaks. Consider serializing by an explicit ID.

## Project Connection

The project uses **magic numbers** for roles:
```java
public static boolean isAdmin(String username, String password) {
    // ... returns roleId == 4
}
public static boolean isChief(String username, String password) {
    // ... returns roleId == 5
}
```

And **magic strings** for status:
```java
insertParameters.put("IS_ACCEPTED", "hold");  // violates CHECK constraint
```

### Fix

```java
public enum Role {
    USER(1), SECRETARY_BASIC(2), SECRETARY_ADVANCED(3), ADMIN(4), CHIEF(5);
    private final int id;
    Role(int id) { this.id = id; }
    public int getId() { return id; }
    public static Role fromId(int id) { ... }
}

public enum DecisionStatus {
    PENDING, ACCEPTED, REJECTED;
    public String dbValue() { return name().charAt(0) + name().substring(1).toLowerCase(); }
}
```

Then:
```java
if (user.getRole() == Role.ADMIN) { ... }
intern = new Intern(..., DecisionStatus.PENDING, ...);
```

See [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]].

## Further reading

- *Effective Java* (Bloch), Item 34 (use enums instead of int constants).
