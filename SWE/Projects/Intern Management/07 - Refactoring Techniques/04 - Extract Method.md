---
tags: [concept, refactoring, extract-method]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
  - [[07 - Refactoring Techniques/03 - Extract Class]]
---

# Extract Method

## What it is

**Extract Method** is the refactoring that turns a piece of a long method into its own method, with a descriptive name.

## When to use

- A method is longer than 20-30 lines.
- A method has comments separating sections (the comment becomes the method name).
- A method does more than one thing.

## Steps

1. Identify a cohesive piece of code (a few lines that do one thing).
2. Create a new method with a descriptive name.
3. Move the code to the new method.
4. Pass any local variables as parameters.
5. Return any results.
6. Replace the original code with a call to the new method.
7. Run tests.

## Example

```java
// Before: 50-line method
public void processOrder(Order order) {
    // Validate
    if (order.getItems().isEmpty()) throw new ValidationException("Empty order");
    if (order.getCustomer() == null) throw new ValidationException("No customer");
    for (Item item : order.getItems()) {
        if (item.getQuantity() <= 0) throw new ValidationException("Bad quantity");
    }
    // Calculate total
    double total = 0;
    for (Item item : order.getItems()) {
        total += item.getPrice() * item.getQuantity();
    }
    order.setTotal(total);
    // Apply discount
    if (order.getCustomer().isVip()) {
        order.setTotal(total * 0.9);
    }
    // Save
    repository.save(order);
    // Notify
    emailService.sendConfirmation(order);
}

// After: 5 small methods
public void processOrder(Order order) {
    validate(order);
    calculateTotal(order);
    applyDiscount(order);
    save(order);
    notify(order);
}

private void validate(Order order) { ... }
private void calculateTotal(Order order) { ... }
private void applyDiscount(Order order) { ... }
private void save(Order order) { ... }
private void notify(Order order) { ... }
```

The original method now reads like a table of contents. Each step is self-documenting.

## Common pitfalls

- **Extracting too aggressively** — 1-2 line methods with cryptic names. Extract only when the name adds clarity.
- **Passing too many parameters** — if the extracted method needs 5 parameters, the method is in the wrong class. Consider Extract Class.
- **Naming** — the method name should describe *what*, not *how*. `calculateTotal` is good; `loopThroughItemsAndSum` is bad.

## Further reading

- *Refactoring* (Fowler), "Extract Method".
