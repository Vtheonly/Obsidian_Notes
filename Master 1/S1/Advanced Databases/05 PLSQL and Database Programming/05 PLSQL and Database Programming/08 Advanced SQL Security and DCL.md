# Advanced SQL Security and DCL

Advanced database work includes not only procedural logic but also controlling who can read or modify data. **Data Control Language (DCL)** provides the SQL-level mechanisms for granting and revoking privileges.

## 1. Views as Security Boundaries

A view can expose a restricted subset of a base table by limiting columns, rows, or both.

```sql
CREATE VIEW V_Service_A003 AS
SELECT EMP_Num, EMP_Nom, EMP_Titre, SRV_Num
FROM EMPLOYE
WHERE SRV_Num = 'A003'
WITH CHECK OPTION;
```

This view provides a horizontal restriction (`SRV_Num = 'A003'`) and can also provide a vertical restriction by selecting only the columns that users need.

`WITH CHECK OPTION` ensures that inserts or updates performed through the view cannot produce rows that no longer satisfy the view's predicate, provided the view is updatable under the target DBMS.

## 2. `GRANT`

`GRANT` assigns one or more privileges to a user or role.

```sql
GRANT SELECT, UPDATE
ON V_Service_A003
TO Manager, Director;
```

A privilege may be granted with delegation authority:

```sql
GRANT SELECT
ON V_Service_A003
TO Manager
WITH GRANT OPTION;
```

`WITH GRANT OPTION` allows the grantee to grant that privilege to other principals, subject to the DBMS's privilege model.

## 3. `REVOKE`

`REVOKE` removes privileges that were previously granted.

```sql
REVOKE SELECT, UPDATE
ON V_Service_A003
FROM Manager;
```

When a user has delegated a privilege to others, revocation can trigger dependent privilege changes according to the DBMS's privilege graph and cascade rules. Do not assume identical propagation semantics across database vendors.

## 4. Why Views and DCL Work Together

A useful security pattern is:

1. Keep sensitive data in the base table.
2. Create a view exposing only the approved rows/columns.
3. Grant users access to the view rather than directly to the base table.
4. Use `WITH CHECK OPTION` where modifications through the filtered view must remain inside the view's permitted scope.

This separates the physical data model from the logical interface exposed to each user group.

## 5. Security vs. Integrity

DCL answers **who is allowed to perform an operation**. Integrity constraints answer **whether the resulting data is valid**.

For example:

* `GRANT UPDATE ON V_Service_A003 TO Manager` controls authorization.
* `CHECK (salary >= 0)` controls a value invariant.
* `FOREIGN KEY (...) REFERENCES ...` controls referential integrity.

These mechanisms are complementary and should not be treated as interchangeable.
