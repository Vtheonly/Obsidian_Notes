# Information Holding — The Responsibility That Becomes a Class

> The bridge between responsibilities and classes. Some responsibilities are "knowing" — and the natural owner of a knowing responsibility is an object whose purpose is to know.

## What you already know

From [[04-Responsibilities]]: responsibilities come in three flavors — doing, knowing, and deciding. From [[06-Coupling-and-Cohesion]]: a module is cohesive if it owns one invariant. This note focuses on the *knowing* responsibility and shows how it generates most of the entities in a typical domain model.

## Why this layer exists

When you walk through a use case and assign responsibilities, you discover that many of them are "know X." Who knows the customer's name? Who knows the account's balance? Who knows the current exchange rate? These knowing responsibilities need an owner — and the owner is usually an object whose reason for existing is to know that thing.

This note exists to make the assignment of *knowing* responsibilities explicit. Without it, knowing responsibilities tend to drift into services (`CustomerService.getName()`, `AccountService.getBalance()`), and you end up with an anemic domain model (cross-link [[05-Anemic-vs-Rich-Models]]).

## What is genuinely new here

- The **Information Holder** as a recognized role in responsibility-driven design.
- The rule: *information holders own their data and the simple derivations from it*.
- The contrast with services, which coordinate but do not own.

## The Information Holder role

An Information Holder is an object whose primary responsibility is to know something and to provide that knowledge to collaborators. It is the most common kind of object in a typical system.

Characteristics:

- It owns state (fields).
- It exposes getters only when necessary (prefer telling over asking — cross-link [[04-Tell-Dont-Ask]]).
- It performs simple derivations from its own state (e.g., `Account.isOverdrawn()`).
- It does *not* coordinate other objects (that's a Service's job).
- It does *not* make decisions about other objects (that's also a Service's job, or a Strategy).
- Its identity is tied to the thing it represents (cross-link [[05-Identity-State-Lifecycle]]).

In DDD terms, an Information Holder is usually an **Entity** (if it has identity) or a **Value Object** (if it does not — cross-link [[01-Entities-Value-Objects]]).

## Banking — Information Holders

The Banking system has these Information Holders:

| Object | Knows | Derivations |
|---|---|---|
| `Customer` | name, contact info, KYC status | `isVerified()`, `canOpenAccount()` |
| `Account` | balance, status, type, customer | `isOverdrawn()`, `canWithdraw(amount)`, `availableBalance()` (incl. overdraft) |
| `LedgerEntry` | amount, account, timestamp, transfer | `isDebit()`, `isCredit()` |
| `Transfer` | source, destination, amount, status, idempotency key | `isPending()`, `isCompleted()` |
| `Money` (value object) | amount, currency | `add(other)`, `convertTo(currency, rate)` |
| `IBAN` (value object) | the string, parsed components | `countryCode()`, `checksumValid()` |
| `AccountStatus` (value object) | the enum value | `allowsDeposit()`, `allowsWithdrawal()` |

Notice that none of these methods coordinate other objects. `Account.canWithdraw(amount)` checks `this.balance` and `this.status` — it does not call out to other services. That is the Information Holder signature.

## Contrast with Services

Services are objects whose primary responsibility is to *do* or *decide*, not to know. They have little state of their own; they orchestrate Information Holders.

| Information Holder | Service |
|---|---|
| `Account` (knows balance) | `TransferService` (coordinates debit + credit) |
| `LedgerEntry` (knows amount) | `StatementService` (assembles entries into a statement) |
| `Customer` (knows KYC status) | `OnboardingService` (orchestrates KYC flow) |

The mistake: putting knowing responsibilities in services. `AccountService.getBalance(accountId)` is wrong — balance is `Account`'s to know. `account.getBalance()` is right.

## The "fat finger" test

A quick test for whether an object is an Information Holder or a Service:

> *If I deleted this object, what would the system lose?*

- Deleting `Account` would lose the balance and status — that's real data. Information Holder.
- Deleting `TransferService` would lose the orchestration logic, but no data. Service.
- Deleting `Money` would lose the amount and currency — real data. Information Holder (value object).
- Deleting `CurrencyConverter` would lose the conversion logic, but no data. Service.

Information Holders hold data; Services hold logic. The rule of thumb: data lives in Information Holders; cross-object logic lives in Services.

## How Information Holders become classes

When you have identified the Information Holders in your CRC card walkthrough (cross-link [[02-CRC-Cards]]), they translate directly to classes:

- Each Information Holder becomes a class.
- Its "knows" list becomes the fields.
- Its derivations become the methods.
- Its collaborators become the references / foreign keys.

This is why the responsibility-driven design step comes *before* the class design step: the responsibilities determine the classes, not the other way around. If you start with classes and try to add responsibilities, you end up with the wrong classes.

## Banking application — from responsibility to class

Recall the CRC card from [[02-CRC-Cards]]:

```text
Class: Account
Responsibilities:
  - Know my balance
  - Know my status
  - Debit myself (with rules)
  - Credit myself (with rules)
  - Enforce balance invariant
Collaborators:
  - LedgerEntry (records changes)
  - AccountStatus (enum)
  - OverdraftPolicy (for checking)
```

Translating to a class:

```java
public final class Account {
    private final AccountId id;
    private final IBAN iban;
    private BigDecimal balance;
    private AccountStatus status;
    private final OverdraftPolicy overdraftPolicy;  // for checking; null for savings

    public void debit(Money amount) {
        if (!status.allowsWithdrawal()) {
            throw new AccountNotActiveException(status);
        }
        var newBalance = balance.subtract(amount.amount());
        if (newBalance.signum() < 0 && overdraftPolicy == null) {
            throw new InsufficientFundsException(balance);
        }
        if (newBalance.signum() < 0 && newBalance.abs().compareTo(overdraftPolicy.limit()) > 0) {
            throw new InsufficientFundsException(balance, overdraftPolicy.limit());
        }
        this.balance = newBalance;
        // Ledger entry is written by the caller, not here — separation of concerns
    }

    public void credit(Money amount) {
        if (!status.allowsDeposit()) {
            throw new AccountNotActiveException(status);
        }
        this.balance = balance.add(amount.amount());
    }

    public boolean isOverdrawn() {
        return balance.signum() < 0;
    }

    public Money availableBalance() {
        var available = balance;
        if (overdraftPolicy != null) {
            available = available.add(overdraftPolicy.limit());
        }
        return Money.of(available, Currency.USD);  // simplification
    }
}
```

Notice:

- The class knows its own state (balance, status, policy).
- The derivations (`isOverdrawn`, `availableBalance`) are methods on the class.
- The mutation methods (`debit`, `credit`) enforce the invariant (balance >= -overdraftLimit).
- The class does *not* write the ledger entry — that is the caller's responsibility (`TransferService` writes both the debit and the ledger entry in one transaction).

This is a rich Information Holder: it owns its data and the rules around it, but it does not coordinate other objects.

## What can go wrong

- **Anemic Information Holders** — the class is just a bag of getters and setters; the rules live in a service. Move the rules into the class.
- **God Information Holders** — the class knows too much; it should be split. If `Account` also held the customer's name and the transfer history, it would be doing too much.
- **Information Holder as Service** — the class coordinates other objects when it should just hold data. Move the coordination to a Service.
- **Service as Information Holder** — the service accumulates state (caches, registries). Either make it a proper Information Holder or move the state to one.

## Trade-offs

- **Rich vs anemic** — rich Information Holders are more cohesive and easier to test in isolation, but they couple behavior to data (which can make persistence harder). Anemic Information Holders are easy to persist but scatter logic. Banking picks rich for entities with strong invariants (Account, LedgerEntry) and accepts the persistence cost via ORM mapping (cross-link [[07-Banking-ORM-Mapping]]).
- **Tell vs ask** — Information Holders should *tell* (call methods on collaborators) rather than *be asked* (expose getters). But some asking is unavoidable (e.g., reporting queries). Use tell for behavior, ask for read models.

## Forward links

- [[01-Objects-And-Classes]] — Information Holders become classes.
- [[01-Entities-Value-Objects]] — Information Holders with identity are entities; without are value objects.
- [[05-Anemic-vs-Rich-Models]] — the trade-off in depth.
- [[02-Aggregates]] — a cluster of Information Holders forms an aggregate.
- [[05-Repository-Pattern]] — repositories persist Information Holders.
- [[04-Enterprise-Patterns]] — the broader pattern catalog.
