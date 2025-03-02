
## Pointers in C Quiz

1. What is a pointer in C programming?
   - [x] a) A variable that stores a memory address.
   - [ ] b) A function that modifies variables.
   - [ ] c) A type of operator for comparing values.

2. Which operator is used to get the address of a variable?
   - [ ] a) *
   - [x] b) &
   - [ ] c) %

3. How do you declare a pointer to an integer in C?
   - [ ] a) `int a;`
   - [x] b) `int *a;`
   - [ ] c) `*int a;`

4. What does dereferencing a pointer mean?
   - [ ] a) Accessing the address stored in the pointer.
   - [x] b) Accessing the value stored at the memory address the pointer points to.
   - [ ] c) Modifying the pointer’s type.

5. What will `*a` do if `a` is a pointer?
   - [ ] a) It prints the address of `a`.
   - [x] b) It prints the value stored at the address in `a`.
   - [ ] c) It modifies the value of `a`.

6. Which of the following shows how to assign a pointer `a` to the address of variable `b`?
   - [x] a) `a = &b;`
   - [ ] b) `*a = &b;`
   - [ ] c) `a = *b;`

7. What is the output of `printf("%p", &b);` if `b` is a variable?
   - [ ] a) The value of `b`.
   - [x] b) The address of `b`.
   - [ ] c) The size of `b`.

8. What is a major use case of pointers in C?
   - [ ] a) To perform logical operations.
   - [x] b) For dynamic memory allocation and passing by reference.
   - [ ] c) To handle syntax errors.

9. In the function `void swap(int *a, int *b)`, what do `a` and `b` represent?
   - [ ] a) Integer variables.
   - [x] b) Memory addresses of integer variables.
   - [ ] c) Temporary variables for computation.

10. How does the address-of operator `&` work?
   - [ ] a) It multiplies the memory addresses.
   - [x] b) It retrieves the memory address of a variable.
   - [ ] c) It increments the value at a memory location.

11. How can a pointer modify a variable it points to?
   - [ ] a) By changing the pointer's value.
   - [x] b) By dereferencing the pointer and assigning a new value.
   - [ ] c) By using the address-of operator.

12. What happens if a pointer is not initialized before being dereferenced?
   - [ ] a) The program will print an error.
   - [x] b) It will point to a random memory location, causing undefined behavior.
   - [ ] c) The pointer will automatically point to zero.

13. What is the output of the following code snippet?
```c
int x = 100;
int *p = &x;
*p = 200;
printf("%d", x);
```
   - [ ] a) 100
   - [x] b) 200
   - [ ] c) Error

14. What does `void *` represent in C?
   - [ ] a) A pointer to an integer.
   - [x] b) A pointer to any data type.
   - [ ] c) A null pointer.

15. Why must pointers be handled carefully in C?
   - [x] a) They can cause segmentation faults or memory corruption.
   - [ ] b) They automatically free memory.
   - [ ] c) They do not allow dereferencing.

### Answers:
1. a  
2. b  
3. b  
4. b  
5. b  
6. a  
7. b  
8. b  
9. b  
10. b  
11. b  
12. b  
13. b  
14. b  
15. a  