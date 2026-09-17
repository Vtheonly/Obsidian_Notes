---
tags: [pattern, behavioral, chain-of-responsibility]
type: concept
status: complete
related:
  - [[06 - Design Patterns/07 - Decorator Pattern]]
  - [[23 - JavaFX UX and Polish/06 - Inline Form Validation]]
---

# Chain of Responsibility Pattern

> "Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it." — GoF

## What it is

A **chain** of handlers. Each handler decides to handle the request or pass it to the next handler.

```java
public interface Validator<T> {
    ValidationResult validate(T target);
    Validator<T> andThen(Validator<T> next);
}

public class EmailValidator implements Validator<Intern> {
    public ValidationResult validate(Intern intern) {
        if (intern.getEmail() == null || !intern.getEmail().contains("@")) {
            return ValidationResult.fail("Invalid email");
        }
        return ValidationResult.ok();
    }
    // ...
}

// Usage: chain validators
Validator<Intern> chain = new EmailValidator()
    .andThen(new AgeValidator())
    .andThen(new NameValidator())
    .andThen(new UniversityValidator());

ValidationResult result = chain.validate(intern);
```

## Why it exists

- **Decoupling** — the sender doesn't know which handler will process the request.
- **Flexibility** — add/remove/reorder handlers at runtime.
- **Single responsibility** — each handler does one thing.

## Servlet filters are a chain

```java
public class LoggingFilter implements Filter {
    public void doFilter(Request req, Response res, FilterChain chain) {
        log.info("Request: {}", req);
        chain.doFilter(req, res);  // pass to next filter
        log.info("Response: {}", res);
    }
}
```

## Project Connection

The project's input validation is scattered `if (value == "")` checks. The fix: a validation chain that runs all validators on an entity and returns a list of errors.

## Common pitfalls

- **Chain that always terminates at the same handler** — useless. The chain should vary based on input.
- **No way to short-circuit** — every handler runs even after a failure. Decide: stop on first failure, or collect all failures.

## Further reading

- *Design Patterns* (GoF), Chain of Responsibility.
