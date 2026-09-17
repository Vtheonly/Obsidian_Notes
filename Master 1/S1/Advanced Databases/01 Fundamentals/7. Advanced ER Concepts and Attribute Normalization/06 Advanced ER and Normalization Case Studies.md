# Advanced ER and Normalization Case Studies

This note preserves the worked modeling material from the course master guide that is useful as a concrete application of the theoretical ER and normalization notes.

## 1. Reflexive Relationships (Self-Association)

A **reflexive relationship** is an association in which an entity type participates in a relationship with itself. The two roles must be named clearly because the same entity type appears on both sides.

Common examples include:

* `EMPLOYEE` supervises `EMPLOYEE`;
* a person is a friend of another person;
* a person is an enemy of another person;
* a family member is parent of another family member.

### Reception-System Case Study

Consider a reception-management system with entities such as:

* `PERSONNES`
* `RECEPTIONS`
* `PLATS`
* `TYPE_VINS`

Typical relationships include:

* `PERSONNES` participates in `RECEPTIONS` as a guest;
* `RECEPTIONS` serves `PLATS`;
* `PLATS` pairs with `TYPE_VINS`;
* `PERSONNES` can appreciate or dislike `PLATS`;
* `PERSONNES` can be related to other `PERSONNES` through reflexive relationships such as `AMIS` and `ENNEMIS`.

The reflexive relationships must be modeled with role names that distinguish the two participations, such as `person` and `friend` rather than treating the association as an undifferentiated self-link.

## 2. Generalization / Specialization (Inheritance)

In an ER model, **generalization** groups several specific entity types under a common supertype, while **specialization** starts with a general entity type and defines more specific subtypes.

Example:

```text
ACCOUNT
 ├── CHECKING_ACCOUNT
 └── SAVINGS_ACCOUNT
```

Each subtype inherits the common attributes of the supertype and adds subtype-specific attributes.

### Three Relational Mapping Strategies

#### Strategy A: Single Table Inheritance / One Table
Store supertype and subtype attributes in one table with a discriminator column.

**Advantages:**

* Simple polymorphic queries.
* No joins required to read a complete object.

**Disadvantages:**

* Many nullable subtype columns.
* Harder to enforce subtype-specific `NOT NULL` rules.

#### Strategy B: Class Table Inheritance
Store the common attributes in a supertype table and each subtype in its own table. The subtype primary key is also a foreign key to the supertype.

**Advantages:**

* Clean subtype-specific schemas.
* Subtype-only attributes can be `NOT NULL`.
* Less sparse storage.

**Disadvantages:**

* Reconstructing an object requires joins.
* Polymorphic queries can become more complex.

#### Strategy C: Concrete Table Inheritance
Create a separate complete table for each concrete subtype, repeating the inherited columns in each table.

**Advantages:**

* Direct access to a complete concrete object.
* No join to a supertype table is required for subtype queries.

**Disadvantages:**

* Attribute duplication across tables.
* Polymorphic queries require `UNION` or multiple joins.
* Schema changes can have to be repeated for every concrete subtype.

The appropriate mapping is a relational design decision rather than something imposed uniquely by the ER model.

## 3. Functional Dependencies and Attribute Closure

A functional dependency:

$$X \rightarrow Y$$

means that two tuples agreeing on all attributes in `X` must also agree on all attributes in `Y`.

The **closure** of an attribute set `X`, written $X^+$, is the set of all attributes functionally determined by `X` under the given dependency set.

A standard candidate-key procedure is:

1. Compute $X^+$ from the functional dependencies.
2. If $X^+$ contains every attribute of the relation, `X` is a superkey.
3. Remove attributes one by one and recompute the closure.
4. If no attribute can be removed while retaining a superkey, `X` is a candidate key.

## 4. Normalization Workflow

The normalization workflow is:

1. Identify the functional dependencies.
2. Determine candidate keys and prime attributes.
3. Check **1NF**: attributes are atomic and repeating groups are removed.
4. Check **2NF**: no non-prime attribute depends on only part of a composite candidate key.
5. Check **3NF**: for every non-trivial dependency $X \rightarrow A$, either `X` is a superkey or `A` is prime.
6. Check **BCNF**: for every non-trivial dependency $X \rightarrow Y$, `X` must be a superkey.
7. If a violation exists, decompose the relation while checking desirable properties such as lossless join and, where possible, dependency preservation.

## 5. Worked Decomposition Pattern

A common exam structure is a relation containing identifying attributes plus descriptive attributes determined by different subsets of the key.

For example, if:

$$AB \rightarrow C$$
$$C \rightarrow D$$

then `D` depends transitively on `AB` through `C`. A 3NF-oriented decomposition can separate:

```text
R1(C, D)
R2(A, B, C)
```

The reasoning is not to memorize the tables but to trace the determinant of each dependency and remove transitive dependencies while preserving the ability to reconstruct the original facts.

## 6. Exam Checklist

When solving an ER-to-relational or normalization problem, explicitly state:

* entity types and relationship roles;
* primary/candidate keys;
* functional dependencies;
* attribute closures;
* the normal form currently violated;
* the decomposition performed;
* whether the decomposition is lossless and whether dependencies are preserved when that property is required;
* the chosen inheritance-mapping strategy and its trade-offs when specialization is present.
