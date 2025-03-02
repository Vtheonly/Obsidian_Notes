Here is a 12-question quiz on the `malloc` function in C with four options for each question:

---

### `malloc` Function Quiz

#### Question 1:
What does the `malloc` function do in C?
- [ ] A. Allocates memory from the stack.
- [ ] B. Allocates memory from the heap and initializes it to zero.
- [ ] C. Allocates memory from the heap and leaves it uninitialized.
- [ ] D. Allocates memory for strings only.

#### Question 2:
What type does `malloc` return?
- [ ] A. `int*`
- [ ] B. `char*`
- [ ] C. `void*`
- [ ] D. `double*`

#### Question 3:
In the following code, what is the correct way to cast the pointer returned by `malloc` to an integer pointer?
```c
void* ptr = malloc(10 * sizeof(int));
```
- [ ] A. `(int) malloc(10 * sizeof(int));`
- [ ] B. `(int*) malloc(10 * sizeof(int));`
- [ ] C. `malloc((int*) 10 * sizeof(int));`
- [ ] D. No casting is required.

#### Question 4:
What happens if `malloc` fails to allocate the requested memory?
- [ ] A. It returns a garbage value.
- [ ] B. It returns a pointer to random memory.
- [ ] C. It returns `NULL`.
- [ ] D. The program crashes.

#### Question 5:
Why is it necessary to call `free` after using `malloc`?
- [ ] A. To avoid memory fragmentation.
- [ ] B. To avoid memory leaks by releasing dynamically allocated memory.
- [ ] C. To reset the memory to zero.
- [ ] D. To reinitialize the allocated memory.

#### Question 6:
Which library must be included to use the `malloc` function in C?
- [ ] A. `<stdio.h>`
- [ ] B. `<malloc.h>`
- [ ] C. `<stdlib.h>`
- [ ] D. `<string.h>`

#### Question 7:
What does the following code do?
```c
int* arr = (int*) malloc(5 * sizeof(int));
```
- [ ] A. Allocates memory for 5 integers on the stack.
- [ ] B. Allocates memory for 5 integers on the heap.
- [ ] C. Allocates memory for 5 characters.
- [ ] D. Initializes 5 integers to zero.

#### Question 8:
Which of the following is true about the memory allocated by `malloc`?
- [ ] A. It is always zero-initialized.
- [ ] B. It contains random, uninitialized values.
- [ ] C. It is initialized to negative values.
- [ ] D. It cannot be used with arrays.

#### Question 9:
In the following code, how many bytes of memory are allocated by `malloc`?
```c
float* arr = (float*) malloc(10 * sizeof(float));
```
- [ ] A. 10 bytes
- [ ] B. 20 bytes
- [ ] C. 40 bytes
- [ ] D. 80 bytes

#### Question 10:
What is the purpose of the following check in a `malloc` call?
```c
if (arr == NULL) {
    printf("Memory not allocated.\n");
    return 1;
}
```
- [ ] A. To ensure the memory allocated is initialized.
- [ ] B. To check if `malloc` failed to allocate memory.
- [ ] C. To check if the pointer points to an array.
- [ ] D. To free the memory if the pointer is `NULL`.

#### Question 11:
What does `calloc` do differently from `malloc`?
- [ ] A. It allocates memory and zero-initializes it.
- [ ] B. It allocates memory only for arrays.
- [ ] C. It allocates memory on the stack.
- [ ] D. It allocates memory without initializing it.

#### Question 12:
What happens if you do not call `free` after using `malloc`?
- [ ] A. The memory is automatically released when the program exits.
- [ ] B. The memory will be garbage collected.
- [ ] C. The memory is leaked, potentially causing a memory leak.
- [ ] D. The program will crash.

---

Answers will be provided in a list format at the end of the file if needed!


Here are the answers to the quiz on `malloc`:

1. B
2. D
3. C
4. B
5. D
6. A
7. C
8. A
9. D
10. C
11. D
12. B