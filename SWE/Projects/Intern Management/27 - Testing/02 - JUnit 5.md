---
tags: [concept, testing, junit]
type: concept
status: complete
related:
  - [[27 - Testing/03 - Mockito]]
---

# JUnit 5

## What it is

**JUnit 5** (Jupiter) is the standard Java testing framework.

## Basic test

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

class InternServiceTest {
    private InternService service;

    @BeforeEach
    void setUp() {
        service = new InternService(mockRepository);
    }

    @Test
    void shouldCreateIntern() {
        Intern intern = service.create(new CreateInternCommand("Alice", 22, "alice@example.com"));
        assertNotNull(intern.getId());
        assertEquals("Alice", intern.getName());
    }

    @Test
    void shouldRejectDuplicateEmail() {
        when(repository.existsByEmail("alice@example.com")).thenReturn(true);
        assertThrows(DuplicateEmailException.class, () ->
            service.create(new CreateInternCommand("Alice", 22, "alice@example.com"))
        );
    }
}
```

## Annotations

| Annotation | Purpose |
|---|---|
| `@Test` | Marks a test method. |
| `@BeforeEach` | Runs before each test. |
| `@AfterEach` | Runs after each test. |
| `@BeforeAll` | Runs once before all tests (static). |
| `@AfterAll` | Runs once after all tests (static). |
| `@DisplayName` | Human-readable test name. |
| `@Disabled` | Skip this test. |
| `@Tag` | Group tests (e.g., `@Tag("integration")`). |
| `@Nested` | Nested test class for grouping. |
| `@ParameterizedTest` | Run with multiple inputs. |

## Parameterized tests

```java
@ParameterizedTest
@CsvSource({
    "Alice, 22, alice@example.com, true",
    "'', 22, alice@example.com, false",
    "Alice, 15, alice@example.com, false",
    "Alice, 22, 'not-an-email', false"
})
void shouldValidateInput(String name, int age, String email, boolean valid) {
    CreateInternCommand cmd = new CreateInternCommand(name, age, email);
    assertEquals(valid, validator.validate(cmd).isEmpty());
}
```

## Assertions

```java
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(object);
assertNotNull(object);
assertThrows(Exception.class, () -> { ... });
assertDoesNotThrow(() -> { ... });
assertIterableEquals(expectedList, actualList);
```

## Project Connection

The project has zero tests. The fix: JUnit 5 for all unit and integration tests.

## Further reading

- JUnit 5 User Guide.
