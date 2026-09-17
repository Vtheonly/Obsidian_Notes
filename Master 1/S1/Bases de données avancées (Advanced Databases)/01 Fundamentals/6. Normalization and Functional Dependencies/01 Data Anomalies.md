# Data Anomalies

Poorly designed relational schemas can store the same fact repeatedly. This redundancy creates anomalies during data manipulation.

## 1. Insertion Anomaly

An insertion anomaly occurs when a valid fact cannot be inserted without also inserting an unrelated fact.

**Example:** If course information is stored only alongside student enrollment information, a new course may be impossible to record until a student enrolls in it.

## 2. Update Anomaly

An update anomaly occurs when the same fact appears in several rows and every copy must be changed.

If a department's address is repeated across 50 employee rows, changing the address requires updating all 50 rows. Missing one row creates contradictory data.

## 3. Deletion Anomaly

A deletion anomaly occurs when removing one fact accidentally removes another fact that should have been retained.

For example, deleting the last student enrolled in a course could also delete the only stored information about that course.

## 4. Why Normalization Helps

Normalization separates facts according to their logical dependencies. The objective is not simply to create more tables; it is to reduce redundancy while preserving the meaning and integrity of the data.

## Exam Checklist

When analyzing a relation, ask:

- Is the same fact repeated across many rows?
- Can one fact be changed without updating multiple rows?
- Can a fact exist independently of another fact?
- Could deleting one row destroy information about a different entity?

These questions usually reveal the motivation for normalization before any functional dependencies are written.
