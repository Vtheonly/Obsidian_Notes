
### 2019 Exam

**Year:** 2019
**Type:** Exam
**Correction:** Yes (Handwritten)

#### Exercise 1 (8 pts)

**Statement:**
Given the following relational schema describing student enrollments in courses:
*   **Student** (matricule, name, firstname, birth_date, address, num_enrollments)
*   **Course** (course_code, name, description, hourly_volume, room, num_students)
*   **Enrollment** (matricule, course_code)

1.  In case the DBMS does not support foreign key verification. Propose two solutions to remedy the reference constraint « Enrollment(course_code) -> Course(course_code) ». Detail.
2.  Consider the constraint: « no more than 40 students can enroll in a course ». In case of an insertion into the **Enrollment** table, program the trigger that guarantees the consistency of the database regarding this constraint. This trigger must ensure consistency of the values of columns *num_enrollments* (Student) and *num_students* (Course) with the records of the Enrollment table.

#### Exercise 2 (12 pts)

**Statement:**
Given the following database schema:
*   **Trainee** (TraineeNum, Name, Firstname, BirthDate, EnrollDate, Address, Phone, TrackNum)
*   **Track** (TrackNum, TrackTitle, Capacity, NumYears)
*   **Grading** (GradingNum, TraineeNum, ModuleNum, Grade, Type, GradingDate)
*   **Module** (ModuleNum, ModuleTitle, HourlyVolume)

1.  **DDL:** Give in SQL the commands to create tables « **Trainee** » and « **Grading** » considering:
    a) « Type » is either 'ETCD' or 'ETLD'.
    b) A trainee cannot have more than one grade per type for a given module.
    c) ETCD grade is between 0 and 15, ETLD grade is between 0 and 20.
    d) Grading dates are later than the trainee's enrollment date.
2.  Display for each track the number of trainees enrolled.
3.  Query giving numbers and titles of modules where the average of ETLD grades of all trainees is less than 10/20 over the last six months.
4.  Knowing there cannot be more than two evaluations per module for a student, display on one line the name and firstname of students with their ETCD and ETLD grades.
5.  Write a stored procedure using a cursor to:
    a) Add 2 points to the ETLD grade of module number 10 (BDA) for trainees in track 01 (Computer Science) if the grade is < 10.
    b) Add 0.5 points to the ETLD grade of module number 10 (BDA) for trainees in track 01 if the grade is >= 10.
    **Lock the modified rows!**

#### Correction (Based on Handwritten Notes)

```sql
-- Exercise 1

-- 1. Solution using Views (Check Option) or Triggers
-- View Solution:
CREATE VIEW V_Enrollment AS
SELECT * FROM Enrollment
WHERE course_code IN (SELECT course_code FROM Course)
WITH CHECK OPTION;
-- Trigger Solution:
CREATE TRIGGER Tri_Ins_Enrollment BEFORE INSERT ON Enrollment FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT * FROM Course WHERE course_code = new.course_code) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Foreign Key Violation';
    END IF;
END;

-- 2. Trigger for constraint (Max 40 students & Update counters)
CREATE TRIGGER Tri_Ins_Enrollment_Count BEFORE INSERT ON Enrollment FOR EACH ROW
BEGIN
    DECLARE v_count INT;
    SELECT num_students INTO v_count FROM Course WHERE course_code = new.course_code;
    
    IF (v_count >= 40) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course full';
    ELSE
        -- Update Student counter
        UPDATE Student SET num_enrollments = num_enrollments + 1 WHERE matricule = new.matricule;
        -- Update Course counter
        UPDATE Course SET num_students = num_students + 1 WHERE course_code = new.course_code;
    END IF;
END;

-- Exercise 2

-- 1. Create Tables
CREATE TABLE Trainee (
    TraineeNum INT PRIMARY KEY,
    Name VARCHAR(30),
    Firstname VARCHAR(30),
    EnrollDate DATE,
    TrackNum INT REFERENCES Track(TrackNum)
);

CREATE TABLE Grading (
    GradingNum INT PRIMARY KEY,
    TraineeNum INT NOT NULL,
    ModuleNum INT NOT NULL,
    Grade DECIMAL(4,2),
    Type CHAR(4) CHECK (Type IN ('ETCD', 'ETLD')),
    GradingDate DATE,
    UNIQUE(TraineeNum, ModuleNum, Type), -- Rule (b)
    CHECK ((Type='ETCD' AND Grade BETWEEN 0 AND 15) OR (Type='ETLD' AND Grade BETWEEN 0 AND 20)) -- Rule (c)
);
-- Rule (d) requires a Trigger because it compares with another table (Trainee)
CREATE TRIGGER Tri_Check_Date BEFORE INSERT ON Grading FOR EACH ROW
BEGIN
    DECLARE v_enrollDate DATE;
    SELECT EnrollDate INTO v_enrollDate FROM Trainee WHERE TraineeNum = new.TraineeNum;
    IF (new.GradingDate <= v_enrollDate) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid Date';
    END IF;
END;

-- 2. Number of trainees per track
SELECT TrackNum, COUNT(*) as CountTrainees
FROM Trainee
GROUP BY TrackNum;

-- 3. Modules with ETLD avg < 10 in last 6 months
SELECT M.ModuleNum, M.ModuleTitle, AVG(G.Grade)
FROM Module M, Grading G
WHERE M.ModuleNum = G.ModuleNum
  AND G.Type = 'ETLD'
  AND G.GradingDate >= ADD_MONTHS(SYSDATE, -6)
GROUP BY M.ModuleNum, M.ModuleTitle
HAVING AVG(G.Grade) < 10;

-- 4. Pivot/Display on one line
SELECT S.TraineeNum, S.Name, S.Firstname, 
       G1.Grade as ETCD, G2.Grade as ETLD
FROM Trainee S, Grading G1, Grading G2
WHERE S.TraineeNum = G1.TraineeNum AND S.TraineeNum = G2.TraineeNum
  AND G1.ModuleNum = G2.ModuleNum
  AND G1.Type = 'ETCD'
  AND G2.Type = 'ETLD';

-- 5. Procedure with Cursor
DELIMITER $$
CREATE PROCEDURE exo2_questions()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_gradingNum INT;
    DECLARE v_grade DECIMAL(4,2);
    
    -- Cursor for ETLD grades of Module 10, Track 01
    DECLARE curs CURSOR FOR 
        SELECT G.GradingNum, G.Grade
        FROM Grading G, Trainee T
        WHERE G.TraineeNum = T.TraineeNum
          AND T.TrackNum = 01
          AND G.ModuleNum = 10
          AND G.Type = 'ETLD'
        FOR UPDATE; -- Lock rows
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN curs;
    read_loop: LOOP
        FETCH curs INTO v_gradingNum, v_grade;
        IF done THEN LEAVE read_loop; END IF;
        
        IF v_grade < 10 THEN
            UPDATE Grading SET Grade = Grade + 2 WHERE CURRENT OF curs;
        ELSE
            UPDATE Grading SET Grade = Grade + 0.5 WHERE CURRENT OF curs;
        END IF;
    END LOOP;
    CLOSE curs;
END $$
DELIMITER ;
```