---
tags: [collection-interface, iterable]
aliases: [collection interface, iterable]
keywords: [collection interface, iterable]
---

## The Collection [[044 Interfaces|Interface]] (`java.util.Collection`)

This is the **root interface** for the hierarchy (excluding Maps). It defines the standard behavior that *all* lists, sets, and queues must have.

Because `List` and `Set` extend `Collection`, they all share these methods:

### Core Methods
*   `boolean add(E e)`: Adds an element.
*   `boolean remove(Object o)`: Removes a specific element.
*   `int size()`: Returns the number of elements.
*   `boolean contains(Object o)`: Checks if an element exists.
*   `boolean isEmpty()`: Checks if size is 0.
*   `void clear()`: Removes everything.
*   `Iterator<E> iterator()`: Allows looping through elements.

### The "Iterable" Parent
`Collection` [[030 Inheritance|extends]] `Iterable`. This is why you can use the "Enhanced For-Loop" (for-each) on any collection.

```java
Collection<String> items = new ArrayList<>();
items.add("Apple");

// Because it implements Iterable:
for (String item : items) {
    System.out.println(item);
}
```

> [!NOTE]
> **[[062 Generics|Generics]] `<E>`**
> `Collection<E>` is generic. `E` stands for "Element". This ensures type safety. Even though [[050 Collections Overview|Collections]] can technically hold `Object` types, we always specify the type (e.g., `<String>`) to prevent [[004 Compile Time vs Run Time|runtime]] casting errors.


---
**Keywords:** #collection-interface, #iterable
