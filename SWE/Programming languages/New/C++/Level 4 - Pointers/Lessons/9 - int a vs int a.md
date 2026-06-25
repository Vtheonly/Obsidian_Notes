---
title: "Pointer Declaration Style: int* p vs. int *p"
---

### `int* p` vs. `int *p` in C++

In C++, when you declare a pointer, the placement of the asterisk (`*`) is a matter of coding style and does not change the meaning of the code to the compiler. Both of the following declarations are identical in function:

```cpp
int* p; // Declares p as a pointer to an integer.
int *p; // Also declares p as a pointer to an integer.
```

The C++ compiler treats them exactly the same. The choice between them is a long-standing stylistic debate.

--- 

### The Argument for `int* p` (Type-centric)

This style groups the `*` with the type (`int*`), emphasizing that the **type of the variable `p` is `int*`** (pointer to an integer).

```cpp
int* p1; // p1 is of type int*
int* p2; // p2 is also of type int*
```

**Advantage**: This style is very clear when declaring one variable per line. It aligns well with how types are thought about in C++, especially with templates and `auto`.

```cpp
auto p = new int; // The type of p is deduced as int*
```

--- 

### The Argument for `int *p` (Variable-centric)

This style groups the `*` with the variable name (`*p`), emphasizing that the **expression `*p` evaluates to an `int`**.

```cpp
int *p1; // *p1 is an int
int *p2; // *p2 is an int
```

**Advantage**: This style avoids a common pitfall when declaring multiple variables on the same line.

#### The Multiple Declaration Pitfall

This is the strongest argument for the `int *p` style. Consider this line:

```cpp
int* p1, p2; // What are the types of p1 and p2?
```

Someone who prefers the `int* p` style might mistakenly think both `p1` and `p2` are pointers. However, the `*` only applies to the variable it is directly in front of.

-   `p1` is declared as `int*` (a pointer to an integer).
-   `p2` is declared as `int` (a regular integer).

To declare both as pointers on the same line, you would have to write:

```cpp
int *p1, *p2;
```

Or, using the other style:

```cpp
int* p1, *p2; // Also works, but can be seen as less clear
```

Because the `int *p` style makes this distinction more visually apparent, many experienced C and C++ programmers, including Bjarne Stroustrup (the creator of C++), prefer it.

--- 

### Best Practice and Conclusion

1.  **Consistency is Key**: Whichever style you choose, be consistent throughout your project.

2.  **One Declaration Per Line**: The best way to avoid the multiple-declaration pitfall entirely is to declare only one variable per line. This is a widely recommended best practice in modern C++ as it improves readability and eliminates ambiguity.

    ```cpp
    // Recommended:
    int* p1;
    int p2;
    ```

In summary, while both `int* p` and `int *p` are functionally identical, the `int *p` style is often favored because it more accurately reflects how the C++ declaration syntax works, especially with multiple declarations. However, the modern C++ guideline of **one declaration per line** makes the choice less critical.