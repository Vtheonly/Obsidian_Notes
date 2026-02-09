
### 2009 Exam (February)

**Year:** 2009
**Type:** Exam
**Correction:** Yes

#### Context
In a company, employees often travel on missions. They use one of the company's cars and sometimes leave for several days.
Here is the relational schema of the mission management domain:

*   **EMPLOYEE** (EMP_Num, EMP_Title, EMP_Lastname, EMP_Salary, SRV_Num, EMP_Manager)
*   **SERVICE** (SRV_Num, SRV_Label)
*   **MISSION** (MIS_Num, VEH_Num, EMP_Num, MIS_DepDay, MIS_DepKm, MIS_ReturnDay, MIS_ReturnKm)
*   **VEHICLE** (VEH_Num, VEH_PlateNum, COL_Code, VEH_PurchaseDate, VEH_PurchasePrice, TYP_Num)
*   **TYPE** (TYP_Num, TYP_Name, TYP_Power, TYP_Weight, TYP_Consumption, BRD_Num)
*   **BRAND** (BRD_Num, BRD_Name)
*   **COLOR** (COL_Code, COL_Label)

**Management Rules:**
*   The MISSION table contains only missions from the current month and the previous 11 months.
*   On the same day, an employee cannot leave on more than two missions.
*   A mission can last more than one day.
*   The color of a vehicle is either black or white.
*   Cars cannot drive more than 150,000 Km.

#### Exercise 1 (Part I)

**Statement:**
Give in SQL the commands to create the preceding tables specifying the data type of each column as well as the integrity constraints ensuring data consistency.

#### Exercise 2 (Part II)

**Statement:**
Program the following queries in SQL:

1.  List of numbers and names of employees in a service of which we only know the first 2 letters 'FI'.
2.  List of employees who went on a mission in the current month.
3.  List of service managers.
4.  List of vehicles with the name of their color, by brand then by type and finally in chronological order of purchase.
5.  List of missions of service managers.
6.  Number of missions, kilometers traveled in alphabetical order of employees for the last two months.
7.  Number of missions by employee name (with the name of their service) provided they have performed more than one in the last two months.
8.  Average, maximum, and minimum mileages of all missions.
9.  List of missions where the mileage is greater than the average mileage of missions.
10. Number of kilometers traveled by each vehicle in descending order.
11. Which service manager has driven the most?
12. List of employees with their name and that of their manager.
13. Number of missions per employee. Those who have not performed any must appear in the result with the digit zero.
14. Is there a brand of which we have vehicles of all listed colors?
15. Grant all employees the SELECT privilege on the entire database.
16. Grant the user "TOTO" all privileges on the table "MISSION".
17. Revoke from the user "Director" all privileges granted on the table "EMPLOYEE".
18. Increase the salary of all service managers by 5%.
19. Delete all missions performed with Renault brand vehicles.
20. Make the necessary declarations to the database so that the deletion of a color can always be done.

#### Correction

```sql
-- Part I: Constraints (Conceptual)
-- Check on EMPLOYEE.EMP_Title: Check (EMP_Title in ('Mr','Ms','Mrs'))
-- Reference on MISSION.EMP_Num: References EMPLOYEE(EMP_Num)
-- Reference on MISSION.VEH_Num: References VEHICLE(VEH_Num)
-- Reference on VEHICLE.COL_Code: References COLOR(COL_Code)
-- Reference on VEHICLE.TYP_Num: References TYPE (TYP_Num)
-- Check on MISSION.MIS_ReturnKm: Check(MIS_ReturnKm <= 150000)
-- Reference on TYPE.BRD_Num: References BRAND(BRD_Num)
-- Check on COLOR.COL_Label: Check (COL_Label in ('White','Black'))

-- Part II: Queries

-- 1. List of numbers and names of employees in a service 
-- of which we only know the first 2 letters 'FI'.
SELECT EMP_Num, EMP_Lastname FROM EMPLOYEE 
WHERE SRV_Num = (SELECT SRV_Num FROM SERVICE WHERE SRV_Label LIKE "FI*");

-- 2. List of employees who went on a mission in the current month.
SELECT EMP_Num, EMP_Lastname FROM EMPLOYEE
WHERE EMP_Num IN (SELECT EMP_Num FROM MISSION WHERE MONTH(MIS_DepDay) = MONTH(DATE()))
ORDER BY EMP_Lastname;

-- 3. List of service managers.
SELECT EMP_Num, EMP_Lastname, SRV_Label FROM EMPLOYEE E, SERVICE S
WHERE E.SRV_Num = S.SRV_Num AND EMP_Num = EMP_Manager ORDER BY EMP_Lastname;

-- 4. List of vehicles with the name of their color, by brand then by type 
-- and finally in chronological order of purchase.
SELECT V.VEH_Num, BRD_Name, TYP_Name, VEH_PlateNum, VEH_PurchaseDate, COL_Label
FROM VEHICLE V, TYPE T, BRAND M, COLOR C
WHERE V.TYP_Num = T.TYP_Num AND T.BRD_Num = M.BRD_Num AND V.COL_Code = C.COL_Code
ORDER BY BRD_Name, TYP_Name, VEH_PurchaseDate;

-- 5. List of missions of service managers.
-- Step 1: Create View
CREATE VIEW Manager AS 
SELECT SRV_Label AS mgr_srv, EMP_Num AS mgr_num, EMP_Lastname AS mgr_name
FROM EMPLOYEE E, SERVICE S
WHERE EMP_Num = EMP_Manager AND E.SRV_Num = S.SRV_Num;
-- Step 2: Query
SELECT mgr.*, MIS_Num, MIS_DepDay, MIS_ReturnDay
FROM Manager, MISSION
WHERE EMP_Num = mgr_num ORDER BY mgr_name, MIS_DepDay;

-- 6. Number of missions, kilometers traveled in alphabetical order of employees 
-- for the last two months.
-- Step 1: Create View for last 2 months
CREATE VIEW mis2months AS 
SELECT * FROM MISSION WHERE MONTH(MIS_DepDay) >= MONTH(DATE()) - 1;
-- Step 2: Query
SELECT EMP_Lastname, E.EMP_Num, COUNT(*) AS NbMissions, 
       SUM(MIS_ReturnKm - MIS_DepKm) AS NbKilms
FROM EMPLOYEE E, mis2months M2 WHERE E.EMP_Num = M2.EMP_Num
GROUP BY EMP_Lastname, E.EMP_Num;

-- 7. Number of missions by employee name (with service name) provided 
-- they have performed more than one in the last two months.
SELECT E.EMP_Num, EMP_Lastname, SRV_Label, COUNT(*) AS NbMiss
FROM EMPLOYEE E, mis2months M2, SERVICE S
WHERE E.EMP_Num = M2.EMP_Num AND E.SRV_Num = S.SRV_Num
GROUP BY E.EMP_Num, EMP_Lastname, SRV_Label
HAVING COUNT(*) > 1
ORDER BY SRV_Label DESC;

-- 8. Average, maximum, and minimum mileages of all missions.
SELECT AVG(MIS_ReturnKm - MIS_DepKm) AS Average, 
       MAX(MIS_ReturnKm - MIS_DepKm) AS Maximum,
       MIN(MIS_ReturnKm - MIS_DepKm) AS Minimum
FROM MISSION;

-- 9. List of missions where the mileage is greater than the average mileage.
SELECT MIS_Num, MIS_ReturnKm - MIS_DepKm AS nbkil FROM MISSION
WHERE MIS_ReturnKm - MIS_DepKm > 
      (SELECT AVG(MIS_ReturnKm - MIS_DepKm) FROM MISSION);

-- 10. Number of kilometers traveled by each vehicle in descending order.
SELECT V.VEH_Num, VEH_PlateNum, SUM(MIS_ReturnKm - MIS_DepKm) AS NbKil
FROM VEHICLE V, MISSION M WHERE V.VEH_Num = M.VEH_Num
GROUP BY V.VEH_PlateNum ORDER BY 3 DESC;

-- 11. Which service manager has driven the most.
-- Step 1: Create View
CREATE VIEW R11 AS 
SELECT mgr_srv, mgr_num, mgr_name, SUM(MIS_ReturnKm - MIS_DepKm) AS Nbkil 
FROM Manager, MISSION WHERE EMP_Num = mgr_num GROUP BY mgr_srv, mgr_num, mgr_name;
-- Step 2: Query
SELECT * FROM R11 WHERE Nbkil = (SELECT MAX(Nbkil) FROM R11);

-- 12. List of employees with their name and that of their manager.
SELECT X.EMP_Num, X.EMP_Lastname, Y.EMP_Num AS Num_Mgr, Y.EMP_Lastname AS NameMgr
FROM EMPLOYEE X, EMPLOYEE Y
WHERE X.EMP_Manager = Y.EMP_Num
ORDER BY Y.EMP_Lastname;

-- 13. Number of missions per employee. Those who have not performed any must appear with zero.
SELECT E.EMP_Num, EMP_Lastname, COUNT(MIS_Num) AS NbMissions
FROM EMPLOYEE E LEFT OUTER JOIN MISSION M ON E.EMP_Num = M.EMP_Num
GROUP BY E.EMP_Num, EMP_Lastname;

-- 14. Is there a brand of which we have vehicles of all listed colors?
SELECT DISTINCT BRD_Name, COL_Code
FROM VEHICLE V, TYPE T, BRAND M
WHERE V.TYP_Num = T.TYP_Num AND T.BRD_Num = M.BRD_Num
GROUP BY BRD_Name
HAVING COUNT(DISTINCT COL_Code) = (SELECT COUNT(*) FROM COLOR);

-- 15. Grant all employees the SELECT privilege on the entire database.
GRANT SELECT ON ALL TO PUBLIC;

-- 16. Grant the user "TOTO" all privileges on the table "MISSION".
GRANT ALL PRIVILEGES ON MISSION TO TOTO;

-- 17. Revoke from the user "Director" all privileges granted on the table "EMPLOYEE".
REVOKE ALL PRIVILEGES ON EMPLOYEE FROM Director;

-- 18. Increase the salary of all service managers by 5%.
UPDATE EMPLOYEE
SET EMP_Salary = EMP_Salary * 1.05
WHERE EMP_Num = EMP_Manager;

-- 19. Delete all missions performed with Renault brand vehicles.
DELETE FROM MISSION M
WHERE VEH_Num IN ( 
    SELECT VEH_Num 
    FROM VEHICLE V, TYPE T, BRAND B 
    WHERE V.TYP_Num = T.TYP_Num
    AND T.BRD_Num = B.BRD_Num
    AND BRD_Name = 'Renault'
);

-- 20. Make the necessary declarations to the database so that the deletion 
-- of a color can always be done.
-- Update Attribute definition for "VEHICLE.COL_Code":
-- VEHICLE.COL_Code Varchar(10) References COLOR(COL_Code) ON DELETE CASCADE;
-- (Note: The correction in the image mentions deleting missions as well via cascade 
-- if a vehicle is deleted, but the question specifically asks about deleting a color).
```

---
