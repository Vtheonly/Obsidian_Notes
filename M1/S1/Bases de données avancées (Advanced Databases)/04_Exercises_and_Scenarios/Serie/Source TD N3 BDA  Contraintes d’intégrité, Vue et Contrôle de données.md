Here is the complete processing for the source **TD N°3 BDA : Contraintes d’intégrité, Vue et Contrôle de données**.

Based on the provided context, I will use the "Corrigé - TD N°3 BDA" document as the authoritative reference to ensure accuracy while expanding the explanations.

---

# Source: TD N°3 BDA - Gestion des Missions

**Context Schema:**
*   `EMPLOYE (EMP_Num, EMP_Titre, EMP_Nom, EMP_Salaire, SRV_Num, EMP_Responsable)`
*   `SERVICE (SRV_Num, SRV_Libelle)`
*   `MISSION (MIS_Num, VEH_Num, EMP_Num, MIS_JourDep, MIS_KlmDep, MIS_JourRetour, MIS_KlmRetour)`
*   `VEHICULE (VEH_Num, VEH_NumMatricule, COU_Code, VEH_DateAchat, VEH_PrixAchat, TYP_Num)`
*   `TYPE (TYP_Num, TYP_Nom, TYP_Puissance, TYP_Poids, TYP_Consommation, MAR_Num)`
*   `MARQUE (MAR_Num, MAR_Nom)`
*   `COULEUR (COU_Code, COU_Libelle)`

---

## Part I: Data Definition & Constraints

**Exercise:** Define integrity constraints for the schema based on the provided rules.

### 1. Solution
```sql
-- Table EMPLOYE
ALTER TABLE EMPLOYE ADD CONSTRAINT CHK_Titre 
CHECK (EMP_Titre IN ('Mr', 'Mlle', 'Mme'));

ALTER TABLE EMPLOYE ADD CONSTRAINT CHK_Salaire 
CHECK (EMP_Salaire >= 15000);

-- Table MISSION
ALTER TABLE MISSION ADD CONSTRAINT FK_Mission_Emp 
FOREIGN KEY (EMP_Num) REFERENCES EMPLOYE(EMP_Num);

ALTER TABLE MISSION ADD CONSTRAINT FK_Mission_Veh 
FOREIGN KEY (VEH_Num) REFERENCES VEHICULE(VEH_Num);

ALTER TABLE MISSION ADD CONSTRAINT CHK_Klm_Retour 
CHECK (MIS_KlmRetour <= 150000); -- "Cars cannot drive more than 150,000 Km" rule applied to mission return

ALTER TABLE MISSION ADD CONSTRAINT CHK_Dates 
CHECK (MIS_JourDep > SYSDATE AND MIS_JourRetour > SYSDATE);

-- Table VEHICULE
ALTER TABLE VEHICULE ADD CONSTRAINT FK_Veh_Coul 
FOREIGN KEY (COU_Code) REFERENCES COULEUR(COU_Code);

ALTER TABLE VEHICULE ADD CONSTRAINT FK_Veh_Type 
FOREIGN KEY (TYP_Num) REFERENCES TYPE(TYP_Num);

ALTER TABLE VEHICULE ADD CONSTRAINT CHK_Prix 
CHECK (VEH_PrixAchat BETWEEN 450000 AND 2000000);

-- Table TYPE
ALTER TABLE TYPE ADD CONSTRAINT FK_Type_Marque 
FOREIGN KEY (MAR_Num) REFERENCES MARQUE(MAR_Num);

ALTER TABLE TYPE ADD CONSTRAINT CHK_TypeNum 
CHECK (TYP_Num BETWEEN 1 AND 100);

-- Table COULEUR
ALTER TABLE COULEUR ADD CONSTRAINT CHK_Couleur_Lib 
CHECK (COU_Libelle IN ('Blanche', 'Noire'));
```

### 2. Reasoning
The exercise provides specific business rules ("Règles de gestion"):
*   **Titles**: Must be specific values -> `CHECK IN (...)`
*   **Salary**: Minimum 15,000 -> `CHECK (>=)`
*   **Keys**: Linking tables requires `FOREIGN KEY`.
*   **Business Limits**: Max Km, Price ranges -> `CHECK BETWEEN` or `<=`

### 3. Detailed Explanation
*   **Domain Constraints (`CHECK`)**: These ensure data validity at the entry level. For example, restricting colors to 'Blanche' or 'Noire' prevents a user from entering 'Rouge'.
*   **Referential Integrity (`FOREIGN KEY`)**: This ensures relationships are valid. You cannot assign a mission to a vehicle that doesn't exist in the database.
*   **`SYSDATE`**: Used to check that mission dates are in the future (superior to "date du jour").

---

## Part II: SQL Queries (DML & DCL)

### Exercise 1: Employees in 'FI...' Service
**Question:** Liste des numéros et des noms des employés d'un service dont on ne connaît que les 2 premières lettres ‘FI’.

#### 1. Solution
```sql
SELECT EMP_Num, EMP_Nom 
FROM EMPLOYE 
WHERE SRV_Num = (
    SELECT SRV_Num 
    FROM SERVICE 
    WHERE SRV_Libelle LIKE 'FI%'
);
```
#### 2. Reasoning
We need employees filtered by service. The service name is in another table (`SERVICE`) and we only have a pattern (`LIKE 'FI%'`).
#### 3. Detailed Explanation
The subquery finds the ID of the "Finance" or "Fiscalité" service. The main query uses this ID to grab the employees. Note: The correction uses `LIKE "FI*"` which is Microsoft Access syntax. Standard SQL uses `%`.

---

### Exercise 2: Current Month Missions
**Question:** Liste des employés qui sont partis en mission le mois en cours.

#### 1. Solution
```sql
SELECT EMP_Num, EMP_Nom 
FROM EMPLOYE
WHERE EMP_Num IN (
    SELECT EMP_Num 
    FROM MISSION 
    WHERE TO_CHAR(MIS_JourDep, 'MM-YYYY') = TO_CHAR(SYSDATE, 'MM-YYYY')
);
```
#### 2. Reasoning
Compare the month and year of the mission start date with the current date (`SYSDATE`).
#### 3. Detailed Explanation
Using `TO_CHAR` ensures we compare the Month and Year parts specifically, ignoring the exact day.

---

### Exercise 3: Service Managers
**Question:** Liste des responsables de service.

#### 1. Solution
```sql
SELECT E.EMP_Num, E.EMP_Nom, S.SRV_Libelle 
FROM EMPLOYE E, SERVICE S
WHERE E.SRV_Num = S.SRV_Num 
  AND E.EMP_Num = E.EMP_Responsable; -- Assuming self-reference or specific column logic
```
*Correction Logic:* The correction assumes `EMP_Responsable` in `EMPLOYE` table points to the manager's ID. If an employee is their own manager, or if the Service table links to the manager, the query might vary. Based on typical schema, a Join is best.

#### 3. Detailed Explanation
This query joins Employee and Service to get the service name, filtering for rows where the employee is flagged as the responsible party.

---

### Exercise 4: Vehicles Sorted
**Question:** Liste des véhicules avec couleur, par marque, type, et ordre chronologique d'achat.

#### 1. Solution
```sql
SELECT V.VEH_Num, M.MAR_Nom, T.TYP_Nom, V.VEH_NumMatricule, V.VEH_DateAchat, C.COU_Libelle
FROM VEHICULE V, TYPE T, MARQUE M, COULEUR C
WHERE V.TYP_Num = T.TYP_Num 
  AND T.MAR_Num = M.MAR_Num 
  AND V.COU_Code = C.COU_Code
ORDER BY M.MAR_Nom, T.TYP_Nom, V.VEH_DateAchat;
```
#### 2. Reasoning
Join 4 tables (`VEHICULE`, `TYPE`, `MARQUE`, `COULEUR`) to get text descriptions instead of IDs.
#### 3. Detailed Explanation
Multi-level sorting: First it groups all 'Renaults' together. Inside 'Renault', it groups 'Clio'. Inside 'Clio', it sorts by date.

---

### Exercise 5: Missions of Service Chiefs
**Question:** Liste des missions des chefs de service.

#### 1. Solution
```sql
CREATE VIEW Chef AS 
SELECT S.SRV_Libelle, E.EMP_Num, E.EMP_Nom
FROM EMPLOYE E, SERVICE S
WHERE E.EMP_Num = E.EMP_Responsable 
  AND E.SRV_Num = S.SRV_Num;

SELECT C.*, M.MIS_Num, M.MIS_JourDep, M.MIS_JourRetour
FROM Chef C, MISSION M
WHERE C.EMP_Num = M.EMP_Num 
ORDER BY C.EMP_Nom, M.MIS_JourDep;
```
#### 2. Reasoning
Create a reusable `VIEW` for managers ("Chefs") first, as this subset is likely useful later. Then join the View with the Mission table.
#### 3. Detailed Explanation
This demonstrates modular SQL. Instead of a complex nested query, we abstract the concept of "Chef" into a view.

---

### Exercise 6: Mission Stats (Last 2 Months)
**Question:** Nombre de missions et kilomètres par employé ces deux derniers mois.

#### 1. Solution
```sql
CREATE VIEW Missions_Recentes AS 
SELECT * FROM MISSION 
WHERE MIS_JourDep >= ADD_MONTHS(SYSDATE, -2);

SELECT E.EMP_Nom, E.EMP_Num, COUNT(*) AS NbMissions, SUM(M.MIS_KlmRetour - M.MIS_KlmDep) AS NbKm
FROM EMPLOYE E, Missions_Recentes M
WHERE E.EMP_Num = M.EMP_Num
GROUP BY E.EMP_Nom, E.EMP_Num;
```
#### 2. Reasoning
Filter missions by date (`ADD_MONTHS -2`). Then Aggregate (`COUNT`, `SUM`) grouping by Employee.
#### 3. Detailed Explanation
The view simplifies the date logic. `SUM(Retour - Dep)` calculates the total distance traveled.

---

### Exercise 7: Frequent Travelers
**Question:** Employés ayant fait plus d'une mission ces deux derniers mois.

#### 1. Solution
```sql
SELECT E.EMP_Num, E.EMP_Nom, S.SRV_Libelle, COUNT(*) AS NbMiss
FROM EMPLOYE E, Missions_Recentes M, SERVICE S
WHERE E.EMP_Num = M.EMP_Num 
  AND E.SRV_Num = S.SRV_Num
GROUP BY E.EMP_Num, E.EMP_Nom, S.SRV_Libelle
HAVING COUNT(*) > 1
ORDER BY S.SRV_Libelle DESC;
```
#### 2. Reasoning
Reuse the `Missions_Recentes` view. Use `HAVING COUNT(*) > 1` to filter the groups.
#### 3. Detailed Explanation
`WHERE` filters rows before grouping. `HAVING` filters groups after aggregation. We need `HAVING` here.

---

### Exercise 8: Mileage Stats
**Question:** Moyenne, max et min des kilométrages.

#### 1. Solution
```sql
SELECT AVG(MIS_KlmRetour - MIS_KlmDep) AS Moyenne, 
       MAX(MIS_KlmRetour - MIS_KlmDep) AS Maximum,
       MIN(MIS_KlmRetour - MIS_KlmDep) AS Minimum
FROM MISSION;
```
#### 2. Reasoning
Standard SQL aggregate functions applied to a calculated expression (Distance).

---

### Exercise 9: Long Distance Missions
**Question:** Missions dont le kilométrage est supérieur à la moyenne.

#### 1. Solution
```sql
SELECT MIS_Num, (MIS_KlmRetour - MIS_KlmDep) AS Distance
FROM MISSION
WHERE (MIS_KlmRetour - MIS_KlmDep) > (
    SELECT AVG(MIS_KlmRetour - MIS_KlmDep) FROM MISSION
);
```
#### 2. Reasoning
Compare the individual row's distance against a subquery returning the global average.

---

### Exercise 10: Vehicle Usage
**Question:** Km parcourus par véhicule, ordre décroissant.

#### 1. Solution
```sql
SELECT V.VEH_Num, V.VEH_NumMatricule, SUM(M.MIS_KlmRetour - M.MIS_KlmDep) AS Total_Km
FROM VEHICULE V, MISSION M
WHERE V.VEH_Num = M.VEH_Num
GROUP BY V.VEH_Num, V.VEH_NumMatricule
ORDER BY Total_Km DESC;
```
#### 2. Reasoning
Group missions by Vehicle ID and sum the distance.

---

### Exercise 11: The "Road Warrior" Chief
**Question:** Quel est le chef de service qui a le plus roulé ?

#### 1. Solution
```sql
CREATE VIEW Chef_Stats AS 
SELECT C.EMP_Nom, SUM(M.MIS_KlmRetour - M.MIS_KlmDep) AS Total_Km
FROM Chef C, MISSION M
WHERE C.EMP_Num = M.EMP_Num
GROUP BY C.EMP_Nom;

SELECT * FROM Chef_Stats 
WHERE Total_Km = (SELECT MAX(Total_Km) FROM Chef_Stats);
```
#### 2. Reasoning
1. Calculate total distance for every chief (View).
2. Select the chief whose distance equals the maximum distance in that view.

---

### Exercise 12: Hierarchy List
**Question:** Liste des employés avec leur nom et celui de leur chef.

#### 1. Solution
```sql
SELECT E.EMP_Nom AS Employe, Chef.EMP_Nom AS Chef
FROM EMPLOYE E, EMPLOYE Chef
WHERE E.EMP_Responsable = Chef.EMP_Num
ORDER BY Chef.EMP_Nom;
```
#### 2. Reasoning
**Self-Join**: The table `EMPLOYE` is joined with itself. One instance represents the subordinate (`E`), the other represents the manager (`Chef`).

---

### Exercise 13: Mission Count (Zero Included)
**Question:** Nombre de missions par employé (inclure 0 si aucune).

#### 1. Solution
```sql
SELECT E.EMP_Num, E.EMP_Nom, COUNT(M.MIS_Num)
FROM EMPLOYE E LEFT JOIN MISSION M ON E.EMP_Num = M.EMP_Num
GROUP BY E.EMP_Num, E.EMP_Nom;
```
#### 2. Reasoning
Standard `JOIN` excludes employees with no missions. `LEFT JOIN` keeps all employees (`Left` table) and puts NULL for missions if none exist. `COUNT(MIS_Num)` counts non-null values, resulting in 0.

---

### Exercise 14: Universal Brand
**Question:** Marque dont on a des véhicules de toutes les couleurs répertoriées ? (Relational Division).

#### 1. Solution
```sql
SELECT M.MAR_Nom
FROM MARQUE M
WHERE NOT EXISTS (
    SELECT C.COU_Code FROM COULEUR C
    WHERE NOT EXISTS (
        SELECT V.VEH_Num FROM VEHICULE V
        WHERE V.TYP_Num IN (SELECT T.TYP_Num FROM TYPE T WHERE T.MAR_Num = M.MAR_Num)
          AND V.COU_Code = C.COU_Code
    )
);
```
#### 2. Reasoning
"Find a Brand where there is NO color that this brand DOES NOT have." (Division).

---

### Exercise 15 to 17: Security (DCL)

**15. Grant Select to All:**
`GRANT SELECT ON ALL TABLES TO PUBLIC;` (Syntax varies by DB, often table by table).

**16. Grant to TOTO:**
`GRANT ALL PRIVILEGES ON MISSION TO TOTO;`

**17. Revoke from Directeur:**
`REVOKE ALL PRIVILEGES ON EMPLOYE FROM Directeur;`

---

### Exercise 18: Salary Raise
**Question:** Augmenter de 5% le salaire des chefs de service.

#### 1. Solution
```sql
UPDATE EMPLOYE
SET EMP_Salaire = EMP_Salaire * 1.05
WHERE EMP_Num IN (SELECT EMP_Responsable FROM EMPLOYE);
```
#### 2. Reasoning
Update rows where the employee ID appears in the `Responsable` column of the table (or matches the logic for being a chief).

---

### Exercise 19: Delete Renault Missions
**Question:** Supprimer missions faites en Renault.

#### 1. Solution
```sql
DELETE FROM MISSION 
WHERE VEH_Num IN (
    SELECT V.VEH_Num 
    FROM VEHICULE V, TYPE T, MARQUE M
    WHERE V.TYP_Num = T.TYP_Num 
      AND T.MAR_Num = M.MAR_Num 
      AND M.MAR_Nom = 'Renault'
);
```
#### 2. Reasoning
Subquery finds IDs of Renault vehicles. Main query deletes missions linked to those IDs.

---

### Exercise 20: Cascading Delete Setup
**Question:** Permettre la suppression d’une couleur (Cascade).

#### 1. Solution
```sql
ALTER TABLE VEHICULE 
DROP CONSTRAINT FK_Veh_Coul;

ALTER TABLE VEHICULE 
ADD CONSTRAINT FK_Veh_Coul 
FOREIGN KEY (COU_Code) REFERENCES COULEUR(COU_Code) ON DELETE CASCADE;
```
#### 2. Reasoning
By default, you cannot delete a Color if a Vehicle uses it. `ON DELETE CASCADE` allows the deletion, automatically deleting the referencing Vehicles (or setting them to NULL depending on requirement, but here context implies enabling the action).

---

### Exercise 21 & 22: View Security
**Question:** Vue pour responsable 'A003' + Droits.

#### 1. Solution
```sql
-- Q21
CREATE VIEW V_Pers_A003 AS
SELECT * FROM EMPLOYE WHERE SRV_Num = 'A003';

-- Q22
GRANT SELECT ON V_Pers_A003 TO Gerant, Directeur WITH GRANT OPTION;
REVOKE SELECT ON V_Pers_A003 FROM Gerant, Directeur;
```
#### 2. Reasoning
Views restrict row access (Vertical/Horizontal security). `WITH GRANT OPTION` allows them to pass this right to others.

---

### Exercise 23: Manual Integrity Check
**Question:** Si le SGBD ne gère pas les FK, comment faire ?

#### 1. Solution
1.  **Triggers (Déclencheurs)**: Create a `BEFORE INSERT` or `UPDATE` trigger on `EMPLOYE` that queries `SERVICE` to ensure `SRV_Num` exists. Raise error if not.
2.  **Application Logic**: Check the existence of the Service ID in the application code (Java/PHP) before sending the SQL `INSERT` command.

#### 3. Detailed Explanation
Foreign Keys are declarative. Without them, we must implement procedural checks. Triggers are the closest to the data (in the database). Application logic is safer but relies on the developer not making mistakes.