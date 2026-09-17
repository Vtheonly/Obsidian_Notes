---
tags: [concept, solid, dip, di]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/17 - Programming to Interfaces]]
  - [[05 - Software Architecture/04 - Dependency Injection]]
---

# Dependency Inversion Principle (DIP)

> 1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
> 2. Abstractions should not depend on details. Details should depend on abstractions.
> — Robert C. Martin

## What it means

In a traditional layered architecture, high-level code depends on low-level code:

```
Controller → Service → DAO → Driver → DB
```

Each layer knows about the layer below. The dependency direction is **downward**.

DIP inverts this. The high-level module defines an interface, and the low-level module implements it:

```
Controller → Service → Repository (interface) ← implements ← OracleRepository
                                       ↑
                            (the dependency points UP, not down)
```

Now `Service` depends on `Repository` (abstraction), not on `OracleRepository` (detail). You can swap `OracleRepository` for `PostgresRepository` without touching `Service`.

## Why it matters

- **Decoupling** — high-level policy is independent of low-level details.
- **Testability** — inject a mock implementation in tests.
- **Flexibility** — swap implementations at runtime.
- **Parallel development** — the team writing `Service` doesn't wait for `OracleRepository` to be finished; they code against the interface.

## The project's DIP violation

```java
public class insertionInternController {
    private oracleConnector Connection = new oracleConnector();  // depends on concrete class
    // ...
    public void searchIntern() {
        List<Map<String, Object>> results = oracleConnector.searchIntern(filters);
        // ...
    }
}
```

The controller depends on `oracleConnector` (concrete, static). Cannot be mocked. Cannot be swapped. Cannot be tested in isolation.

## The fix

```java
public class InternSearchController {
    private final InternService internService;  // interface

    public InternSearchController(InternService internService) {
        this.internService = internService;
    }

    public void search() {
        List<Intern> results = internService.findByFilters(criteria);
        // ...
    }
}

public class InternService {
    private final InternRepository repository;  // interface

    public InternService(InternRepository repository) {
        this.repository = repository;
    }
}

public class OracleInternRepository implements InternRepository {  // implements abstraction
    private final DataSource dataSource;
    // ...
}
```

The dependency graph: `Controller → InternService → InternRepository ← OracleInternRepository`. Dependencies point **inward** toward the abstraction.

## Common pitfalls

- **Depending on concrete classes** — `new OracleInternRepository()` inside the service. Inject it instead.
- **Static methods** — `oracleConnector.searchIntern()` — cannot be overridden, cannot be mocked. The worst DIP violation.
- **`new` is glue** (Mark Seemann) — every `new` keyword is a hard dependency. Use a DI container or manual constructor injection.

## Project Connection

The project's every class depends on `oracleConnector` (concrete, static). The fix: introduce interfaces (`Repository<T, ID>`, `AuthService`), inject implementations via constructors. See [[05 - Software Architecture/04 - Dependency Injection]].

## Further reading

- *Clean Architecture* (Martin), Chapter 11 (DIP).
- *Dependency Injection in .NET* (Seemann) — applies to Java too.
