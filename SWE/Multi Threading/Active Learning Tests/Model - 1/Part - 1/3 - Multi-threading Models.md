# Multi-threading Models: User, Kernel, and Combined Threads Quiz

### 1. What is the primary characteristic of **user threads**?
- [ ] A) Managed by the operating system kernel
- [ ] B) Managed entirely by the application using a thread library
- [ ] C) Managed through both the kernel and the application
- [ ] D) Non-blocking system calls are used by default

### 2. What is a major disadvantage of user threads?
- [ ] A) They have high context switching overhead.
- [ ] B) User threads can only run on multi-core systems.
- [ ] C) If one thread blocks, the entire process is blocked.
- [ ] D) They cannot communicate with other threads within the same process.

### 3. How do **kernel threads** differ from user threads in terms of blocking?
- [ ] A) Kernel threads block the entire process when one thread is blocked.
- [ ] B) Kernel threads do not block other threads in the process if one thread is blocked.
- [ ] C) Kernel threads never block.
- [ ] D) Kernel threads are always faster than user threads.

### 4. What is a key advantage of using **kernel threads**?
- [ ] A) They are faster to create than user threads.
- [ ] B) They can be used on systems with only a single processor.
- [ ] C) They allow threads to run on different CPUs in multi-processor systems.
- [ ] D) They have lower context switching overhead than user threads.

### 5. Which threading model allows threads to map to multiple kernel threads?
- [ ] A) Many-to-one
- [ ] B) One-to-one
- [ ] C) Many-to-many
- [ ] D) One-to-many

### 6. Which system call is used to create a new thread in the POSIX thread library?
- [ ] A) `Pthread_exit`
- [ ] B) `Pthread_create`
- [ ] C) `Pthread_join`
- [ ] D) `Pthread_yield`

### 7. In a **many-to-one** threading model, how are user threads mapped to kernel threads?
- [ ] A) One user thread maps to multiple kernel threads.
- [ ] B) Multiple user threads map to a single kernel thread.
- [ ] C) One user thread maps directly to one kernel thread.
- [ ] D) All user threads map to all kernel threads.

### 8. How does the **SELECT** system call improve thread execution efficiency?
- [ ] A) It prevents blocking by avoiding page faults.
- [ ] B) It predicts whether a subsequent operation, such as `READ`, would block.
- [ ] C) It increases the number of kernel threads available to a process.
- [ ] D) It speeds up context switching between user threads.

### 9. What happens when a **page fault** occurs within a multi-threaded process?
- [ ] A) Only the thread that caused the page fault is blocked.
- [ ] B) The entire process is blocked, even if other threads could continue.
- [ ] C) The system immediately terminates the thread causing the fault.
- [ ] D) The fault is ignored, and the thread continues execution.

### 10. What is the purpose of **wrapper code** in thread management?
- [ ] A) To handle errors in thread creation.
- [ ] B) To manage thread execution before and after a system call.
- [ ] C) To create threads faster.
- [ ] D) To terminate threads that are no longer needed.

### 11. What is the **main disadvantage** of using **kernel threads** compared to **user threads**?
- [ ] A) Kernel threads are slower to create and manage.
- [ ] B) Kernel threads cannot use multiple CPUs.
- [ ] C) Kernel threads do not allow blocking calls.
- [ ] D) Kernel threads are less efficient at managing resources.

### 12. Which threading model offers the most flexibility for utilizing multi-core processors?
- [ ] A) Many-to-one model
- [ ] B) One-to-one model
- [ ] C) Many-to-many model
- [ ] D) User-level threading only

### 13. What system feature helps prevent **global blocking** in kernel threads?
- [ ] A) Thread library management
- [ ] B) Non-blocking system calls
- [ ] C) Kernel-level scheduling
- [ ] D) Predictive thread state management

### 14. Which of the following is **not** a feature of user threads?
- [ ] A) Faster context switching than kernel threads
- [ ] B) Managed by the operating system kernel
- [ ] C) Portable across different platforms
- [ ] D) Prone to global blocking during I/O operations

### 15. What is the **major benefit** of the **combined threading model**?
- [ ] A) It eliminates the need for kernel threads.
- [ ] B) It balances the fast context switching of user threads with the multiprocessing capabilities of kernel threads.
- [ ] C) It allows more user threads to be created than kernel threads.
- [ ] D) It uses less memory than user or kernel threads.

---

## Answers:
1. B  
2. C  
3. B  
4. C  
5. C  
6. B  
7. B  
8. B  
9. B  
10. B  
11. A  
12. C  
13. C  
14. B  
15. B  
