---
tags: [concept, refactoring, parameter-object]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/04 - Extract Method]]
  - [[06 - Design Patterns/03 - Builder Pattern]]
---

# Introduce Parameter Object

## What it is

**Introduce Parameter Object** groups related parameters into a single object.

## When to use

- A method has > 3 parameters.
- The same group of parameters appears in multiple methods.

## Example

```java
// Before: 5 parameters
public List<Intern> searchInterns(String name, String email, String university,
                                   DecisionStatus status, Long themeId, Long deptId) {
    // ...
}

// After: parameter object
public record InternSearchCriteria(
    String name,
    String email,
    String university,
    DecisionStatus status,
    Long themeId,
    Long deptId
) {}

public List<Intern> searchInterns(InternSearchCriteria criteria) {
    // ...
}
```

## Benefits

- **Fewer parameters** — one object instead of 6.
- **Extensibility** — add a field to the criteria without changing the method signature.
- **Naming** — `criteria.name()` is clearer than the 4th parameter.
- **Builder** — pair with a Builder for optional fields.

## Project Connection

The project's `oracleConnector.searchIntern(Map<String, Object> filters)` is a degenerate parameter object — a Map with no type safety. The fix: `InternSearchCriteria` record (or with a Builder).

## Common pitfalls

- **Parameter object with one field** — overkill. Use the field directly.
- **Mega parameter object** — one object passed to 50 methods. Split by concern.

## Further reading

- *Refactoring* (Fowler), "Introduce Parameter Object".
