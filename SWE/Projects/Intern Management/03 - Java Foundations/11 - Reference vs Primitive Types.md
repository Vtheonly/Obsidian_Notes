---
tags: [concept, java, types, memory]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/08 - Memory and Pointers]]
related:
  - [[03 - Java Foundations/13 - String comparison (== vs equals)]]
---

# Reference vs Primitive Types

## The rule

> Primitives hold their value directly. References hold a pointer to a heap object.

```java
int a = 5;
int b = a;          // b is a COPY of 5
b = 10;             // a is still 5

String s1 = "hi";
String s2 = s1;     // s2 is a COPY of the reference — same object
s2 = "bye";         // s1 still points to "hi"
```

## Pass-by-value

Java is **always pass-by-value**. For primitives, the value is the number itself. For references, the value is the pointer.

```java
void mutate(int x) { x = 10; }           // no effect on caller
void mutate(List l) { l.add("x"); }      // caller sees the addition (same heap object)
void reassign(List l) { l = new ArrayList(); }  // no effect on caller (l is a copy of the pointer)
```

## == vs equals

- `==` compares references (for objects) or values (for primitives).
- `.equals()` compares contents (for objects that override it).

```java
String a = new String("hi");
String b = new String("hi");
a == b;          // false — different heap objects
a.equals(b);     // true  — same content
```

## Common pitfalls

- Using `==` for object comparison — use `.equals()`.
- Forgetting that `==` on primitives of different types promotes: `int 5 == long 5L` is true.
- Assuming autoboxing preserves `==`: `Integer a = 127; Integer b = 127; a == b` is true (cached); `Integer a = 128; Integer b = 128; a == b` is false (not cached). Always use `.equals()` for boxed primitives.

## Project Connection

- `if (value == "" || value.isEmpty())` — `value == ""` is always false for runtime strings. See [[03 - Java Foundations/13 - String comparison (== vs equals)]].
- `oracleConnector.isAdmin` returns `roleId == 4` — `roleId` is `int` (primitive), so `==` is correct here.

## Further reading

- *Effective Java* (Bloch), Item 10 (obey general contract when overriding equals).
- JLS §15.21 (Equality Operators).
