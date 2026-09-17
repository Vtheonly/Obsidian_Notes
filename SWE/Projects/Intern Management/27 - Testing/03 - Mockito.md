---
tags: [concept, testing, mockito, mocking]
type: concept
status: complete
related:
  - [[27 - Testing/02 - JUnit 5]]
---

# Mockito

## What it is

**Mockito** is a Java mocking framework. Create mock objects, stub methods, verify calls.

## Basic usage

```java
@ExtendWith(MockitoExtension.class)
class InternServiceTest {
    @Mock InternRepository repository;
    @Mock AuditService auditService;
    @InjectMocks InternService service;

    @Test
    void shouldSaveIntern() {
        // Arrange
        Intern intern = new Intern("Alice", 22, "alice@example.com");
        when(repository.existsByEmail("alice@example.com")).thenReturn(false);

        // Act
        service.create(intern);

        // Assert
        verify(repository).save(intern);
        verify(auditService).log("CREATE", intern);
    }
}
```

## Stubbing

```java
when(repository.findById(123L)).thenReturn(Optional.of(intern));
when(repository.findById(999L)).thenReturn(Optional.empty());
when(repository.save(any())).thenThrow(new SQLException("DB down"));
```

## Verification

```java
verify(repository).save(intern);              // called once with intern
verify(repository, times(2)).findById(any()); // called twice
verify(repository, never()).delete(any());    // never called
verify(repository, atLeastOnce()).findAll();  // at least once
```

## Argument matchers

```java
when(repository.findById(anyLong())).thenReturn(Optional.empty());
when(repository.findByName(startsWith("Ali"))).thenReturn(List.of(intern));
verify(repository).save(argThat(i -> i.getName().equals("Alice")));
```

## Spy

A **spy** wraps a real object — calls real methods unless stubbed:
```java
List<String> list = spy(new ArrayList<>());
list.add("a");  // real method
when(list.size()).thenReturn(100);  // stubbed
assertEquals(100, list.size());
```

## Project Connection

The project's `oracleConnector` is a static utility — can't be mocked with Mockito (without `mockStatic`, which is fragile). The fix: introduce interfaces (`InternRepository`), inject into services, mock with Mockito in tests.

## Further reading

- Mockito documentation.
