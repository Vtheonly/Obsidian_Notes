---
tags: [concept, ood, oop]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/08 - Encapsulation]]
  - [[04 - OOD and SOLID/05 - Composition over Inheritance]]
---

# The Four Pillars of OOP

## What it is

Object-oriented programming rests on four principles:

1. **Encapsulation** — bundle data with the methods that operate on it; hide internal state.
2. **Abstraction** — expose what an object does, hide how it does it.
3. **Inheritance** — derive new classes from existing ones, reusing code.
4. **Polymorphism** — treat objects of different classes uniformly via a common interface.

## Encapsulation

```java
public class BankAccount {
    private double balance;  // hidden
    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException();
        balance += amount;
    }
    public double getBalance() { return balance; }  // read-only access
}
```

The `balance` field is `private`. The only way to change it is `deposit()` (which validates). Callers cannot set `balance` directly.

## Abstraction

```java
public interface Account {
    void deposit(double amount);
    void withdraw(double amount);
    double getBalance();
}
```

`Account` exposes *what* an account can do, not *how* it does it. A `SavingsAccount` and `CheckingAccount` both implement `Account`, but their internals differ.

## Inheritance

```java
public class SavingsAccount extends Account {
    // inherits deposit, withdraw, getBalance
    // adds its own behavior: interest
    public void applyInterest(double rate) { ... }
}
```

Inheritance is for **is-a** relationships. `SavingsAccount` is an `Account`. Use **composition** for has-a relationships.

## Polymorphism

```java
List<Account> accounts = List.of(new SavingsAccount(), new CheckingAccount());
for (Account a : accounts) {
    a.deposit(100);  // calls the right deposit() for each type
}
```

The same `deposit(100)` call does different things depending on the actual type. This is polymorphism.

## Why OOP matters

- **Encapsulation** — protects invariants. Without it, any code can corrupt any state.
- **Abstraction** — manages complexity. You think in terms of `Account`, not `SavingsAccount_with_overdraft_protection_and_minimum_balance`.
- **Inheritance** — reuses code. (But see [[04 - OOD and SOLID/05 - Composition over Inheritance]].)
- **Polymorphism** — enables extensibility. Add a new `Account` subclass without changing the loop above.

## Common pitfalls

- **God classes** — one class does everything. Violates encapsulation and SRP.
- **Anemic domain model** — classes with only getters/setters, no behavior. Violates encapsulation.
- **Deep inheritance hierarchies** — fragile, hard to understand. Prefer composition.
- **Getter/setter everything** — exposes internal state. Encapsulation in name only.

## Project Connection

The project violates all four pillars:
- **Encapsulation** — `oracleConnector.connection` is `static` (one shared mutable field). `Map<String, Object>` exposes raw data with no invariants.
- **Abstraction** — no interfaces, no abstract classes. Every consumer is locked to `oracleConnector` (concrete class).
- **Inheritance** — no inheritance hierarchy at all. Only concrete classes.
- **Polymorphism** — no polymorphism. The 4 copy-pasted CRUD methods could be polymorphic via a `Repository<T, ID>` interface.

See [[04 - OOD and SOLID/01 - Anemic Domain Model]] and [[05 - Software Architecture/00 - MOC - Architecture]].
