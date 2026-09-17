---
tags: [concept, ood, interfaces, dip]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]]
  - [[06 - Design Patterns/17 - Strategy Pattern]]
---

# Programming to Interfaces

## What it is

> "Program to an interface, not an implementation." — Gang of Four, Design Patterns (1994)

Depend on the **abstraction** (interface or abstract class), not the **concrete class**. This decouples your code from specific implementations.

```java
// Bad: depends on concrete ArrayList
ArrayList<String> names = new ArrayList<>();

// Good: depends on List interface
List<String> names = new ArrayList<>();
```

The variable type is `List` (interface). The implementation is `ArrayList`. You can swap `ArrayList` for `LinkedList` without changing any code that uses `names`.

## Why it matters

1. **Flexibility** — swap implementations without rewriting callers.
2. **Testability** — mock the interface in tests.
3. **Decoupling** — callers don't know about the implementation's details.
4. **Polymorphism** — multiple implementations can be used interchangeably.

## At the architectural level

```java
// Controller depends on interface (AuthService)
public class LoginController {
    private final AuthService authService;  // interface, not AuthServiceImpl

    public LoginController(AuthService authService) {
        this.authService = authService;
    }
}

// In production: inject AuthServiceImpl
// In tests: inject MockAuthService
```

The controller doesn't know whether it's using a real `AuthServiceImpl` or a `MockAuthService`. It only knows the `AuthService` contract.

## Common pitfalls

- **No interfaces at all** — the project has zero `interface` declarations. Every class is concrete. Untestable.
- **Interface with one implementation** — sometimes YAGNI, but for architectural seams (Repository, AuthService), the interface is worth it.
- **`var` hiding the interface** — `var list = new ArrayList<>()` infers `ArrayList`, not `List`. Use `List<String> list = new ArrayList<>()` for the interface.
- **Returning concrete types** — `public ArrayList<String> getNames()` forces callers to depend on `ArrayList`. Return `List<String>`.

## Project Connection

The project has **no interfaces**. Every class depends on `oracleConnector` (concrete). This:
- Makes the project untestable (can't mock `oracleConnector`).
- Makes the project unportable (can't swap Oracle for PostgreSQL without rewriting every consumer).
- Locks every consumer to the `oracleConnector` API.

### Fix

```java
public interface InternRepository {
    void save(Intern intern) throws SQLException;
    Optional<Intern> findById(long id) throws SQLException;
    List<Intern> findByFilters(InternSearchCriteria criteria) throws SQLException;
    void delete(long id) throws SQLException;
}

public class OracleInternRepository implements InternRepository {
    // Oracle-specific implementation
}

public class InternService {
    private final InternRepository repository;  // interface, not OracleInternRepository
    public InternService(InternRepository repository) {
        this.repository = repository;
    }
}
```

Now `InternService` can be tested with a `MockInternRepository` or `InMemoryInternRepository`, and can be ported to PostgreSQL by writing `PostgresInternRepository`.

See [[05 - Software Architecture/14 - Repository Pattern]] and [[05 - Software Architecture/04 - Dependency Injection]].
