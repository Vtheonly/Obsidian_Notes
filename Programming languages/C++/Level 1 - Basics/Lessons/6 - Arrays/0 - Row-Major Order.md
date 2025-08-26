---
title: "Arrays in C++"
---

Arrays are a fundamental data structure in C++, representing a fixed-size, sequential collection of elements of the same type. C++ inherits C-style arrays and also provides a more modern, safer alternative in the Standard Library.

### C-Style Arrays

A C-style array is declared with a fixed size at compile time.

**Declaration and Initialization**

```cpp
// Declare an array of 10 integers
int c_array[10];

// Declare and initialize an array
int numbers[] = {1, 2, 3, 4, 5}; // Size is automatically deduced to 5

// Initialize all elements to zero
int zeros[10] = {0};

// Designated initializers (C++20)
int designated[5] = {[2] = 5, [1] = 2, [4] = 9}; // {0, 2, 5, 0, 9}
```

**Accessing Elements**

Elements are accessed using the subscript operator `[]` with a zero-based index.

```cpp
int first_element = numbers[0]; // Accesses the first element (1)
numbers[1] = 20; // Modifies the second element
```

**Row-Major Order and Iteration**

Like in C, C++ multi-dimensional arrays are stored in **row-major order**. This means that when iterating over a 2D array, it is more cache-efficient to iterate row by row.

```cpp
#define ROWS 100
#define COLS 100
int matrix[ROWS][COLS];

// Efficient iteration (row by row)
for (int i = 0; i < ROWS; ++i) {
    for (int j = 0; j < COLS; ++j) {
        matrix[i][j] = 0;
    }
}

// Inefficient iteration (column by column - causes cache misses)
for (int j = 0; j < COLS; ++j) {
    for (int i = 0; i < ROWS; ++i) {
        matrix[i][j] = 0;
    }
}
```

### The C++ Way: `std::array` and `std::vector`

While C-style arrays are available, modern C++ strongly encourages the use of container classes from the Standard Library, which are safer and more powerful.

#### `std::array` (C++11)

`std::array` is a thin, type-safe wrapper around a C-style array. It provides the performance of a C-style array but with the benefits of a standard container.

-   **Fixed size**, known at compile-time.
-   **Bounds checking** with the `.at()` member function.
-   Behaves like a standard container (has `.size()`, `.begin()`, `.end()`).

```cpp
#include <iostream>
#include <array>

int main() {
    std::array<int, 5> my_array = {1, 2, 3, 4, 5};

    std::cout << "Size: " << my_array.size() << std::endl;

    // Range-based for loop (easy and safe)
    for (int element : my_array) {
        std::cout << element << " ";
    }
    std::cout << std::endl;

    // Bounds-checked access
    try {
        std::cout << my_array.at(10) << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
```

#### `std::vector`

`std::vector` is a dynamic array that can grow or shrink in size at runtime. It is the most commonly used container in C++ for holding sequences of elements.

-   **Dynamic size**.
-   Manages its own memory automatically (no manual `new`/`delete`).
-   Provides a rich set of member functions for adding, removing, and accessing elements.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> my_vector = {10, 20, 30};

    my_vector.push_back(40); // Add an element to the end
    my_vector.push_back(50);

    std::cout << "Size: " << my_vector.size() << std::endl;

    for (int element : my_vector) {
        std::cout << element << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

### Summary

| Feature             | C-Style Array (`int[]`) | `std::array`              | `std::vector`             |
|---------------------|-------------------------|---------------------------|---------------------------|
| **Size**            | Fixed, compile-time     | Fixed, compile-time       | Dynamic, run-time         |
| **Memory**          | Stack (usually)         | Stack (usually)           | Heap                      |
| **Size Discovery**  | Lost on decay to pointer| `.size()` member function | `.size()` member function |
| **Bounds Checking** | No (unsafe)             | Yes, with `.at()`         | Yes, with `.at()`         |
| **Usage**           | Legacy code, low-level  | Prefer over C-style arrays| Default choice for sequences|

For new C++ code, you should always prefer `std::vector` for dynamic-size arrays and `std::array` for fixed-size arrays over traditional C-style arrays.
