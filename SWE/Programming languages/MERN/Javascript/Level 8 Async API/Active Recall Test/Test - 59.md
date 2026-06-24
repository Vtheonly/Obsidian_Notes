### Quiz: Synchronous and Asynchronous Programming

#### Question 1:
- **What is the key difference between synchronous and asynchronous programming?**
  - [ ] Synchronous programming allows tasks to run concurrently, while asynchronous programming executes them one after another.
  - [ ] Synchronous programming executes tasks sequentially, while asynchronous programming allows tasks to run concurrently.
  - [ ] Both synchronous and asynchronous programming execute tasks sequentially.

#### Question 2:
- **Which of the following best describes synchronous programming?**
  - [ ] Tasks are executed in parallel, without waiting for the previous task to complete.
  - [ ] Tasks are executed one after another, with each task waiting for the previous one to complete.
  - [ ] Tasks are executed in random order.

#### Question 3:
- **In the following synchronous code, what will be logged to the console first?**
  ```javascript
  console.log("First");
  console.log("Second");
  console.log("Third");
  ```
  - [ ] "Second"
  - [ ] "Third"
  - [ ] "First"

#### Question 4:
- **What does asynchronous programming allow that synchronous programming does not?**
  - [ ] Execution of multiple tasks simultaneously.
  - [ ] Blocking of all other tasks until one is completed.
  - [ ] Execution of tasks in the exact order they are written.

#### Question 5:
- **Which of the following is an example of asynchronous programming?**
  - [ ] A for-loop that counts from 1 to 10.
  - [ ] A function that makes a network request and continues executing other code while waiting for a response.
  - [ ] A function that calculates the sum of two numbers.

#### Question 6:
- **In the following asynchronous code, which console log will appear first?**
  ```javascript
  console.log("Start");
  setTimeout(() => {
      console.log("Later");
  }, 1000);
  console.log("End");
  ```
  - [ ] "Start"
  - [ ] "Later"
  - [ ] "End"

#### Question 7:
- **Which of the following methods is commonly used to manage asynchronous operations in JavaScript?**
  - [ ] Loops
  - [ ] Callbacks
  - [ ] Conditionals

#### Question 8:
- **What is a Promise in JavaScript?**
  - [ ] A function that is executed immediately without delay.
  - [ ] An object representing the eventual completion or failure of an asynchronous operation.
  - [ ] A loop that continues until a condition is met.

#### Question 9:
- **Which of the following is a characteristic of synchronous programming?**
  - [ ] Non-blocking
  - [ ] Blocking
  - [ ] Concurrency

#### Question 10:
- **When would you prefer using asynchronous programming over synchronous programming?**
  - [ ] When you need to execute a simple, linear sequence of tasks.
  - [ ] When you need to handle time-consuming operations like network requests without blocking the main thread.
  - [ ] When you want to avoid complexity in your code.

---

### **Answers**
1. [ ] Synchronous programming executes tasks sequentially, while asynchronous programming allows tasks to run concurrently.
2. [ ] Tasks are executed one after another, with each task waiting for the previous one to complete.
3. [ ] "First"
4. [ ] Execution of multiple tasks simultaneously.
5. [ ] A function that makes a network request and continues executing other code while waiting for a response.
6. [ ] "Start"
7. [ ] Callbacks
8. [ ] An object representing the eventual completion or failure of an asynchronous operation.
9. [ ] Blocking
10. [ ] When you need to handle time-consuming operations like network requests without blocking the main thread.