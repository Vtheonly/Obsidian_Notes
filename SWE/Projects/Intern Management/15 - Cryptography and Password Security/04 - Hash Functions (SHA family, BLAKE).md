---
tags: [concept, cryptography, hash-functions]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/05 - Hashing vs Encryption]]
---

# Hash Functions (SHA family, BLAKE)

## What it is

A **cryptographic hash function** takes input of any size and produces a fixed-size digest. Properties:
- **Deterministic** — same input always produces same output.
- **Fast to compute** — O(n) in input size.
- **One-way** — infeasible to recover input from output.
- **Collision-resistant** — infeasible to find two inputs with the same output.
- **Avalanche** — small change in input → completely different output.

## The SHA family

| Algorithm | Output size | Status |
|---|---|---|
| MD5 | 128 bits | Broken — don't use |
| SHA-1 | 160 bits | Broken — don't use |
| SHA-256 | 256 bits | Secure |
| SHA-384 | 384 bits | Secure |
| SHA-512 | 512 bits | Secure |
| SHA-3 | 224-512 bits | Secure (different design) |
| BLAKE2 / BLAKE3 | variable | Secure, faster than SHA |

## When to use which

- **File integrity** — SHA-256 or BLAKE3.
- **Digital signatures** — SHA-256 or SHA-384.
- **Password storage** — **NOT SHA-256**. Use BCrypt, Argon2id, or PBKDF2 (slow hashes).
- **HMAC** (keyed hash) — SHA-256.

## SHA-256 in Java

```java
MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] hash = digest.digest("hello".getBytes(StandardCharsets.UTF_8));
String hex = HexFormat.of().formatHex(hash);
// hex = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
```

## Why SHA-256 is wrong for passwords

SHA-256 is designed to be **fast**. For password storage, you want **slow**. A fast hash means an attacker can try billions of passwords per second. A slow hash means millions of attempts per second — 1000x harder to brute-force.

See [[15 - Cryptography and Password Security/06 - Key Stretching (PBKDF2, BCrypt, SCrypt)]].

## Project Connection

The project uses SHA-256 (fast hash) for passwords. Wrong tool. The fix: Argon2id (slow hash, memory-hard).

## Further reading

- NIST FIPS 180-4 (SHA-2 standard).
- NIST FIPS 202 (SHA-3 standard).
