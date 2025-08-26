---
title: "Function Pointers in C++"
---

### Understanding Function Pointers

A function pointer is a pointer that, instead of storing the memory address of a variable, stores the memory address of a function. This allows you to treat functions like any other data—you can store them, pass them as arguments to other functions, and call them dynamically.

### Declaring and Using Function Pointers

To declare a function pointer, you must specify the function's return type and parameter types.

**Syntax**: `return_type (*pointer_name)(parameter_types);`

```cpp
#include <iostream>

// A function we want to point to
int add(int x, int y) {
    return x + y;
}

int subtract(int x, int y) {
    return x - y;
}

int main() {
    // 1. Declare a function pointer
    int (*operation)(int, int);

    // 2. Assign a function to the pointer
    operation = &add; // or simply 'operation = add;'

    // 3. Call the function through the pointer
    int result = operation(10, 5); // Implicitly dereferences and calls add()
    std::cout << "Result of add: " << result << std::endl; // Output: 15

    // Reassign to another compatible function
    operation = &subtract;
    result = operation(10, 5);
    std::cout << "Result of subtract: " << result << std::endl; // Output: 5

    return 0;
}
```

### Why Use Function Pointers?

Function pointers are powerful for creating flexible and generic code.

1.  **Callbacks**: Pass a function as an argument to another function. This is common in event-driven programming or for customizing algorithms.
2.  **Strategy Pattern**: Select an algorithm or behavior at runtime.
3.  **State Machines**: Use an array of function pointers to transition between states.

### Example: Using Function Pointers for Callbacks

A classic example is a generic sorting function that takes a comparison function as an argument.

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // For std::sort

// Comparison function for ascending order
bool ascending(int a, int b) {
    return a < b;
}

// Comparison function for descending order
bool descending(int a, int b) {
    return a > b;
}

// A function that takes a function pointer as an argument
void custom_sort(std::vector<int>& vec, bool (*compare_func)(int, int)) {
    // A simple bubble sort for demonstration
    for (size_t i = 0; i < vec.size() - 1; ++i) {
        for (size_t j = 0; j < vec.size() - i - 1; ++j) {
            if (compare_func(vec[j], vec[j + 1])) {
                std::swap(vec[j], vec[j + 1]);
            }
        }
    }
}

int main() {
    std::vector<int> numbers = {5, 2, 8, 1, 9};

    // The C standard library qsort uses this pattern
    // std::sort in C++ uses templates and function objects, which are often preferred

    custom_sort(numbers, &descending);

    for (int n : numbers) {
        std::cout << n << " "; // Output: 1 2 5 8 9 (if sorted with ascending logic)
    }
    std::cout << std::endl;

    return 0;
}
```

### Modern C++ Alternatives

While function pointers are a core concept, modern C++ provides more powerful and safer alternatives that are often preferred:

1.  **Function Objects (Functors)**: A class or struct that overloads the `operator()`. It can hold state, unlike a regular function.

2.  **Lambdas (C++11)**: Anonymous, in-place functions that are concise and can capture variables from their surrounding scope. Lambdas are the most common and idiomatic way to handle callbacks in modern C++.

3.  **`std::function` (C++11)**: A general-purpose, polymorphic function wrapper. `std::function` can store, copy, and invoke any "callable" target—a function pointer, lambda, or functor.

**Example with `std::function` and a Lambda:**

```cpp
#include <iostream>
#include <vector>
#include <functional> // For std::function

void perform_operation(const std::vector<int>& vec, const std::function<void(int)>& op) {
    for (int x : vec) {
        op(x);
    }
}

int main() {
    std::vector<int> data = {1, 2, 3};

    // Use a lambda to print each element doubled
    auto double_and_print = [](int val) {
        std::cout << val * 2 << " ";
    };

    perform_operation(data, double_and_print);
    std::cout << std::endl;

    return 0;
}
```

### Summary

Function pointers are a fundamental concept for enabling dynamic behavior in C++. However, for new code, you should **prefer modern C++ alternatives like lambdas and `std::function`**. They are more expressive, safer, and can handle more complex scenarios (like capturing state) than raw function pointers.