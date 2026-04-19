
### 2012 Control

**Year:** 2012
**Type:** Control
**Correction:** No (AI-Generated Solution Provided)

#### Exercise 1

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

1.  Give in SQL the commands to create the tables "**Registration**" (Inscription) and "**Client**" specifying the data type of each column and integrity constraints.
    *   The registration date is later than the current date (Note: Usually registration is <= current, but prompt says "postérieure" which means later/after. This might be a logic trap or specific rule, assuming planned registration).
    *   Preference type is either 'Apartment' or 'House'.
    *   Phone number is 10 digits and always starts with '06'.
2.  Staff whose salary is between 10,000 DA and 30,000 DA, position is 'Manager' or 'Supervisor', and the birth month is even.
3.  Number of properties visited in May of last year.
4.  List of all employees whose salary is greater than at least one salary of an employee from agency "A003".
5.  Find the number of properties managed by each staff member.
6.  Find all staff members who work at the Boumerdes agency (provide 2 solutions).
7.  Create a view such that the manager of agency "A003" can see details only of the staff working in their agency.
8.  Grant the SELECT privilege on the "**Agency**" table to all users.
9.  Promote Mr. Rabah ZHAR (StaffNum = 'EM14') to the rank of 'Manager' and raise his salary to 25,000 DA.

#### Correction (AI-Generated)

```sql
-- 1. Table Creation
CREATE TABLE Client (
    clientNum VARCHAR(10) PRIMARY KEY,
    lastName VARCHAR(50),
    firstName VARCHAR(50),
    address VARCHAR(100),
    phoneNum VARCHAR(10) CHECK (phoneNum LIKE '06%' AND LENGTH(phoneNum) = 10),
    prefType VARCHAR(20) CHECK (prefType IN ('Apartment', 'House')),
    maxRent DECIMAL(10, 2)
);

CREATE TABLE Registration (
    clientNum VARCHAR(10),
    agencyNum VARCHAR(10),
    staffNum VARCHAR(10),
    registrationDate DATE CHECK (registrationDate > SYSDATE), -- As requested "postérieure"
    PRIMARY KEY (clientNum, agencyNum),
    FOREIGN KEY (clientNum) REFERENCES Client(clientNum),
    FOREIGN KEY (agencyNum) REFERENCES Agency(agencyNum),
    FOREIGN KEY (staffNum) REFERENCES Staff(staffNum)
);

-- 2. Staff: Salary 10k-30k, Manager/Supervisor, Even birth month
SELECT * FROM Staff
WHERE salary BETWEEN 10000 AND 30000
AND position IN ('Manager', 'Supervisor')
AND MOD(TO_NUMBER(TO_CHAR(birthDate, 'MM')), 2) = 0;

-- 3. Number of properties visited in May of last year
SELECT COUNT(DISTINCT propertyNum)
FROM Visit
WHERE TO_CHAR(visitDate, 'MM-YYYY') = '05-' || TO_CHAR(ADD_MONTHS(SYSDATE, -12), 'YYYY');

-- 4. Employees with salary > at least one employee of A003
SELECT * FROM Staff
WHERE salary > ANY (SELECT salary FROM Staff WHERE agencyNum = 'A003');

-- 5. Number of properties managed by each staff member
SELECT staffNum, COUNT(*) AS PropertyCount
FROM PropertyForRent
GROUP BY staffNum;

-- 6. Staff working in Boumerdes (2 solutions)
-- Sol 1: Join
SELECT S.* FROM Staff S, Agency A
WHERE S.agencyNum = A.agencyNum AND A.city = 'Boumerdes';
-- Sol 2: Subquery
SELECT * FROM Staff
WHERE agencyNum IN (SELECT agencyNum FROM Agency WHERE city = 'Boumerdes');

-- 7. View for A003 Manager
CREATE VIEW ViewStaffA003 AS
SELECT * FROM Staff WHERE agencyNum = 'A003';

-- 8. Grant Select on Agency
GRANT SELECT ON Agency TO PUBLIC;

-- 9. Promote Rabah ZHAR
UPDATE Staff
SET position = 'Manager', salary = 25000
WHERE staffNum = 'EM14';
```