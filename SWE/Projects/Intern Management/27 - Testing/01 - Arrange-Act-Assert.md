---
tags: [concept, testing, aaa]
type: concept
status: complete
---

# Arrange-Act-Assert (AAA)

## The pattern

Every test has three sections:

```java
@Test
void shouldCreateIntern() {
    // Arrange — set up the test
    InternService service = new InternService(mockRepo);
    CreateInternCommand cmd = new CreateInternCommand("Alice", 22, "alice@example.com");

    // Act — do the thing being tested
    Intern result = service.create(cmd);

    // Assert — verify the outcome
    assertNotNull(result.getId());
    assertEquals("Alice", result.getName());
    verify(mockRepo).save(any());
}
```

## Why

- **Readability** — the test structure is clear.
- **One assert per test** (ideally) — if the test fails, you know what failed.
- **Separation** — setup is distinct from action, distinct from verification.

## Given-When-Then (BDD style)

Equivalent, but in BDD language:
```java
@Test
void shouldCreateIntern() {
    // Given an intern service with a mock repository
    InternService service = new InternService(mockRepo);

    // When creating an intern named Alice
    Intern result = service.create(new CreateInternCommand("Alice", 22, "alice@example.com"));

    // Then the intern has an ID and was saved
    assertNotNull(result.getId());
    verify(mockRepo).save(any());
}
```

## Project Connection

The project has no tests. The fix: every test follows AAA.

## Further reading

- *Growing Object-Oriented Software, Guided by Tests* (Freeman & Pryce).
