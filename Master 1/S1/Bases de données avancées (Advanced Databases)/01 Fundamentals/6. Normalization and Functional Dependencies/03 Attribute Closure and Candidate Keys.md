# Attribute Closure and Candidate Keys

Attribute closure is one of the main tools for reasoning about functional dependencies and keys.

## 1. Attribute Closure

The closure of an attribute set `X`, written `X+`, is the set of all attributes that can be functionally determined from `X` using a given set of functional dependencies.

### Basic Procedure

1. Start with `X+ = X`.
2. Find an FD whose left side is contained in `X+`.
3. Add its right-side attributes to `X+`.
4. Repeat until no new attribute can be added.

If `X+` contains every attribute of the relation, then `X` is a superkey.

## 2. Candidate Keys

A **candidate key** is a minimal superkey.

It therefore satisfies two conditions:

- Its closure contains every attribute in the relation.
- Removing any attribute from it prevents it from determining the whole relation.

## 3. Example

Consider:

`R(A, B, C, D)`

with:

`A → B`

`B → C`

`AC → D`

Starting with `{A}`:

`A+ = {A}`

Using `A → B`:

`A+ = {A, B}`

Using `B → C`:

`A+ = {A, B, C}`

Now `AC → D` applies, giving:

`A+ = {A, B, C, D}`

Therefore `A` is a superkey. Because it contains only one attribute, it is also minimal and is therefore a candidate key.

## Exam Strategy

When finding candidate keys:

1. Identify attributes that never appear on the right side of an FD; they often must belong to every key.
2. Compute closures systematically.
3. Test minimality after finding a superkey.
4. Check whether multiple candidate keys exist.

> [!warning] Common mistake
> A superkey is not automatically a candidate key. Candidate keys must be minimal.
