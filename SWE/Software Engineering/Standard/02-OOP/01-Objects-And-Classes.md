# Objects and Classes — The First Concrete Artifact

> Objects and classes are the first concrete thing you produce when you move from responsibility assignments to code. This chapter clarifies the small but persistent confusions: object vs class, instance vs type, identity vs state, and — most practically — *when* you should introduce a new class.

## What you already know

From [[00-OOP-Foundations]]: OOP exists to bundle mutable state, the rules that govern it, and the operations that change it into one place. From [[05-Identity-State-Lifecycle]]: identity is the property that lets us say "this is the same X" across time and transformations, and it comes in three flavors — object, logical, and surrogate. From [[04-Responsibilities]]: a responsibility becomes a class when it needs an owner with state and behavior.

If you can already say "an object is an instance; a class is the template; identity is what makes two instances the same even when their state differs," you can skim. The interesting part is *when* to introduce a new class.

## Why this layer exists

You cannot execute responsibilities. You can only execute code. Somewhere between "Account owns the balance invariant" (a responsibility) and `account.debit(amount)` (a line of code) there has to be a concrete artifact: a thing with a name, a shape, and a place in the type system. That artifact is the class. Instances of it are objects. This chapter exists because the distinction sounds trivial and is not — it generates most of the day-to-day decisions in OOP design.

## What is genuinely new here

Two things, both small but load-bearing:

1. **A class is a type.** Objects are values of that type. The class defines what is true of *all* instances; the object holds what is true of *this* instance. Conflating them leads to designs where state leaks into static fields, or where behavior that should be per-instance is shared globally.
2. **The decision to introduce a class is a cohesion decision.** You do not introduce a class because "it feels right." You introduce it because there is a responsibility that needs an owner with its own state and behavior — i.e., because a new invariant has emerged that no existing class protects.

## Concepts

- **Object** — a runtime instance; an identity holding state and exposing behavior defined by its class.
- **Class** — a compile-time template defining the shape (fields) and behavior (methods) of objects of one type.
- **Instance** — a synonym for object, emphasizing the relationship to its class.
- **Type** — the contract a class exposes to its callers. In Java, the type is the union of the class's public methods (and any interfaces it implements).
- **Reference** — a handle to an object in memory; the JVM-level realization of object identity.
- **Identity vs equality** — `==` compares references (object identity); `equals` compares logical state (equality by value, if implemented that way).

These terms are not interchangeable. Saying "I created a new type" means you have changed what callers can depend on. Saying "I created a new object" means you have allocated memory. The first is a design decision; the second is a runtime event.

## Banking application

The Banking case study ([[00-Banking-Case-Study]]) gives us our first real class decision. Consider the responsibility "know my balance and enforce the balance invariant." The natural owner is `Account`. So we write:

```java
public final class Account {
    private final AccountId id;
    private Money balance;
    private AccountStatus status;

    public Account(AccountId id, Money openingBalance) {
        this.id = id;
        this.balance = openingBalance;
        this.status = AccountStatus.PENDING;
    }

    public void activate() {
        if (status != AccountStatus.PENDING) {
            throw new IllegalStateException("Cannot activate from " + status);
        }
        this.status = AccountStatus.ACTIVE;
    }

    public void deposit(Money amount) {
        ensureActive();
        this.balance = balance.add(amount);
    }

    public void withdraw(Money amount) {
        ensureActive();
        this.balance = balance.subtract(amount);
    }

    public Money balance() { return balance; }
    public AccountStatus status() { return status; }

    private void ensureActive() {
        if (status != AccountStatus.ACTIVE) {
            throw new AccountNotActiveException(id);
        }
    }
}
```

Several decisions are visible in that small class:

- `Account` is `final`. We are not allowing subclassing (see [[03-Inheritance]] and [[05-Composition-Over-Inheritance]]). Variation is handled by composition, not inheritance.
- `id` is a value type (`AccountId`), not a raw `Long`. This prevents mixing up an account ID with a customer ID at compile time. See [[01-Entities-Value-Objects]] for the full pattern.
- `balance` is private and mutable, but only mutated through `deposit` / `withdraw`. There is no `setBalance`. This is encapsulation in action ([[02-Encapsulation]]).
- `status` transitions are guarded. `activate()` only works from `PENDING`. This enforces the lifecycle invariant from [[05-Identity-State-Lifecycle]].
- `balance()` and `status()` are read-only accessors. They expose *current* state without allowing mutation. This is fine; encapsulation is not about hiding data, it is about hiding *mutation paths*.

### When to introduce a new class

The hard question is not "what does this class look like" but "should this be a class at all?" Here are the heuristics, in order of authority:

1. **A new invariant has emerged that no existing class protects.** If you find yourself writing the same `if (balance < 0) throw ...` in three places, that is a signal that the "no negative balance" rule needs a home. Introduce (or enrich) a class.
2. **A group of fields always change together.** Cohesion: things that change together belong together. If `overdraftLimit`, `overdraftFeeRate`, and `overdraftGracePeriod` are always updated as a unit, they want to be an `OverdraftPolicy` object, not three fields on `Account`.
3. **A behavior keeps growing until it does not fit.** A `Transfer` class with a 200-line `execute()` method is too big. The internal phases — validate, fraud-check, debit, credit, persist, notify — want to be collaborators. See [[02-CRC-Cards]].
4. **Two responsibilities are entangled in one class.** If `Account` is also sending notification emails, it has two reasons to change. Split: `Account` owns the balance; `NotificationService` owns the emails.
5. **The same value is being passed around as primitive parameters.** If `transfer(amount, currency, fromIban, toIban, idempotencyKey)` shows up in five places, those primitives want to be `Money`, `AccountId`, `Iban`, `IdempotencyKey`. The class exists to enforce invariants the primitives cannot.

The reverse heuristics — when *not* to introduce a class — are equally important:

- **Do not introduce a class for one boolean.** A `WithdrawalAllowed` class wrapping a `boolean` adds ceremony without value. Use a method on the existing class.
- **Do not introduce a class for a name.** An `AccountName` class wrapping a `String` is fine if you need to enforce format invariants; it is noise if you do not.
- **Do not introduce a class to mirror a database table.** Tables are persistence artifacts; classes are behavior artifacts. They are not the same (see [[09-Object-Model-vs-Data-Model]]).

### Identity vs state — the canonical confusion

Two `Account` objects constructed with the same `id` and the same `balance` are *equal* but not *identical*:

```java
Account a = new Account(new AccountId(1L), Money.ZERO);
Account b = new Account(new AccountId(1L), Money.ZERO);
a == b        // false — different references
a.equals(b)   // depends on how equals is implemented
```

If `equals` is defined by `id`, then `a.equals(b)` is true. If `equals` is defined by `id` *and* `balance`, then it is true now and false after `a.deposit(Money.of(100))`. The choice matters enormously for collections, deduplication, and ORM sessions (see [[01-Identity-Map]]).

For entities with surrogate identity, the right pattern is the one from [[05-Identity-State-Lifecycle]]: `equals` based on logical identity (e.g., `iban`) when both have one, falling back to reference equality for transient (unpersisted) objects. For value objects (`Money`, `Iban`), `equals` is based on all fields and the object is immutable.

```java
public final class Iban {
    private final String value;

    public Iban(String value) {
        Objects.requireNonNull(value);
        if (!value.matches("[A-Z]{2}\\d{2}[A-Z0-9]{1,30}")) {
            throw new IllegalArgumentException("Invalid IBAN: " + value);
        }
        this.value = value;
    }

    @Override public boolean equals(Object o) {
        return o instanceof Iban other && value.equals(other.value);
    }
    @Override public int hashCode() { return value.hashCode(); }
    @Override public String toString() { return value; }
}
```

`Iban` is a class not because it has behavior (it has almost none) but because it has an *invariant* — the format — that no caller should be able to violate. A `String` cannot enforce that. A class can.

## What can go wrong

1. **Class explosion.** Introducing a class for every concept leads to a codebase where you cannot see the forest for the wrappers. Symptoms: `Username`, `Password`, `Email`, `PhoneNumber` each wrapping a `String` with no behavior. Cure: only introduce a class when it owns an invariant or groups fields that change together.
2. **God classes.** The opposite failure: one `BankingService` that does everything. Cure: apply the cohesion test from [[06-Coupling-and-Cohesion]] — one invariant per class.
3. **Primitive obsession.** Using `long` for IDs, `String` for IBANs, `BigDecimal` for money without wrapping them. Cure: introduce value types for any primitive that has a format, a unit, or a meaning beyond its raw value.
4. **Mistaking the class for the type.** A class has both a public type (its interface) and a private implementation. If callers depend on the implementation (e.g., they know `Account` uses a `TreeMap` internally), changing the implementation breaks them. Cure: program to the interface, not the concrete class (see [[05-DIP]]).
5. **Treating objects as data containers.** If your objects only have getters and setters, they are structs. You have the ceremony of OOP without any of its benefits. Cure: move behavior next to the state it protects — this is the path to rich models ([[05-Anemic-vs-Rich-Models]]).

## Trade-offs

- **Final classes vs open classes.** Marking `Account` `final` prevents subclassing, which prevents a whole class of bugs ( subclass that breaks invariants) but also prevents legitimate extension. Java 21's sealed classes (see [[06-Abstract-Classes-And-Interfaces]]) give a middle ground: closed by default, with a permit list.
- **Value types vs primitives.** Wrapping every primitive in a class adds safety and expressiveness but also adds allocation overhead and verbosity. For hot paths, the JVM's escape analysis and Project Valhalla's value classes may eventually remove the overhead; until then, profile before optimizing.
- **Rich vs anemic.** Putting behavior in entities (`Account.withdraw`) makes them cohesive but harder to test in isolation. Putting behavior in services (`TransferService.withdraw(account, amount)`) makes them testable but spreads the invariant across two places. See [[05-Anemic-vs-Rich-Models]] for the full trade-off.
- **One class per file vs many.** Java forces one public class per file, which is a cohesion forcing function. Other languages allow many. The discipline of one-class-per-file is worth keeping even where the language does not require it.

## Forward links

- [[02-Encapsulation]] — what makes the boundary between an object's state and its callers trustworthy.
- [[03-Inheritance]] — what happens when one class declares another as its parent.
- [[05-Identity-State-Lifecycle]] — the deeper treatment of identity, state, and lifecycle.
- [[01-Entities-Value-Objects]] — the DDD refinement: entities have identity; value objects do not.
- [[02-Aggregates]] — when a cluster of objects should be treated as one consistency boundary.
- [[05-Anemic-vs-Rich-Models]] — the consequences of putting behavior in entities vs services.
