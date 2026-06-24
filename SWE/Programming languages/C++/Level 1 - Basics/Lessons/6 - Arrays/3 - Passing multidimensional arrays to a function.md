---
title: "Passing Multidimensional Arrays to Functions in C++"
---

When working with multidimensional arrays in C++, it's important to know how to pass them to functions correctly. The method you choose depends on whether you are using C-style arrays or modern C++ containers.

### 1. Passing C-Style Multidimensional Arrays

When you pass a C-style multidimensional array to a function, you must specify the size of all but the first dimension. This is because the compiler needs this information to correctly calculate the memory offset of elements.

```cpp
#include <iostream>

// The size of the second dimension (columns) must be specified.
void print_matrix(int matrix[][3], int rows) {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < 3; ++j) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    int my_matrix[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    print_matrix(my_matrix, 2);
    return 0;
}
```

**Using Templates for Generality (C++)**

A more generic C++ approach is to use templates. This allows you to write a function that can accept C-style arrays of any size without hardcoding the dimensions.

```cpp
#include <iostream>

// N and M are deduced by the compiler
template <size_t N, size_t M>
void print_matrix_template(int (&matrix)[N][M]) {
    for (size_t i = 0; i < N; ++i) {
        for (size_t j = 0; j < M; ++j) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    int my_matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};
    print_matrix_template(my_matrix);
    return 0;
}
```
Here, the function takes the array by reference (`&matrix`) to prevent it from decaying into a pointer, which allows the compiler to deduce its dimensions `N` and `M`.

### 2. The Modern C++ Way: Passing Containers

The best practice in modern C++ is to use standard library containers like `std::vector` or `std::array` and pass them to functions, preferably by reference to avoid unnecessary copies.

#### Passing a `std::vector<std::vector<int>>`

This is the most flexible approach, as the dimensions can be determined at runtime.

```cpp
#include <iostream>
#include <vector>

// Pass by const reference to avoid copying the vector
void print_vector_matrix(const std::vector<std::vector<int>>& matrix) {
    for (size_t i = 0; i < matrix.size(); ++i) {
        for (size_t j = 0; j < matrix[i].size(); ++j) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    std::vector<std::vector<int>> vec_matrix = {
        {1, 2, 3},
        {4, 5, 6}
    };
    print_vector_matrix(vec_matrix);
    return 0;
}
```

#### Passing a `std::array<std::array<int, M>, N>`

If the dimensions of your matrix are fixed and known at compile time, `std::array` is a more efficient choice.

```cpp
#include <iostream>
#include <array>

// Template allows this function to work for any size of std::array
template <size_t Rows, size_t Cols>
void print_array_matrix(const std::array<std::array<int, Cols>, Rows>& matrix) {
    for (const auto& row : matrix) {
        for (const auto& element : row) {
            std::cout << element << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    std::array<std::array<int, 3>, 2> arr_matrix = {{ {1, 2, 3}, {4, 5, 6} }};
    print_array_matrix(arr_matrix);
    return 0;
}
```

### Summary

-   **C-Style Arrays**: Require you to specify all but the first dimension in the function signature. Use templates to make these functions more generic.
-   **`std::vector`**: The most flexible option. Pass by `const` reference (`const&`) to avoid expensive copies.
-   **`std::array`**: The most efficient option for fixed-size matrices. Pass by `const` reference or use templates for generic functions.

For new C++ code, **prefer passing standard containers like `std::vector` or `std::array`** over C-style arrays. They are safer, more expressive, and integrate seamlessly with the rest of the C++ Standard Library.