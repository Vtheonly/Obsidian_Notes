# Design Forces

> A design force is a constraint or pressure on the design: scalability, testability, maintainability, latency, correctness, auditability, time-to-market, team structure. LLD is the act of naming these forces, finding where they conflict, and choosing a structure that resolves them. Without naming the forces, every design decision feels arbitrary.

## What you already know

From [[08-Trade-offs-Everywhere]]: every design decision is a trade-off. Forces are the two ends of every trade-off axis. You cannot make a trade-off without naming the forces.

From [[06-Coupling-and-Cohesion]]: coupling and cohesion are themselves forces — the two that appear at every layer of the system. Most other forces are specializations or consequences of these two.

From [[00-LLD-Method]]: step 4 of the LLD method is "name the design forces." This chapter is the deep dive on that step.

From [[03-Dependency-As-Root-Concept]]: dependencies point toward stability. Forces determine what "stability" means — a system optimized for scalability is stable in one direction; a system optimized for auditability is stable in another.

## Why this layer exists

A junior engineer asks: "which is better, A or B?" A senior engineer asks: "what does A cost, what does B cost, and which cost fits *this* problem?" The difference is the *forces*. Without naming them, every decision is aesthetic. With them, every decision is a trade-off with a justification.

Forces exist because real systems have multiple stakeholders with competing goals:

- The product team wants features fast → **time-to-market**.
- The ops team wants the system to survive outages → **availability**.
- The compliance team wants an audit trail → **auditability**.
- The customer wants low latency → **performance**.
- The engineering team wants the code to be maintainable → **maintainability**.
- The finance team wants low cost → **efficiency**.

No structure optimizes all of these at once. LLD is the act of choosing which forces to favor and which to sacrifice — and writing down the choice so future engineers can revisit it when the constraints change.

## What is genuinely new here

- The vocabulary of design forces — a checklist you can apply to any problem.
- **Conway's Law** as a force — the architecture will mirror the org chart, whether you want it to or not.
- How forces conflict and how to resolve the conflicts via trade-offs.
- The discipline of enumerating forces *before* choosing a structure.

## Concepts

### The canonical force list

These are the forces that appear in almost every system. Different lists exist (Bass/Clements/Kazman's quality attributes, ISO 25010); they overlap heavily. This is the practical set.

| Force | Question it answers | What it pushes the design toward |
|---|---|---|
| Correctness | Does the system do the right thing? | Strong invariants, transactions, validation |
| Availability | Is the system up when needed? | Redundancy, failover, no single point of failure |
| Reliability | Does it not break? | Error handling, retries, circuit breakers |
| Scalability | Can it grow? | Stateless services, sharding, async |
| Latency | How fast is a single request? | Caching, indexing, sync over async |
| Throughput | How many requests per second? | Batching, parallelism, async |
| Consistency | Do all readers see the same data? | Synchronous replication, strong isolation |
| Auditability | Can we trace what happened? | Immutable logs, event sourcing, audit tables |
| Security | Can the wrong people do wrong things? | Auth, authz, encryption, least privilege |
| Maintainability | Can engineers change it? | Low coupling, high cohesion, clear abstractions |
| Testability | Can we verify it works? | Dependency injection, mocks, side-effect isolation |
| Deployability | Can we ship safely? | Independent components, feature flags, canaries |
| Time-to-market | Can we ship soon? | Simpler architecture, fewer components, less polish |
| Cost | Is it cheap to run? | Smaller instances, fewer services, shared infra |
| Team structure (Conway) | Does it fit how the team is organized? | Component boundaries aligned to team boundaries |

### How to enumerate forces for a problem

For any new problem, walk the list and ask: "does this force matter here, and how much?" Mark each as critical, important, or negligible.

For the Banking transfer flow:

- **Correctness**: critical. A bug costs real money.
- **Auditability**: critical. Regulators require it.
- **Consistency**: critical. The balance must be right.
- **Latency**: important. Customers wait for confirmation.
- **Throughput**: important. Thousands of transfers per second at peak.
- **Availability**: important. Outages are headline news.
- **Maintainability**: important. The codebase will live for decades.
- **Testability**: important. We must be able to prove correctness.
- **Scalability**: important. The customer base grows.
- **Security**: important. Money is involved.
- **Deployability**: important. We deploy daily.
- **Time-to-market**: low. Banking is not a startup racing to launch.
- **Cost**: low. Banks have budgets; correctness is worth more than infrastructure savings.

The critical forces — correctness, auditability, consistency — drive the design toward serializable transactions, immutable ledger entries, and synchronous validation. The important forces — latency, throughput, availability — drive toward async notifications, horizontal scaling, and redundancy. The low forces do not bend the design.

If you tried to optimize all fifteen forces equally, you would have a paralyzed design. The discipline is in *ranking* the forces.

### Conway's Law — the invisible force

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." — Melvin Conway, 1968

If your organization has a "frontend team," a "backend team," and a "database team," your architecture will have a frontend, a backend, and a database — even if a different decomposition would be technically better. The communication overhead of crossing team boundaries is a *real cost*, and the design evolves to minimize it.

This is not a failure. It is a force. The question is whether to *align* the architecture to the org chart (accept Conway's Law) or to *change the org chart* to enable a better architecture (the "Conway maneuver" — reverse-engineer the org structure to produce the architecture you want).

For the Banking system, suppose the org has:

- A Customer Onboarding team
- A Payments team (transfers, withdrawals, deposits)
- A Risk & Compliance team (fraud, KYC)
- A Platform team (database, broker, deployment)

The architecture will naturally have components aligned to these teams:

- OnboardingService (Customer Onboarding team)
- TransferService, AccountService (Payments team)
- FraudService, KycService (Risk & Compliance team)
- Shared infrastructure (Platform team)

This is not arbitrary — it is the org chart expressed as deployment units. Changing the architecture requires changing the org chart.

### How forces conflict

Forces conflict when optimizing one degrades another. The most common conflicts:

| Conflict | Resolution |
|---|---|
| Correctness vs latency | Strong isolation is correct but slow; pick the isolation level deliberately (see [[02-Isolation-Levels]]) |
| Consistency vs availability | The CAP theorem (see [[00-CAP-PACELC]]) — under partition, you cannot have both |
| Auditability vs cost | Immutable logs are audit-friendly but storage-heavy; sample or roll up |
| Maintainability vs time-to-market | Clean abstractions take longer to build but pay back later |
| Scalability vs simplicity | Sharding scales but adds complexity; start simple, shard when forced |
| Security vs latency | Encryption adds CPU; TLS handshakes add latency; offline encryption at rest avoids the latency |
| Testability vs performance | Indirection makes code testable but adds runtime overhead |

Each conflict is a trade-off (see [[08-Trade-offs-Everywhere]]). The resolution is *deliberate*: pick the side that fits the constraint, and write down what would change the answer.

### How to resolve conflicts

Three strategies:

1. **Favor one force explicitly.** "We choose correctness over latency because banking." Write it down.
2. **Split the system along the conflict.** "The transfer path favors correctness (serializable); the statement-generation path favors latency (snapshot isolation). Different paths, different choices." This is CQRS — see [[04-Enterprise-Patterns]].
3. **Change the constraint.** "If we shard the database, we can have both correctness and throughput — at the cost of operational complexity." This is a one-way door — see [[08-Trade-offs-Everywhere]].

The wrong resolution: drift into the middle. A system that tries to balance correctness and latency by using "read committed" isolation gets neither — it has anomalies *and* is slower than read-uncommitted.

## Banking application — the force table

For the transfer flow, the force table is:

| Force | Priority | How it shapes the design |
|---|---|---|
| Correctness | Critical | Serializable transaction, double-entry ledger, idempotency |
| Auditability | Critical | Immutable ledger entries, audit log on every state change |
| Consistency | Critical | Synchronous balance update in same transaction as ledger write |
| Latency | Important | Async notification; sync fraud check (cannot avoid) |
| Throughput | Important | Horizontal scaling of TransferService; connection pooling |
| Availability | Important | Two app server instances; failover database |
| Maintainability | Important | Hexagonal architecture; ports for all dependencies |
| Testability | Important | All dependencies injectable; in-memory test doubles |
| Scalability | Important | Stateless TransferService; sharding when forced |
| Security | Important | Auth on every request; least privilege on DB credentials |
| Deployability | Important | Independent component for FraudService (different release cadence) |
| Time-to-market | Low | — |
| Cost | Low | — |
| Conway | Active | Component boundaries match team boundaries |

The critical forces dominate. The important forces refine. The low forces do not bend the design. This is how a senior engineer reads the table: not as a checklist, but as a *ranking* that drives every decision.

## Code / diagrams — forces visible in code

A well-designed codebase makes the forces visible. Here is the TransferService skeleton with the forces called out as comments:

```java
public final class TransferService implements TransferPort {
    // Force: testability, maintainability — inject interfaces, not concretions
    private final AccountPort accounts;
    private final FraudPort fraud;
    private final NotificationPort notifications;
    private final LedgerPort ledger;
    private final IdempotencyStore idempotency;
    // Force: correctness — the transaction manager enforces atomicity
    private final TransactionManager tx;

    public TransferService(AccountPort accounts, FraudPort fraud,
                           NotificationPort notifications, LedgerPort ledger,
                           IdempotencyStore idempotency, TransactionManager tx) {
        this.accounts = accounts;
        this.fraud = fraud;
        this.notifications = notifications;
        this.ledger = ledger;
        this.idempotency = idempotency;
        this.tx = tx;
    }

    public TransferResult transfer(TransferRequest req) {
        // Force: idempotency — check before doing anything
        Optional<TransferResult> prior = idempotency.lookup(req.idempotencyKey());
        if (prior.isPresent()) return prior.get();

        Account from = accounts.load(req.from());
        Account to   = accounts.load(req.to());

        // Force: correctness — fraud check before any state change
        FraudDecision decision = fraud.evaluate(req);

        // Force: correctness, consistency, atomicity — serializable transaction
        TransferResult result = tx.inTransaction(() -> {
            from.withdraw(req.amount());
            to.deposit(req.amount());
            // Force: auditability — every state change has a ledger entry
            ledger.write(req.from(), req.amount().negate(), req.transferId());
            ledger.write(req.to(),   req.amount(),         req.transferId());
            accounts.save(from);
            accounts.save(to);
            return TransferResult.completed();
        });

        // Force: latency, throughput — async notification
        notifications.notifyAsync(new TransferEvent(req));

        idempotency.store(req.idempotencyKey(), result);
        return result;
    }
}
```

Every comment is a force. Every choice is a trade-off. The code reads as a *documented* design, not an accident.

## What can go wrong

- **Listing forces without ranking.** A flat list of fifteen forces all marked "important" is useless. The discipline is in the ranking.
- **Forces that do not conflict.** If your force analysis has no conflicts, you have either missed the hard part or the problem is trivial. Real problems have conflicts.
- **Forgetting Conway's Law.** The org chart *will* shape the architecture. Ignoring it leads to architectures that fight the team structure and lose.
- **Treating forces as static.** Forces change. A startup optimizes for time-to-market; the same company five years later optimizes for maintainability. The force analysis should be revisited.
- **Optimizing for a force that does not matter.** A bank that optimizes for cost over correctness will eventually be regulated out of existence. Match the optimization to the problem.
- **Not writing the force analysis down.** If the analysis lives in one engineer's head, it dies when they leave. Write it in a design doc; review it when constraints change.

## Trade-offs

- **Time spent in force analysis vs time spent in design.** More analysis = better-informed design, but analysis has diminishing returns. The right amount: enough to rank the top five forces and identify the main conflicts.
- **Formal vs informal force analysis.** A formal table (ISO 25010) is rigorous but heavy. An informal list on a whiteboard is fast but lossy. Use formal for regulated systems (banking, healthcare); informal for early-stage products.
- **Team-owned vs solo-owned force analysis.** Solo analysis is fast but blind. Team analysis catches more forces but takes longer. Use solo for the first cut, team for the review.

## Forward links

- [[00-LLD-Method]] — where force analysis sits in the pipeline.
- [[08-Trade-offs-Everywhere]] — the meta-force that organizes all others.
- [[05-Architecture-Trade-offs]] — the architecture-level trade-offs the forces drive.
- [[02-Layered-Architecture]] through [[04-Clean-Architecture]] — the structures chosen based on which forces dominate.
- [[06-Banking-LLD]] — the full force analysis for the transfer flow.
- [[00-CAP-PACELC]] — the canonical example of forces in conflict (consistency vs availability).
- [[02-Isolation-Levels]] — another canonical conflict (correctness vs latency).
