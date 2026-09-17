---
tags: [pattern, behavioral, strategy]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/15 - Open-Closed Principle (OCP)]]
  - [[06 - Design Patterns/16 - State Pattern]]
---

# Strategy Pattern

> "Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it." — GoF

## What it is

A **strategy** is an interface with multiple implementations. The client holds a reference to the interface and calls its method — the actual implementation is decided at runtime.

```java
public interface PasswordEncoder {
    String encode(String raw);
    boolean matches(String raw, String encoded);
}

public class Argon2PasswordEncoder implements PasswordEncoder {
    public String encode(String raw) { /* Argon2id hash */ }
    public boolean matches(String raw, String encoded) { /* Argon2id verify */ }
}

public class BCryptPasswordEncoder implements PasswordEncoder {
    public String encode(String raw) { /* BCrypt hash */ }
    public boolean matches(String raw, String encoded) { /* BCrypt verify */ }
}

// Usage
PasswordEncoder encoder = new Argon2PasswordEncoder();  // or BCrypt, decided at config time
String hash = encoder.encode("password123");
```

The caller doesn't know (or care) whether it's Argon2 or BCrypt.

## Why it exists

- **OCP** — add a new strategy (e.g., `SCryptPasswordEncoder`) without modifying existing code.
- **Testability** — inject a `NoOpPasswordEncoder` in tests (don't actually hash).
- **Configuration** — switch strategies at deploy time.
- **Eliminate conditionals** — instead of `if (algorithm.equals("argon2")) { ... } else if (algorithm.equals("bcrypt")) { ... }`, use polymorphism.

## Strategy vs State

- **Strategy** — the client chooses the algorithm. "I want to hash with Argon2."
- **State** — the object's state determines behavior. "The intern is PENDING, so accept() works."

Same structure (interface + implementations), different intent.

## Strategy vs Template Method

- **Strategy** — composition. The client holds a strategy.
- **Template Method** — inheritance. The base class defines the algorithm; subclasses override steps.

## Project Connection

The project's `toolkit.hashIt` is a static method — not a strategy. Can't swap, can't mock. The fix: `PasswordEncoder` interface with `Argon2PasswordEncoder` implementation.

Other strategies the project should adopt:
- `ReportExporter` — PDF, CSV, XLSX.
- `InternFilter` — different filter strategies.
- `EmailSender` — SMTP, SendGrid, mock.

## Common pitfalls

- **One-implementation strategy** — if there's only one implementation, the strategy might be YAGNI. But for architectural seams (PasswordEncoder, EmailSender), the interface is worth it.
- **Strategy with too many methods** — if the interface has 10 methods, it's probably ISP violation. Split.

## Further reading

- *Design Patterns* (GoF), Strategy.
