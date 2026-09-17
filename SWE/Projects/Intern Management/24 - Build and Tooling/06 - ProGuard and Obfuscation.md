---
tags: [concept, build, proguard, obfuscation]
type: concept
status: complete
related:
  - [[17 - Application Security/10 - Security by Design vs Obscurity]]
---

# ProGuard and Obfuscation

## What it is

**ProGuard** shrinks, optimizes, and obfuscates Java bytecode. Class/method names become `a`, `b`, `c` — harder to reverse-engineer.

## Should you obfuscate?

### Arguments for
- **IP protection** — makes decompilation harder.
- **Smaller JAR** — removes unused code.

### Arguments against
- **Security by obscurity** — doesn't add real security. An attacker can still decompile; obfuscation just slows them down.
- **Debugging nightmare** — stack traces have `a.b.c()` instead of `com.example.InternService.save()`.
- **Reflection breaks** —FXML, JPA, serialization rely on names; obfuscation breaks them.
- **False sense of security** — the README's claim of "Obfuscation" is meaningless without real security.

## The project's claim

The README says "Reverse Engineering Protection (Obfuscation)" but there's no ProGuard config in `pom.xml`. The claim is false.

## Recommendation

**Don't obfuscate** unless you have a specific IP protection need. Focus on real security:
- Argon2id passwords.
- Least-privilege DB user.
- TLS.
- Input validation.
- Audit logging.

If you must obfuscate, use ProGuard with careful configuration to preserve FXML/JPA/reflection.

## Further reading

- ProGuard documentation.
