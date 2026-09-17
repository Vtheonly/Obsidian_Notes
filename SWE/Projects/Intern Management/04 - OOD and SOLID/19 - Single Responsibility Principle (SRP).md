---
tags: [concept, solid, srp]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/10 - God Class (God Object)]]
  - [[05 - Software Architecture/15 - Separation of Concerns]]
---

# Single Responsibility Principle (SRP)

> "A class should have one, and only one, reason to change." — Robert C. Martin

## What it means

A class should have **one responsibility** — one reason to change. If a class has multiple responsibilities, those responsibilities become coupled: a change to one affects the others.

## The project's `oracleConnector` — 6 responsibilities

1. Connection lifecycle management.
2. Authentication queries (`login`, `isAdmin`, `isChief`).
3. CRUD for 4 entities.
4. SQL string construction.
5. UI feedback (`JOptionPane`).
6. ID generation (`getMaxId`).

**6 reasons to change `oracleConnector`:**
- Change the DB driver → edit `oracleConnector`.
- Change the auth logic → edit `oracleConnector`.
- Add a new entity → edit `oracleConnector`.
- Change the SQL building approach → edit `oracleConnector`.
- Change the UI feedback (e.g., replace JOptionPane with JavaFX Alert) → edit `oracleConnector`.
- Change the ID generation (e.g., use IDENTITY) → edit `oracleConnector`.

Every one of these changes risks breaking the others.

## The fix

Split into 6 classes:
- `ConnectionManager` (responsibility: pool lifecycle).
- `AuthService` (responsibility: authentication).
- `InternRepository`, `WorkerUserRepository`, etc. (responsibility: CRUD for one entity).
- (SQL construction is internal to each repository.)
- (UI feedback moves to controllers.)
- (ID generation moves to the DB via IDENTITY columns.)

## How to identify SRP violations

- A class with > 500 LOC is suspect.
- A class with > 10 public methods is suspect.
- A class whose methods can be grouped into unrelated clusters (auth, CRUD, SQL, UI) is suspect.
- A class that imports from unrelated packages (`java.sql`, `javax.swing`, `com.lowagie.text`) is suspect.

## Common pitfalls

- **Misunderstanding "responsibility"** — SRP is not "does one thing." It's "has one reason to change." A `UserController` may create, read, update, delete users — that's still one responsibility (user management).
- **Over-splitting** — splitting a cohesive class into many tiny classes that always change together. This is false decoupling.
- **Confusing SRP with "small classes"** — a class can be large and still have one responsibility (e.g., a complex algorithm).

## Project Connection

The project's `oracleConnector` (940 LOC, 6 responsibilities) is the textbook SRP violation. The reviews identify this as the #1 architectural problem.

See [[01 - Code Walkthrough/10 - oracleConnector java (the God Class)]] and [[05 - Software Architecture/17 - Smart UI Anti-Pattern]].

## Further reading

- *Clean Architecture* (Martin), Chapter 7 (SRP).
- *Agile Software Development, Principles, Patterns, and Practices* (Martin).
