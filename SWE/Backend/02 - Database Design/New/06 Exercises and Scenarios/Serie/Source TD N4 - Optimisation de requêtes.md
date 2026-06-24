
# Source: TD N°4 - Optimisation de requêtes

**Context Schema:**
*   `Train (NoTrain, NoWagon)` - *Note: This schema implies a Train is composed of Wagons.*
*   `Wagon (NoWagon, TypeWagon, PoidsVide, Capacité, Etat, Gare)`
*   **Statistics provided:**
    *   `Train`: 60,000 tuples.
    *   `Wagon`: 200,000 tuples.
    *   `NoTrain` distinct values: 2,000.

---

### Exercise 1: Algebraic Tree Comparison

**Source:** TD 4 - Exercice 1
**Context:** Two algebraic trees are presented for the query "Find the wagon type for Train #4002".
*   **Tree (a):** Join $\to$ Select ($\sigma_{NoTrain=4002}$) $\to$ Project.
*   **Tree (b):** Select ($\sigma_{NoTrain=4002}$) on Train $\to$ Join $\to$ Project.

#### 1. Solution
**Q1. Equivalence:**
Both trees produce the same result because of the **Commutativity of Selection with Join**.
Algebraically: $\sigma_p(R \bowtie S) \equiv (\sigma_p(R)) \bowtie S$ (provided the predicate $p$ only concerns attributes of $R$).

**Q2. Data Volume (Cost Analysis):**
*   **Tree (a) [The Bad Tree]:**
    1.  **Join:** Joins 60,000 Trains with 200,000 Wagons. Assuming every wagon belongs to a train, the intermediate result has **200,000 rows** (or more if M:N).
    2.  **Selection:** Scans 200,000 rows to find those matching `#4002`.
    3.  **Total processed:** ~260,000 operations.
*   **Tree (b) [The Good Tree]:**
    1.  **Selection:** Filters `Train` table first. Since there are 2,000 distinct trains distributed over 60,000 rows, filtering for *one* specific train reduces the cardinality drastically (e.g., to ~30 rows).
    2.  **Join:** Joins only these ~30 rows with the `Wagon` table (using an index on `NoWagon`).
    3.  **Total processed:** A tiny fraction of the original size.

**Q3. SQL Query:**
```sql
SELECT W.TypeWagon
FROM Train T, Wagon W
WHERE T.NoWagon = W.NoWagon
  AND T.NoTrain = 4002;
```

#### 2. Reasoning
Optimization relies on the heuristic **"Push Selections Down"**. The earlier you filter data in the tree (closer to the leaves), the less work the upper nodes (Joins) have to perform.

#### 3. Detailed Explanation
*   **Tree (a)** represents a "Naive" execution plan. It constructs the entire universe of Trains and Wagons before checking which one we actually care about. It consumes massive memory and I/O.
*   **Tree (b)** represents an "Optimized" execution plan. By applying the filter `NoTrain=4002` immediately on the `Train` table, the input to the Join becomes negligible. The database engine only has to look up wagons for that specific train, skipping 99.9% of the data.

---

### Exercise 2: The Archaeology Database

**Source:** TD 4 - Exercice 2
**Context Schema:**
*   `Objet (num-obj, type, num-musée)`
*   `Musée (num-musée, nom)`
*   `Publication (num-pub, titre, date, éditeur)`
*   `Auteur (num-aut, nom, prénom)`
*   `Coopération (num-aut, num-pub)`
*   `Référence (num-pub, num-obj)`

**Target Query:** A complex SQL query linking all tables with specific filters (`A.nom='Vieille'`, `O.type='Mosaïque'`, `M.nom='Louvre'`).

#### 1. Solution

**Q1. What does the query do?**
"Find the titles and dates of publications written by the author 'Pierre Vieille' (published by 'Éditions archéologiques modernes') that reference 'Mosaic' type objects located in the 'Louvre' museum."

**Q2. Algebraic Trees (Worst vs. Best):**

*   **Tree 1: The Worst Possible (Canonical Tree)**
    *   **Root:** $\pi_{titre, date}$
    *   **Middle:** $\sigma_{Global\_Condition}$ (Huge AND condition)
    *   **Bottom:** Cartesian Product ($A \times C \times P \times R \times O \times M$)
    *   *Why it's bad:* It creates a Cartesian product of 6 tables before filtering anything. The size is $N_A \times N_C \times N_P \dots$ (Astronomically large).

*   **Tree 2: The Optimized Heuristic Tree**
    *   **Step 1 (Leaves):** Apply Selections ($\sigma$) immediately on base tables:
        *   $\sigma_{Nom='Vieille', Prénom='Pierre'}(Auteur)$
        *   $\sigma_{Editeur='Modernes'}(Publication)$
        *   $\sigma_{Type='Mosaïque'}(Objet)$
        *   $\sigma_{Nom='Louvre'}(Musée)$
    *   **Step 2 (Joins):** Join the filtered results using the most restrictive path first.
        *   Join (Filtered Author) $\bowtie$ (Cooperation)
        *   Join Result $\bowtie$ (Filtered Publication)
        *   Join (Filtered Museum) $\bowtie$ (Filtered Object)
        *   Join (Object Result) $\bowtie$ (Reference)
        *   Join everything together.
    *   **Step 3 (Root):** $\pi_{titre, date}$

#### 2. Reasoning
The SQL query provided puts all conditions in the `WHERE` clause. A naive parser might execute the joins first. The optimization task is to restructure this into a tree where:
1.  **Selections** are pushed to the bottom.
2.  **Projections** are pushed down (keep only Join Keys + Final Output columns).
3.  **Cartesian Products** are replaced by **Equi-Joins**.

#### 3. Detailed Explanation
*   **Heuristic 1: Selection Pushdown**: The condition `M.nom='Louvre'` is purely local to the `Musée` table. If the Louvre has 1,000 objects but the database has 100 museums, filtering this *before* joining with `Objet` saves processing 99 other museums' objects.
*   **Heuristic 2: Join Ordering**: It is usually better to join tables that have been heavily filtered first. For example, if there is only **1 author** named 'Vieille', joining `Auteur` with `Coopération` yields very few rows. Starting the join chain there is efficient.
*   **Pipelining**: In the optimized tree, the result of one operator is passed to the next without generating large temporary tables on disk, making the query execution real-time feasible.