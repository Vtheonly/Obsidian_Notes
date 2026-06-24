---
title: "Array Size in C++"
---

Determining the number of elements in an array is a common task. How you do it in C++ depends on whether you are using a C-style array or a modern C++ container like `std::array` or `std::vector`.

### C-Style Arrays

For a raw C-style array, you can calculate the number of elements by dividing the total size of the array in bytes by the size of a single element.

```cpp
#include <iostream>

int main() {
    int numbers[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    // Calculate the number of elements
    size_t length = sizeof(numbers) / sizeof(numbers[0]);

    std::cout << "Total size of array: " << sizeof(numbers) << " bytes" << std::endl;
    std::cout << "Size of one element: " << sizeof(numbers[0]) << " bytes" << std::endl;
    std::cout << "Number of elements: " << length << std::endl;

    return 0;
}
```

**The Pitfall: Array Decay**

This `sizeof` trick has a major limitation: it only works when the array has not "decayed" into a pointer. When you pass a C-style array to a function, it decays into a pointer to its first element, and the size information is lost.

```cpp
void print_size(int arr[]) {
    // This will NOT work as expected!
    // sizeof(arr) will return the size of a pointer, not the array.
    size_t length = sizeof(arr) / sizeof(arr[0]); 
    std::cout << "Size inside function: " << length << std::endl; // Incorrect result
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    print_size(numbers); // The array decays to a pointer here
    return 0;
}
```

To correctly handle C-style arrays in functions, you must pass the size as a separate argument.

### The Modern C++ Way: `.size()`

Modern C++ containers like `std::array` and `std::vector` solve the problem of array decay by storing their size internally. You can easily and safely get the number of elements using the `.size()` member function.

#### `std::array`

`std::array` is for fixed-size arrays. Its size is known at compile-time.

```cpp
#include <iostream>
#include <array>

void print_array_size(const std::array<int, 5>& arr) {
    // .size() works perfectly inside functions!
    std::cout << "Array size: " << arr.size() << std::endl;
}

int main() {
    std::array<int, 5> my_array = {1, 2, 3, 4, 5};
    std::cout << "Array size: " << my_array.size() << std::endl;
    print_array_size(my_array);
    return 0;
}
```

#### `std::vector`

`std::vector` is for dynamic arrays. Its size can change at runtime.

```cpp
#include <iostream>
#include <vector>

void print_vector_size(const std::vector<int>& vec) {
    std::cout << "Vector size: " << vec.size() << std::endl;
}

int main() {
    std::vector<int> my_vector = {10, 20, 30};
    my_vector.push_back(40);

    std::cout << "Vector size: " << my_vector.size() << std::endl;
    print_vector_size(my_vector);
    return 0;
}
```

### C++17 `std::size`

C++17 introduced `std::size`, a free function that can get the size of C-style arrays and standard containers in a uniform way.

```cpp
#include <iostream>
#include <vector>
#include <iterator> // For std::size

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    std::vector<int> my_vector = {10, 20, 30};

    std::cout << "Size of C-style array: " << std::size(numbers) << std::endl;
    std::cout << "Size of vector: " << std::size(my_vector) << std::endl;

    return 0;
}
```
Note that `std::size` still doesn't work for decayed pointers.

### Summary

-   For C-style arrays, use `sizeof(arr)/sizeof(arr[0])`, but be aware of array decay.
-   For modern C++ code, **always prefer `std::array` or `std::vector`** and use their `.size()` member function to get the number of elements. This is the safest and most idiomatic approach.