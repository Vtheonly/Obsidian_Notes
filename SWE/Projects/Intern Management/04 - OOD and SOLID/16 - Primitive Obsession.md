---
tags: [concept, code-smell, primitive-obsession]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/01 - Anemic Domain Model]]
  - [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]]
---

# Primitive Obsession

## What it is

Using primitive types (int, String, double) where a small object would be more appropriate. The code is "obsessed" with primitives, missing opportunities for type safety.

## Examples

```java
// Primitive obsession
public void setPhoneNumber(String phone) { ... }   // any string accepted
public void setAge(int age) { ... }                 // any int accepted
public void setEmail(String email) { ... }          // any string accepted
public void setStatus(String status) { ... }        // any string accepted

// Better
public void setPhoneNumber(PhoneNumber phone) { ... }  // validated at construction
public void setAge(Age age) { ... }                     // range-checked
public void setEmail(Email email) { ... }               // format-checked
public void setStatus(DecisionStatus status) { ... }    // enum, type-safe
```

## The project's primitive obsession

- `Map<String, Object>` — the ultimate primitive obsession. Any key, any value.
- `String status = "Pending"` — should be `DecisionStatus.PENDING`.
- `int roleId = 4` — should be `Role.ADMIN`.
- `String password_hash` — should be a `PasswordHash` value object.
- `String phone_number` — should be a `PhoneNumber` value object.

## Why it matters

- **No type safety** — `setEmail("not an email")` compiles.
- **No validation** — validation must be repeated everywhere the primitive is used.
- **No behavior** — a `PhoneNumber` could have `format()`, `getCountryCode()`, etc. A `String` has none of that.
- **Ubiquitous bugs** — typos like `params.get("full_naem")` return null silently.

## The fix: Value Objects

```java
public record Email(String value) {
    public Email {
        Objects.requireNonNull(value);
        if (!value.matches("^[^@]+@[^@]+\\.[^@]+$")) {
            throw new IllegalArgumentException("Invalid email: " + value);
        }
    }
}

public record PhoneNumber(String value) {
    public PhoneNumber {
        // validate E.164 format
    }
    public String getCountryCode() { ... }
    public String getNationalNumber() { ... }
}

public record Age(int value) {
    public Age {
        if (value < 16 || value > 100) {
            throw new IllegalArgumentException("Age must be 16-100");
        }
    }
}
```

Now:
```java
public void createIntern(Email email, PhoneNumber phone, Age age) { ... }
```

The compiler enforces the types. The constructor enforces the invariants. No validation needed at the call site.

## Common pitfalls

- **Over-engineering** — wrapping every primitive in a value object is overkill. Wrap primitives that have validation rules or meaningful behavior.
- **Anemic value objects** — a `Money` class that's just a `BigDecimal` wrapper with no behavior is pointless. Add `add(Money)`, `multiply(int)`, `format()`.
- **Forgetting equals/hashCode** — value objects should be compared by value, not reference. Java records handle this automatically.

## Project Connection

The project's `Map<String, Object>` is primitive obsession at scale. The fix: introduce value objects for `Email`, `PhoneNumber`, `Age`, etc. See [[03 - Java Foundations/07 - Java Records]].

## Further reading

- *Refactoring* (Fowler), "Primitive Obsession" smell.
- *Domain-Driven Design* (Evans), Value Objects.
