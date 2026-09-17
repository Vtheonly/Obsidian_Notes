---
tags: [concept, cryptography, salt]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/07 - Rainbow Tables]]
  - [[15 - Cryptography and Password Security/12 - Why Hashing ≠ Encryption]]
---

# Salt (and why it matters)

## What it is

A **salt** is a random value added to a password before hashing. Each password gets its own unique salt.

```java
byte[] salt = new byte[16];
SecureRandom.getInstanceStrong().nextBytes(salt);
String hash = argon2.hash(password, salt);
// Store both hash and salt in the DB.
```

## Why

### 1. Defeats rainbow tables
A rainbow table is a pre-computed map of hash → password. Without salt, an attacker pre-computes a table once and cracks all passwords instantly.

With salt, each password has a unique hash. The attacker would need a separate rainbow table per salt — infeasible.

### 2. Hides identical passwords
Without salt, two users with password "password123" have the same hash. An attacker sees they share a password.

With salt, even identical passwords produce different hashes. No information leak.

### 3. Slows brute-force
Without salt, an attacker hashes "password123" once and checks all users. With salt, the attacker must re-hash per user (different salt).

## Salt requirements

- **Unique per password** — never reuse.
- **Random** — use `SecureRandom`, not `Math.random`.
- **Long enough** — 16 bytes (128 bits) minimum.
- **Stored with the hash** — the salt isn't secret; it just needs to be unique.

## The project's bug

The schema has a `salt` column but `toolkit.hashIt` never generates or uses a salt:

```java
public static String hashIt(String input) {
    MessageDigest digest = MessageDigest.getInstance("SHA-256");
    byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));  // no salt!
    return Base64.getEncoder().encodeToString(hash);
}
```

Every password is hashed identically. Rainbow tables crack the entire DB in one pass.

## The fix

BCrypt and Argon2id **auto-generate** the salt and embed it in the hash string:
```java
// BCrypt — salt is part of the hash
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));
// hash = "$2a$12$N9qo8uLOickgx2ZMRZoMy...salt+hash..."

// Argon2id — same
String hash = argon2.hash(3, 65536, 4, password);
// hash contains salt + parameters + digest
```

You store the entire string in `password_hash`. The salt is auto-extracted on verify.

## Further reading

- OWASP Password Storage Cheat Sheet.
