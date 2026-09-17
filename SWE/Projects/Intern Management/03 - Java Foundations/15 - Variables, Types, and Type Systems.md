---
tags: [concept, java, types]
type: concept
status: complete
related:
  - [[02 - CS Foundations/09 - Number Systems and Binary]]
  - [[02 - CS Foundations/06 - Floating Point and Numeric Precision]]
---

# Variables, Types, and Type Systems

## What it is

A **type** is a set of values plus a set of operations on those values. A **type system** is a set of rules that assigns types to expressions and checks that operations are valid.

Java has:
- **Primitive types** (8): `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`, `char`. Stored by value.
- **Reference types**: classes, interfaces, arrays, enums. Stored by reference (pointer to heap).
- **Boxed primitives**: `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Boolean`, `Character`. Objects that wrap primitives. Can be `null`.

## Type safety

Java is **statically typed** — type errors are caught at compile time. Java is **strongly typed** — implicit conversions are limited.

But Java's type system has holes:
- **Boxing/Unboxing** — `Integer i = 5;` autoboxes; `int x = i;` auto-unboxes. If `i` is `null`, unboxing throws `NullPointerException`.
- **Generic erasure** — `List<String>` and `List<Integer>` are both `List` at runtime. Type safety is enforced at compile time only.
- **Casts** — `(String) obj` compiles but throws `ClassCastException` at runtime if `obj` is not a String.
- **Raw types** — `List list = new ArrayList()` compiles with a warning. Type safety lost.

## Why this matters

The project's `Map<String, Object>` is a **type-erased escape hatch**. Any value can be stored as `Object`, retrieved as `Object`, and cast to the expected type. A typo like `params.get("full_naem")` returns `null` at runtime — not a compile error.

The fix: use typed domain objects (`Intern`, `WorkerUser`) with fields of specific types. The compiler catches typos. See [[04 - OOD and SOLID/01 - Anemic Domain Model]].

## Primitive ranges

| Type | Bits | Min | Max |
|---|---|---|---|
| `byte` | 8 | -128 | 127 |
| `short` | 16 | -32,768 | 32,767 |
| `int` | 32 | -2,147,483,648 | 2,147,483,647 |
| `long` | 64 | -9.2 × 10^18 | 9.2 × 10^18 |
| `float` | 32 | ~±3.4 × 10^38 | 7 sig digits |
| `double` | 64 | ~±1.8 × 10^308 | 15-17 sig digits |
| `char` | 16 | 0 | 65,535 (UTF-16 code unit) |
| `boolean` | 1 | false | true |

## Common pitfalls

- Using `int` for primary keys — use `long`. 32-bit IDs run out.
- Using `Integer` (boxed) when `int` (primitive) would do — unnecessary allocation.
- Using `double` for money — use `BigDecimal`.
- Using `Integer.parseInt` for phone numbers — use `String`.
- Forgetting that `Integer` can be `null` but `int` cannot.

## Project Connection

- `Integer.parseInt(phone_number)` — bug. Phone numbers are not integers.
- `getInt("intern_id")` on `NUMBER(10)` — should be `getLong`.
- `Map<String, Object>` everywhere — no compile-time type safety.
- `(String) intern.get("theme_id")` then `Integer.parseInt` — round-trip type juggling.

## Further reading

- *Effective Java* (Bloch), Item 61 (prefer primitive types to boxed primitives).
- JLS §4 (Types, Values, and Variables).
