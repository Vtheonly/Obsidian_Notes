---
tags: [concept, code-smell, catalog]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/02 - Clean Code Principles]]
  - [[07 - Refactoring Techniques/00 - MOC - Refactoring]]
---

# Code Smells Catalog

> A **code smell** is a surface indication that there may be a deeper problem in the code. — Martin Fowler

Code smells are not bugs — they don't break the code. They're indicators that the code will be hard to maintain, extend, or understand.

## The catalog (Fowler, *Refactoring*)

### Bloaters (code that has grown too large)
1. **Long Method** — methods > 20-30 lines. Extract Method.
2. **Large Class** — classes > 200-300 LOC. Extract Class.
3. **Primitive Obsession** — using primitives instead of small objects. Replace Data Value with Object.
4. **Long Parameter List** — > 3-4 parameters. Introduce Parameter Object.
5. **Data Clumps** — the same group of fields passed together everywhere. Extract Class.

### Object-Oriented Abusers
6. **Switch Statements** — switch on type codes. Replace with Polymorphism.
7. **Temporary Field** — a field that's null most of the time. Extract Class or Introduce Null Object.
8. **Refused Bequest** — a subclass that doesn't want the parent's methods. Replace inheritance with composition.
9. **Alternative Classes with Different Interfaces** — two classes do the same thing with different method names. Rename.
10. **Data Class** — a class with only fields and getters/setters. Move behavior into the class.

### Change Preventers
11. **Divergent Change** — one class changes for many different reasons. Extract Class (SRP).
12. **Shotgun Surgery** — one change requires editing many classes. Move Method/Field to consolidate.
13. **Parallel Inheritance Hierarchies** — creating a subclass in one hierarchy forces creating one in another. Move Method/Field.

### Dispensables (things that could be removed)
14. **Comments** — comments that explain bad code. Fix the code.
15. **Duplicate Code** — same logic in multiple places. Extract Method.
16. **Lazy Class** — a class that does too little. Inline Class or delete.
17. **Data Class** — see above.
18. **Dead Code** — unused variables, methods, classes. Delete.
19. **Speculative Generality** — code "for the future" that's never used. Delete.

### Couplers
20. **Feature Envy** — a method more interested in another class. Move Method.
21. **Inappropriate Intimacy** — two classes that know too much about each other. Move Method, Extract Class.
22. **Message Chains** — `a.getB().getC().getD()`. Hide Delegate.
23. **Middle Man** — a class that just delegates to another. Remove Middle Man.
24. **Incomplete Library Class** — a library class that's missing a method you need. Introduce Foreign Method or Local Extension.

## The project's smells

- **Large Class** — `oracleConnector` (940 LOC), `insertionUserController` (444 LOC), `insertionInternController` (376 LOC).
- **Long Method** — `addToPool` (50+ lines), `searchIntern` (40+ lines).
- **Primitive Obsession** — `Map<String, Object>` everywhere.
- **Switch Statements** — `getIdByName` switch on table name.
- **Data Class** — there are no domain classes, but if there were, they'd be data classes.
- **Duplicate Code** — 4 copy-pasted CRUD methods per operation, 3 copy-pasted `addToXPool` methods, `DataPreprocessor` duplicate of `toolkit`.
- **Dead Code** — `DataPreprocessor.java`, `toolkit.isHashEqual`, dead schema tables, `worker_user_user` case, `PrintButton.setOnAction` commented, email tab Button with no onAction, Cancel buttons with no onAction, `startDatePicker` declared but not injected.
- **Speculative Generality** — 7 dead schema tables.
- **Feature Envy** — controllers envious of (non-existent) `Intern` class.
- **Message Chains** — the 5-level UI tree walk in `addToPool`.
- **Comments** — TODO comments throughout.
- **Inappropriate Intimacy** — controllers reach into `oracleConnector`'s static state.

## How to use this catalog

When reviewing code (yours or others'), scan for these smells. Each smell has a corresponding refactoring in [[07 - Refactoring Techniques/00 - MOC - Refactoring]].

## Further reading

- *Refactoring* (Fowler), Chapter 3 (Bad Smells in Code).
- refactoring.guru — interactive catalog.
