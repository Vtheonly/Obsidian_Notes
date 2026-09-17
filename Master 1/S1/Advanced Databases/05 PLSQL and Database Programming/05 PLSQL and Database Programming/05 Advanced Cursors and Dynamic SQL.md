# Advanced Cursors and Dynamic SQL

Standard SQL is "set-oriented"—it processes sets of rows. Procedural SQL introduces row-by-row logic where required. **Cursors** provide the bridge between these approaches.

## 1. Implicit vs. Explicit Cursors

### Implicit Cursors
The DBMS automatically uses an execution context for statements such as `INSERT`, `UPDATE`, `DELETE`, and single-row `SELECT ... INTO`. Procedural dialects expose status attributes differently; in Oracle, examples include:

* `SQL%FOUND`: the previous statement affected/found rows;
* `SQL%NOTFOUND`: no row was affected/found;
* `SQL%ROWCOUNT`: number of rows affected/fetched as defined by the dialect.

### Explicit Cursors
For a query that returns multiple rows and needs procedural row-by-row processing, define an explicit cursor.

1. **DECLARE:** Define the query.
2. **OPEN:** Execute/activate the cursor.
3. **FETCH:** Retrieve the next row into variables.
4. **CLOSE:** Release the cursor resources.

```sql
DECLARE
    CURSOR emp_cursor IS
        SELECT name, salary FROM employees WHERE dept = 'IT';
    v_name employees.name%TYPE;
    v_salary employees.salary%TYPE;
BEGIN
    OPEN emp_cursor;
    LOOP
        FETCH emp_cursor INTO v_name, v_salary;
        EXIT WHEN emp_cursor%NOTFOUND;
        -- Procedural logic
    END LOOP;
    CLOSE emp_cursor;
END;
```

MySQL-style cursors use a different syntax and normally pair `FETCH` with a `CONTINUE HANDLER FOR NOT FOUND` flag. Do not mix Oracle `%NOTFOUND` syntax with MySQL handler syntax in the same implementation.

## 2. Advanced Cursor Control (`FOR UPDATE`)

When a cursor iterates over rows that the procedure intends to update or delete, locking may be required to prevent concurrent modifications.

Oracle-style example:

```plsql
CURSOR salary_cursor IS
    SELECT id, salary
    FROM employees
    WHERE status = 'Active'
    FOR UPDATE;
```

Then the current row can be updated with:

```plsql
UPDATE employees
SET salary = salary * 1.10
WHERE CURRENT OF salary_cursor;
```

`FOR UPDATE` and `WHERE CURRENT OF` semantics are DBMS-specific. In MySQL stored programs, `WHERE CURRENT OF` is not available in the same form, so the common workaround is to fetch the row's primary key and issue `UPDATE ... WHERE primary_key = v_id` or `DELETE ... WHERE primary_key = v_id` while the cursor transaction holds the required locks.

## 3. Dynamic SQL

Static SQL names its schema objects at compile time. **Dynamic SQL** constructs a statement at runtime when identifiers or statement structure must vary.

### Oracle-style `EXECUTE IMMEDIATE`
```plsql
CREATE PROCEDURE update_salary (p_new_salary NUMBER, p_id NUMBER) IS
BEGIN
    EXECUTE IMMEDIATE
        'UPDATE employees SET salary = :1 WHERE id = :2'
        USING p_new_salary, p_id;
END;
```

### Identifier vs. Value Safety
Bind variables are designed for **values**, not arbitrary table or column names. A dynamic table name therefore requires identifier validation/quoting according to the DBMS rather than simple value binding.

For example, this is unsafe when `p_name` is untrusted input:

```text
'... WHERE name = ''' || p_name || ''''
```

A safer value comparison uses a bind variable:

```plsql
EXECUTE IMMEDIATE
    'UPDATE employees SET salary = :1 WHERE id = :2'
    USING v_new_salary, v_id;
```

For a dynamic identifier such as a table name, first validate the identifier against an allowed list or DBMS-specific identifier rules before constructing the statement.

## 4. Dynamic SQL Cost and Trade-Offs

Dynamic SQL provides flexibility but may introduce parsing/optimization overhead and makes SQL harder to analyze statically. Use static SQL when the statement structure is known and dynamic SQL only where runtime variability requires it.
