---
title: "Multidimensional Arrays in C++"
---

Multidimensional arrays are essentially "arrays of arrays." They are used to store data in a tabular format, like a matrix or a grid.

### C-Style Multidimensional Arrays

C++ supports C-style multidimensional arrays, which are fixed in size at compile time.

**Declaration and Initialization**

```cpp
// Declare a 2D array (3 rows, 4 columns)
int matrix[3][4];

// Declare and initialize a 2D array
int identity_matrix[3][3] = {
    {1, 0, 0},
    {0, 1, 0},
    {0, 0, 1}
};

// You can omit the inner braces
int another_matrix[2][3] = {1, 2, 3, 4, 5, 6};
```

**Accessing Elements**

You use multiple subscript operators `[]` to access elements.

```cpp
// Access the element at row 1, column 2
int element = identity_matrix[1][2]; // This would be 0
```

### The C++ Way: Nested Containers

While C-style multidimensional arrays work, the modern C++ approach is to use nested standard containers, most commonly a `std::vector` of `std::vector`s. This provides much greater flexibility and safety.

**`std::vector<std::vector<int>>`**

This creates a dynamic 2D array where the number of rows and the length of each row can be changed at runtime.

```cpp
#include <iostream>
#include <vector>

int main() {
    // Create a 2D vector with 3 rows and 4 columns, initialized to 0
    int rows = 3;
    int cols = 4;
    std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols, 0));

    // Initialize with values
    matrix = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };

    // Add a new row
    matrix.push_back({13, 14, 15, 16});

    // Print the elements
    for (size_t i = 0; i < matrix.size(); ++i) {
        for (size_t j = 0; j < matrix[i].size(); ++j) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << std::endl;
    }

    return 0;
}
```

**Advantages of `std::vector<std::vector<T>>`:**

-   **Dynamic Size**: You can add or remove rows and columns easily.
-   **Safety**: Provides bounds checking with `.at()`.
-   **Ease of Use**: Integrates well with standard algorithms and range-based for loops.

**Disadvantage:**

-   **Performance**: The rows are not guaranteed to be contiguous in memory. Each row is a separate heap allocation. For performance-critical applications where cache locality matters (like image processing or scientific computing), this might not be ideal.

### For High Performance: A Flattened 1D Vector

To get the performance of a contiguous C-style array with the safety and convenience of `std::vector`, you can simulate a 2D array with a single, "flattened" 1D `std::vector`.

You manually calculate the index for each element.

```cpp
#include <iostream>
#include <vector>

int main() {
    int rows = 3;
    int cols = 4;
    std::vector<int> matrix(rows * cols);

    // Access element at (row, col) using index: row * num_cols + col
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            matrix[i * cols + j] = i * 10 + j;
        }
    }

    // Print the element at (1, 2)
    std::cout << "Element at (1, 2) is: " << matrix[1 * cols + 2] << std::endl;

    return 0;
}
```

This approach combines the best of both worlds: the memory is a single contiguous block (great for cache performance), and you still get the benefits of `std::vector` (automatic memory management, dynamic resizing if needed).

### Summary

| Method                                | Pros                                       | Cons                                     | Best For                                      |
|---------------------------------------|--------------------------------------------|------------------------------------------|-----------------------------------------------|
| **C-Style Array** (`int[][]`)         | Contiguous memory, fast access             | Fixed size, unsafe, decays to pointer    | Legacy code, low-level programming.           |
| **Nested Vector** (`vector<vector<int>>`)| Dynamic size, easy to use, safe          | Rows not contiguous, potential overhead  | General-purpose, when flexibility is key.     |
| **Flattened Vector** (`vector<int>`)  | Contiguous memory, fast, safe, flexible    | Requires manual index calculation        | High-performance computing, matrices.         |
