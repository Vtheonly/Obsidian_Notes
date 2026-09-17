---
tags: [concept, principles, lod]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/23 - Tell-Dont-Ask]]
  - [[04 - OOD and SOLID/03 - Code Smells Catalog]]
---

# Law of Demeter

> "Only talk to your immediate friends, don't talk to strangers." — Karl Lieberherr

## What it means

A method `m` of an object `O` may only call methods of:
1. `O` itself.
2. Objects passed as parameters to `m`.
3. Objects created within `m`.
4. Direct component objects of `O`.

A method should **not** call methods on objects returned by other method calls (i.e., don't reach through to "strangers").

## Violations

```java
// Violation
String city = order.getCustomer().getAddress().getCity();

// Better
String city = order.getCustomerCity();  // order delegates to customer, customer delegates to address
```

```java
// Violation
session.getConnection().createStatement().executeQuery("...");

// Better
List<Intern> interns = internRepository.findByFilters(criteria);
```

## Why it matters

- **Coupling** — `order.getCustomer().getAddress().getCity()` couples the caller to the internal structure of `Order`, `Customer`, and `Address`. Change any of them, and the caller breaks.
- **Fragility** — if `getCustomer()` returns `null`, you get NPE three levels deep.
- **Testability** — to test the caller, you need to mock `Order`, `Customer`, and `Address`.

## The project's Law of Demeter violation

```java
// insertionInternController.addToPool — DeleteButton handler
labelText = ((Label) ((AnchorPane) ((VBox) ((HBox) DeleteButton.getParent()).getParent()).getChildren().get(0)).getChildren().get(0)).getText();
```

This is a 5-level chain through the scene graph:
- `DeleteButton.getParent()` → HBox
- `.getParent()` → VBox
- `.getChildren().get(0)` → AnchorPane
- `.getChildren().get(0)` → Label
- `.getText()` → String

If anyone adds a wrapper, reorders children, or replaces HBox with BorderPane, this throws `ClassCastException`.

## The fix

```java
// Set the Intern on the button's userData when creating it
DeleteButton.setUserData(intern);

// In the handler
DeleteButton.setOnAction(event -> {
    Intern intern = (Intern) event.getSource().getUserData();
    repository.delete(intern.getId());
});
```

No tree walking. No casts. The button knows its `Intern` directly.

## Common pitfalls

- **"Train wrecks"** — `a.getB().getC().getD()`. Refactor so `a` exposes the needed value directly.
- **Static call chains** — `oracleConnector.searchIntern(filters).get(0).get("name")`. Same problem.
- **Confusing with encapsulation** — Law of Demeter is about *reach-through*, encapsulation is about *hiding internals*. Related but distinct.

## Further reading

- *The Pragmatic Programmer* (Hunt & Thomas), "The Law of Demeter".
- Lieberherr, "Assuring Good Style for Object-Oriented Programs" (1989).
