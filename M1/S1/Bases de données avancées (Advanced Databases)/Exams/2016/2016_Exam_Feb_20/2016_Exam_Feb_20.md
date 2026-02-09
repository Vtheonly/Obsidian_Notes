
### 2016 Exam

**Year:** 2016
**Type:** Exam
**Correction:** Yes (Handwritten)

#### Exercise 1 (4 pts)

**Statement:**
1.  What is a table join? Describe the different types of joins seen in class.
2.  What is a transaction? Detail.
3.  What are the properties of a transaction? Explain.
4.  How to initialize and terminate a transaction in MySQL? Explain.

#### Exercise 2 (16 pts)

**Statement:**
Given the following relational schema describing accounts managed by several banks:
*   **BANK** (Bid, Bname, BinterestRate, BfeeRate)
*   **ACCOUNT** (Cid, Cnumber, Clabel, Cbalance, Bid)
*   **OPERATION** (Oid, Odate, Oamount, Osense, Rid, Cid)
*   **STATEMENT** (Rid, Rdate, Cid)

1.  **DDL:** Give in SQL the commands to create the tables **ACCOUNT** and **OPERATION** respecting the following management rules:
    a.  « Osense » represents the direction of the operation: either a *credit* ('C') or a *debit* ('D') of a certain amount on the account.
    b.  The date of the operation « Odate » is in the current month and prior to the current day.
    c.  There can be only one credit and one debit per day.
2.  **Queries:** Write the following queries in SQL:
    a.  Create a view describing per bank the total of *credits* and *debits* of each of its accounts over the last six months.
    b.  Give the user « Director » full access to this view, with the privilege to transmit the access to other users. Then, revoke the access of this user.
    c.  Give the names of the banks that have a global balance (Total credits - Total debits) negative over the last six months.
3.  In case the DBMS does not support constraint verification. Propose two solutions to remedy the reference constraint « ACCOUNT(Cid) -> BANK(Bid) ». Detail.
4.  Consider the constraint: « For an account, the total maximum amount of debits cannot exceed 20,000 DA per day and 100,000 DA per week (last 7 days). For credits, it cannot exceed 100,000 per day and 500,000 DA per week ». Program the trigger that guarantees the consistency of the base regarding this rule.
5.  Manage the consistency of the balance (Cbalance) of an account regarding credit or debit operations:
    a.  Write a procedure « update_balance (Cid, sense, amount) » which, depending on the sense of an operation on an account Cid, adds (if credit) or subtracts (if debit) the amount from the balance (Cbalance) of this account.
    b.  Program a trigger in case of an insertion of an operation (credit and debit).
    c.  Program a trigger in case of a modification of an operation.
6.  In order to manage bank interests, write a procedure using a cursor to:
    *   Credit *creditor accounts* (positive balance) with a sum calculated from the balance and the bank's interest rate.
    *   Debit *debtor accounts* (negative balance) with a sum calculated from the balance and the bank's fee rate.
    *   **Lock the modified rows!**

#### Correction (Based on Handwritten Notes)

```sql
-- 1. Create Tables
CREATE TABLE ACCOUNT (
    Cid int(5) PRIMARY KEY,
    Cnumber int(10) UNIQUE,
    Clabel varchar(10),
    Cbalance decimal(10, 2), -- Csolde
    Bid int(5) REFERENCES BANK(Bid)
);

CREATE TABLE OPERATION (
    Oid int(5) PRIMARY KEY,
    Odate date,
    Oamount decimal(10,2),
    Osense char(1) CHECK (Osense IN ('D', 'C')),
    Rid int(5) REFERENCES STATEMENT(Rid),
    Cid int(5) REFERENCES ACCOUNT(Cid),
    UNIQUE (Odate, Osense), -- One credit/debit per day rule (c)
    CHECK (MONTH(sysdate()) = MONTH(Odate) AND Odate < sysdate()) -- Rule (b)
);

-- 2a. Create View (Total credits and debits per bank/account last 6 months)
CREATE VIEW V_Banque AS
SELECT C.Bid, C.Cid, C.Cnumber, SUM(Oamount) as AmountTotal, Osense
FROM ACCOUNT C, OPERATION O
WHERE C.Cid = O.Cid
  AND Odate >= DATE_SUB(sysdate(), INTERVAL 6 MONTH)
GROUP BY C.Bid, C.Cid, Osense;

-- To separate Credit and Debit columns specifically:
CREATE VIEW V_Banque_CD AS 
SELECT V1.Bid, V1.Cid, V1.AmountTotal as TotalCredit, V2.AmountTotal as TotalDebit
FROM V_Banque V1, V_Banque V2
WHERE V1.Bid = V2.Bid AND V1.Cid = V2.Cid 
  AND V1.Osense = 'C' AND V2.Osense = 'D';

-- 2b. Grant/Revoke
GRANT ALL ON V_Banque_CD TO Directeur WITH GRANT OPTION;
REVOKE ALL ON V_Banque_CD FROM Directeur; -- (Logic note: usually revoke from public or specific user)

-- 2c. Banks with negative global balance (Credit - Debit < 0)
SELECT B.Bid, B.Bname
FROM BANK B, V_Banque_CD V
WHERE B.Bid = V.Bid
GROUP BY B.Bid, B.Bname
HAVING SUM(TotalCredit) - SUM(TotalDebit) < 0;

-- 4. Trigger for Debit/Credit limits
CREATE TABLE TRACE (Note varchar(80)); -- Error logging table
CREATE TRIGGER Tri_Q4 BEFORE INSERT ON OPERATION FOR EACH ROW
BEGIN
    DECLARE CJ DECIMAL(10,2) DEFAULT 0; -- Credit Day
    DECLARE CS DECIMAL(10,2) DEFAULT 0; -- Credit Week
    DECLARE DJ DECIMAL(10,2) DEFAULT 0; -- Debit Day
    DECLARE DS DECIMAL(10,2) DEFAULT 0; -- Debit Week

    IF new.Osense = 'C' THEN
        -- Calculate existing sums for Credits
        SELECT SUM(Oamount) INTO CJ FROM OPERATION WHERE Cid=new.Cid AND Odate=new.Odate AND Osense='C';
        SELECT SUM(Oamount) INTO CS FROM OPERATION WHERE Cid=new.Cid AND Odate >= DATE_SUB(sysdate(), INTERVAL 7 DAY) AND Osense='C';
        
        IF (CJ + new.Oamount > 100000) OR (CS + new.Oamount > 500000) THEN
            INSERT INTO TRACE VALUES ('Limit Exceeded');
            -- Signal SQLSTATE or force error
        END IF;
    ELSE -- Debit
        SELECT SUM(Oamount) INTO DJ FROM OPERATION WHERE Cid=new.Cid AND Odate=new.Odate AND Osense='D';
        SELECT SUM(Oamount) INTO DS FROM OPERATION WHERE Cid=new.Cid AND Odate >= DATE_SUB(sysdate(), INTERVAL 7 DAY) AND Osense='D';

        IF (DJ + new.Oamount > 20000) OR (DS + new.Oamount > 100000) THEN
             INSERT INTO TRACE VALUES ('Limit Exceeded');
        END IF;
    END IF;
END;

-- 5a. Procedure update_balance
DELIMITER $$
CREATE PROCEDURE maj_solde(IN pCid INT, IN pSens CHAR(1), IN pMontant DECIMAL)
BEGIN
    IF pSens = 'C' THEN
        UPDATE ACCOUNT SET Cbalance = Cbalance + pMontant WHERE Cid = pCid;
    ELSE
        UPDATE ACCOUNT SET Cbalance = Cbalance - pMontant WHERE Cid = pCid;
    END IF;
END $$
DELIMITER ;

-- 5b. Trigger on Insert
CREATE TRIGGER Tri_Ins_Op AFTER INSERT ON OPERATION FOR EACH ROW
BEGIN
    CALL maj_solde(new.Cid, new.Osense, new.Oamount);
END;

-- 5c. Trigger on Update
CREATE TRIGGER Tri_Upd_Op AFTER UPDATE ON OPERATION FOR EACH ROW
BEGIN
    -- Reverse old operation
    CALL maj_solde(old.Cid, old.Osense, -old.Oamount); -- Note: Logic simplifies to reversing impact
    -- Apply new operation
    CALL maj_solde(new.Cid, new.Osense, new.Oamount);
END;
```

---
