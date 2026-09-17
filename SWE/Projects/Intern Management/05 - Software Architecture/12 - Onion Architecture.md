---
tags: [concept, architecture, onion]
type: concept
status: complete
related:
  - [[05 - Software Architecture/02 - Clean Architecture (Uncle Bob)]]
  - [[05 - Software Architecture/08 - Hexagonal Architecture (Ports and Adapters)]]
---

# Onion Architecture

> "The center of the onion is the domain model. Surrounding it are domain services. Surrounding those are application services. The outermost layer is infrastructure: UI, DB, external services." — Jeffrey Palermo, 2008

## What it is

Onion Architecture (Palermo, 2008) is a layered architecture organized like an onion — concentric circles with the domain at the center. Dependencies point inward, like Clean Architecture.

```
┌─────────────────────────────────────┐
│  Infrastructure (UI, DB, External)  │
│  ┌─────────────────────────────┐    │
│  │  Application Services       │  │  Use cases
│  │  ┌─────────────────────┐    │  │
│  │  │  Domain Services     │    │  │ Domain rules
│  │  │  ┌─────────────┐     │    │  │
│  │  │  │  Domain     │     │    │  │ Entities, value objects
│  │  │  │  Model      │     │    │  │
│  │  │  └─────────────┘     │    │  │
│  │  └─────────────────────┘    │  │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## The four layers

1. **Domain Model** — entities, value objects, aggregates. Pure domain, no dependencies.
2. **Domain Services** — domain rules that don't fit on a single entity. Cross-entity coordination.
3. **Application Services** — use cases. Orchestrate domain services and repositories. Transaction boundaries.
4. **Infrastructure** — UI, DB, external APIs. Implements interfaces defined in inner layers.

## Differences from Clean Architecture

Onion and Clean Architecture are very similar. The main differences:
- Onion uses 4 layers; Clean uses 4 circles (Entities, Use Cases, Interface Adapters, Frameworks).
- Onion emphasizes "Domain Services" as a distinct layer; Clean folds them into Use Cases.
- Both follow the dependency rule (inner circles know nothing of outer).

## When to use Onion

- When the domain is complex enough to warrant a separate Domain Services layer.
- When you want a clear distinction between "enterprise business rules" (domain) and "application business rules" (use cases).

## Project Connection

The project has no layers at all. Either Clean or Onion would be a massive improvement. For a CRUD app like this, the simpler 3-layer (presentation / service / data) is usually sufficient — Clean/Onion are overkill.

## Further reading

- Palermo, "The Onion Architecture" series (jeffreypalermo.com, 2008).
