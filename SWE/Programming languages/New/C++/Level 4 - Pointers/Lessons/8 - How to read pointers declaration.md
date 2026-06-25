---
title: "How to Read Complex C++ Declarations"
---

C++ declarations, especially those involving pointers, references, and functions, can sometimes be complex. The key to understanding them is to read them systematically. The **"right-left rule"** is a helpful mnemonic for this.

### The Right-Left Rule (Spiral Rule)

1.  **Find the identifier** (the variable or function name).
2.  **Look to the right** for `[]` (array) or `()` (function) operators.
3.  **Look to the left** for `*` (pointer), `&` (reference), `const`, and the base type.
4.  Use parentheses `()` to override the normal precedence.

### Operator Precedence

-   **Highest**: `[]` (array) and `()` (function call) - evaluated left-to-right.
-   **Lower**: `*` (pointer) - evaluated right-to-left.

Let's apply this to some examples.

--- 

### Example 1: Array of Pointers

**`char* names[20];`**

1.  **Identifier**: `names`
2.  **Right**: `[20]` -> "is an array of size 20"
3.  **Left**: `*` -> "of pointers"
4.  **Left**: `char` -> "to `char`"

**Result**: `names` is an **array of 20 pointers to `char`**.

--- 

### Example 2: Pointer to an Array

**`int (*arr_ptr)[10];`**

1.  **Identifier**: `arr_ptr`
2.  **Parentheses**: The `()` around `*arr_ptr` mean we process the `*` first.
3.  **Left (inside `()`)**: `*` -> "is a pointer"
4.  **Right**: `[10]` -> "to an array of size 10"
5.  **Left**: `int` -> "of `int`s"

**Result**: `arr_ptr` is a **pointer to an array of 10 `int`s**.

--- 

### Example 3: Function Pointer

**`void (*fp)(int, double);`**

1.  **Identifier**: `fp`
2.  **Parentheses**: Process `*fp` first.
3.  **Left (inside `()`)**: `*` -> "is a pointer"
4.  **Right**: `(int, double)` -> "to a function that takes an `int` and a `double`"
5.  **Left**: `void` -> "and returns `void`"

**Result**: `fp` is a **pointer to a function** that takes an `int` and a `double` and returns `void`.

--- 

### Example 4: Function Returning a Pointer

**`int* create_array(int size);`**

1.  **Identifier**: `create_array`
2.  **Right**: `(int size)` -> "is a function that takes an `int`"
3.  **Left**: `*` -> "and returns a pointer"
4.  **Left**: `int` -> "to an `int`"

**Result**: `create_array` is a **function** that takes an `int` and returns a pointer to an `int`.

--- 

### Example 5: A More Complex Declaration

**`const int* (*(*foo)())[5];`**

Let's break it down:

1.  **Identifier**: `foo`
2.  `(*foo)` -> `foo` is a pointer...
3.  `(*foo)()` -> ...to a function that takes no arguments...
4.  `*(*foo)()` -> ...and returns a pointer...
5.  `(*(*foo)())[5]` -> ...to an array of size 5...
6.  `*(*(*foo)())[5]` -> ...of pointers...
7.  `const int* (*(*foo)())[5]` -> ...to `int`s that are `const`.

**Result**: `foo` is a **pointer to a function** that takes no arguments and returns a **pointer to an array of 5 pointers to `const int`**.

### Summary

While complex declarations like the last example are rare and generally discouraged in modern C++ (type aliases like `using` or `typedef` should be used for clarity), understanding the parsing rules is essential for reading legacy code and fully grasping C++'s type system.

**Modern C++ Tip**: Use `using` to create type aliases for complex types to make your code much more readable.

```cpp
using IntArray5 = int[5];
using FuncPtr = IntArray5* (*)();

FuncPtr my_func_ptr;
```
