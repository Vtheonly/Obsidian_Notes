---
tags: [pattern, behavioral, state]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/11 - State Machines]]
related:
  - [[06 - Design Patterns/17 - Strategy Pattern]]
  - [[03 - Java Foundations/05 - Java Enums]]
---

# State Pattern

> "Allow an object to alter its behavior when its internal state changes. The object will appear to change its class." — GoF

## What it is

The **State pattern** is the object-oriented implementation of a state machine. Each state is a class. The context object delegates to the current state.

```java
public interface InternState {
    void accept(InternContext ctx);
    void reject(InternContext ctx);
}

public class PendingState implements InternState {
    public void accept(InternContext ctx) {
        ctx.setState(new AcceptedState());
    }
    public void reject(InternContext ctx) {
        ctx.setState(new RejectedState());
    }
}

public class AcceptedState implements InternState {
    public void accept(InternContext ctx) {
        throw new IllegalStateException("Already accepted");
    }
    public void reject(InternContext ctx) {
        throw new IllegalStateException("Cannot reject after acceptance");
    }
}

public class InternContext {
    private InternState state = new PendingState();

    public void accept() { state.accept(this); }
    public void reject() { state.reject(this); }
    void setState(InternState s) { this.state = s; }
}
```

The `InternContext` delegates `accept()` and `reject()` to the current state. The state decides what to do (transition or throw).

## State vs enum

For simple state machines, an enum with a `switch` is often enough:

```java
public enum DecisionStatus {
    PENDING, ACCEPTED, REJECTED;

    public DecisionStatus accept() {
        return switch (this) {
            case PENDING -> ACCEPTED;
            case ACCEPTED -> throw new IllegalStateException("Already accepted");
            case REJECTED -> throw new IllegalStateException("Cannot accept after rejection");
        };
    }
}
```

Use the State pattern when:
- Each state has complex behavior (more than a transition).
- States share a lot of code (use a base class).
- You want to add states without modifying existing ones (OCP).

Use an enum when:
- States are simple (just a transition table).
- The set of states is closed.

## Project Connection

The project's `is_accepted` string field is a degenerate state machine. The fix: `DecisionStatus` enum (for simplicity) or `InternState` interface + state classes (for complex behavior).

The Database Resilience Engine uses a `ConnectionState` enum (CONNECTED, RECONNECTING, OFFLINE) — see [[29 - Resilience and Fault Tolerance/07 - State Pattern for Connection Recovery]].

## Common pitfalls

- **State explosion** — too many state classes. Consolidate if states share behavior.
- **Forgotten transitions** — some states don't handle some events. Decide: throw, ignore, or log.

## Further reading

- *Design Patterns* (GoF), State.
