---
tags: [concept, solid, lsp]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/05 - Composition over Inheritance]]
---

# Liskov Substitution Principle (LSP)

> "Subtypes must be substitutable for their base types." — Barbara Liskov, 1987

## What it means

If `B` is a subtype of `A`, then you should be able to use a `B` anywhere an `A` is expected, without surprises.

## Classic LSP violations

### 1. Square extends Rectangle

```java
public class Rectangle { protected int w, h; ... setWidth, setHeight ... }
public class Square extends Rectangle {
    @Override public void setWidth(int w) { this.w = this.h = w; }  // changes height too!
    @Override public void setHeight(int h) { this.w = this.h = h; }
}

void resize(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.getArea() == 50;  // fails for Square!
}
```

`Square` is not substitutable for `Rectangle` — calling `setWidth` on a Square changes the height. The base class contract (independent width/height) is violated.

### 2. EmptyList throws on add

```java
public class EmptyList extends ArrayList {
    @Override public boolean add(Object e) { throw new UnsupportedOperationException(); }
}
// Caller expects: list.add(x) returns true. EmptyList throws. LSP violated.
```

### 3. ReadOnlyFile extends File

```java
public class ReadOnlyFile extends File {
    @Override public void write(byte[] data) { throw new UnsupportedOperationException(); }
}
// Caller expects: file.write(data) writes. ReadOnlyFile throws. LSP violated.
```

## The contract

LSP requires that subtypes honor the base type's **contract**:
- **Preconditions** cannot be strengthened in a subtype.
- **Postconditions** cannot be weakened in a subtype.
- **Invariants** must be preserved.
- **History constraint** — mutable methods that the base doesn't allow (e.g., immutable base, mutable subtype) violate LSP.

## Why it matters

Without LSP, polymorphism is unsafe. Code that uses the base type must check `if (instanceof Square)` to avoid surprises — defeating the purpose of polymorphism.

## Common pitfalls

- Overriding a method to throw `UnsupportedOperationException`.
- Overriding a method to do nothing (silent failure).
- Strengthening preconditions (subtype rejects inputs the base accepts).
- Weakening postconditions (subtype returns worse results).

## Project Connection

The project has no inheritance, so no LSP violations. But the fix's `OracleInternRepository implements InternRepository` must honor the `InternRepository` contract — e.g., if `findById` returns `Optional<Intern>`, it must not throw `SQLException` for "not found" (that's what empty `Optional` is for). It may throw `SQLException` for actual DB errors.

## Further reading

- *Clean Architecture* (Martin), Chapter 9 (LSP).
- Liskov, "Data Abstraction and Hierarchy" (1987).
