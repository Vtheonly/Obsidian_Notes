---
tags: [concept, enterprise, multi-tenancy, saas]
type: concept
status: complete
---

# Multi-Tenancy

## What it is

**Multi-tenancy** is serving multiple customers (tenants) from one application instance, with data isolation.

## Strategies

### 1. Database per tenant
Each tenant has their own database.
- Pro: strongest isolation.
- Con: expensive (one DB per tenant), hard to scale.

### 2. Schema per tenant
One database, one schema per tenant.
- Pro: moderate isolation, cheaper.
- Con: schema migrations must run per tenant.

### 3. Discriminator column
One database, one schema, a `tenant_id` column on every table.
- Pro: cheapest, simplest.
- Con: weakest isolation (a bug in the WHERE clause leaks data.

Hibernate `@TenantId`:
```java
@Entity
public class Intern {
    @TenantId
    private String tenantId;
    // ...
}
```

Hibernate auto-adds `WHERE tenant_id = ?` to every query.

## When to use

- **SaaS apps** — multiple customers on one instance.
- **Cloud services** — cost-effective scaling.

## When NOT to use

- **Single-organization apps** — no need for tenancy.
- **Regulated** — some regulations require physical isolation.

## Project Connection

The intern app is single-tenant (one organization). Multi-tenancy is only relevant if it evolves to a SaaS where multiple organizations use the same instance.

## Further reading

- Hibernate multi-tenancy documentation.
