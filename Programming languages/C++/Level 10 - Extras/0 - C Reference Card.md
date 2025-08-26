---
title: "C++ Core Language and Standard Library Reference"
---

## Program Structure and Functions

-   **Function Prototype**: `return_type function_name(type1 arg1, type2 arg2);`
-   **Variable Declaration**: `type name;` or `type name = initial_value;`
-   **Main Function**: `int main() { /* ... */ }` or `int main(int argc, char* argv[]) { /* ... */ }`
-   **Function Definition**:
    ```cpp
    return_type function_name(type1 arg1, type2 arg2) {
        // ... statements ...
        return value;
    }
    ```
-   **Comments**: `// Single-line` or `/* Multi-line */`
-   **Terminate Execution**: `return 0;` from `main` or `exit(code);` from `<cstdlib>`

## C++ Preprocessor

-   **Include Standard Library**: `#include <iostream>`
-   **Include Local File**: `#include "my_header.h"`
-   **Constant Macro**: `#define PI 3.14159`
-   **Function-like Macro**: `#define SQUARE(x) ((x) * (x))`
-   **Conditional Compilation**: `#if`, `#else`, `#elif`, `#endif`, `#ifdef`, `#ifndef`

## Fundamental Data Types

-   **Boolean**: `bool` (`true`, `false`)
-   **Character**: `char`, `wchar_t`, `char16_t`, `char32_t`
-   **Integer**: `short`, `int`, `long`, `long long` (can be `signed` or `unsigned`)
-   **Floating-Point**: `float`, `double`, `long double`
-   **Void**: `void` (represents the absence of a type)
-   **Null Pointer**: `nullptr` (C++11)

## Compound Types and User-Defined Types

-   **Pointer**: `type* name;`
-   **Reference**: `type& name = existing_variable;`
-   **Array**: `type name[size];`
-   **Enumeration**: `enum class Color { Red, Green, Blue };` (scoped enum, C++11)
-   **Struct**: `struct Point { double x; double y; };`
-   **Class**: `class MyClass { /* ... */ };`
-   **Type Alias**: `using Number = int;` (preferred over `typedef`)
-   **Size of Type/Object**: `sizeof(type)` or `sizeof(expression)`

## Initialization

-   **C-style**: `int x = 10;`
-   **Constructor**: `std::string s("hello");`
-   **Uniform Initialization (C++11)**: `int y{20};`, `std::vector<int> v{1, 2, 3};`

## Literals

-   **Integer**: `42`, `052` (octal), `0x2A` (hex), `0b101010` (binary, C++14)
-   **Suffixes**: `u` (unsigned), `l` (long), `ll` (long long)
-   **Floating-Point**: `3.14`, `3.14f` (float), `3.14L` (long double), `6.022e23`
-   **Character**: `'a'`, `L'β'`, `'
'`
-   **String**: `"Hello"`, `L"World"`, `R"(Raw string data)"` (raw, C++11)
-   **Boolean**: `true`, `false`
-   **Pointer**: `nullptr`

## Pointers, References, and Structs/Classes

-   **Pointer Declaration**: `type* name;`
-   **Reference Declaration**: `type& name = variable;`
-   **Address-of**: `&variable`
-   **Dereference**: `*pointer`
-   **Member Access (object)**: `object.member`
-   **Member Access (pointer)**: `pointer->member`
-   **Generic Pointer**: `void*`

## Operators (A Selection)

-   **Arithmetic**: `+`, `-`, `*`, `/`, `%`
-   **Increment/Decrement**: `++`, `--` (pre and post)
-   **Relational & Comparison**: `==`, `!=`, `>`, `<`, `>=`, `<=`
-   **Logical**: `!`, `&&`, `||`
-   **Bitwise**: `&`, `|`, `^`, `~`, `<<`, `>>`
-   **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
-   **Ternary Conditional**: `condition ? expr1 : expr2`
-   **Casts**: `static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`

## Control Flow

-   **Conditional**: `if`, `else if`, `else`
-   **Switch**: `switch`, `case`, `break`, `default`
-   **Loops**: `while`, `do-while`, `for`
-   **Range-based for loop (C++11)**: `for (auto& element : container)`
-   **Loop Control**: `break`, `continue`
-   **Function Return**: `return value;`

## C++ Standard Library (A Glimpse)

-   **`<iostream>`**: For stream-based input/output (`std::cin`, `std::cout`).
-   **`<string>`**: `std::string` class for text manipulation.
-   **`<vector>`**: `std::vector` dynamic array.
-   **`<array>`**: `std::array` fixed-size array.
-   **`<map>`**: `std::map` key-value store (ordered).
-   **`<unordered_map>`**: `std::unordered_map` key-value store (hashed).
-   **`<algorithm>`**: `std::sort`, `std::find`, `std::for_each`, etc.
-   **`<memory>`**: Smart pointers (`std::unique_ptr`, `std::shared_ptr`).
-   **`<stdexcept>`**: Standard exception classes like `std::runtime_error`.
-   **`<thread>`**: For creating and managing threads.
-   **`<chrono>`**: For time and duration.
-   **`<filesystem>`**: For interacting with the file system (C++17).