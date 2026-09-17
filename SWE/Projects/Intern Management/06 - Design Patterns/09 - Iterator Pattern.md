---
tags: [pattern, behavioral, iterator]
type: concept
status: complete
related:
  - [[03 - Java Foundations/01 - Collections Framework]]
  - [[03 - Java Foundations/12 - Stream API]]
---

# Iterator Pattern

> "Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation." — GoF

## What it is

An **iterator** is an object that lets you traverse a collection without knowing how it's stored.

```java
public interface Iterator<E> {
    boolean hasNext();
    E next();
}

public class ArrayListIterator<E> implements Iterator<E> {
    private int index = 0;
    private final List<E> list;
    public boolean hasNext() { return index < list.size(); }
    public E next() { return list.get(index++); }
}
```

## Java's enhanced for-loop

```java
for (String name : names) {
    System.out.println(name);
}
```

This works for any `Iterable` (which has an `iterator()` method). The compiler expands it to:
```java
Iterator<String> it = names.iterator();
while (it.hasNext()) {
    String name = it.next();
    System.out.println(name);
}
```

## Why it exists

- **Uniform traversal** — arrays, lists, sets, trees, files — all traversed the same way.
- **Lazy** — the iterator produces elements one at a time, no need to load everything.
- **Removal during traversal** — `Iterator.remove()` lets you remove elements safely during iteration.

## Java's `Iterable` and `Iterator`

```java
public interface Iterable<E> {
    Iterator<E> iterator();
}

public interface Iterator<E> {
    boolean hasNext();
    E next();
    default void remove() { throw new UnsupportedOperationException(); }
}
```

## Project Connection

The project uses enhanced for-loops correctly (e.g., iterating `HashMap.keySet()`). No fix needed here — but the underlying `HashMap` iteration order bug is a separate issue. See [[03 - Java Foundations/01 - Collections Framework]].

## Further reading

- *Design Patterns* (GoF), Iterator.
- Java `Iterable` and `Iterator` documentation.
