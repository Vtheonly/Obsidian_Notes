---
tags: [concept, refactoring, polymorphism]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
  - [[04 - OOD and SOLID/15 - Open-Closed Principle (OCP)]]
  - [[06 - Design Patterns/17 - Strategy Pattern]]
---

# Replace Conditional with Polymorphism

## What it is

**Replace Conditional with Polymorphism** turns a `switch` or `if/else if` chain on a type code into polymorphic method calls.

## When to use

- You have a switch on a type code that keeps growing.
- You add a new type and have to update multiple switches.
- OCP violation: adding a type requires modifying existing code.

## Example

```java
// Before: switch on type
public double calculateArea(Shape s) {
    switch (s.getType()) {
        case "circle": return Math.PI * s.getRadius() * s.getRadius();
        case "square": return s.getSide() * s.getSide();
        case "triangle": return 0.5 * s.getBase() * s.getHeight();
        default: throw new IllegalArgumentException("Unknown shape");
    }
}

// After: polymorphism
public abstract class Shape {
    public abstract double calculateArea();
}
public class Circle extends Shape {
    public double calculateArea() { return Math.PI * radius * radius; }
}
public class Square extends Shape {
    public double calculateArea() { return side * side; }
}
public class Triangle extends Shape {
    public double calculateArea() { return 0.5 * base * height; }
}

// Usage
double area = shape.calculateArea();  // no switch
```

Adding a new shape (e.g., `Hexagon`) requires writing a new class — no modification of existing code (OCP).

## Project Connection

The project's `getIdByName` switch on table name is the textbook case:

```java
// Before
switch (tableName) {
    case "intern": // ...
    case "theme": // ...
    case "department": // ...
    case "worker_user": // ...
    default: throw new IllegalArgumentException();
}

// After: polymorphism
public interface Repository<T, ID> {
    Optional<Long> findIdByName(String name);
}
public class OracleInternRepository implements Repository<Intern, Long> {
    public Optional<Long> findIdByName(String name) { /* query interns */ }
}
public class OracleThemeRepository implements Repository<Theme, Long> {
    public Optional<Long> findIdByName(String name) { /* query themes */ }
}
// Adding a new entity: write a new class. No modification.
```

## When NOT to use

- **Simple switches** — a 3-case switch that never grows doesn't need polymorphism.
- **Performance-critical code** — polymorphism has a small overhead. Usually negligible, sometimes not.
- **When the type changes at runtime** — if the same object changes type, polymorphism doesn't fit (use State pattern).

## Further reading

- *Refactoring* (Fowler), "Replace Conditional with Polymorphism".
