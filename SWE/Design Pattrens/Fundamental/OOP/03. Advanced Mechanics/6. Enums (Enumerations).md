### 1. More than just Constants

From File 2, we see `enum Membership { Bronze, Silver, Gold }`.

In C++, enums are basically integers (0, 1, 2). In Java, Enums are **full-blown Classes**.

- They can have constructors.
- They can have methods.
- They can have instance variables.

### 2. Type Safety

Using Enums prevents "Magic Strings" or "Magic Numbers."

- **Bad:** `setMembership("Gold")` -> What if I type "gold" (lowercase) or "Golden"? The system breaks.
- **Good:** `setMembership(Membership.Gold)` -> The compiler forces you to use a valid value. If you type `Membership.Platnum`, the code won't even compile.

### 3. Useful Methods

- `.name()`: Returns the string name ("Gold").
- `.ordinal()`: Returns the numerical index (0, 1, or 2). This is useful for sorting tiers (Gold > Silver).
