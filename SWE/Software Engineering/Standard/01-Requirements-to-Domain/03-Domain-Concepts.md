# Domain Concepts — Discovering Nouns and Verbs

> Domain concepts are the vocabulary of the problem. They are not classes yet; they are not tables yet. They are the *words* the business uses, captured before we commit to any implementation.

## What you already know

From [[02-Use-Cases]]: use cases structure behavior into scenarios. From [[04-Abstraction-and-Models]]: a model is selective forgetting for a purpose. Domain concepts are the first cut of the model — we forget the procedural detail of the use cases and keep only the *nouns and verbs* that the business treats as meaningful.

## Why this layer exists

A common failure mode: a developer reads requirements, jumps straight to code, and discovers six months later that the domain has concepts nobody modeled. The customer service team has a word for something the engineers never heard of. The compliance team has a category the engineers treated as a single field. The accounting team has a distinction the engineers collapsed into one enum value.

Domain modeling — extracting the nouns and verbs *before* designing — exists to surface this vocabulary while it is still cheap to incorporate. A concept discovered at requirements time costs an hour to add. A concept discovered in production costs a quarter to retrofit.

## What is genuinely new here

- The discipline of **noun extraction** — what are the things in this domain?
- The discipline of **verb extraction** — what are the actions?
- The discipline of **ubiquitous language** — using the same words as the domain experts, not technical synonyms.

These are not technical skills. They are listening skills.

## The technique — noun-first extraction

1. Take a use case (e.g., the transfer use case from [[02-Use-Cases]]).
2. Read it carefully, highlighting every noun phrase.
3. List them. Some are entities; some are attributes; some are roles; some are external systems.
4. Repeat for each use case.
5. Cluster synonyms; resolve homonyms.
6. The result is the domain's vocabulary.

## Banking — noun extraction from the transfer use case

From the transfer use case, the nouns are:

- Customer (actor)
- Source account (entity)
- Destination account (entity)
- Account status (attribute, with values: ACTIVE, FROZEN, CLOSED)
- Account owner (relationship — Customer owns Account)
- Balance (attribute)
- Overdraft limit (attribute, only for checking accounts)
- Amount (parameter)
- Per-transfer limit (constraint)
- Daily limit (constraint)
- Idempotency key (parameter)
- FraudService (external system)
- NotificationService (external system)
- Transfer (entity, with status: PENDING, COMPLETED, FRAUD_REVIEW, FRAUD_PENDING)
- Ledger entry (entity)
- Transaction (technical concept — note this!)
- Audit log (technical concept)
- Notification (entity)

Notice that "transaction" appears here as a technical concept, not a domain concept. We will need to decide: is it part of the ubiquitous language, or is it an implementation detail? In banking, "transaction" is heavily used in the domain, so it stays. In other domains, it might be hidden.

## Verbs — the actions

From the same use case, the verbs are:

- Transfer (action)
- Submit (action)
- Authenticate (action)
- Validate (action)
- Check (action)
- Debit (action)
- Credit (action)
- Approve (action)
- Reject (action)
- Flag (action)
- Notify (action)
- Audit (action)

Each verb is a *responsibility waiting to be assigned* (see [[04-Responsibilities]]).

## Ubiquitous language

The term comes from Domain-Driven Design (DDD, see [[00-Domain-Modeling]]). The idea:

> The vocabulary used in code, in conversations with domain experts, in tests, in documentation, and in the UI should be *the same*.

If the business calls it a "transfer" and the code calls it a "TransactionRequest," that is a leak. The next engineer will translate in their head every time they read the code. Eventually, someone will translate wrong.

Examples of vocabulary alignment in banking:

| Business says | Code should say | Not |
|---|---|---|
| Transfer | `Transfer` | `TransactionRequest`, `MoneyMovement` |
| Account | `Account` | `AccountRecord`, `CustomerAccount` |
| Ledger entry | `LedgerEntry` | `TransactionLog`, `BalanceChange` |
| Debit | `debit()` | `subtractFromBalance()`, `applyNegativeDelta()` |
| Credit | `credit()` | `addToBalance()`, `applyPositiveDelta()` |
| Freeze | `freeze()` | `setStatus(STATUS_FROZEN)`, `lock()` |
| Overdraft | `overdraftLimit` | `negativeBalanceLimit`, `minBalanceThreshold` |

The rule: if the business has a word for it, use that word. If the business does not have a word for it, ask whether the concept is real before inventing a word.

## Bounded contexts — same word, different meaning

A word in the business vocabulary may mean different things in different contexts.

- "Account" in retail banking means a financial container owned by a customer.
- "Account" in the authentication subsystem means a login credential.
- "Account" in the audit subsystem means a record of an actor's actions.

Same word; three meanings. Each meaning is legitimate in its context. The mistake is to collapse them into a single `Account` class. The DDD solution is a **bounded context**: a boundary within which a term has one consistent meaning (see [[03-Bounded-Contexts]]).

In banking, we have at least these contexts:

- **Account Management** — Account as a financial container.
- **Identity & Access** — Account as a login.
- **Audit** — Account as a record of actions.
- **Reporting** — Account as a row in a statement.

Each context has its own model. They communicate by translation, not by sharing classes.

## Banking application — the domain glossary

A condensed glossary for the Account Management context:

```text
Account
  A financial container owned by a Customer, holding a balance in a single currency.

Customer
  A person or organization that owns one or more Accounts.

Checking Account
  An Account that permits overdraft up to an overdraft limit.

Savings Account
  An Account that accrues interest and does not permit overdraft.

Ledger Entry
  An immutable record of a single monetary movement against an Account.

Transfer
  A request to move money from one Account to another, producing two Ledger Entries.

Balance
  The sum of all Ledger Entries for an Account.

Overdraft Limit
  The maximum negative balance permitted on a Checking Account.

Interest Rate
  The annual rate at which a Savings Account accrues interest.

Account Status
  One of: PENDING, ACTIVE, FROZEN, CLOSED.
```

This glossary is the contract. Every later artifact (class, table, API, message) must use these words consistently. When the glossary changes, the artifacts must change.

## What can go wrong

- **Synonyms not resolved** — "Transfer," "Transaction," "Money Movement" all used for the same thing. Engineers pick different ones in different files.
- **Homonyms not separated** — "Account" used for both login and financial container in the same module.
- **Technical vocabulary leaking into the domain** — `TransactionManager`, `EntityRepository`, `DtoMapper` are not domain concepts; they are technical concepts. Keep them out of the ubiquitous language.
- **Domain vocabulary leaking into technical layers** — `TransferService` is fine, but `TransferStrategyFactoryImpl` is leaking domain words into plumbing. Use neutral names for plumbing.
- **Glossary drift** — the glossary is written once and never updated. Two years later, the code uses different words. The glossary is fiction.

## Trade-offs

- **How much to model?** Too little: you miss critical concepts. Too much: you spend months modeling and never ship. The right amount: model the invariants and the entities that enforce them; defer the rest.
- **Formal vs informal?** A formal glossary (in a wiki, with definitions) is more rigorous but heavier. An informal glossary (in code, as class names and comments) is lighter but easier to lose. Use both: formal for the critical few, informal for the rest.
- **When to refactor the language?** Whenever the domain reveals a new concept. Language is not frozen; it evolves with understanding. But each evolution should be deliberate, not accidental.

## Forward links

- [[04-Responsibilities]] — turn these verbs into responsibility assignments.
- [[00-Domain-Modeling]] — full DDD treatment.
- [[03-Bounded-Contexts]] — when the same word means different things.
- [[00-UML-As-Modeling-Language]] — visualize the domain model.
