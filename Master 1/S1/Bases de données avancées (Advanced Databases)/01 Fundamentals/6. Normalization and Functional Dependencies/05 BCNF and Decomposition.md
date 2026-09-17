# BCNF and Decomposition

Boyce-Codd Normal Form (BCNF) strengthens the requirements of 3NF.

## 1. BCNF

A relation is in BCNF if, for every non-trivial functional dependency:

`X → Y`

`X` is a superkey.

This means every determinant must be capable of uniquely identifying a tuple.

## 2. Why BCNF Is Stronger

A relation can satisfy 3NF while still violating BCNF. BCNF removes certain dependency structures that 3NF permits, giving a stricter redundancy criterion.

## 3. Decomposition

Normalization often decomposes one relation into several relations.

A useful decomposition should ideally provide:

- **Lossless join:** joining the decomposed relations reconstructs the intended information without generating spurious tuples.
- **Dependency preservation:** important functional dependencies can still be enforced without reconstructing the original relation.

There can be a trade-off between these properties, especially when aiming for BCNF.

## 4. Practical Principle

Do not decompose a relation merely because a table looks large. First identify the functional dependencies, candidate keys, and exact normal-form violation.

## Study Checklist

- Identify every determinant.
- Determine whether each determinant is a superkey.
- If not, test the dependency against 3NF and BCNF conditions.
- Design a decomposition and verify its properties.
