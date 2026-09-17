# Dependency — The Root Concept

> If you read only one foundational note, read this one. Dependency is the single most reused idea in the vault. It reappears in UML, OOP, SOLID, schema design, foreign keys, joins, query plans, and distributed systems — always wearing different vocabulary, always meaning the same thing.

## What you already know

From [[02-The-Continuous-Chain]]: every layer adds something. Dependency is not one layer's contribution — it lives *across* every layer.

## The core definition

> **A dependency exists when a change in one place can force a change in another place.**

That is the entire concept. Every other definition — UML dependency arrow, software coupling, foreign key, import, function call, schema dependency, join dependency — is a specialization of this one sentence.

## The two directions of dependency

There is always a *direction*.

- **A depends on B** means: A needs B to exist, to be correct, or to be available. A change in B can ripple into A. A change in A does not ripple into B (unless B also depends on A — which would be a cycle).

This direction matters enormously. It determines:

- Which side can be changed safely
- Which side must be deployed first
- Which side is the *interface provider* and which is the *interface consumer*
- Which side owns the contract

## Where dependency appears — once, then mapped

| Layer | Vocabulary | Same idea |
|---|---|---|
| Code | `import`, `using`, `requires` | "I cannot compile without you" |
| OOP | A holds a reference to B | "A sends messages to B" |
| UML | `A --> B` (dependency arrow), `A --> B` (association) | "A mentions B" |
| SOLID | DIP — depend on abstractions | "Invert the direction so the policy does not depend on the detail" |
| Package | A imports from package B | "A change in B's public surface can break A's build" |
| Schema | Table A has a foreign key to B | "A's row cannot exist without a matching B row" |
| SQL | `JOIN` A and B | "The query depends on both schemas" |
| Query plan | Hash join depends on building the hash table first | "Execution depends on data availability" |
| Distributed | Service A calls service B | "A's availability depends on B's availability" |

Every row in that table is the same concept. Do not learn it nine times.

## The two operations on dependencies

Once you can see dependencies, you can do exactly two things to them:

1. **Reduce** them. Fewer dependencies = fewer ripples = easier change.
2. **Invert** them. Make the policy depend on an abstraction, and let the detail depend on the same abstraction. The total number of dependencies may stay the same, but the *direction* now favors the stable side.

These two operations generate almost every design rule you have ever been taught:

- "Loose coupling" = reduce dependencies.
- "Depend on abstractions, not concretions" = invert dependencies.
- "Single Responsibility" = a class with one responsibility has fewer reasons to change, so it has fewer dependency ripples.
- "Open/Closed" = extend without modifying = add new dependencies without changing existing dependents.
- "Interface Segregation" = split a fat interface so consumers depend only on what they use.
- "Foreign keys point at stable tables" = the direction of dependency should follow the direction of stability.
- "Avoid cyclic schema dependencies" = a cycle means neither side can change independently.
- "Avoid cyclic package dependencies" = same idea, code layer.
- "Microservice calls should flow in one direction" = same idea, distributed layer.

Notice that none of those rules is a new idea. They are all instances of *reduce* or *invert* applied at a specific layer.

## Dependency direction and stability

The single most useful heuristic in software design:

> **Dependencies should point toward stability.**

If module A changes every sprint and module B has not changed in five years, B should not depend on A. If it does, every change to A threatens B. Either invert the dependency (A depends on B), or introduce an abstraction that both depend on (DIP).

This heuristic explains:

- Why domain code should not depend on infrastructure (infrastructure changes more often than the domain model)
- Why business code should not depend on UI frameworks
- Why applications should depend on a database *interface*, not on a specific vendor
- Why a high-churn table should not be referenced by fifty other tables via foreign keys

## Dependency in the Banking case study

In a banking system, what depends on what?

- `TransferService` depends on `Account` (it needs accounts to move money between them).
- `Account` does *not* depend on `TransferService` (the account has no idea someone might transfer into it).
- `Account` depends on `LedgerEntry` (every state change is recorded as a ledger entry).
- `LedgerEntry` depends on nothing (it is a primitive, immutable record).
- The dependency graph points *toward* `LedgerEntry`, which is the most stable, most depended-upon, least-changing concept in the system.

This is not accidental. It is the design.

When we get to schema design, the same picture emerges:

- `transfers` table has foreign keys to `accounts`.
- `accounts` table has a foreign key to `customers`.
- `ledger_entries` has foreign keys to `accounts`.
- Nothing has a foreign key to `ledger_entries`. It is a leaf.

The dependency arrows in code and the foreign key arrows in schema *point the same direction*. They are the same force.

## What dependency is *not*

- Dependency is not "uses." A class can use another class without depending on it, if the use goes through an abstraction owned by the consumer.
- Dependency is not "association." Association is structural (A holds B); dependency is logical (A's correctness requires B's correctness). All associations are dependencies; not all dependencies are associations.
- Dependency is not "call." A calls B at runtime, but A depends on B's *contract*, not on B's *implementation*.

## What is genuinely new here

Nothing, if you understood the first sentence. The whole note is one concept plus a map of where it reappears. The map matters because the vocabulary differs; the concept does not.

## Where this goes next

Every chapter. But specifically:

- [[00-SOLID-as-Dependency-Management]] — SOLID is dependency management formalized.
- [[01-Primary-Foreign-Keys]] — schema dependencies, formalized.
- [[00-ORM-Impedance-Mismatch]] — where the dependency graph in code disagrees with the dependency graph in schema.
- [[03-Sharding-Revisited]] — when a dependency crosses a shard boundary, you have a distributed dependency, and the cost goes up by orders of magnitude.
