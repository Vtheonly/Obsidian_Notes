---
tags: [concept, refactoring, strangler-fig, legacy]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
  - [[05 - Software Architecture/01 - Big Ball of Mud]]
---

# Strangler Fig Pattern

> "The strangler fig pattern is a way of gradually replacing an existing system by building a new system around it, piece by piece, until the old system can be retired." — Martin Fowler, 2004

## What it is

Named after the strangler fig tree, which grows around a host tree and eventually replaces it, the **Strangler Fig pattern** is a strategy for gradually replacing legacy code:

1. Identify a piece of legacy functionality.
2. Build a new implementation alongside the legacy.
3. Route new requests to the new implementation; old requests still go to the legacy.
4. Gradually route more requests to the new, until the legacy is no longer used.
5. Delete the legacy.

## Why it exists

- **Big-bang rewrites fail** — they take too long, run over budget, and the new system has new bugs.
- **Strangler is incremental** — each piece is small and shippable.
- **You can stop anytime** — if the new system is "good enough," you stop. The legacy continues to work.

## Example

```java
// Legacy: oracleConnector.searchIntern (static, returns Map)
// New: InternService.search (instance, returns Intern)

// Facade routes between them
public class SearchFacade {
    private final InternService newService;
    private final oracleConnector legacy;

    public List<Intern> search(InternSearchCriteria criteria) {
        if (featureFlags.useNewSearch()) {
            return newService.search(criteria);  // new
        } else {
            return legacy.searchIntern(criteria.toMap()).stream()
                .map(Intern::fromMap)
                .collect(Collectors.toList());  // legacy
        }
    }
}
```

Use a feature flag to switch. Start with 0% new, gradually increase to 100%, then delete the legacy.

## Project Connection

The project's refactoring roadmap is a Strangler Fig:
- Phase 0: hygiene (no behavior change).
- Phase 1: characterization tests (lock in behavior).
- Phase 2: extract new layered code alongside the legacy `oracleConnector`.
- Phase 3: route controllers to the new services.
- Phase 4: delete `oracleConnector`.

## Common pitfalls

- **Never deleting the legacy** — the strangler grows but the host never dies. Plan the deletion.
- **Feature flags forever** — the flag becomes permanent technical debt. Set a sunset date.
- **Two systems diverge** — the new and legacy implement the same feature differently. Sync them or migrate fully.

## Further reading

- Fowler, "StranglerFigApplication" (martinfowler.com, 2004).
