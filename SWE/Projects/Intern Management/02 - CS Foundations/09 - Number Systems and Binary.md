---
tags: [concept, cs-foundations, numbers]
type: concept
status: complete
related:
  - [[03 - Java Foundations/15 - Variables, Types, and Type Systems]]
  - [[08 - Relational DB Foundations/08 - Oracle Data Types]]
---

# Number Systems and Binary

## What it is

Computers store everything as bits. The four bases you need:
- **Binary** (base 2): digits 0–1. Hardware native.
- **Octal** (base 8): digits 0–7. Rare.
- **Decimal** (base 10): digits 0–9. Human native.
- **Hexadecimal** (base 16): digits 0–9 + A–F. Compact byte representation; used for hashes, colors, memory addresses.

## Integer overflow

Java `int` is 32-bit signed: range `-2,147,483,648` to `2,147,483,647`. Adding 1 to max wraps to min:

```java
int max = Integer.MAX_VALUE;       // 2147483647
int overflow = max + 1;            // -2147483648 (silent wrap!)
```

Java `long` is 64-bit signed: range ±9.2 × 10^18. Use for primary keys.

## Two's complement

First bit is the sign. For negatives, invert the rest and add 1. Consequence: signed integers have one more negative than positive. `Math.abs(Integer.MIN_VALUE)` returns `Integer.MIN_VALUE` (negative!) because there is no positive 2147483648.

## Hex encoding for hashes

SHA-256 produces 32 bytes. Hex-encoding doubles to 64 characters. BCrypt produces 60 chars. Argon2id produces ~100 chars. The project's `password_hash VARCHAR2(256)` column is generous.

## Common pitfalls

- Treating phone numbers, IDs, ZIP codes as integers → use `String`/`VARCHAR2`.
- Using `int` for primary keys → use `long`/`NUMBER(10)`.
- `Integer.parseInt("2147483648")` throws → use `Long.parseLong`.
- `0x10` is 16, `010` is 8 (legacy octal), `10` is 10.

## Project Connection

- `Integer.parseInt(phone_number)` — bug. International numbers exceed `Integer.MAX_VALUE` and contain `+`/spaces.
- `getInt("intern_id")` on `NUMBER(10)` — should be `getLong`.
- Hex-encoded SHA-256 in `VARCHAR2(256)` — sufficient length, but unsalted hashing itself is broken (see [[15 - Cryptography and Password Security/12 - Why Hashing ≠ Encryption]]).

## Further reading

- *Code: The Hidden Language of Computer Hardware and Software* (Petzold).
- JLS §4.2 (Primitive Types and Values).
