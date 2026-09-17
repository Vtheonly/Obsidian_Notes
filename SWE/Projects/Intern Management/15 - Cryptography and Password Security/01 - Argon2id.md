---
tags: [concept, cryptography, argon2, passwords]
type: concept
status: complete
prerequisites:
  - [[15 - Cryptography and Password Security/06 - Key Stretching (PBKDF2, BCrypt, SCrypt)]]
---

# Argon2id

## What it is

**Argon2id** is the OWASP-recommended password hashing function (2023). It's the hybrid variant of Argon2 (the Password Hashing Competition winner, 2015).

## Why Argon2id

- **Memory-hard** — requires significant RAM (e.g., 64 MB per hash). This makes GPU/ASIC attacks expensive (GPUs have limited memory per core).
- **CPU-hard** — configurable iterations.
- **Side-channel resistant** — the "id" variant combines data-dependent (d) and data-independent (i) memory access, resisting timing attacks.
- **Built-in salt** — auto-generates and embeds the salt.

## Parameters (OWASP 2023)

- `m` (memory) = 65536 KB (64 MB)
- `t` (iterations) = 3
- `p` (parallelism) = 4

## Java usage

Add the dependency:
```xml
<dependency>
    <groupId>de.mkammerer</groupId>
    <artifactId>argon2-jvm</artifactId>
    <version>2.11</version>
</dependency>
```

```java
import de.mkammerer.argon2.Argon2;
import de.mkammerer.argon2.Argon2Factory;

Argon2 argon2 = Argon2Factory.create();

// Hash (auto-generates salt)
String hash = argon2.hash(3,        // iterations
                          65536,    // memory (KB)
                          4,        // parallelism
                          password.toCharArray());
// hash = "$argon2id$v=19$m=65536,t=3,p=4$<salt>$<digest>"

// Verify
boolean ok = argon2.verify(hash, candidatePassword.toCharArray());
```

The hash string contains the algorithm, parameters, salt, and digest. You store the entire string in `password_hash`.

## Why over BCrypt

- **Memory-hard** — BCrypt is not. GPUs can crack BCrypt faster than Argon2id.
- **Modern** — designed in 2015 (PHC), BCrypt is from 1999.
- **Side-channel resistant** — BCrypt has some timing sensitivity.

## Why some still use BCrypt

- **Wider deployment** — BCrypt is in more frameworks.
- **Simpler** — fewer parameters.
- **Proven** — 25 years of use.

Both are acceptable. OWASP prefers Argon2id; BCrypt is a close second.

## Project Connection

The project's unsalted SHA-256 is replaced by Argon2id:
```java
public class Argon2PasswordEncoder implements PasswordEncoder {
    private static final Argon2 ARGON2 = Argon2Factory.create();
    private static final int ITERATIONS = 3;
    private static final int MEMORY_KB = 65536;
    private static final int PARALLELISM = 4;

    public String encode(String rawPassword) {
        return ARGON2.hash(ITERATIONS, MEMORY_KB, PARALLELISM, rawPassword.toCharArray());
    }

    public boolean matches(String rawPassword, String encodedPassword) {
        return ARGON2.verify(encodedPassword, rawPassword.toCharArray());
    }
}
```

## Further reading

- Argon2 RFC 9106.
- OWASP Password Storage Cheat Sheet.
