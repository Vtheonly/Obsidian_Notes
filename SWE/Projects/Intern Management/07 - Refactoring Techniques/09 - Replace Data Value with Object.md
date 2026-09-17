---
tags: [concept, refactoring, value-object]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/16 - Primitive Obsession]]
  - [[03 - Java Foundations/07 - Java Records]]
---

# Replace Data Value with Object

## What it is

**Replace Data Value with Object** turns a primitive (String, int, double) into a small object with behavior.

## When to use

- The primitive has validation rules (email, phone, ISBN).
- The primitive has associated behavior (formatting, parsing, comparison).
- The primitive appears in many places with duplicated validation.

## Example

```java
// Before: primitive obsession
public class Intern {
    private String email;
    public void setEmail(String email) {
        if (!email.contains("@")) throw new IllegalArgumentException();
        this.email = email;
    }
    public String getEmail() { return email; }
}
// Validation duplicated everywhere email is set

// After: value object
public record Email(String value) {
    public Email {
        Objects.requireNonNull(value);
        if (!value.matches("^[^@]+@[^@]+\\.[^@]+$")) {
            throw new IllegalArgumentException("Invalid email: " + value);
        }
    }
}

public class Intern {
    private Email email;
    public void setEmail(Email email) { this.email = email; }
    public Email getEmail() { return email; }
}
```

Now validation happens once (in `Email`'s constructor). The `Intern` doesn't need to validate.

## Value objects to introduce in the project

- `Email` — validate format.
- `PhoneNumber` — validate E.164, expose country code.
- `Age` — range 16-100.
- `Username` — length, charset.
- `PasswordHash` — opaque, can't be accidentally logged.
- `InternId`, `UserId`, `ThemeId` — typed IDs, prevent mixing.

## Common pitfalls

- **Anemic value objects** — a `Money` class that's just a `BigDecimal` wrapper with no behavior. Add `add`, `multiply`, `format`.
- **Forgetting equals/hashCode** — value objects should compare by value. Records handle this automatically.
- **Mutable value objects** — value objects should be immutable.

## Further reading

- *Refactoring* (Fowler), "Replace Data Value with Object".
- *Domain-Driven Design* (Evans), Value Objects.
