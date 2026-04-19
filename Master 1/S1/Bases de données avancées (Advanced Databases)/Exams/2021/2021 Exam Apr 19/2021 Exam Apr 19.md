
### 2021 Exam

**Year:** 2021
**Type:** Exam
**Correction:** Yes

#### Exercise 1 (4 pts)

**Statement:**
1.  What is a view? Explain the difference between a view and a base table.
2.  What is a table join?
3.  Describe the different types of joins seen in class.

#### Exercise 2 (16 pts)

**Statement:**
Given the following relational schema describing a hotel network:
*   **Hotel** (hotelNum, hotelName, city, numberGuestsPresent)
*   **Room** (roomNum, hotelNum, type, price)
*   **Reservation** (hotelNum, clientNum, startDate, endDate, roomNum)
*   **Client** (clientNum, clientName, clientAddress)

**Work to be done:**

**I/ Table Creation (6 pts):**
Give in SQL the commands to create tables **Room** and **Reservation**, specifying types and integrity constraints.
a) *type* value is 'Single', 'Double', or 'Family'.
b) *price* is between 1000 and 10000 DA.
c) *roomNum* is between 1 and 100.
d) *startDate* and *endDate* are greater than the current date.

**II/ Queries (10 pts):**
1.  What is the average price of a room?
2.  Give the clients who have a reservation in the same hotel where the client 'TOTO' resides. Knowing 'TOTO' has clientNum 1. Use a self-join.
3.  Create a view **VQ3** containing the hotel name and the names of clients residing there.
4.  Give users « Manager » and « Director » full access to view **VQ3**, with privilege to transmit access.
5.  Give user « Accountant » SELECT access to **VQ3**.
6.  Give the invoice amount for each client of hotel « Aurassi ».
7.  If the DBMS does not support reference constraints, propose two solutions to remedy the constraint `Room(hotelNum) -> Hotel(hotelNum)` (One using Triggers, one using Views).

#### Correction

```sql
-- I/ Creation
CREATE TABLE Room (
    roomNum int(5),
    hotelNum int(5),
    type varchar(10) NOT NULL,
    price numeric(10,2) NOT NULL,
    PRIMARY KEY (roomNum, hotelNum),
    FOREIGN KEY (hotelNum) REFERENCES Hotel(hotelNum),
    CHECK (type IN ('Single', 'Double', 'Family')),
    CHECK (price BETWEEN 1000 AND 10000),
    CHECK (roomNum BETWEEN 1 AND 100)
);

CREATE TABLE Reservation (
    hotelNum int(5),
    clientNum int(5),
    startDate date,
    endDate date NOT NULL,
    roomNum int(5) NOT NULL,
    PRIMARY KEY (hotelNum, clientNum, startDate),
    FOREIGN KEY (hotelNum, roomNum) REFERENCES Room(hotelNum, roomNum),
    FOREIGN KEY (clientNum) REFERENCES Client(clientNum),
    CHECK (startDate > sysdate()),
    CHECK (endDate > sysdate())
);

-- II/ Queries
-- 1. Average Price
SELECT AVG(price) FROM Room;

-- 2. Clients in same hotel as TOTO (num 1)
SELECT DISTINCT R2.clientNum
FROM Reservation R1, Reservation R2
WHERE R1.clientNum = 1
  AND R1.hotelNum = R2.hotelNum;

-- 3. View VQ3
CREATE VIEW VQ3 AS
SELECT H.hotelName, C.clientName
FROM Hotel H, Client C, Reservation R
WHERE R.hotelNum = H.hotelNum
  AND R.clientNum = C.clientNum;

-- 4. Grant Manager/Director
GRANT ALL PRIVILEGES ON VQ3 TO Manager, Director WITH GRANT OPTION;

-- 5. Grant Accountant
GRANT SELECT ON VQ3 TO Accountant;
-- (Correction mentions revoking afterwards based on standard exam patterns, but prompt asked to give)
-- REVOKE ALL PRIVILEGES ON VQ3 FROM Accountant;

-- 6. Invoice Amount for 'Aurassi'
SELECT R.clientNum, DATEDIFF(R.endDate, R.startDate) * C.price AS Invoice
FROM Reservation R, Hotel H, Room C
WHERE R.hotelNum = H.hotelNum
  AND H.hotelName = 'Aurassi'
  AND R.hotelNum = C.hotelNum 
  AND R.roomNum = C.roomNum;

-- 7. Remedy for Reference Constraint Room -> Hotel
-- Case A: Views (Check Option)
-- Insertion in Room:
CREATE VIEW V_Room AS
SELECT * FROM Room
WHERE hotelNum IN (SELECT hotelNum FROM Hotel)
WITH CHECK OPTION;

-- Case B: Triggers
-- Insertion in Room:
CREATE TRIGGER Tri_Ins_Room BEFORE INSERT ON Room FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT * FROM Hotel WHERE hotelNum = new.hotelNum) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FK Error';
    END IF;
END;

-- Deletion in Hotel:
CREATE TRIGGER Tri_Del_Hotel BEFORE DELETE ON Hotel FOR EACH ROW
BEGIN
    IF EXISTS (SELECT * FROM Room WHERE hotelNum = old.hotelNum) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FK Error';
    END IF;
END;
```

---
