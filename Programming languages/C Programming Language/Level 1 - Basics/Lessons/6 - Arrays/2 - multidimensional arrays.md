Yes, the concepts of declaring and using multidimensional arrays in C are similar to those in C++. Let's look at examples in C for both methods:

### 1. Array of Arrays

This is the typical way to declare and use multidimensional arrays in C.

```c
#include <stdio.h>

int main() {
    // Declare a 2D array of size 3x3
    int array[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    // Print the elements of the array
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }

    return 0;
}
```

### 2. Array of Pointers

This method is more flexible, where each row is dynamically allocated.

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Number of rows and columns
    int rows = 3;
    int cols = 3;

    // Declare an array of pointers
    int** array = (int**)malloc(rows * sizeof(int*));

    // Allocate memory for each row
    for (int i = 0; i < rows; ++i) {
        array[i] = (int*)malloc(cols * sizeof(int));
    }

    // Initialize the array
    int value = 1;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            array[i][j] = value++;
        }
    }

    // Print the elements of the array
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }

    // Deallocate memory
    for (int i = 0; i < rows; ++i) {
        free(array[i]);
    }
    free(array);

    return 0;
}
```

### Explanation

1. **Array of Arrays**:
   - This method is straightforward and easy to use.
   - The size of the array is fixed at compile time.
   - Memory is allocated on the stack.

2. **Array of Pointers**:
   - This method is more flexible because the size of the array can be determined at runtime.
   - Memory is allocated on the heap using `malloc`.
   - You need to manually deallocate the memory using `free` to avoid memory leaks.

Both methods have their use cases, and the choice between them depends on the specific requirements of your program. The main difference between C and C++ in this context is the syntax for memory allocation and deallocation (`malloc`/`free` in C vs. `new`/`delete` in C++).