# 05 Anomaly Analysis Exercises

## Exercise 1

`R(student, class, teacher)` contains the teacher name on every row for every student in the class.

**Question:** what happens when a teacher changes?

**Expected reasoning:** repeated teacher facts create an update anomaly.

## Exercise 2

A new course exists but has no enrolled students. The only relation available is `ENROLLMENT(student, course, grade)`.

**Question:** can the course be recorded independently?

**Expected reasoning:** not cleanly; course facts should have their own relation.

## Exercise 3

A customer's last order is deleted, and the customer's name disappears from the database.

**Question:** what anomaly is present?

**Answer:** deletion anomaly.

## Exam method

For any flat relation:

1. underline repeated facts;
2. ask what happens when one fact changes;
3. ask whether a new independent fact can be inserted;
4. ask what disappears when a row is deleted;
5. propose relations that separate the independent themes.
