---
tags: [concept, java, collections]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/05 - Data Structures Overview]]
  - [[03 - Java Foundations/15 - Variables, Types, and Type Systems]]
related:
  - [[06 - Design Patterns/09 - Iterator Pattern]]
---

# Collections Framework

## What it is

The Java Collections Framework (JCF) is a unified architecture for storing and manipulating groups of objects. It lives in `java.util`.

## Core interfaces

| Interface | Description | Key implementations |
|---|---|---|
| `Collection<E>` | Root interface | — |
| `List<E>` | Ordered, allows duplicates, indexable | `ArrayList`, `LinkedList`, `CopyOnWriteArrayList` |
| `Set<E>` | No duplicates | `HashSet`, `LinkedHashSet`, `TreeSet` |
| `Queue<E>` | FIFO | `ArrayDeque`, `LinkedList`, `PriorityQueue` |
| `Deque<E>` | Double-ended queue | `ArrayDeque`, `LinkedList` |
| `Map<K,V>` | Key-value pairs (not a `Collection`) | `HashMap`, `LinkedHashMap`, `TreeMap`, `ConcurrentHashMap` |

## HashMap iteration order

**`HashMap` does not guarantee iteration order.** The order can change between JVM versions, after a rehash, or even between runs (because hash seeds are randomized in Java 8+ for security).

```java
HashMap<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);
map.put("c", 3);
map.forEach((k, v) -> System.out.println(k));  // order is undefined
```

If you need:
- **Insertion order** → `LinkedHashMap`.
- **Sorted order** → `TreeMap` (by key) or `Collections.sort()`.
- **Thread safety** → `ConcurrentHashMap` (iteration order still undefined, but weakly consistent).

## The project's bug

```java
StringBuilder columns = new StringBuilder();
for (String key : internData.keySet()) {        // iteration 1
    columns.append(key).append(", ");
}
// ...
int i = 1;
for (Object value : internData.values()) {      // iteration 2
    pstmt.setObject(i++, value);
}
```

This works *today* because `keySet()` and `values()` are both backed by the same internal map, so they iterate in the same order. But:

1. The Java spec does **not** guarantee this.
2. If someone switches to `ConcurrentHashMap`, the two iterations may diverge.
3. If the map is rehashed between iterations (e.g., by a concurrent modification), the order may change.

### Fix

Option 1: `LinkedHashMap` (preserves insertion order):
```java
Map<String, Object> internData = new LinkedHashMap<>();
```

Option 2: Iterate `entrySet()` in a single loop:
```java
for (Map.Entry<String, Object> e : internData.entrySet()) {
    columns.append(e.getKey()).append(", ");
    values.add(e.getValue());
}
```

Option 3 (best): Use a typed domain object with a hardcoded SQL string:
```java
public void save(Intern intern) {
    String sql = "INSERT INTO interns (name, age, email, ...) VALUES (?, ?, ?, ...)";
    try (PreparedStatement ps = conn.prepareStatement(sql)) {
        ps.setString(1, intern.name());
        ps.setInt(2, intern.age());
        ps.setString(3, intern.email());
        // ...
    }
}
```

## Common pitfalls

- Using `HashMap` when order matters → `LinkedHashMap` or `TreeMap`.
- Using `ArrayList` when you need fast contains → `HashSet`.
- Modifying a collection while iterating → `ConcurrentModificationException`. Use `Iterator.remove()` or `Collection.removeIf()`.
- Assuming `ArrayList` and `LinkedList` are interchangeable → `LinkedList.get(i)` is O(n).
- Using `Vector` (legacy, synchronized) → use `ArrayList` + `Collections.synchronizedList()` or `CopyOnWriteArrayList`.

## Project Connection

- `HashMap` iteration order bug — see above.
- `List<Map<String,Object>>` instead of `List<Intern>` — see [[04 - OOD and SOLID/01 - Anemic Domain Model]].
- `FXCollections.observableArrayList()` — JavaFX's observable wrapper. Used correctly in the PieChart data.

## Further reading

- *Java Generics and Collections* (Naftalin & Wadler).
- `java.util` package documentation.
