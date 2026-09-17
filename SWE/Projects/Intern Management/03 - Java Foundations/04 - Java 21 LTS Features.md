---
tags: [concept, java, java21, modern-java]
type: concept
status: complete
related:
  - [[18 - Java Concurrency/04 - Java 21 Virtual Threads]]
---

# Java 21 LTS Features

## What it is

Java 21 (September 2023) is the latest LTS (Long-Term Support) release. It introduces several major features the reviews reference.

## Virtual Threads (JEP 444)

Virtual threads are lightweight threads managed by the JVM, not the OS. Millions can run on a single JVM.

```java
// Before: platform thread (OS thread, expensive)
Thread t = new Thread(() -> { ... });
t.start();

// Java 21: virtual thread (JVM-managed, cheap)
Thread t = Thread.ofVirtual().start(() -> { ... });

// Or via ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> {
            // blocking I/O here — virtual thread is parked, not blocked
            return fetchFromDb(i);
        })
    );
}
```

Virtual threads are best for **I/O-bound** work (DB calls, HTTP requests). For CPU-bound work, use platform threads.

See [[18 - Java Concurrency/04 - Java 21 Virtual Threads]].

## Pattern Matching for instanceof (JEP 441)

```java
// Before
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// Java 21
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

## Pattern Matching for switch (JEP 441)

```java
// Before
String describe(Object o) {
    if (o instanceof Integer i) return "int " + i;
    if (o instanceof String s) return "string " + s;
    return "unknown";
}

// Java 21
String describe(Object o) {
    return switch (o) {
        case Integer i -> "int " + i;
        case String s -> "string " + s;
        case null -> "null";
        default -> "unknown";
    };
}
```

## Sealed Classes (JEP 409, finalized in 17)

```java
public sealed interface Shape permits Circle, Square, Triangle {}
public record Circle(double radius) implements Shape {}
public record Square(double side) implements Shape {}
public record Triangle(double base, double height) implements Shape {}
```

The compiler knows all subtypes of `Shape`. Combined with pattern matching, enables exhaustive switch:

```java
double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Square s -> s.side() * s.side();
        case Triangle t -> 0.5 * t.base() * t.height();
        // no default needed — exhaustive
    };
}
```

## Record Patterns (JEP 440)

```java
void printIntern(Object o) {
    if (o instanceof Intern(String name, Integer age, String email)) {
        System.out.println(name + " (" + age + ") " + email);
    }
}
```

## Text Blocks (Java 15+, standard in 17)

```java
String json = """
    {
        "name": "Alice",
        "age": 30
    }
    """;
```

## Switch Expressions (Java 14)

```java
DecisionStatus status = switch (statusStr) {
    case "Pending" -> DecisionStatus.PENDING;
    case "Accepted" -> DecisionStatus.ACCEPTED;
    case "Rejected" -> DecisionStatus.REJECTED;
    default -> throw new IllegalArgumentException("Unknown: " + statusStr);
};
```

## Why this matters

The project targets Java 20 (non-LTS, EOL). The fix is Java 21 LTS:
- Records for domain objects.
- Pattern matching for cleaner instanceof.
- Sealed classes for closed hierarchies.
- Virtual threads for high-concurrency DB calls.
- Switch expressions for cleaner status mapping.

## Common pitfalls

- Using `var` everywhere — reduces readability when the type is not obvious.
- Using virtual threads for CPU-bound work — they don't help (and may hurt).
- Forgetting that sealed classes need a `permits` clause (or the compiler infers it from the same file).

## Project Connection

The project is on Java 20. Migrating to Java 21 LTS enables:
- Records for `Intern`, `WorkerUser`, etc.
- Pattern matching for cleaner controller code.
- Virtual threads for the background DB executor.
- Switch expressions for status mapping.

See [[24 - Build and Tooling/00 - MOC - Build and Tooling]].

## Further reading

- JEP 444 (Virtual Threads).
- JEP 441 (Pattern Matching for switch).
- *Java 21 in Action* (when published).
