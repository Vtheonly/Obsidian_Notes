# Trade-offs Everywhere

> The fifth and last force. There are no solutions in software — only trade-offs. The job of an engineer is not to find the "correct" answer but to *make trade-offs explicit*.

## What you already know

From [[03-Dependency-As-Root-Concept]] to [[07-Composition-vs-Inheritance]]: every design choice has costs. Coupling reduces changeability. Inheritance reduces flexibility. Abstraction hides details but adds indirection. This note formalizes the meta-force that organizes them all.

## The core claim

> **Every design decision is a trade-off. The decision is not "which is better" but "which cost am I willing to pay, given the constraints of this system?"**

This is the difference between a junior and a senior engineer. A junior asks "which is better, A or B?" A senior asks "what does A cost, what does B cost, and which cost fits *this* problem?"

## The shape of a trade-off

A trade-off has four parts:

1. **The axis** — what is being traded (latency vs throughput; consistency vs availability; normalization vs read speed; flexibility vs simplicity).
2. **The two ends** — the extremes of the axis.
3. **The current position** — where on the axis you are now.
4. **The force pushing you** — what is making you reconsider the position.

Without naming all four, you cannot reason about a trade-off. "We should denormalize" is meaningless without saying "we are trading write complexity for read speed because the dashboard query is too slow."

## The canonical trade-off axes

These appear in every system. Learn to recognize them.

### In design

| Axis | End A | End B |
|---|---|---|
| Coupling | Tightly integrated (fast, brittle) | Loosely coupled (flexible, slower) |
| Abstraction | Concrete (fast, rigid) | Abstract (flexible, indirect) |
| Cohesion | One big module (convenient, fragile) | Many small modules (clean, verbose) |
| Inheritance vs composition | Inheritance (compact, rigid) | Composition (verbose, flexible) |
| Synchronous vs asynchronous | Sync (simple, slow) | Async (fast, complex) |

### In databases

| Axis | End A | End B |
|---|---|---|
| Normalization | Fully normalized (no redundancy, slow reads) | Denormalized (redundant, fast reads) |
| Isolation | Serializable (correct, slow) | Read uncommitted (fast, wrong) |
| Indexing | No indexes (fast writes, slow reads) | Many indexes (slow writes, fast reads) |
| Consistency | Strong (correct, slow, unavailable under partition) | Eventual (fast, stale reads) |
| Storage layout | Row store (OLTP, fast point lookups) | Column store (OLAP, fast scans) |
| Replication | Synchronous (consistent, slow commits) | Asynchronous (fast commits, replica lag) |

### In distributed systems

| Axis | End A | End B |
|---|---|---|
| CAP | Consistency | Availability |
| PACELC | Latency under partition | Consistency without partition |
| Coupling | Synchronous RPC (tight) | Async events (loose) |
| Coupling | Shared database (tightest) | API integration (loose) |
| Granularity | Coarse services (chatty network, simple ops) | Fine services (network-heavy, complex ops) |

### In query optimization

| Axis | End A | End B |
|---|---|---|
| Plan time | Search exhaustively (best plan, slow parse) | Heuristic (fast parse, worse plan) |
| Index choice | Use index (fast lookup, random IO) | Sequential scan (slow lookup, sequential IO) |
| Join order | Build hash on smaller side (memory-heavy, fast) | Nested loop (memory-light, slow) |
| Materialization | Materialize intermediate (memory-heavy, avoids recompute) | Streaming (memory-light, recomputes) |

## Trade-offs are not symmetric

A common mistake: thinking the optimal position is the midpoint. It almost never is. The midpoint is usually bad at both ends.

Example: at isolation level "read committed," you get neither the correctness of "serializable" nor the speed of "read uncommitted." You get the worst of both — *and* you get non-repeatable reads and phantom reads for free. The midpoint is not optimal; it is the lazy default.

The right position is *deliberate*: pick the end that fits the constraint, and accept its cost knowingly. If you need correctness, pick serializable and pay the latency. If you need throughput and can tolerate stale reads, pick snapshot isolation and pay the staleness. Do not drift into the middle.

## The trade-off you don't notice is the trade-off that hurts you

The worst trade-off is the one you make without realizing it.

- Default isolation level? That's a trade-off you inherited.
- ORM default fetch strategy? That's a trade-off someone else made for you.
- "We'll add caching later"? That's a trade-off deferred, and the deferred cost is interest.
- "Let's just use a single database for all services"? That's a coupling trade-off, often made for short-term convenience.

A senior engineer's job is to make these implicit trade-offs explicit, write them down, and revisit them when constraints change.

## Trade-offs and reversibility

Some trade-offs are reversible; some are not. Jeff Bezos's "two-way door vs one-way door" framing applies directly:

- **Reversible (two-way door)**: choice of cache library, choice of HTTP framework, choice of testing tool. Make the choice quickly; revert if wrong.
- **Irreversible (one-way door)**: choice of primary database, choice of monorepo vs polyrepo, choice of synchronous vs asynchronous inter-service communication, choice of programming language for a large codebase. Spend the time to get it right; the cost of changing it later is enormous.

The skill is recognizing which kind of decision you are making. Many teams treat one-way doors as two-way and suffer for years. Others treat two-way doors as one-way and ship nothing.

## The trade-off table as a design artifact

When making a significant design decision, write a one-page trade-off note:

```text
Decision: Should the banking system use synchronous or event-driven transfers?

Axis: Coupling between TransferService and FraudService

Option A: Synchronous RPC
  + Simple flow, immediate response
  + Easy to reason about (one transaction)
  - FraudService outage blocks transfers
  - Tight coupling; FraudService changes ripple

Option B: Event-driven (transfer created → fraud check → approve)
  + TransferService is decoupled from FraudService
  + FraudService can be down without blocking transfer creation
  - Eventual consistency: a transfer may be created and then rejected
  - More moving parts (broker, consumer, retry, DLQ)

Force pushing us: FraudService has had three outages in the last quarter, each
blocking all transfers for an hour. Decoupling is worth the eventual consistency.

Decision: Option B, with the constraint that transfer status is PENDING until
fraud check completes, and PENDING transfers are not visible to customers.

Revisit when: FraudService uptime exceeds 99.99% for two quarters, or when
customer complaints about PENDING transfers exceed X/month.
```

This is a design artifact. It survives the team. It tells future engineers *why* the decision was made and *what would change the answer*.

## Banking application — the trade-offs you will see

Throughout the vault, the banking case study makes these trade-offs explicit:

- **Normalization vs read speed**: ledger entries are normalized (one row per entry); current balance is denormalized (one column on the account). Why? Because computing balance from ledger entries on every read is too slow.
- **Strong vs eventual consistency**: balance is updated synchronously in the same transaction as the ledger entry (strong); the customer notification is sent asynchronously (eventual). Why? Because the customer can tolerate a delayed email; they cannot tolerate a wrong balance.
- **Serializable vs snapshot isolation**: transfers use serializable (correctness is non-negotiable); statement generation uses snapshot (eventually consistent reads are fine).
- **Index trade-offs**: an index on `(account_id, occurred_at)` makes ledger queries fast; an index on `(occurred_at)` makes daily reports fast; both slow down inserts. We pay the cost because both queries are common.
- **Monolith vs microservices**: start as a monolith (faster to build, fewer moving parts). Decompose into services only when a bounded context becomes a deployment bottleneck.

Every one of these is a deliberate choice. The vault does not pretend there is a "right" answer — only a right answer *given the constraints*.

## What is genuinely new here

- Trade-offs are the meta-force; every other force is a trade-off axis.
- A trade-off has four parts: axis, two ends, current position, the force pushing.
- The midpoint is usually wrong; pick an end deliberately.
- Implicit trade-offs are the dangerous ones. Make them explicit.
- Some trade-offs are reversible (decide fast) and some are not (decide carefully).
- Write trade-off notes as design artifacts.

## Where this goes next

- Every later chapter makes trade-offs explicit.
- Especially: [[10-Normalization-Trade-offs]], [[02-Isolation-Levels]], [[00-CAP-PACELC]], [[00-Query-Optimization-Strategy]].
- [[05-Architecture-Trade-offs]] collects the architecture-level trade-offs in one place.
