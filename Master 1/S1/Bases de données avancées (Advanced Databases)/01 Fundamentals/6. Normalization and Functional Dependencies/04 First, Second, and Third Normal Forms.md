# First, Second, and Third Normal Forms

Normalization uses progressively stronger rules to reduce problematic redundancy.

## 1. First Normal Form (1NF)

A relation is in 1NF when each attribute contains atomic values and there are no repeating groups represented inside a single cell.

A column should represent one value for one tuple, rather than a list such as:

`PhoneNumbers = '0550..., 0660...'`

## 2. Second Normal Form (2NF)

A relation is in 2NF when:

- it is already in 1NF; and
- every non-prime attribute is fully functionally dependent on every candidate key.

2NF primarily addresses **partial dependencies** on part of a composite candidate key.

If the candidate key is a single attribute, partial dependency cannot occur.

## 3. Third Normal Form (3NF)

A relation is in 3NF when it is in 2NF and non-key attributes do not create problematic transitive dependencies on a candidate key.

A formal formulation is that for every non-trivial FD `X → A`, either:

- `X` is a superkey; or
- `A` is a prime attribute.

## 4. Normalization Workflow

For a relation and its FDs:

1. Establish the candidate keys.
2. Check atomicity and 1NF.
3. Check for partial dependencies and 2NF.
4. Check for transitive dependencies and 3NF.
5. Decompose where necessary.

## Important Distinction

Normalization is based on **functional dependencies and candidate keys**, not simply on how many columns a table contains.
