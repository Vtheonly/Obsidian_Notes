# CRC Cards — Class, Responsibility, Collaborator

> CRC cards are a low-tech design technique invented at Tektronix in the late 1980s by Kent Beck and Ward Cunningham, then popularized by Wirfs-Brock and McKean. The idea is brutally simple: write each candidate class on a 4x6 index card, list its responsibilities and collaborators, and walk through use cases by pointing at the cards. The constraint of the physical card is the point — it forces splitting when a class gets too big.

## What you already know

From [[04-Responsibilities]]: a responsibility is "do X" or "know Y"; the natural owner is the object that has the information to fulfill it; whoever owns an invariant owns the responsibility for enforcing it. From [[06-Coupling-and-Cohesion]]: a class with one responsibility is cohesive; a class with many unrelated responsibilities is a God Object. From [[01-Object-Collaboration]]: responsibilities become collaborations when one object needs another to fulfill a use case.

CRC cards are the technique that operationalizes all of that *before* you commit to code. They are not a deliverable; they are a thinking tool.

## Why this layer exists

The standard failure mode of object design is to start coding immediately and discover, three months in, that `BankingService` has 47 methods, depends on 12 other classes, and cannot be tested without a database. The mistake was not in the coding; it was in skipping the design step where you would have noticed that `BankingService` was trying to own *everything*.

CRC cards exist to make that design step cheap enough that you actually do it. A stack of index cards costs a dollar. Walking through a use case takes 20 minutes. The cost of catching a God Object at the card stage is 1/1000th of the cost of catching it at the code stage.

## What is genuinely new here

Three things:

1. **The physical card is a forcing function.** A 4x6 index card holds about 3-5 responsibilities in readable handwriting. If you cannot fit them, the class is too big — split it. This is the same constraint that drives single-responsibility classes in code ([[01-SRP]]), but the card makes the constraint physical and immediate.
2. **Walking through use cases by pointing at cards is the act of design.** You narrate: "the client calls TransferService (point at TS card). TransferService asks Account to withdraw (point at Account card). Account needs to record a ledger entry (point at LedgerEntry card)." When a step has no obvious owner, you create a new card. When a card has too many responsibilities, you split. This is design by simulation.
3. **CRC cards prevent God Objects by making the symptoms visible early.** A card with 12 responsibilities is obviously wrong. A class with 12 methods is sometimes not obvious until it is too late. The card's small size makes the smell impossible to ignore.

## Concepts

- **CRC card** — a 4x6 (or similar) index card with three sections: Class name (top), Responsibilities (left), Collaborators (right).
- **Class** — the candidate class being designed. Named after the responsibility cluster, not after a noun in the requirements (though they often coincide).
- **Responsibility** — a short phrase describing something the class does or knows. "Know my balance." "Debit myself." "Coordinate the transfer."
- **Collaborator** — another class that this class sends messages to. Listed by name, not by reference.
- **Walkthrough** — the act of stepping through a use case by pointing at cards, narrating who does what and who talks to whom.
- **God Object** — a class with too many responsibilities. The card that does not fit is a God Object candidate.
- **Information holder, Service, Controller, Structurer** — wirfs-brock's role stereotypes; useful labels for the top of the card to remind you what kind of class this is.

## Banking application

Let's design the transfer flow ([[00-Banking-Case-Study]]) with CRC cards. Five cards:

### Card 1: TransferService

```text
┌──────────────────────────────────────────────┐
│ Class: TransferService            (Controller)│
├──────────────────────────────────────────────┤
│ Responsibilities:                             │
│  - Coordinate a transfer between two accounts│
│  - Enforce idempotency of transfer requests  │
│  - Decide sync vs async based on fraud result│
├──────────────────────────────────────────────┤
│ Collaborators:                                │
│  - TransferValidator                          │
│  - FraudService                               │
│  - Account (source, dest)                     │
│  - IdempotencyStore                           │
│  - NotificationService                        │
└──────────────────────────────────────────────┘
```

Three responsibilities. Five collaborators. The collaborators tell you this is a *coordinator* — it does not do the work, it asks others to do it. If `TransferService` also had "validate the request," "evaluate fraud," and "write ledger entries" as responsibilities, the card would not fit. That would be the God Object smell.

### Card 2: Account

```text
┌──────────────────────────────────────────────┐
│ Class: Account              (Information Holder)│
├──────────────────────────────────────────────┤
│ Responsibilities:                             │
│  - Know my balance                            │
│  - Know my status (PENDING/ACTIVE/FROZEN/CLOSED)│
│  - Debit myself (with overdraft rule)         │
│  - Credit myself                              │
│  - Enforce balance invariant                  │
├──────────────────────────────────────────────┤
│ Collaborators:                                │
│  - LedgerEntry (records mutations)            │
│  - OverdraftPolicy (decides if withdrawal ok) │
│  - AccountStatus (enum)                       │
└──────────────────────────────────────────────┘
```

Five responsibilities. They all belong together — they all protect the *same* invariant (balance == sum of ledger entries). The card is at the edge of fullness; that is correct for a rich domain entity.

If we tried to add "send a notification on large withdrawal" or "compute monthly interest," the card would not fit. That is the signal to *split*: move notification to `NotificationService`, move interest to `InterestService` (or to an `InterestPolicy` strategy — see [[04-Polymorphism]]).

### Card 3: LedgerEntry

```text
┌──────────────────────────────────────────────┐
│ Class: LedgerEntry         (Information Holder)│
├──────────────────────────────────────────────┤
│ Responsibilities:                             │
│  - Know my amount (signed)                    │
│  - Know my account and timestamp              │
│  - Be immutable                               │
├──────────────────────────────────────────────┤
│ Collaborators:                                │
│  - (none — primitive, depended-upon)          │
└──────────────────────────────────────────────┘
```

Three responsibilities. No collaborators. `LedgerEntry` is a *leaf* in the dependency graph (per [[03-Dependency-As-Root-Concept]]) — the most stable, most depended-upon concept. The card reflects that: nothing depends on from its side.

### Card 4: FraudService

```text
┌──────────────────────────────────────────────┐
│ Class: FraudService                    (Service)│
├──────────────────────────────────────────────┤
│ Responsibilities:                             │
│  - Evaluate a transfer for fraud risk         │
│  - Return: APPROVED / DENIED / PENDING        │
├──────────────────────────────────────────────┤
│ Collaborators:                                │
│  - FraudRule (multiple strategies)            │
│  - CustomerRiskProfile                        │
│  - AccountHistory                             │
└──────────────────────────────────────────────┘
```

Two responsibilities. Three collaborators. This is a *service* — no state of its own, orchestrates other objects. The card makes the role clear.

### Card 5: NotificationService

```text
┌──────────────────────────────────────────────┐
│ Class: NotificationService             (Service)│
├──────────────────────────────────────────────┤
│ Responsibilities:                             │
│  - Send notifications to customers            │
│  - Pick the right channel (email/SMS/push)    │
│  - Retry on failure                           │
├──────────────────────────────────────────────┤
│ Collaborators:                                │
│  - Customer (for contact info)                │
│  - EmailGateway, SMSGateway                   │
│  - RetryPolicy                                │
└──────────────────────────────────────────────┘
```

### Walking through the transfer use case

With the cards laid out on the table, narrate the transfer flow:

1. "Client calls **TransferService.transfer(request)**." (Point at TS card.)
2. "TransferService asks **IdempotencyStore** if this key was seen." (Point at IdempotencyStore — wait, that card is missing! Create it.)
3. "TransferService asks **TransferValidator** to validate the request." (Point at Validator card — also missing. Create it: one responsibility, 'validate the shape of a transfer request,' one collaborator, 'TransferRequest'.)"
4. "TransferService asks **FraudService** to evaluate." (Point at FraudService card.)
5. "FraudService asks **FraudRule** strategies and returns a result." (FraudRule card is missing. Create it: an interface, 'evaluate a transfer for risk,' collaborators: 'CustomerRiskProfile, AccountHistory'.)"
6. "TransferService asks **Account (source)** to withdraw." (Point at Account card.)
7. "Account asks **OverdraftPolicy** whether the withdrawal is allowed." (Already on the Account card as a collaborator. Good.)
8. "Account creates a **LedgerEntry** for the debit." (Point at LedgerEntry card.)
9. "TransferService asks **Account (dest)** to deposit." (Same Account card; different instance.)
10. "TransferService stores the result in **IdempotencyStore**."
11. "TransferService tells **NotificationService** to notify."
12. "TransferService returns the result to the client."

By the end of the walkthrough, you have:

- Five initial cards, plus three created during the walkthrough (IdempotencyStore, TransferValidator, FraudRule).
- A clear picture of who talks to whom.
- A clear picture of which responsibilities have natural owners and which were missing.
- No card has more than five responsibilities. No card has more than five collaborators. (If one did, that would be the signal to split.)

### How CRC cards prevent God Objects

The classic God Object — `BankingService` with `openAccount`, `transferMoney`, `computeInterest`, `sendNotification`, `generateStatement`, `detectFraud` — would be impossible to fit on a card. The card forces the designer to confront the question: "what does this class *not* do?"

```text
┌──────────────────────────────────────────────┐
│ Class: BankingService         (DOES NOT FIT)   │
├──────────────────────────────────────────────┤
│ Responsibilities:                             │
│  - Open accounts                              │
│  - Transfer money                             │
│  - Compute interest                           │
│  - Send notifications                         │
│  - Generate statements                        │
│  - Detect fraud                               │
│  - ... (card full; cannot fit more)           │
└──────────────────────────────────────────────┘
```

The physical constraint of the card makes the smell unavoidable. The cure is to split:

- `AccountService` — open, freeze, close accounts
- `TransferService` — coordinate transfers
- `InterestService` — accrue interest
- `NotificationService` — send notifications
- `StatementService` — generate statements
- `FraudService` — evaluate fraud

Each of those fits on a card. Each has one cohesive responsibility cluster. Each is testable in isolation. The card forced the right design.

### Why physical cards matter

You can do CRC exercises with sticky notes, with a whiteboard, or with a digital tool. None of them are as effective as physical 4x6 index cards, for three reasons:

1. **The size is fixed.** A 4x6 card holds about 3-5 responsibilities in handwriting. A digital card can be resized, and the temptation to add "just one more" is real.
2. **Cards can be picked up and moved.** When you walk through a use case, you arrange the cards on the table to show the current collaboration. You can pick up a card and ask, "what if this class did not exist?" You can move a responsibility from one card to another physically — and the act of moving makes the trade-off concrete.
3. **Cards are disposable.** You do not feel guilty throwing away a card and starting over. You feel very guilty deleting a class file with 200 lines of code. The disposability encourages iteration.

CRC cards are not a deliverable. They are a thinking tool. After the walkthrough, you transcribe the conclusions into code and throw the cards away. (Or keep one or two as design documentation, if the design was non-obvious.)

## What can go wrong

1. **Treating CRC cards as deliverables.** Polishing the cards, putting them in a wiki, updating them after the code has drifted — this is ceremony without benefit. The card's value is in the *conversation* it forces during design. Once code exists, the code is the source of truth.
2. **Skipping the walkthrough.** Writing the cards without walking through use cases is just writing a list. The walkthrough is where the design happens — where you discover missing classes, missing responsibilities, and God Objects.
3. **Too many cards.** A use case that produces 30 cards has over-decomposed the problem. Each card is a class; each class is an indirection. Aim for 5-10 cards per use case; more than that, look for clusters that can be merged.
4. **Too few cards.** A use case with two cards (Client and BankingService) has under-decomposed the problem. Look for responsibilities that are buried inside a card and ask whether they should be their own card.
5. **Doing CRC alone.** The technique is most powerful as a group exercise — two or three engineers walking through the cards together, disagreeing, splitting, merging. Solo CRC is better than nothing, but it loses the diversity of perspectives that catches mistakes.
6. **Forgetting role stereotypes.** A card that is simultaneously a Controller, an Information Holder, and a Service is doing too much. Label the card with one role; if you cannot pick one, split.

## Trade-offs

- **Upfront design vs emergent design.** CRC is upfront design — you think before you code. The alternative is emergent design — you code first and refactor. Both work; CRC is faster for domains you understand well, and emergent is faster for domains you are exploring. Banking is well understood; CRC fits.
- **Card size as a constraint.** The 4x6 card is a heuristic, not a law. Some legitimate classes (a rich domain entity) have 5-7 responsibilities. The card is a forcing function for *questioning*, not a hard limit. If a card is full, ask "do these responsibilities really belong together?" — and only split if the answer is no.
- **Documentation vs thinking tool.** Cards are thinking tools. If you need documentation, write the design as a markdown file or a UML diagram ([[01-Class-Diagrams]]) after the cards have done their job. Do not try to maintain the cards as living documentation.
- **Physical vs digital.** Physical cards have the advantages above. Digital cards are searchable, shareable, and survive the cleanup of the meeting room. If your team is remote, digital is the only option — use a tool that enforces a small card size to preserve the constraint.

## Forward links

- [[04-Responsibilities]] — the foundational chapter on responsibility-driven design.
- [[01-Objects-And-Classes]] — turning CRC conclusions into actual classes.
- [[01-Object-Collaboration]] — turning the collaborator lists into message sequences.
- [[01-SRP]] — the SOLID formalization of "one responsibility per class."
- [[05-Anti-Patterns]] — the God Object anti-pattern that CRC prevents.
- [[01-Class-Diagrams]] — the UML artifact that often follows from a CRC walkthrough.
- [[00-LLD-Method]] — the design method that uses CRC cards as an early step.
