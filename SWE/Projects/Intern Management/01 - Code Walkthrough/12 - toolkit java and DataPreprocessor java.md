---
tags: [case-study, code-walkthrough, security, hashing]
type: case-study
status: complete
related:
  - "[[15 - Cryptography and Password Security/12 - Why Hashing ≠ Encryption]]"
  - "[[04 - OOD and SOLID/01 - Anemic Domain Model]]"
---

# toolkit.java and DataPreprocessor.java

## toolkit.java (160 lines) — static utilities

### `hashIt` — unsalted SHA-256

```java
public static String hashIt(String input) {
    try {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hash);
    } catch (NoSuchAlgorithmException e) {
        throw new RuntimeException(e);
    }
}
```

#### What's wrong
1. **SHA-256 is a fast hash** — designed for throughput, not password storage. A single RTX 4090 computes ~2.3 billion SHA-256 hashes/sec.
2. **No salt** — identical passwords produce identical hashes. Rainbow tables crack the entire password database in one pass. See [[15 - Cryptography and Password Security/07 - Rainbow Tables]].
3. **Base64 encoding** — fine for transport, but the `salt` column in the DB is never populated. The schema has the column; the code ignores it.
4. **`RuntimeException` wrapping** — `NoSuchAlgorithmException` is impossible for "SHA-256" (it's mandatory in every JDK). Wrapping it as `RuntimeException` is acceptable but signals the author didn't understand checked exceptions.

#### Fix
Replace with **Argon2id** (OWASP 2023 recommendation):
```java
Argon2Advanced argon2 = Argon2Factory.createAdvanced(Argon2Types.ARGON2id);
String hash = argon2.hash(iterations=3, memoryKB=65536, parallelism=4, password, salt);
boolean ok = argon2.verify(hash, inputPassword);
```
See [[15 - Cryptography and Password Security/01 - Argon2id]].

### `generatePassword` — 8-char ASCII

```java
private static final SecureRandom RANDOM = new SecureRandom();
private static final int PASSWORD_LENGTH = 8;
private static final int ASCII_START = 33;
private static final int ASCII_END = 126;

public static String generatePassword() {
    StringBuilder sb = new StringBuilder(PASSWORD_LENGTH);
    for (int i = 0; i < PASSWORD_LENGTH; i++) {
        int randomAscii = ASCII_START + RANDOM.nextInt(ASCII_END - ASCII_START + 1);
        sb.append((char) randomAscii);
    }
    return sb.toString();
}
```

#### What's wrong
1. **8 characters is too short** — ~52 bits of entropy. With unsalted SHA-256, rainbow tables crack it instantly. With Argon2id, exhaustive search takes ~31 days on one GPU. NIST recommends 128 bits.
2. **ASCII 33–126 includes ambiguous characters** — `O` vs `0`, `l` vs `1`, `I` vs `l`. Users will mistype.
3. **No character class requirements** — may produce all-punctuation passwords.
4. **Magic numbers** — 33, 126, 8 are unexplained.

#### Fix
- 16+ characters.
- Use a password-strength estimator (zxcvbn) to reject weak passwords.
- Avoid ambiguous characters.
- Recommend a passphrase (4-5 random words) — higher entropy, easier to remember.

### `parseText` — string surgery to recover a Map

```java
public static Map<String, String> parseText(String text) {
    Map<String, String> map = new HashMap<>();
    String[] lines = text.split("\n");
    for (String line : lines) {
        String[] parts = line.split(":", 2);
        if (parts.length == 2) {
            String key = parts[0].trim();
            String value = parts[1].trim();
            if (value.endsWith(",")) value = value.substring(0, value.length() - 1);
            map.put(key, value);
        }
    }
    return map;
}
```

#### What's wrong
1. **Round-tripping through strings** — the controller does `intern.toString()` (which calls `Map.toString()` → `"{key=value, key=value}"`), displays it in a Label, then `parseText` parses it back to a Map. This is the [[04 - OOD and SOLID/01 - Anemic Domain Model|Anemic Domain Model]] anti-pattern taken to its extreme.
2. **Fragile parsing** — any value containing `:` or `, ` breaks the parser. An intern named "Smith, John" or an email with a comma breaks the delete query.
3. **No error handling** — malformed input produces a partial map silently.
4. **Couples database to UI layout** — if you change the Label's text format, the parser breaks.

#### Fix
Hold typed `Intern` objects in the controller. When a row is clicked, pass the typed `Intern` to the handler — never a string. The `formatString`/`parseText` methods can be deleted entirely.

### `isHashEqual` — dead and buggy

```java
public static boolean isHashEqual(String hashed_pass, String Entered_hash) {
    return hashed_pass.equals(Entered_hash);
}
```

#### What's wrong
1. **Dead code** — never called anywhere.
2. **`String.equals` is not constant-time** — vulnerable to timing attacks. An attacker measuring response time can deduce the hash byte-by-byte.
3. **Wrong parameter names** — `hashed_pass` and `Entered_hash` suggest comparing a stored hash to a user-entered hash. But the correct flow is: re-hash the entered password with the stored salt, then compare. This method doesn't do that.

#### Fix
Use `MessageDigest.isEqual()` (constant-time). Better: use Argon2id's `verify()` method which handles comparison internally.

## DataPreprocessor.java (125 lines) — dead duplicate

The entire class is a copy-paste of `toolkit.preProcess` with a `main()` test harness using Java text blocks. It is never referenced by any other class.

### What's wrong
1. **DRY violation** — two copies of the same logic in the same package.
2. **`main()` as test harness** — should be a JUnit test in `src/test/java/`.
3. **Dead code** — future maintainers won't know which is canonical.

### Fix
Delete `DataPreprocessor.java`. Move its `main()` test harness to a proper JUnit test in `src/test/java/`. See [[27 - Testing/00 - MOC - Testing]].
