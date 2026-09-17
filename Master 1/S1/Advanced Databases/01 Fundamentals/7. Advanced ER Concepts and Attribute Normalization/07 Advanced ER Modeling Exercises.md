# 06 Advanced ER Modeling Exercises

## Exercise 1 — repeated borrowing

A subscriber may borrow the same book many times, but never twice on the same borrowing date.

**Task:** identify the information needed to distinguish two borrowing events and determine where `Return_Date` belongs.

**Expected reasoning:** the borrowing event needs a key that distinguishes repeated subscriber-book occurrences; `Return_Date` describes the event.

## Exercise 2 — supplier quantity

A supplier provides several articles. The same article may be provided by several suppliers, with a different quantity from each supplier.

**Task:** decide whether `Quantity` belongs to SUPPLIER, ARTICLE, or SUPPLIES.

**Expected answer:** it belongs to the association because it depends on the supplier-article pair.

## Exercise 3 — employee contact data

An employee has several phone numbers, each with a type such as mobile or work.

**Task:** decide whether one `PhoneNumbers` attribute is sufficient.

**Expected reasoning:** the repeated values have independent meaning and should be modeled explicitly when they must be managed individually.

## Exam habit

For every difficult attribute, ask:

1. What does it describe?
2. What facts determine its value?
3. Can it occur more than once?
4. Is it derived from other facts?
5. Does it describe an entity or a relationship occurrence?
