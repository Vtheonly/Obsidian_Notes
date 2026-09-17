---
tags: [concept, jdbc, callable-statement, stored-procedures]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/PL/SQL Basics]]
---

# CallableStatement

## What it is

`CallableStatement` calls stored procedures and functions.

## Calling a procedure

```java
// Procedure: accept_intern(p_intern_id IN NUMBER, p_chief_id IN NUMBER)
try (CallableStatement cs = conn.prepareCall("{call accept_intern(?, ?)}")) {
    cs.setLong(1, internId);
    cs.setLong(2, chiefId);
    cs.execute();
}
```

## Calling a function

```java
// Function: count_pending(p_dept_id IN NUMBER) RETURN NUMBER
try (CallableStatement cs = conn.prepareCall("{? = call count_pending(?)}")) {
    cs.registerOutParameter(1, Types.NUMERIC);
    cs.setLong(2, deptId);
    cs.execute();
    int count = cs.getInt(1);
}
```

## IN/OUT/INOUT parameters

```java
// Procedure with OUT parameter
try (CallableStatement cs = conn.prepareCall("{call get_intern_count(?, ?)}")) {
    cs.setLong(1, deptId);                    // IN
    cs.registerOutParameter(2, Types.NUMERIC); // OUT
    cs.execute();
    int count = cs.getInt(2);
}
```

## When to use

- **Complex logic in the DB** — encapsulate in a procedure.
- **Performance** — avoid round-trips for multi-step operations.
- **Security** — grant execute on the procedure, not on the tables.

## When NOT to use

- **Simple CRUD** — PreparedStatement is simpler.
- **Portability** — stored procedures are vendor-specific.
- **Testability** — procedures are harder to unit-test than Java code.

## Project Connection

The project doesn't use stored procedures. The advanced redesign could encapsulate the chief's accept/reject logic in a procedure (atomic update + audit log), but a Java service layer with `@Transactional` achieves the same.

## Further reading

- JDBC `CallableStatement` documentation.
