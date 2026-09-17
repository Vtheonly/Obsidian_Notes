---
tags: [concept, java, static]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/03 - JVM Architecture]]
  - [[02 - CS Foundations/08 - Memory and Pointers]]
related:
  - [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]]
---

# The static Keyword

## What it is

`static` means "belongs to the class, not to an instance." There is one copy per class, shared by all instances (and by all code that can access the class).

## Four uses

1. **Static fields** — one value per class.
2. **Static methods** — callable without an instance.
3. **Static initializers** — run once when the class is loaded.
4. **Static nested classes** — nested classes that don't need an outer instance.

## Static fields

```java
public class Counter {
    private static int count = 0;  // one copy, shared by all instances
    public Counter() { count++; }
    public static int getCount() { return count; }
}
```

`count` lives in the method area. All `Counter` instances share it. All threads share it. **Static mutable fields are a concurrency hazard.**

## Static methods

```java
public class MathUtils {
    public static int square(int x) { return x * x; }
}
// Call: MathUtils.square(5)  — no instance needed
```

Static methods cannot access instance fields (there is no `this`). They can access static fields.

## Static initializers

```java
public class DbConnection {
    private static Connection connection;
    static {
        try {
            connection = DriverManager.getConnection(URL, USER, PASS);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

The `static {}` block runs once, when the class is loaded. **Side effects in static initializers are an anti-pattern** — the class cannot be loaded without a live DB.

## When static is OK

- **Constants** — `public static final double PI = 3.14159;` (immutable, thread-safe).
- **Pure utility functions** — `Math.sqrt`, `Collections.sort`. No state, no side effects.
- **Factory methods** — `List.of(1, 2, 3)`, `Optional.empty()`.
- **Logger fields** — `private static final Logger log = LoggerFactory.getLogger(MyClass.class);` (logger is thread-safe).

## When static is bad

- **Mutable static fields** — shared state, race conditions, untestable.
- **Static initializers with side effects** — class loading triggers I/O, network, DB.
- **Static utility classes that should be singletons** — hides dependencies, untestable.
- **Static methods that should be instance methods** — prevents polymorphism, mocking.

## Common pitfalls

- Using `static` for "convenience" (no need to create an instance) — hides dependencies.
- Assuming `static` means "constant" — it means "one per class," not "immutable."
- Forgetting that static initializers run at class-load time — surprising side effects.
- Using `static` to share state between controllers — race conditions, untestable.

## Project Connection

The project abuses `static` extensively:

1. `oracleConnector.connection` (static mutable Connection) — shared across all threads, not thread-safe, no pool.
2. `oracleConnector.URL/USERNAME/PASSWORD` (static final String) — fine (immutable), but hardcoded.
3. `oracleConnector`'s entire API is static — every method is `public static`. This makes the class untestable (can't mock) and tightly coupled to every controller.
4. `toolkit` — same pattern. All static methods.
5. `insertionInternController.labelText` (static mutable String) — cross-controller shared state, race condition.
6. `insertionUserController.labelText` (static mutable String) — same.
7. `oracleConnector` static initializer opens a DB connection at class-load time.
8. `oracleConnector Connection = new oracleConnector();` in two controllers — instantiates a class with only static methods. Wasteful, signals misunderstanding of `static`.

### Fix

- Replace static DAO with instance repositories, injected via constructor.
- Remove static `labelText`, pass data via controller setters.
- Replace static initializer with lazy initialization or explicit `init()` called from `main`.
- Replace static utility `toolkit` with instance classes (`PasswordHasher`, `RecordFormatter`) or proper utility classes with no mutable state.

See [[05 - Software Architecture/04 - Dependency Injection]] and [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]].

## Further reading

- *Effective Java* (Bloch), Item 4 (enforce noninstantiability with private constructor), Item 1 (consider static factory methods).
- *Working Effectively with Legacy Code* (Feathers).
