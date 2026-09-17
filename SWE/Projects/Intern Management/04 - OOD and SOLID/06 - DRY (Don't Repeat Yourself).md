---
tags: [concept, principles, dry]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/19 - Single Responsibility Principle (SRP)]]
  - [[07 - Refactoring Techniques/00 - MOC - Refactoring]]
---

# DRY (Don't Repeat Yourself)

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." — Hunt & Thomas, The Pragmatic Programmer

## What it means

Don't duplicate knowledge. If the same rule appears in two places, changing it requires updating both — and forgetting one creates a bug.

## The project's DRY violations

### 1. Four copy-pasted CRUD methods

`insertIntern`, `insertTheme`, `insertDepartment`, `insertWorkerUser` are 95% identical — only the table name and column list differ. ~600 lines that could be ~80 lines.

`searchIntern`, `searchTheme`, `searchDepartment`, `searchWorkerUser` — same.

`deleteIntern`, `deleteTheme`, `deleteDepartment`, `deleteWorkerUser` — same.

`updateInter`, `updateWorkerUser` — same.

### 2. `DataPreprocessor.preProcess` is a duplicate of `toolkit.preProcess`

Same logic, two classes. `DataPreprocessor` is dead code, but if someone "fixes" `toolkit.preProcess`, `DataPreprocessor` stays broken.

### 3. Three copy-pasted `addToXPool` methods

`addToWorkerUserPool`, `addToThemePool`, `addToDepartmentPool` in `insertionUserController`. Same structure, only the entity name differs.

## The fix

### Generic repository

```java
public interface Repository<T, ID> {
    void save(T entity);
    Optional<T> findById(ID id);
    List<T> findAll();
    void delete(ID id);
}

public abstract class AbstractJdbcRepository<T, ID> implements Repository<T, ID> {
    protected final DataSource dataSource;
    protected abstract String tableName();
    protected abstract T mapRow(ResultSet rs);
    protected abstract void setInsertParams(PreparedStatement ps, T entity);
    // shared save, findById, findAll, delete implementations
}
```

### Generic `addToPool`

```java
public <T> void addToPool(T entity, Function<T, String> formatter, Function<T, Node> actionsFactory) {
    // ...
}
```

## When DRY goes wrong

- **Premature DRY** — extracting "duplicate" code that happens to look similar but represents different business concepts. The two concepts will diverge, and the shared code will become a god function.
- **DRY across layers** — sharing the same `Intern` class between DB, service, and UI layers couples the layers. Use a DTO or view model in each layer.
- **Over-abstraction** — extracting a generic `AbstractJdbcRepository<T, ID>` before you have 3 entities is YAGNI. Wait until you see the pattern.

## Rule of three

A common heuristic: tolerate duplication once, extract on the second occurrence, definitely extract on the third. By the third time, the pattern is clear.

## Common pitfalls

- **Copy-paste with slight variations** — when you fix a bug in one copy, you forget the others.
- **Magic numbers** — the same constant (e.g., role ID 4) repeated across files. Extract to a named constant.
- **Validation logic repeated** — email validation in 5 controllers. Extract to a `Validator`.

## Project Connection

See above. The project is a DRY violation playground.

## Further reading

- *The Pragmatic Programmer* (Hunt & Thomas), Chapter 2 (DRY).
- *Refactoring* (Fowler), "Extract Method" and "Extract Class".
