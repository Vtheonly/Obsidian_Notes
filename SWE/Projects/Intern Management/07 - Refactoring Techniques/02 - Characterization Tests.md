---
tags: [concept, refactoring, testing, characterization]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
  - [[27 - Testing/00 - MOC - Testing]]
---

# Characterization Tests

> "A characterization test is a test that characterizes the actual behavior of a piece of software. The test does not define what the behavior should be; it records what the behavior is." — Michael Feathers, *Working Effectively with Legacy Code*

## What it is

A **characterization test** (also called a "golden master test" or "approval test") captures the *current* behavior of code, even if that behavior is buggy. The test passes for the current code; if you refactor and break something, the test fails.

## When to use

- Before refactoring legacy code with no tests.
- When you don't fully understand what the code does.
- When the code has known bugs that you can't fix yet (the test documents the bug).

## The cycle

1. Run the code with a representative input.
2. Capture the output (the "golden master").
3. Write a test that asserts the code produces this output.
4. Refactor.
5. Run the test. If it passes, the refactoring preserved behavior. If it fails, you changed behavior.

## Example

```java
@Test
void characterizeParseText() {
    // Capture current behavior of toolkit.parseText
    String input = "Name: Alice,\nAge: 22,\nEmail: alice@example.com";
    Map<String, String> result = toolkit.parseText(input);

    // Assert the current (possibly buggy) output
    assertEquals("Alice", result.get("Name"));
    assertEquals("22", result.get("Age"));
    assertEquals("alice@example.com", result.get("Email"));
}
```

If `parseText` has a bug (e.g., it strips trailing commas incorrectly), the test documents the bug. After refactoring, the test should still pass — the behavior is preserved. *Then* you can write a separate test for the *correct* behavior and fix the bug.

## Project Connection

The project has zero tests. Before refactoring, write characterization tests for:
- `toolkit.hashIt` — given "password", produces a specific Base64 hash.
- `toolkit.parseText` — given a specific input, produces a specific Map.
- `toolkit.formatString` — given a Map, produces a specific string.
- `oracleConnector.searchIntern` — given specific filters, returns specific results (against a Testcontainers Oracle instance with seed data).
- `oracleConnector.getMaxId` — given a specific table, returns a specific number.

These tests lock in current behavior. After refactoring, they should still pass. Then you can fix bugs (and update the tests to assert the *correct* behavior).

## Common pitfalls

- **Testing what you think it should do** — characterization tests record what it *does*, not what it *should*.
- **Not enough inputs** — test with diverse inputs to capture edge cases.
- **Refactoring before characterization** — without tests, you don't know if your refactoring preserved behavior.

## Further reading

- *Working Effectively with Legacy Code* (Feathers).
- Approval testing frameworks (ApprovalTests, Sparky).
