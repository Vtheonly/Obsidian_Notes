---
tags: [concept, cs-foundations, numbers, precision]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/08 - Oracle Data Types]]
---

# Floating Point and Numeric Precision

## What it is

Computers represent non-integer numbers using **floating-point** arithmetic (IEEE 754 standard). A float is stored as `sign × mantissa × 2^exponent`. This representation is *not exact* — most decimal fractions cannot be represented exactly in binary.

```java
System.out.println(0.1 + 0.2);    // 0.30000000000000004
```

This is not a Java bug — it's a fundamental property of binary floating-point. Every language that uses IEEE 754 (Python, JavaScript, C, C++, C#) has the same behavior.

## Why it matters

### Money
Never use `double` or `float` for money. Use `BigDecimal` (Java) or `DECIMAL`/`NUMBER(p,s)` (SQL). The project's schema uses `NUMBER(10)` for IDs and `NUMBER(3)` for age — both exact decimal types, no floating-point issues.

### Oracle NUMBER vs Java double
Oracle's `NUMBER` is a *decimal* type — it stores base-10 digits exactly. `NUMBER(10,2)` stores up to 10 digits with 2 after the decimal point. Java's `double` is binary floating-point. They are not interchangeable.

### Phone numbers
Phone numbers look numeric but are not — they:
- Can start with `+` (international prefix).
- Can contain spaces, dashes, parentheses.
- Can exceed `Integer.MAX_VALUE` (~2.1 billion; international phone numbers can reach 15 digits per E.164).
- Have no arithmetic meaning.

The project's `Integer.parseInt(phone_number)` is therefore a bug. Use `String`/`VARCHAR2`.

## IEEE 754 quick reference

| Type | Bits | Significant digits | Exponent range |
|---|---|---|---|
| `float` | 32 | ~7 | ±38 |
| `double` | 64 | ~15-17 | ±308 |
| `BigDecimal` | arbitrary | arbitrary | arbitrary |

## Special values

- `+0.0` and `-0.0` are distinct (compare equal with `==`, distinct with `Double.compare`).
- `NaN` (Not a Number) — result of `0.0/0.0`. `NaN != NaN` is true (the only value where `x != x`).
- `+Infinity` / `-Infinity` — result of `1.0/0.0`.

## Common pitfalls

- `0.1 + 0.2 != 0.3` — always use `BigDecimal` or compare with epsilon.
- `Math.abs(Integer.MIN_VALUE)` is negative — overflow.
- Storing money as `double` — rounding errors accumulate.
- `Integer.parseInt("+213770123456")` throws — phone numbers are not integers.

## Project Connection

- `Integer.parseInt(insert_intern_Age.getText())` — `age` is `NUMBER(3)`, range 0–999. `int` is fine here. But `Integer.parseInt(phone_number)` is wrong.
- `getInt("intern_id")` on `NUMBER(10)` — should be `getLong`.
- The schema uses `DATE` for `start_date` and `TIMESTAMP WITH LOCAL TIME ZONE` in the advanced redesign. See [[03 - Java Foundations/09 - Modern Date and Time API (java.time)]].

## Further reading

- *What Every Computer Scientist Should Know About Floating-Point Arithmetic* (Goldberg).
- IEEE 754 standard.
