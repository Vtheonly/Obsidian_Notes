# 03 1:N and 1:1 Functional Dependencies

Cardinalities indicate how many occurrences can be associated. They also reveal where a foreign key can represent the relationship.

## 1:N

If each child-side occurrence is associated with at most one parent-side occurrence, the parent's key can usually be stored as a foreign key in the child-side relation.

Example:

`CLIENT(num_client, ...)`

`COMMANDE(num_commande, date, num_client*)`

Each order references its client.

## 1:1

For a 1:1 relationship, either side can sometimes carry the other's key, but the choice should respect optionality, nullability, and participation constraints.

Do not memorize "always put the key on the 1,1 side" without checking the exact cardinalities and course notation.

## Reasoning method

Ask:

1. Which entity occurrence can be linked to many occurrences?
2. Which entity occurrence is linked to at most one occurrence?
3. Which relation can therefore store the other relation's key without creating repeating groups?
4. Are participation and optionality constraints preserved?
