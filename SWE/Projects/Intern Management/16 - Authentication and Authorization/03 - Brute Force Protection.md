---
tags: [concept, security, brute-force, rate-limiting]
type: concept
status: complete
related:
  - [[29 - Resilience and Fault Tolerance/01 - Bucket4j]]
  - [[16 - Authentication and Authorization/07 - Password Reset Flows]]
---

# Brute Force Protection

## What it is

Preventing attackers from guessing passwords by trying thousands of combinations.

## Techniques

### 1. Account lockout
After N failed attempts, lock the account for a period.
```
Failed attempt 1, 2, 3, 4 → allow.
Failed attempt 5 → lock for 5 minutes.
Failed attempt 6 (after unlock) → lock for 10 minutes.
Failed attempt 7 → lock for 30 minutes.
```
Risk: **denial-of-service** — an attacker can lock out users by trying their username.

### 2. Exponential backoff
Each failed attempt increases the wait time.
```
Attempt 1: immediate.
Attempt 2: wait 1 sec.
Attempt 3: wait 2 sec.
Attempt 4: wait 4 sec.
Attempt 5: wait 8 sec.
...
```

### 3. CAPTCHA
After N failures, require a CAPTCHA. Stops automated attacks.

### 4. Rate limiting (per IP)
Limit the number of login attempts per IP per minute.
```
IP 1.2.3.4: 5 attempts/min, 20/hour.
```
Use **Bucket4j** or **Resilience4j RateLimiter**.

### 5. Rate limiting (per username)
Limit per username, regardless of IP. Stops distributed attacks on one user.

### 6. Multi-factor authentication
Even if the password is guessed, the attacker needs the second factor.

### 7. Password strength
Strong passwords are harder to brute-force. See [[02 - CS Foundations/07 - Information Theory (Entropy, Compression)]].

## The project's vulnerability

The project has **no brute-force protection**. An attacker can hammer login with thousands of guesses per second.

## The fix

Combine multiple techniques:
1. **Account lockout** after 5 failures, with exponential backoff.
2. **Rate limiting** per IP (Bucket4j: 5/min).
3. **CAPTCHA** after 3 failures (optional).
4. **Audit log** of all login attempts (success and failure).
5. **MFA** for admin accounts (optional).

```java
public AuthResult authenticate(String username, char[] password) {
    if (rateLimiter.tryConsume(username)) {
        Optional<User> user = users.findByUsername(username);
        if (user.isPresent() && passwordEncoder.matches(password, user.get().getPasswordHash())) {
            lockoutCounter.reset(username);
            return AuthResult.success(user.get());
        }
    }
    int failures = lockoutCounter.increment(username);
    if (failures >= 5) {
        lockout.lock(username, Duration.ofMinutes(5 * (failures - 4)));
    }
    return AuthResult.failure();
}
```

## Further reading

- OWASP Authentication Cheat Sheet — Account Lockout.
- NIST SP 800-63B §5.2.2.
