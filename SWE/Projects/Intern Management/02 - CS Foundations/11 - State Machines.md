---
tags: [concept, cs-foundations, state-machines]
type: concept
status: complete
related:
  - [[21 - JavaFX Concurrency/05 - UI State Machine Pattern]]
  - [[29 - Resilience and Fault Tolerance/03 - Circuit Breaker Pattern]]
---

# State Machines

## What it is

A **state machine** (finite automaton) is a mathematical model of computation. It consists of:
- A finite set of **states**.
- A finite set of **inputs** (events).
- A **transition function** that maps (current state, input) → next state.
- An **initial state**.
- A set of **accepting states** (optional).

At any moment, the machine is in exactly one state. When an event arrives, the machine transitions to a new state.

## Why it exists

State machines model any system whose behavior depends on history. Examples:
- A turnstile (locked / unlocked; coin / push events).
- A TCP connection (CLOSED, SYN_SENT, ESTABLISHED, FIN_WAIT_1, ...).
- An order in an e-commerce site (cart, paid, shipped, delivered, returned).
- An intern's application status (Pending, Accepted, Rejected).
- A UI view (Loading, Empty, Error, Presenting).
- A circuit breaker (Closed, Open, Half-Open).

State machines make implicit state explicit. Instead of scattered `if (status.equals("Accepted"))` checks, you have a single transition table.

## Representations

1. **Transition table** — rows are states, columns are events, cells are next states.
2. **State diagram** — circles for states, arrows for transitions.
3. **Switch statement** — code: `switch(state) { case A: ... }`.
4. **State pattern** (GoF) — one class per state, polymorphic `handle(event)`.

## Common pitfalls

- **Implicit state** — using a string field with `if/else` chains. The state machine exists in the developer's head, not in the code.
- **Invalid transitions** — not guarding against transitions that shouldn't happen.
- **Forgotten states** — not handling the "Error" or "Cancelled" states.
- **Race conditions** — two threads changing state simultaneously without synchronization.

## Project Connection

The project's `intern.is_accepted` column is a state field with three values: `'Pending'`, `'Accepted'`, `'Rejected'`. But:

1. The schema defines a CHECK constraint allowing these three values.
2. The Java code inserts `'hold'` (lowercase, not in the list) — violating the constraint.
3. The display logic checks `case "Hold"` (capitalized, different from what's stored).
4. There is no enum; state is a magic string scattered across multiple files.
5. The transition rules are not enforced — there's no rule that says "you can't go from Rejected back to Pending."

The fix: define a `DecisionStatus` enum in Java, map it to the DB via a JPA converter or JDBC mapper, and document the legal transitions. See [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]].

The advanced UI redesign uses an explicit **UI State Machine** with four states (LOADING, EMPTY, ERROR, PRESENTING) — see [[21 - JavaFX Concurrency/05 - UI State Machine Pattern]].

The Database Resilience Engine uses a `ConnectionState` enum (CONNECTED, RECONNECTING, OFFLINE) — see [[29 - Resilience and Fault Tolerance/07 - State Pattern for Connection Recovery]].

## Further reading

- *Design Patterns* (GoF), State Pattern.
- *Domain-Driven Design* (Evans), on aggregates and invariants.
