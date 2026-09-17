---
tags: [concept, java, optional]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/08 - Encapsulation]]
  - [[03 - Java Foundations/02 - Exception Handling]]
---

# Optional<T>

## What it is

`Optional<T>` is a container object that may or may not contain a non-null value. Introduced in Java 8 to address `NullPointerException` — the "billion-dollar mistake" (Tony Hoare).

```java
Optional<Intern> result = repository.findById(123);
if (result.isPresent()) {
    Intern intern = result.get();
    // ...
} else {
    // not found
}
```

## Why it exists

`null` is ambiguous — it can mean "not found," "not set," "error," or "intentionally absent." Methods that return `null` force every caller to remember to null-check. Forgetting leads to `NullPointerException`.

`Optional<T>` makes absence explicit in the type signature. A method returning `Optional<Intern>` says "this might not find anything." The compiler and IDE remind you to handle the empty case.

## API

```java
Optional<Intern> opt = repository.findById(123);

// Check
opt.isPresent();        // true if value exists
opt.isEmpty();          // true if empty (Java 11+)

// Get
opt.get();              // throws NoSuchElementException if empty
opt.orElse(default);    // return default if empty
opt.orElseThrow();      // throws NoSuchElementException if empty
opt.orElseThrow(() -> new NotFoundException());  // custom exception

// Transform
opt.map(Intern::getName);           // Optional<String>
opt.filter(i -> i.getAge() > 18);   // Optional<Intern>
opt.flatMap(i -> Optional.ofNullable(i.getTheme()));  // Optional<Theme>

// Consume
opt.ifPresent(i -> display(i));
opt.ifPresentOrElse(i -> display(i), () -> showNotFound());
```

## When to use Optional

- **Method return types** — "this method might not return a value."
- **Stream operations** — `findFirst()`, `findAny()`, `max()`, `min()`, `reduce()` return `Optional`.

## When NOT to use Optional

- **Fields** — `Optional` is a wrapper object; storing it in a field wastes memory. Use `@Nullable` annotation instead.
- **Method parameters** — adds overhead. Use method overloading or `@Nullable`.
- **In collections** — `List<Optional<T>>` is wasteful. Use `List<T>` and filter nulls.
- **For serialization** — `Optional` is not serializable.

## Common pitfalls

- Calling `.get()` without checking `.isPresent()` — throws `NoSuchElementException`. Use `.orElse()` or `.orElseThrow()`.
- Using `Optional.of(null)` — throws `NullPointerException`. Use `Optional.ofNullable(null)` (returns empty).
- Storing `Optional` in fields — wasteful.
- Returning `Optional` for everything — overkill. Use it only when absence is meaningful.

## Project Connection

`oracleConnector.getIdByName` returns `Integer` (nullable). Callers do `Integer.parseInt(params.get("theme_id"))` or `oracleConnector.getIdByName(...).toString()`. If the lookup fails, the next line throws `NullPointerException`.

### Fix

```java
public interface InternRepository {
    Optional<Intern> findById(long id) throws SQLException;
    List<Intern> findByFilters(InternSearchCriteria criteria) throws SQLException;
}

// Usage:
Optional<Intern> opt = repository.findById(id);
Intern intern = opt.orElseThrow(() -> new NotFoundException("Intern", id));
```

See [[04 - OOD and SOLID/08 - Encapsulation]] and [[13 - JDBC and Data Access/00 - MOC - JDBC]].

## Further reading

- *Effective Java* (Bloch), Item 55 (return optionals instead of null).
- JLS §8 (Optional class).
