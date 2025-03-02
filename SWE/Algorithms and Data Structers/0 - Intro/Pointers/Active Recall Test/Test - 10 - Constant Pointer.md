Here are 12 questions based on the differences between a **constant pointer** and a **pointer to a constant** in C, with answers provided at the end.

---

### Questions

**1.** What is a key characteristic of a constant pointer (`T* const ptr`)?
- [ ] A) It allows changing the address it points to.
- [ ] B) It allows modifying both the pointer address and the pointed value.
- [ ] C) It does not allow modifying the pointed value.
- [ ] D) It does not allow changing the address it points to.  
[[link_to_answer_1]]

**2.** Which of the following is correct for a `const T* ptr`?
- [ ] A) The pointer itself is constant.
- [ ] B) The pointed value is constant, but the pointer address can change.
- [ ] C) Both the pointer address and pointed value are constant.
- [ ] D) The pointer is constant but the pointed value can change.  
[[link_to_answer_2]]

**3.** What does `char* const ptr = &a;` allow?
- [ ] A) Changing the address stored in `ptr`.
- [ ] B) Changing the value of `a` through `ptr`.
- [ ] C) Changing both the address and the value.
- [ ] D) Changing neither the address nor the value.  
[[link_to_answer_3]]

**4.** In `const char* ptr = &a;`, which of the following is true?
- [ ] A) You can modify the value of `a` through `ptr`.
- [ ] B) `ptr` cannot point to another address.
- [ ] C) You can change what `ptr` points to.
- [ ] D) `ptr` is a constant pointer to a constant.  
[[link_to_answer_4]]

**5.** What does `const T* const ptr` signify?
- [ ] A) The value pointed to can change.
- [ ] B) Only the pointer itself is constant.
- [ ] C) The pointer can point to different addresses.
- [ ] D) Both the pointer and the pointed value are constant.  
[[link_to_answer_5]]

**6.** Which syntax allows a pointer to be constant, but not the value it points to?
- [ ] A) `const T* ptr`
- [ ] B) `T* const ptr`
- [ ] C) `const T* const ptr`
- [ ] D) `T* ptr`  
[[link_to_answer_6]]

**7.** If you declare `const int* ptr;`, what is restricted?
- [ ] A) Changing the address stored in `ptr`.
- [ ] B) Modifying the integer value `ptr` points to.
- [ ] C) Reassigning `ptr` to a different address.
- [ ] D) All operations with `ptr` are allowed.  
[[link_to_answer_7]]

**8.** Which of the following statements about `T* const ptr` is true?
- [ ] A) It points to a constant value of type `T`.
- [ ] B) It cannot change the pointed-to address after initialization.
- [ ] C) It cannot change the value at the pointed-to address.
- [ ] D) It is equivalent to `const T* ptr`.  
[[link_to_answer_8]]

**9.** What is the difference between `T* const ptr` and `const T* ptr`?
- [ ] A) `T* const ptr` prevents value modification, while `const T* ptr` prevents address change.
- [ ] B) `T* const ptr` allows changing the address but not the value.
- [ ] C) `const T* ptr` allows changing the address, but not the value.
- [ ] D) Both have the same behavior.  
[[link_to_answer_9]]

**10.** Which code snippet results in a compile-time error when modifying the value pointed to?
- [ ] A) `const int* ptr = &a; *ptr = 5;`
- [ ] B) `int* const ptr = &a; *ptr = 5;`
- [ ] C) `int* ptr = &a; *ptr = 5;`
- [ ] D) `const int* const ptr = &a;`  
[[link_to_answer_10]]

**11.** What type of pointer does `const T* const ptr` represent?
- [ ] A) A constant pointer to a modifiable value.
- [ ] B) A modifiable pointer to a constant value.
- [ ] C) A modifiable pointer to a modifiable value.
- [ ] D) A constant pointer to a constant value.  
[[link_to_answer_11]]

**12.** How can you modify the address stored in a pointer that is declared as `const T* ptr`?
- [ ] A) By directly changing the value of `T` through `ptr`.
- [ ] B) By reassigning `ptr` to a new address.
- [ ] C) By casting `ptr` to a non-constant pointer.
- [ ] D) It is not possible to change the address in this case.  
[[link_to_answer_12]]

---

### Answers

1. D) It does not allow changing the address it points to.
2. B) The pointed value is constant, but the pointer address can change.
3. B) Changing the value of `a` through `ptr`.
4. C) You can change what `ptr` points to.
5. D) Both the pointer and the pointed value are constant.
6. B) `T* const ptr`
7. B) Modifying the integer value `ptr` points to.
8. B) It cannot change the pointed-to address after initialization.
9. C) `const T* ptr` allows changing the address, but not the value.
10. A) `const int* ptr = &a; *ptr = 5;`
11. D) A constant pointer to a constant value.
12. B) By reassigning `ptr` to a new address.

---

These questions cover the distinctions between constant pointers and pointers to constants, helping to test understanding of pointer behavior and `const` keyword usage in C.