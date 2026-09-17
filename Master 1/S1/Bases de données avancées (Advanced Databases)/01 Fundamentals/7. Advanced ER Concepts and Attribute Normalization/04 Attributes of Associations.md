# 04 Attributes of Associations

An attribute belongs to an association when its value depends on the particular combination of participating entities.

## Example: SUPPLIER supplies ARTICLE

Suppose a supplier can supply many articles and an article can be supplied by many suppliers.

`Quantity` cannot normally belong to `SUPPLIER`, because one supplier can provide different quantities for different articles.

It cannot normally belong to `ARTICLE`, because an article can be supplied by different suppliers in different quantities.

Therefore `Quantity` belongs to the `SUPPLIES` association.

## Dependency test

Ask:

> Does this value describe one entity, or does it describe this specific relationship between entities?

If it describes the relationship occurrence, place it on the association.

## Common examples

- `Grade` on STUDENT — COURSE enrollment.
- `Quantity` on SUPPLIER — ARTICLE supply.
- `Price_Agreed` on CUSTOMER — PRODUCT purchase.
- `Return_Date` on SUBSCRIBER — BOOK borrowing.

## Relational consequence

For an N:M association, the association usually becomes a relation containing the participating foreign keys plus its own attributes.
