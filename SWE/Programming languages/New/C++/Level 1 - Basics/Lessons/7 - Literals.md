---
title: "Literals in C++"
---

In C++, **literals** are fixed values that are embedded directly in the source code. They represent constant values of various types, such as integers, floating-point numbers, characters, and strings.

Here’s an overview of the different types of literals in C++:

### 1. Integer Literals

Integer literals represent whole numbers. They can be specified in several bases:

-   **Decimal (base 10)**: `42`, `100`, `-12`
-   **Octal (base 8)**: Start with `0`, like `052` (which is 42 in decimal).
-   **Hexadecimal (base 16)**: Start with `0x` or `0X`, like `0x2A` (42 in decimal).
-   **Binary (base 2) (C++14)**: Start with `0b` or `0B`, like `0b101010` (42 in decimal).

```cpp
int a = 42;      // Decimal
int b = 052;     // Octal
int c = 0x2A;    // Hexadecimal
int d = 0b101010; // Binary
```

You can also use suffixes to specify the type, like `L` for `long`, `LL` for `long long`, and `U` for `unsigned`.

### 2. Floating-Point Literals

Floating-point literals represent numbers with a fractional part. By default, they are of type `double`.

```cpp
float pi = 3.14f;       // 'f' suffix for float
double e = 2.71828;    // double (default)
long double ld = 3.141592L; // 'L' suffix for long double
double small = 5.2e-3;  // Scientific notation
```

### 3. Character Literals

A character literal represents a single character and is enclosed in single quotes (`' '`).

```cpp
char ch = 'A';
char newline = '\n'; // Escape sequence for newline
```

C++ also supports wide character literals, prefixed with `L`, `u`, or `U` for `wchar_t`, `char16_t`, and `char32_t` respectively.

### 4. String Literals

String literals are sequences of characters enclosed in double quotes (`" "`). They are of type `const char[]`.

```cpp
const char* message = "Hello, World!";
```

Modern C++ offers more powerful string handling with `std::string` and special literal types:

-   **`std::string` literals (C++14)**: Use the `s` suffix to create a `std::string` directly.
    ```cpp
    using namespace std::string_literals;
    auto s = "Hello"s;
    ```
-   **Raw string literals (C++11)**: `R"(...)"`, useful for strings with many special characters.
    ```cpp
    std::string path = R"(C:\Users\Me\Documents)";
    ```

### 5. Boolean Literals

C++ has a built-in `bool` type with two literals: `true` and `false`.

```cpp
bool is_active = true;
bool is_done = false;
```

### 6. Pointer Literal

C++11 introduced the `nullptr` literal, which represents a null pointer. It is the modern and type-safe way to represent a null pointer, replacing the use of `NULL` or `0` from C.

```cpp
int* ptr = nullptr;
```

### User-Defined Literals (C++11)

C++11 also introduced the ability for programmers to create their own literal suffixes. This allows for creating objects of user-defined types with a syntax similar to built-in literals.

```cpp
// Example of a user-defined literal for converting degrees to radians
long double operator"" _deg(long double deg) {
    return deg * 3.141592 / 180.0;
}

// Usage
long double angle = 90.0_deg; // angle is now pi/2
```

### Summary

Literals are a fundamental part of C++ syntax, providing a way to express constant values directly in code. Modern C++ has expanded on the concept of literals, introducing more types and features that make code safer and more expressive.
