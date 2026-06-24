### Quiz: Event Loop and Callback Queue in JavaScript

#### Question 1:
- **What is the primary role of the call stack in JavaScript's execution model?**
  - [ ] To execute asynchronous functions immediately.
  - [ ] To track and manage function calls in a single-threaded manner.
  - [ ] To handle tasks in parallel.

#### Question 2:
- **How does JavaScript handle asynchronous operations despite being single-threaded?**
  - [ ] By creating additional threads for each asynchronous operation.
  - [ ] By using the event loop and callback queue to manage the execution of asynchronous callbacks.
  - [ ] By executing all asynchronous operations in the main thread without delay.

#### Question 3:
- **What happens when an asynchronous function like `setTimeout` is called in JavaScript?**
  - [ ] It immediately executes the callback function.
  - [ ] It sends the function to the browser's Web API, which handles it independently of the main thread.
  - [ ] It blocks the execution of subsequent code until the timeout is complete.

#### Question 4:
- **What does the event loop do in JavaScript?**
  - [ ] It handles synchronous code execution.
  - [ ] It continuously checks the call stack and, when empty, moves callbacks from the callback queue to the call stack.
  - [ ] It executes functions in parallel.

#### Question 5:
- **In JavaScript, what is the purpose of the callback queue?**
  - [ ] To store functions that need to be executed after a delay.
  - [ ] To hold asynchronous callbacks that are waiting to be executed once the call stack is empty.
  - [ ] To manage the execution of synchronous functions.

#### Question 6:
- **How does the microtask queue differ from the callback queue in JavaScript?**
  - [ ] The microtask queue is processed before the callback queue and handles tasks like promise resolution.
  - [ ] The microtask queue is for handling synchronous tasks, while the callback queue handles asynchronous tasks.
  - [ ] The microtask queue handles tasks with higher priority after all callbacks have been executed.

#### Question 7:
- **What is the order of execution in the following JavaScript code?**
  ```javascript
  console.log("Start");

  setTimeout(() => {
      console.log("Task 1");
  }, 1000);

  Promise.resolve().then(() => {
      console.log("Promise 1");
  });

  console.log("End");
  ```
  - [ ] "Start", "Task 1", "Promise 1", "End"
  - [ ] "Start", "End", "Promise 1", "Task 1"
  - [ ] "Start", "End", "Task 1", "Promise 1"

#### Question 8:
- **What is the primary benefit of using the event loop in JavaScript?**
  - [ ] It allows JavaScript to run multiple threads simultaneously.
  - [ ] It enables non-blocking, asynchronous execution while maintaining a single-threaded model.
  - [ ] It simplifies the execution of synchronous code.

#### Question 9:
- **Which rule does the callback queue follow when processing callbacks?**
  - [ ] Last In, First Out (LIFO)
  - [ ] First In, First Out (FIFO)
  - [ ] Random Order

#### Question 10:
- **Why is the event loop crucial for JavaScript's performance in web applications?**
  - [ ] It ensures that all tasks are executed in parallel, increasing performance.
  - [ ] It manages asynchronous operations efficiently, keeping the user interface responsive.
  - [ ] It prevents the execution of heavy computations by delaying them indefinitely.

---

### **Answers**
1. [ ] To track and manage function calls in a single-threaded manner.
2. [ ] By using the event loop and callback queue to manage the execution of asynchronous callbacks.
3. [ ] It sends the function to the browser's Web API, which handles it independently of the main thread.
4. [ ] It continuously checks the call stack and, when empty, moves callbacks from the callback queue to the call stack.
5. [ ] To hold asynchronous callbacks that are waiting to be executed once the call stack is empty.
6. [ ] The microtask queue is processed before the callback queue and handles tasks like promise resolution.
7. [ ] "Start", "End", "Promise 1", "Task 1"
8. [ ] It enables non-blocking, asynchronous execution while maintaining a single-threaded model.
9. [ ] First In, First Out (FIFO)
10. [ ] It manages asynchronous operations efficiently, keeping the user interface responsive.