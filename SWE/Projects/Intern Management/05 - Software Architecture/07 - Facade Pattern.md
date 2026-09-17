---
tags: [concept, pattern, facade]
type: concept
status: complete
related:
  - [[06 - Design Patterns/00 - MOC - Design Patterns]]
  - [[05 - Software Architecture/16 - Service Layer Pattern]]
---

# Facade Pattern

> "Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use." — Gang of Four

## What it is

A **facade** is a simplified interface to a complex subsystem. It doesn't add functionality — it hides complexity.

```java
// Without facade: client must know 5 classes
public class Client {
    public void doWork() {
        OrderProcessor processor = new OrderProcessor();
        InventorySystem inventory = new InventorySystem();
        PaymentGateway gateway = new PaymentGateway();
        ShippingService shipping = new ShippingService();
        NotificationService notifier = new NotificationService();

        processor.validate(order);
        inventory.reserve(order.getItems());
        gateway.charge(order.getPayment());
        shipping.schedule(order);
        notifier.sendConfirmation(order);
    }
}

// With facade: client calls one method
public class OrderFacade {
    private final OrderProcessor processor;
    private final InventorySystem inventory;
    // ...

    public void placeOrder(Order order) {
        processor.validate(order);
        inventory.reserve(order.getItems());
        gateway.charge(order.getPayment());
        shipping.schedule(order);
        notifier.sendConfirmation(order);
    }
}

public class Client {
    private final OrderFacade facade;
    public void doWork() { facade.placeOrder(order); }
}
```

## Why it exists

- **Simplicity** — clients don't need to know the subsystem's internal structure.
- **Decoupling** — clients depend only on the facade, not on 5 subsystem classes.
- **Layered access** — the facade provides the "public API" of a subsystem.

## Facade vs Service Layer

The Service Layer pattern (Fowler) is essentially a facade for the business layer. The terms are often used interchangeably.

## Facade vs Adapter

- **Facade** — simplifies a complex subsystem (one-to-many).
- **Adapter** — converts one interface to another (one-to-one).

## Project Connection

The project has no facades. Controllers call `oracleConnector` directly, which exposes 30+ methods. The fix: introduce an `InternManagementFacade` (or per-entity services) that exposes the 5-10 use cases the UI actually needs.

## Common pitfalls

- **God facade** — one facade with 100 methods. Split into multiple facades.
- **Facade that adds functionality** — facades simplify, they don't add behavior. If you're adding logic, it's a service, not a facade.
- **Bypassing the facade** — clients that reach through to subsystem classes. Enforce the facade via package visibility.

## Further reading

- *Design Patterns* (GoF), Facade pattern.
