---
tags: [concept, cryptography, tls, https]
type: concept
status: complete
related:
  - [[15 - Cryptography and Password Security/09 - Symmetric Encryption (AES)]]
  - [[15 - Cryptography and Password Security/02 - Asymmetric Encryption (RSA, ECC)]]
---

# TLS and HTTPS

## What it is

**TLS** (Transport Layer Security) encrypts data in transit between client and server. **HTTPS** is HTTP over TLS.

## Why

- **Confidentiality** — an eavesdropper can't read the data.
- **Integrity** — an attacker can't modify the data undetected.
- **Authentication** — the client verifies the server's identity (via certificate).

## The TLS handshake (simplified)

1. **ClientHello** — client sends supported ciphers, TLS version, random.
2. **ServerHello** — server picks cipher, sends certificate, random.
3. **Key exchange** — client and server derive a shared secret (RSA or ECDH).
4. **Finished** — both sides switch to encrypted communication with the shared key.

## TLS 1.3 (2018)

- Simplified handshake (1 round-trip instead of 2).
- Removed weak algorithms (RSA key exchange, CBC mode, SHA-1).
- Mandatory forward secrecy (each session key is independent).
- Faster than TLS 1.2.

## Certificates

A **certificate** binds a public key to an identity (domain name). Issued by a **Certificate Authority (CA)**.
- **Let's Encrypt** — free, automated certificates.
- **Paid CAs** — DigiCert, Sectigo, etc.

Certificates contain:
- The public key.
- The domain name.
- The CA's signature.
- Validity period.

## Project Connection

The project's JDBC URL is `jdbc:oracle:thin:@localhost:1521:XE` — no TLS. The DB password travels in plaintext over the network (if the DB is remote). The fix: configure Oracle Native Network Encryption (ANE) or TLS:

```java
config.addDataSourceProperty("oracle.net.ssl_server_dn_match", "true");
config.addDataSourceProperty("oracle.net.ssl_version", "3.0");
// JDBC URL: jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST=...)(PORT=2484))...)
```

For a desktop app connecting to localhost, TLS is less critical (no network). But for any remote DB, it's essential.

## Further reading

- *Bulletproof TLS and PKI* (Ristic).
- Let's Encrypt documentation.
