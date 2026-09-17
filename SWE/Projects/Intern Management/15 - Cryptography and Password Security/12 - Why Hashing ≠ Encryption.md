---
tags: [concept, cryptography, hashing, passwords]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/05 - Hashing vs Encryption]]
  - [[15 - Cryptography and Password Security/08 - Salt (and why it matters)]]
---

# Why Hashing ≠ Encryption (and why the project's SHA-256 is broken)

## The project's password storage

```java
// toolkit.hashIt
public static String hashIt(String input) {
    MessageDigest digest = MessageDigest.getInstance("SHA-256");
    byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
    return Base64.getEncoder().encodeToString(hash);
}
```

SHA-256 produces a 32-byte digest. The project stores this in `password_hash VARCHAR2(256)`. No salt. No key stretching.

## Why this is broken

### 1. SHA-256 is too fast
SHA-256 is designed for throughput — verifying file integrity, certificate signatures, etc. A single RTX 4090 GPU computes ~2.3 billion SHA-256 hashes per second.

An 8-character password (the project's `generatePassword` length) has ~6 × 10^13 combinations. At 2.3 billion/sec, exhaustive search takes ~26 seconds.

### 2. No salt
Identical passwords produce identical hashes. If 100 users have password "password123", all 100 have the same hash. An attacker who steals the DB can:
- Use a **rainbow table** (pre-computed hash → password map) to crack all 100 in one pass.
- See which users share a password (information leak).

### 3. The salt column exists but is unused
The schema has a `salt` column, but `toolkit.hashIt` never generates or uses a salt. The column is always NULL.

## What the project should do

Use **Argon2id** (OWASP 2023 recommendation):
- Memory-hard (resists GPU/ASIC attacks).
- Slow (configurable work factor).
- Built-in salt (auto-generated per password).
- Resistant to timing attacks.

```java
Argon2Advanced argon2 = Argon2Factory.createAdvanced(Argon2Types.ARGON2id);
String hash = argon2.hash(3, 65536, 4, password, salt);
boolean ok = argon2.verify(hash, inputPassword);
```

See [[15 - Cryptography and Password Security/01 - Argon2id]].

## Further reading

- OWASP Password Storage Cheat Sheet.
- *Real-World Cryptography* (Wong).
