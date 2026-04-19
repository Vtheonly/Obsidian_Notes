Here are the next 3 exams (2012 Exam, 2016 Exam, and 2019 Exam) based on your file list structure.

---

### 2012 Exam

**Year:** 2012
**Type:** Exam
**Correction:** Yes

#### Exercise 1 (6 pts)

**Statement:**
1.  What is a view? Explain the difference between a view and a base table.
2.  Describe the difference between candidate keys and the primary key of a relation. Explain what a foreign key means.
3.  What is a table join? Describe the different types of joins seen in class.
4.  What is a transaction? Detail.
5.  What are the properties of a transaction? Explain.
6.  How to initialize and terminate a transaction in MySQL? Explain.
7.  What is a table index?

#### Exercise 2 (6 pts)

**Statement:**
Given the following relational schema describing a hotel network:
*   **Hotel** (hotelNum, hotelName, city)
*   **Room** (roomNum, hotelNum, type, price)
*   **Reservation** (hotelNum, clientNum, startDate, endDate, roomNum)
*   **Client** (clientNum, clientName, clientAddress)

1.  **DDL:** Give in SQL the commands to create the tables **Room** and **Reservation** taking into account the following management rules:
    a) The value of *type* is either 'Single', 'Double' or 'Family'.
    b) *startDate* and *endDate* are greater than the current date. Furthermore, *endDate* is greater than *startDate*.
    c) A client cannot reserve a hotel if they have a reservation that has not ended yet.
2.  **Queries:** Write the following queries in SQL:
    a) Create a view containing the bill (the invoice amount) for each client of the hotel "Aurassi" for the current year.
    b) Give users "Manager" and "Director" full access to this view, with the privilege to pass the access to other users. Then, revoke the access from this user (public).
    c) Give the name of hotels that booked at least one 'Family' room in the last 3 months.

#### Exercise 3 (8 pts)

**Statement:**
Given the following relational schema describing student enrollments in courses:
*   **Student** (matricule, name, firstname, birth_date, address, num_enrollments)
*   **Course** (course_code, name, description, hourly_volume, room)
*   **Enrollment** (matricule, course_code)

1.  In case the DBMS does not support foreign key verification. Propose two solutions to remedy the reference constraint « Enrollment(matricule) -> Student(matricule) ». Detail.
2.  Consider the constraint that « a student cannot be enrolled in more than five (5) courses ». Here, it is about ensuring consistency between the value of the column *num_enrollments* of the Student table and the records of the Enrollment table in case of an insertion like: `INSERT INTO Enrollment VALUES ('M010001','C1')`. Program the trigger that guarantees the consistency of the database regarding this rule.
3.  Write a procedure using a cursor to:
    *   Increase the hourly volume by 10 hours for courses in room 'S10' whose hourly volume is less than 50 hours.
    *   Increase the hourly volume by 8 hours for courses in room 'S10' whose hourly volume is greater than 50 hours.
    *   Delete courses whose hourly volume is less than 8 hours.

#### Correction

```sql
-- Exercise 2

-- 1. Create Tables
CREATE TABLE Reservation (
    numHotel varchar(7), 
    numClient varchar(7),
    dateDebut date, 
    dateFin date, 
    numChambre varchar(7),
    CONSTRAINT pk_reser PRIMARY KEY (numHotel, numClient, dateDebut),
    CONSTRAINT dat_d CHECK (dateDebut >= ADDDATE(SYSDATE(), 1)),
    CONSTRAINT dat_f CHECK (dateFin >= ADDDATE(SYSDATE(), 1))
    -- Note: Additional check dateFin > dateDebut is implied or added similarly
);

-- Trigger for rule (c): A client cannot reserve if they have an active reservation
CREATE TRIGGER trig BEFORE INSERT ON Reservation FOR EACH ROW
BEGIN
    DECLARE v_date DATE; 
    SELECT dateFin INTO v_date
    FROM Reservation
    WHERE new.numClient = numClient 
      AND new.numHotel = numHotel;
      
    IF (new.dateDebut <= v_date) THEN
        -- Force an error or handle logic
        INSERT INTO Tracer Values (null); -- This will fail if Tracer doesn't exist/accept nulls, stopping the insert
    END IF;
END;

-- 2a. Create View for Bill (Hotel 'Aurassi', current year)
-- Assuming Bill = Days * Price. 
-- Note: Logic uses PERIOD_DIFF to check for "current year" or recent entries (<= 12 months)
CREATE VIEW NOTE AS 
SELECT DATEDIFF(R.dateFin, R.dateDebut) * CH.prix AS La_Note, C.numClient
FROM Reservation R, Room CH, Client C, Hotel H
WHERE R.numChambre = CH.numChambre 
  AND R.numHotel = CH.numHotel -- Join condition for room/hotel
  AND C.numClient = R.numClient
  AND H.numHotel = R.numHotel
  AND H.nomHotel = 'Aurassi'
  AND PERIOD_DIFF(DATE_FORMAT(R.dateDebut, '%Y%m'), DATE_FORMAT(SYSDATE(), '%Y%m')) <= 12;

-- 2b. Grant/Revoke
GRANT ALL ON NOTE TO Directeur, Gérant WITH GRANT OPTION;
REVOKE ALL ON NOTE FROM PUBLIC;

-- 2c. Hotels with 'Family' room reserved in last 3 months
SELECT H.numHotel, H.nomHotel
FROM Hotel H, Reservation R, Room CH
WHERE R.numHotel = H.numHotel 
  AND CH.numChambre = R.numChambre
  AND CH.numHotel = R.numHotel
  AND CH.type = 'Family'
  AND PERIOD_DIFF(DATE_FORMAT(SYSDATE(), '%Y%m'), DATE_FORMAT(R.dateDebut, '%Y%m')) <= 3;
```

---
