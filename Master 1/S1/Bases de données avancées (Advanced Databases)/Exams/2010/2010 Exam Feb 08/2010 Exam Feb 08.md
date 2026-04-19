
### 2010 Exam (February)

**Year:** 2010
**Type:** Exam
**Correction:** No (AI-Generated Solution Provided)

#### Exercise 1 (8 pts)

**Statement:**
1.  What is a view? Explain the difference between a view and a base table.
2.  Describe the difference between candidate keys and the primary key of a relation. Explain what a foreign key means. What correspondence is there between foreign keys of relations and candidate keys? Give examples illustrating your answer.
3.  What is a table index?
4.  What is a table join? And describe the different types of joins seen in class.

#### Exercise 2 (12 pts)

**Statement:**
Given the following relational schema describing a hotel network:

*   **Hotel** (hotelNum, hotelName, city)
*   **Room** (roomNum, hotelNum, type, price)
*   **Reservation** (hotelNum, clientNum, startDate, endDate, roomNum)
*   **Client** (clientNum, clientName, clientAddress)

**Work to be done:**

**I/ (4 pts):**
Give in SQL the commands to create these tables specifying the data type of each column as well as the integrity constraints ensuring the consistency of data. Among the constraints, one can find:
a) The value of type is either 'Single', 'Double', or 'Family'.
b) The price is between 1000 and 10000 DA.
c) The roomNum is between 1 and 100.
d) The startDate and endDate are greater than the current date.

**II/ Queries (8 pts):**
Program the following queries in SQL:
1.  Create a view containing the name of the hotel and the names of clients residing in this hotel.
2.  Create a view containing the bill (the invoice amount) for each client of the hotel "Aurassi".
3.  Give users "Manager" and "Director" full access to these views, with the privilege to pass the access to other users.
4.  Give the user "Accountant" SELECT access to these views. Then, revoke the access from this user.
5.  What is the average price of a room?
6.  What is the loss of revenue for each hotel, at the current date, due to unoccupied rooms?
7.  Clients having a reservation in a hotel where 'BOUZIAD' (with client number 1) has a reservation. Use a self-join.
8.  Give the name of hotels that booked at least one 'Family' room last month.

#### Correction (AI-Generated)

```sql
-- I/ Table Creation
CREATE TABLE Hotel (
    hotelNum INT PRIMARY KEY,
    hotelName VARCHAR(50),
    city VARCHAR(50)
);

CREATE TABLE Client (
    clientNum INT PRIMARY KEY,
    clientName VARCHAR(50),
    clientAddress VARCHAR(100)
);

CREATE TABLE Room (
    roomNum INT,
    hotelNum INT,
    type VARCHAR(10) CHECK (type IN ('Single', 'Double', 'Family')),
    price DECIMAL(10, 2) CHECK (price BETWEEN 1000 AND 10000),
    PRIMARY KEY (roomNum, hotelNum),
    FOREIGN KEY (hotelNum) REFERENCES Hotel(hotelNum),
    CONSTRAINT chk_roomNum CHECK (roomNum BETWEEN 1 AND 100)
);

CREATE TABLE Reservation (
    hotelNum INT,
    clientNum INT,
    startDate DATE,
    endDate DATE,
    roomNum INT,
    PRIMARY KEY (hotelNum, clientNum, startDate),
    FOREIGN KEY (hotelNum, roomNum) REFERENCES Room(hotelNum, roomNum),
    FOREIGN KEY (clientNum) REFERENCES Client(clientNum),
    CONSTRAINT chk_dates CHECK (startDate > SYSDATE AND endDate > SYSDATE)
);

-- II/ SQL Queries

-- 1. View: Hotel name and Client names residing there
CREATE VIEW HotelResidents AS
SELECT H.hotelName, C.clientName
FROM Hotel H, Client C, Reservation R
WHERE H.hotelNum = R.hotelNum AND C.clientNum = R.clientNum;

-- 2. View: Bill for each client of "Aurassi"
-- Assuming Bill = (EndDate - StartDate) * RoomPrice
CREATE VIEW AurassiBills AS
SELECT C.clientName, (R.endDate - R.startDate) * Rm.price AS BillAmount
FROM Client C, Reservation R, Room Rm, Hotel H
WHERE C.clientNum = R.clientNum
AND R.roomNum = Rm.roomNum AND R.hotelNum = Rm.hotelNum
AND Rm.hotelNum = H.hotelNum
AND H.hotelName = 'Aurassi';

-- 3. Grant access to Manager and Director with Grant Option
GRANT ALL PRIVILEGES ON HotelResidents TO Manager, Director WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON AurassiBills TO Manager, Director WITH GRANT OPTION;

-- 4. Grant and Revoke SELECT for Accountant
GRANT SELECT ON HotelResidents TO Accountant;
GRANT SELECT ON AurassiBills TO Accountant;

REVOKE SELECT ON HotelResidents FROM Accountant;
REVOKE SELECT ON AurassiBills FROM Accountant;

-- 5. Average price of a room
SELECT AVG(price) FROM Room;

-- 6. Loss of revenue for each hotel (unoccupied rooms today)
-- Logic: Sum of prices of rooms NOT in the list of reserved rooms for today
SELECT H.hotelName, SUM(Rm.price) AS RevenueLoss
FROM Hotel H, Room Rm
WHERE H.hotelNum = Rm.hotelNum
AND (Rm.roomNum, Rm.hotelNum) NOT IN (
    SELECT roomNum, hotelNum 
    FROM Reservation 
    WHERE SYSDATE BETWEEN startDate AND endDate
)
GROUP BY H.hotelName;

-- 7. Clients having a reservation in a hotel where 'BOUZIAD' (client 1) has a reservation (Self-Join)
SELECT DISTINCT C.clientName
FROM Client C, Reservation R1, Reservation R2
WHERE C.clientNum = R1.clientNum
AND R1.hotelNum = R2.hotelNum
AND R2.clientNum = 1
AND C.clientNum <> 1;

-- 8. Hotels that booked at least one 'Family' room last month
SELECT DISTINCT H.hotelName
FROM Hotel H, Reservation R, Room Rm
WHERE H.hotelNum = R.hotelNum
AND R.roomNum = Rm.roomNum AND R.hotelNum = Rm.hotelNum
AND Rm.type = 'Family'
AND R.startDate BETWEEN ADD_MONTHS(SYSDATE, -1) AND SYSDATE;
```

---
