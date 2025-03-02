# Kernel-Level Threads and POSIX Thread Management in Linux Quiz

### 1. What is a primary characteristic of **kernel threads** in Linux?
- [ ] A) Managed by the user application
- [ ] B) Fully managed by the OS kernel
- [ ] C) Only used for I/O operations
- [ ] D) Only run on single-core processors

### 2. In Linux, what system call is used to create threads and specify shared resources?
- [ ] A) `fork()`
- [ ] B) `pthread_create()`
- [ ] C) `clone()`
- [ ] D) `exec()`

### 3. What is the role of **thread recycling** in kernel threads?
- [ ] A) To switch between threads faster
- [ ] B) To reuse thread data structures after a thread is destroyed
- [ ] C) To avoid creating new kernel threads
- [ ] D) To manage thread priorities

### 4. Which of the following is a **disadvantage** of kernel threads in Linux?
- [ ] A) Slow page fault handling
- [ ] B) They are less portable than user threads
- [ ] C) They cannot run on multiple CPUs
- [ ] D) Kernel threads are always slower than user threads

### 5. What happens during a **page fault** in a multi-threaded process?
- [ ] A) The entire process is blocked.
- [ ] B) Only the thread causing the fault is blocked.
- [ ] C) The process terminates.
- [ ] D) All threads continue execution.

### 6. What is the purpose of `pthread_create()` in POSIX thread management?
- [ ] A) To terminate a thread
- [ ] B) To create a new thread
- [ ] C) To suspend a thread
- [ ] D) To cancel a thread

### 7. What is a **detached thread** in POSIX thread management?
- [ ] A) A thread that cannot be canceled
- [ ] B) A thread that automatically releases its resources after completion
- [ ] C) A thread that never finishes
- [ ] D) A thread that must be manually joined

### 8. Which function is used to **terminate** a thread in POSIX?
- [ ] A) `pthread_cancel()`
- [ ] B) `pthread_exit()`
- [ ] C) `pthread_join()`
- [ ] D) `pthread_cleanup_pop()`

### 9. Which system call is used to wait for a thread to complete before proceeding?
- [ ] A) `pthread_create()`
- [ ] B) `pthread_exit()`
- [ ] C) `pthread_join()`
- [ ] D) `pthread_cancel()`

### 10. What is the use of **pthread_cleanup_push()** in POSIX?
- [ ] A) To push a thread to the ready queue
- [ ] B) To register a cleanup handler for resource management
- [ ] C) To suspend a thread
- [ ] D) To cancel a thread’s execution

### 11. What does `pthread_setcancelstate()` control?
- [ ] A) A thread's ability to join with others
- [ ] B) A thread's priority level
- [ ] C) Whether a thread can be cancelled or not
- [ ] D) How a thread handles page faults

### 12. Why is **slow context switching** a disadvantage of kernel threads?
- [ ] A) It uses more CPU cycles
- [ ] B) It leads to high memory usage
- [ ] C) It requires kernel intervention, which increases overhead
- [ ] D) It decreases the system's ability to use multiprocessing

### 13. Which POSIX function allows a thread to be cancelled by another thread?
- [ ] A) `pthread_create()`
- [ ] B) `pthread_join()`
- [ ] C) `pthread_cancel()`
- [ ] D) `pthread_exit()`

### 14. In Linux, how does **multiprocessing** benefit from kernel threads?
- [ ] A) Threads can run on different CPUs simultaneously
- [ ] B) Threads are created faster
- [ ] C) There are fewer context switches
- [ ] D) Kernel threads are more portable

---

## Answers:
1. B  
2. C  
3. B  
4. B  
5. B  
6. B  
7. B  
8. B  
9. C  
10. B  
11. C  
12. C  
13. C  
14. A  
