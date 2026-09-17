---
tags: [concept, security, threat-modeling, stride]
type: concept
status: complete
---

# Threat Modeling (STRIDE)

## What it is

**Threat modeling** is systematically identifying threats to a system. **STRIDE** (Microsoft) categorizes threats:

| Letter | Threat | Example |
|---|---|---|
| S | Spoofing | Attacker pretends to be another user |
| T | Tampering | Attacker modifies data in transit or at rest |
| R | Repudiation | User denies an action; no audit trail |
| I | Information disclosure | PII leaked |
| D | Denial of service | App made unavailable |
| E | Elevation of privilege | User gains admin access |

## Applying STRIDE to the project

### Spoofing
- Login accepts username + password hash sent to DB. No MFA. → Attacker can spoof if they steal the hash.
- No session management. → Anyone with the JAR can launch any FXML.

### Tampering
- No transactions. → Partial updates can corrupt data.
- No integrity checks on PDF output. → PDF could be modified.

### Repudiation
- No audit log. → User can deny changing an intern's status.

### Information disclosure
- Hardcoded `system/rootroot` credentials. → Anyone with repo access has DB credentials.
- Password hash displayed in update form. → Admin sees all hashes.
- `e.getMessage()` shown to users. → Internal DB structure leaked.
- No TLS on DB connection. → Passwords travel in plaintext.

### Denial of service
- No rate limiting. → Login can be hammered.
- `MAX(id)+1` race condition. → Concurrent inserts fail.

### Elevation of privilege
- Role checked once, never re-validated. → User can launch admin FXML directly.
- DB user is `system` (SYSDBA). → SQL injection = full DB compromise.

## The fix

Each threat has a corresponding control:
- Spoofing → MFA, session management.
- Tampering → transactions, integrity checks.
- Repudiation → audit log.
- Information disclosure → encryption, redaction, least privilege.
- Denial of service → rate limiting, connection pooling.
- Elevation of privilege → per-action authorization, least-privilege DB user.

## Further reading

- *Threat Modeling: Designing for Security* (Shostack).
- Microsoft STRIDE.
