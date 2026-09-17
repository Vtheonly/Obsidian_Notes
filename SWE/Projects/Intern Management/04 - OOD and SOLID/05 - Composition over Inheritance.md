---
tags: [concept, ood, composition, inheritance]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/24 - The Four Pillars of OOP]]
  - [[06 - Design Patterns/07 - Decorator Pattern]]
---

# Composition over Inheritance

## What it is

**Inheritance** — "is-a." `Dog extends Animal`. The subclass gets the parent's behavior for free.

**Composition** — "has-a." `Dog has-a Tail`. The class holds a reference to another object and delegates to it.

The GoF recommendation: **favor composition over inheritance.**

## Why inheritance is problematic

1. **Tight coupling** — the subclass depends on the parent's implementation. Changing the parent breaks the subclass.
2. **Fragile base class** — the parent's author didn't anticipate all the ways subclasses might use it.
3. **Deep hierarchies** — hard to understand. `MultiProtocolDownloadHandler extends HttpDownloadHandler extends DownloadHandler extends IOHandler extends Handler`.
4. **Single inheritance** — Java allows only one parent. You can't extend two classes.
5. **LSP violations** — a subclass that overrides a method to do nothing violates the parent's contract.

## Why composition is better

1. **Loose coupling** — the composed object depends on an interface, not a concrete class.
2. **Runtime flexibility** — you can swap the composed object at runtime (`new Dog(new ShortTail())` vs `new Dog(new LongTail())`).
3. **Multiple composition** — a class can compose multiple objects (`Dog has-a Tail, has-a BarkStrategy, has-a Diet`).
4. **Testability** — easy to mock the composed dependencies.

## Example

```java
// Inheritance (fragile)
public class LoggingList extends ArrayList<String> {
    @Override public boolean add(String s) {
        System.out.println("Adding: " + s);
        return super.add(s);
    }
}
// Problem: if ArrayList adds a new addAll that calls add, the logging may or may not fire
// depending on the JVM version's ArrayList implementation.

// Composition (robust)
public class LoggingList implements List<String> {
    private final List<String> delegate;
    public LoggingList(List<String> delegate) { this.delegate = delegate; }
    @Override public boolean add(String s) {
        System.out.println("Adding: " + s);
        return delegate.add(s);
    }
    @Override public String get(int i) { return delegate.get(i); }
    // ... delegate every method
}
```

## When inheritance is OK

- **Pure type hierarchies** — `ArrayList implements List` (interface inheritance, not implementation inheritance).
- **Template method pattern** — the parent defines an algorithm skeleton, subclasses override specific steps.
- **Framework base classes** — when the framework is designed for inheritance (e.g., `AbstractList`, `HttpServlet`).

## Common pitfalls

- **Extending concrete classes** — prefer implementing interfaces.
- **Using inheritance for code reuse** — wrong tool. Use composition or helper methods.
- **Deep hierarchies (>3 levels)** — usually a sign of over-design.

## Project Connection

The project uses no inheritance at all — every class is concrete with no parent (other than `Object`). The fix is not to add inheritance, but to add **interfaces** (`Repository<T, ID>`, `AuthService`) and **composition** (controllers hold services, services hold repositories, repositories hold `DataSource`).

See [[05 - Software Architecture/04 - Dependency Injection]].
