

### Section 10.3: Array Length

- **Size Calculation**: You can calculate the size of an array using `sizeof`:

```c
int array[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
size_t size = sizeof(array);  // Total size in bytes
size_t length = sizeof(array) / sizeof(array[0]);  // Number of elements
```

> **Important**: In most expressions, arrays decay into pointers, which lose the size information. For example, if you pass an array to a function, you must pass its size separately.

- **Example: Getting the Last Element**:

```c
int get_last(int input[], size_t length) {
    return input[length - 1];
}

int array[] = {1, 2, 3, 4, 5};
size_t length = sizeof(array) / sizeof(array[0]);
int last = get_last(array, length);
```

> **Common Mistake**: Attempting to determine array size from a pointer inside a function is incorrect:

```c
int BAD_get_last(int input[]) {
    size_t length = sizeof(input) / sizeof(input[0]);  // Wrong! This will not work
    return input[length - 1];
}
```



In C, it's **not possible** to determine the size of an array inside a function without explicitly passing the size. This is because when an array is passed to a function, it decays into a pointer, and the information about the number of elements is lost.
You cannot determine the size of an array **by iterating through it** inside a function unless there is a **sentinel value** (like `-1` for integer arrays or `'\0'` for strings) that marks the end of the array. This is because when you pass an array to a function, it decays into a pointer, losing all information about its length.
### Why Iterating Doesn't Work Without Size Information:
When an array is passed to a function, the function only knows the address of the first element of the array (due to pointer decay). There is no built-in way to detect the length of the array from the pointer itself. 

Without some **extra information**, like:
- **Explicit array size** (passed as a parameter),
- **Sentinel value** (special value marking the end of the array),

### Why You Can't Determine Array Size Without Passing It:
1. **Array Decay**: When an array is passed to a function, it decays to a pointer. For example, `int arr[]` in a function is treated as `int* arr`. You no longer know how many elements are in the array—just where the first element is.
   
2. **`sizeof` Won't Work**: Since the function receives a pointer, using `sizeof` on the array inside the function will only give the size of the pointer (4 bytes on a 32-bit system or 8 bytes on a 64-bit system), not the size of the original array.

```c
int BAD_size(int arr[]) {
    return sizeof(arr);  // This will give the size of the pointer, not the array
}
```

3. **Null Terminators (for strings)**: In the case of strings, you can determine the length of a character array using the null terminator `'\0'`, but this doesn't work for arrays of numbers or other types.

### Possible Approaches:
The only way to know the size of an array without explicitly passing the size is if the array itself contains some metadata, like a **special sentinel value**, or if it's a global variable and you access the size from there. But, this is not efficient or ideal.

### Sentinel Value Approach:
If you're working with an array where a specific value (called a "sentinel") indicates the end of the array, you could design a function to recognize that value. For example, for arrays of integers, you could agree that `-1` represents the end of the array:

```c
int get_size_with_sentinel(int arr[]) {
    int i = 0;
    while (arr[i] != -1) {  // Sentinel value -1 indicates end of array
        i++;
    }
    return i;
}
```

Usage:

```c
int arr[] = {1, 2, 3, 4, 5, -1};  // Array with sentinel value -1
int size = get_size_with_sentinel(arr);  // Will return 5
```

### Global Array Approach:
If the array is declared globally, you could use `sizeof` in the same scope as the array declaration and store the result in a global variable:

```c
int arr[] = {1, 2, 3, 4, 5};  // Global array
size_t array_size = sizeof(arr) / sizeof(arr[0]);  // Calculate size globally

int get_size() {
    return array_size;  // Use the globally stored size
}
```

### Why You Still Need to Pass Size:
For most cases, especially in real-world programming, the **best practice** is to **pass the size of the array** when calling the function. This avoids all the limitations and risks associated with array decay and allows you to work with arrays safely inside functions.



---

### Summary
- Arrays in C are fixed-length and stored contiguously in memory.
- Initialization can be done partially or explicitly with designated initializers.
- Iterating efficiently through multi-dimensional arrays by respecting the memory layout (row-major order) can greatly improve performance.
- Always remember that arrays decay into pointers in most contexts, so their length information must be passed separately when needed.

