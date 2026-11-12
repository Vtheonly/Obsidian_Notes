# Relationships & ER Modeling

Entity-Relationship (ER) modeling captures entities, attributes, and connections visually before writing DDL, ensuring the schema accurately mirrors real-world domain rules.

---

## 1. The Three Relationship Types & Foreign Key Placement

Every relationship connects a **parent table** (holds the referenced primary key) and a **child table** (holds the foreign key pointing back to the parent). Determining parent vs. child is straightforward: ask which entity cannot exist meaningfully without the other—the dependent entity is the child and receives the foreign key.

```mermaid
erDiagram
    DEPARTMENT ||--o{ TEACHER : "employs (1:N)"
    DEPARTMENT ||--o{ CLASS : "contains (1:N)"
    CLASS ||--o{ STUDENT : "enrolls (1:N)"
    TEACHER }o--o{ CLASS : "teaches via teacher_class (M:N)"
```

### A. One-to-One (1:1)

One instance of A connects to at most one instance of B, and vice versa (e.g., person and SSN, employee and assigned parking space, user account and profile).

- **When to keep in ONE table:** When the related item is a simple attribute with no extra properties (e.g., `username VARCHAR(50) UNIQUE NOT NULL` inside `users`), or both sides share an identical lifecycle and are always queried together.
- **When to split into TWO tables:** When the second entity has its own attributes (`cards`: `max_amount`, `issue_date`, `late_fee` belong to the card, not the cardholder!), contains large `TEXT`/`BLOB` fields (`bio`), requires stricter security isolation (`users` auth vs. public `user_profiles`), or has an independent/optional lifecycle.
- **Two-table implementation patterns:** (1) Unique foreign key (`holder_id INT UNIQUE NOT NULL` in `cards`), or (2) Shared primary key (`user_id INT PRIMARY KEY REFERENCES users(user_id)` in `user_profiles`).

### B. One-to-Many (1:N)

One parent row links to many child rows; each child row links to at most one parent (e.g., `users` $\to$ `comments`, `departments` $\to$ `employees`, `cardholders` $\to$ `cards`, `department` $\to$ `teacher`).

- **Golden Rule:** **Always place the foreign key on the "many" (child) side.** Putting child IDs in the parent (`review_id1, review_id2`) creates repeating groups, unbounded columns, and wasted `NULL` cells.
- **Directional awareness:** Given a child row (a comment), following `user_id` immediately identifies its parent; given a parent (a user), finding children requires querying the child table.

### C. Many-to-Many (M:N) — TP 1 Part E Case Study

Multiple rows of A link to multiple rows of B (`students` $\leftrightarrow$ `classes`, `orders` $\leftrightarrow$ `products`, `teacher` $\leftrightarrow$ `class` in **TP 1 Part E**).

- **Why 2 tables fail (TP 1 Part E Q1–Q3):**
  1. Adding `class_id` to `teacher` allows only **1 class per teacher**.
  2. Adding `teacher_id` to `class` allows only **1 teacher per class**.
  3. Storing `'10, 20, 30'` in a single column violates **1NF** (non-atomic) and breaks foreign-key checks and joins.
- **The Junction Table Solution (TP 1 Part E Q4–Q7):** Introduce a third **junction / bridge / association table** (`teacher_class` or `class_students`) that decomposes M:N into **two 1:N relationships** pointing inward to the junction table (which is the child of both parents):
  - Contains `teacher_id` (FK) and `class_id` (FK) forming a **composite primary key `(teacher_id, class_id)`** so the same `(teacher, class)` pair cannot be inserted twice.
  - **Key principle:** Neither `teacher` nor `class` is modified! Additional relationship attributes (`enrolled_date`, `grade`, `academic_year`, `semester`) can be added directly to the junction table without touching the parents.

### Business Rules Dictate Cardinality

The exact same entity pair (`professor` and `class`) can be **1:1** (small training center: 1 dedicated instructor per course), **1:N** (standard: 1 professor teaches many classes, 1 instructor per class), or **M:N** (team-taught courses). Always model the domain's business rules.

---

## 2. Weak Entities, Crow's Foot Cardinality & Modality

### Strong vs. Weak Entities (Identifying vs. Non-Identifying)

- **Weak Entity (Identifying Relationship):** Child cannot exist or be identified without its parent; parent's PK becomes **part of the child's composite PK** (e.g., `order_items(order_id, item_id)` with `PRIMARY KEY (order_id, item_id)`).
- **Strong Entity (Non-Identifying Relationship):** Child has its own independent PK (`emp_id`, `teacher_id`), while the parent's PK is simply a non-PK foreign key (`dept_id`, `department_id`).

### Crow's Foot Notation: Cardinality vs. Modality

- **Cardinality** = _maximum_ participation (`|` = one, `<` = many).
- **Modality** = _minimum_ participation (`O` = 0 optional / nullable FK, `|` = 1 mandatory / `NOT NULL` FK).
- **Four common child-side patterns:**
  1. **Optional One (`0..1`):** `O|` — child may reference 0 or 1 parent (`class.instructor_id` nullable).
  2. **Mandatory One (`1..1`):** `||` — child must reference 1 parent (`card.holder_id NOT NULL`).
  3. **Optional Many (`0..M`):** `O<` — parent has 0 or more children; child FK may be `NULL` (`student.class_id` nullable).
  4. **Mandatory Many (`1..M`):** `|<` — child must participate (`order_item.order_id NOT NULL`).

_(Tools such as MySQL Workbench, Vertabelo, Lucidchart, and draw.io support forward engineering ER diagrams directly into SQL `CREATE TABLE` DDL.)_

---

## 3. Advanced Conceptual (French E/A MCD) Rules & Complex Translations

_(From `Source TD Modèle Entité Association` and conceptual design methodology)_

### Four Strict Attribute Normalization Rules in E/R

1. **No Composite or Multi-Valued Attributes:** Explode `Address` into `Street, City, ZipCode`; extract `PhoneNumbers` into a separate `PHONE` entity.
2. **No Derived / Calculated Attributes:** Never store `Total_Price` physically when `Quantity` and `Unit_Price` exist—compute it dynamically in SQL to avoid desynchronization.
3. **Enumerated Attributes Become Entities:** Fixed value lists (`Emission_Type` = `'Radio'`, `'TV'`, `'Web'`) become a dedicated `TYPE` entity linked 1:N to enforce referential integrity and prevent spelling errors.
4. **Association Attributes:** An attribute belongs inside an association **only if it depends on all participating entities simultaneously** (e.g., `Quantity` sits inside `SUPPLIES(Supplier, Article)`, not in `Supplier` or `Article` alone).

### The "Borrowing" Problem (Promoting Binary M:N to Ternary)

A naive binary M:N association `SUBSCRIBER (0,n) — Borrows — (0,n) BOOK` gives implicit PK `(Subscriber_ID, Book_ID)`, which restricts each subscriber to borrowing any given book **at most once in their entire lifetime**.

- **Fix:** Introduce a `DATE` entity and promote `BORROWS` to a **ternary association** so the implicit identifier becomes `(Subscriber_ID, ISBN, Borrow_Date)`, allowing repeat borrows on different dates.

### Complex Translation Rules (1,1 Functional Dependencies & Edge Cases)

- **Never turn a `1,1` or `0,1` association into its own table:** The primary key of the `0,n` entity always migrates as a **foreign key into the entity sitting on the `1,1` / `0,1` side**.
  - _Command Example:_ `CLIENT (0,n) — Passée_par — (1,1) COMMANDE (0,n) — Concerne(quantité) — (0,n) ARTICLE` translates to:
    - `CLIENT(num_client, nom, adresse)`
    - `ARTICLE(num_article, designation, prix)`
    - `COMMANDE(num_commande, date, num_client*)` _(FK placed in `COMMANDE` because of its `1,1` leg!)_
    - `DETAIL_COMMANDE(num_commande*, num_article*, quantité)`
  - _Teaching Edge Case:_ `ELEVE (0,n) — A_suivi(note) — (0,n) UV (1,1) — Enseignant — (0,n) PROFESSEUR` translates to `ELEVE`, `PROFESSEUR`, `UV(code_UV, nom, annee, code_professeur*)`, and `NOTE(code_eleve*, code_UV*, note)`.

---

## 4. Worked E/A Conceptual Design Exercises (`Source TD Modèle E-A`)

### Exercise 1: Reception Management System

- **Entities:** `PERSONNES(Nom, Prénom [PK], Sexe, Age, Profession)`, `RECEPTIONS(DateReception [PK])`, `PLATS(NomPlat [PK], Nature)`, `TYPEVINS(Region, Type [PK])`.
- **Associations:**
  - `ESTINVITE` (`Personnes 0,N — 1,N Receptions`), `ESTSERVI` (`Plats 0,N — 1,N Receptions`), `VAAVEC` (`Plats 0,N — 0,N TypeVins`—wine pairs with the dish, not the reception directly), `APPRECIE` (`0,N — 0,N`) and `DETESTE` (`0,N — 0,N`) between `Personnes` and `Plats`.
  - **Reflexive Relationships:** `AMIS(0,N — 0,N)` and `ENNEMIS(0,N — 0,N)` linking `PERSONNES` to itself (translates to junction tables `AMITIE(P1_ID, P2_ID)` and `INIMITIE(P1_ID, P2_ID)`).

### Exercise 2: Airline Company (Inheritance + Flight Instances)

- **Class Table Inheritance for Staff Hierarchy:**
  - `PERSONNE(NoSecu PK, Nom, Prenom, Adresse)` $\leftarrow$ `EMPLOYE(NoSecu PK/FK, Salaire)` $\leftarrow$ `AUSOL(NoSecu PK/FK)` & `NAVIGANT(NoSecu PK/FK, NbHrVol)` $\leftarrow$ `PILOTE(NoSecu PK/FK, NoLicence)` & `EQUIPAGE(NoSecu PK/FK, Fonction)`. _(Flattened alternative duplicates inherited attributes inside `PILOTE` and `EQUIPAGE`.)_
- **Flight Operations:** `APPAREIL(NoImm PK, Type, Capa)`, `LIAISON(NoL PK, VilleDep, VilleArr)`, `VOL(NoV PK, DateDeb, DateFin, HrDep, HrArr, NoL*, NoImm*)`, `DEPART(NoVol PK/FK, DateDep PK, NbLibre, NbOccup, NoPil1*, NoPil2*, NoEquip1*..4*)` _(or normalized junction table `AFFECTATION_PILOTE`)_, `BILLET(NoB PK, DateEm, Prix, NoP*, NoVol*, DateDep*)`.
