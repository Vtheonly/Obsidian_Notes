---
tags: [concept, refactoring, move-method, move-field]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/03 - Extract Class]]
  - [[04 - OOD and SOLID/09 - Feature Envy]]
---

# Move Method and Move Field

## What it is

**Move Method** moves a method from one class to another. **Move Field** moves a field. Use when behavior or data is in the wrong class.

## When to use

- **Feature Envy** — a method is more interested in another class than its own. Move it there.
- **Data Clumps** — the same group of fields appears in multiple classes. Extract a class and move the fields.
- **After Extract Class** — some methods may need to move to the new class.

## Steps

1. Identify the target class (where the method/field should live).
2. Create the method/field in the target.
3. Update the source to delegate (or remove if no longer needed).
4. Update callers.
5. Run tests.

## Example

```java
// Before: ReportService is envious of Intern
public class ReportService {
    public String generateInternReport(Intern intern) {
        return "Name: " + intern.getName() + "\n" +
               "Age: " + intern.getAge() + "\n" +
               "Email: " + intern.getEmail();
    }
}

// After: the report method lives on Intern
public class Intern {
    public String toReport() {
        return "Name: " + name + "\n" +
               "Age: " + age + "\n" +
               "Email: " + email;
    }
}

public class ReportService {
    public String generateInternReport(Intern intern) {
        return intern.toReport();  // delegate
    }
    // or just delete ReportService.generateInternReport and call intern.toReport() directly
}
```

## Common pitfalls

- **Moving too much** — moving all behavior to domain objects creates anemic services and fat domain objects. Balance.
- **Circular dependencies** — moving a method creates a cycle. Break the cycle first.

## Further reading

- *Refactoring* (Fowler), "Move Method" and "Move Field".
