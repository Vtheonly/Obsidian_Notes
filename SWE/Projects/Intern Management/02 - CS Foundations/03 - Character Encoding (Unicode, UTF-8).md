---
tags: [concept, cs-foundations, encoding, unicode]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/04 - Hash Functions (SHA family, BLAKE)]]
---

# Character Encoding (Unicode, UTF-8)

## What it is

Computers store bytes. Characters are an abstraction. An **encoding** is a mapping between characters and bytes.

- **ASCII** — 7-bit, 128 characters. English-only.
- **ISO-8859-1 (Latin-1)** — 8-bit, 256 characters. Western European.
- **UTF-16** — 16-bit per code unit (Java `String` internal representation). Variable length (1–2 code units per character).
- **UTF-8** — variable length (1–4 bytes per character). Backward-compatible with ASCII. The dominant encoding on the web.

**Unicode** is the abstract character set (over 1 million code points). UTF-8, UTF-16, UTF-32 are encodings of Unicode.

## Why this matters

Java `String` is internally UTF-16. When you call `getBytes()` without a charset, the platform default is used — which may be Windows-1252 on Windows, UTF-8 on Linux, MacRoman on old macOS. This is a portability bug.

```java
String s = "café";
byte[] b1 = s.getBytes();                       // platform-dependent!
byte[] b2 = s.getBytes(StandardCharsets.UTF_8); // explicit, portable
```

The project's `toolkit.hashIt` does:
```java
byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
```
This is correct — explicit UTF-8 charset. If it had used `input.getBytes()`, the same password would hash differently on Windows vs. Linux, breaking login when users switch machines.

## Common pitfalls

- `String.getBytes()` without charset — platform-dependent.
- Assuming `char` is one character — Unicode code points above U+FFFF (e.g., some emoji) take two Java `char`s (a surrogate pair).
- Storing UTF-8 in a `VARCHAR2` column without declaring character semantics — `VARCHAR2(100 BYTE)` may not hold 100 characters of multibyte text. Use `VARCHAR2(100 CHAR)`.
- Comparing strings with different Unicode normalization forms (NFC vs. NFD).

## Project Connection

- `toolkit.hashIt` uses `StandardCharsets.UTF_8` — correct.
- `toolkit.parseText` splits on `:` and `,` — does not handle Unicode normalization.
- The schema's `VARCHAR2(n CHAR)` in `insertion.sql` is correct. `requstes.sql` uses `VARCHAR2(255)` (byte semantics) — another inconsistency.

## Further reading

- *The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)* (Spolsky).
- Unicode Standard.
