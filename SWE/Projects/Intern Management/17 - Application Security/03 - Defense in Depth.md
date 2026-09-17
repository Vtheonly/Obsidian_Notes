---
tags: [concept, security, defense-in-depth]
type: concept
status: complete
---

# Defense in Depth

## What it is

**Defense in depth** is using multiple, independent layers of security. If one layer fails, others still protect.

## Layers

1. **Network** — firewall, VPN, network segmentation.
2. **Host** — OS hardening, antivirus, host firewall.
3. **Application** — input validation, auth, authz.
4. **Database** — least-privilege user, VPD, redaction.
5. **Data** — encryption at rest, encryption in transit.
6. **Monitoring** — logging, alerting, audit.
7. **Response** — incident response plan.

## Example

An attacker tries to read all interns' PII:
- Network firewall blocks the attacker's IP (layer 1).
- If they get through, the app requires login (layer 3).
- If they have an account, RBAC limits their access (layer 3).
- If they exploit a bug, VPD limits their query (layer 4).
- If they bypass VPD, redaction masks the phone (layer 4).
- If they get the data, encryption at rest prevents reading the disk (layer 5).
- If they decrypt, the audit log shows who accessed what (layer 6).

No single layer is sufficient. Each adds protection.

## Project Connection

The project has **zero layers**:
- No network security (localhost only).
- No host hardening.
- No input validation.
- No RBAC (role checked once).
- DB user is `system` (no least privilege).
- No encryption.
- No logging.
- No response plan.

The fix adds layers at each level.

## Further reading

- NIST SP 800-53 (Security Controls).
