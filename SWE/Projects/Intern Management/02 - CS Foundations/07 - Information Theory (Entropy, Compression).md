---
tags: [concept, cs-foundations, information-theory, compression]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/04 - Hash Functions (SHA family, BLAKE)]]
  - [[12 - Advanced Database Features/14 - Table Compression]]
---

# Information Theory (Entropy, Compression)

## What it is

Information theory, founded by Claude Shannon in 1948, quantifies information. The core concept is **entropy** — a measure of uncertainty or surprise in a random variable.

- A fair coin flip has 1 bit of entropy.
- A fair six-sided die roll has ~2.58 bits of entropy.
- An 8-character ASCII password (95 possible chars) has `log_2(95^8) ≈ 52.6` bits of entropy — *if* randomly generated.

## Why this matters for passwords

The project's `toolkit.generatePassword()` produces an 8-character password from ASCII 33–126 (94 characters). If random, that's `log_2(94^8) ≈ 52.4` bits of entropy. At 2.3 billion SHA-256 hashes/sec (RTX 4090), exhaustive search takes `2^52.4 / 2.3×10^9 ≈ 31 days`. With unsalted SHA-256 and a rainbow table, however, the entire password database falls in one pass — see [[15 - Cryptography and Password Security/07 - Rainbow Tables]].

NIST SP 800-63B recommends at least 128 bits of entropy for high-security applications. A 16-character random ASCII password has ~104 bits — still short of 128. A 20-character password has ~131 bits.

## Compression and entropy

Shannon's source coding theorem: data cannot be compressed below its entropy. A truly random 8-character password (52 bits of entropy) cannot be compressed — it's already maximally entropic.

This is why:
- Compressing already-encrypted data does nothing (ciphertext is high-entropy).
- Compressing database columns with low cardinality (e.g., `status` with 3 values) achieves high ratios (low entropy).
- Compressing unique IDs achieves nothing (high entropy).

Oracle's `ROW STORE COMPRESS ADVANCED` works by deduplicating repeated values within blocks — effective for low-entropy columns (status, department_id) and ineffective for high-entropy columns (UUIDs, hashes). See [[12 - Advanced Database Features/14 - Table Compression]].

## Hashing and entropy

A cryptographic hash function takes input of any size and produces a fixed-size output (e.g., SHA-256 produces 32 bytes). The output has high entropy — for a secure hash, the output is indistinguishable from random.

This is why hashing is one-way: the output has 256 bits of entropy regardless of input entropy, so the input is "lost" in the hash. There's no way to recover the input from the output (except by brute force).

## Common pitfalls

- Measuring password strength by length, not entropy. "Password1" is 9 chars but ~30 bits of entropy (dictionary words + simple suffix). "x7Q!mP2v" is 8 chars but ~52 bits.
- Assuming compression reduces storage by a fixed ratio. It depends on the data's entropy.
- Reusing a hash function as a checksum — use CRC32 or a cryptographic MAC (HMAC) depending on the threat model.

## Project Connection

- `toolkit.generatePassword()` produces 8 chars from ASCII 33–126 — ~52 bits of entropy if random. Too short for production. Recommend 16+ chars.
- Unsalted SHA-256 + low-entropy passwords = rainbow tables crack the database in one pass.
- Oracle's `ROW STORE COMPRESS ADVANCED` on `interns`, `departments`, `users`, `audit_logs` — effective because these tables have low-cardinality columns.

## Further reading

- *A Mathematical Theory of Communication* (Shannon, 1948).
- *The Code Book* (Singh).
- NIST SP 800-63B.
