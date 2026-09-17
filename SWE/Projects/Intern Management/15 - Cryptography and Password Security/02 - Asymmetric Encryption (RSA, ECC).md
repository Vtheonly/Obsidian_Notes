---
tags: [concept, cryptography, rsa, ecc, encryption]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/09 - Symmetric Encryption (AES)]]
---

# Asymmetric Encryption (RSA, ECC)

## What it is

**Asymmetric encryption** (public-key cryptography) uses two keys: a **public key** (shared with everyone) and a **private key** (kept secret). What one encrypts, the other decrypts.

## RSA (1977)

Based on the difficulty of factoring large numbers.
- Key sizes: 2048 bits (minimum), 4096 bits (recommended).
- Slow — used for key exchange, not bulk encryption.
- Used for: TLS certificates, SSH keys, digital signatures.

## ECC (Elliptic Curve Cryptography)

Based on the elliptic curve discrete logarithm problem.
- Key sizes: 256 bits (equivalent to 3072-bit RSA).
- Faster than RSA for the same security.
- Used for: TLS (ECDSA certificates), Bitcoin (secp256k1), Signal (X3DH).

## Ed25519

A specific elliptic curve (Edwards curve) for fast, secure signatures. Recommended for new applications.

## How asymmetric encryption is used

### Key exchange (TLS)
1. Client and server use RSA/ECDH to agree on a shared symmetric key.
2. They use AES with that key for bulk encryption.

Asymmetric encryption is slow; symmetric is fast. We use asymmetric to establish a symmetric key, then use symmetric for the actual data.

### Digital signatures
1. Alice hashes the document.
2. Alice encrypts the hash with her private key — that's the signature.
3. Bob verifies by decrypting the signature with Alice's public key and comparing to his own hash.

### Identity
1. Alice generates a key pair.
2. Alice shares her public key.
3. Anyone can encrypt a message to Alice using her public key; only Alice (with her private key) can decrypt.

## Project Connection

The project doesn't use asymmetric encryption. If it ever needs:
- **TLS** for DB connections (Oracle Net encryption).
- **JWT signing** for API tokens (RS256 or ES256).
- **SSH keys** for server access.

## Further reading

- *Understanding Cryptography* (Paar & Pelzl).
- NIST FIPS 186-5 (Digital Signature Standard).
