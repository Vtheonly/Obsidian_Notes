
---


### 2008 Retake

**Year:** 2008
**Type:** Retake
**Correction:** Yes

#### Exercise 1 (Part I & II)

**Statement:**
Given the following relational schema describing a real estate agency network:

*   **Agency** (agencyNum, street, city, zipCode)
*   **Staff** (staffNum, lastName, firstName, position, gender, birthDate, salary, agencyNum)
*   **PropertyForRent** (propertyNum, street, city, zipCode, type, rooms, rentAmount, ownerNum, staffNum, agencyNum)
*   **Client** (clientNum, lastName, firstName, address, phoneNum, prefType, maxRent)
*   **Owner** (ownerNum, lastName, firstName, address, phoneNum)
*   **Visit** (clientNum, propertyNum, visitDate, comment)
*   **Registration** (clientNum, agencyNum, staffNum, registrationDate)

**Work to be done:**

**I/** Give in SQL the commands to create the tables "Agency", "PropertyForRent" and "Visit", specifying the data type of each column as well as the integrity constraints ensuring the consistency of data. Among the constraints, one can find:
*   The column "Staff.gender" can only contain 'M' or 'F'.
*   Prohibition for staff to administer more than 100 properties at a time.
*   etc...

**II/** Program the following queries in SQL:

1.  Numbers of all properties for rent that have already been visited.
2.  Number, name, first name, and monthly salary of staff whose annual salary is > 10,000 DA.
3.  Staff whose salary is between 10,000 DA and 30,000 DA, and whose position is 'Manager' or 'Supervisor'.
4.  List of properties classified by ascending order of property type and by descending order of rent amount.
5.  Number of properties whose rent amount is greater than 7,000 DA.
6.  Number of properties that were visited in May 2004.
7.  Total number of managers (Staff.position) and calculate the total sum of their salaries.
8.  Find the number of employees working in each agency and calculate the sum of their salaries for each agency.
9.  For all agencies with more than one employee, find the number of employees working in each agency and the sum of their salaries.
10. List of employees whose salary is greater than the average salary.
11. List of all employees whose salary is greater than at least one salary of an employee from agency "A003".
12. Find the number of properties managed by each staff member.
13. Find all staff members who work at the Boumerdes agency (provide 2 solutions).
14. List of cities that have both an agency and at least one property for rent.
15. Create a view such that the manager of agency "A003" can see details only of the staff working in their agency.
16. Grant the SELECT privilege on the "Agency" table to all users.
17. Grant the user "manager" all privileges on the "Staff" table.
18. Revoke from user "Director" all privileges granted on the "Staff" table.
19. Insert a new line into the Staff table and give values to all mandatory columns: staffNum, name, firstName, position, gender, salary, and agencyNum.
20. Increase the salary of all managers by 5%.
21. Promote Mr. Rabah ZHAR (StaffNum = 'EM14') to the rank of 'Manager' and raise his salary to 250,000 DA.
22. Delete all lines from the Visit table.

#### Correction

```sql
-- I/ Table Creation

CREATE TABLE PropertyForRent(
    propertyNum varchar(5) PRIMARY KEY, 
    street varchar(25) not null,
    city varchar(15) not null,
    zipCode varchar(8),
    type number(1) default 'A' check (type in ('A','M')),
    rooms number(2) not null default 4 check(rooms between 1 and 15),
    rentAmount decimal(7,2) not null,
    ownerNum varchar(5) not null,
    staffNum varchar(5) not null,
    agencyNum char(4) not null,
    FOREIGN KEY (ownerNum) REFERENCES Owner,
    FOREIGN KEY (staffNum) REFERENCES Staff,
    FOREIGN KEY (agencyNum) REFERENCES Agency
);

CREATE TABLE Agency(
    agencyNum char(4) PRIMARY KEY,
    street varchar(25) not null, 
    city varchar(15) not null, 
    zipCode varchar(8)
);

CREATE TABLE Visit(
    clientNum varchar(5) not null,
    propertyNum varchar(5) not null,
    visitDate date not null,
    comment varchar(255),
    PRIMARY KEY (clientNum, propertyNum),
    FOREIGN KEY (clientNum) REFERENCES Client,
    FOREIGN KEY (propertyNum) REFERENCES PropertyForRent
);

-- II/ SQL Queries

-- 1. Numbers of all properties for rent that have already been visited
SELECT DISTINCT propertyNum 
FROM Visit;

-- 2. Number, name, first name, and monthly salary of staff whose annual salary is > 10,000 DA
SELECT staffNum, lastName, firstName, position, salary/12 AS monthlySalary
FROM Staff
WHERE salary > 10000;

-- 3. Staff whose salary is between 10,000 DA and 30,000 DA, 
-- and whose position is 'Manager' or 'Supervisor'
SELECT staffNum, lastName, firstName, position, salary
FROM Staff
WHERE salary BETWEEN 10000 AND 30000
AND position IN ('Manager', 'Supervisor');

-- 4. List of properties classified by ascending order of type and descending order of rent
SELECT propertyNum, type, rooms, rentAmount
FROM PropertyForRent
ORDER BY type ASC, rentAmount DESC;

-- 5. Number of properties whose rent amount is greater than 7,000 DA
SELECT COUNT(*) AS Number
FROM PropertyForRent
WHERE rentAmount > 7000;

-- 6. Number of properties that were visited in May 2004
SELECT COUNT(DISTINCT propertyNum) As Number
FROM Visit
WHERE visitDate BETWEEN '01 May 04' AND '31 Mai 04';

-- 7. Total number of managers and calculate the total sum of their salaries
SELECT COUNT(staffNum) As Number, SUM(salary) AS TotalSum
FROM Staff
WHERE position = 'Manager';

-- 8. Find the number of employees working in each agency and sum of their salaries
SELECT agencyNum, COUNT(staffNum) AS Number, SUM(salary) AS TotalSum
FROM Staff
GROUP BY agencyNum
ORDER BY agencyNum;

-- 9. For all agencies with more than one employee, find the count and sum of salaries
SELECT agencyNum, COUNT(staffNum) AS Number, SUM(salary) AS TotalSum
FROM Staff
GROUP BY agencyNum
HAVING COUNT(staffNum) > 1
ORDER BY agencyNum;

-- 10. List of employees whose salary is greater than the average salary
SELECT staffNum, lastName, firstName, salary
FROM Staff
WHERE salary > (SELECT AVG(salary) FROM Staff);

-- 11. List of all employees whose salary is greater than at least one salary of agency "A003"
SELECT staffNum, lastName, firstName, position, salary
FROM Staff
WHERE salary > SOME (SELECT salary FROM Staff WHERE agencyNum='A003');

-- 12. Find the number of properties managed by each staff member
SELECT p.agencyNum, p.staffNum, COUNT(*) AS Number
FROM Staff p, PropertyForRent l
WHERE p.staffNum = l.staffNum
GROUP BY p.agencyNum, p.staffNum
ORDER BY p.agencyNum, p.staffNum;

-- 13. Find all staff members who work at the Boumerdes agency (2 solutions)
SELECT staffNum, lastName, firstName, position
FROM Staff p, Agency a
WHERE p.agencyNum = a.agencyNum 
AND city = 'Boumerdes';

-- 14. List of cities that have both an agency and at least one property for rent
-- Version 1:
(SELECT city FROM Agency)
INTERSECT
(SELECT city FROM PropertyForRent);

-- Version 2:
SELECT city
FROM Agency a, PropertyForRent l
WHERE a.city = l.city;

-- Version 3:
SELECT DISTINCT city
FROM Agency a
WHERE EXISTS (SELECT * 
 FROM PropertyForRent l
 WHERE a.city = l.city);

-- 15. Create a view such that the manager of agency "A003" can see details 
-- only of the staff working in their agency
CREATE VIEW Manager3Staff
AS SELECT *
FROM Staff
WHERE agencyNum ='A003';

-- 16. Grant the SELECT privilege on the "Agency" table to all users
GRANT SELECT
ON Agency
TO PUBLIC;

-- 17. Grant the user "manager" all privileges on the "Staff" table
GRANT ALL PRIVILEGES
ON Staff
TO Manager WITH GRANT OPTION;

-- 18. Revoke from user "Director" all privileges granted on the "Staff" table
REVOKE ALL PRIVILEGES
ON Staff
FROM Director;

-- 19. Insert a new line into the Staff table
INSERT INTO Staff(staffNum, lastName, firstName, position, gender, salary, agencyNum)
VALUES ('SM44', 'ZHAR', 'Ahmed', 'Manager', 'M', 1000000, 'A003');

-- 20. Increase the salary of all managers by 5%
UPDATE Staff
SET salary = salary * 1.05
WHERE position ='Manager';

-- 21. Promote Mr. Rabah ZHAR (StaffNum = 'EM14') to 'Manager' and salary 250,000 DA
UPDATE Staff
SET position ='Manager', salary = 250000
WHERE staffNum = 'EM14';

-- 22. Delete all lines from the Visit table
DELETE FROM Visit;
```