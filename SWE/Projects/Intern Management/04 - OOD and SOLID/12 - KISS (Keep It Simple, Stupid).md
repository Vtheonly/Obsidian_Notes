---
tags: [concept, principles, kiss]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/25 - YAGNI (You Aren't Gonna Need It)]]
  - [[04 - OOD and SOLID/06 - DRY (Don't Repeat Yourself)]]
---

# KISS (Keep It Simple, Stupid)

> "Keep it simple, stupid." — Kelly Johnson (Lockheed Skunk Works)

## What it means

Simplicity is a virtue. The simplest solution that works is usually the best. Don't add complexity unless it's justified.

## The project's KISS violations

### String serialization of records

```java
// Controller does:
intern.toString()  →  "{name=Alice, age=22, ...}"
// displayed in Label
// later parsed back via toolkit.parseText by splitting on ":" and ","
```

This is far more complex than holding a typed `Intern` object in the controller. The string round-trip adds:
- A serialization step (ambiguous, lossy).
- A parser (fragile, no error handling).
- Coupling between DB and UI layout.

The simple solution: hold `Intern` objects in a `TableView<Intern>`. Click a row → you have the `Intern`. No serialization, no parsing.

### Dynamic SQL by HashMap iteration

```java
StringBuilder columns = new StringBuilder();
for (String key : internData.keySet()) {
    columns.append(key).append(", ");
}
// ... build INSERT with dynamic columns
```

This is more complex than a hardcoded SQL string:
```java
String sql = "INSERT INTO interns (name, age, email, ...) VALUES (?, ?, ?, ...)";
```

The dynamic approach is "clever" but fragile (HashMap order, SQL injection if keys come from user input, no compile-time check). The hardcoded approach is "dumb" but reliable.

### UI tree walking

```java
((Label) ((AnchorPane) ((VBox) ((HBox) DeleteButton.getParent()).getParent()).getChildren().get(0)).getChildren().get(0)).getText()
```

Five chained casts. The simple solution: `deleteButton.setUserData(intern)` then `(Intern) event.getSource().getUserData()`.

## When to add complexity

- **Performance** — a simple O(n²) algorithm is fine for n=10. For n=1,000,000, you need O(n log n).
- **Security** — Argon2id is more complex than SHA-256, but the complexity is justified.
- **Extensibility** — if you genuinely need to swap implementations, an interface adds justified complexity.

But the default is simple. Add complexity only when the simple solution demonstrably fails.

## Common pitfalls

- **"Clever" code** — clever is a code smell. Readable beats clever.
- **Premature optimization** — "I'll need this to be fast" → write complex code. Measure first.
- **Over-engineering** — "What if we need to support 5 database engines?" → write abstraction layers. You won't.
- **Pattern obsession** — "I read about the Visitor pattern, let me use it." Use patterns when they fit, not because they exist.

## Project Connection

The project's string serialization, dynamic SQL, and UI tree walking are all KISS violations. The fixes are simpler than the original code.

## Further reading

- *The Pragmatic Programmer* (Hunt & Thomas).
- *The Mythical Man-Month* (Brooks), "The Second-System Effect".
