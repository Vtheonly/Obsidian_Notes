---
tags: [concept, solid, isp]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/17 - Programming to Interfaces]]
---

# Interface Segregation Principle (ISP)

> "Clients should not be forced to depend upon interfaces that they do not use." — Robert C. Martin

## What it means

Split fat interfaces into smaller, cohesive ones. A class that needs only `read` shouldn't be forced to also implement `write` and `delete`.

## Example

```java
// Bad: fat interface
public interface Worker {
    void work();
    void eat();
    void sleep();
}

public class Robot implements Worker {
    @Override public void work() { ... }
    @Override public void eat() { throw new UnsupportedOperationException(); }  // robots don't eat
    @Override public void sleep() { throw new UnsupportedOperationException(); }
}

// Good: segregated
public interface Workable { void work(); }
public interface Eatable { void eat(); }
public interface Sleepable { void sleep(); }

public class Robot implements Workable { ... }
public class Human implements Workable, Eatable, Sleepable { ... }
```

## Why it matters

- **No useless methods** — `Robot` doesn't have to stub `eat()` and `sleep()`.
- **Stable interfaces** — changing `Eatable` doesn't affect `Robot`.
- **Cohesion** — each interface has one responsibility.

## The project's (lack of) interfaces

The project has zero interfaces, so ISP doesn't apply yet. But the fix should design interfaces carefully:

```java
// Don't put everything in one fat Repository<T, ID>
public interface Repository<T, ID> {
    void save(T entity);
    Optional<T> findById(ID id);
    List<T> findAll();
    void delete(ID id);
}

// Split if some clients only need read access:
public interface ReadRepository<T, ID> {
    Optional<T> findById(ID id);
    List<T> findAll();
}
public interface WriteRepository<T> {
    void save(T entity);
    void delete(Long id);
}
// A read-only view can depend only on ReadRepository.
```

## Common pitfalls

- **Fat interfaces** — one interface with 20 methods. Split.
- **Empty marker interfaces** — `interface Serializable {}` (Java's, not yours). Use annotations instead.
- **Over-segregation** — 50 single-method interfaces. Find the balance.

## Further reading

- *Clean Architecture* (Martin), Chapter 10 (ISP).
