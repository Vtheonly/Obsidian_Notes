# Functional Dependencies — The Engine of Normalization

> Functional dependencies (FDs) are the single most important formal concept in relational theory. They are the input to every normal form from 2NF onward. They are also, in disguise, the same concept as **dependency** in [[03-Dependency-As-Root-Concept]] — a constraint of the form "if you know X, you know Y." Master FDs and normalization stops being rules to memorize; it becomes reasoning.

## What you already know

From [[03-Dependency-As-Root-Concept]]: a dependency is "a change in one place can force a change in another." A functional dependency is the *strictest* form: "if X is the same, Y must be the same — always, no exceptions."

From [[02-Keys-Superkeys-Candidate-Keys]]: a superkey is a set of attributes that uniquely identifies a tuple. Equivalently, $K$ is a superkey iff $K \to$ all attributes. Keys *are* a special case of FDs.

From [[06-Coupling-and-Cohesion]]: a relation is cohesive when it holds one fact type. FDs are the formal test for that — if a relation has FDs that do not follow from its key, it is holding multiple fact types, and it should be decomposed.

## Why this layer exists

Without FDs, "normalize this schema" is folklore — apply rules 1NF, 2NF, 3NF, BCNF in order and hope. With FDs, normalization is **algorithmic**: given a set of FDs, you can compute (a) all the candidate keys, (b) whether the schema is in BCNF, (c) a lossless BCNF decomposition. The whole of normalization theory is *inference over FDs*.

FDs are also how we *discover* the design of a schema from a real domain. You interview a domain expert ("if you know the IBAN, do you know the balance?"), translate their answers into FDs, and then normalize. The FDs are the bridge from natural language to schema.

## What is genuinely new

Three formal things:

1. The **definition** of a functional dependency.
2. **Armstrong's axioms** — the sound and complete inference rules for FDs.
3. The **closure** of a set of FDs and the **attribute closure** of a set of attributes — the tools that let you compute "all FDs that follow from these" and "is this set a superkey?"

## Concepts

### Definition

Let $R$ be a relation with attribute set $U$. Let $X, Y \subseteq U$. A **functional dependency** (FD) $X \to Y$ holds on $R$ iff, for every pair of tuples $t_1, t_2 \in R$:

$$\text{if } t_1[X] = t_2[X] \text{ then } t_1[Y] = t_2[Y]$$

Read it as: "**X determines Y**" or "**Y is functionally dependent on X**."

The FD is a *constraint* on the relation — it must hold for every legal instance of $R$, not just for the rows currently in the table. If you ever insert two rows that agree on $X$ but disagree on $Y$, the FD is violated.

Notes:

- $X$ is called the **determinant**; $Y$ is the **dependent**.
- If $X \to Y$ and $Y \to X$, we say $X \leftrightarrow Y$ (they are equivalent).
- If $Y \subseteq X$, the FD is **trivial** (it always holds, e.g., $\{iban, balance\} \to \{iban\}$).
- An FD $X \to Y$ where $Y$ is a single attribute is called a *simple* FD.

### Armstrong's axioms

Three inference rules that are **sound** (every FD derived is genuinely implied) and **complete** (every implied FD can be derived). They are the only rules you need.

1. **Reflexivity**: if $Y \subseteq X$, then $X \to Y$. (Trivial dependencies.)
2. **Augmentation**: if $X \to Y$, then $XZ \to YZ$ for any $Z$. (You can add attributes to both sides.)
3. **Transitivity**: if $X \to Y$ and $Y \to Z$, then $X \to Z$.

From these three, two useful derived rules follow:

- **Union**: if $X \to Y$ and $X \to Z$, then $X \to YZ$.
- **Decomposition**: if $X \to YZ$, then $X \to Y$ and $X \to Z$.

These two together mean: any FD $X \to Y$ is equivalent to a set of FDs $X \to A_i$ for each attribute $A_i \in Y$. We can always work with single-attribute right-hand sides.

### FD closure ($F^+$)

Given a set $F$ of FDs, the **closure** $F^+$ is the set of *all* FDs that can be derived from $F$ via Armstrong's axioms. $F^+$ includes the trivial FDs and every consequence. $F^+$ is typically exponentially larger than $F$ — we never compute it directly; we compute attribute closures instead.

### Attribute closure ($X^+$)

Given $F$ and a set of attributes $X$, the **attribute closure** $X^+$ is the set of all attributes $A$ such that $X \to A$ is in $F^+$.

Algorithm:

```
X⁺ := X
repeat:
    changed := false
    for each FD (W → V) in F:
        if W ⊆ X⁺ and V ⊄ X⁺:
            X⁺ := X⁺ ∪ V
            changed := true
until not changed
return X⁺
```

$X^+$ is the most-used tool in normalization. Three immediate uses:

1. **Is $X$ a superkey?** Yes iff $X^+ = U$ (all attributes).
2. **Is $X$ a candidate key?** Yes iff $X^+ = U$ and no proper subset of $X$ has this property.
3. **Does $X \to A$ hold?** Yes iff $A \in X^+$.

### Finding FDs in practice

You do not derive FDs from data — you *discover* them from the domain. The data can only falsify an FD (by showing a counterexample); it can never confirm one (because the next row might violate it).

The process:

1. **Interview**: "If you know the IBAN, can there be two different balances? Can there be two different customers? Two different statuses?" Translate yes/no answers into FDs.
2. **Verify against data**: query for counterexamples. `SELECT iban, COUNT(DISTINCT balance) FROM accounts GROUP BY iban HAVING COUNT(DISTINCT balance) > 1`. If any row is returned, the FD `{iban} → {balance}` does *not* hold (or your data is dirty).
3. **Document the FDs** alongside the schema. They are part of the design, not a derivative.

This is the same "interview then verify" discipline as in domain modeling — see [[03-Domain-Concepts]].

## Banking application

For the `accounts` relation with attributes `{id, iban, balance, status, customer_id}`, the FDs that hold are:

1. `{id} → {iban, balance, status, customer_id}` — the surrogate PK determines everything.
2. `{iban} → {id, balance, status, customer_id}` — the natural key determines everything (because IBAN is also a candidate key).
3. `{customer_id, iban} → {id, balance, status}` — by augmentation and transitivity from (2).
4. Trivial FDs: `{id, iban} → {id}`, etc.

Computing the attribute closure of `{id}`:

```
{id}⁺ = {id}
  apply (1): {id}⁺ = {id, iban, balance, status, customer_id}  (= all attributes)
{id}⁺ = U  ⟹  {id} is a superkey (and minimal, so it is a candidate key).
```

Similarly, `{iban}^+ = U`, so `{iban}` is also a candidate key. `{customer_id}^+ = {customer_id}` — not a superkey (a customer may have many accounts). `{balance}^+ = {balance}` — not a superkey.

So `accounts` has two candidate keys: `{id}` and `{iban}`. We choose `{id}` as the primary key for FK-convenience (see [[02-Keys-Superkeys-Candidate-Keys]]).

For a *denormalized* relation `accounts_with_customer` with attributes `{account_id, iban, balance, customer_id, customer_name, customer_tax_id}`, additional FDs hold:

- `{customer_id} → {customer_name, customer_tax_id}` — customer facts depend on customer, not on account.
- `{account_id} → {customer_id}` (and hence, transitively, `{account_id} → {customer_name, customer_tax_id}`).

This transitive dependency is the signature of a 3NF violation — see [[06-1NF-2NF-3NF]]. The fix is to decompose `accounts_with_customer` into `accounts` and `customers`, with a FK from `accounts.customer_id` to `customers.id`.

## Code

### Documenting FDs in SQL — there is no native syntax

SQL has no `DECLARE FUNCTIONAL DEPENDENCY` statement. FDs are *enforced* via constraints (PK, UNIQUE, FK, CHECK) but they are not *named* as FDs. Documenting them is a discipline:

```sql
-- accounts relation:
--   FD1: {id} -> {iban, balance, status, customer_id}     enforced by PRIMARY KEY (id)
--   FD2: {iban} -> {id, balance, status, customer_id}     enforced by UNIQUE (iban)
--   FD3: {customer_id} -> {} (no FD; one customer has many accounts)
```

### Verifying an FD against data

```sql
-- Verify {iban} -> {balance} (should hold if FD2 holds).
-- If this query returns any rows, the FD is violated (or data is dirty).
SELECT iban, COUNT(DISTINCT balance) AS distinct_balances
FROM accounts
GROUP BY iban
HAVING COUNT(DISTINCT balance) > 1;

-- Verify {customer_id} -> {} does NOT hold (one customer, many accounts).
-- This should return many rows.
SELECT customer_id, COUNT(*) AS account_count
FROM accounts
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

### PostgreSQL: query for hidden FDs

Some FDs are implied by the schema (via PK and UNIQUE) but not enforced elsewhere. You can query the catalog to discover declared keys:

```sql
-- List all candidate keys (PK + UNIQUE) of accounts
SELECT conname, contype, pg_get_constraintdef(oid) AS def
FROM pg_constraint
WHERE conrelid = 'accounts'::regclass
  AND contype IN ('p', 'u');   -- p = primary key, u = unique
```

PostgreSQL does not infer FDs across joins; the planner does use *some* FD reasoning (e.g., knowing that `GROUP BY primary_key` implies `GROUP BY all columns`), but only for keys declared in the catalog. See [[07-Cost-Based-Optimizer]].

## What can go wrong

- **Assuming an FD from a small sample.** "Every account in our test data has one customer, so `{account_id} → {customer_id}`." But if accounts can be jointly held, the FD is wrong, and a 2NF decomposition based on it will be wrong. Always verify against domain rules, not data.
- **Confusing FD with implication over time.** An FD is a constraint on the *current* legal state, not a statement about history. `{customer_id} → {customer_name}` is an FD; "this customer used to be called X" is a *slowly changing dimension* problem (see [[02-Denormalization-For-Reads]]).
- **Hidden transitive dependencies.** `{A} → {B}` and `{B} → {C}` together imply `{A} → {C}`. If you declare only the first two as constraints, the third is implied — but a denormalized table that includes $A$, $B$, $C$ in one relation violates 3NF whether or not you "declared" the transitive FD. The FD exists by virtue of the data, not by declaration.
- **Multi-valued dependencies (MVDs) mistaken for FDs.** An FD says "same X implies same Y." An MVD says "same X implies a *set* of Y values, independent of other attributes." Conflating them leads to wrong decompositions — see [[08-4NF-5NF]].
- **NULL breaking FD semantics.** If `customer_tax_id` is nullable, two accounts with `customer_id = 701` and one NULL `tax_id` and one non-NULL `tax_id` — does the FD `{customer_id} → {tax_id}` still hold? SQL's three-valued logic makes this murky. The model says: make the column NOT NULL or decompose so the FD lives in a table where it always holds. See [[02-Domain-Check-Constraints]].

## Trade-offs

- **Strict FDs vs. real-world exceptions.** "IBAN determines currency" is an FD in the EU (one IBAN, one currency). It is *not* an FD globally (some non-EU IBANs have been re-denominated). Strict FDs make for clean schemas; real-world exceptions force either weaker constraints or separate tables. The trade-off is normalization purity vs. modeling fidelity.
- **Enforcing FDs via constraints vs. triggers.** PK and UNIQUE enforce FDs declaratively. FDs that span relations (e.g., "an account's currency must equal its customer's country currency") require triggers or application checks. Declarative is preferred; see [[03-Triggers-As-Constraints]].
- **Discovering FDs late.** If you discover an FD after the schema is in production, you may find dirty data that violates it. You then face: clean the data, weaken the FD, or split the table. Each is a real cost.
- **Over-decomposing.** A schema that decomposes every FD into its own table is in BCNF but is impossible to query without five-way joins. The trade-off is normalization vs. read performance — see [[10-Normalization-Trade-offs]] and [[02-Denormalization-For-Reads]].

## Forward links

- [[04-Relational-Algebra]] — FDs are used by the optimizer to simplify queries.
- [[06-1NF-2NF-3NF]] — partial and transitive FDs are the violations 2NF and 3NF target.
- [[07-BCNF]] — "every determinant is a candidate key" is an FD-based definition.
- [[08-4NF-5NF]] — multi-valued and join dependencies, the next generalizations.
- [[03-Domain-Concepts]] and [[00-ER-Modeling]] — where FDs come from in practice.
- [[06-Coupling-and-Cohesion]] — FDs are the formal test for relational cohesion.
- [[07-Cost-Based-Optimizer]] — the planner's FD-based simplifications.
