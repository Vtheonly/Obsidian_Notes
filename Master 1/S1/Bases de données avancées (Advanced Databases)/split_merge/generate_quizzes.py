#!/usr/bin/env python3
"""
Quiz File Generator
Generates 2 quiz files per chapter with exactly:
- 10 True/False questions
- 10 Multiple Choice questions  
- 10 Matching questions

Total: 6 chapters × 2 files × 30 questions = 360 questions
"""

import os

QUIZ_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Quiz')

CHAPTERS = [
    {
        'num': 'Chapter_01',
        'sources': [
            '[[1. Relational Model Fundamentals]]',
            '[[2. Relational Algebra Operators]]',
            '[[3. Advanced Relational Algebra Functions]]',
            '[[1. Relational Algebra - The Join Family]]',
            '[[2. SQL Inner Join Deep Dive]]',
            '[[3. SQL Outer Joins Explained]]',
            '[[01 Views]]',
            '[[01 Database Classifications Architectures]]',
            '[[02 DBMS Architecture and Models]]',
        ]
    },
    {
        'num': 'Chapter_02',
        'sources': [
            '[[01 Static Constraints]]',
            '[[02 Foreign Key Behaviors]]',
            '[[03 Dynamic Constraints Triggers]]',
            '[[04 Advanced Triggers]]',
            '[[05 Triggers and Events]]',
            '[[06 Assertions and Deferrable Constraints]]',
            '[[07 Altering Constraints and Operational Behavior]]',
            '[[08 Trigger Execution and Automation Scenarios]]',
            '[[09 Metadata and the Information Schema]]',
        ]
    },
    {
        'num': 'Chapter_03',
        'sources': [
            '[[01 ACID Properties]]',
            '[[02 Concurrency Control and Isolation]]',
            '[[03 Crash Recovery Mechanisms]]',
            '[[05 Transactions and Crash Recovery]]',
            '[[06 Master Class Transactions & Integrity]]',
            '[[07 Advanced Concurrency Protocols]]',
            '[[08 Concurrency Anomalies Deep Dive]]',
            '[[09 Disaster Recovery Protocols]]',
        ]
    },
    {
        'num': 'Chapter_04',
        'sources': [
            '[[1. Query Processing Architecture]]',
            '[[2. Relational Algebra & Logical Plans]]',
            '[[3. Physical Operators & Algorithms]]',
            '[[4. Advanced Physical Design]]',
            '[[5. Cost Estimation & Calculations]]',
            '[[8. Database Indexing Deep Dive]]',
            '[[11. Algebraic Rewrite Rules and Heuristics]]',
            '[[12. Physical Access Paths and Join Costs]]',
            '[[15. Database Statistics and Selectivity Estimation]]',
        ]
    },
    {
        'num': 'Chapter_05',
        'sources': [
            '[[01 PLSQL Basics]]',
            '[[02 Functions and Stored Procedures]]',
            '[[03 Stored Procedures and Functions]]',
            '[[04 Exception Handling and Debugging]]',
            '[[05 Advanced Cursors and Dynamic SQL]]',
            '[[06 Procedural Control Structures and Handlers]]',
            '[[07 Delimiters and Procedural Parsing Mechanics]]',
        ]
    },
    {
        'num': 'Chapter_06',
        'sources': [
            '[[Source TD N1 BDA Rappel SQL]]',
            '[[Source TD N2 BDA Gestion des Ventes]]',
            '[[Source TD N3 BDA Contraintes d\'intégrité, Vue et Contrôle de données]]',
            '[[Source TD N4 - Optimisation de requêtes]]',
            '[[Source TD N4 MySQL Procédural (The Airline Database).]]',
            '[[Source TD N5 - Transactions, Concurrence et Récupération]]',
        ]
    },
]

# Each chapter has 2 files with specific quiz content
QUIZ_CONTENT = {}

# ============================================================
# CHAPTER 01 - QUIZ 1
# ============================================================
QUIZ_CONTENT['Chapter_01_1'] = """---
sources:
  - "[[1. Relational Model Fundamentals]]"
  - "[[2. Relational Algebra Operators]]"
  - "[[3. Advanced Relational Algebra Functions]]"
  - "[[1. Relational Algebra - The Join Family]]"
---

> [!question] A relation in the relational model is an unordered set of tuples.
>> [!success]- Answer
>> True

> [!question] The natural join automatically removes duplicate columns with the same name.
>> [!success]- Answer
>> True

> [!question] The division operator in relational algebra requires that the divisor's attributes be a subset of the dividend's attributes.
>> [!success]- Answer
>> True

> [!question] A theta-join can only use the equality operator (=).
>> [!success]- Answer
>> False

> [!question] In relational algebra, the rename operation (ρ) can change both the relation name and attribute names.
>> [!success]- Answer
>> True

> [!question] The outer join preserves only matching tuples from both relations.
>> [!success]- Answer
>> False

> [!question] A subquery in SQL always executes before the outer query.
>> [!success]- Answer
>> False

> [!question] The Cartesian product of two relations always produces a meaningful result without further selection.
>> [!success]- Answer
>> False

> [!question] The set difference operator (-) is commutative.
>> [!success]- Answer
>> False

> [!question] Relational algebra is considered procedural because it specifies the order of operations.
>> [!success]- Answer
>> True

> [!question] Which operation removes duplicate tuples from a relation?
> a) Selection
> b) Projection
> c) Division
> d) Rename
>> [!success]- Answer
>> b) Projection

> [!question] What is the result of R ⋈ S when R and S share no common attributes?
> a) Natural join returns an empty set
> b) Natural join returns the Cartesian product
> c) Natural join returns R
> d) Natural join returns S
>> [!success]- Answer
>> b) Natural join returns the Cartesian product

> [!question] Which join type returns all tuples from the left relation and matching tuples from the right?
> a) Inner join
> b) Left outer join
> c) Right outer join
> d) Full outer join
>> [!success]- Answer
>> b) Left outer join

> [!question] In relational algebra, which symbol represents the selection operation?
> a) π
> b) σ
> c) ρ
> d) τ
>> [!success]- Answer
>> b) σ

> [!question] Which of the following is NOT a valid relational algebra operation?
> a) Union
> b) Intersection
> c) Multiplication
> d) Division
>> [!success]- Answer
>> c) Multiplication

> [!question] The division operator R ÷ S answers which type of query?
> a) Find all tuples in R that match all tuples in S
> b) Find all tuples in R that match at least one tuple in S
> c) Find all tuples in R that match no tuple in S
> d) Find all tuples in S that are not in R
>> [!success]- Answer
>> a) Find all tuples in R that match all tuples in S

> [!question] What does the semi-join (⋉) return?
> a) All tuples from both relations
> b) Tuples from the left relation that have a match in the right relation
> c) Tuples from the right relation only
> d) The Cartesian product filtered by a condition
>> [!success]- Answer
>> b) Tuples from the left relation that have a match in the right relation

> [!question] Which SQL clause is equivalent to the projection operation in relational algebra?
> a) WHERE
> b) SELECT
> c) FROM
> d) GROUP BY
>> [!success]- Answer
>> b) SELECT

> [!question] What is the degree (arity) of a relation?
> a) The number of tuples
> b) The number of attributes
> c) The number of primary keys
> d) The number of foreign keys
>> [!success]- Answer
>> b) The number of attributes

> [!question] Which operation combines two relations but keeps only the common tuples?
> a) Union
> b) Difference
> c) Intersection
> d) Cartesian product
>> [!success]- Answer
>> c) Intersection

> [!question] Match the relational algebra operator with its symbol.
>> [!example] Group A
>> a) Selection
>> b) Projection
>> c) Rename
>> d) Join
>
>> [!example] Group B
>> n) ρ
>> o) ⋈
>> p) σ
>> q) π
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the SQL clause with its relational algebra equivalent.
>> [!example] Group A
>> a) WHERE
>> b) SELECT
>> c) FROM
>> d) DISTINCT
>
>> [!example] Group B
>> n) Projection
>> o) Selection
>> p) Remove duplicates
>> q) Relation reference
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the join type with its description.
>> [!example] Group A
>> a) Inner join
>> b) Left outer join
>> c) Right outer join
>> d) Full outer join
>
>> [!example] Group B
>> n) Keeps all tuples from both sides, NULLs for non-matches
>> o) Keeps all tuples from the right side
>> p) Keeps only matching tuples from both sides
>> q) Keeps all tuples from the left side
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the set operation with its property.
>> [!example] Group A
>> a) Union
>> b) Intersection
>> c) Difference
>> d) Cartesian product
>
>> [!example] Group B
>> n) Not commutative
>> o) Commutative and associative
>> p) Combines every tuple of R with every tuple of S
>> q) Returns only common tuples
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the relational algebra concept with its definition.
>> [!example] Group A
>> a) Cardinality
>> b) Degree
>> c) Domain
>> d) Tuple
>
>> [!example] Group B
>> n) Number of attributes in a relation
>> o) A single row in a relation
>> p) Set of allowed values for an attribute
>> q) Number of tuples in a relation
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> p)
>> d) -> o)

> [!question] Match the SQL join type with its relational algebra implementation.
>> [!example] Group A
>> a) CROSS JOIN
>> b) NATURAL JOIN
>> c) JOIN ... ON
>> d) LEFT JOIN
>
>> [!example] Group B
>> n) σ condition (R × S)
>> o) R ⋈ S (automatic equality on common attributes)
>> p) R × S
>> q) R ⟕ S
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the subquery type with its characteristic.
>> [!example] Group A
>> a) Correlated subquery
>> b) Scalar subquery
>> c) Row subquery
>> d) Table subquery
>
>> [!example] Group B
>> n) Returns multiple columns and rows
>> o) Returns a single value
>> p) References outer query columns
>> q) Returns a single row with multiple columns
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the constraint type with its description.
>> [!example] Group A
>> a) PRIMARY KEY
>> b) FOREIGN KEY
>> c) UNIQUE
>> d) NOT NULL
>
>> [!example] Group B
>> n) Ensures no duplicate values
>> o) Uniquely identifies each row
>> p) References a primary key in another table
>> q) Ensures a column cannot have NULL
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the key type with its property.
>> [!example] Group A
>> a) Superkey
>> b) Candidate key
>> c) Primary key
>> d) Foreign key
>
>> [!example] Group B
>> n) Minimal superkey
>> o) Chosen unique identifier
>> p) References another relation's key
>> q) Set of attributes that uniquely identifies tuples
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)
"""

# ============================================================
# CHAPTER 01 - QUIZ 2
# ============================================================
QUIZ_CONTENT['Chapter_01_2'] = """---
sources:
  - "[[2. SQL Inner Join Deep Dive]]"
  - "[[3. SQL Outer Joins Explained]]"
  - "[[4. Auto-Join and Self-Reference]]"
  - "[[01 Views]]"
  - "[[02 Views and Virtual Tables]]"
  - "[[03 Updatable Views and Check Options]]"
---

> [!question] A self-join is performed by joining a table with itself using aliases.
>> [!success]- Answer
>> True

> [!question] A view in SQL is physically stored as a separate table on disk.
>> [!success]- Answer
>> False

> [!question] The WITH CHECK OPTION clause prevents inserts that would make the row disappear from the view.
>> [!success]- Answer
>> True

> [!question] An outer join always returns fewer rows than an inner join.
>> [!success]- Answer
>> False

> [!question] Views can be used to provide row-level and column-level security.
>> [!success]- Answer
>> True

> [!question] A correlated subquery is evaluated once for each row of the outer query.
>> [!success]- Answer
>> True

> [!question] The UNION operator removes duplicate rows by default.
>> [!success]- Answer
>> True

> [!question] In an auto-join, you must use table aliases to avoid ambiguity.
>> [!success]- Answer
>> True

> [!question] A view that is based on multiple base tables is always updatable.
>> [!success]- Answer
>> False

> [!question] The EXISTS operator returns TRUE if the subquery returns at least one row.
>> [!success]- Answer
>> True

> [!question] Which clause is used to filter groups in SQL?
> a) WHERE
> b) HAVING
> c) ORDER BY
> d) GROUP BY
>> [!success]- Answer
>> b) HAVING

> [!question] What does the COALESCE function do?
> a) Returns the first non-NULL value from a list
> b) Returns NULL if any argument is NULL
> c) Concatenates two strings
> d) Converts a value to a different data type
>> [!success]- Answer
>> a) Returns the first non-NULL value from a list

> [!question] Which join returns only the rows where the join condition is satisfied?
> a) LEFT JOIN
> b) RIGHT JOIN
> c) INNER JOIN
> d) FULL OUTER JOIN
>> [!success]- Answer
>> c) INNER JOIN

> [!question] What is the purpose of the GROUP BY clause?
> a) To sort the result set
> b) To filter rows before grouping
> c) To group rows that have the same values in specified columns
> d) To join tables
>> [!success]- Answer
>> c) To group rows that have the same values in specified columns

> [!question] Which of the following is true about SQL views?
> a) Views always improve query performance
> b) Views are stored as temporary tables
> c) Views provide a layer of abstraction over base tables
> d) Views cannot reference other views
>> [!success]- Answer
>> c) Views provide a layer of abstraction over base tables

> [!question] What does the ANY operator do when used with a subquery?
> a) Returns TRUE if all values in the subquery satisfy the condition
> b) Returns TRUE if any value in the subquery satisfies the condition
> c) Returns TRUE if the subquery returns no rows
> d) Returns TRUE if the subquery returns exactly one row
>> [!success]- Answer
>> b) Returns TRUE if any value in the subquery satisfies the condition

> [!question] Which SQL function returns the current date and time?
> a) GETDATE()
> b) CURRENT_TIMESTAMP
> c) SYSDATE
> d) All of the above
>> [!success]- Answer
>> d) All of the above

> [!question] What is the difference between UNION and UNION ALL?
> a) UNION is faster than UNION ALL
> b) UNION removes duplicates, UNION ALL keeps all rows
> c) UNION ALL removes duplicates, UNION keeps all rows
> d) There is no difference
>> [!success]- Answer
>> b) UNION removes duplicates, UNION ALL keeps all rows

> [!question] Which of the following is NOT a valid aggregate function?
> a) COUNT
> b) SUM
> c) AVG
> d) FIND
>> [!success]- Answer
>> d) FIND

> [!question] What does the NULLIF function do?
> a) Returns NULL if both arguments are equal
> b) Returns NULL if the first argument is NULL
> c) Returns the first non-NULL value
> d) Returns NULL if both arguments are NULL
>> [!success]- Answer
>> a) Returns NULL if both arguments are equal

> [!question] Match the SQL join with the Venn diagram description.
>> [!example] Group A
>> a) INNER JOIN
>> b) LEFT JOIN
>> c) RIGHT JOIN
>> d) FULL OUTER JOIN
>
>> [!example] Group B
>> n) All from right, matching from left
>> o) Intersection only
>> p) All from both sides
>> q) All from left, matching from right
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the SQL concept with its description.
>> [!example] Group A
>> a) Correlated subquery
>> b) Scalar subquery
>> c) Derived table
>> d) CTE
>
>> [!example] Group B
>> n) Named temporary result set using WITH
>> o) Subquery in FROM clause
>> p) Inner query references outer query
>> q) Returns a single value
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the view characteristic with its description.
>> [!example] Group A
>> a) Simple view
>> b) Complex view
>> c) Updatable view
>> d) WITH CHECK OPTION
>
>> [!example] Group B
>> n) Contains functions or joins
>> o) Prevents invisible row modifications
>> p) Derived from a single table without functions
>> q) Allows DML operations
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the SQL join with its correct use case.
>> [!example] Group A
>> a) Self-join
>> b) Equi-join
>> c) Theta-join
>> d) Cross join
>
>> [!example] Group B
>> n) Uses an operator other than equality
>> o) Combine every row with every other row
>> p) Join a table with itself
>> q) Uses equality condition
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the aggregate function with its behavior.
>> [!example] Group A
>> a) COUNT(*)
>> b) COUNT(DISTINCT col)
>> c) SUM(col)
>> d) AVG(col)
>
>> [!example] Group B
>> n) Adds all non-NULL values
>> p) Counts unique non-NULL values
>> q) Counts all rows including NULLs
>> r) Average of non-NULL values
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> r)

> [!question] Match the SQL operator with its purpose.
>> [!example] Group A
>> a) IN
>> b) BETWEEN
>> c) LIKE
>> d) EXISTS
>
>> [!example] Group B
>> n) Pattern matching with wildcards
>> o) Checks value within a range
>> p) Checks membership in a set
>> q) Checks if subquery returns rows
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the query clause with its execution order.
>> [!example] Group A
>> a) WHERE
>> b) GROUP BY
>> c) HAVING
>> d) ORDER BY
>
>> [!example] Group B
>> n) Second
>> o) Third
>> p) First
>> q) Fourth
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the view operation with its requirement.
>> [!example] Group A
>> a) CREATE VIEW
>> b) DROP VIEW
>> c) ALTER VIEW
>> d) SELECT from view
>
>> [!example] Group B
>> n) Requires SELECT privilege on base tables
>> o) Requires DROP privilege
>> p) Requires CREATE VIEW privilege
>> q) Modifies view definition
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the subquery operator with its behavior.
>> [!example] Group A
>> a) ALL
>> b) ANY
>> c) EXISTS
>> d) IN
>
>> [!example] Group B
>> n) TRUE if subquery has any rows
>> o) TRUE if value matches any in list
>> p) TRUE if condition holds for every subquery value
>> q) TRUE if condition holds for at least one subquery value
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)
"""

# ============================================================
# CHAPTER 02 - QUIZ 1
# ============================================================
QUIZ_CONTENT['Chapter_02_1'] = """---
sources:
  - "[[01 Static Constraints]]"
  - "[[02 Foreign Key Behaviors]]"
  - "[[03 Dynamic Constraints Triggers]]"
  - "[[04 Advanced Triggers]]"
---

> [!question] A CHECK constraint can reference columns in other tables.
>> [!success]- Answer
>> False

> [!question] A FOREIGN KEY constraint ensures referential integrity between two tables.
>> [!success]- Answer
>> True

> [!question] A trigger can be fired BEFORE, AFTER, or INSTEAD OF an event.
>> [!success]- Answer
>> True

> [!question] The DEFAULT constraint automatically assigns a value when no value is provided.
>> [!success]- Answer
>> True

> [!question] A table can have multiple PRIMARY KEY constraints.
>> [!success]- Answer
>> False

> [!question] A UNIQUE constraint allows multiple NULL values in SQL.
>> [!success]- Answer
>> True

> [!question] Triggers can be used to enforce complex business rules that cannot be expressed as constraints.
>> [!success]- Answer
>> True

> [!question] The ON DELETE CASCADE option automatically deletes child rows when a parent row is deleted.
>> [!success]- Answer
>> True

> [!question] Constraints are always evaluated at the end of a transaction.
>> [!success]- Answer
>> False

> [!question] A NOT NULL constraint is a column-level constraint that prevents NULL values.
>> [!success]- Answer
>> True

> [!question] Which constraint ensures that a column value must exist in another table?
> a) PRIMARY KEY
> b) UNIQUE
> c) FOREIGN KEY
> d) CHECK
>> [!success]- Answer
>> c) FOREIGN KEY

> [!question] What happens when ON DELETE SET NULL is specified on a foreign key?
> a) Parent rows are deleted and child rows are also deleted
> b) Parent rows are deleted and child foreign key values are set to NULL
> c) Parent deletion is prevented if child rows exist
> d) Parent rows are deleted and child rows are updated with default values
>> [!success]- Answer
>> b) Parent rows are deleted and child foreign key values are set to NULL

> [!question] Which trigger timing executes the trigger action instead of the triggering statement?
> a) BEFORE
> b) AFTER
> c) INSTEAD OF
> d) ON
>> [!success]- Answer
>> c) INSTEAD OF

> [!question] What is a statement-level trigger?
> a) A trigger that fires once per modified row
> b) A trigger that fires once per SQL statement regardless of rows affected
> c) A trigger that fires before the statement executes
> d) A trigger that fires after the statement executes
>> [!success]- Answer
>> b) A trigger that fires once per SQL statement regardless of rows affected

> [!question] Which of the following is NOT a type of trigger event?
> a) INSERT
> b) UPDATE
> c) SELECT
> d) DELETE
>> [!success]- Answer
>> c) SELECT

> [!question] What is the purpose of an assertion in SQL?
> a) To define a primary key
> b) To enforce a condition that must always be true across multiple tables
> c) To create an index
> d) To define a foreign key
>> [!success]- Answer
>> b) To enforce a condition that must always be true across multiple tables

> [!question] Which keyword is used to defer constraint checking to the end of a transaction?
> a) DEFERRABLE
> b) DEFERRED
> c) INITIALLY DEFERRED
> d) CHECK ON COMMIT
>> [!success]- Answer
>> c) INITIALLY DEFERRED

> [!question] What does the ON UPDATE CASCADE option do?
> a) Updates the parent table when the child is updated
> b) Cascades updates to foreign key values in child tables
> c) Prevents updates to the primary key
> d) Logs all update operations
>> [!success]- Answer
>> b) Cascades updates to foreign key values in child tables

> [!question] Which statement is used to remove a trigger from the database?
> a) DELETE TRIGGER
> b) REMOVE TRIGGER
> c) DROP TRIGGER
> d) ALTER TRIGGER
>> [!success]- Answer
>> c) DROP TRIGGER

> [!question] What is a row-level trigger?
> a) A trigger that fires once per affected row
> b) A trigger that fires once per statement
> c) A trigger that fires before the statement
> d) A trigger that fires after the statement
>> [!success]- Answer
>> a) A trigger that fires once per affected row

> [!question] Match the constraint with its SQL keyword.
>> [!example] Group A
>> a) Primary key
>> b) Foreign key
>> c) Unique constraint
>> d) Check constraint
>
>> [!example] Group B
>> n) REFERENCES
>> o) UNIQUE
>> p) CHECK
>> q) PRIMARY KEY
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the foreign key referential action with its behavior.
>> [!example] Group A
>> a) CASCADE
>> b) SET NULL
>> c) SET DEFAULT
>> d) NO ACTION
>
>> [!example] Group B
>> n) Rejects the operation
>> o) Propagates changes to child rows
>> p) Sets child FK to default value
>> q) Sets child FK to NULL
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the trigger type with its description.
>> [!example] Group A
>> a) BEFORE trigger
>> b) AFTER trigger
>> c) INSTEAD OF trigger
>> d) Row-level trigger
>
>> [!example] Group B
>> n) Fires on views
>> o) Fires per affected row
>> p) Fires before the event
>> q) Fires after the event
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the constraint characteristic with its property.
>> [!example] Group A
>> a) NOT NULL
>> b) DEFAULT
>> c) UNIQUE
>> d) PRIMARY KEY
>
>> [!example] Group B
>> n) Can have only one per table
>> o) Allows one NULL per column
>> p) Automatically assigns values
>> q) Prevents NULL values
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the constraint deferrability option with its behavior.
>> [!example] Group A
>> a) NOT DEFERRABLE
>> b) INITIALLY IMMEDIATE
>> c) INITIALLY DEFERRED
>> d) DEFERRABLE
>
>> [!example] Group B
>> n) Can be deferred
>> o) Checked at end of transaction
>> p) Checked immediately, cannot defer
>> q) Checked immediately by default
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the DDL command with its function.
>> [!example] Group A
>> a) CREATE TABLE
>> b) ALTER TABLE
>> c) DROP TABLE
>> d) TRUNCATE TABLE
>
>> [!example] Group B
>> n) Removes all rows but keeps structure
>> o) Modifies table structure
>> p) Removes table and structure
>> q) Creates a new table
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> p)
>> d) -> n)

> [!question] Match the DML statement with its effect.
>> [!example] Group A
>> a) INSERT
>> b) UPDATE
>> c) DELETE
>> d) MERGE
>
>> [!example] Group B
>> n) Modifies existing rows
>> o) Removes rows
>> p) Adds new rows
>> q) Upserts (insert or update)
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the trigger variable with its meaning.
>> [!example] Group A
>> a) NEW
>> b) OLD
>> c) TG_OP
>> d) TG_TABLE_NAME
>
>> [!example] Group B
>> n) Name of the table affected
>> o) Operation that fired the trigger
>> p) New row values
>> q) Old row values
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the integrity constraint category with its scope.
>> [!example] Group A
>> a) Domain constraint
>> b) Tuple constraint
>> c) Referential constraint
>> d) Assertion
>
>> [!example] Group B
>> n) Across multiple tables
>> o) Limits attribute values
>> p) Between two tables via FK
>> q) Within a single row
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)
"""

# ============================================================
# CHAPTER 02 - QUIZ 2
# ============================================================
QUIZ_CONTENT['Chapter_02_2'] = """---
sources:
  - "[[05 Triggers and Events]]"
  - "[[06 Assertions and Deferrable Constraints]]"
  - "[[07 Altering Constraints and Operational Behavior]]"
  - "[[08 Trigger Execution and Automation Scenarios]]"
  - "[[09 Metadata and the Information Schema]]"
---

> [!question] The INFORMATION_SCHEMA contains metadata about database objects.
>> [!success]- Answer
>> True

> [!question] A trigger can call stored procedures and functions.
>> [!success]- Answer
>> True

> [!question] Assertions in SQL are widely supported by all major database systems.
>> [!success]- Answer
>> False

> [!question] A DEFERRABLE constraint can be checked at the end of a transaction.
>> [!success]- Answer
>> True

> [!question] Multiple triggers of the same type on the same table are not allowed.
>> [!success]- Answer
>> False

> [!question] The pg_catalog schema in PostgreSQL contains system tables.
>> [!success]- Answer
>> True

> [!question] An EVENT trigger can be fired on DDL statements.
>> [!success]- Answer
>> True

> [!question] Disabling a constraint temporarily allows data that violates the constraint.
>> [!success]- Answer
>> True

> [!question] The INFORMATION_SCHEMA.TABLES view shows all tables in the database.
>> [!success]- Answer
>> True

> [!question] A trigger can fire on SELECT statements.
>> [!success]- Answer
>> False

> [!question] Which schema contains metadata about database objects in SQL standard?
> a) sys
> b) INFORMATION_SCHEMA
> c) pg_catalog
> d) master
>> [!success]- Answer
>> b) INFORMATION_SCHEMA

> [!question] What does the SET CONSTRAINTS statement do?
> a) Creates a new constraint
> b) Drops an existing constraint
> c) Changes the deferral mode of constraints for the current transaction
> d) Disables all constraints
>> [!success]- Answer
>> c) Changes the deferral mode of constraints for the current transaction

> [!question] What is the purpose of a trigger function?
> a) To define the trigger condition
> b) To encapsulate the trigger logic in a reusable function
> c) To replace the trigger
> d) To disable the trigger
>> [!success]- Answer
>> b) To encapsulate the trigger logic in a reusable function

> [!question] Which system catalog view contains information about table columns?
> a) TABLES
> b) COLUMNS
> c) SCHEMATA
> d) VIEWS
>> [!success]- Answer
>> b) COLUMNS

> [!question] What happens when you ALTER a table to add a NOT NULL constraint to a column that contains NULL values?
> a) The constraint is added and NULLs are automatically converted
> b) The ALTER statement fails
> c) The constraint is added but only applies to new rows
> d) NULLs are deleted
>> [!success]- Answer
>> b) The ALTER statement fails

> [!question] Which of the following can be used to execute automated tasks at scheduled times?
> a) Trigger
> b) Event
> c) Constraint
> d) Assertion
>> [!success]- Answer
>> b) Event

> [!question] What is a transition table in a trigger?
> a) A temporary table that stores the old and new values of affected rows
> b) A permanent log table
> c) A view created by the trigger
> d) An index maintained by the trigger
>> [!success]- Answer
>> a) A temporary table that stores the old and new values of affected rows

> [!question] Which command is used to view existing triggers?
> a) SHOW TRIGGERS
> b) LIST TRIGGERS
> c) SELECT FROM INFORMATION_SCHEMA.TRIGGERS
> d) DISPLAY TRIGGERS
>> [!success]- Answer
>> c) SELECT FROM INFORMATION_SCHEMA.TRIGGERS

> [!question] What is the purpose of a trigger condition (WHEN clause)?
> a) To specify when the trigger should not fire
> b) To filter which rows cause the trigger to execute
> c) To set the trigger timing
> d) To define the trigger event
>> [!success]- Answer
>> b) To filter which rows cause the trigger to execute

> [!question] Which of the following is true about materialized views?
> a) They are always up-to-date with base tables
> b) They store data physically on disk
> c) They cannot be indexed
> d) They cannot be refreshed
>> [!success]- Answer
>> b) They store data physically on disk

> [!question] Match the system catalog with its description.
>> [!example] Group A
>> a) INFORMATION_SCHEMA
>> b) pg_catalog
>> c) sys
>> d) mysql
>
>> [!example] Group B
>> n) SQL standard metadata
>> o) MySQL system tables
>> p) SQL Server system catalog
>> q) PostgreSQL system catalog
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> p)
>> d) -> o)

> [!question] Match the trigger event with its description.
>> [!example] Group A
>> a) BEFORE INSERT
>> b) AFTER UPDATE
>> c) INSTEAD OF DELETE
>> d) TRUNCATE
>
>> [!example] Group B
>> n) Used on views
>> o) Fires before row insertion
>> p) Fires after row modification
>> q) Cannot be captured by standard triggers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the constraint operation with the SQL command.
>> [!example] Group A
>> a) Add constraint
>> b) Drop constraint
>> c) Rename constraint
>> d) Disable constraint
>
>> [!example] Group B
>> n) ALTER TABLE ... DISABLE
>> o) ALTER TABLE ... RENAME CONSTRAINT
>> p) ALTER TABLE ... DROP CONSTRAINT
>> q) ALTER TABLE ... ADD CONSTRAINT
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the metadata view with its content.
>> [!example] Group A
>> a) INFORMATION_SCHEMA.TABLES
>> b) INFORMATION_SCHEMA.COLUMNS
>> c) INFORMATION_SCHEMA.TABLE_CONSTRAINTS
>> d) INFORMATION_SCHEMA.TRIGGERS
>
>> [!example] Group B
>> n) Column definitions
>> o) Table names and types
>> p) Trigger definitions
>> q) Constraint information
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the transaction property with its purpose.
>> [!example] Group A
>> a) Atomicity
>> b) Consistency
>> c) Isolation
>> d) Durability
>
>> [!example] Group B
>> n) Concurrent transactions don't interfere
>> o) Permanent after commit
>> p) All-or-nothing execution
>> q) Valid state maintained
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the constraint type with the violation scenario.
>> [!example] Group A
>> a) NOT NULL
>> b) UNIQUE
>> c) CHECK
>> d) FOREIGN KEY
>
>> [!example] Group B
>> n) Inserting a duplicate value
>> o) Inserting NULL in a non-null column
>> p) Inserting a value with no matching parent
>> q) Inserting a value outside the allowed range
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the ALTER TABLE operation with its effect.
>> [!example] Group A
>> a) ALTER TABLE ... ADD COLUMN
>> b) ALTER TABLE ... DROP COLUMN
>> c) ALTER TABLE ... ALTER COLUMN
>> d) ALTER TABLE ... SET SCHEMA
>
>> [!example] Group B
>> n) Removes a column
>> o) Changes column data type
>> p) Moves table to another schema
>> q) Adds a new column
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the trigger scope with its definition.
>> [!example] Group A
>> a) Statement-level
>> b) Row-level
>> c) Column-level UPDATE
>> d) Event-level
>
>> [!example] Group B
>> n) Fires on DDL operations
>> o) Fires once per SQL statement
>> p) Fires only when specific columns updated
>> q) Fires once per affected row
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the privilege type with its description.
>> [!example] Group A
>> a) SELECT
>> b) INSERT
>> c) UPDATE
>> d) DELETE
>
>> [!example] Group B
>> n) Add new rows
>> o) Read data
>> p) Remove rows
>> q) Modify existing rows
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)
"""

# ============================================================
# CHAPTER 03 - QUIZ 1
# ============================================================
QUIZ_CONTENT['Chapter_03_1'] = """---
sources:
  - "[[01 ACID Properties]]"
  - "[[02 Concurrency Control and Isolation]]"
  - "[[03 Crash Recovery Mechanisms]]"
  - "[[05 Transactions and Crash Recovery]]"
---

> [!question] The ACID acronym stands for Atomicity, Consistency, Isolation, and Durability.
>> [!success]- Answer
>> True

> [!question] Dirty read occurs when a transaction reads uncommitted data from another transaction.
>> [!success]- Answer
>> True

> [!question] The SERIALIZABLE isolation level prevents all concurrency anomalies.
>> [!success]- Answer
>> True

> [!question] A commit makes the transaction's changes permanent and visible to others.
>> [!success]- Answer
>> True

> [!question] The two-phase locking protocol guarantees serializability.
>> [!success]- Answer
>> True

> [!question] A deadlock occurs when two transactions wait indefinitely for locks held by each other.
>> [!success]- Answer
>> True

> [!question] The READ UNCOMMITTED isolation level prevents dirty reads.
>> [!success]- Answer
>> False

> [!question] Checkpointing is a technique used to reduce recovery time after a crash.
>> [!success]- Answer
>> True

> [!question] The Write-Ahead Logging (WAL) protocol ensures that log records are written before data pages.
>> [!success]- Answer
>> True

> [!question] The phantom read anomaly cannot occur at the REPEATABLE READ isolation level.
>> [!success]- Answer
>> False

> [!question] Which isolation level guarantees that no concurrency anomalies can occur?
> a) READ UNCOMMITTED
> b) READ COMMITTED
> c) REPEATABLE READ
> d) SERIALIZABLE
>> [!success]- Answer
>> d) SERIALIZABLE

> [!question] What is a dirty read?
> a) Reading data that was committed
> b) Reading data that was written by an uncommitted transaction
> c) Reading the same data twice and getting different results
> d) Reading phantom rows
>> [!success]- Answer
>> b) Reading data that was written by an uncommitted transaction

> [!question] Which concurrency anomaly occurs when a transaction reads the same data twice and gets different results?
> a) Dirty read
> b) Non-repeatable read
> c) Phantom read
> d) Lost update
>> [!success]- Answer
>> b) Non-repeatable read

> [!question] What is a lost update?
> a) When a transaction deletes data by mistake
> b) When two concurrent transactions overwrite each other's changes
> c) When a transaction reads expired data
> d) When a transaction cannot complete due to deadlock
>> [!success]- Answer
>> b) When two concurrent transactions overwrite each other's changes

> [!question] Which lock type allows other transactions to read but not write?
> a) Exclusive lock
> b) Shared lock
> c) Update lock
> d) Intent lock
>> [!success]- Answer
>> b) Shared lock

> [!question] What is the purpose of the ROLLBACK command?
> a) To save changes permanently
> b) To undo all changes made in the current transaction
> c) To create a savepoint
> d) To lock a table
>> [!success]- Answer
>> b) To undo all changes made in the current transaction

> [!question] Which component of the DBMS is responsible for crash recovery?
> a) Query optimizer
> b) Storage manager
> c) Recovery manager
> d) Transaction manager
>> [!success]- Answer
>> c) Recovery manager

> [!question] What is a phantom read?
> a) Reading a row that does not exist
> b) A set of rows that appear and disappear during a transaction
> c) Reading uncommitted data
> d) Reading data from a different database
>> [!success]- Answer
>> b) A set of rows that appear and disappear during a transaction

> [!question] In the two-phase locking protocol, what happens in the shrinking phase?
> a) Locks are acquired
> b) Locks are released
> c) Locks are escalated
> d) Locks are converted
>> [!success]- Answer
>> b) Locks are released

> [!question] Which isolation level is the default in PostgreSQL?
> a) READ UNCOMMITTED
> b) READ COMMITTED
> c) REPEATABLE READ
> d) SERIALIZABLE
>> [!success]- Answer
>> b) READ COMMITTED

> [!question] Match the transaction property with its description.
>> [!example] Group A
>> a) Atomicity
>> b) Consistency
>> c) Isolation
>> d) Durability
>
>> [!example] Group B
>> n) Changes survive system failures
>> o) Concurrent execution appears serial
>> p) Transaction executes fully or not at all
>> q) Database constraints are preserved
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the isolation level with its main characteristic.
>> [!example] Group A
>> a) READ UNCOMMITTED
>> b) READ COMMITTED
>> c) REPEATABLE READ
>> d) SERIALIZABLE
>
>> [!example] Group B
>> n) Snapshot-based consistency
>> o) No isolation at all
>> p) Full isolation with serial execution
>> q) Prevents dirty reads only
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the concurrency anomaly with its definition.
>> [!example] Group A
>> a) Dirty read
>> b) Non-repeatable read
>> c) Phantom read
>> d) Lost update
>
>> [!example] Group B
>> n) Two writes cancel each other
>> o) Row set changes between reads
>> p) Same row read twice yields different values
>> q) Uncommitted data is read
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the locking term with its meaning.
>> [!example] Group A
>> a) Shared lock
>> b) Exclusive lock
>> c) Deadlock
>> d) Two-phase locking
>
>> [!example] Group B
>> n) Write lock
>> o) Read lock
>> p) Protocol guaranteeing serializability
>> q) Circular wait condition
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the recovery concept with its role.
>> [!example] Group A
>> a) Redo log
>> b) Undo log
>> c) Checkpoint
>> d) WAL
>
>> [!example] Group B
>> n) Protocol ensuring log-before-data
>> o) Reapplies committed transactions after crash
>> p) Reverses uncommitted transactions
>> q) Marks point where all changes are flushed
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the concurrency control mechanism with its description.
>> [!example] Group A
>> a) Lock-based
>> b) Timestamp-based
>> c) Optimistic
>> d) MVCC
>
>> [!example] Group B
>> n) Maintains multiple versions of data
>> o) Assigns unique timestamps to transactions
>> p) Locks resources to prevent conflicts
>> q) Validates at commit time
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the transaction state with its meaning.
>> [!example] Group A
>> a) Active
>> b) Partially committed
>> c) Committed
>> d) Aborted
>
>> [!example] Group B
>> n) Transaction terminated unsuccessfully
>> p) Transaction completed successfully
>> q) Executing normally
>> r) Final statement executed
>
>> [!success]- Answer
>> a) -> q)
>> b) -> r)
>> c) -> p)
>> d) -> n)

> [!question] Match the schedule type with its property.
>> [!example] Group A
>> a) Serializable schedule
>> b) Recoverable schedule
>> c) Cascadeless schedule
>> d) Strict schedule
>
>> [!example] Group B
>> n) No dirty reads after transaction aborts
>> o) Equivalent to some serial execution
>> p) Cascading aborts are impossible
>> q) Uncommitted data not read by others
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match the log record type with its content.
>> [!example] Group A
>> a) Begin transaction
>> b) Update record
>> c) Commit record
>> d) Abort record
>
>> [!example] Group B
>> n) Transaction has ended successfully
>> o) Marks the start of a transaction
>> p) Transaction has failed
>> q) Old and new values of modified data
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)
"""

# ============================================================
# CHAPTER 03 - QUIZ 2
# ============================================================
QUIZ_CONTENT['Chapter_03_2'] = """---
sources:
  - "[[06 Master Class Transactions & Integrity]]"
  - "[[07 Advanced Concurrency Protocols]]"
  - "[[08 Concurrency Anomalies Deep Dive]]"
  - "[[09 Disaster Recovery Protocols]]"
---

> [!question] A cascading abort occurs when one transaction's abort forces other dependent transactions to abort.
>> [!success]- Answer
>> True

> [!question] Snapshot isolation is a variant of MVCC that gives each transaction a consistent snapshot.
>> [!success]- Answer
>> True

> [!question] In timestamp-based concurrency control, older transactions always win conflicts.
>> [!success]- Answer
>> False

> [!question] The write-skew anomaly can occur under snapshot isolation.
>> [!success]- Answer
>> True

> [!question] A strict schedule allows reading uncommitted data.
>> [!success]- Answer
>> False

> [!question] Disaster recovery protocols include backup and replication strategies.
>> [!success]- Answer
>> True

> [!question] The RPO (Recovery Point Objective) measures how much data loss is acceptable.
>> [!success]- Answer
>> True

> [!question] The RTO (Recovery Time Objective) measures the maximum acceptable downtime.
>> [!success]- Answer
>> True

> [!question] Optimistic concurrency control is best suited for high-conflict workloads.
>> [!success]- Answer
>> False

> [!question] A savepoint allows partial rollback within a transaction.
>> [!success]- Answer
>> True

> [!question] Which concurrency anomaly occurs when two transactions concurrently read and write overlapping data sets?
> a) Dirty read
> b) Phantom read
> c) Write-skew
> d) Lost update
>> [!success]- Answer
>> c) Write-skew

> [!question] What is a cascading abort?
> a) When a transaction aborts itself
> b) When aborting one transaction forces aborting dependent transactions
> c) When the system aborts all transactions
> d) When a transaction aborts due to deadlock
>> [!success]- Answer
>> b) When aborting one transaction forces aborting dependent transactions

> [!question] What is the difference between RPO and RTO?
> a) RPO is cost, RTO is time
> b) RPO measures data loss tolerance, RTO measures downtime tolerance
> c) RPO measures downtime, RTO measures data loss
> d) They are the same concept
>> [!success]- Answer
>> b) RPO measures data loss tolerance, RTO measures downtime tolerance

> [!question] Which backup type captures only the data changed since the last full backup?
> a) Full backup
> b) Differential backup
> c) Incremental backup
> d) Mirror backup
>> [!success]- Answer
>> c) Incremental backup

> [!question] What is the primary advantage of MVCC over lock-based concurrency control?
> a) Simpler implementation
> b) Readers never block writers and vice versa
> c) Requires less memory
> d) Prevents all anomalies
>> [!success]- Answer
>> b) Readers never block writers and vice versa

> [!question] What is the purpose of a savepoint in a transaction?
> a) To save the transaction permanently
> b) To mark a point within a transaction that can be rolled back to
> c) To save data to disk
> d) To create a checkpoint in the log
>> [!success]- Answer
>> b) To mark a point within a transaction that can be rolled back to

> [!question] Which replication strategy copies data to one or more standby servers?
> a) Synchronous replication
> b) Asynchronous replication
> c) Both a and b
> d) Sharding
>> [!success]- Answer
>> c) Both a and b

> [!question] What is the write-ahead logging (WAL) protocol?
> a) Writing data before logging
> b) Writing log records before data pages
> c) Writing data to multiple locations
> d) Writing logs after commit
>> [!success]- Answer
>> b) Writing log records before data pages

> [!question] Which of the following is NOT a disaster recovery strategy?
> a) Hot standby
> b) Cold backup
> c) Query optimization
> d) Geographic replication
>> [!success]- Answer
>> c) Query optimization

> [!question] What does the ARIES recovery algorithm stand for?
> a) Algorithm for Recovery and Isolation Exploiting Semantics
> b) Atomic Recovery with Integrated Error Safety
> c) Advanced Recovery of Isolated Event Systems
> d) Automatic Recovery from Integrated System Errors
>> [!success]- Answer
>> a) Algorithm for Recovery and Isolation Exploiting Semantics

> [!question] Match the isolation anomaly with its prevention level.
>> [!example] Group A
>> a) Dirty read
>> b) Non-repeatable read
>> c) Phantom read
>> d) Write-skew
>
>> [!example] Group B
>> n) Prevented at REPEATABLE READ
>> o) Prevented at READ COMMITTED
>> p) Prevented at SERIALIZABLE
>> q) Prevented at READ UNCOMMITTED (not applicable)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> p)

> [!question] Match the concurrency control protocol with its approach.
>> [!example] Group A
>> a) Two-phase locking
>> b) Timestamp ordering
>> c) Optimistic CC
>> d) MVCC
>
>> [!example] Group B
>> n) Validate at commit
>> o) Use timestamps for ordering
>> p) Multi-version snapshots
>> q) Lock acquisition and release phases
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the replication type with its description.
>> [!example] Group A
>> a) Synchronous replication
>> b) Asynchronous replication
>> c) Semi-synchronous
>> d) Group replication
>
>> [!example] Group B
>> n) Master waits for at least one replica
>> o) Multiple nodes coordinate replication
>> p) Master waits for all replicas
>> q) Master does not wait for replicas
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the backup type with its characteristic.
>> [!example] Group A
>> a) Full backup
>> b) Differential backup
>> c) Incremental backup
>> d) Transaction log backup
>
>> [!example] Group B
>> n) Captures all changes since last full backup
>> o) Captures all data
>> p) Captures all changes since last backup of any type
>> q) Captures committed transaction records
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match the deadlock handling strategy with its approach.
>> [!example] Group A
>> a) Timeout
>> b) Deadlock detection
>> c) Deadlock prevention
>> d) Wait-die
>
>> [!example] Group B
>> n) Older transaction waits for younger
>> o) Transaction aborts after waiting too long
>> p) Waits-for graph analysis
>> q) Ensures no circular waits can form
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the ARIES recovery phase with its purpose.
>> [!example] Group A
>> a) Analysis phase
>> b) Redo phase
>> c) Undo phase
>> d) Checkpoint phase
>
>> [!example] Group B
>> n) Reverses uncommitted transactions
>> q) Records consistent state
>> r) Determines which transactions to redo/undo
>> s) Reapplies committed changes
>
>> [!success]- Answer
>> a) -> r)
>> b) -> s)
>> c) -> n)
>> d) -> q)

> [!question] Match the transaction termination with its SQL command.
>> [!example] Group A
>> a) Successful completion
>> b) Manual rollback
>> c) Partial rollback
>> d) Auto-abort
>
>> [!example] Group B
>> n) ROLLBACK TO SAVEPOINT
>> o) COMMIT
>> p) System-generated ROLLBACK
>> q) ROLLBACK
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the log-based recovery term with its meaning.
>> [!example] Group A
>> a) LSN
>> b) Dirty page table
>> c) Transaction table
>> d) Redoable log
>
>> [!example] Group B
>> n) Tracks active transaction state
>> o) Tracks pages modified in buffer
>> p) Unique log sequence number
>> q) Contains committed transactions' changes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the fault tolerance technique with its description.
>> [!example] Group A
>> a) RAID 1
>> b) RAID 5
>> c) RAID 6
>> d) RAID 0
>
>> [!example] Group B
>> n) Striping without redundancy
>> o) Mirroring
>> p) Striping with parity
>> q) Striping with dual parity
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)
"""

# ============================================================
# CHAPTER 04 - QUIZ 1
# ============================================================
QUIZ_CONTENT['Chapter_04_1'] = """---
sources:
  - "[[1. Query Processing Architecture]]"
  - "[[2. Relational Algebra & Logical Plans]]"
  - "[[3. Physical Operators & Algorithms]]"
  - "[[4. Advanced Physical Design]]"
  - "[[5. Cost Estimation & Calculations]]"
---

> [!question] Query optimization aims to find the most efficient execution plan for a query.
>> [!success]- Answer
>> True

> [!question] A query execution plan is a sequence of operations used to evaluate a query.
>> [!success]- Answer
>> True

> [!question] The query optimizer always chooses the optimal execution plan.
>> [!success]- Answer
>> False

> [!question] An index scan is always faster than a sequential scan.
>> [!success]- Answer
>> False

> [!question] The cost of a query is measured in terms of disk I/O, CPU, and memory usage.
>> [!success]- Answer
>> True

> [!question] A B+ tree index stores both keys and actual data in its leaf nodes.
>> [!success]- Answer
>> True

> [!question] A bitmap index is well-suited for columns with high cardinality.
>> [!success]- Answer
>> False

> [!question] Hash joins are efficient for equi-joins on large datasets.
>> [!success]- Answer
>> True

> [!question] The nested loop join is most efficient when one relation is very small.
>> [!success]- Answer
>> True

> [!question] Materializing intermediate results always improves query performance.
>> [!success]- Answer
>> False

> [!question] Which join algorithm is best for joining a small table with a large table?
> a) Hash join
> b) Nested loop join
> c) Sort-merge join
> d) Index nested loop join
>> [!success]- Answer
>> b) Nested loop join

> [!question] What does a query optimizer use to estimate costs?
> a) Query syntax only
> b) Database statistics and metadata
> c) User preferences
> d) Network speed
>> [!success]- Answer
>> b) Database statistics and metadata

> [!question] Which type of index is best for range queries (e.g., salary BETWEEN 1000 AND 2000)?
> a) Hash index
> b) B+ tree index
> c) Bitmap index
> d) Clustered index
>> [!success]- Answer
>> b) B+ tree index

> [!question] What is a clustered index?
> a) An index that stores data in a separate structure from the table
> b) An index that determines the physical order of data in the table
> c) An index that can have only one column
> d) An index that cannot be dropped
>> [!success]- Answer
>> b) An index that determines the physical order of data in the table

> [!question] What is the main advantage of a sort-merge join?
> a) It works well for non-equi joins
> b) It requires no indexing
> c) It is always the fastest
> d) It uses the least memory
>> [!success]- Answer
>> a) It works well for non-equi joins

> [!question] What does selectivity estimate in query optimization?
> a) The number of columns selected
> b) The fraction of rows that satisfy a predicate
> c) The speed of the query
> d) The size of the table
>> [!success]- Answer
>> b) The fraction of rows that satisfy a predicate

> [!question] How does a hash join work?
> a) It sorts both relations then merges them
> b) It builds a hash table on the smaller relation and probes with the larger
> c) It iterates through each row of both relations
> d) It uses indexes to find matching rows
>> [!success]- Answer
>> b) It builds a hash table on the smaller relation and probes with the larger

> [!question] What is a covering index?
> a) An index that covers all columns of a table
> b) An index that contains all columns needed by a query, avoiding table access
> c) An index that covers multiple tables
> d) An index that covers only the primary key
>> [!success]- Answer
>> b) An index that contains all columns needed by a query, avoiding table access

> [!question] Which optimization technique transforms a query into an equivalent but more efficient form?
> a) Physical optimization
> b) Logical optimization
> c) Semantic optimization
> d) Parametric optimization
>> [!success]- Answer
>> b) Logical optimization

> [!question] What is the purpose of query decomposition?
> a) To break a query into smaller subqueries
> b) To parse and validate the SQL query
> c) To separate the query from the data
> d) To create indexes
>> [!success]- Answer
>> a) To break a query into smaller subqueries

> [!question] Match the join algorithm with its description.
>> [!example] Group A
>> a) Nested loop join
>> b) Hash join
>> c) Sort-merge join
>> d) Index nested loop join
>
>> [!example] Group B
>> n) Uses an existing index for lookups
>> o) Creates a hash table on the smaller input
>> p) Iterates through each pair of tuples
>> q) Sorts both inputs then merges
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the index type with its best use case.
>> [!example] Group A
>> a) B+ tree
>> b) Hash index
>> c) Bitmap index
>> d) GiST index
>
>> [!example] Group B
>> n) Full-text search
>> o) Equality lookups
>> p) Range queries
>> q) Low cardinality columns
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the query processing step with its description.
>> [!example] Group A
>> a) Parsing
>> b) Rewriting
>> c) Optimization
>> d) Execution
>
>> [!example] Group B
>> n) Selecting the best plan
>> o) Syntax checking and tree building
>> p) Running the chosen plan
>> q) View expansion and simplification
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the physical operator with its description.
>> [!example] Group A
>> a) Sequential scan
>> b) Index scan
>> c) Index-only scan
>> d) Bitmap scan
>
>> [!example] Group B
>> n) Reads all pages of a table in order
>> o) Reads index pages then fetches table rows
>> p) Combines multiple bitmap index scans
>> q) Reads only from the index, no table access
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> q)
>> d) -> p)

> [!question] Match the cost metric with its unit.
>> [!example] Group A
>> a) I/O cost
>> b) CPU cost
>> c) Memory cost
>> d) Network cost
>
>> [!example] Group B
>> n) Bytes or pages
>> o) Page transfers
>> p) Instructions
>> q) Packet transfers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the optimization heuristic with its rule.
>> [!example] Group A
>> a) Push selection down
>> b) Push projection down
>> c) Combine cascading selections
>> d) Replace Cartesian product with join
>
>> [!example] Group B
>> n) Merge σ conditions with AND
>> o) Convert R × S with WHERE condition
>> p) Apply filters as early as possible
>> q) Remove unnecessary columns early
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the statistic type with its purpose.
>> [!example] Group A
>> a) Cardinality
>> b) Number of distinct values
>> c) Data distribution histogram
>> d) Null fraction
>
>> [!example] Group B
>> n) Frequency of values across ranges
>> o) Uniqueness measure for a column
>> p) Proportion of NULLs in a column
>> q) Number of rows in a table
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the explain plan component with its meaning.
>> [!example] Group A
>> a) Estimated rows
>> b) Actual rows
>> c) Cost
>> d) Width
>
>> [!example] Group B
>> n) True number of rows processed
>> o) Relative computational expense
>> p) Average row size in bytes
>> q) Planner's row count estimate
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the index property with its definition.
>> [!example] Group A
>> a) Clustering factor
>> b) Index height
>> c) Fill factor
>> d) Leaf density
>
>> [!example] Group B
>> n) How many levels in the tree
>> o) Page fullness percentage
>> p) How ordered index matches table order
>> q) Number of keys per leaf page
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)
"""

# ============================================================
# CHAPTER 04 - QUIZ 2
# ============================================================
QUIZ_CONTENT['Chapter_04_2'] = """---
sources:
  - "[[8. Database Indexing Deep Dive]]"
  - "[[11. Algebraic Rewrite Rules and Heuristics]]"
  - "[[12. Physical Access Paths and Join Costs]]"
  - "[[15. Database Statistics and Selectivity Estimation]]"
  - "[[3. Query Optimization Heuristics]]"
---

> [!question] The query plan cache stores previously computed execution plans for reuse.
>> [!success]- Answer
>> True

> [!question] An index on (last_name, first_name) can be used for a query filtering only on first_name.
>> [!success]- Answer
>> False

> [!question] The order of tables in the FROM clause affects the optimizer's choices.
>> [!success]- Answer
>> True

> [!question] Statistics on a table are automatically updated after every INSERT or DELETE.
>> [!success]- Answer
>> False

> [!question] A partial index indexes only a subset of rows that satisfy a condition.
>> [!success]- Answer
>> True

> [!question] The IN clause is typically rewritten as a series of OR conditions by the optimizer.
>> [!success]- Answer
>> True

> [!question] A correlated subquery cannot be decorrelated by modern optimizers.
>> [!success]- Answer
>> False

> [!question] Index-only scans require that all queried columns be present in the index.
>> [!success]- Answer
>> True

> [!question] An ANALYZE command updates the statistics used by the query optimizer.
>> [!success]- Answer
>> True

> [!question] The merge join is optimal when both inputs are already sorted on the join key.
>> [!success]- Answer
>> True

> [!question] What command updates statistics for the query optimizer?
> a) UPDATE STATISTICS
> b) ANALYZE
> c) OPTIMIZE
> d) REFRESH
>> [!success]- Answer
>> b) ANALYZE

> [!question] Which of the following is true about query plan caching?
> a) Plans are never cached
> b) Cached plans are always optimal
> c) Parameterized queries can reuse cached plans
> d) Plan caching increases query execution time
>> [!success]- Answer
>> c) Parameterized queries can reuse cached plans

> [!question] What is the purpose of the EXPLAIN command?
> a) To execute a query
> b) To show the execution plan of a query
> c) To explain query syntax
> d) To create an index
>> [!success]- Answer
>> b) To show the execution plan of a query

> [!question] Which type of join is most memory-intensive?
> a) Nested loop join
> b) Hash join
> c) Sort-merge join
> d) Index nested loop join
>> [!success]- Answer
>> b) Hash join

> [!question] What does an index-organized table (IOT) store?
> a) Only the index structure separately
> b) The actual table data in the index structure
> c) Only foreign keys
> d) Only metadata
>> [!success]- Answer
>> b) The actual table data in the index structure

> [!question] Which factor does NOT affect join cost estimation?
> a) Table sizes
> b) Available indexes
> c) Number of columns in SELECT
> d) User name
>> [!success]- Answer
>> d) User name

> [!question] What is the primary purpose of a composite index?
> a) To index multiple columns for faster multi-condition queries
> b) To replace multiple single-column indexes
> c) To save disk space
> d) To enforce uniqueness
>> [!success]- Answer
>> a) To index multiple columns for faster multi-condition queries

> [!question] How does a bitmap scan work in PostgreSQL?
> a) Scans a single bitmap index
> b) Converts index entries to a bitmap then fetches pages
> c) Scans the entire table
> d) Uses a hash table
>> [!success]- Answer
>> b) Converts index entries to a bitmap then fetches pages

> [!question] What is a parallel query execution plan?
> a) A plan that uses multiple threads to execute parts of the query
> b) A plan that runs queries on multiple databases
> c) A plan that executes queries simultaneously
> d) A plan that uses parallel indexes
>> [!success]- Answer
>> a) A plan that uses multiple threads to execute parts of the query

> [!question] Which optimization rule transforms a WHERE clause condition to push filters closer to data?
> a) Commutativity of joins
> b) Selection pushdown
> c) View expansion
> d) Subquery flattening
>> [!success]- Answer
>> b) Selection pushdown

> [!question] Match the index type with its storage structure.
>> [!example] Group A
>> a) B+ tree
>> b) Hash index
>> c) Bitmap index
>> d) GiST index
>
>> [!example] Group B
>> n) Bit arrays per distinct value
>> o) Balanced tree with sorted keys
>> p) Generalized search tree
>> q) Buckets with hash codes
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the query optimization technique with its description.
>> [!example] Group A
>> a) Predicate pushdown
>> b) Join reordering
>> c) Subquery flattening
>> d) View merging
>
>> [!example] Group B
>> n) Combine view queries with outer query
>> o) Change join execution order
>> p) Move WHERE conditions closer to data
>> q) Convert subqueries to joins or semi-joins
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the database statistic with its role.
>> [!example] Group A
>> a) reltuples
>> b) relpages
>> c) n_distinct
>> d) correlation
>
>> [!example] Group B
>> n) Physical ordering correlation
>> o) Number of pages occupied
>> p) Estimated number of rows
>> q) Number of distinct values
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the access path with its cost characteristic.
>> [!example] Group A
>> a) Full table scan
>> b) Unique index scan
>> c) Range index scan
>> d) Bitmap scan
>
>> [!example] Group B
>> n) I/O proportional to table pages
>> o) I/O proportional to index height + one data page
>> p) I/O proportional to number of matching pages
>> q) I/O proportional to bitmap size plus fetch
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the optimizer approach with its method.
>> [!example] Group A
>> a) Rule-based optimizer
>> b) Cost-based optimizer
>> c) Genetic optimizer
>> d) Heuristic optimizer
>
>> [!example] Group B
>> n) Uses evolutionary algorithms
>> o) Uses predefined transformation rules
>> p) Uses statistics and cost formulas
>> q) Uses simple best-practice rules
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the algebraic rewrite rule with its transformation.
>> [!example] Group A
>> a) σ(R × S) → R ⋈ S
>> b) σ(R ∪ S) → σ(R) ∪ σ(S)
>> c) π(R ⋈ S) → π(π(R) ⋈ π(S))
>> d) σ(π(R)) → π(σ(R))
>
>> [!example] Group B
>> n) Push selection through projection
>> o) Convert Cartesian product with predicate to join
>> p) Push projection through join
>> q) Push selection through union
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the join ordering strategy with its approach.
>> [!example] Group A
>> a) Left-deep tree
>> b) Right-deep tree
>> c) Bushy tree
>> d) Zigzag tree
>
>> [!example] Group B
>> n) Inner relations are always base tables
>> o) No restriction on join shape
>> p) Non-standard tree shape
>> q) Outer relations are always base tables
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the cardinality estimation method with its technique.
>> [!example] Group A
>> a) Uniformity assumption
>> b) Independence assumption
>> c) Histogram-based
>> d) Sampling-based
>
>> [!example] Group B
>> n) Assumes column values are unrelated
>> o) Uses value distribution buckets
>> p) Assumes uniform value distribution
>> q) Estimates using a subset of data
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)
"""

# ============================================================
# CHAPTER 05 - QUIZ 1
# ============================================================
QUIZ_CONTENT['Chapter_05_1'] = """---
sources:
  - "[[01 PLSQL Basics]]"
  - "[[02 Functions and Stored Procedures]]"
  - "[[03 Stored Procedures and Functions]]"
  - "[[04 Exception Handling and Debugging]]"
---

> [!question] PL/SQL is a procedural extension of SQL used in Oracle databases.
>> [!success]- Answer
>> True

> [!question] A stored procedure must return a value.
>> [!success]- Answer
>> False

> [!question] A function in PL/SQL must return a value.
>> [!success]- Answer
>> True

> [!question] Variables in PL/SQL are declared in the DECLARE section.
>> [!success]- Answer
>> True

> [!question] Exception handling in PL/SQL uses the EXCEPTION block.
>> [!success]- Answer
>> True

> [!question] A cursor in PL/SQL is used to iterate over the result set of a query.
>> [!success]- Answer
>> True

> [!question] The INTO clause in PL/SQL stores the result of a SELECT in variables.
>> [!success]- Answer
>> True

> [!question] PL/SQL blocks cannot be nested inside other blocks.
>> [!success]- Answer
>> False

> [!question] The %TYPE attribute declares a variable with the same data type as a column.
>> [!success]- Answer
>> True

> [!question] An implicit cursor is created for each SQL statement in PL/SQL.
>> [!success]- Answer
>> True

> [!question] Which PL/SQL block is used to handle runtime errors?
> a) DECLARE
> b) BEGIN
> c) EXCEPTION
> d) END
>> [!success]- Answer
>> c) EXCEPTION

> [!question] What is the difference between a function and a procedure in PL/SQL?
> a) Functions cannot have parameters
> b) Procedures must return a value
> c) Functions must return a value, procedures may not
> d) There is no difference
>> [!success]- Answer
>> c) Functions must return a value, procedures may not

> [!question] Which cursor attribute returns TRUE if the cursor is open?
> a) %FOUND
> b) %NOTFOUND
> c) %ISOPEN
> d) %ROWCOUNT
>> [!success]- Answer
>> c) %ISOPEN

> [!question] What does the %ROWCOUNT cursor attribute return?
> a) The number of rows in the cursor
> b) The number of rows fetched so far
> c) The total rows returned by the query
> d) The number of columns
>> [!success]- Answer
>> b) The number of rows fetched so far

> [!question] Which statement is used to raise a user-defined exception?
> a) THROW
> b) RAISE
> c) RAISE_APPLICATION_ERROR
> d) Both b and c
>> [!success]- Answer
>> d) Both b and c

> [!question] What is the purpose of the COMMIT statement in PL/SQL?
> a) To save changes to the database
> b) To undo changes
> c) To close a cursor
> d) To declare a variable
>> [!success]- Answer
>> a) To save changes to the database

> [!question] How do you declare a cursor variable in PL/SQL?
> a) CURSOR cur_name IS SELECT ...
> b) DECLARE cur_name CURSOR
> c) cur_name AS CURSOR
> d) CURSOR FOR cur_name
>> [!success]- Answer
>> a) CURSOR cur_name IS SELECT ...

> [!question] Which loop is best for iterating through all rows of an explicit cursor?
> a) FOR loop
> b) WHILE loop
> c) Simple LOOP with EXIT
> d) REPEAT loop
>> [!success]- Answer
>> a) FOR loop

> [!question] What does the WHEN OTHERS clause handle?
> a) A specific named exception
> b) All exceptions not handled by other handlers
> c) Only system-generated errors
> d) Only user-defined errors
>> [!success]- Answer
>> b) All exceptions not handled by other handlers

> [!question] Which of the following is a predefined PL/SQL exception?
> a) NO_DATA_FOUND
> b) EOF
> c) NULL_POINTER
> d) STACK_OVERFLOW
>> [!success]- Answer
>> a) NO_DATA_FOUND

> [!question] Match the PL/SQL block section with its purpose.
>> [!example] Group A
>> a) DECLARE
>> b) BEGIN
>> c) EXCEPTION
>> d) END
>
>> [!example] Group B
>> n) Error handling code
>> o) Executable statements
>> p) Variable declarations
>> q) Block terminator
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the variable attribute with its description.
>> [!example] Group A
>> a) %TYPE
>> b) %ROWTYPE
>> c) RECORD type
>> d) TABLE type
>
>> [!example] Group B
>> n) Declares a collection
>> o) Declares a composite variable with custom fields
>> p) Inherits column type
>> q) Inherits row structure
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the cursor operation with its statement.
>> [!example] Group A
>> a) Open cursor
>> b) Fetch from cursor
>> c) Close cursor
>> d) Check cursor status
>
>> [!example] Group B
>> n) CLOSE
>> o) OPEN
>> p) %FOUND, %NOTFOUND
>> q) FETCH ... INTO
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the parameter mode with its behavior.
>> [!example] Group A
>> a) IN
>> b) OUT
>> c) IN OUT
>> d) DEFAULT
>
>> [!example] Group B
>> n) Read and write
>> o) Read-only
>> p) Default parameter value
>> q) Write-only
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the exception type with its source.
>> [!example] Group A
>> a) Predefined exception
>> b) User-defined exception
>> c) System exception
>> d) Pragma exception_init
>
>> [!example] Group B
>> n) Raised by the runtime environment
>> o) Defined in STANDARD package
>> p) Associates error number with a named exception
>> q) Defined by the programmer
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the DML statement with its PL/SQL usage.
>> [!example] Group A
>> a) INSERT
>> b) UPDATE
>> c) DELETE
>> d) SELECT ... INTO
>
>> [!example] Group B
>> n) Modifies existing rows
>> o) Stores query result in variables
>> p) Adds new rows
>> q) Removes rows
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the loop construct with its syntax.
>> [!example] Group A
>> a) Basic LOOP
>> b) WHILE LOOP
>> c) FOR LOOP
>> d) Cursor FOR LOOP
>
>> [!example] Group B
>> n) FOR i IN 1..n LOOP
>> o) LOOP ... EXIT WHEN ... END LOOP
>> p) FOR rec IN cursor LOOP
>> q) WHILE condition LOOP
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the conditional statement with its syntax.
>> [!example] Group A
>> a) IF-THEN
>> b) IF-THEN-ELSE
>> c) IF-THEN-ELSIF
>> d) CASE
>
>> [!example] Group B
>> n) Single condition, two branches
>> o) Multiple conditions
>> p) Simple condition, one branch
>> q) Multi-way branch using expression
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the transaction control statement with its effect.
>> [!example] Group A
>> a) COMMIT
>> b) ROLLBACK
>> c) SAVEPOINT
>> d) SET TRANSACTION
>
>> [!example] Group B
>> n) Marks a point for partial rollback
>> o) Configures transaction properties
>> p) Undoes the current transaction
>> q) Makes changes permanent
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> o)
"""

# ============================================================
# CHAPTER 05 - QUIZ 2
# ============================================================
QUIZ_CONTENT['Chapter_05_2'] = """---
sources:
  - "[[05 Advanced Cursors and Dynamic SQL]]"
  - "[[06 Procedural Control Structures and Handlers]]"
  - "[[07 Delimiters and Procedural Parsing Mechanics]]"
---

> [!question] Dynamic SQL allows constructing and executing SQL statements at runtime.
>> [!success]- Answer
>> True

> [!question] The EXECUTE IMMEDIATE statement executes dynamically constructed SQL.
>> [!success]- Answer
>> True

> [!question] A REF CURSOR is a cursor variable that can be opened for different queries.
>> [!success]- Answer
>> True

> [!question] Bind variables in dynamic SQL help prevent SQL injection.
>> [!success]- Answer
>> True

> [!question] A cursor with the FOR UPDATE clause locks the selected rows.
>> [!success]- Answer
>> True

> [!question] The WHERE CURRENT OF clause updates or deletes the current cursor row.
>> [!success]- Answer
>> True

> [!question] Delimiters in PL/SQL define the boundaries of procedural code blocks.
>> [!success]- Answer
>> True

> [!question] A function declared with DETERMINISTIC always returns the same result for the same input.
>> [!success]- Answer
>> True

> [!question] Pipelined table functions return rows incrementally as they are produced.
>> [!success]- Answer
>> True

> [!question] A trigger cannot use dynamic SQL in some database systems.
>> [!success]- Answer
>> True

> [!question] What is a REF CURSOR?
> a) A static cursor
> b) A cursor variable that can point to different result sets
> c) A cursor that references another cursor
> d) A read-only cursor
>> [!success]- Answer
>> b) A cursor variable that can point to different result sets

> [!question] What is the main advantage of using bind variables in dynamic SQL?
> a) Faster query parsing
> b) Prevention of SQL injection
> c) Better readability
> d) Support for DDL
>> [!success]- Answer
>> b) Prevention of SQL injection

> [!question] Which clause locks the rows selected by a cursor for update?
> a) FOR UPDATE
> b) FOR LOCK
> c) WITH LOCK
> d) LOCK ROW
>> [!success]- Answer
>> a) FOR UPDATE

> [!question] What does the WHERE CURRENT OF clause do?
> a) Selects the current row in a result set
> b) Updates or deletes the current row of an explicit cursor
> c) Moves the cursor to a specific position
> d) Opens a cursor at a specific position
>> [!success]- Answer
>> b) Updates or deletes the current row of an explicit cursor

> [!question] What is a pipelined table function?
> a) A function that returns a collection
> b) A function that returns rows incrementally without waiting for the entire result
> c) A function that processes data in a pipeline
> d) A function that executes in parallel
>> [!success]- Answer
>> b) A function that returns rows incrementally without waiting for the entire result

> [!question] Which statement is used to parse dynamic SQL without executing it?
> a) EXECUTE IMMEDIATE
> b) DBMS_SQL.PARSE
> c) PREPARE
> d) COMPILE
>> [!success]- Answer
>> b) DBMS_SQL.PARSE

> [!question] What does the PRAGMA AUTONOMOUS_TRANSACTION do?
> a) Makes a transaction dependent on the main transaction
> b) Creates an independent transaction within a main transaction
> c) Disables transactions
> d) Enforces serializable isolation
>> [!success]- Answer
>> b) Creates an independent transaction within a main transaction

> [!question] Which of the following is a valid cursor attribute?
> a) %ISOPEN
> b) %FOUND
> c) %NOTFOUND
> d) All of the above
>> [!success]- Answer
>> d) All of the above

> [!question] What is a collection type in PL/SQL?
> a) A single variable
> b) A data type that holds multiple values, like an array
> c) A cursor
> d) A table
>> [!success]- Answer
>> b) A data type that holds multiple values, like an array

> [!question] What does the BULK COLLECT clause do?
> a) Collects data in bulk
> b) Fetches multiple rows into a collection at once
> c) Collects garbage
> d) Groups rows for aggregation
>> [!success]- Answer
>> b) Fetches multiple rows into a collection at once

> [!question] Match the cursor type with its characteristic.
>> [!example] Group A
>> a) Implicit cursor
>> b) Explicit cursor
>> c) REF CURSOR
>> d) Cursor variable
>
>> [!example] Group B
>> n) Dynamically assignable to different queries
>> o) Another name for REF CURSOR
>> p) Automatically created for DML
>> q) Explicitly declared and managed
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the dynamic SQL method with its description.
>> [!example] Group A
>> a) EXECUTE IMMEDIATE
>> b) DBMS_SQL package
>> c) Native dynamic SQL
>> d) Bind variables
>
>> [!example] Group B
>> n) Alternative dynamic SQL approach
>> o) Simplest dynamic SQL method
>> p) Placeholders for runtime values
>> q) SQL with EXECUTE IMMEDIATE syntax
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the collection type with its property.
>> [!example] Group A
>> a) Associative array
>> b) Nested table
>> c) VARRAY
>> d) PL/SQL table
>
>> [!example] Group B
>> n) Variable-size array with max size
>> o) Key-value pairs
>> p) Old name for associative array
>> q) Unordered set of elements
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the bulk operation with its description.
>> [!example] Group A
>> a) BULK COLLECT
>> b) FORALL
>> c) SAVE EXCEPTIONS
>> d) LIMIT clause
>
>> [!example] Group B
>> n) Binds collection to DML in bulk
>> o) Restricts number of rows per bulk fetch
>> p) Continues despite errors
>> q) Fetches multiple rows at once
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> p)
>> d) -> o)

> [!question] Match the PRAGMA with its purpose.
>> [!example] Group A
>> a) EXCEPTION_INIT
>> b) AUTONOMOUS_TRANSACTION
>> c) SERIALLY_REUSABLE
>> d) RESTRICT_REFERENCES
>
>> [!example] Group B
>> n) Creates independent transaction
>> o) Associates error code with exception name
>> p) Controls purity level of functions
>> q) Saves package state between calls
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the PL/SQL optimization with its technique.
>> [!example] Group A
>> a) Native compilation
>> b) Bulk binding
>> c) Pipelining
>> d) Inlining
>
>> [!example] Group B
>> n) Row-by-row processing elimination
>> o) Replaces function call with body
>> p) Compiles to machine code
>> q) Streams result rows
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the delimiter with its PL/SQL purpose.
>> [!example] Group A
>> a) /
>> b) ;
>> c) BEGIN ... END
>> d) << >>
>
>> [!example] Group B
>> n) Label for nested blocks
>> o) Statement terminator
>> p) Block delimiters
>> q) PL/SQL block terminator
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> p)
>> d) -> n)

> [!question] Match the exception handling concept with its definition.
>> [!example] Group A
>> a) Exception propagation
>> b) Exception scope
>> c) Unhandled exception
>> d) SQLCODE
>
>> [!example] Group B
>> n) Returns the error code
>> o) Moves to outer block
>> p) Terminates execution
>> q) Where exception is active
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the cursor attribute with its return type.
>> [!example] Group A
>> a) %FOUND
>> b) %NOTFOUND
>> c) %ROWCOUNT
>> d) %ISOPEN
>
>> [!example] Group B
>> n) Integer
>> o) Boolean (TRUE if rows remain)
>> p) Boolean (TRUE if no rows remain)
>> q) Boolean (TRUE if cursor is open)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)
"""

# ============================================================
# CHAPTER 06 - QUIZ 1
# ============================================================
QUIZ_CONTENT['Chapter_06_1'] = """---
sources:
  - "[[Source TD N1 BDA Rappel SQL]]"
  - "[[Source TD N2 BDA Gestion des Ventes]]"
  - "[[Source TD N3 BDA Contraintes d'intégrité, Vue et Contrôle de données]]"
---

> [!question] An SQL query using GROUP BY must include all non-aggregated columns from the SELECT clause.
>> [!success]- Answer
>> True

> [!question] A LEFT JOIN returns all rows from the left table, even if there is no match in the right table.
>> [!success]- Answer
>> True

> [!question] The HAVING clause can reference columns not in the SELECT list.
>> [!success]- Answer
>> False

> [!question] A correlated subquery is evaluated once for each row of the outer query.
>> [!success]- Answer
>> True

> [!question] The COALESCE function returns NULL if all its arguments are NULL.
>> [!success]- Answer
>> True

> [!question] An index can be created on a view in all database systems.
>> [!success]- Answer
>> False

> [!question] The DISTINCT keyword can be used with aggregate functions like COUNT.
>> [!success]- Answer
>> True

> [!question] A NULL value in SQL is equal to another NULL value.
>> [!success]- Answer
>> False

> [!question] The UNION operator automatically removes duplicate rows from the result set.
>> [!success]- Answer
>> True

> [!question] SQL constraints can be added after a table is created using ALTER TABLE.
>> [!success]- Answer
>> True

> [!question] Which SQL operator tests for membership in a list or subquery?
> a) BETWEEN
> b) LIKE
> c) IN
> d) EXISTS
>> [!success]- Answer
>> c) IN

> [!question] What is the result of NULL = NULL in SQL?
> a) TRUE
> b) FALSE
> c) UNKNOWN
> d) NULL
>> [!success]- Answer
>> c) UNKNOWN

> [!question] Which clause is used to sort the result set of a query?
> a) GROUP BY
> b) HAVING
> c) ORDER BY
> d) SORT BY
>> [!success]- Answer
>> c) ORDER BY

> [!question] What is the purpose of the CASE expression in SQL?
> a) To handle exceptions
> b) To perform conditional logic within a query
> c) To create a new table
> d) To define a variable
>> [!success]- Answer
>> b) To perform conditional logic within a query

> [!question] Which of the following is NOT a valid aggregate function?
> a) MAX
> b) MIN
> c) MEDIAN
> d) MODE
>> [!success]- Answer
>> d) MODE

> [!question] What does the EXCEPT operator do in SQL?
> a) Returns rows from the first query that are not in the second
> b) Returns rows common to both queries
> c) Returns all rows from both queries
> d) Returns rows from the second query not in the first
>> [!success]- Answer
>> a) Returns rows from the first query that are not in the second

> [!question] Which join type returns the Cartesian product of two tables?
> a) INNER JOIN
> b) LEFT JOIN
> c) CROSS JOIN
> d) NATURAL JOIN
>> [!success]- Answer
>> c) CROSS JOIN

> [!question] What is the purpose of the WITH clause (CTE)?
> a) To create a temporary table
> b) To define a named subquery that can be referenced multiple times
> c) To join tables
> d) To create indexes
>> [!success]- Answer
>> b) To define a named subquery that can be referenced multiple times

> [!question] Which function returns the number of characters in a string?
> a) LENGTH
> b) COUNT
> c) SIZE
> d) CHAR_LENGTH
>> [!success]- Answer
>> a) LENGTH

> [!question] What does the OVER clause do in SQL window functions?
> a) Defines the partition and ordering of rows for the function
> b) Overrides default settings
> c) Creates a new view
> d) Joins two tables
>> [!success]- Answer
>> a) Defines the partition and ordering of rows for the function

> [!question] Match the SQL join with its Venn diagram region.
>> [!example] Group A
>> a) INNER JOIN
>> b) LEFT JOIN
>> c) RIGHT JOIN
>> d) FULL OUTER JOIN
>
>> [!example] Group B
>> n) Right circle plus intersection
>> o) Intersection only
>> p) Left circle plus intersection
>> q) Both circles entirely
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the aggregate function with its purpose.
>> [!example] Group A
>> a) COUNT
>> b) SUM
>> c) AVG
>> d) MAX
>
>> [!example] Group B
>> n) Total of numeric values
>> p) Number of rows
>> q) Largest value
>> r) Arithmetic mean
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> r)
>> d) -> q)

> [!question] Match the string function with its behavior.
>> [!example] Group A
>> a) CONCAT
>> b) SUBSTRING
>> c) UPPER
>> d) TRIM
>
>> [!example] Group B
>> n) Removes leading/trailing spaces
>> o) Extracts part of a string
>> p) Combines strings
>> q) Converts to uppercase
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the date function with its description.
>> [!example] Group A
>> a) EXTRACT
>> b) DATEADD
>> c) DATEDIFF
>> d) GETDATE
>
>> [!example] Group B
>> n) Returns current date and time
>> o) Calculates difference between dates
>> p) Adds to a date
>> q) Retrieves a date part
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the subquery type with its return value.
>> [!example] Group A
>> a) Scalar subquery
>> b) Row subquery
>> c) Column subquery
>> d) Table subquery
>
>> [!example] Group B
>> n) Multiple rows, single column
>> o) Single row, single column
>> p) Multiple rows, multiple columns
>> q) Single row, multiple columns
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the constraint type with its enforcement.
>> [!example] Group A
>> a) Column constraint
>> b) Table constraint
>> c) Referential integrity
>> d) Domain integrity
>
>> [!example] Group B
>> n) Validates column data types and ranges
>> o) Defined inline with a column
>> p) Defined separately from column
>> q) Ensures FK matches PK
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the data type category with an example.
>> [!example] Group A
>> a) Numeric
>> b) Character
>> c) Date/Time
>> d) Binary
>
>> [!example] Group B
>> n) TIMESTAMP
>> o) BLOB
>> p) VARCHAR
>> q) DECIMAL
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> o)

> [!question] Match the SQL clause with its logical processing order.
>> [!example] Group A
>> a) FROM
>> b) WHERE
>> c) GROUP BY
>> d) SELECT
>
>> [!example] Group B
>> n) Third
>> o) Fourth
>> p) First
>> q) Second
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the DML operation with its SQL statement.
>> [!example] Group A
>> a) Create
>> b) Read
>> c) Update
>> d) Delete
>
>> [!example] Group B
>> n) DELETE
>> o) INSERT
>> p) SELECT
>> q) UPDATE
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)
"""

# ============================================================
# CHAPTER 06 - QUIZ 2
# ============================================================
QUIZ_CONTENT['Chapter_06_2'] = """---
sources:
  - "[[Source TD N4 - Optimisation de requêtes]]"
  - "[[Source TD N4 MySQL Procédural (The Airline Database).]]"
  - "[[Source TD N5 - Transactions, Concurrence et Récupération]]"
  - "[[Source TD Modèle Entité Association (Conceptual Design)]]"
---

> [!question] An entity-relationship diagram (ERD) is a conceptual modeling tool for databases.
>> [!success]- Answer
>> True

> [!question] In a many-to-many relationship, a junction table is typically required.
>> [!success]- Answer
>> True

> [!question] A weak entity does not have its own primary key and depends on a strong entity.
>> [!success]- Answer
>> True

> [!question] Transaction isolation levels can be set per session in most database systems.
>> [!success]- Answer
>> True

> [!question] The GRANT statement is used to assign privileges to database users.
>> [!success]- Answer
>> True

> [!question] A cursor in MySQL procedural code is read-only and non-scrollable by default.
>> [!success]- Answer
>> True

> [!question] An index can significantly improve the performance of SELECT queries but may slow down INSERT operations.
>> [!success]- Answer
>> True

> [!question] A normalized database always stores data in fewer tables than a denormalized one.
>> [!success]- Answer
>> False

> [!question] The REVOKE statement removes previously granted privileges.
>> [!success]- Answer
>> True

> [!question] A primary key can be composed of multiple columns.
>> [!success]- Answer
>> True

> [!question] What is the purpose of normalization in database design?
> a) To increase data redundancy
> b) To eliminate data redundancy and ensure data integrity
> c) To speed up queries
> d) To create more tables
>> [!success]- Answer
>> b) To eliminate data redundancy and ensure data integrity

> [!question] Which normal form eliminates transitive dependencies?
> a) 1NF
> b) 2NF
> c) 3NF
> d) BCNF
>> [!success]- Answer
>> c) 3NF

> [!question] What is a functional dependency?
> a) A relationship between two tables
> b) A constraint that determines one attribute based on another
> c) A type of index
> d) A join condition
>> [!success]- Answer
>> b) A constraint that determines one attribute based on another

> [!question] Which of the following is NOT a valid transaction isolation level?
> a) READ UNCOMMITTED
> b) READ COMMITTED
> c) REPEATABLE WRITE
> d) SERIALIZABLE
>> [!success]- Answer
>> c) REPEATABLE WRITE

> [!question] What does the term "entity integrity" refer to?
> a) No NULL values in foreign keys
> b) No duplicate or NULL values in primary keys
> c) All columns must have values
> d) Tables must be normalized
>> [!success]- Answer
>> b) No duplicate or NULL values in primary keys

> [!question] In the context of database optimization, what is an index?
> a) A table constraint
> b) A data structure that speeds up data retrieval
> c) A type of join
> d) A stored procedure
>> [!success]- Answer
>> b) A data structure that speeds up data retrieval

> [!question] What is referential integrity?
> a) All foreign key values must match a primary key or be NULL
> b) All tables must have primary keys
> c) Columns must have appropriate data types
> d) Tables must be in third normal form
>> [!success]- Answer
>> a) All foreign key values must match a primary key or be NULL

> [!question] Which MySQL storage engine supports transactions?
> a) MyISAM
> b) InnoDB
> c) MEMORY
> d) ARCHIVE
>> [!success]- Answer
>> b) InnoDB

> [!question] What is the purpose of the DENY statement in SQL Server?
> a) To grant permissions
> b) To revoke permissions
> c) To explicitly prevent a user or role from accessing a securable
> d) To create a user
>> [!success]- Answer
>> c) To explicitly prevent a user or role from accessing a securable

> [!question] Which type of database relationship is represented by a foreign key in a child table referencing a primary key in a parent table?
> a) One-to-one
> b) One-to-many
> c) Many-to-many
> d) Self-referencing
>> [!success]- Answer
>> b) One-to-many

> [!question] Match the normal form with its requirement.
>> [!example] Group A
>> a) 1NF
>> b) 2NF
>> c) 3NF
>> d) BCNF
>
>> [!example] Group B
>> n) Every determinant is a candidate key
>> o) No partial dependencies
>> p) No transitive dependencies
>> q) Atomic columns
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> p)
>> d) -> n)

> [!question] Match the ERD component with its symbol.
>> [!example] Group A
>> a) Entity
>> b) Attribute
>> c) Relationship
>> d) Weak entity
>
>> [!example] Group B
>> n) Diamond shape
>> p) Double rectangle
>> q) Rectangle
>> r) Ellipse
>
>> [!success]- Answer
>> a) -> q)
>> b) -> r)
>> c) -> n)
>> d) -> p)

> [!question] Match the cardinality with its meaning.
>> [!example] Group A
>> a) 1:1
>> b) 1:N
>> c) M:N
>> d) 1:0..N
>
>> [!example] Group B
>> n) Many-to-many
>> p) Zero or many
>> q) One-to-many
>> r) One-to-one
>
>> [!success]- Answer
>> a) -> r)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the optimization technique with its description.
>> [!example] Group A
>> a) Query rewriting
>> b) Indexing strategy
>> c) Denormalization
>> d) Partitioning
>
>> [!example] Group B
>> n) Combines tables to reduce joins
>> o) Splits tables across multiple files
>> p) Restructuring queries for efficiency
>> q) Creating appropriate indexes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the security statement with its purpose.
>> [!example] Group A
>> a) GRANT
>> b) REVOKE
>> c) DENY
>> d) CREATE USER
>
>> [!example] Group B
>> n) Removes a permission
>> o) Creates a database account
>> p) Explicitly blocks access
>> q) Assigns a permission
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> p)
>> d) -> o)

> [!question] Match the database object with its description.
>> [!example] Group A
>> a) View
>> b) Index
>> c) Synonym
>> d) Sequence
>
>> [!example] Group B
>> n) Generates unique numbers
>> o) Virtual table based on a query
>> p) Alias for a database object
>> q) Speeds up data access
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the transaction property with the concurrency anomaly it prevents.
>> [!example] Group A
>> a) Atomicity
>> b) Consistency
>> c) Isolation
>> d) Durability
>
>> [!example] Group B
>> n) No partial updates visible
>> o) Data survives crashes
>> p) Prevents concurrency anomalies
>> q) No constraint violations
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> p)
>> d) -> o)

> [!question] Match the MySQL procedural element with its syntax.
>> [!example] Group A
>> a) Stored procedure
>> b) Function
>> c) Trigger
>> d) Event
>
>> [!example] Group B
>> n) CREATE TRIGGER ...
>> o) CREATE EVENT ...
>> p) CREATE PROCEDURE ...
>> q) CREATE FUNCTION ...
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)
"""


def generate_files():
    """Generate all quiz files."""
    chapters = ['Chapter_01', 'Chapter_02', 'Chapter_03', 'Chapter_04', 'Chapter_05', 'Chapter_06']
    
    for ch in chapters:
        dir_path = os.path.join(QUIZ_DIR, ch)
        os.makedirs(dir_path, exist_ok=True)
        
        for quiz_num in [1, 2]:
            key = f"{ch}_{quiz_num}"
            content = QUIZ_CONTENT.get(key)
            if not content:
                print(f"WARNING: No content for {key}")
                continue
            
            filepath = os.path.join(dir_path, f'Q{quiz_num}.md')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.lstrip('\n'))
            print(f"  Created: {filepath}")
    
    print(f"\nGenerated {len(chapters) * 2} quiz files across {len(chapters)} chapters.")


if __name__ == '__main__':
    generate_files()