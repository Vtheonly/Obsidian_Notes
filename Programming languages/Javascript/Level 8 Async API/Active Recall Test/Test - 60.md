### Quiz: JavaScript and Single-Threaded Execution

#### Question 1:
- **What does it mean that JavaScript is single-threaded?**
  - [ ] It can execute multiple tasks simultaneously.
  - [ ] It has a single call stack and can only execute one task at a time.
  - [ ] It can only handle one network request at a time.

#### Question 2:
- **Which of the following is true about JavaScript’s single-threaded nature?**
  - [ ] JavaScript can execute tasks in parallel.
  - [ ] JavaScript has multiple call stacks for handling different tasks.
  - [ ] JavaScript uses a single call stack to manage function calls and their execution contexts.

#### Question 3:
- **How does JavaScript handle long-running operations like network requests without blocking the main thread?**
  - [ ] By executing them in the same thread sequentially.
  - [ ] By using asynchronous handling mechanisms like Web APIs, the event loop, and callbacks.
  - [ ] By ignoring them until the main thread is free.

#### Question 4:
- **What is the role of the event loop in JavaScript?**
  - [ ] To execute synchronous code only.
  - [ ] To manage asynchronous tasks by checking the task queue and executing tasks when the main thread is idle.
  - [ ] To create additional threads for parallel execution.

#### Question 5:
- **In the following JavaScript code, what will be logged to the console first?**
  ```javascript
  console.log("Start");
  
  setTimeout(() => {
      console.log("Task 1");
  }, 1000);
  
  console.log("End");
  ```
  - [ ] "Task 1"
  - [ ] "Start"
  - [ ] "End"

#### Question 6:
- **What happens when a CPU-bound task runs on JavaScript’s main thread?**
  - [ ] It completes quickly without affecting other tasks.
  - [ ] It can block the main thread, causing performance issues.
  - [ ] It runs in parallel with other tasks.

#### Question 7:
- **Which of the following is a limitation of JavaScript’s single-threaded execution?**
  - [ ] JavaScript can handle asynchronous tasks efficiently.
  - [ ] JavaScript can manage multiple network connections simultaneously.
  - [ ] JavaScript cannot perform true parallel processing without additional constructs like Web Workers.

#### Question 8:
- **How can JavaScript handle CPU-intensive tasks without blocking the main thread?**
  - [ ] By using the event loop alone.
  - [ ] By leveraging Web Workers to offload such tasks to background threads.
  - [ ] By waiting until the task queue is empty.

#### Question 9:
- **What is an advantage of JavaScript being single-threaded?**
  - [ ] It avoids complex issues related to concurrent execution, such as race conditions and deadlocks.
  - [ ] It can perform multiple tasks simultaneously without any performance degradation.
  - [ ] It can natively handle parallel processing without additional constructs.

#### Question 10:
- **Which of the following tasks is JavaScript well-suited for, given its single-threaded nature?**
  - [ ] Running heavy computations in parallel.
  - [x] Handling multiple I/O operations concurrently using non-blocking I/O.
  - [ ] Performing true parallel processing without additional threads.

---

### **Answers**
1. [ ] It has a single call stack and can only execute one task at a time.
2. [ ] JavaScript uses a single call stack to manage function calls and their execution contexts.
3. [ ] By using asynchronous handling mechanisms like Web APIs, the event loop, and callbacks.
4. [ ] To manage asynchronous tasks by checking the task queue and executing tasks when the main thread is idle.
5. [ ] "Start"
6. [ ] It can block the main thread, causing performance issues.
7. [ ] JavaScript cannot perform true parallel processing without additional constructs like Web Workers.
8. [ ] By leveraging Web Workers to offload such tasks to background threads.
9. [ ] It avoids complex issues related to concurrent execution, such as race conditions and deadlocks.
10. [ ] Handling multiple I/O operations concurrently using non-blocking I/O.