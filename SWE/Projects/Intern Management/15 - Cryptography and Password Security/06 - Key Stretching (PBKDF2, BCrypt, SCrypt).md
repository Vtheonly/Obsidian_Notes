---
tags: [concept, cryptography, key-stretching]
type: concept
status: complete
prerequisites:
  - [[15 - Cryptography and Password Security/08 - Salt (and why it matters)]]
related:
  - [[15 - Cryptography and Password Security/01 - Argon2id]]
  - [[15 - Cryptography and Password Security/03 - BCrypt]]
---

# Key Stretching (PBKDF2, BCrypt, SCrypt)

## What it is

**Key stretching** is running a hash function many times (thousands to millions) to make each hash computation slow. This is the opposite of what SHA-256 optimizes for.

## Why

An attacker with a stolen hash DB tries billions of password guesses. With SHA-256, each guess takes nanoseconds. With a stretched hash, each guess takes milliseconds — 1000x to 1,000,000x slower for the attacker.

## The three main KDFs (Key Derivation Functions)

### PBKDF2 (Password-Based Key Derivation Function 2)
- RFC 2898 (2000).
- Runs HMAC-SHA256 (or SHA512) N times.
- N is typically 600,000+ (OWASP 2023).
- Widely supported (Java has it built-in).
- **Not memory-hard** — vulnerable to GPU/ASIC attacks.

### BCrypt (1999)
- Designed for passwords.
- Uses the Blowfish cipher as the hash.
- Cost factor (e.g., 12 = 2^12 iterations).
- **Not memory-hard** but slower than PBKDF2 on GPUs.
- Widely used (`org.mindrot:jbcrypt`).

### SCrypt (2009)
- Memory-hard (requires significant RAM).
- Resistant to GPU/ASIC attacks.
- Less widely deployed.

### Argon2 (2015, PHC winner)
- Memory-hard + CPU-hard.
- Argon2id (hybrid) is the OWASP recommendation.
- See [[15 - Cryptography and Password Security/01 - Argon2id]].

## Choosing parameters

OWASP 2023 recommendations:
- **Argon2id**: memory = 64 MB, iterations = 3, parallelism = 4.
- **BCrypt**: cost factor = 12 (or higher).
- **PBKDF2**: 600,000 iterations with SHA-256.

Tune so that a single hash takes ~250 ms on your server.

## Project Connection

The project uses plain SHA-256 (no stretching). The fix: Argon2id with the OWASP parameters, or BCrypt with cost 12.

## Further reading

- OWASP Password Storage Cheat Sheet.
- Argon2 specification (RFC 9106).
