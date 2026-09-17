# 01 Entities and Basic Translation Rules

## Entity type

An entity type normally becomes a relation.

Example:

`CLIENT(num_client, nom, adresse)`

The entity identifier becomes the primary key.

## Attributes

Simple attributes become columns. Composite attributes are decomposed when their components are modeled separately.

## Foreign keys

A relationship represented by a foreign key requires the referenced primary key to appear as a foreign-key attribute in the appropriate relation.

## Translation workflow

1. Create one relation for each entity type.
2. Identify each primary key.
3. Inspect every association and its cardinalities.
4. Decide whether the association needs its own relation or can be represented with a foreign key.
5. Add association attributes to the relation representing the association occurrence.
6. Check that the resulting keys and foreign keys preserve the conceptual constraints.
