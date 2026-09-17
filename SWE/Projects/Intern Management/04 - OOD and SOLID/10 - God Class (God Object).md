---
tags: [concept, anti-pattern, god-class]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/19 - Single Responsibility Principle (SRP)]]
  - [[01 - Code Walkthrough/10 - oracleConnector java (the God Class)]]
---

# God Class (God Object)

## What it is

A **God Class** (or God Object) is a class that knows too much or does too much. It has many responsibilities, many fields, many methods, and is referenced from everywhere. It violates SRP spectacularly.

## Symptoms

- **Many fields** (> 10) — the class holds state for many concerns.
- **Many methods** (> 20) — the class does many things.
- **Many imports** — from unrelated packages.
- **High LOC** (> 500) — usually a sign of too much in one place.
- **High fan-in** — many other classes depend on it.
- **Low cohesion** — methods can be grouped into unrelated clusters.

## The project's `oracleConnector`

940 LOC, 30+ public methods, 6 distinct responsibilities:
1. Connection lifecycle.
2. Authentication.
3. CRUD for 4 entities.
4. SQL string construction.
5. UI feedback (`JOptionPane`).
6. ID generation.

Imports from `java.sql`, `javax.swing`, `java.time`, `java.util` — unrelated packages.

## Why God Classes are bad

- **Hard to understand** — no one can hold 940 LOC in their head.
- **Hard to change** — every change risks breaking something else in the class.
- **Hard to test** — to test one method, you need to set up the whole class.
- **Hard to extend** — adding a feature usually means editing the God Class.
- **High bug density** — bug density correlates with class size.

## The fix: extract

Split `oracleConnector` into:
- `ConnectionManager` (responsibility: pool lifecycle).
- `AuthService` (responsibility: authentication).
- `InternRepository`, `WorkerUserRepository`, `ThemeRepository`, `DepartmentRepository` (one per entity).
- `ExceptionTranslator` (responsibility: translate SQLException to business exceptions).

Each class is 80–150 LOC with one responsibility.

## Refactoring technique

Use Fowler's **Extract Class** refactoring:
1. Identify a cohesive cluster of methods and fields.
2. Create a new class.
3. Move the methods and fields to the new class.
4. Have the original class delegate to the new class.
5. Repeat until the original class is small.

See [[07 - Refactoring Techniques/00 - MOC - Refactoring]].

## Common pitfalls

- **"It's easier to just add one more method"** — yes, in the short term. In the long term, you have a 940-LOC monster.
- **"I'll split it later"** — later never comes. Split now.
- **Splitting too aggressively** — 50 tiny classes that always change together is also a smell. Find the natural boundaries.

## Project Connection

`oracleConnector` is the textbook God Class. The reviews identify splitting it as the #1 architectural fix.

## Further reading

- *Refactoring* (Fowler), "God Class" smell and "Extract Class" refactoring.
- *Clean Code* (Martin), Chapter 10 (Classes).
