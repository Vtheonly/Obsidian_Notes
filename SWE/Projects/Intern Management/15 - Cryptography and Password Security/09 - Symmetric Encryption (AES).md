---
tags: [concept, cryptography, aes, encryption]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/05 - Hashing vs Encryption]]
---

# Symmetric Encryption (AES)

## What it is

**Symmetric encryption** uses the same key to encrypt and decrypt. **AES** (Advanced Encryption Standard) is the standard symmetric cipher (replaced DES in 2001).

## AES variants

| Variant | Key size | Rounds |
|---|---|---|
| AES-128 | 128 bits | 10 |
| AES-192 | 192 bits | 12 |
| AES-256 | 256 bits | 14 |

AES-256 is recommended for most use cases.

## Modes of operation

### ECB (Electronic Codebook) — DON'T USE
Each block encrypted independently. Identical plaintext blocks produce identical ciphertext — leaks patterns.

### CBC (Cipher Block Chaining)
Each block XORed with the previous ciphertext block. Needs an IV (initialization vector). Vulnerable to padding oracle attacks if not used with HMAC.

### GCM (Galois/Counter Mode) — RECOMMENDED
Authenticated encryption — provides confidentiality + integrity. No padding needed. Parallelizable.

## Java usage (AES-GCM)

```java
SecretKey key = ...;  // 256-bit key
byte[] iv = new byte[12];  // 96-bit IV (GCM standard)
SecureRandom.getInstanceStrong().nextBytes(iv);

Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));
byte[] ciphertext = cipher.doFinal(plaintext.getBytes(UTF_8));

// Store iv + ciphertext together
byte[] combined = new byte[iv.length + ciphertext.length];
System.arraycopy(iv, 0, combined, 0, iv.length);
System.arraycopy(ciphertext, 0, combined, iv.length, ciphertext.length);
```

## When to use

- **Data at rest** — encrypt sensitive columns (credit card numbers, SSNs).
- **Data in transit** — TLS uses AES for bulk encryption.
- **File encryption** — encrypt backups.

## Key management

The hard part isn't the encryption — it's **key management**:
- Where do you store the key?
- How do you rotate it?
- Who has access?

Options:
- **Environment variables** — simple, but visible in process listing.
- **Secrets manager** — AWS Secrets Manager, HashiCorp Vault.
- **HSM** (Hardware Security Module) — dedicated hardware for key storage.
- **KMS** (Key Management Service) — AWS KMS, Azure Key Vault.

## Project Connection

The project doesn't encrypt sensitive data (passwords are hashed, which is correct; PII like phone/email is stored in plaintext). If encryption at rest is needed:
- Use Oracle TDE (Transparent Data Encryption) — encrypts the entire tablespace.
- Or encrypt specific columns in the app using AES-GCM.

## Further reading

- NIST FIPS 197 (AES standard).
- OWASP Cryptographic Storage Cheat Sheet.
