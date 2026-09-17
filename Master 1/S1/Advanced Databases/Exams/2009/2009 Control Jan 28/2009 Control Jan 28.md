Here are the next 3 exams from the year 2009.

---

### 2009 Control 2

**Year:** 2009
**Type:** Control
**Correction:** No (AI-Generated Solution Provided)

#### Exercise 1

**Statement:**
Given the following relational schema describing a faculty:

*   **Student** (NumStud, Name, FirstName, Street, ZipCode, City, Phone, Age, DeptNum)
*   **Department** (DeptNum, DeptName, Manager, Budget)

**Work to be done in SQL:**

1.  Write the commands to create these 2 tables.
2.  List of students whose number is between 180 and 200, living in the city "P'VILLE".
3.  Number and average age of students living in 'Boumerdès' and enrolled in the 'Computer Science' department.
4.  Number of students in each city that shelters more students than the city 'Boumerdès'.
5.  Create a view named STUD-INF that allows consulting only the students of the Computer Science departments.
6.  Modify the Name, First Name, and City of the student number 1000.

#### Correction (AI-Generated)

```sql
-- 1. Write the commands to create these 2 tables
CREATE TABLE Department (
    DeptNum INT PRIMARY KEY,
    DeptName VARCHAR(50),
    Manager VARCHAR(50),
    Budget DECIMAL(10, 2)
);

CREATE TABLE Student (
    NumStud INT PRIMARY KEY,
    Name VARCHAR(50),
    FirstName VARCHAR(50),
    Street VARCHAR(100),
    ZipCode VARCHAR(10),
    City VARCHAR(50),
    Phone VARCHAR(15),
    Age INT,
    DeptNum INT,
    FOREIGN KEY (DeptNum) REFERENCES Department(DeptNum)
);

-- 2. List of students whose number is between 180 and 200, 
-- living in the city "P'VILLE"
SELECT * 
FROM Student
WHERE NumStud BETWEEN 180 AND 200
  AND City = 'P''VILLE';

-- 3. Number and average age of students living in 'Boumerdès' 
-- and enrolled in the 'Computer Science' department
SELECT COUNT(*) AS StudentCount, AVG(Age) AS AverageAge
FROM Student S, Department D
WHERE S.DeptNum = D.DeptNum
  AND S.City = 'Boumerdès'
  AND D.DeptName = 'Computer Science';

-- 4. Number of students in each city that shelters more students 
-- than the city 'Boumerdès'
SELECT City, COUNT(*) AS StudentCount
FROM Student
GROUP BY City
HAVING COUNT(*) > (
    SELECT COUNT(*) 
    FROM Student 
    WHERE City = 'Boumerdès'
);

-- 5. Create a view named STUD-INF that allows consulting only 
-- the students of the Computer Science departments
CREATE VIEW STUD_INF AS
SELECT S.*
FROM Student S, Department D
WHERE S.DeptNum = D.DeptNum
  AND D.DeptName = 'Computer Science';

-- 6. Modify the Name, First Name, and City of the student number 1000
UPDATE Student
SET Name = 'NewName', FirstName = 'NewFirstName', City = 'NewCity'
WHERE NumStud = 1000;
```

---
