---
tags: [concept, cryptography, hashing, encryption]
type: concept
status: complete
---

# Hashing vs Encryption

## The fundamental distinction

| | Hashing | Encryption |
|---|---|---|
| Direction | One-way | Two-way |
| Reversible? | No | Yes (with the key) |
| Purpose | Integrity, verification | Confidentiality |
| Examples | SHA-256, BCrypt, Argon2id | AES, RSA |
| Same input, same output? | Yes (deterministic) | Depends on mode (IV, nonce) |

**Hashing** takes input and produces a fixed-size digest. You cannot recover the input from the digest.

**Encryption** takes input and a key, produces ciphertext. With the key, you can decrypt back to the input.

## When to use which

- **Passwords** → hashing (you should never be able to recover the password).
- **Credit card numbers** → encryption (you need to recover them for payments).
- **File integrity** → hashing (compare digests to detect changes).
- **Email content** → encryption (only the recipient should read it).
- **Digital signatures** → hashing + asymmetric encryption (hash the document, sign the hash).

## The project's confusion

The project calls SHA-256 a "hash" (correct) but stores the result in a column named `password_hash` (correct). The problem isn't the terminology — it's that **SHA-256 is the wrong hash for passwords**. SHA-256 is a *fast* hash designed for integrity verification, not a *slow* hash designed for password storage.

See [[15 - Cryptography and Password Security/12 - Why Hashing ≠ Encryption]] and [[15 - Cryptography and Password Security/06 - Key Stretching (PBKDF2, BCrypt, SCrypt)]].

## Further reading

- *Cryptography Engineering* (Ferguson, Schneier, Kohno).
- OWASP Cryptographic Storage Cheat Sheet.
