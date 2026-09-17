---
tags: [concept, anti-pattern, big-ball-of-mud]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[04 - OOD and SOLID/10 - God Class (God Object)]]
---

# Big Ball of Mud

> "A Big Ball of Mud is a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle. ... These systems show unmistakable signs of never having been designed." — Brian Foote and Joseph Yoder, 1999

## What it is

A **Big Ball of Mud** is a system with no discernible architecture. Everything is connected to everything. There are no layers, no boundaries, no cohesion. Code is scattered, duplicated, and entangled.

## Symptoms

- Any class can call any other class.
- Business logic is in UI classes, UI code is in business classes, SQL is everywhere.
- "Where does this logic live?" has no good answer.
- Every change risks breaking something unrelated.
- New developers take weeks to make simple changes.

## Causes

- "Get it done yesterday" culture.
- No architectural review.
- High turnover (no one understands the whole system).
- Lack of design skills.
- "We'll clean it up later" (later never comes).

## The project as Big Ball of Mud

The project qualifies:
- `oracleConnector` is called from every controller, does everything.
- Controllers do UI + business logic + DB access + dialogs.
- No layers, no interfaces, no separation.
- "Where does intern creation logic live?" — scattered across `insertionInternController.insertInternController`, `oracleConnector.insertIntern`, `oracleConnector.getMaxId`, the FXML form, and `toolkit.hashIt` (for the password).

## The fix

You can't refactor a Big Ball of Mud in one shot. The strategy:
1. **Stop the bleeding** — establish boundaries for new code. New features follow layered architecture, even if old code doesn't.
2. **Strangler Fig pattern** — gradually replace old code with new, layered code. Each new feature replaces a chunk of the old mud.
3. **Characterization tests** — write tests that capture current behavior before refactoring.
4. **Incremental refactoring** — extract one class at a time. Run tests after each extraction.

See [[32 - Putting It All Together/00 - MOC - Rebuild]] for the specific roadmap.

## Common pitfalls

- **"We'll rewrite it from scratch"** — usually a mistake. The rewrite takes longer than expected, and the new system has new bugs. See Joel Spolsky's "Things You Should Never Do."
- **"We need to refactor everything before adding features"** — no. Refactor incrementally, alongside feature work.
- **Big-bang refactors** — touching 100 files in one PR. Break into small refactors with tests.

## Further reading

- Foote and Yoder, "Big Ball of Mud" (laputan.org, 1999).
- *Working Effectively with Legacy Code* (Feathers).
