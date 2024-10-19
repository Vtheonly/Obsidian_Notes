
### **Quiz 1**
**What is the primary purpose of a monitor in concurrent programming?**
- [ ] A) To handle memory allocation
- [ ] B) To allow multiple processes to execute simultaneously
- [ ] C) To ensure mutual exclusion of processes
- [ ] D) To manage file operations

**Answer**: [[C]]

---

### **Quiz 2**
**Who introduced the concept of monitors in programming?**
- [ ] A) Edsger Dijkstra and Alan Turing
- [ ] B) Tony Hoare and Per Brinch Hansen
- [ ] C) John von Neumann and Bill Gates
- [ ] D) Dennis Ritchie and Ken Thompson

**Answer**: [[B]]

---

### **Quiz 3**
**How does a monitor ensure mutual exclusion?**
- [ ] A) By using a binary semaphore
- [ ] B) By using a mutex lock
- [ ] C) By allowing multiple processes to execute critical sections concurrently
- [ ] D) By scheduling processes on different CPUs

**Answer**: [[A]]

---

### **Quiz 4**
**What happens when a process tries to enter a monitor while another process is active inside it?**
- [ ] A) It is allowed to enter immediately
- [ ] B) It is suspended until the current process exits
- [ ] C) It continues executing outside the monitor
- [ ] D) It is terminated

**Answer**: [[B]]

---

### **Quiz 5**
**Which of the following is NOT a component of a monitor?**
- [ ] A) Procedures
- [ ] B) Local variables
- [ ] C) Condition variables
- [ ] D) Threads

**Answer**: [[D]]

---

### **Quiz 6**
**What role do condition variables play in a monitor?**
- [ ] A) They store numerical values used by processes
- [ ] B) They manage waiting processes that need to synchronize
- [ ] C) They track the execution state of processes
- [ ] D) They allocate resources to processes

**Answer**: [[B]]

---

### **Quiz 7**
**What does the operation `X.wait` do in a monitor?**
- [ ] A) It suspends the calling process and places it in the queue for `X`
- [ ] B) It signals all processes waiting on `X` to continue
- [ ] C) It checks if the monitor is free
- [ ] D) It releases a resource to a waiting process

**Answer**: [[A]]

---

### **Quiz 8**
**What happens when a process calls `X.signal` and no process is waiting on `X`?**
- [ ] A) The calling process is suspended
- [ ] B) The signal has no effect
- [ ] C) A new process is created
- [ ] D) The monitor is reset

**Answer**: [[B]]

---

### **Quiz 9**
**What does the `X.empty` operation return?**
- [ ] A) It checks if any process is waiting on `X`
- [ ] B) It retrieves the value of the condition variable `X`
- [ ] C) It returns the size of the waiting queue for `X`
- [ ] D) It checks if the monitor is occupied

**Answer**: [[A]]

---

### **Quiz 10**
**In the `allocator` monitor example, what happens when the `acquire` procedure is called and the resource is occupied?**
- [ ] A) The calling process waits in the `free` queue
- [ ] B) The calling process terminates
- [ ] C) The resource is forcibly taken by the process
- [ ] D) The monitor is reset

**Answer**: [[A]]

---

### **Quiz 11**
**What is the primary advantage of using monitors?**
- [ ] A) They centralize critical sections
- [ ] B) They allow multiple processes to share a single resource simultaneously
- [ ] C) They eliminate the need for condition variables
- [ ] D) They guarantee faster process execution

**Answer**: [[A]]

---

### **Quiz 12**
**In the `Resource_Allocator` monitor example, what does the `request` procedure do when all resources are occupied?**
- [ ] A) It releases a resource
- [ ] B) It adds the calling process to the `C.wait` queue
- [ ] C) It terminates the process
- [ ] D) It increments the resource count

**Answer**: [[B]]

---

### **Quiz 13**
**What does the `release` procedure in the `allocator` monitor do after setting `occupied := false`?**
- [ ] A) It terminates the process
- [ ] B) It resets the monitor
- [ ] C) It signals a waiting process using `free.signal`
- [ ] D) It locks the monitor

**Answer**: [[C]]

---

### **Quiz 14**
**Which of the following statements about monitors is TRUE?**
- [ ] A) Processes can enter a monitor simultaneously if they access different procedures
- [ ] B) Condition variables can be initialized with integer values
- [ ] C) A process inside a monitor automatically has access to shared variables
- [ ] D) Monitors eliminate the need for semaphores in process synchronization

**Answer**: [[C]]

---

### **Quiz 15**
**In which scenario does a process inside a monitor release the monitor?**
- [ ] A) After it finishes executing a procedure
- [ ] B) When another process signals it to exit
- [ ] C) When a resource becomes available
- [ ] D) When the semaphore count is zero

**Answer**: [[A]]

---

These quiz questions cover the main aspects of monitors, such as their purpose, structure, synchronization techniques, and the use of condition variables, ensuring a comprehensive understanding of the topic.