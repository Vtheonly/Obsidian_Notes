---
tags: [concept, testing, tdd]
type: concept
status: complete
---

# TDD (Test-Driven Development)

## The cycle

1. **Red** — write a failing test for the behavior you want.
2. **Green** — write the minimum code to make the test pass.
3. **Refactor** — improve the code while keeping tests green.

Repeat.

## Why

- **Design feedback** — writing the test first forces you to think about the API.
- **Coverage** — every line of code is tested (because you wrote the test first).
- **Confidence** — refactoring is safe (tests catch regressions).
- **Documentation** — tests document how the code is supposed to behave.

## Example

```java
// Red — write the test
@Test
void shouldRejectUnderageIntern() {
    InternService service = new InternService(...);
    assertThrows(ValidationException.class, () ->
        service.create(new CreateInternCommand("Alice", 15, "alice@example.com"))
    );
}
// Test fails (InternService doesn't exist yet, or doesn't validate age).

// Green — make it pass
public Intern create(CreateInternCommand cmd) {
    if (cmd.age() < 16) throw new ValidationException("Age must be >= 16");
    // ...
}
// Test passes.

// Refactor — improve
// Extract the age validation to a separate validator, etc.
```

## When to TDD

- **New code** — TDD shines.
- **Bug fixes** — write a test that reproduces the bug, then fix the code.

## When NOT to TDD

- **Exploratory coding** — you don't know what you want yet.
- **UI layout** — visual work is hard to test first.
- **Spike** — throwaway code to learn an API.

## Project Connection

The project wasn't TDD'd (no tests). The refactored version can be — every new feature starts with a test.

## Further reading

- *Test-Driven Development: By Example* (Beck).
