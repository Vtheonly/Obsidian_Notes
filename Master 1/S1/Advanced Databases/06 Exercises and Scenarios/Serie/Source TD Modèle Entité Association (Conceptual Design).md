Here is the complete processing for the sources **TD Modèle Entité Association** and **TD Dépendance Fonctionnelle**.

These exercises focus on the **Conceptual Phase** (Entity-Relationship Modeling) and the **Logical Phase** (Normalization, Functional Dependencies, 3NF) of Database Design.

---

# Source: TD Modèle Entité Association (Conceptual Design)

**Context:**
*   **Exercise 1:** Design a system for managing Receptions (Guests, Menus, Wines, Affinities).
*   **Exercise 2:** Design a system for an Airline Company (Employees, Flights, Planes).

---

### Exercise 1: The Reception System

**Source:** TD Modèle Entité Association - Exercice 1
**Goal:** Create an Entity-Association (E-A) Diagram to manage receptions, guests, dishes, wines, and interpersonal relationships (friends/enemies).

#### 1. Solution (Based on provided Diagram)

**Entities:**
*   **PERSONNES** (<u>Nom, Prénom</u>, Sexe, Age, Profession)
*   **RECEPTIONS** (<u>DateReception</u>)
*   **PLATS** (<u>NomPlat</u>, Nature)
*   **TYPEVINS** (<u>Region, Type</u>)

**Associations (Relationships):**
1.  **ESTINVITE** (Personnes 0,N — 1,N Receptions): A person is invited to a reception.
2.  **ESTSERVI** (Plats 0,N — 1,N Receptions): A dish is served at a reception.
3.  **VAAVEC** (Plats 0,N — 0,N TypeVins): A dish goes well with a specific wine type.
4.  **APPRECIE** (Personnes 0,N — 0,N Plats): A person likes a dish.
5.  **DETESTE** (Personnes 0,N — 0,N Plats): A person dislikes a dish.
6.  **AMIS** (Personnes 0,N — 0,N Personnes): Reflexive relationship (Friendship).
7.  **ENNEMIS** (Personnes 0,N — 0,N Personnes): Reflexive relationship (Enmity).

#### 2. Reasoning
*   **Identification:** A person is identified by Name+Firstname.
*   **Preferences:** To avoid serving disliked food, we need `APPRECIE` and `DETESTE` linking People to Dishes.
*   **Social Dynamics:** To seat people correctly, we need reflexive relationships `AMIS` and `ENNEMIS` on the `PERSONNES` entity.
*   **Menu:** A menu is simply the set of dishes (`ESTSERVI`) linked to a specific `RECEPTION`.
*   **Wine Pairing:** We don't track specific bottles, but "types" of drinks compatible with dishes (`VAAVEC`).

#### 3. Detailed Explanation
*   **Reflexive Relationships:** The `AMIS` and `ENNEMIS` associations connect an entity to *itself*. In the physical database, this will create a table (e.g., `AMITIE`) with two foreign keys pointing to the `PERSONNES` table (e.g., `Person1_ID`, `Person2_ID`).
*   **Ternary vs Binary:** The text implies a menu is specific to a reception. The link is `Receptions` <-> `Plats`. Wine matches the *Plat*, not the reception directly (you choose wine based on the food).

---

### Exercise 2: Airline Company (Conceptual to Relational)

**Source:** TD Modèle Entité Association - Exercice 2
**Goal:** Transform the conceptual model of an Airline (Pilots, Crew, Flights) into a Relational Schema.

#### 1. Solution (Relational Schema)

**Employee Hierarchy (Inheritance Strategy):**
*   `PERSONNE` (<u>NoSecu</u>, Nom, Prenom, Adresse)
*   `EMPLOYE` (<u>NoSecu</u>, Salaire) -> *References PERSONNE*
*   `AUSOL` (<u>NoSecu</u>) -> *References EMPLOYE (Ground Staff)*
*   `NAVIGANT` (<u>NoSecu</u>, NbHrVol) -> *References EMPLOYE (Flying Staff)*
*   `PILOTE` (<u>NoSecu</u>, NoLicence) -> *References NAVIGANT*
*   `EQUIPAGE` (<u>NoSecu</u>, Fonction) -> *References NAVIGANT (Crew)*

*Alternative Strategy (Flattened Tables):*
*   `PILOTE` (<u>NoSecu</u>, Nom, Prenom, Adresse, Salaire, NbHrVol, NoLicence)
*   `EQUIPAGE` (<u>NoSecu</u>, ..., Fonction)

**Flight Operations:**
*   `APPAREIL` (<u>NoImm</u>, Type, Capa)
*   `LIAISON` (<u>NoL</u>, VilleDep, VilleArr)
*   `VOL` (<u>NoV</u>, DateDeb, DateFin, HrDep, HrArr, NoL, NoImm)
    *   *FK NoL -> LIAISON*
    *   *FK NoImm -> APPAREIL*
*   `DEPART` (<u>NoVol, DateDep</u>, NbLibre, NbOccup, NoPil1, NoPil2, NoEquip1, ..., NoEquip4)
    *   *This table handles the specific instance of a flight on a specific day.*
*   `BILLET` (<u>NoB</u>, DateEm, Prix, NoP, NoVol, DateDep)
    *   *FK NoP -> PASSAGER*
    *   *FK (NoVol, DateDep) -> DEPART*

#### 2. Reasoning
*   **Generalization/Specialization:** The text describes "Employees", divided into "Ground" and "Navigating", with "Navigating" divided into "Pilots" and "Crew". This is an inheritance hierarchy.
*   **Relationships:**
    *   A **Vol** (Flight Number) is a template (e.g., Flight AF123).
    *   A **Depart** (Departure) is the actual occurrence (Flight AF123 on Dec 25th).
    *   A **Billet** (Ticket) links a Passenger to a specific Departure.

#### 3. Detailed Explanation
*   **Handling Inheritance:** The solution proposes creating tables for the subtypes (`PILOTE`) containing only specific attributes, linked by the primary key to the supertype (`NAVIGANT`/`EMPLOYE`). This is the "Class Table Inheritance" pattern.
*   **Departures:** Note that `DEPART` has fixed slots for pilots (`NoPil1`, `NoPil2`). This is a simple way to handle the "1 or 2 pilots" rule, though a separate association table `AFFECTATION_PILOTE(NoVol, DateDep, NoPil)` would be more flexible (Normalization). The solution provided uses columns, which implies `NULL` allowed for the second pilot.

---

# Source: TD Dépendance Fonctionnelle (Normalization)

**Context:**
*   **Exercise 1:** Analyzing dependencies for Apartment rentals.
*   **Exercise 2:** Analyzing dependencies for Course grading.

---

### Exercise 1: Apartment Occupancy

**Source:** TD Dépendance fonctionnelle - Exercice 1
**Attributes:** `Propriétaire (P)`, `Occupant (O)`, `Adresse (A)`, `Noapt (N)`, `Nbpièces (nb1)`, `Nbpersonnes (nb2)`.
**Initial FDs (Functional Dependencies):**
1.  $O \to A$
2.  $O \to N$
3.  $O \to nb2$
4.  $A, N \to P$
5.  $A, N \to O$
6.  $A, N \to nb1$

#### 1. Solution

**Q1. Elementary FDs (Transitive Closure):**
*   From $O \to A$ and $O \to N$, and knowing $A, N \to P$, we can deduce $O \to P$ (Transitivity).
*   Similarly, $O \to nb1$ (via $A,N$).
*   **Resulting FDs:**
    *   $O \to \{A, N, nb2, P, nb1\}$
    *   $A, N \to \{P, O, nb1, nb2\}$ (Since $A,N \to O$ and $O \to nb2$)

**Q2. Potential Keys:**
*   **Occupant (O):** Determines all other attributes.
*   **Adresse, Noapt (A, N):** Determines O, and thus determines everything else.
*   **Keys:** `{Occupant}` and `{Adresse, Noapt}`.

**Q3. Normal Form (3NF):**
*   **Key Attributes:** $O, A, N$.
*   **Non-Key Attributes:** $P, nb1, nb2$.
*   **Check 2NF:** Do non-key attributes depend on a *part* of a candidate key?
    *   If Key is $O$: No partial dependency (single attribute).
    *   If Key is $A, N$: Does $P$ depend on just $A$ or just $N$? No.
    *   Result: It is in **2NF**.
*   **Check 3NF:** Are there transitive dependencies between non-key attributes?
    *   Do non-key attributes depend on other non-key attributes? No.
    *   However, we check if non-key depends on Key via another Key.
    *   $A, N \to O \to nb2$. Since $O$ is a candidate key, this is valid 3NF.
*   **Conclusion:** The relation is in **3NF**.

#### 2. Detailed Explanation
*   **Interpretation:** An occupant lives in exactly one apartment ($O \to A, N$). An apartment ($A, N$) has exactly one current occupant ($A, N \to O$). Therefore, knowing the occupant gives you the apartment info, and knowing the apartment gives you the occupant info. They are equivalent identifiers.

---

### Exercise 2: University Courses

**Source:** TD Dépendance fonctionnelle - Exercice 2
**Attributes:** `C (Cours)`, `P (Prof)`, `H (Heure)`, `S (Salle)`, `E (Etudiant)`, `N (Note)`.
**Initial FDs:**
1.  $C \to P$ (A course has one professor)
2.  $H, S \to C$ (A room at a specific time hosts one course)
3.  $H, P \to S$ (A prof at a specific time is in one room)
4.  $C, E \to N$ (Course + Student = Grade)
5.  $H, E \to S$ (Student at a specific time is in one room)

#### 1. Solution

**Q1. Elementary FDs & Inferences:**
*   $H, E \to S$ and $S, H \to C$ implies $H, E \to C$.
*   $H, E \to C$ and $C \to P$ implies $H, E \to P$.
*   $H, E \to C$ and $C, E \to N$ implies $H, E \to N$.
*   **Conclusion:** $H, E$ determines $\{S, C, P, N\}$.

**Q2. Candidate Key:**
*   **Key:** `{H, E}` (Heure, Etudiant).
*   **Reasoning:** Given a time and a student, we know where they are ($S$), what course they are taking ($C$), who teaches it ($P$), and their grade ($N$). No subset of $\{H, E\}$ determines the whole relation.

**Q3. Normal Form & Decomposition:**
*   **Check 2NF:** Is there a partial dependency?
    *   $C, E \to N$. Here $C$ is determined by $H, E$. So $N$ depends on the full key $\{H, E\}$.
    *   However, look at $C \to P$. $C$ is *not* a subset of the key $\{H, E\}$. It is a transitive dependency ($H, E \to C \to P$).
*   **Check 3NF:**
    *   We have $H, E \to C$ and $C \to P$.
    *   $P$ depends on $C$, and $C$ is not a superkey (it doesn't determine $H$ or $E$).
    *   **Result:** NOT in 3NF.

**Decomposition into 3NF:**
We must break dependencies to remove transitivity.
1.  **R1 (C, E, N)**: Preserves $C, E \to N$. Key: $(C, E)$.
2.  **R2 (C, P)**: Preserves $C \to P$. Key: $(C)$.
3.  **R3 (H, S, C)**: Preserves $H, S \to C$. Key: $(H, S)$. *(Wait, correction suggests merging differently)*.
4.  **R4 (H, E, S)**: Preserves $H, E \to S$. Key: $(H, E)$.

*Refined Decomposition based on Correction:*
*   **R1(C, E, N)**: Grades.
*   **R2(C, P)**: Course assignments.
*   **R3(H, S, C)**: Room Schedule.
*   **R4(H, E, S)**: Student Schedule (derived).

*Note:* The dependencies $H, P \to S$ and $H, E \to S$ are interesting.
The correction proposes:
1.  `R1(C, E, N)` using $C, E \to N$.
2.  `R2(C, P)` using $C \to P$.
3.  `R3(H, S, C)` using $H, S \to C$.
4.  `R4(H, E, C)` is actually derived from $H, E \to S$ and $S \to C$... actually $H, E$ is the primary key of the universal relation. To reconstruct the data, we need to link students to time.
    *   If we keep `R4(H, E, C)` (Student $E$ at hour $H$ is in course $C$), this links to R1 and R2.

#### 3. Detailed Explanation
*   **Why not 3NF?** Because of **Transitive Dependencies**.
    *   Knowing the Student and Time ($H, E$) tells you the Course ($C$).
    *   Knowing the Course ($C$) tells you the Professor ($P$).
    *   Therefore, $P$ depends on $H, E$ *transitively* through $C$. This redundancy (storing the professor for every student at that hour) causes update anomalies. If the professor changes for the course, we have to update it for every student taking that course.
    *   **Decomposition** isolates facts: One table tells us "Who teaches Course X", another tells us "Who is taking Course X at Time Y".