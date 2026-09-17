---
tags: [concept, refactoring]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/22 - Technical Debt]]
  - [[04 - OOD and SOLID/03 - Code Smells Catalog]]
---

# What Is Refactoring?

> "Refactoring is the process of changing a software system in such a way that it does not alter the external behavior of the code yet improves its internal structure." — Martin Fowler, *Refactoring*, 1999

## What it is

**Refactoring** is the disciplined technique for improving the structure of existing code without changing its behavior. The key word is **disciplined** — small, behavior-preserving steps, with tests.

## The cycle

1. **Red** — write a failing test (or run existing tests to confirm current behavior).
2. **Green** — make the test pass.
3. **Refactor** — improve the structure while keeping tests green.

This is the Test-Driven Development (TDD) cycle. Refactoring without tests is "vandalizing" (Fowler).

## When to refactor

- **Rule of three** — the third time you write similar code, refactor.
- **When you add a feature** — refactor the surrounding code first.
- **When you fix a bug** — refactor the buggy code to make the bug class impossible.
- **During code review** — if you smell something, refactor.

## When NOT to refactor

- **Near a deadline** — refactoring at the last minute is risky.
- **When you don't have tests** — write characterization tests first.
- **When the code is being rewritten** — don't refactor code you're about to delete.

## The two hats

Fowler's metaphor: when developing, you wear one of two hats:
1. **Refactoring hat** — you change structure, not behavior. Tests must stay green.
2. **Adding-function hat** — you change behavior, not structure. Tests may go red.

Don't wear both hats at once. Refactor, then add the feature. Or add the feature, then refactor.

## Project Connection

The project needs massive refactoring. The reviews' Phase 0-4 roadmap is the refactoring plan:
- Phase 0: Hygiene (rename, delete dead code).
- Phase 1: Characterization tests.
- Phase 2: Architectural refactor (extract classes, introduce layers).
- Phase 3: UI/UX overhaul.
- Phase 4: Enterprise hardening.

## Further reading

- *Refactoring* (Fowler, 1999, 2nd ed. 2018).
- *Working Effectively with Legacy Code* (Feathers).
- *Refactoring to Patterns* (Kerievsky).
