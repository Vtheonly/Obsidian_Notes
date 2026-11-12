# 00 — Master Index & Curriculum Alignment

> [!INFO] About This Vault
> Full-depth restructured study vault for **Advanced Databases (BDA)**, **Academic Year 2026/2027**, taught by **Dr. ISHAK BOUSHAKI Saida** (Faculty of Sciences, Department of Computer Science, M'hamed Bougara University of Boumerdès — Master 1 GL / I2A).
>
> This vault integrates **all 2026/2027 course materials** (Lectures Chapters 1 & 2, TP 1, TD 1, TP 2, TD 2, TP 3, TD 3 on **PostgreSQL / pgAdmin 4** and **ISO/IEC SQL/PSM**) together with the **full depth of the prior vault** (Foundations, Relational Algebra, Keys, ER/MCD Modeling, Normalization, Joins, Integrity, Transactions/ARIES, Query Optimization/Indexing, Database Classifications/NoSQL, and Worked Practice Banks), eliminating redundant condensed summaries without losing knowledge.

---

## 1. Vault Structure & Reading Order

### Module 01 — Foundations & Database Design (Prerequisites & Theory)

1. [[01 - Database Concepts, Relational Model & SQL Overview]] — DB vs. spreadsheet, DBMS vs. RDBMS, ISO/IEC SQL vs. PostgreSQL, client/server decoupling, DDL/DML/DQL/DCL/TCL, naming conventions, 3 schema levels, formal relational terms, atomicity.
2. [[02 - Relational Algebra & Formal Foundations]] — Set vs. bag semantics, $\sigma, \pi, \rho, \cup, \cap, -, \times, \bowtie, \ltimes, \triangleright, \div$, 5-step outer-join derivation, division derivation, string/math/aggregate $\lambda$ notation, SQL-to-Algebra mapping, and 20 worked query translations.
3. [[03 - Keys, Data Types & Static Constraints (PostgreSQL)]] — Superkey, candidate, primary, alternate, surrogate vs. natural guide, simple/composite/compound, foreign keys, `NOT NULL` FKs, lookup tables, PostgreSQL & SQL data types, `CHECK` 3VL rules, `ON DELETE`/`ON UPDATE` actions, `ALTER TABLE`.
4. [[04 - Relationships & ER Modeling]] — 1:1 (single vs. split tables), 1:N, M:N (`teacher_class` & `student_classes` junction tables), weak vs. strong entities, Crow's Foot cardinality & modality, French E/A (MCD) rules (Borrowing ternary, derived/enumerated attributes, 1:1 migration, Teaching edge case), Reception & Airline MCD solutions.
5. [[05 - Normalization & Functional Dependencies]] — Anatomy of anomalies (`Dupuis`/`Martin`/`Dubois`), functional dependencies & Armstrong's axioms, 1NF (3 patterns), 2NF (`author/book`), 3NF (`review/star_rating`, `employee/dept`), BCNF, plus Apartment Occupancy & University Courses FD/3NF worked problems.

### Module 02 — Advanced SQL (`university` Database: Ch 1, TP 1 & TD 1)

6. [[01 - The University Database Setup, Constraints & DML]] — PostgreSQL & pgAdmin 4 setup, all 5 tables and exact seed data, dependency graph & insertion order, `INSERT`/`UPDATE`/`DELETE`, all 10 Part O integrity violation tests, Part P `ALTER TABLE`, Part Q checks, all 28 Part R exercises (`pg_constraint` & `information_schema`), and all 16 Part S Biology Challenge steps.
7. [[02 - Querying, Filtering, Aggregation & Joins]] — `SELECT` pipeline, quoting rules, `LIKE`/`ILIKE`, `NULL` semantics, scalar & aggregate functions, `GROUP BY` vs. `HAVING` vs. `WHERE`, complete join family (`CROSS`, `INNER`, `LEFT`, `RIGHT`, `FULL OUTER`, `SELF JOIN`, `NATURAL`, 3-table chains, `NOT NULL` FK effects, Video-Sharing & Diana Prince traces), TP 1 Part L, and TD 1 Q1*–19* & Q30.
8. [[03 - Set Operations, Subqueries, CTEs & CASE Expressions]] — `UNION`/`UNION ALL`/`INTERSECT`/`EXCEPT` vs. joins, `IN`/`NOT IN` NULL trap, `EXISTS`/`NOT EXISTS`, correlated subqueries, `ANY`/`SOME`/`ALL` equivalences & traps, relational division, CTEs (`WITH`), `CASE`, TD 1 Q20\*–29 & Q31, plus SQL optimization anti-patterns.

### Module 03 — Views & Server-Side Programming (Ch 2, TP 2–3 & TD 2–3)

9. [[01 - Standard Views, Updatability & Materialized Views]] — Standard & nested views, access control matrices (`T1/T2/V1/V2/V3`), "Max of Sums" & Division views (`R11`, `V20`, `V21`), updatability rules, `WITH [LOCAL] CHECK OPTION` & direct base-table bypass, materialized views (`REFRESH MATERIALIZED VIEW`), TP 2 Ex 1–3, and TD 2 Ex 1*–2*.
10. [[02 - Procedural SQL (SQL-PSM & PL-pgSQL), Control Flow & Exceptions]] — Declarative vs. procedural SQL, ISO SQL/PSM vs. PostgreSQL PL/pgSQL (`DO $$`, `:=`, `%TYPE`, `RECORD`, `ELSIF`, `FOUND`) vs. legacy MySQL/Oracle (`DELIMITER` mechanics, `@session` vs. local variables), `NULL` vs. missing row, loops (`FOR`, `WHILE`, `LOOP`, `REPEAT`, `CONTINUE WHEN`), exceptions (`division_by_zero`, `SQLERRM`, protected-block rollback, `SIGNAL`/`RESIGNAL`), TP 2 Ex 4–7, and TD 2 Ex 3\*–4, 6–8.
11. [[03 - Stored Functions, Stored Procedures & Dynamic SQL]] — Functions vs. procedures (`CALL` vs. `SELECT`), `IN`/`OUT`/`INOUT`, determinism & binlog replication hazard, TP 2 Ex 8–9 & 12, TD 2 Ex 9\*–15 (`number_of_teachers`, `average_salary`, `salary_category`, `calculate_increased_salary`, `increase_department_salaries`, `increase_teacher_salary`, `CASE` raises), Dynamic SQL (`PREPARE`/`EXECUTE`, `EXECUTE IMMEDIATE` & bind variables), and legacy Airline TD4 (`EffectifsHeure`, `PlusExperimente`, `factorielle`).
12. [[04 - Cursors & Row-by-Row Processing]] — 6-step explicit cursor lifecycle, `NOT FOUND` handlers vs. `EXIT WHEN NOT FOUND`, extra-`FETCH` trace, common cursor bugs, PL/pgSQL cursor `FOR` loops, cursor types & `FOR UPDATE` / `WHERE CURRENT OF`, cursor vs. set-based SQL, all TP 3 Ex 1–7 & 15, all TD 3 Ex 1\*–6, and legacy `total_hvol_AF` & `Gestion_Pilotes`.
13. [[05 - Recursive Queries (WITH RECURSIVE)]] — Hierarchies of unknown depth vs. non-recursive entity chains, self-referencing FKs, anchor vs. recursive member, `UNION ALL` vs. `UNION`, cycle risks, full $T_0 \to T_6$ trace, TP 2 Ex 11, TD 2 Ex 5, TP 3 Ex 8–14 & 16 (`manager` 6-row tree, subtrees, `::TEXT` paths, aggregates), and TD 3 Ex 7\*–9 (`parent_department_id`, 1..10, `n < 5` trace).

### Module 04 — Dynamic Integrity & Triggers

14. [[01 - Triggers, Automatic Auditing & Constraints vs Triggers]] — Static constraints vs. triggers (`TD 2 Ex 16*` `CHECK` vs. `NULL`), ECA model, `BEFORE`/`AFTER`/`INSTEAD OF`, row vs. statement scope, `OLD`/`NEW` & `IS DISTINCT FROM`, SQL/PSM vs. PostgreSQL 2-step triggers, salary auditing (`salary_history`/`salary_audit` & rollback atomicity), `INSTEAD OF INSERT` on `teacher_department_view`, `information_schema` & `pg_constraint`, plus all legacy triggers (`Process_Completed_Order`, `Clients_Audit`, `handle_order_cancellation`, Aviation TD4 `TrigDelQualif`, `TrigInsQualif`, `TrigUpdQualif`, `TrigInsGrade`, `CheckMaxQualif`).
15. [[02 - Schema-Level Assertions & Deferrable Constraints]] — `CREATE ASSERTION`, multi-table budget constraints, why modern DBMSs omit native assertions, cyclic FK bootstrap deadlock, `NOT DEFERRABLE` vs. `DEFERRABLE INITIALLY IMMEDIATE` vs. `INITIALLY DEFERRED`.

### Module 05 — Transactions, Concurrency & Recovery

16. [[01 - ACID Properties, Transaction Control & Crash Recovery]] — ACID + analogies, transaction states, Draft Mode / Auto-Commit / `SAVEPOINT` (`Easy Jet` script), crash behavior matrix, **TP 2 PostgreSQL transaction semantics** (reversible testing, trigger rollback, `EXCEPTION` block rollback), STEAL/NO-FORCE, WAL, `LSN`/`PrevLSN`/`CLR`, Checkpoints, ARIES 3 phases, 4 failure types, replication, and TD 5 Ex 1, 2, 5, 6.
17. [[02 - Concurrency Anomalies, Isolation Levels & Locking Protocols]] — Step-by-step traces for Dirty Read, Non-Repeatable Read, Phantom Read, Lost Update, Write-Skew; SQL isolation levels; S/X locks, 2PL/S2PL/SS2PL; Timestamp Ordering & Thomas Write Rule; OCC; MVCC; Deadlocks (Wait-Die, Wound-Wait, WFG); TD 5 Ex 3–4; `Gestion_Pilotes` `FOR UPDATE`.

### Module 06 — Query Optimization & Indexing

18. [[01 - Query Processing, Algebraic Rewriting & Cost Estimation]] — Parser/rewriter/CBO architecture, algebraic equivalences, 4 rewrite heuristics, catalog stats & selectivity formulas, Equi-Width vs. Equi-Depth histograms, periodic vs. sampling stats, mathematical proof of heuristic failure (`Film`/`Seance` $429$ vs. $464$ E/S), and TD 4 Trains & Archaeology DB analyses.
19. [[02 - Physical Join Algorithms & Database Indexing]] — Sequential/Index/Index-Only scans, SNLJ, INLJ, SMJ, HJ + Grace Hash Join (full pseudocode & complexity), Volcano pipelining vs. materialization, Book vs. Phone Book analogies, Clustered vs. Secondary, Composite Index Leftmost Prefix rule, B+ Tree fan-out math, Static vs. Extendible Hashing, Bitmap Indexes.

### Module 07 — Database Classifications & NoSQL Ecosystem

20. [[01 - DBMS Architectures, Specialized Models & NoSQL Internals]] — Client-server vs. replication/sharding, Physical & Logical Data Independence, legacy Hierarchical/Network flaws, OODBMS & Hibernate Impedance Mismatch, Multimedia DBs & CBR, Time-Series DBs & downsampling, CAP theorem, Key-Value, Document (BSON & JSONiq), Wide-Column (4D sparse map, LWW, Tombstones, MemTable/SSTable/Compaction), Graph (Index-Free Adjacency).

### Module 08 — Practice & Curriculum Reference

21. [[01 - Worked SQL & Relational Algebra Drills (Practice Bank)]] — All 20 RA-to-SQL examples, 30 Join & 10 Division drills (`Employees/Departments/Projects/WorksOn`), SQL best practices, plus a complete verification checklist mapping every TP 1–3 and TD 1–3 question.

---

## 2. Recommended Study Paths

- **2026/2027 Current Semester Exam Path:** Module 02 (`01`–`03`) $\to$ Module 03 (`01`–`05`) $\to$ Module 04 (`01`).
- **Foundations & Conceptual Modeling Review:** Module 01 (`01`–`05`).
- **Full Master 1 BDA Final Exam (Including Optimization, Transactions & NoSQL):** Modules 02 $\to$ 03 $\to$ 04 $\to$ 05 $\to$ 06 $\to$ 07 $\to$ 08.

---

## 3. Vault Audit: Prioritization, Redundancy Cleanup & Source Discrepancies

### A. Source Prioritization Policy

1. **Primary Authority (2026/2027):** Lecture Slides (Chapters 1 & 2), TP 1, TD 1, TP 2, TD 2, TP 3, TD 3 (**PostgreSQL + pgAdmin 4 + ISO SQL/PSM** using the **`university`** database).
2. **Preserved & Contextualized Legacy Materials (2008–2025):** Prior vault chapters (`01 Fundamentals`–`06 Exercises`), TD 4 (`Pilote`, `Trains`, `Archaeology`), TD 5 (`Transactions`), and past `Exams/`. All unique conceptual, algorithmic, and problem-solving depth is retained and explicitly labeled where older dialects (**MySQL** `DELIMITER`/`SIGNAL`, **Oracle** `SYSDATE`/`EXECUTE IMMEDIATE`) differ from PostgreSQL.
3. **Key Corrections Applied:**
   - Replaced the obsolete note claiming Materialized Views were "not covered here" with full coverage of `CREATE/REFRESH MATERIALIZED VIEW`.
   - Corrected the MySQL-centric claim that SQL lacks native `INTERSECT`, `EXCEPT`, and `FULL OUTER JOIN` (**PostgreSQL** supports all three natively).
   - Relocated the misplaced `DELIMITER //` section out of Query Optimization into Procedural SQL, moved `Database Classifications & Ecosystem` out of `10 - Views` into Module 07, and replaced all raw ASCII diagrams with Mermaid diagrams and tables.

### B. Elimination of Redundant Condensed Notes (Zero Content Loss)

Every sub-file in the original 179-file vault was audited line-by-line and its unique content merged into the 22 main notes before marking the redundant condensed copies for deletion:

- `01 Fundamentals/01 - Foundations/01`–`11` $\to$ `01/01`
- `01 Fundamentals/02 - Relational Algebra/01`–`04` & `09/01, 10, 14` $\to$ `01/02`
- `01 Fundamentals/03 - Keys & Constraints/01`–`12` & `08 - Data Types/01` $\to$ `01/03`
- `01 Fundamentals/05 - Relationships/01`–`09`, `06 - ER Modeling/01`–`05`, `Source TD Modèle E-A` $\to$ `01/04`
- `01 Fundamentals/07 - Normalization/01`–`06`, `Source TD Dépendance Fonctionnelle` $\to$ `01/05`
- `01 Fundamentals/09 - Joins/02`–`09, 11`–`13, 15` & `12 - Exercises/01`–`03` $\to$ `02/02` & `02/03`
- `01 Fundamentals/10 - Views/01`–`02` $\to$ `03/01`
- `05 PLSQL and Database Programming/01`–`07` & `05 PLSQL.md` $\to$ `03/02`, `03/03`, `03/04`
- `02 Integrity Management/01`–`09` & `02 Integrity Management.md` $\to$ `04/01` & `04/02`
- `03 Transactions and Security/01`–`09`, `04/Combined_Syntax.md` & `03 Transactions.md` $\to$ `05/01` & `05/02`
- `04 Query Optimization and Processing/1`–`15`, `01/04 - Indexes/01`, `04 Query Optimization.md` $\to$ `06/01` & `06/02`
- `10 - Views/11 - Database Classifications & Ecosystem/01`–`07` & `12/05` $\to$ `07/01`
- `12 - Exercises/04, 06` $\to$ `08/01`
- Duplicate archive/quiz files: `06 Exercises/Interview.md` (duplicate of `Exams/2008/2008 Control Dec 13`) and `Quiz/Chapter_01/Q3`–`Q10` (duplicates of `Quiz/01 Fundamentals/Q1`–`Q8`). `Exams/` (2008–2025) and unique `Quiz/` banks remain untouched as archival exam prep.

### C. Source Discrepancy & Errata Log

1. **TP 1 Part O vs. Part D:** `O.5` (`teacher.salary < 0`), `O.6` (`UNIQUE class_name`), and `O.7` (`CHECK class_name`), plus `R.16` (`chk_student_age`), require adding/naming those constraints via `ALTER TABLE` first because Part D did not define them.
2. **TP 1 Part Q Count:** Part Q expects `13` rows in `teacher_class`, whereas Part J inserts **14** pairs.
3. **`manager` Table Schema:** Ch 2 Slides & TP 2 Ex 11 define `manager(manager_id, name, supervisor_id)` with **5 rows** (`level` 0–4), whereas TP 3 Ex 8–16 defines `manager(manager_id, manager_name, supervisor_id)` with **6 rows** (`level` 0–5).
4. **Audit Table & `<>` NULL Bug:** Ch 2 Slide 65–66 & TD 2 Ex 17–18 use `salary_audit` with `IF OLD.salary <> NEW.salary` (which misses `NULL <-> value` updates like teacher 109), whereas TP 2 Ex 10 uses `salary_history` with `IF OLD.salary IS DISTINCT FROM NEW.salary` (safe for `NULL`!).
5. **Ch 2 View Name Collision:** Slide 9 names a non-updatable join view `computer_science_teacher_view`, while Slide 11 reuses that name directly on `teacher` with `WITH CHECK OPTION`. TP 2 resolves this by naming the updatable view `department_1_teachers`.
6. **TP 2 Ex 12 & Part IV Numbering:** Ex 12 tasks are numbered `4–9` (instead of `1–6`), and Part IV questions are numbered `10–19` (instead of `1–10`).
7. **`file.md` TD 2 Ex 3 Snippet:** Uses wrong column name `id_department` instead of `department_id` and mixes MySQL cursor syntax; Ch 2 Slide 58 gives the authoritative SQL/PSM cursor solution and TP 2 Ex 6 gives the PL/pgSQL `FOR` loop.
