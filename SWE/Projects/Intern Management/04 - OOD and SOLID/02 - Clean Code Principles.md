---
tags: [concept, clean-code, quality]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/03 - Code Smells Catalog]]
  - [[03 - Java Foundations/06 - Java Naming Conventions]]
---

# Clean Code Principles

> "Clean code is simple and direct. Clean code reads like well-written prose. Clean code never obscures the designer's intent but rather is full of crisp abstractions and straightforward lines of control." — Grady Booch

## The principles (Uncle Bob)

### 1. Meaningful names
- Use intention-revealing names. `d` is bad; `daysSinceCreation` is good.
- Avoid disinformation. Don't call something `accountList` if it's not a `List`.
- Make meaningful distinctions. `account1`, `account2` is not a distinction.
- Use pronounceable names. `genymdhms` is bad; `generationTimestamp` is good.
- Use searchable names. `5` is hard to search for; `MAX_RETRIES = 5` is easy.

### 2. Small functions
- Functions should be small. 20 lines is a guideline; 100 lines is too long.
- Do one thing. A function should do exactly what its name says, no more.
- One level of abstraction per function. Don't mix high-level orchestration with low-level details.
- Few arguments. 0 is ideal, 1-2 is fine, 3 is borderline, 4+ is usually bad.

### 3. Comments
- Comments don't compensate for bad code. Fix the code instead.
- Explain *why*, not *what*. The code already says what.
- Good comments: legal, informative, intent explanation, warning, TODO (with reason), amplification.
- Bad comments: redundant, misleading, mandated, noisy, position markers.

### 4. Formatting
- Vertical openness: separate concepts with blank lines.
- Vertical density: related lines should be close.
- Horizontal openness: space around operators.
- Indentation: consistent (4 spaces is Java convention).
- Team rules: formatting should be consistent across the codebase.

### 5. Error handling
- Use exceptions, not return codes.
- Don't return null. Don't pass null.
- Define exceptions based on caller needs.
- Don't ignore caught exceptions.

### 6. Classes
- Small. The first rule of classes is "small." The second rule is "smaller than that."
- Single Responsibility.
- Cohesion. Methods should use the class's fields.
- Dependencies on abstractions, not concretions.

## The project's violations

- Lowercase class names (`main`, `toolkit`, `oracleConnector`).
- 940-LOC `oracleConnector` class.
- 30+ catch blocks with `e.printStackTrace()`.
- Methods named after the class (`insertionInternController.insertInternController()`).
- Comments like `// TODO make a string to text-date`.
- `value == ""` — disinformative.
- `oracleConnector Connection = new oracleConnector();` — confusing (variable named after a class).
- `paramsMap` (SET values) and `paramsNext` (WHERE) — disinformative.

## Common pitfalls

- **"Clean code is slow"** — no. Clean code is often faster because it's easier to optimize.
- **"Clean code takes longer to write"** — initially yes, but it pays off in maintenance.
- **"I'll clean it up later"** — later never comes. Write clean code now.

## Project Connection

The project violates nearly every Clean Code principle. The refactoring roadmap (Phase 0 in the reviews) starts with naming and hygiene fixes.

## Further reading

- *Clean Code* (Martin) — the book.
- *The Clean Coder* (Martin) — professionalism.
- *Code Complete* (McConnell).
