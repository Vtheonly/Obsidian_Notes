---
tags: [concept, refactoring, constants]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]]
  - [[04 - OOD and SOLID/16 - Primitive Obsession]]
---

# Replace Magic Number with Symbolic Constant

## What it is

A **magic number** is a numeric literal with no explanation. Replace it with a named constant.

```java
// Before
if (roleId == 4) { ... }  // what is 4?
double load = bytes / 1024.0;  // what is 1024?

// After
public static final int ROLE_ADMIN = 4;
public static final int BYTES_PER_KB = 1024;

if (roleId == ROLE_ADMIN) { ... }
double load = bytes / (double) BYTES_PER_KB;
```

## When to use

- The number appears more than once.
- The number's meaning isn't obvious.
- The number might change (a constant gives it one place to change).

## When NOT to use

- `0`, `1`, `-1` are usually obvious.
- Numbers used once in a clearly-named context: `for (int i = 0; i < list.size(); i++)` doesn't need `START_INDEX = 0`.

## Better: enums

For a closed set of values, use an enum:

```java
// Before
public static final int ROLE_USER = 1;
public static final int ROLE_SECRETARY_BASIC = 2;
public static final int ROLE_ADMIN = 4;
public static final int ROLE_CHIEF = 5;
if (roleId == ROLE_ADMIN) { ... }

// After
public enum Role { USER(1), SECRETARY_BASIC(2), ADMIN(4), CHIEF(5); ... }
if (user.getRole() == Role.ADMIN) { ... }
```

Enums give type safety, IDE autocomplete, and exhaustiveness checking.

## Project Connection

The project is full of magic numbers:
- Role IDs 4, 5, 1, 2, 3.
- ASCII 33, 126 for password generation.
- Password length 8.
- `count == 1` for login success.
- `-1` for "no access."
- `SQLCODE != -942` (Oracle "table does not exist").
- PieChart values 33, 20, 17, 30.

All should be named constants or enums.

## Further reading

- *Refactoring* (Fowler), "Replace Magic Number with Symbolic Constant".
- *Clean Code* (Martin), Chapter 2 (Meaningful Names).
