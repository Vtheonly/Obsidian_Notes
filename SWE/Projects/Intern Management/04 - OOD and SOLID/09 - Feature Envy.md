---
tags: [concept, code-smell, feature-envy]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/03 - Code Smells Catalog]]
  - [[04 - OOD and SOLID/23 - Tell-Dont-Ask]]
---

# Feature Envy

## What it is

A method that is more interested in another class than its own. The method reaches into another object's data repeatedly, while barely using its own state.

## Example

```java
public class ReportService {
    public String generateInternReport(Intern intern) {
        return "Name: " + intern.getName() + "\n" +
               "Age: " + intern.getAge() + "\n" +
               "Email: " + intern.getEmail() + "\n" +
               "Status: " + intern.getStatus() + "\n" +
               "University: " + intern.getUniversity();
    }
}
```

`ReportService.generateInternReport` is envious of `Intern` — it accesses 5 of `Intern`'s getters. The report logic should probably live on `Intern` itself:

```java
public class Intern {
    public String toReport() {
        return "Name: " + name + "\n" + ... ;
    }
}
```

## Why it matters

- **Coupling** — `ReportService` is coupled to `Intern`'s internal structure. Change a field, and `ReportService` breaks.
- **Cohesion** — the report logic is more cohesive with `Intern` than with `ReportService`.
- **Testability** — testing the report requires a `ReportService` instance, but the logic only depends on `Intern`.

## When Feature Envy is OK

- **DTO assemblers** — a `InternDtoAssembler` that converts `Intern` to `InternDto` is naturally envious. That's its job.
- **Visitors** — the Visitor pattern intentionally puts behavior in a separate class.
- **Serializers** — converting an object to JSON/XML is naturally envious.

## The project's Feature Envy

`oracleConnector.searchIntern` returns `List<Map<String, Object>>`. The controller then:
- Iterates the list.
- For each map, calls `getNameById` to resolve `theme_id`.
- Calls `intern.toString()` to serialize.
- Calls `toolkit.formatString` to reformat.
- Builds a TitledPane with the data.

The controller is envious of the (non-existent) `Intern` class. The fix: introduce `Intern` with a `toDisplayString()` method (or use JavaFX properties for binding).

## Common pitfalls

- **Moving behavior to the wrong class** — sometimes the envious method belongs in a third class, not the envied one.
- **Anemic envied class** — if `Intern` has no behavior, all behavior is envious. Fix the anemia first.

## Further reading

- *Refactoring* (Fowler), "Feature Envy" smell.
