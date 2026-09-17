---
tags: [concept, java, strings, bug]
type: concept
status: complete
prerequisites:
  - [[03 - Java Foundations/11 - Reference vs Primitive Types]]
  - [[02 - CS Foundations/08 - Memory and Pointers]]
related:
  - [[04 - OOD and SOLID/03 - Code Smells Catalog]]
---

# String comparison: == vs equals

## The bug in the project

```java
// insertionInternController.java and insertionUserController.java
if (value == "" || value.isEmpty()) {
    JOptionPane.showMessageDialog(null, "Fill all the inputs fields");
    return;
}
```

`value == ""` is **always false** for runtime-constructed strings. The code "works" only because `value.isEmpty()` catches the empty case.

## Why `==` fails

`==` compares references — "do these two variables point to the same heap object?"

```java
String a = "hi";                          // literal, interned
String b = "hi";                          // same literal, same interned object
String c = new String("hi");              // new heap object
String d = "h" + "i";                     // compile-time constant, interned
String e = "h";
String f = e + "i";                       // runtime concatenation, new object

a == b;          // true  (both refer to the interned literal)
a == c;          // false (c is a different heap object)
a == d;          // true  (d is a compile-time constant)
a == f;          // false (f is runtime-constructed)
a.equals(c);     // true  (contents are equal)
a.equals(f);     // true
```

`TextField.getText()` returns a runtime-constructed string. `""` is a compile-time literal at a different heap address. So `value == ""` is false even when `value` is empty.

## Why literals are interned

The JVM maintains a **string pool** (interned strings). When the compiler sees the same literal twice, it reuses the same `String` object. This is an optimization — it saves memory.

```java
String a = "hi";
String b = "hi";
// a and b refer to the SAME object in the string pool
```

This is why `a == b` is true for literals. But it's an implementation detail, not a guarantee. **Never rely on it.**

## String interning

You can explicitly intern a string: `String c = new String("hi").intern();` — this returns the canonical interned instance, so `c == a` would be true. But this is rarely necessary and can cause memory leaks (interned strings are never GC'd in old JVMs).

## The correct way

```java
if (value == null || value.isEmpty()) { ... }
// or (Java 11+)
if (value == null || value.isBlank()) { ... }
// or (using Objects)
if (value == null || value.isEmpty()) { ... }
```

`isBlank()` is stricter — it returns true for whitespace-only strings too.

## Static analysis

SonarQube rule `java:S4973` ("Strings should be compared with equals()") flags `==` on strings as a blocker. SpotBugs has a similar rule. Both would catch this bug.

## Project Connection

The bug appears in:
- `insertionInternController.java` line ~167
- `insertionUserController.java` line ~399

Both use the same `value == ""` pattern. The fix is `value.isEmpty()` (already there) — just remove the `value == ""` clause.

## Further reading

- *Effective Java* (Bloch), Item 10.
- JLS §3.10.5 (String Literals).
- JLS §15.21 (Equality Operators).
