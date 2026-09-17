# 02 N:M Associations and Association Attributes

An N:M association generally cannot be represented by placing a single foreign key in one of the two entity relations because each side may reference many occurrences of the other.

## Example

`COMMANDE` and `ARTICLE` are connected by `Concerne`.

The association has an attribute `quantité`.

The relational representation is:

`DETAIL_COMMANDE(num_commande*, num_article*, quantité)`

The participating foreign keys together commonly form the primary key when one line represents one command-article pair.

## Key principle

The association relation stores:

- the identity of each participating entity;
- attributes that describe that specific association occurrence.

## Typical examples

- STUDENT — COURSE: `grade`;
- ORDER — PRODUCT: `quantity`;
- SUPPLIER — PRODUCT: `supplied_quantity`;
- EMPLOYEE — PROJECT: `hours`.
