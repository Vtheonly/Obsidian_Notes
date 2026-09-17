---
tags: [concept, cs-foundations, memory, jvm]
type: concept
status: complete
related:
  - [[03 - Java Foundations/11 - Reference vs Primitive Types]]
  - [[03 - Java Foundations/13 - String comparison (== vs equals)]]
  - [[18 - Java Concurrency/05 - Java Memory Model]]
---

# Memory and Pointers

## What it is

Every running program has two regions of memory that concern Java developers:

- **The stack** — per-thread, stores method frames (local variables, return addresses). Small, fast, automatically freed on method return.
- **The heap** — shared across threads, stores objects. Larger, slower, managed by the garbage collector.

A "pointer" (or "reference" in Java) is a variable whose value is the *address* of a heap object. Java does not expose raw addresses the way C does, but references are still pointers under the hood.

## The single most important rule

> **Variables of primitive type (`int`, `double`, `boolean`, `char`) hold their value directly. Variables of reference type (`String`, `Object`, `int[]`) hold a *reference* to the value, which lives on the heap.**

This explains:
- Why `==` on Strings fails (compares references, not contents).
- Why passing an object to a method lets the method mutate it.
- Why the project's `if (value == "")` is a bug.
- Why Java's GC exists (heap memory is not freed automatically when the variable goes out of scope).

## Mental model

```java
int a = 5;          // 'a' is the literal value 5, on the stack.
int b = a;          // 'b' is a COPY of the value 5.
b = 10;             // 'a' is still 5. Primitives are copied by value.

String s1 = "hi";   // 's1' is a reference to a String on the heap.
String s2 = s1;     // 's2' is a COPY of the reference — same object.
s2 = "bye";         // 's1' still points to "hi". References are copied by value,
                    // but the object itself is shared until reassigned.
```

## Why `==` on Strings is broken

```java
String a = new String("hi");
String b = new String("hi");
System.out.println(a == b);        // false — different heap objects
System.out.println(a.equals(b));   // true  — same content
```

`==` compares references. `.equals()` compares contents. The project has:
```java
if (value == "" || value.isEmpty()) { ... }
```
`value == ""` is *almost always false* because `value` is a runtime-constructed string and `""` is a compile-time literal at a different heap address. The code "works" only because the `||` short-circuits to `isEmpty()`.

## Stack vs heap

| Property | Stack | Heap |
|---|---|---|
| Size | Small (default 512 KB/thread) | Large (gigabytes, `-Xmx`) |
| Speed | CPU-register fast | Slower (pointer indirection, GC) |
| Lifetime | Automatic (frame popped on return) | Garbage-collected (when no refs) |
| Thread-safety | Thread-local | Shared (requires synchronization) |
| Stores | Primitives, references to heap | All objects, arrays |

## Why this matters for concurrency

Two threads each calling a method with a local `int x = 5` have separate `x` variables on separate stacks. No synchronization needed.

Two threads each holding a reference to the same `List` point at the same heap object. Mutations are visible to both. Synchronization required. This is the root of every race condition. See [[18 - Java Concurrency/05 - Java Memory Model]].

## Why this matters for `static`

A `static` field lives on the *class itself*, not on instances. There is one copy shared by everyone. The project's `static String labelText` is a single heap-allocated String reference, shared across every UI flow. If two windows open at once, they overwrite each other. See [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]].

## Common pitfalls

- Comparing arrays/objects with `==`. Always use `Arrays.equals()` or `.equals()`.
- Assuming local variables are thread-safe — they are, *unless* you leak a reference to a mutable heap object.
- Confusing pass-by-reference with pass-by-value. Java is *always* pass-by-value. For reference types, the value being passed is the reference itself (a copy of the pointer).
- Forgetting that `String` literals are interned. `String a = "hi"; String b = "hi"; a == b` is true (compiler reuses the literal). This is *not* a reason to use `==`.

## Project Connection

- The `value == ""` bug — see [[03 - Java Foundations/13 - String comparison (== vs equals)]].
- The `static String labelText` shared-state bug — see [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]].
- The static `Connection` shared across threads — see [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]].

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapter 3.
- *Effective Java* (Bloch), Item 10.
- JLS §2 (JVM Structure).
