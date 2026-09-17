---
tags: [concept, anti-pattern, smart-ui]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[05 - Software Architecture/15 - Separation of Concerns]]
  - [[04 - OOD and SOLID/20 - Smart UI Anti-Pattern]]
---

# Smart UI Anti-Pattern

> See [[04 - OOD and SOLID/20 - Smart UI Anti-Pattern]] for the full treatment. This note is a stub for the Architecture chapter's MOC.

## Summary

A Smart UI is a UI class that does everything: renders UI, handles events, validates, executes business logic, accesses the DB, shows dialogs. There is no separation of concerns.

The project's controllers are all Smart UIs. The fix: introduce layered architecture (presentation / service / data access).

## Why it's listed in the Architecture chapter

Smart UI is fundamentally an architectural choice — or rather, the absence of one. It's the default when you don't think about architecture. The fix is to choose a layered or Clean Architecture.
