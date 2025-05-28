Here is a 12-question quiz based on the `int* a` vs `int *a` concept in C:

---

### Pointer Declarations Quiz

#### Question 1:
What does `int* a;` mean in C?
- [ ] A. `a` is a pointer to a character.
- [ ] B. `a` is a pointer to an integer.
- [ ] C. `a` is an integer.
- [ ] D. `a` is an array of integers.

#### Question 2:
What does `int *a;` mean in C?
- [ ] A. `a` is a pointer to an integer.
- [ ] B. `a` is a reference to an integer.
- [ ] C. `a` is an integer.
- [ ] D. `a` is a pointer to a float.

#### Question 3:
Is there any functional difference between `int* a;` and `int *a;`?
- [ ] A. Yes, they have different behaviors.
- [ ] B. No, both are functionally identical.
- [ ] C. Yes, but only in certain compilers.
- [ ] D. Yes, `int* a` is a pointer, and `int *a` is an integer.

#### Question 4:
Which of the following is considered a best practice when declaring multiple pointers?
- [ ] A. Declaring multiple pointers on the same line.
- [ ] B. Declaring each pointer on a separate line.
- [ ] C. Declaring pointers without using `*`.
- [ ] D. Using `int**` for pointer declarations.

#### Question 5:
What does the following declaration do?
```c
int *a, b;
```
- [ ] A. Declares both `a` and `b` as pointers to integers.
- [ ] B. Declares `a` as a pointer to an integer and `b` as a regular integer.
- [ ] C. Declares both `a` and `b` as regular integers.
- [ ] D. Declares both `a` and `b` as pointers to floats.

#### Question 6:
What does the following declaration do?
```c
int *a, *b;
```
- [ ] A. Declares `a` as a pointer to an integer and `b` as an integer.
- [ ] B. Declares both `a` and `b` as regular integers.
- [ ] C. Declares both `a` and `b` as pointers to integers.
- [ ] D. Declares `a` as a pointer to a float and `b` as a pointer to an integer.

#### Question 7:
Which style is preferred to avoid confusion when declaring multiple variables in C?
- [ ] A. Declaring all variables on the same line with `*`.
- [ ] B. Declaring each pointer separately.
- [ ] C. Using `int*` for all variables.
- [ ] D. Using `int *a` for arrays and `int*` for pointers.

#### Question 8:
Which style emphasizes that `a` is a pointer in the following declaration?
```c
int* a;
```
- [ ] A. Emphasizes the type `int`.
- [ ] B. Emphasizes that `a` is a pointer.
- [ ] C. Emphasizes the pointer size.
- [ ] D. Emphasizes the variable name `a`.

#### Question 9:
Which style aligns the `*` symbol with the variable name to show that the `*` binds to the variable?
- [ ] A. `int a*;`
- [ ] B. `int* a;`
- [ ] C. `int *a;`
- [ ] D. `int *a*;`

#### Question 10:
Why is it important to place the `*` next to each variable when declaring multiple pointers?
- [ ] A. To prevent memory leaks.
- [ ] B. To make the code more readable and avoid confusion.
- [ ] C. To follow compiler requirements.
- [ ] D. To initialize the pointers automatically.

#### Question 11:
Which declaration is more readable and less prone to confusion when dealing with pointers?
- [ ] A. `int *a, *b;`
- [ ] B. `int* a, b;`
- [ ] C. `int a, b;`
- [ ] D. `int** a, *b;`

#### Question 12:
What is the main reason programmers use `int *a` instead of `int* a`?
- [ ] A. To highlight that `*` is a separate operator.
- [ ] B. To avoid ambiguity when declaring multiple variables.
- [ ] C. To emphasize that `*` binds with `int`.
- [ ] D. To save space in the code.

---

Let me know if you'd like answers provided at the end or additional examples!


Here are the answers to the quiz:

1. B
2. A
3. B
4. B
5. B
6. C
7. B
8. B
9. C
10. B
11. A
12. B