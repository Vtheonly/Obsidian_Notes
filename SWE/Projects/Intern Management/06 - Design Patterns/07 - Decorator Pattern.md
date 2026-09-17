---
tags: [pattern, structural, decorator]
type: concept
status: complete
related:
  - [[06 - Design Patterns/02 - Adapter Pattern]]
  - [[04 - OOD and SOLID/05 - Composition over Inheritance]]
  - [[05 - Software Architecture/03 - Cross-Cutting Concerns]]
---

# Decorator Pattern

> "Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality." — GoF

## What it is

A **decorator** wraps an object and adds behavior, without changing the interface. The decorator "decorates" the wrapped object with extra functionality.

```java
// Base interface
public interface InternRepository {
    Optional<Intern> findById(long id);
}

// Base implementation
public class OracleInternRepository implements InternRepository {
    public Optional<Intern> findById(long id) { /* query Oracle */ }
}

// Decorator: adds caching
public class CachingInternRepository implements InternRepository {
    private final InternRepository delegate;
    private final Cache<Long, Intern> cache;

    public CachingInternRepository(InternRepository delegate, Cache<Long, Intern> cache) {
        this.delegate = delegate;
        this.cache = cache;
    }

    @Override
    public Optional<Intern> findById(long id) {
        Intern cached = cache.getIfPresent(id);
        if (cached != null) return Optional.of(cached);
        Optional<Intern> result = delegate.findById(id);
        result.ifPresent(i -> cache.put(id, i));
        return result;
    }
}

// Usage: decorate Oracle with caching
InternRepository repo = new CachingInternRepository(
    new OracleInternRepository(dataSource),
    Caffeine.newBuilder().build()
);
```

The caller uses `InternRepository` — doesn't know it's cached.

## Why it exists

- **Composition over inheritance** — instead of `CachingOracleInternRepository extends OracleInternRepository`, wrap it.
- **Stackable** — you can stack multiple decorators:
```java
InternRepository repo = new LoggingInternRepository(
    new CachingInternRepository(
        new OracleInternRepository(dataSource),
        cache
    )
);
```
- **Single responsibility** — each decorator adds one concern.
- **Runtime flexibility** — decorators can be added/removed at runtime.

## Decorator vs inheritance

Inheritance: `class LoggingOracleInternRepository extends OracleInternRepository`. If you also want `LoggingPostgresInternRepository`, you need another subclass. Combinatorial explosion.

Decorator: `new LoggingRepository(new OracleRepository())` or `new LoggingRepository(new PostgresRepository())`. One logging decorator, multiple base implementations.

## Java I/O is all decorators

```java
InputStream in = new BufferedInputStream(
    new GZIPInputStream(
        new FileInputStream("file.gz")
    )
);
```
- `FileInputStream` — reads from a file.
- `GZIPInputStream` — decorates with decompression.
- `BufferedInputStream` — decorates with buffering.

Each adds one concern. Stack them as needed.

## Project Connection

The project has no decorators. The fix can use decorators for:
- `CachingInternRepository` — cache lookups.
- `LoggingDataSource` — log connection borrow/return.
- `MetricsRepository` — time repository methods.
- `AuditingRepository` — log mutations.

## Common pitfalls

- **Decorator that changes behavior instead of adding** — decorators add; they don't replace. If you're replacing, use Strategy.
- **Too many decorators** — 10 layers of decorators is hard to debug. Limit to 2-3.
- **Forgetting to delegate** — the decorator must call the delegate; otherwise it's not a decorator, it's a replacement.

## Further reading

- *Design Patterns* (GoF), Decorator.
- *Head First Design Patterns* (Freeman & Robson), Decorator chapter.
