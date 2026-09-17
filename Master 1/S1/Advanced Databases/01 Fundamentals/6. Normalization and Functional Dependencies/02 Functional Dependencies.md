# Functional Dependencies

A **functional dependency (FD)** describes a constraint between attributes in a relation.

We write:

`X → Y`

and read it as: **X functionally determines Y**.

## 1. Formal Meaning

For every pair of tuples in a relation, if their values for `X` are equal, their values for `Y` must also be equal.

Therefore, an FD is a statement about the data's semantics, not merely an observation from one small sample.

## 2. Examples

If each student has exactly one date of birth:

`StudentID → DateOfBirth`

If each course code identifies exactly one course title:

`CourseCode → CourseTitle`

But generally:

`CourseCode → StudentID`

is false because many students can enroll in the same course.

## 3. Trivial Dependencies

An FD `X → Y` is **trivial** when `Y ⊆ X`.

Example:

`{StudentID, Name} → Name`

Trivial dependencies are always satisfied and usually do not provide useful information about schema design.

## 4. Full and Partial Dependency

A dependency is **fully functional** when no proper subset of the determinant can determine the dependent attribute.

This distinction becomes important when testing for 2NF, especially when a relation has a composite candidate key.

## 5. Transitive Dependency

A transitive dependency can occur when:

`A → B` and `B → C`

which means `A` indirectly determines `C` through `B`.

Transitive dependencies are central to understanding 3NF.

## Key Principle

Do not infer functional dependencies solely from the current rows of a table. Determine them from the real-world rules represented by the schema.
