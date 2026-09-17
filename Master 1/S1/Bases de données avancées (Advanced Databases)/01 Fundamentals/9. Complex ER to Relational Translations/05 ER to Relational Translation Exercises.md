# 05 ER to Relational Translation Exercises

## Exercise 1

STUDENT follows COURSE. A student can follow many courses and a course can have many students. Each enrollment has a grade.

**Task:** translate the model.

**Expected structure:** `STUDENT`, `COURSE`, and an enrollment relation containing both keys plus `grade`.

## Exercise 2

Each ORDER belongs to one CUSTOMER. A customer can have many orders.

**Task:** decide where the customer key belongs.

**Expected reasoning:** the order relation can carry the customer foreign key.

## Exercise 3

A PROJECT has many EMPLOYEES and an employee can work on many projects. Each participation records `hours`.

**Task:** identify the relation created by the N:M association.

**Expected structure:** a participation relation containing employee key, project key, and `hours`.

## Exam checklist

- entity → relation;
- identifier → primary key;
- N:M → association relation;
- association attribute → association relation;
- 1:N → usually foreign key on the N side;
- verify optionality and uniqueness constraints before finalizing a 1:1 translation.
