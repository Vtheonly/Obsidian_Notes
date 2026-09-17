---
tags: [pattern, creational, singleton]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]]
  - [[05 - Software Architecture/04 - Dependency Injection]]
---

# Singleton Pattern

> "Ensure a class has only one instance, and provide a global point of access to it." — GoF

## What it is

A **singleton** is a class that has exactly one instance, accessible globally.

## The classic implementation (broken)

```java
public class Database {
    private static Database instance;
    private Database() {}
    public static Database getInstance() {
        if (instance == null) {
            instance = new Database();
        }
        return instance;
    }
}
```

Problems:
- **Not thread-safe** — two threads can both see `instance == null` and both create.
- **Global state** — any code can access `Database.getInstance()`, hidden dependencies.
- **Hard to test** — can't substitute a mock.

## Thread-safe implementations

### Synchronized
```java
public static synchronized Database getInstance() {
    if (instance == null) instance = new Database();
    return instance;
}
```
Slow (synchronized on every call).

### Double-checked locking
```java
private static volatile Database instance;
public static Database getInstance() {
    if (instance == null) {
        synchronized (Database.class) {
            if (instance == null) instance = new Database();
        }
    }
    return instance;
}
```
Fast but tricky to get right (the `volatile` is essential).

### Initialization-on-demand holder (lazy, thread-safe)
```java
public class Database {
    private Database() {}
    private static class Holder {
        static final Database INSTANCE = new Database();
    }
    public static Database getInstance() { return Holder.INSTANCE; }
}
```
The JVM guarantees `Holder.INSTANCE` is initialized once, lazily, thread-safely.

### Enum singleton (Effective Java Item 3)
```java
public enum Database {
    INSTANCE;
    // methods
}
```
The simplest, safest singleton. Serialization-safe, reflection-safe.

## When Singleton is justified

- **Truly one instance** — `DataSource`, `ObjectMapper`, `Configuration`.
- **Heavy to create** — a `DataSource` opens a pool; you don't want two pools.
- **Thread-safe** — the singleton's methods must be thread-safe.

## When Singleton is misused

- **Static utility with mutable state** — `oracleConnector.connection` is a singleton in spirit but with mutable state. Anti-pattern.
- **Hidden dependency** — `Database.getInstance()` called from inside business logic. Inject instead.
- **For "convenience"** — `AuthService.getInstance()` instead of injecting. Hides the dependency.

## The right way: DI-managed singleton

In a DI container, you declare a class as singleton-scoped, and the container ensures one instance. The class itself is a normal POJO — no `getInstance()`, no static fields.

```java
@Service
public class DataSourceBean {
    @Bean
    public DataSource dataSource() {
        return new HikariDataSource(config);
    }
}

@Service
public class InternService {
    private final InternRepository repository;
    public InternService(InternRepository repository) {  // injected, singleton-scoped
        this.repository = repository;
    }
}
```

The container manages the singleton lifecycle. The class is testable.

## Project Connection

The project's `oracleConnector` is a singleton in the worst way — static mutable state, global access, no DI. The fix: convert to an instance class, inject via constructor, let the composition root (or DI container) manage the singleton lifecycle.

## Further reading

- *Effective Java* (Bloch), Item 3 (enum singleton).
- *Design Patterns* (GoF), Singleton.
