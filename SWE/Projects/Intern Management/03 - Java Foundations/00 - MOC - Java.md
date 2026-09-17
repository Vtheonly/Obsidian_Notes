---
tags: [moc, java, java-foundations]
type: moc
status: complete
---

# MOC — Java Foundations

> The project has real bugs from misunderstanding `static`, `==` on Strings,
> `HashMap` iteration order, `try-with-resources`, and exceptions. This chapter
> covers the Java language features the reviews assume you already know.

## Notes (read in order)

1. [[03 - Java Foundations/03 - JVM Architecture]] — class loader, runtime data areas, execution engine.
2. [[03 - Java Foundations/15 - Variables, Types, and Type Systems]] — primitives, references, boxing, generics.
3. [[03 - Java Foundations/11 - Reference vs Primitive Types]] — pass-by-value, == vs equals.
4. [[03 - Java Foundations/13 - String comparison (== vs equals)]] — the project's `value == ""` bug.
5. [[03 - Java Foundations/01 - Collections Framework]] — List, Set, Map, HashMap iteration order, LinkedHashMap.
6. [[03 - Java Foundations/02 - Exception Handling]] — checked vs unchecked, try-with-resources, multi-catch.
7. [[03 - Java Foundations/14 - The static Keyword]] — static fields, methods, initializers, blocks.
8. [[03 - Java Foundations/09 - Modern Date and Time API (java.time)]] — LocalDate, Instant, ZonedDateTime, formatting.
9. [[03 - Java Foundations/07 - Java Records]] — immutable data carriers (Java 16+).
10. [[03 - Java Foundations/05 - Java Enums]] — type-safe constants, the State pattern in miniature.
11. [[03 - Java Foundations/10 - Optional]] — why `Optional<T>` is better than null.
12. [[03 - Java Foundations/06 - Java Naming Conventions]] — PascalCase, camelCase, why lowercase class names are bad.
13. [[03 - Java Foundations/08 - Lambda Expressions and Functional Interfaces]] — `() -> {}`, `Function`, `Predicate`, `Consumer`, `Supplier`.
14. [[03 - Java Foundations/12 - Stream API]] — `stream().filter().map().collect()`.
15. [[03 - Java Foundations/16 - try-with-resources Deep Dive]] — `AutoCloseable`, suppressed exceptions.
16. [[03 - Java Foundations/04 - Java 21 LTS Features]] — virtual threads, pattern matching, sealed classes, switch expressions.

## Why this chapter matters

- The project's `value == ""` bug is a `==` vs `equals` misunderstanding.
- The `HashMap` iteration order bug is a Collections Framework misunderstanding.
- The `static Connection` shared across threads is a `static` misunderstanding.
- The `Integer.parseInt(phone_number)` bug is a type-system misunderstanding.
- The inconsistent `try-with-resources` usage is an exception-handling misunderstanding.
