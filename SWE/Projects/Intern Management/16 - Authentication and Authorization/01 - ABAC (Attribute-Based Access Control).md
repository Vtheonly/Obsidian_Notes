---
tags: [concept, auth, abac, authorization]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/09 - RBAC (Role-Based Access Control)]]
  - [[12 - Advanced Database Features/17 - Virtual Private Database (VPD)]]
---

# ABAC (Attribute-Based Access Control)

## What it is

**ABAC** grants permissions based on **attributes** of the user, the resource, and the environment. More fine-grained than RBAC.

```
Allow if:
  user.role == "chief"
  AND user.department_id == resource.department_id
  AND resource.status == "pending"
  AND environment.time.hour BETWEEN 9 AND 17
```

## Why

- **Fine-grained** — "a chief can accept interns in their own department, during business hours."
- **Dynamic** — permissions change based on context (time, location, resource state).
- **Composable** — combine user, resource, and environment attributes.

## RBAC vs ABAC

| | RBAC | ABAC |
|---|---|---|
| Granularity | Coarse (role → permissions) | Fine (attributes → permissions) |
| Simplicity | Simple | Complex |
| Flexibility | Static | Dynamic |
| Best for | Well-defined roles | Complex, context-dependent rules |

Most apps use **RBAC** for the basics and **ABAC** for special cases.

## Implementation

### Policy language
XACML (eXtensible Access Control Markup Language) is the standard, but it's verbose. Many apps use custom rules.

### Oracle VPD
Oracle's VPD (see [[12 - Advanced Database Features/17 - Virtual Private Database (VPD)]]) is essentially ABAC at the DB level — the policy function returns a predicate based on user attributes.

## Project Connection

The project's RBAC is too coarse. Adding ABAC would allow:
- "A chief can only accept interns in their own department."
- "A secretary can only edit interns they created."
- "No deletions after 30 days."

The advanced redesign's VPD implements ABAC: "standard users see only interns in their own department."

## Further reading

- NIST ABAC guide (SP 800-162).
