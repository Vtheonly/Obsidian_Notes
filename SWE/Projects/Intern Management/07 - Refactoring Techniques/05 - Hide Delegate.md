---
tags: [concept, refactoring, hide-delegate]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/13 - Law of Demeter]]
---

# Hide Delegate

## What it is

**Hide Delegate** fixes Law of Demeter violations by adding a delegating method to the intermediate object.

## When to use

- You see `a.getB().getC().doThing()` — a chain through multiple objects.
- The caller is reaching through an intermediate to get to a delegate.

## Example

```java
// Before: reaching through
String city = order.getCustomer().getAddress().getCity();

// After: hide the delegate
public class Order {
    public String getCustomerCity() {
        return customer.getCity();  // delegate
    }
}
public class Customer {
    public String getCity() {
        return address.getCity();  // delegate
    }
}

// Caller
String city = order.getCustomerCity();
```

The caller no longer knows that `Order` has a `Customer` which has an `Address`. The structure can change without breaking callers.

## Trade-offs

- **Pro** — encapsulation. The structure is hidden.
- **Con** — you might write many delegating methods. If the intermediate is just a thin wrapper, maybe the caller should know about it.

## Project Connection

The project's 5-level UI tree walk (`DeleteButton.getParent().getParent()...`) is the extreme Law of Demeter violation. The fix: store the `Intern` on the button's `userData`, access it directly.

## Further reading

- *Refactoring* (Fowler), "Hide Delegate".
