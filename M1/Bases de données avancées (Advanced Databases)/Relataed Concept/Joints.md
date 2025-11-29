Based on the **Correction of Exam 2021 (Exercice 1)** and **Correction of Exam 2010** found in your documents, here is the explanation of Joins.

In these documents, a Join is defined as: **"A link created momentarily between 2 tables having at least one common column."**

To make this easy to understand, let's use the **Hotel Database schema** found in **Exam 2021**:

**Table: HOTEL**

| numHotel | nomHotel |
| :--- | :--- |
| 10 | Aurassi |
| 20 | Hilton |

**Table: CHAMBRE (Room)**

| numChambre | numHotel | Prix |
| :--- | :--- | :--- |
| 101 | 10 | 5000 |
| 102 | 10 | 6000 |
| 201 | 20 | 8000 |

---

### 1. Simple Join (Jointure Simple)

**Definition from PDF:** "Connects a single column from each of the two tables."

This is the standard join used to combine data. We want to see the Room Price and the Name of the Hotel it belongs to. We match them using the common column `numHotel`.

**SQL Code (from Exam 2021 Correction, Q6 approach):**
```sql
SELECT H.nomHotel, C.numChambre, C.Prix
FROM   Hotel H, Chambre C
WHERE  H.numHotel = C.numHotel;
```

**Result:**

| nomHotel | numChambre | Prix |
| :--- | :--- | :--- |
| Aurassi | 101 | 5000 |
| Aurassi | 102 | 6000 |
| Hilton | 201 | 8000 |

---

### 2. Multiple Join (Jointure Multiple)

**Definition from PDF:** "Connects **several columns** from each of the linked tables."

This happens when a simple ID isn't enough to identify a row, or you need to match on two criteria at the same time (e.g., matching a date AND an ID).

*Imagine we have a table `ARCHIVE_CHAMBRE` and we want to match rows that have the same Hotel AND the same Room Number.*

**SQL Concept:**
```sql
SELECT *
FROM   Chambre C, Archive_Chambre A
WHERE  C.numHotel = A.numHotel 
AND    C.numChambre = A.numChambre;
```
*Note: The join condition uses **two** columns.*

---

### 3. [[Auto-Join]] (Auto-jointure)

**Definition from PDF:** "A join between a table and itself."

This is used when you need to compare rows within the *same* table.
**Example from Exam 2021 (Question 2):** Find clients who are in the *same* hotel as client #1.

To do this, we pretend we have two copies of the `RESERVATION` table (calling them `R1` and `R2`).
1. `R1` finds where Client #1 is staying.
2. `R2` finds other people staying in that same hotel.

**SQL Code (from Exam 2021 Correction):**
```sql
SELECT DISTINCT R2.numClient
FROM   Reservation R1, Reservation R2
WHERE  R1.numClient = 1 
AND    R1.numHotel = R2.numHotel;
```

---

### 4. Outer Join (Jointure Externe)

**Definition from PDF:** "A simple join where the link is respected by only one of the two tables."

In a simple join, if a Hotel has no Rooms listed, that Hotel disappears from the result. In an **Outer Join**, we keep the Hotel even if it has no match.

*   **Left/Right Join:** If we keep the `HOTEL` row even if `CHAMBRE` is empty (NULL).

*Imagine Hotel "Sheraton" (ID 30) exists in the HOTEL table but has no rooms in the CHAMBRE table.*

**SQL Concept (Algebraic equivalent mentioned in TD notes):**
It keeps the rows from one side (e.g., Hotel) and puts `NULL` for the other side (Chambre) if no match is found.

**Result (Conceptual):**

| nomHotel | numChambre |
| :--- | :--- |
| Aurassi | 101 |
| Hilton | 201 |
| **Sheraton** | **NULL** |




*(The Sheraton appears even though it has no rooms).*