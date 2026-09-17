---
tags: [concept, anti-pattern, static]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/14 - The static Keyword]]
related:
  - [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]]
  - [[05 - Software Architecture/04 - Dependency Injection]]
---

# Static Utility Anti-Pattern

## What it is

A **static utility class** is a class with only static methods and no instance state. Common examples: `java.lang.Math`, `java.util.Collections`, the project's `toolkit` and `oracleConnector`.

Static utilities are not always an anti-pattern. `Math.sqrt` is fine — it's a pure function with no state. The anti-pattern is **static mutable state** or **static methods that should be polymorphic**.

## When static is OK

- **Pure functions** — `Math.sqrt`, `Collections.sort`. No state, no side effects, no dependencies.
- **Constants** — `public static final double PI = 3.14159;`.
- **Logger fields** — `private static final Logger log = LoggerFactory.getLogger(MyClass.class);` (logger is thread-safe).
- **Factory methods** — `List.of(1, 2, 3)`, `Optional.empty()`.

## When static is bad

### 1. Static mutable state

```java
public class oracleConnector {
    private static Connection connection;  // shared mutable state
    static {
        connection = DriverManager.getConnection(...);  // side effect at class load
    }
}
```

Problems:
- **Not thread-safe** — `Connection` is not thread-safe; sharing it across threads corrupts transactions.
- **Global** — every consumer depends on the same connection; no isolation.
- **Untestable** — you cannot replace the connection with a mock.
- **Lifecycle** — the connection opens at class-load time, before the user has even seen the login screen. If the DB is down, the app silently fails.

### 2. Static methods that should be polymorphic

```java
public class oracleConnector {
    public static List<Map<String, Object>> searchIntern(Map<String, Object> filters) { ... }
}
```

Problems:
- **Cannot be overridden** — subclasses cannot change the behavior.
- **Cannot be mocked** — tests cannot substitute a fake.
- **Tight coupling** — every caller is locked to `oracleConnector`.

### 3. Static "singletons" with mutable state

```java
public class AppState {
    private static User currentUser;  // mutable
    public static User getCurrentUser() { return currentUser; }
    public static void setCurrentUser(User u) { currentUser = u; }
}
```

Problems:
- **Global mutable state** — any thread can change it.
- **Hidden dependency** — methods that read `AppState.getCurrentUser()` have a hidden dependency on this global.
- **Untestable** — tests interfere with each other via the shared state.

## The fix

Convert static utilities to instance classes with injected dependencies:

```java
// Before (static utility)
public class oracleConnector {
    private static Connection connection;
    public static List<Map<String, Object>> searchIntern(...) { ... }
}

// After (instance class with injected dependency)
public class OracleInternRepository implements InternRepository {
    private final DataSource dataSource;  // injected

    public OracleInternRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public List<Intern> findByFilters(InternSearchCriteria criteria) {
        try (Connection conn = dataSource.getConnection()) {  // borrow per operation
            // ...
        }
    }
}
```

## "Static is dangerous" (Bloch, Effective Java Item 4)

If you must have a utility class (e.g., `Math`), make it **noninstantiable**:
```java
public class MathUtils {
    private MathUtils() { throw new AssertionError(); }  // prevent instantiation
    public static int square(int x) { return x * x; }
}
```

The private constructor prevents anyone from creating an instance. The `AssertionError` (not just `private`) prevents reflection-based instantiation.

## Common pitfalls

- **Static mutable fields** — almost always wrong. Use instance fields with injection.
- **Static initializers with side effects** — class loading triggers I/O, network, DB. Avoid.
- **Static methods that "are convenient"** — convenience hides coupling. Inject instead.
- **"It's just a utility"** — utilities grow. Today's utility is tomorrow's god class.

## Project Connection

The project's `oracleConnector` and `toolkit` are both static utility classes. `oracleConnector` has static mutable state (the Connection) — the worst form. `toolkit` is closer to OK (mostly pure functions), but `isHashEqual` is dead code and `hashIt` should be an instance of a `PasswordEncoder` interface for testability.

## Further reading

- *Effective Java* (Bloch), Item 4 (enforce noninstantiability).
- *Working Effectively with Legacy Code* (Feathers).
