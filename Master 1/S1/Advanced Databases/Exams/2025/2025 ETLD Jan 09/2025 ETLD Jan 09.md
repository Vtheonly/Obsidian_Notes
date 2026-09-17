Here are the final 2 exams from the year 2025.

---

### 2025 ETLD (Exam)

**Year:** 2025
**Type:** Exam (ETLD - Continuous Assessment)
**Correction:** Yes

#### QCM (2 pts)

**Statement:**
1.  Check the algebraic expression(s) equivalent to: $\sigma_{A=B} (R \times S)$
    *   $\Pi_B(\Pi_A(R) \times S)$
    *   $R \bowtie_{A=B} S$
    *   $\Pi_{A,B}(R - S)$
    *   None

2.  Check the algebraic expression(s) equivalent to: $R - (S - R)$
    *   $R \cap S$
    *   $R$
    *   $S$
    *   $\emptyset$
    *   None

#### Exercise 1 (8 pts)

**Statement:**
Given the following database:
*   **Client** (idc, name, firstname, city)
*   **Order** (idcmd, #idc, #idp, datecmd, qtycmd)
*   **Product** (idp, label, unitprice)

**Questions:**
1.  Give the SQL code to create this database.
2.  Give the SQL code to create a function that calculates the number of orders made between two dates passed as parameters. Give an example of calling this function.
3.  Give the SQL code to create a procedure that uses the previous function to count the number of orders made between two dates (Date1 and Date2) and displays the message:
    a.  'Red Period' if this number is greater than 100.
    b.  'Yellow Period' if this number is between 50 and 100.
    c.  'White Period' otherwise.
4.  What is the code to add to the previous procedure to control that Date1 is always earlier than Date2?

#### Exercise 2 (4 pts)

**Statement:**
Consider the schema:
*   **CINEMA** (NoCinema, Address, Manager)
*   **HALL** (NoCinema, NoHall, Capacity)

**Hypotheses:**
*   There are 300 tuples in CINEMA, occupying 30 pages.
*   There are 1200 tuples in HALL, occupying 120 pages.
*   Assume that only 5% of halls have more than 150 seats.

**Questions:**
1.  Give the SQL query to display the address of cinemas having halls with more than 150 seats.
2.  Given the following algebraic representation: $\Pi_{Cinema}(\sigma_{Capacity>150}(CINEMA \bowtie HALL))$
    a.  Give the cost of this representation.
3.  Propose another more optimal algebraic representation.
4.  What is its cost?

#### Exercise 3 (6 pts)

**Statement:**
Given the following relational schema, realized by an intern but unfortunately incomplete:
*   **Consortiums** (idC, nameC, dateC)
*   **Probes** (idS, nameS, launchDate, launchPlace, mass, #idC)
*   **Planets** (nomP, gravity, speed, discoverer)
*   **Observations** (#idS, #nomP, dateO, description)
*   **Equipment** (idE, nameE, categoryE)
*   **Assemblages** (#idS, #idE, location)

**Questions:**
During tests, the following SQL query is executed:
```sql
SELECT nameC, nameS
FROM Probes s, Consortiums c, Observations o
WHERE s.idC = c.idC AND s.idS = o.idS AND YEAR(dateO) = 2006;
```
1.  Consider the following part of an algebraic plan: $OBSERVATIONS \bowtie PROBES \bowtie CONSORTIUMS$.
    The table **Observations** contains 50,000 tuples of 200 bytes, the table **Probes** contains 5,000 tuples of 200 bytes, and the table **Consortiums** contains 300 tuples of 100 bytes. Primary keys are stored on 4 bytes.
    a.  How many tuples (maximum) are returned by this query?
    b.  What is the size of each tuple?
2.  Which algebraic plan(s) can be generated for the SQL query?
3.  Among the plans in question 2, which one is optimal?

#### Correction

**QCM:**
1.  **Correct Answer:** $R \bowtie_{A=B} S$
2.  **Correct Answer:** $R$

**Exercise 1:**

**1. Database Creation**
```sql
-- Create Database
CREATE DATABASE gestion_commande;
USE gestion_commande;

-- Create Client
CREATE TABLE Client (
    idc INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    ville VARCHAR(50)
);

-- Create Product
CREATE TABLE Produit (
    idp INT AUTO_INCREMENT PRIMARY KEY,
    libelle VARCHAR(100),
    prixunitaire DECIMAL(10, 2)
);

-- Create Order
CREATE TABLE Commande (
    idcmd INT AUTO_INCREMENT PRIMARY KEY,
    idc INT,
    idp INT,
    datecmd DATE,
    qtitecmd INT,
    FOREIGN KEY (idc) REFERENCES Client(idc),
    FOREIGN KEY (idp) REFERENCES Produit(idp)
);
```

**2. Function Code**
```sql
DELIMITER //
CREATE FUNCTION NombreCommandesEntreDates(p_date_debut DATE, p_date_fin DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE nombre_commandes INT;
    -- Count orders between dates
    SELECT COUNT(*) INTO nombre_commandes
    FROM Commande
    WHERE datecmd BETWEEN p_date_debut AND p_date_fin;
    RETURN nombre_commandes;
END //
DELIMITER ;

-- Call to function
SELECT NombreCommandesEntreDates('2025-01-01', '2025-01-31') AS TotalCommandes;
```

**3. Procedure Code**
```sql
DELIMITER //
CREATE PROCEDURE AfficherMessageCommandes(IN p_date_debut DATE, IN p_date_fin DATE)
BEGIN
    DECLARE nombre_commandes INT;
    -- Call function
    SET nombre_commandes = NombreCommandesEntreDates(p_date_debut, p_date_fin);
    
    -- Display message based on count
    IF nombre_commandes > 100 THEN
        SELECT 'Période rouge' AS Message;
    ELSEIF nombre_commandes BETWEEN 50 AND 100 THEN
        SELECT 'Période jaune' AS Message;
    ELSE
        SELECT 'Période blanche' AS Message;
    END IF;
END //
DELIMITER ;
```

**4. Error Management Code**
```sql
-- Check dates
IF p_date_debut > p_date_fin THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La date de début doit être antérieure à la date de fin.';
END IF;
```

**Exercise 2:**

**1. SQL Query**
```sql
SELECT Adresse
FROM CINEMA, SALLE
WHERE capacité > 150
AND CINEMA.NoCinema = SALLE.NoCinema; -- Correction implies Join on Cinema Name or ID (assumed NoCinema is key)
-- Note: Correction explicitly uses "CINEMA.cinéma = Salle.cinéma" logic
```

**2. Cost Calculation (Non-Optimized)**
*   **Join:** Reading 3,600 pages ($120 \times 30$).
*   **Selection:** We obtain 5% of 120 pages, i.e., 6 pages.
*   **Total I/O:** $3600 + (120 \times 2) + 6 = 3846$ (Based on correction logic: Cartesian product cost logic applied).

**3. Optimized Representation**
$\Pi_{Cinema}(CINEMA \bowtie \sigma_{Capacity>150}(SALLE))$

**4. Optimized Cost**
*   **Selection:** Reads 120 pages and obtains 6 pages.
*   **Join:** Reads 180 pages ($6 \times 30$).
*   **Total I/O:** $120 + 6 + 180 + 6 = 312$.

**Exercise 3:**

**1. Tuples and Size**
a.  **Number of tuples:** 50,000 (Based on the largest table driving the result in a join without filtering).
b.  **Tuple size:** 492 bytes.

**2. Algebraic Plans**
*   $\Pi_{names}(\sigma_{year=2006}(Observations) \bowtie Consortiums \bowtie Sondes)$
*   $\Pi_{names}(\sigma_{join}(\Pi(Obs) \times \Pi(Sondes) \bowtie Consortiums))$
*   (Various combinations of join orders are valid candidates).

**3. Optimal Plan**
*   Plan involving filtering $\sigma_{year=2006}$ on **Observations** *before* joining is optimal. Specifically:
    $\Pi_{names}((\sigma_{year=2006} Observations) \bowtie Sondes \bowtie Consortiums)$

---
