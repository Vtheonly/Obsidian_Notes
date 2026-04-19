
### 2023 Control

**Year:** 2023
**Type:** Control (N1)
**Correction:** No (AI-Generated Solution Provided)

#### Exercise 1

**Statement:**
Given the following relational database:
*   **Patient** (PatCode, Name, Firstname, Addr, InsNum)
*   **Doctor** (DocCode, DocName)
*   **Disease** (DisCode, DisName)
*   **Insurer** (InsNum, InsName, InsAddr)
*   **Hospitalization** (PatCode, DocCode, DisCode, StartDate, EndDate)

**Express the following queries in SQL (use join):**

1.  List of hospitalizations with the patient's name, doctor's name, and disease name.
2.  Find doctors (name) who examined the patient linked to insurance number (1892065).
3.  Find the names of diseases that were examined by doctors "Mohamed" and "Ali".

#### Exercise 2

**Statement:**
Given the following relational schema:
*   **Individual** (ind_num, name, firstname)
*   **Act** (ind_num, film_num, role)
*   **Film** (film_num, ind_num, title, genre, year)
    *   *Note: ind_num in Film likely refers to the Director.*
*   **Screening** (cinema_num, film_num, pdate)
*   **Cinema** (cinema_num, name, address)

1.  **Express the following queries in Relational Algebra:**
    a.  List all names and first names of individuals who acted in a film in 2022.
    b.  Find all numbers of individuals who acted in *all* films.

2.  **What does the following query do:**
    $$ \Pi_{ind\_num, name, firstname} (\sigma_{genre='Comedy'}(Film) \bowtie_{Film.film\_num = Act.film\_num} Act) - \Pi_{ind\_num, name, firstname} (\sigma_{genre='Drama'}(Film) \bowtie_{Film.film\_num = Act.film\_num} Act) $$

#### Correction (AI-Generated)

```sql
-- Exercise 1 (SQL)

-- 1. List of hospitalizations with names
SELECT P.Name AS Patient, D.DocName AS Doctor, M.DisName AS Disease
FROM Hospitalization H
JOIN Patient P ON H.PatCode = P.PatCode
JOIN Doctor D ON H.DocCode = D.DocCode
JOIN Disease M ON H.DisCode = M.DisCode;

-- 2. Doctors who examined patient with insurance 1892065
SELECT DISTINCT D.DocName
FROM Doctor D
JOIN Hospitalization H ON D.DocCode = H.DocCode
JOIN Patient P ON H.PatCode = P.PatCode
WHERE P.InsNum = 1892065;

-- 3. Diseases examined by BOTH "Mohamed" and "Ali"
-- (INTERSECT logic)
SELECT M.DisName
FROM Disease M
JOIN Hospitalization H ON M.DisCode = H.DisCode
JOIN Doctor D ON H.DocCode = D.DocCode
WHERE D.DocName = 'Mohamed'
INTERSECT
SELECT M.DisName
FROM Disease M
JOIN Hospitalization H ON M.DisCode = H.DisCode
JOIN Doctor D ON H.DocCode = D.DocCode
WHERE D.DocName = 'Ali';
```

**Exercise 2 (Relational Algebra)**

**1. Queries:**

a. **List names of individuals who acted in a film in 2022.**
$$ R1 \leftarrow \sigma_{year=2022}(Film) $$
$$ R2 \leftarrow R1 \bowtie_{Film.film\_num = Act.film\_num} Act $$
$$ R3 \leftarrow R2 \bowtie_{Act.ind\_num = Individual.ind\_num} Individual $$
$$ Result \leftarrow \Pi_{name, firstname}(R3) $$

b. **Find individuals who acted in ALL films (Division).**
$$ AllFilms \leftarrow \Pi_{film\_num}(Film) $$
$$ ActorFilms \leftarrow \Pi_{ind\_num, film\_num}(Act) $$
$$ Result \leftarrow ActorFilms \div AllFilms $$

**2. Query Explanation:**
The expression performs the Difference (MINUS) between two sets:
1.  Set A: Individuals (Actors) who acted in 'Comedy' films.
2.  Set B: Individuals (Actors) who acted in 'Drama' films.

**Result:** It returns the list of individuals (num, name, firstname) who have acted in at least one **Comedy** but have **NEVER** acted in a **Drama**.