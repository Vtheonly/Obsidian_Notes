---
tags: [concept, cryptography, timing-attacks, security]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/01 - Argon2id]]
---

# Timing Attacks and Constant-Time Comparison

## What it is

A **timing attack** measures how long an operation takes to deduce information about secret data. If comparing two strings takes longer when more characters match, an attacker can guess the secret character by character.

## The vulnerability

`String.equals()` compares character by character, returning false on the first mismatch:

```java
public boolean equals(Object o) {
    // ...
    for (int i = 0; i < length; i++) {
        if (this.charAt(i) != other.charAt(i)) return false;
    }
    return true;
}
```

If the first character matches, it takes slightly longer (one more comparison). An attacker measuring response time can:
1. Try all first characters. The one that takes longest is correct.
2. Try all second characters (with the correct first). The longest is correct.
3. Repeat until the full string is recovered.

For a 60-character BCrypt hash, this is 60 × 256 = 15,360 attempts — feasible.

## The fix: constant-time comparison

`MessageDigest.isEqual()` compares all characters regardless of mismatches:

```java
public static boolean isEqual(byte[] digesta, byte[] digestb) {
    if (digesta.length != digestb.length) return false;
    int result = 0;
    for (int i = 0; i < digesta.length; i++) {
        result |= digesta[i] ^ digestb[i];  // XOR; nonzero if different
    }
    return result == 0;
}
```

Every comparison takes the same time (proportional to length, not content).

## When to use

- **Password hash verification** — always.
- **API token verification** — always.
- **HMAC verification** — always.
- **General string comparison of secrets** — always.

## The project's bug

`toolkit.isHashEqual` uses `String.equals`:
```java
public static boolean isHashEqual(String hashed_pass, String Entered_hash) {
    return hashed_pass.equals(Entered_hash);
}
```

This is vulnerable to timing attacks. (It's also dead code — never called — but if it were, it would be vulnerable.)

## The fix

Use `MessageDigest.isEqual()`:
```java
public static boolean isHashEqual(byte[] expected, byte[] actual) {
    return MessageDigest.isEqual(expected, actual);
}
```

Or use BCrypt/Argon2id's built-in `verify()` — they handle comparison internally.

## Further reading

- CWE-208 (Observable Timing Discrepancy).
- *Cryptography Engineering* (Ferguson, Schneier, Kohno), Chapter 17.
