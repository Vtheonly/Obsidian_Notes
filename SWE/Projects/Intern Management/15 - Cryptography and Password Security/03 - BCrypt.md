---
tags: [concept, cryptography, bcrypt, passwords]
type: concept
status: complete
prerequisites:
  - [[15 - Cryptography and Password Security/06 - Key Stretching (PBKDF2, BCrypt, SCrypt)]]
---

# BCrypt

## What it is

**BCrypt** is a password hashing function designed in 1999 by Niels Provos and David Mazières. It's based on the Blowfish cipher and is widely deployed.

## Why BCrypt

- **Adaptive** — the cost factor can be increased over time as hardware improves.
- **Salt is built-in** — auto-generated and embedded in the hash.
- **Slow** — by design, each hash takes ~100 ms (at cost 12).
- **Battle-tested** — 25 years of use.

## Hash format

```
$2a$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
```

- `$2a$` — algorithm identifier.
- `12` — cost factor (2^12 = 4096 iterations).
- `N9qo8uLOickgx2ZMRZoMyeIj` — 22-character Base64 salt (128 bits).
- `Agcfl7p92ldGxad68LJZdL17lhWy` — 31-character Base64 hash (184 bits).

The salt and hash are in one string. You store the entire string in `password_hash`.

## Java usage

```xml
<dependency>
    <groupId>org.mindrot</groupId>
    <artifactId>jbcrypt</artifactId>
    <version>0.4</version>
</dependency>
```

```java
import org.mindrot.jbcrypt.BCrypt;

// Hash
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));

// Verify
boolean ok = BCrypt.checkpw(candidatePassword, hash);
```

## Cost factor

- Cost 10 = 2^10 = 1024 iterations. ~50 ms.
- Cost 12 = 2^12 = 4096 iterations. ~200 ms. (OWASP minimum)
- Cost 14 = 2^14 = 16384 iterations. ~800 ms.

Increase the cost over time as hardware improves. To upgrade, re-hash on next login.

## Limitations

- **72-byte password limit** — BCrypt truncates passwords longer than 72 bytes. Pre-hash with SHA-256 if you need longer (but this loses some BCrypt properties).
- **Not memory-hard** — GPUs can parallelize BCrypt better than Argon2id.

## Project Connection

The project's unsalted SHA-256 can be replaced by BCrypt as a simpler alternative to Argon2id:

```java
public class BCryptPasswordEncoder implements PasswordEncoder {
    private static final int COST = 12;

    public String encode(String raw) {
        return BCrypt.hashpw(raw, BCrypt.gensalt(COST));
    }

    public boolean matches(String raw, String encoded) {
        return BCrypt.checkpw(raw, encoded);
    }
}
```

## Further reading

- Provos & Mazières, "A Future-Adaptable Password Scheme" (1999).
- OWASP Password Storage Cheat Sheet.
