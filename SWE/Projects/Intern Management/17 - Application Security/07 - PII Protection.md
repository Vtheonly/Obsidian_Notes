---
tags: [concept, security, pii, gdpr]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/02 - Data Redaction (DBMS_REDACT)]]
  - [[14 - Schema Evolution/01 - Audit Columns]]
---

# PII Protection

## What is PII?

**PII** (Personally Identifiable Information) is data that can identify a person: name, email, phone, address, SSN, IP address, biometrics.

## Regulations

- **GDPR** (EU) — strict rules on PII processing, retention, deletion.
- **CCPA** (California) — similar to GDPR.
- **HIPAA** (US healthcare) — medical data.
- **PCI DSS** — credit card data.

## Principles

### Data minimization
Collect only what you need. Don't store "just in case."

### Purpose limitation
Use PII only for the stated purpose. Don't reuse marketing data for analytics without consent.

### Storage limitation
Retain PII only as long as needed. Delete (or anonymize) after.

### Access control
Only authorized users can access PII. Use RBAC/ABAC.

### Encryption
Encrypt PII at rest (TDE, column encryption) and in transit (TLS).

### Masking/redaction
Mask PII in non-prod environments. Redact PII for users who don't need it (see [[12 - Advanced Database Features/02 - Data Redaction (DBMS_REDACT)]]).

### Audit
Log every access to PII. "Who viewed this user's phone number?"

## The project's PII

The project stores:
- Name, email, phone, university, age of interns.
- Username, email, phone, password hash of users.

None of it is encrypted at rest. None of it is redacted. Any user with DB access sees all PII. The password hash is displayed in the update form.

## The fix

1. **Encrypt at rest** — Oracle TDE on the tablespace, or column-level encryption.
2. **Redact in non-prod** — mask phone/email in dev/test DBs.
3. **Audit access** — log every SELECT on PII columns.
4. **Minimize** — don't collect data you don't need (e.g., do you really need phone?).
5. **Retain** — define retention periods; auto-delete after.
6. **Subject access requests** — support GDPR "export my data" and "delete my data" requests.

## Further reading

- GDPR (gdpr.eu).
- OWASP Privacy Risks.
