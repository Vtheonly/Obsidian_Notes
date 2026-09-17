# 05 Enumerated Values and Reference Entities

A strict list of allowed categories can be modeled as a reference entity when those categories need their own identity, metadata, or referential integrity.

## Example

Instead of storing arbitrary text such as:

`Emission_Type = Radio | TV | Web`

create a `TYPE` entity when the type is part of the domain model.

Conceptually:

`TYPE(Type_ID, Label)`

and associate the original entity with `TYPE`.

## Benefits

- prevents inconsistent spelling;
- centralizes allowed values;
- makes the domain extensible;
- allows metadata to be attached to each type.

## Do not over-model

A short, stable set of values does not automatically require a new entity in every database. The decision depends on whether the values have independent meaning and lifecycle, and on the modeling conventions required by the course.

## Exam clue

If the question emphasizes a controlled vocabulary, shared categories, or metadata about the categories themselves, consider a reference entity.
