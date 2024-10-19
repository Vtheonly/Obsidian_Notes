### Quiz: Understanding Function Pointers in C

**Question 1:** What is the primary benefit of using function pointers in C?  
- [ ] A) To store large amounts of data  
- [ ] B) To enable indirect function calls and flexibility in choosing functions at runtime  
- [ ] C) To optimize the memory usage of variables  
- [ ] D) To make loops more efficient  
[[link_to_answer_at_end_of_file]]

**Question 2:** Which of the following correctly declares a function pointer that points to a function taking two integers and returning an integer?  
- [ ] A) `int fnPointer(int x, int y);`  
- [ ] B) `int *fnPointer(int, int);`  
- [ ] C) `int (*fnPointer)(int, int);`  
- [ ] D) `int (*fnPointer)();`  
[[link_to_answer_at_end_of_file]]

**Question 3:** How do you assign a function `myFunction` to a function pointer `fnPointer`?  
- [ ] A) `fnPointer = myFunction;`  
- [ ] B) `fnPointer = &myFunction;`  
- [ ] C) Both A and B are correct  
- [ ] D) `fnPointer = *myFunction;`  
[[link_to_answer_at_end_of_file]]

**Question 4:** What is the output of the following code?  
```c
int multiply(int x, int y) { return x * y; }
int (*fnPointer)(int, int) = multiply;
int result = fnPointer(3, 4);
```
- [ ] A) 3  
- [ ] B) 4  
- [ ] C) 7  
- [ ] D) 12  
[[link_to_answer_at_end_of_file]]

**Question 5:** Which of these is a use case for function pointers?  
- [ ] A) Storing multiple functions in an array for dynamic selection  
- [ ] B) Accessing memory outside the program's allocated space  
- [ ] C) Managing memory allocation for data structures  
- [ ] D) Implementing loops  
[[link_to_answer_at_end_of_file]]

**Question 6:** How do you call a function through a pointer named `fnPointer`?  
- [ ] A) `(*fnPointer)(args);`  
- [ ] B) `fnPointer(args);`  
- [ ] C) Both A and B  
- [ ] D) `fnPointer->(args);`  
[[link_to_answer_at_end_of_file]]

**Question 7:** What is a callback function?  
- [ ] A) A function that modifies global variables  
- [ ] B) A function that calls itself  
- [ ] C) A function passed as an argument to another function  
- [ ] D) A function that returns a pointer to another function  
[[link_to_answer_at_end_of_file]]

**Question 8:** What is the result of `operations[2](10, 2);` given this array of function pointers?  
```c
int subtract(int x, int y) { return x - y; }
int multiply(int x, int y) { return x * y; }
int divide(int x, int y) { return x / y; }

int (*operations[])(int, int) = {subtract, multiply, divide};
```
- [ ] A) 5  
- [ ] B) 20  
- [ ] C) 8  
- [ ] D) 10  
[[link_to_answer_at_end_of_file]]

**Question 9:** Which function pointer-related operation is not allowed?  
- [ ] A) Passing function pointers as arguments  
- [ ] B) Assigning functions to pointers  
- [ ] C) Performing arithmetic on function pointers  
- [ ] D) Using function pointers in arrays  
[[link_to_answer_at_end_of_file]]

**Question 10:** Why should you avoid excessive use of function pointers?  
- [ ] A) They are slower than regular function calls  
- [ ] B) They make code difficult to read and maintain  
- [ ] C) They are not compatible with C++  
- [ ] D) They increase the size of the executable  
[[link_to_answer_at_end_of_file]]

**Question 11:** What is the purpose of returning a function pointer from a function?  
- [ ] A) To optimize code for better memory usage  
- [ ] B) To dynamically choose a function based on conditions  
- [ ] C) To create a pointer to a data structure  
- [ ] D) To allocate memory for arrays  
[[link_to_answer_at_end_of_file]]

**Question 12:** Which of the following is a valid function pointer assignment in C?  
- [ ] A) `fnPointer = &myFunction();`  
- [ ] B) `fnPointer = myFunction;`  
- [ ] C) `&fnPointer = myFunction;`  
- [ ] D) `fnPointer = *myFunction;`  
[[link_to_answer_at_end_of_file]]

**Question 13:** What is the output of this code snippet?  
```c
int (*operation)(int, int) = selectOperation(2);
int result = operation(6, 5);
```
Assuming `selectOperation(2)` returns `multiply`.  
- [ ] A) 30  
- [ ] B) 1  
- [ ] C) 11  
- [ ] D) 12  
[[link_to_answer_at_end_of_file]]

**Question 14:** How do function pointers improve modularity in C code?  
- [ ] A) By reducing the number of variables  
- [ ] B) By allowing functions to change their return types dynamically  
- [ ] C) By enabling passing functions as arguments and changing behavior at runtime  
- [ ] D) By creating smaller executable files  
[[link_to_answer_at_end_of_file]]

**Question 15:** Which statement is true about function pointers and arrays?  
- [ ] A) Only one function pointer can be stored in an array  
- [ ] B) Array of function pointers must be of the same return type  
- [ ] C) You cannot call functions from a function pointer array  
- [ ] D) Function pointers cannot be assigned to arrays  
[[link_to_answer_at_end_of_file]]

---

### **Answers**
1. B) To enable indirect function calls and flexibility in choosing functions at runtime
2. C) `int (*fnPointer)(int, int);`
3. C) Both A and B are correct
4. D) 12
5. A) Storing multiple functions in an array for dynamic selection
6. C) Both A and B
7. C) A function passed as an argument to another function
8. A) 5
9. C) Performing arithmetic on function pointers
10. B) They make code difficult to read and maintain
11. B) To dynamically choose a function based on conditions
12. B) `fnPointer = myFunction;`
13. A) 30
14. C) By enabling passing functions as arguments and changing behavior at runtime
15. B) Array of function pointers must be of the same return type