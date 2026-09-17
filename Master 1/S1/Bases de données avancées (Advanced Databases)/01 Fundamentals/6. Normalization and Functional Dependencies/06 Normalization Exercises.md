# Normalization Exercises

## Exercise 1 — Identify Anomalies

Given a relation that stores student, course, instructor, and instructor-office information in every enrollment row:

1. Identify an insertion anomaly.
2. Identify an update anomaly.
3. Identify a deletion anomaly.
4. Propose entities that should be separated.

## Exercise 2 — Compute Closure

Given:

`R(A, B, C, D, E)`

and:

`A → BC`

`C → D`

`BD → E`

Compute `A+` and determine whether `A` is a superkey.

### Solution Method

Start with `{A}`. Apply every dependency whose determinant is contained in the current closure, repeating until the closure stops growing.

## Exercise 3 — Find Candidate Keys

Given:

`R(A, B, C, D)`

`A → B`

`B → C`

`CD → A`

Determine all candidate keys. Show the closure for each candidate you propose and prove minimality.

## Exercise 4 — Normal-Form Analysis

For each relation supplied in an exam problem:

1. List its candidate keys.
2. Mark prime and non-prime attributes.
3. Identify partial dependencies.
4. Identify transitive dependencies.
5. Determine the highest normal form satisfied.
6. Propose a decomposition if required.

## Exam Habit

Never jump directly to a decomposition. Write the functional dependencies first, find the candidate keys, and explicitly state which normal-form rule is violated.
