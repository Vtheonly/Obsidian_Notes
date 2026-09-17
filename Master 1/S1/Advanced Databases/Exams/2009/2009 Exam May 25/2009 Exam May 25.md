

### 2009 Exam (May)

**Year:** 2009
**Type:** Exam (BDA2 - Optimization)
**Correction:** No (AI-Generated Solution Provided)

#### Exercise 1 (7 pts)

**Statement:**
In the design phase of an application, we do not have data with real volumes because the application is not yet realized.
Given the following database schema:

*   **CLIENT** (CLI_NumCli, CLI_NameCli, CLI_AdrCli, CLI_Country)
*   **ARTICLE** (ART_NumArt, ART_Designation, ART_Price)
*   **STOCK** (ART_NumArt, STK_WarehouseName, STK_QtyStock)
*   **ORDER** (ORD_NumOrd, ORD_DateOrd, CLI_NumCli)
*   **ORDER_LINE** (ORD_NumOrd, ART_NumArt, LIN_QtyOrd)

And given the following query:
```sql
SELECT CLI.CLI_NumCli
FROM CLIENT CLI, ARTICLE ART, ORDER ORD, ORDER_LINE LIN
WHERE CLI.CLI_NumCli = ORD.CLI_NumCli
AND ORD.ORD_NumOrd = LIN.ORD_NumOrd
AND LIN.ART_NumArt = ART.ART_NumArt
AND ART.ART_Designation = 'Table'
```
We want to know if this query can be executed within the time limits required by users.

**Question:** Propose the steps of the general approach to follow for the optimization of an application in the design phase and illustrate with examples based on the schema and the query above.

#### Exercise 2 (14 pts)

**Statement:**
Given the relational schema of the mission management domain in a company:

*   **EMPLOYEE** (EMP_Num, EMP_Title, EMP_Name, EMP_Salary, SRV_Num, EMP_Manager)
*   **SERVICE** (SRV_Num, SRV_Label)
*   **MISSION** (MIS_Num, VEH_Num, EMP_Num, MIS_DepDay, MIS_DepKm, MIS_RetDay, MIS_RetKm)
*   **VEHICLE** (VEH_Num, VEH_Plate, COL_Code, VEH_BuyDate, VEH_BuyPrice, TYP_Num)
*   **TYPE** (TYP_Num, TYP_Name, TYP_Power, TYP_Weight, TYP_Consumption, BRD_Num)
*   **BRAND** (BRD_Num, BRD_Name)
*   **COLOR** (COL_Code, COL_Label)

**With the following management rules:**
1.  Bold columns are declared "Primary Keys".
2.  The column "MIS_RetDay" is very often modified.
3.  The insertion operation is much more frequent than queries in the SERVICE table.
4.  The Color of a vehicle is either black or white.
5.  The tables MISSION, EMPLOYEE, VEHICLE, and SERVICE contain respectively 500,000, 10,000, 500, and 20 rows.

**And given the following extract of used queries:**
1.  `SELECT * FROM MISSION ORDER BY MIS_DepDay;`
2.  `SELECT * FROM MISSION ORDER BY MIS_RetDay;`
3.  `SELECT * FROM BRAND WHERE BRD_NAME = "MMMM";`
4.  `SELECT * FROM SERVICE WHERE SRV_Label like "SRV%";`
5.  `SELECT * FROM EMPLOYEE E, MISSION M WHERE E.EMP_Num = M.EMP_Num and EMP_Num = 1100;`
6.  `SELECT E.* FROM EMPLOYEE E, SERVICE S WHERE E.SRV_Num = S.SRV_Num and SRV_Label ='Operations';`
7.  `SELECT E.* FROM SERVICE S, EMPLOYEE E, VEHICLE V, MISSION M ...` (Complex join with substring and date comparison).

**Work to be done:**

1.  Give the SQL query allowing to create an index on the column "EMPLOYEE.SRV_Num". And give a B-Tree structure containing the 15 indexed values (of SRV_Num) following: 1001, 1002, 1003, ..., 1015. We assume a leaf block contains 3 values maximum, other blocks 5 elements maximum.
2.  Declare in SQL the indexes necessary for the optimization of queries on this DB.
3.  What do the update operations INSERT, DELETE, and UPDATE cause on the indexes? Compare the three impacts.
4.  What does a massive entry cause in an indexed table? What should be done to remedy possible problems? And what can be gained?
5.  Query (5) lists the missions of employee 1100. What can be done to accelerate this query? Give the corresponding SQL commands and illustrate with a schema.
6.  The join of query (6) turns out to be very expensive! Propose a solution to remedy it and give the SQL orders necessary for its implementation.
7.  Optimize query (7).
8.  Explain the two access methods to a table under ORACLE.

#### Correction (AI-Generated)

> **Note:** This exam focuses on physical database optimization.

**Exercise 1:**
The approach generally involves:
1.  **Logical Optimization (Algebraic):** Push selections down. In the example, apply `ART_Designation = 'Table'` first before joining with `ORDER_LINE`.
2.  **Physical Optimization (Indexing):** Check if access paths exist. Create indexes on join keys (`CLI_NumCli`, `ORD_NumOrd`, `ART_NumArt`) and the selection predicate (`ART_Designation`).
3.  **Volume Estimation:** Calculate the cardinality of intermediate results based on statistics (e.g., selectivity of 'Table').
4.  **Cost Model:** Estimate disk I/O and CPU cost for different execution plans (Nested Loops vs Hash Join) to ensure the query meets delay requirements.

**Exercise 2:**

**1. Index Creation and B-Tree:**
```sql
CREATE INDEX idx_emp_srv ON EMPLOYEE(SRV_Num);
```
**B-Tree Structure (Values 1001 to 1015):**
*Constraints:* Leaf max = 3, Internal max = 5.
Total values = 15.
Number of leaves = 15 / 3 = 5 leaves.
Leaf 1: [1001, 1002, 1003]
Leaf 2: [1004, 1005, 1006]
Leaf 3: [1007, 1008, 1009]
Leaf 4: [1010, 1011, 1012]
Leaf 5: [1013, 1014, 1015]

Root Node (Internal) needs to index these 5 leaves. It will contain separators (smallest values of the sub-trees, usually starting from the 2nd leaf).
Root: [1004, 1007, 1010, 1013] (4 keys < 5 max capacity).
Structure: Root points to the 5 leaves.

**2. Necessary Indexes:**
Based on the queries and row counts:
*   Q1: `CREATE INDEX idx_mis_dep ON MISSION(MIS_DepDay);`
*   Q2: `MIS_RetDay` is frequently modified (Rule 2), avoid index if possible, or accept overhead. However, Q2 orders by it. Given the volume (500,000), a sort is expensive. An index helps reading, but hurts updates.
*   Q3: `CREATE INDEX idx_brd_name ON BRAND(BRD_Name);`
*   Q4: `SRV_Label` is used with `LIKE 'SRV%'`. Standard index works for prefix search. `CREATE INDEX idx_srv_label ON SERVICE(SRV_Label);`
*   Q5: `EMP_Num` is likely Primary Key (Auto-indexed). FK in Mission: `CREATE INDEX idx_mis_emp ON MISSION(EMP_Num);`
*   Q6: Join on `SRV_Num`. `CREATE INDEX idx_emp_srv ON EMPLOYEE(SRV_Num);`
*   Q7: Complex. Indexes on Join keys (`VEH_Num`, etc.).

**3. Impact of Updates:**
*   **INSERT:** Requires inserting the key into the B-Tree. May cause node splitting if a block is full (expensive).
*   **DELETE:** Requires removing the key. May cause node merging if a block is underutilized (expensive).
*   **UPDATE:** Logically a Delete followed by an Insert. If the indexed column is modified (like `MIS_RetDay`), the entry moves in the tree. If non-indexed columns change, no impact on the index.

**4. Massive Entry:**
Causes frequent node splitting and fragmentation (blocks only partially full). The tree becomes unbalanced or deeper than necessary.
*Remedy:* Drop index before massive insert, recreate it afterwards. Or reorganize/rebuild index.
*Gain:* Faster insertion speed (no index overhead per row), compact and balanced index upon recreation.

**5. Optimizing Query 5 (Employee 1100 Missions):**
The query selects from EMPLOYEE and MISSION for a specific Employee.
*Optimization:* **Cluster** (Clustered Table). Store the EMPLOYEE record and their associated MISSION records physically close on the disk.
```sql
CREATE CLUSTER Emp_Miss_Cluster (emp_no NUMBER);
CREATE INDEX idx_cluster ON CLUSTER Emp_Miss_Cluster;
CREATE TABLE EMPLOYEE ... CLUSTER Emp_Miss_Cluster(EMP_Num);
CREATE TABLE MISSION ... CLUSTER Emp_Miss_Cluster(EMP_Num);
```

**6. Optimizing Query 6:**
Query 6 joins EMPLOYEE (10k rows) and SERVICE (20 rows).
If the join is expensive, we can **Denormalize**.
Add `SRV_Label` directly into the `EMPLOYEE` table.
```sql
ALTER TABLE EMPLOYEE ADD (SRV_Label VARCHAR(50));
UPDATE EMPLOYEE E SET SRV_Label = (SELECT SRV_Label FROM SERVICE S WHERE S.SRV_Num = E.SRV_Num);
-- New Query:
SELECT * FROM EMPLOYEE WHERE SRV_Label = 'Operations';
```

**7. Optimizing Query 7:**
Avoid functions on indexed columns in the WHERE clause.
`TO_CHAR(MIS_DepDay, ...)` prevents index usage.
Rewrite:
`AND MIS_DepDay > TO_DATE('01/01/2009', 'DD/MM/YYYY')`

**8. Access Methods in Oracle:**
1.  **Full Table Scan:** Reads all blocks of the table. Used when a large portion of the table is accessed or no index exists.
2.  **Index Scan (Range/Unique):** Traverses the B-Tree to find RowIDs, then accesses specific blocks. Used for high selectivity queries.