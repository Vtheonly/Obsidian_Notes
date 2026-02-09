
### 2025 Retake

**Year:** 2025
**Type:** Retake
**Correction:** Yes

#### Exercise 1 (10 pts)

**Statement:**
1.  Give 3 different ways to translate this query into relational algebra: `SELECT * FROM T1, T2 WHERE T1.b = T2.b AND T2.b = 1`.
2.  Calculate the number of instructions for each example of relational expression considering that restrictions are performed by a full scan on unsorted lists (like FOR loops) and assuming each operation is performed separately.
    *   *Hypothesis:* Table T1 has 100 tuples ($n_1$), T2 has 10 tuples ($n_2$). $n_3$ is the result of the join.
3.  Perform the calculations for three values of $n_1, n_2$, and $n_3$ (minimum, maximum, and median).
4.  Give an interval `[min..max]` independent of $n_1, n_2, n_3$.
5.  Conclude by indicating which operation requires the fewest instructions. Justify your answer.

#### Exercise 2 (10 pts)

**Statement:**
1.  Explain why this query (involving joins and sorting on price) might pose performance problems when the database contains many records.
2.  Propose and justify a first optimization solution to implement that will be useful in all cases and will have few undesirable effects.
3.  Propose two alternative solutions which, if we stay in the relational model, would allow considerably improving performance. State the advantages, disadvantages, and measures to take to contain these disadvantages.

#### Correction

**Exercise 1:**

**1. Three Translations:**
1.  $\sigma_{T2.b=1}(T1 \bowtie T2)$
2.  $T1 \bowtie \sigma_{b=1}(T2)$
3.  $T2 \bowtie \sigma_{b=1}(T1)$ (Note: Logic assumes b exists in T1 too based on join condition T1.b=T2.b)

**2. Instruction Calculation:**
*   **Case 1:** Restriction($T1 \bowtie T2$)
    *   Join: $100 \times 10 = 1000$ instructions. Returns $n_3$ tuples.
    *   Restriction: $n_3$ instructions.
    *   **Total:** $1000 + n_3$.
*   **Case 2:** Join($T1$, $\sigma_{b=1}(T2)$)
    *   Restriction on T2: 10 instructions. Returns $n_2'$ tuples.
    *   Join: $n_2' \times 100$.
    *   **Total:** $10 + (n_2' \times 100)$.
*   **Case 3:** Join($T2$, $\sigma_{b=1}(T1)$)
    *   Restriction on T1: 100 instructions. Returns $n_1'$ tuples.
    *   Join: $n_1' \times 10$.
    *   **Total:** $100 + (n_1' \times 10)$.

**4. Calculations (Min, Max, Median):**
*   *(Detailed numeric calculations provided in the correction document based on variable tuple counts).*
*   Example Median ($n_3=500, n_2=5, n_1=50$):
    *   Case 1: $1000 + 500 = 1500$.
    *   Case 2: $10 + 5 \times 100 = 510$.
    *   Case 3: $100 + 50 \times 10 = 600$.

**6. Conclusion:**
In (almost) all cases, queries 2 and 3 are more efficient than 1 (it is better to perform restriction before join). The choice between 2 and 3 depends on $n_1$ and $n_2$.
A case where joining first might be preferred is if $n_3 = 0$ (no matching tuples), though the gain is marginal.
The query engine must:
*   Decide the order of operations.
*   Have *a priori* information on table volumes ($10$ vs $100$).
*   Have *a priori* information on result selectivity ($n_1', n_2', n_3$).

**Exercise 2:**

**1. Performance Problems:**
*   Problems are linked to the **Sort** (on price) and **Joins** executed between all tables to extract figurine lists with characteristics.

**2. First Optimization:**
*   **Indexing** the *price* field. This accelerates the sorting operation with negligible side effects (slight slowing of updates/disk usage).

**3. Alternative Solutions:**
1.  **Denormalization:** Eliminate joins by merging tables.
    *   *Disadvantage:* Redundancy.
    *   *Measure:* Control redundancy via Application logic or Triggers.
2.  **Materialized View:** Pre-calculate joins and sort.
    *   *Advantage:* Fast read.
    *   *Disadvantage:* Data lag (not real-time).
    *   *Measure:* Refresh view periodically or via triggers on update.
3.  **Partitioning:** (Note: Correction states partitioning is of no interest here because the query requires all data/attributes, unless partitioned by price, but union would be needed before sorting).