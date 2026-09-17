---
tags: [concept, java, stream, functional]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/08 - Lambda Expressions and Functional Interfaces]]
  - [[03 - Java Foundations/01 - Collections Framework]]
---

# Stream API

## What it is

Java 8+ Streams are a declarative way to process collections. A stream is a pipeline of operations that does not store elements.

```java
List<String> names = interns.stream()
    .filter(i -> i.getAge() > 18)
    .map(Intern::getName)
    .sorted()
    .collect(Collectors.toList());
```

## Operations

**Intermediate** (lazy, return a Stream):
- `filter(Predicate)` — keep matching elements.
- `map(Function)` — transform each element.
- `flatMap(Function<T, Stream<R>>)` — flatten.
- `sorted()` / `sorted(Comparator)` — sort.
- `distinct()` — remove duplicates.
- `limit(n)` / `skip(n)` — truncate.
- `peek(Consumer)` — inspect (for debugging).

**Terminal** (eager, produce a result):
- `collect(Collector)` — gather into a collection.
- `forEach(Consumer)` — side effect.
- `count()` — count.
- `reduce(BinaryOperator)` — combine.
- `findFirst()` / `findAny()` — return `Optional<T>`.
- `anyMatch` / `allMatch` / `noneMatch` — boolean.
- `min` / `max` — `Optional<T>`.

## Lazy evaluation

Intermediate operations are lazy — they don't execute until a terminal operation is invoked. This allows optimizations like short-circuiting (`findFirst` stops after the first match).

## Parallel streams

```java
interns.parallelStream().filter(...).map(...).collect(...);
```

Uses the common `ForkJoinPool`. Use with caution:
- Only helps for CPU-bound work on large datasets (>10,000 elements).
- The common pool is shared — blocking operations can starve other parallel streams.
- Order is not preserved (unless you use `forEachOrdered`).

## Common pitfalls

- **Calling `stream()` multiple times** — reuse the source collection, not the stream.
- **Using `forEach` for side effects** — prefer `collect` or `reduce`.
- **Mixing lazy and eager** — `peek` is lazy; it won't run until a terminal operation.
- **Using parallel streams for I/O** — the common pool is for CPU work. Use a custom `ForkJoinPool` for I/O.
- **Large pipelines** — break into named methods for readability.

## Project Connection

The project doesn't use streams at all. The 4 copy-pasted CRUD methods could use streams:
```java
public List<Intern> findByFilters(InternSearchCriteria criteria) {
    return findAll().stream()
        .filter(i -> matches(i, criteria))
        .collect(Collectors.toList());
}
```

But the real fix is to do the filtering in SQL, not in Java. See [[13 - JDBC and Data Access/09 - PreparedStatement]].

## Further reading

- *Modern Java in Action* (Urma, Fusco, Mycroft), Chapters 4-6.
