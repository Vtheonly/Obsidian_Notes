---
title: "Operators in C++"
---

C++ provides a rich set of operators to perform various operations on data. Here are some of the most common ones.

### Conditional (Ternary) Operator (`? :`)

The conditional operator is a concise way to write an `if-else` statement. It is the only ternary operator in C++.

**Syntax**:
`condition ? value_if_true : value_if_false;`

-   If the `condition` evaluates to `true`, the expression returns `value_if_true`.
-   Otherwise, it returns `value_if_false`.

**Example**:
```cpp
#include <iostream>

int main() {
    int a = 5, b = 10;
    int min_val = (a < b) ? a : b; // min_val will be 5
    std::cout << "The minimum value is: " << min_val << std::endl;
    return 0;
}
```
This is equivalent to:
```cpp
if (a < b) {
    min_val = a;
} else {
    min_val = b;
}
```

### Bitwise Operators

Bitwise operators manipulate the individual bits of integer types. They are often used in low-level programming, such as device drivers or for performance optimization.

-   `&` : Bitwise AND
-   `|` : Bitwise OR
-   `^` : Bitwise XOR (exclusive OR)
-   `~` : Bitwise NOT (inverts all bits)
-   `<<`: Left shift (multiplies by 2 for each shift)
-   `>>`: Right shift (divides by 2 for each shift)

**Example**:
```cpp
#include <iostream>
#include <bitset>

int main() {
    unsigned int a = 29; // 0001 1101
    unsigned int b = 48; // 0011 0000

    std::cout << "a = " << std::bitset<8>(a) << std::endl;
    std::cout << "b = " << std::bitset<8>(b) << std::endl;
    std::cout << "a & b = " << std::bitset<8>(a & b) << std::endl; // 0001 0000 (16)
    std::cout << "a | b = " << std::bitset<8>(a | b) << std::endl; // 0011 1101 (61)
    std::cout << "a ^ b = " << std::bitset<8>(a ^ b) << std::endl; // 0010 1101 (45)
    std::cout << "~a = " << std::bitset<8>(~a) << std::endl;    // 1110 0010
    std::cout << "a << 2 = " << std::bitset<8>(a << 2) << std::endl; // 0111 0100 (116)
    std::cout << "a >> 2 = " << std::bitset<8>(a >> 2) << std::endl; // 0000 0111 (7)

    return 0;
}
```

### Comma Operator (`,`)

The comma operator evaluates its first operand and discards the result, then evaluates its second operand and returns its value and type.

It is most commonly used to place multiple expressions in a single statement, such as in the initialization or update part of a `for` loop.

**Example**:
```cpp
#include <iostream>

int main() {
    for (int i = 0, j = 5; i < 5; ++i, --j) {
        std::cout << "i = " << i << ", j = " << j << std::endl;
    }
    return 0;
}
```

### Increment and Decrement Operators (`++`, `--`)

These operators are used to increment or decrement a variable's value by one.

-   **Pre-increment/decrement (`++c`, `--c`)**: The variable is changed *before* its value is used in the expression.
-   **Post-increment/decrement (`c++`, `c--`)**: The variable is changed *after* its value is used in the expression.

**Example**:
```cpp
#include <iostream>

int main() {
    int c = 5;
    std::cout << "Pre-increment: " << ++c << std::endl; // Prints 6, c is now 6

    int d = 5;
    std::cout << "Post-increment: " << d++ << std::endl; // Prints 5, d is now 6
    std::cout << "d is now: " << d << std::endl; // Prints 6

    return 0;
}
```

### Cast Operators

Casting is used to explicitly convert a value from one type to another.

-   **C-style cast `(type)expression`**: This is the old way of casting. It is powerful but unsafe because it can perform any kind of cast.
-   **C++-style casts**: Modern C++ introduced four types of casts that are safer because they make the programmer's intent clear.
    -   `static_cast<type>(expression)`: For safe, well-defined conversions (e.g., `int` to `double`).
    -   `dynamic_cast<type>(expression)`: For safe downcasting in polymorphic class hierarchies.
    -   `const_cast<type>(expression)`: To add or remove `const` or `volatile` qualifiers.
    -   `reinterpret_cast<type>(expression)`: For low-level, unsafe casts between unrelated types (e.g., pointer to integer).

**Example**:
```cpp
#include <iostream>

int main() {
    int x = 3;
    int y = 4;

    // Using C++ static_cast for a safe conversion
    double result = static_cast<double>(x) / y;
    std::cout << "Result: " << result << std::endl; // Outputs 0.75

    return 0;
}
```