# 03 Derived Attributes and Redundancy

A derived attribute is calculated from other stored information.

## Example

If a line contains:

- `Quantity`
- `Unit_Price`

then `Total_Price` can be derived as:

`Total_Price = Quantity × Unit_Price`

Storing both the source values and the derived value introduces a synchronization risk: one value may change while the other is not updated.

## Modeling principle

Prefer storing the facts that are needed to derive a value. Calculate derived values when they are needed unless there is a documented reason to materialize them.

## Important distinction

A value being derivable does not automatically mean it can never be stored. Performance, historical snapshots, audit requirements, and business rules can justify materialization. The conceptual-model question is whether the value is fundamentally derived from other attributes.

## Exam question

**Should `Total_Price` be a base attribute when `Quantity` and `Unit_Price` already determine it?**

Usually no: it is a derived value and should be treated as such in the conceptual model.
