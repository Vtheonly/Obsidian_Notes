# Procedural SQL (SQL/PSM & PL/pgSQL), Control Flow & Exceptions

This note integrates **Chapter 2 Part II (Slides 16–33)**, **TP 2 (Part II.4–7, Exercises 4–7, Part IV Q12–14)**, **TD 2 (Exercises 3*, 4, 6, 7*, 8)**, and foundational procedural SQL mechanics (delimiters, variable scoping, control flow, and exception handling across **ISO SQL/PSM**, **PostgreSQL PL/pgSQL**, **MySQL**, and **Oracle PL/SQL**).

---

## 1. Declarative SQL vs. Procedural Programming (Ch 2 Slides 16–18)

Plain SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) is **declarative**: you specify *what* data you want, and the optimizer decides *how* to fetch it. While inline `CASE` expressions exist inside queries, plain SQL **cannot** express loops, program-flow `IF/ELSE` branching, local state variables, custom error recovery, or multi-step server algorithms.

**Why move from Views to Server-Side Programming?** Views only *present* data; when the university requires *"Every salary increase must be controlled, calculated according to a rate, and automatically recorded in a history"*, we need server-side **procedural SQL** running inside the DBMS engine (avoiding client round-trips):
1. **ISO/IEC SQL/PSM (SQL Persistent Stored Modules):** Standardized procedural SQL taught in lectures and conceptual TDs (**Ch 2, TD 2, TD 3**).
2. **PL/pgSQL:** **PostgreSQL's** procedural language used in labs (**TP 2, TP 3, pgAdmin 4**).
3. **Oracle PL/SQL & MySQL Procedural SQL:** Vendor dialects encountered in historical BDA exams and TD 4 (**PL/SQL** is Oracle-exclusive, Ada-style with packages; **MySQL** has its own procedural SQL/PSM-like dialect—never confuse the two!).

---

## 2. Dialect Comparison & Delimiter Parsing Mechanics (TD 2 Ex 6)

Because **TD 2 Ex 6** specifically asks *"which parts of the syntax may depend on the DBMS"*, compare all four dialects side-by-side:

| Feature | ISO SQL/PSM (Lectures / TD 2–3) | PostgreSQL PL/pgSQL (TP 2–3 / pgAdmin) | MySQL Procedural (TD 4 / Legacy) | Oracle PL/SQL (Legacy) |
| :--- | :--- | :--- | :--- | :--- |
| **Anonymous Block** | `BEGIN ATOMIC ... END` | `DO $$ DECLARE ... BEGIN ... END $$;` | Inside `CREATE PROCEDURE` | `DECLARE ... BEGIN ... END; /` |
| **Assignment** | `SET v = val;` | `v := val;` (also `=`) | `SET v = val;` | `v := val;` |
| **Conditionals** | `IF ... ELSEIF ... ELSE ... END IF;` | `IF ... ELSIF ... ELSE ... END IF;` | `IF ... ELSEIF ... ELSE ... END IF;` | `IF ... ELSIF ... ELSE ... END IF;` |
| **Output / Print** | `SELECT v;` | `RAISE NOTICE 'Msg: %', v;` | `SELECT v;` | `DBMS_OUTPUT.PUT_LINE(v);` |
| **Missing Row** | `DECLARE CONTINUE HANDLER FOR NOT FOUND ...` | `IF NOT FOUND` (or `SELECT INTO STRICT` $\to$ `no_data_found`) | `DECLARE CONTINUE HANDLER FOR NOT FOUND ...` | `EXCEPTION WHEN NO_DATA_FOUND` |
| **Error Handler** | `DECLARE EXIT HANDLER FOR SQL EXCEPTION ...` | `BEGIN ... EXCEPTION WHEN division_by_zero THEN ... WHEN OTHERS THEN ... SQLERRM ... END;` | `DECLARE EXIT\|CONTINUE HANDLER FOR SQLEXCEPTION ...` | `EXCEPTION WHEN ZERO_DIVIDE THEN ... WHEN OTHERS THEN ...` |
| **Raise Error** | `SIGNAL SQLSTATE ...` | `RAISE EXCEPTION 'msg';` | `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...';` | `RAISE_APPLICATION_ERROR(-20001, '...');` |

### Why Delimiters Matter (`DELIMITER //` in MySQL vs. `$$` Dollar-Quoting in PostgreSQL)
In interactive clients, `;` terminates a single SQL statement. Inside a procedure/function, multiple internal statements end with `;`:
- **MySQL CLI Conflict:** Sending `CREATE PROCEDURE ... BEGIN INSERT ...; UPDATE ...; END;` with `;` active causes the client to truncate at the first `;` and crash with syntax error `1064`. Therefore, MySQL scripts use the **client-side directive** `DELIMITER // ... END // DELIMITER ;` (note: `DELIMITER` is a client tool directive, not SQL!).
- **PostgreSQL Solution (`$$` Dollar-Quoting):** PostgreSQL wraps procedural bodies inside `AS $$ ... $$;` (or `DO $$ ... $$;`), so internal `;` characters and single quotes `'...'` inside the body need no escaping or client delimiter switches!

---

## 3. Variables, Scopes & `SELECT ... INTO` Mechanics

### PostgreSQL Variables (TP 2 Part II.4 & TP 3)
- Declared between `DECLARE` and `BEGIN` inside `DO $$ ... $$;` or a function/procedure.
- **Anchored type (`%TYPE`):** `v_salary teacher.salary%TYPE;` automatically inherits the column's exact type (`NUMERIC(10,2)`), remaining resilient if the column schema widens later.
- **Generic row (`RECORD`):** `rec RECORD;` holds any row structure dynamically (used in cursor `FOR` loops).
- **`SELECT ... INTO` Rules:**
  - In PostgreSQL PL/pgSQL, `SELECT salary INTO v_salary FROM teacher WHERE teacher_id = 101;` stores the retrieved column into `v_salary` and updates the automatic boolean **`FOUND`** (`TRUE` if $\ge 1$ row, `FALSE` if 0 rows).
  - Without `STRICT`, 0 rows leaves `v_salary = NULL` and sets `FOUND = FALSE`; multiple rows assign only the first row unless `STRICT` is specified (`SELECT ... INTO STRICT` enforces exactly 1 row, raising `no_data_found` or `too_many_rows`!).
  - *(In MySQL/Oracle, `SELECT ... INTO` returning 0 rows raises `NOT FOUND` / `NO_DATA_FOUND`, and >1 row raises `TOO_MANY_ROWS` `21000`.)*

### Legacy MySQL Variable Scopes (For Reading TD 4 & Past Exams)
| Scope | Syntax | Lifespan | Typing |
| :--- | :--- | :--- | :--- |
| **Local Variable** | `DECLARE v INT DEFAULT 0;` | Current `BEGIN...END` block only (stack-allocated) | Strongly & statically typed |
| **Session Variable** | `SET @v = 10;` | Entire connection session (no `DECLARE` needed) | Weakly & dynamically typed |
| **System Variable** | `@@GLOBAL.var` / `@@SESSION.var` | Server/session configuration | Strongly typed |

---

## 4. Conditionals, `NULL` vs. Missing Row & Loops (TP 2 Ex 4–6, TD 2 Ex 3*–4)

### Critical Rules for `IF / ELSIF`, `CASE`, `NULL`, and `FOUND` (TP 2 Part II.5 & Ex 4–5)
1. **PL/pgSQL spelling:** Always write **`ELSIF`** (never `ELSE IF` or `ELSEIF`!).
2. **Test `IS NULL` explicitly:** Because `NULL >= 70000` evaluates to `UNKNOWN` (not `TRUE`), omitting `IS NULL` lets `NULL` fall silently into the `ELSE` branch (`'Low'`)!
3. **Distinguish a `NULL` attribute from a missing row (TP 2 Ex 4 & TD 2 Ex 4):**
   - Teacher `109` (`Khelifi Nora`) **exists** with `salary = NULL` (`FOUND = TRUE`, `v_salary IS NULL`).
   - Teacher `999` **does not exist** (`FOUND = FALSE`). Treating these identically corrupts reports or hides data-integrity gaps.
4. **Check `FOUND` immediately (TP 2 Ex 5 Correction Note):** Check `IF NOT FOUND` **immediately after `SELECT INTO`**, before any other SQL statement overwrites `FOUND`!

```sql
-- TP 2 Ex 4 & 5: Robust classification (IF/ELSIF and CASE)
DO $$
DECLARE
    v_salary NUMERIC(10,2);
    v_category VARCHAR(20);
BEGIN
    SELECT salary INTO v_salary FROM teacher WHERE teacher_id = 109;

    IF NOT FOUND THEN
        v_category := 'Teacher not found';
    ELSIF v_salary IS NULL THEN
        v_category := 'Unknown';
    ELSIF v_salary >= 70000 THEN
        v_category := 'High';
    ELSIF v_salary >= 50000 THEN
        v_category := 'Medium';
    ELSE
        v_category := 'Low';
    END IF;

    RAISE NOTICE 'Salary: %, category: %', v_salary, v_category;
END $$;
```
*(In `CASE` expression form: `v_category := CASE WHEN NOT FOUND THEN 'Teacher not found' WHEN v_salary IS NULL THEN 'Unknown' WHEN v_salary >= 70000 THEN 'High' WHEN v_salary >= 50000 THEN 'Medium' ELSE 'Low' END;` — valid only when evaluated right after `SELECT INTO`.)*

### TD 2 Ex 4: Processing Students 1..10 & Handling `NULL` `class_id` vs. Non-Existent Student
```sql
DO $$
DECLARE
    i INTEGER;
    v_class_id student.class_id%TYPE;
BEGIN
    FOR i IN 1..10 LOOP
        SELECT class_id INTO v_class_id FROM student WHERE student_id = i;
        IF NOT FOUND THEN
            RAISE NOTICE 'Student % does not exist.', i;
        ELSIF v_class_id IS NULL THEN
            RAISE NOTICE 'Student % exists, but class_id is NULL (unassigned).', i;
        ELSE
            RAISE NOTICE 'Student % is in class %.', i, v_class_id;
        END IF;
    END LOOP;
END $$;
```
*Why they must not be treated as equivalent:* Student `8` (`Farah Ines`) is a valid enrolled student awaiting class assignment (`class_id IS NULL`), whereas ID `11` does not represent any student at all—treating both as "unassigned" or both as "missing" would either drop real students or fabricate nonexistent ones.

### Loop Constructs & `CONTINUE WHEN` (Ch 2 Slides 28–32, TP 2 Ex 6, TD 2 Ex 3*)
- **PostgreSQL PL/pgSQL:**
  - `FOR i IN 1..5 LOOP ... END LOOP;` (known integer range; `REVERSE` for descending).
  - `WHILE condition LOOP ... END LOOP;` (pre-tested; forgetting `i := i + 1;` causes an infinite loop!).
  - `LOOP ... EXIT WHEN condition; ... END LOOP;` (infinite until `EXIT` / `EXIT WHEN`).
  - `CONTINUE` / `CONTINUE WHEN cond;` skips to the next iteration—**always increment before `CONTINUE WHEN`** in `WHILE`/`LOOP`!
- **ISO SQL/PSM & MySQL additions:** `REPEAT ... UNTIL cond END REPEAT;` (post-tested—executes **at least once**!), `label: LOOP ... LEAVE label; ... ITERATE label; END LOOP;`.

```sql
-- TD 2 Ex 3* / TP 2 Ex 6 Task 1: Iterate department IDs 1..5 + skipping evens safely
DO $$
DECLARE i INTEGER := 0;
BEGIN
    WHILE i < 5 LOOP
        i := i + 1;
        CONTINUE WHEN i % 2 = 0; -- safe because increment already occurred!
        RAISE NOTICE 'Department ID (odd): %', i;
    END LOOP;
END $$;
```

---

## 5. Exception Handling, `NOT FOUND` Handlers & Validation (TP 2 Ex 7, TD 2 Ex 6–8)

### Why Handle Exceptions & How PostgreSQL Rolls Back Protected Blocks (TP 2 Part II.7)
Runtime errors arise from division by zero, constraint violations (`23000`/`23505`), missing data (`02000`), or business logic checks (`45000`).
> [!IMPORTANT] Crucial PostgreSQL `EXCEPTION` Rollback Rule (TP 2 Part II.7)
> In PL/pgSQL, a `BEGIN ... EXCEPTION ... END;` block creates an implicit subtransaction. **When an exception is caught, PostgreSQL rolls back all database changes made inside that protected block back to its entry state before executing the handler**, while allowing outer execution after `END;` to continue!
> Moreover, **specific handlers (`WHEN division_by_zero`) are strongly preferred over `WHEN OTHERS`** because catching everything can silently hide programming typos or unrelated constraint bugs.

### Worked Solutions: TP 2 Ex 7, TD 2 Ex 6, TD 2 Ex 7*, TD 2 Ex 8

**TP 2 Ex 7 / TD 2 Ex 6 — Division by Zero (PL/pgSQL vs. SQL/PSM):**
```sql
-- PostgreSQL PL/pgSQL (TP 2 Ex 7)
DO $$
DECLARE v_result NUMERIC;
BEGIN
    BEGIN
        v_result := 100 / 0; -- Change to 100 / 4 -> prints Result: 25
        RAISE NOTICE 'Result: %', v_result;
    EXCEPTION
        WHEN division_by_zero THEN
            RAISE NOTICE 'Error: division by zero is not allowed.';
        WHEN OTHERS THEN
            RAISE NOTICE 'Unexpected error: %', SQLERRM;
    END;
    RAISE NOTICE 'Execution continues after the handled inner block.';
END $$;
```
*(In ISO SQL/PSM, Ch 2 Slide 33 uses `DECLARE EXIT HANDLER FOR SQL EXCEPTION BEGIN ... END;` inside `BEGIN ATOMIC ... END;`, where block delimiters `BEGIN ATOMIC`, `DECLARE ... HANDLER`, `EXCEPTION WHEN`, `RAISE NOTICE`, and `SQLERRM` are all DBMS-dependent syntax elements!)*

**TD 2 Ex 7* — Handling Missing Student 100:**
- If student `100` exists, display their retrieved attributes normally; if not, emit an explicit not-found message/status rather than proceeding with `NULL`/uninitialized variables (explicit handling prevents silent garbage outputs or false updates).
```sql
-- ISO SQL/PSM style (TD 2 Ex 7*)
BEGIN ATOMIC
    DECLARE v_last_name VARCHAR(50);
    DECLARE v_first_name VARCHAR(50);
    DECLARE v_not_found BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_not_found = TRUE;

    SELECT last_name, first_name INTO v_last_name, v_first_name
    FROM student WHERE student_id = 100;

    IF v_not_found THEN
        SELECT 'Student 100 does not exist.' AS status;
    ELSE
        SELECT v_last_name, v_first_name;
    END IF;
END;
```
*(In PostgreSQL PL/pgSQL, either use `SELECT ... INTO` followed by `IF NOT FOUND THEN RAISE NOTICE ...` or `SELECT ... INTO STRICT` inside a `BEGIN ... EXCEPTION WHEN no_data_found THEN ... END;` block!)*

**TD 2 Ex 8 — Controlled 10% Salary Update for Teacher 101:**
Validate *before* executing `UPDATE` so invalid/NULL rows are never modified, error causes are clearly distinguished (`teacher missing` vs. `NULL salary`), and locks/audit triggers are never triggered on bad states:
```sql
DO $$
DECLARE v_salary teacher.salary%TYPE;
BEGIN
    SELECT salary INTO v_salary FROM teacher WHERE teacher_id = 101;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Update aborted: teacher 101 does not exist.';
    ELSIF v_salary IS NULL THEN
        RAISE EXCEPTION 'Update aborted: teacher 101 has a NULL salary.';
    ELSE
        UPDATE teacher SET salary = salary * 1.10 WHERE teacher_id = 101;
        RAISE NOTICE 'Teacher 101 salary increased by 10%%.';
    END IF;
END $$;
```
*(Wrap in `BEGIN; ... ROLLBACK;` in lab sessions to keep the TP 1 baseline intact.)*

### Legacy MySQL Error Codes (`SQLSTATE`) & Transaction Handler Pattern
Standardized `SQLSTATE` classes: `00000` (Success), `01000` (Warning/Truncation), `02000` (`NOT FOUND`), `23000` (Integrity constraint violation), `45000` (User-defined exception via `SIGNAL`). In MySQL procedures, declare variables $\to$ declare handlers (`DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET exit_flag = 1;`) $\to$ run `START TRANSACTION` $\to$ `IF exit_flag = 1 THEN ROLLBACK; ELSE COMMIT; END IF;` (or `RESIGNAL;` inside an `EXIT HANDLER` to log and rethrow).

---

## 6. Review Questions Summary (TP 2 Part IV Q12–Q14)
- **Q12 (`DO` block vs. Stored Function vs. Stored Procedure):** A `DO $$ ... $$;` block executes one-time anonymous procedural code without storing anything in the database; a **stored function** is saved permanently, returns a value, and can be embedded in `SELECT` expressions; a **stored procedure** is saved permanently, performs actions without requiring a return value, and is invoked with `CALL`.
- **Q13 (Why test `NULL` explicitly?):** Relational comparisons like `salary >= 70000` or `salary <> 50000` evaluate to `UNKNOWN` when `salary` is `NULL`, causing `IF`/`ELSIF` conditions to fall unexpectedly into `ELSE`. Always check `IS NULL` / `IS NOT NULL` (or `IS DISTINCT FROM`) first.
- **Q14 (`EXCEPTION`, `WHEN`, `RAISE NOTICE`, `RAISE EXCEPTION`):** `EXCEPTION` opens the error-handling section of a block; `WHEN` selects the specific SQLSTATE/condition to catch; `RAISE NOTICE` prints an informational message to the Messages tab without stopping execution; `RAISE EXCEPTION` deliberately triggers an error, aborting normal execution and rolling back the block unless caught by an enclosing handler.
