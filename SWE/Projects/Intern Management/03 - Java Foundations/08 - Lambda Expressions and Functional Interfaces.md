---
tags: [concept, java, lambda, functional]
type: concept
status: complete
related:
  - [[03 - Java Foundations/12 - Stream API]]
  - [[06 - Design Patterns/17 - Strategy Pattern]]
---

# Lambda Expressions and Functional Interfaces

## What it is

A **lambda expression** is a concise way to represent an instance of a functional interface (an interface with one abstract method).

```java
// Before Java 8: anonymous class
Runnable r = new Runnable() {
    @Override public void run() { System.out.println("Hello"); }
};

// Java 8+: lambda
Runnable r = () -> System.out.println("Hello");
```

## Functional interfaces

A functional interface has exactly one abstract method. Java provides many in `java.util.function`:

| Interface | Method | Example use |
|---|---|---|
| `Runnable` | `void run()` | `() -> System.out.println("hi")` |
| `Supplier<T>` | `T get()` | `() -> new Intern()` |
| `Consumer<T>` | `void accept(T)` | `intern -> System.out.println(intern)` |
| `Function<T,R>` | `R apply(T)` | `intern -> intern.getName()` |
| `Predicate<T>` | `boolean test(T)` | `intern -> intern.getAge() > 18` |
| `BiFunction<T,U,R>` | `R apply(T,U)` | `(a, b) -> a + b` |
| `UnaryOperator<T>` | `T apply(T)` | `x -> -x` |
| `BinaryOperator<T>` | `T apply(T,T)` | `(a, b) -> a + b` |

## Method references

A shorthand for lambdas that call a single method:
```java
intern -> intern.getName()       // lambda
Intern::getName                  // method reference

() -> new Intern()               // lambda
Intern::new                      // constructor reference

name -> System.out.println(name) // lambda
System.out::println              // method reference
```

## Why lambdas exist

- **Conciseness** — less boilerplate than anonymous classes.
- **Readability** — the intent is clearer.
- **Enable functional programming** — `stream().filter(...).map(...).collect(...)`.

## Common pitfalls

- **Capturing mutable local variables** — the variable must be effectively final. Use a container (`AtomicInteger`) if you need to mutate.
- **Using `this` in a lambda** — `this` refers to the enclosing class, not the lambda. (In anonymous classes, `this` refers to the anonymous instance.)
- **Overusing lambdas** — a complex lambda should be a named method for readability.
- **Lambdas that throw checked exceptions** — functional interfaces don't declare checked exceptions. Wrap in `RuntimeException` or use a custom functional interface.

## Project Connection

The project uses lambdas correctly in some places:
```java
filters.forEach((key, value) -> {  // BiConsumer lambda
    // ...
});
DeleteButton.setOnAction(event -> {  // EventHandler lambda
    // ...
});
```

But misses opportunities elsewhere:
- The 4 copy-pasted `addToXPool` methods could be a generic method taking a `Function<T, String>` formatter.
- The 4 copy-pasted insert methods could use `Function<Intern, PreparedStatement>` setter.

## Further reading

- *Modern Java in Action* (Urma, Fusco, Mycroft), Chapter 3.
- `java.util.function` package documentation.
