# Relational Algebra & Formal Foundations

Relational Algebra is the formal, **procedural** query language underlying all relational databases. When you submit a declarative SQL query, the DBMS parser translates it into a relational algebra expression (logical plan) before optimization (see [[01 - Query Processing, Algebraic Rewriting & Cost Estimation]]).

---

## 1. Set Semantics vs. Bag (Multiset) Semantics

- **Relational Algebra (Theory — Sets):** Relations are strict mathematical **sets**.
  - **No duplicates:** $\{A, B, A\}$ is automatically reduced to $\{A, B\}$. Every algebraic projection ($\pi$) implicitly deduplicates.
  - **Unordered:** Row order has no semantic meaning.
- **SQL (Practice — Bags / Multisets):** SQL tables and query results are **bags**.
  - **Duplicates allowed:** `SELECT col FROM R` keeps duplicate rows unless `SELECT DISTINCT` is specified.
  - **Ordering:** Unordered unless `ORDER BY` is explicitly added.

> [!TIP] Exam Tip
> When computing the **Relational Algebra** result of $\pi$, always eliminate duplicate rows. When tracing **SQL**, preserve duplicates unless `DISTINCT` (or set operators `UNION`/`INTERSECT`/`EXCEPT` without `ALL`) is used.

---

## 2. Unary Operators (Single Relation)

### Selection ($\sigma$) — Horizontal Slicing

Filters **rows** satisfying predicate $C$, preserving the full schema (columns):
$$\sigma_{C}(R)$$

- **SQL equivalent:** `WHERE` clause.
- **Commutativity:** $\sigma_{C_1}(\sigma_{C_2}(R)) \equiv \sigma_{C_2}(\sigma_{C_1}(R)) \equiv \sigma_{C_1 \land C_2}(R)$.

### Projection ($\pi$) — Vertical Slicing

Extracts specified **columns** $A_1, \dots, A_k$ and eliminates duplicates created by dropping distinguishing columns:
$$\pi_{A_1, \dots, A_k}(R)$$

- **SQL equivalent:** `SELECT DISTINCT A1, ..., Ak`.
- **Cascading:** $\pi_{L_1}(\pi_{L_2}(R)) \equiv \pi_{L_1}(R)$ whenever $L_1 \subseteq L_2$.

### Rename ($\rho$)

Renames a relation and/or its attributes, **mandatory for Self-Joins** and disambiguating shared column names:
$$\rho_{S(B_1, \dots, B_n)}(R) \quad \text{or} \quad \rho_{t_1}(\text{teacher})$$

- **Shortcut notation in course slides:** $NewRel(Col_1, Col_2, \dots) = R_1 \times R_2$ renames output attributes left-to-right sequentially (must match exact column count).

---

## 3. Binary Set Operators

> [!WARNING] Union Compatibility Requirement
> Before applying $\cup$, $\cap$, or $-$, both relations $R$ and $S$ must satisfy:
>
> 1. **Same Arity (Degree):** Equal number of columns.
> 2. **Domain Compatibility:** The $i$-th column of $R$ and the $i$-th column of $S$ must have compatible data types.

| Operator         |   Symbol   | Logic                                   | SQL Equivalent                   | Algebraic Laws                                                   |
| :--------------- | :--------: | :-------------------------------------- | :------------------------------- | :--------------------------------------------------------------- |
| **Union**        | $R \cup S$ | Tuples in $R$ **OR** $S$ (deduplicated) | `UNION` (`UNION ALL` keeps bags) | Commutative, Associative                                         |
| **Intersection** | $R \cap S$ | Tuples in **BOTH** $R$ **AND** $S$      | `INTERSECT`                      | Commutative, Associative; equals $R - (R - S)$                   |
| **Difference**   |  $R - S$   | Tuples in $R$ and **NOT** in $S$        | `EXCEPT` (Oracle `MINUS`)        | **Not commutative** ($R - S \neq S - R$); $R - (S - R) \equiv R$ |

---

## 4. The Join Family ($\bowtie$) & Cartesian Product ($\times$)

### A. Cartesian Product ($R \times S$)

Concatenates every tuple of $R$ with every tuple of $S$. Result cardinality is $|R| \times |S|$; degree is $\text{deg}(R) + \text{deg}(S)$. Rarely desired alone because of combinatorial explosion; serves as the formal basis for joins.

### B. Theta-Join ($\bowtie_\theta$) and Equi-Join ($\bowtie_=$)

Defined mathematically as a Cartesian product followed by a selection:
$$R \bowtie_{\theta} S = \sigma_{\theta}(R \times S)$$

- **Theta-Join:** $\theta$ can use any comparison ($<, \le, >, \ge, =, \neq$).
- **Equi-Join:** $\theta$ uses strictly equality ($R.k = S.k$). Retains both join columns side-by-side (`INNER JOIN ... ON`).

### C. Natural Join ($R \bowtie S$)

1. Automatically equi-joins on all attributes sharing the **exact same name and domain** in both $R$ and $S$.
2. **Eliminates the duplicate join column** from the output schema.
   _(If $R$ and $S$ share no attribute names, $R \bowtie S = R \times S$. Warning: dangerous in production SQL because adding an unrelated same-named column like `notes` to both tables silently alters the join condition!)_

### D. Semi-Joins ($\ltimes, \rtimes$) and Anti-Joins ($\triangleright, \triangleleft$)

- **Left Semi-Join ($R \ltimes S$):** Returns tuples of $R$ that have **at least one match** in $S$, keeping **only columns of $R$** (e.g., producers who produced at least one product; conceptually `WHERE EXISTS`).
- **Left Anti-Join ($R \triangleright S$):** Returns tuples of $R$ that have **zero matches** in $S$ (e.g., producers who never produced a product; conceptually `WHERE NOT EXISTS`).

### E. Outer Joins ($\leftouterjoin, \rightouterjoin, \fullouterjoin$) & 5-Step Mechanism

Outer joins preserve unmatched tuples by padding missing columns with `NULL`:

- **Left Outer Join ($R \leftouterjoin S$):** Keeps all rows from $R$, padding unmatched $S$ attributes with `NULL`.
- **Right Outer Join ($R \rightouterjoin S$):** Keeps all rows from $S$, padding unmatched $R$ attributes with `NULL`.
- **Full Outer Join ($R \fullouterjoin S$):** Keeps all rows from both $R$ and $S$.

**Mathematical 5-Step Outer Join Construction** (e.g., `Producteur(Nom, Prenom, Produit_ID)` $\fullouterjoin$ `Produit(Id, Nom)`):

1. **Cartesian Product:** Form all pairs of $R_1 \times R_2$.
2. **Nullify Left Orphans:** For each row of $R_1$ whose join key matches no $R_2$, set $R_2$'s columns on those unmatched pairings to `NULL`.
3. **Nullify Right Orphans:** For each row of $R_2$ whose join key matches no $R_1$, set $R_1$'s columns to `NULL`.
4. **Deduplicate:** Eliminate duplicate null-padded rows introduced in steps 2–3.
5. **Consolidate Join Column:** Merge matching join keys (`Produit_ID` and `Id`) into one column (producing matched rows, left-only orphans, and right-only orphans). Left Outer discards right orphans; Right Outer discards left orphans.

---

## 5. The Division Operator ($\div$)

Division answers **universal quantification** queries: _"Find every $A$ in $R$ associated with **ALL** $B$ values in $S$."_ (Keywords: "all", "every").

### Derivation Using Double Negation

Given $R(A, B)$ and $S(B)$:
$$R \div S = \pi_A(R) - \pi_A\big((\pi_A(R) \times S) - R\big)$$

1. $\pi_A(R)$: All candidate $A$ values.
2. $\pi_A(R) \times S$: The "perfect world" where every candidate $A$ is paired with every required $B \in S$.
3. $(\pi_A(R) \times S) - R$: All **missing pairs** (what candidates failed to satisfy).
4. $\pi_A(\dots)$: Disqualified candidates who missed at least one item.
5. Subtracting disqualified candidates from all candidates leaves only those associated with **every** item in $S$.

**Worked Example:** Suppose $R = \{(A,1), (A,2), (B,1), (C,1), (C,2)\}$ and $S = \{1, 2\}$.

- Candidates $\pi_{\text{User}}(R) = \{A, B, C\}$.
- Ideal world $\pi_{\text{User}}(R) \times S$ has 6 pairs; subtracting $R$ leaves the single missing pair $\{(B, 2)\}$.
- Disqualified = $\{B\}$. Final result $R \div S = \{A, B, C\} - \{B\} = \{A, C\}$.

### Two SQL Implementations

_Example: Find students enrolled in ALL `'Core'` courses:_

- **Method 1 — Double `NOT EXISTS`** (literally _"students for whom there is NO Core course that they have NOT enrolled in"_):

```sql
SELECT S.Name
FROM Student S
WHERE NOT EXISTS (
    SELECT C.CourseID
    FROM Courses C
    WHERE C.Type = 'Core'
      AND NOT EXISTS (
          SELECT 1 FROM Enrolled E
          WHERE E.StudentID = S.StudentID AND E.CourseID = C.CourseID
      )
);
```

- **Method 2 — `GROUP BY` + `HAVING COUNT(DISTINCT ...)`:**

```sql
SELECT StudentID
FROM Enrolled
WHERE CourseID IN (SELECT CourseID FROM Courses WHERE Type = 'Core')
GROUP BY StudentID
HAVING COUNT(DISTINCT CourseID) = (SELECT COUNT(*) FROM Courses WHERE Type = 'Core');
```

_(Caveat: Method 2 assumes the divisor set is non-empty; if 0 `'Core'` courses exist, `NOT EXISTS` returns all students vacuously while `HAVING` returns none.)_

---

## 6. Extended Relational Algebra: Scalar Functions & Aggregation ($\lambda$)

- **Pattern Matching (`LIKE`):** `_` matches **exactly one** character (e.g., $\sigma_{Nom\ \text{LIKE}\ '\_a\%'}(\text{Employé})$ finds names whose second letter is `'a'`, $\sigma_{Nom\ \text{LIKE}\ 'T\_\_\_\_\_'}$ matches 6-letter names starting with `'T'`); `%` matches **zero or more** characters. Transformation functions like `UPPER()`, `LOWER()`, `LENGTH()`, `CONCAT()`, `LEFT()`, `RIGHT()`, `MID()` work inside $\sigma$ and $\pi$.
- **Arithmetic:** `+`, `-`, `*`, `/`, `^`, `div` (integer division, $5\ \text{div}\ 2 = 2$), `mod` ($5\ \text{mod}\ 2 = 1$), `ABS()`, `COS`, `SIN`, `LOG`, `ROUND`, `FLOOR`, `CEIL` (e.g., $\sigma_{Salaire * 1.05 < 25000}(\text{Employé})$).
- **Aggregate Operator ($\lambda$ or $\mathcal{G}$):** Supports `COUNT`, `MIN`, `MAX`, `SUM`, `AVG`.
  - _Global:_ $R' = \lambda_{\text{COUNT}(IdProduit)}(\text{Producteur})$ returns 1 scalar row.
  - _Grouped:_ $R' = Nom, Pr\acute{e}nom\ \lambda_{\text{COUNT}(IdProduit)}(\text{Producteur})$ groups by `(Nom, Prénom)` and creates column `COUNT_IdProduit` (`GROUP BY`).

---

## 7. SQL $\leftrightarrow$ Relational Algebra Mapping & Worked Translations

| SQL Clause                       | Algebraic Operator              | Notes                        |
| :------------------------------- | :------------------------------ | :--------------------------- |
| `SELECT DISTINCT x, y`           | $\pi_{x, y}$                    | Algebra is always distinct   |
| `FROM A, B`                      | $A \times B$                    | Cartesian product            |
| `WHERE x = 5`                    | $\sigma_{x=5}$                  | Selection                    |
| `JOIN ... ON ...`                | $\bowtie_{cond}$                | Theta / Equi-join            |
| `AS`                             | $\rho$                          | Mandatory for self-joins     |
| `UNION` / `INTERSECT` / `EXCEPT` | $\cup$ / $\cap$ / $-$           | Requires union-compatibility |
| `GROUP BY g` + `AGG(col)`        | $_{g}\lambda_{\text{AGG}(col)}$ | Grouping & aggregation       |

**Worked Construction Steps (Self-Join Example):** _"Find employees earning more than their manager."_

```sql
SELECT E.Name
FROM Employee E, Employee M
WHERE E.ManagerID = M.ID AND E.Salary > M.Salary;
```

1. Start from relations and rename instances via $\rho$: $\rho_E(\text{Employee})$ and $\rho_M(\text{Employee})$.
2. Join on manager relationship: $\rho_E(\text{Employee}) \bowtie_{E.ManagerID = M.ID} \rho_M(\text{Employee})$.
3. Apply salary selection $\sigma_{E.Salary > M.Salary}$ and final projection $\pi_{E.Name}$:
   $$\pi_{E.Name}\Big(\sigma_{E.Salary > M.Salary}\big(\rho_E(\text{Employee}) \bowtie_{E.ManagerID = M.ID} \rho_M(\text{Employee})\big)\Big)$$

_(For 20 more worked Relational Algebra $\leftrightarrow$ SQL query translations, see [[01 - Worked SQL & Relational Algebra Drills (Practice Bank)]].)_
