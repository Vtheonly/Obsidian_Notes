# 02 Composite and Multivalued Attributes

## Composite attributes

A composite attribute contains several meaningful components.

Example:

`Address = Street + City + ZipCode`

If the components are needed independently, model them separately rather than hiding them inside one undifferentiated value.

## Multivalued attributes

A multivalued attribute represents several values for one entity occurrence.

Example:

`EMPLOYEE.PhoneNumbers = {home, work, mobile}`

When the values have their own identity or must be managed independently, model them as a separate entity/relationship rather than storing a list inside one attribute.

## Why this matters

Decomposing structured or repeated data improves:

- searching and filtering;
- integrity constraints;
- uniqueness rules;
- updates to individual values;
- translation to relational tables.

## Quick test

Ask: "Can I identify and manipulate each component or repeated value independently?"

If yes, a single flat attribute is usually hiding structure that should be modeled explicitly.
