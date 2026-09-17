---
tags: [concept, cs-foundations, logic]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
---

# Boolean Logic

## What it is

The algebra of true/false values, formalized by George Boole in 1847. Operators: AND (∧), OR (∨), NOT (¬), XOR (⊕). Every `if` statement, every SQL `WHERE` clause, every digital circuit reduces to boolean logic.

## Laws

- **Identity:** `A ∧ true = A`, `A ∨ false = A`
- **Domination:** `A ∧ false = false`, `A ∨ true = true`
- **Idempotent:** `A ∧ A = A`, `A ∨ A = A`
- **Complement:** `A ∧ ¬A = false`, `A ∨ ¬A = true`
- **De Morgan's:** `¬(A ∧ B) = ¬A ∨ ¬B`, `¬(A ∨ B) = ¬A ∧ ¬B`
- **Double negation:** `¬¬A = A`

## Short-circuit evaluation

`A && B` evaluates `B` only if `A` is true. `A || B` evaluates `B` only if `A` is false. Essential for null-safety:

```java
if (user != null && user.isActive()) { ... }   // safe
```

## Why this matters for SQL

Every `WHERE` clause is a boolean expression. `WHERE 1=1` is `true` (identity law) — useful as a no-op starter for dynamic SQL builders (the project uses this in `searchDepartment`).

## Project Connection

- `WHERE 1=1` in `searchDepartment` — identity-law trick for dynamic WHERE. Not wrong, but the surrounding dynamic-SQL approach is fragile.
- `if (value == "" || value.isEmpty())` — short-circuit OR, but `value == ""` is reference equality (always false for runtime strings). The `isEmpty()` check is the real one. See [[03 - Java Foundations/13 - String comparison (== vs equals)]].

## Further reading

- *Code* (Petzold), Chapters 7–11.
