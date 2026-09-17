---
tags: [concept, security, obscurity]
type: concept
status: complete
---

# Security by Design vs Obscurity

## Security by obscurity

Relying on the secrecy of the design/implementation for security. "If attackers don't know the algorithm, they can't break it."

Examples:
- Custom crypto algorithm (don't).
- Hidden admin URL (`/admin-secret-123`).
- Obfuscated code (ProGuard).
- Security through the attacker's ignorance.

## Why it fails

- **Kerckhoffs's principle** (1883): a cryptosystem should remain secure even if everything except the key is public.
- Attackers can reverse-engineer, leak, or guess the secret.
- Once the secret is out, security collapses.
- No peer review (custom crypto is untested).

## Security by design

Security comes from **sound design**, not secrecy:
- Use well-reviewed algorithms (AES, SHA-256, Argon2id).
- Use well-reviewed libraries (Bouncy Castle, jbcrypt).
- Assume the attacker has the source code.
- The secret is the key, not the algorithm.

## The project's claim

The README claims "Reverse Engineering Protection (Obfuscation)." But:
- No ProGuard/obfuscation config in `pom.xml`.
- Even with obfuscation, it's security by obscurity.
- The hardcoded `system/rootroot` is in the (decompilable) class file.

## The fix

Remove the "obfuscation" claim. Implement real security:
- Argon2id for passwords.
- Least-privilege DB user.
- TLS for DB connection.
- Input validation.
- Audit logging.

Security by design, not by obscurity.

## Further reading

- Kerckhoffs, "La cryptographie militaire" (1883).
- *Security Engineering* (Anderson).
