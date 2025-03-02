# Multi-threading in Modern Systems Quiz

### 1. What is the main difference between a single-threaded and multi-threaded process?
- [ ] A) A single-threaded process can execute multiple tasks simultaneously.
- [ ] B) A single-threaded process has one control flow, while a multi-threaded process has multiple control flows.
- [ ] C) A multi-threaded process requires more memory than a single-threaded process.
- [ ] D) A single-threaded process is faster than a multi-threaded process.

### 2. What component is responsible for keeping track of a thread’s current instruction during execution?
- [ ] A) File handler
- [ ] B) Ordinal counter
- [ ] C) Execution stack
- [ ] D) Device handler

### 3. What are the components that threads within a process share?
- [ ] A) Local variables and registers
- [ ] B) Execution stack and ordinal counter
- [ ] C) Memory space and file handlers
- [ ] D) Registers and device handlers

### 4. In modern systems, how is a **thread** commonly defined?
- [ ] A) A complete process with its own memory space
- [ ] B) A lightweight process that operates within the context of a parent process
- [ ] C) A standalone entity independent of processes
- [ ] D) A special kind of process used only for I/O operations

### 5. Which of the following best describes the **shared memory** concept in multi-threading?
- [ ] A) Threads have separate memory spaces but share data through the file system.
- [ ] B) Threads from the same process share the same memory space, allowing resource sharing.
- [ ] C) Each thread has its own independent memory and data segments.
- [ ] D) Threads only share memory during synchronization.

### 6. How does multi-threading enhance a system’s **responsiveness**?
- [ ] A) It allows blocked threads to continue execution.
- [ ] B) It prevents I/O operations from blocking the entire process, allowing other threads to continue running.
- [ ] C) It minimizes the need for file handlers.
- [ ] D) It runs only one thread at a time to avoid memory contention.

### 7. What is the **main thread** in a process?
- [ ] A) The only thread that can access the process’s memory.
- [ ] B) The primary thread that handles the main execution flow of the process.
- [ ] C) A thread dedicated to handling file I/O operations.
- [ ] D) A thread that can create new processes within the parent process.

### 8. Which of the following is an advantage of threads over processes?
- [ ] A) Threads have their own memory space, reducing memory conflicts.
- [ ] B) Thread creation is faster and more efficient compared to process creation.
- [ ] C) Threads have better isolation from each other than processes.
- [ ] D) Threads can operate independently without any shared resources.

### 9. How does resource sharing among threads improve performance in multi-threaded systems?
- [ ] A) It reduces the need for communication between processes.
- [ ] B) It allows threads to share data without the overhead of copying.
- [ ] C) It eliminates the need for synchronization mechanisms.
- [ ] D) It prevents memory leaks by isolating memory spaces.

### 10. Why is **thread creation** faster than **process creation** in most operating systems?
- [ ] A) Threads require more system resources, making them easier to create.
- [ ] B) Threads share resources like memory and file handlers, whereas processes require independent resources.
- [ ] C) Threads have more sophisticated error-handling mechanisms.
- [ ] D) Threads operate independently of the operating system, while processes need OS management.

### 11. Which system resource is **not** typically shared by threads within a process?
- [ ] A) Memory space
- [ ] B) Ordinal counter
- [ ] C) File handlers
- [ ] D) Registers

### 12. What is the potential drawback of threads sharing the same memory space?
- [ ] A) It limits the number of threads that can be created.
- [ ] B) It increases the likelihood of resource contention and data corruption.
- [ ] C) It reduces the performance of the system.
- [ ] D) It makes thread communication slower and more complex.

### 13. What are **local variables** in the context of multi-threading?
- [ ] A) Variables that are shared across all threads in a process.
- [ ] B) Variables that are specific to each thread and stored in the thread’s execution stack.
- [ ] C) Global variables accessible by any thread in the system.
- [ ] D) Variables that store the thread’s ordinal counter.

### 14. How does **multi-threading** contribute to **memory efficiency** in a system?
- [ ] A) It allows multiple processes to share the same memory space.
- [ ] B) Threads use shared memory, reducing the need for allocating separate memory for each process.
- [ ] C) Threads prevent memory fragmentation.
- [ ] D) Each thread manages its own memory, leading to more efficient memory usage.

### 15. Which of the following is **not** an advantage of multi-threading?
- [ ] A) Reduced memory usage due to shared memory.
- [ ] B) Improved responsiveness and system performance.
- [ ] C) Simplified debugging process compared to single-threaded systems.
- [ ] D) Faster creation time compared to process creation.

---

## Answers:
1. B  
2. B  
3. C  
4. B  
5. B  
6. B  
7. B  
8. B  
9. B  
10. B  
11. D  
12. B  
13. B  
14. B  
15. C  
