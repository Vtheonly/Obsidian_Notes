# Modality

Modality describes whether participation in a relationship is mandatory or optional. While cardinality specifies how many rows can be associated (one or many), modality specifies whether at least one row must be associated (zero or one as the minimum). Together, cardinality and modality fully define the constraints on a relationship between two tables in an ER diagram. See [[33 - Cardinality]] for the companion concept and [[32 - Introduction to Entity Relationship Modeling]] for the broader context of ER modeling.

## Mandatory vs. Optional Participation

A relationship has **mandatory** participation when every row in the child table must be associated with a row in the parent table. This corresponds to a `NOT NULL` constraint on the foreign key column in the child table. If the foreign key is `NOT NULL`, every child row must reference a valid parent row, and the relationship is mandatory.

A relationship has **optional** participation when rows in the child table can exist without being associated with any row in the parent table. This corresponds to a nullable foreign key column. If the foreign key allows `NULL`, a child row can exist without referencing a parent, and the relationship is optional.

## Representing Modality in ER Diagrams

In Crow's Foot notation, modality is represented by adding a circle or a dash (vertical line) next to the cardinality symbol on the child side of the relationship. A circle (`O`) indicates that the minimum is zero (optional participation), while a dash (`|`) indicates that the minimum is one (mandatory participation).

| Modality | Symbol | Minimum | Meaning |
|---|---|---|---|
| Optional | `O` | 0 | Child may not reference a parent |
| Mandatory | `|` | 1 | Child must reference a parent |

When combined with cardinality, the complete notation expresses both the minimum (modality) and maximum (cardinality) number of related rows.

## The Four Common Relationship Patterns

For a one-to-many relationship (the most common type), combining modality and cardinality on the child side produces four possible patterns:

### 1. Optional One (0..1)

```
parent ----O|---- child
```

A child row may reference zero or one parent row. The foreign key is nullable, and the relationship is optional. The child can exist without any parent association.

Example: A `class` table where `instructor_id` is nullable. A class may or may not have an assigned instructor.

### 2. Mandatory One (1..1)

```
parent ----||---- child
```

A child row must reference exactly one parent row. The foreign key is `NOT NULL`, and every child row is required to have a parent association.

Example: A `card` table where `holder_id` is `NOT NULL`. Every card must be owned by a card holder; unowned cards are not stored in this table.

### 3. Optional Many (0..M)

```
parent ----O<---- child
```

A child row may reference zero or more parent rows (from the parent's perspective, one parent can have zero or more children). The foreign key in the child is nullable, meaning some children may not reference any parent.

Example: A `person` table where `car_id` is nullable. A person may own zero or more cars, but some people do not own any car.

### 4. Mandatory Many (1..M)

```
parent ----|<---- child
```

A child row must reference at least one parent row (from the parent's perspective, one parent must have one or more children). The foreign key is `NOT NULL`, and every child is required to participate.

Example: An `order_item` table where `order_id` is `NOT NULL`. Every line item must belong to an order; orphaned line items are not permitted.

## Credit Card Example

Consider a credit card company with a `card_holder` table and a `card` table. The relationship between card holders and cards can be designed with different modality depending on business rules:

**Scenario A: Cards must have an owner (mandatory)**

```sql
CREATE TABLE card (
    card_id INT PRIMARY KEY,
    holder_id INT NOT NULL,  -- mandatory: every card must have an owner
    card_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (holder_id) REFERENCES card_holder(holder_id)
);
```

In this design, every row in `card` must have a `holder_id` value. Unactivated cards, canceled cards, or cards without current owners cannot be stored. This is appropriate if the table only tracks active, owned cards.

**Scenario B: Cards may not have an owner (optional)**

```sql
CREATE TABLE card (
    card_id INT PRIMARY KEY,
    holder_id INT,  -- optional: card may not have an owner
    card_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (holder_id) REFERENCES card_holder(holder_id)
);
```

In this design, `holder_id` can be `NULL`, allowing cards without owners to exist in the table. This is useful if the table needs to track unactivated cards, canceled cards, or cards that are not currently assigned to any holder.

## Modality vs. Cardinality

Cardinality and modality answer different questions about a relationship:

| Concept | Question | Values |
|---|---|---|
| Cardinality | What is the maximum number of related rows? | One or Many |
| Modality | What is the minimum number of related rows? | Zero or One |

Together they define the complete participation constraint. For example, "a card holder has zero or more cards" combines a modality of zero (optional) with a cardinality of many. "An order item has exactly one order" combines a modality of one (mandatory) with a cardinality of one.

Cross-reference: [[32 - Introduction to Entity Relationship Modeling]], [[33 - Cardinality]], [[28 - NOT NULL Foreign Key]]
