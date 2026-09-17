---
tags: [concept, auth, mfa, 2fa, totp]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/03 - Brute Force Protection]]
---

# MFA and 2FA

## What it is

**Multi-Factor Authentication (MFA)** requires multiple independent factors:
1. **Something you know** — password.
2. **Something you have** — phone, security key, token.
3. **Something you are** — fingerprint, face, voice.

**2FA** is MFA with exactly two factors.

## TOTP (Time-based One-Time Password)

RFC 6238. The user's app (Google Authenticator, Authy) and the server share a secret. Both compute a 6-digit code that changes every 30 seconds.

```
Shared secret: JBSWY3DPEHPK3PXP
Current time: 2026-07-13T14:30:00Z
Time step: 30 sec, counter = 1770000
TOTP: 123456
```

The user enters the current code. The server computes the same code (using the shared secret and current time) and compares.

## HOTP (HMAC-based One-Time Password)

RFC 4222. Like TOTP, but the counter increments per use (not per time). Less common.

## WebAuthn / FIDO2

Hardware security keys (YubiKey, Touch ID, Windows Hello). The user taps the key instead of entering a code. More secure (phishing-resistant) and more convenient.

## SMS codes

A code texted to the user's phone. **Not recommended** — SIM swapping, SS7 vulnerabilities, interception.

## Implementation

### TOTP in Java
```xml
<dependency>
    <groupId>dev.samstevens.totp</groupId>
    <artifactId>totp</artifactId>
    <version>1.7.1</version>
</dependency>
```

```java
SecretGenerator generator = new DefaultSecretGenerator();
String secret = generator.generate();  // store per user

CodeGenerator codeGen = new DefaultCodeGenerator();
String code = codeGen.generate(secret, currentCounter);  // for display in QR code

CodeVerifier verifier = new DefaultCodeVerifier(codeGen, new SystemTimeProvider());
boolean valid = verifier.isValidCode(secret, userInputCode);
```

## Project Connection

The project has no MFA. For a desktop app, MFA is less critical (the "something you have" is the device). For a server app, MFA is essential for admin accounts.

## Further reading

- RFC 6238 (TOTP).
- WebAuthn specification (W3C).
