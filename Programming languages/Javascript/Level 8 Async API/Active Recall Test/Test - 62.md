### Quiz: JavaScript Promises

#### Question 1:
- **What are the three possible states of a JavaScript Promise?**
  - [ ] Pending, Fulfilled, Completed
  - [ ] Pending, Fulfilled, Rejected
  - [ ] Waiting, Resolved, Failed

#### Question 2:
- **How do you create a new Promise in JavaScript?**
  - [ ] Using the `new Promise()` constructor, which requires an executor function with `resolve` and `reject` parameters.
  - [ ] By using the `Promise.create()` method.
  - [ ] By wrapping a function in `try...catch` blocks.

#### Question 3:
- **What is the purpose of the `then` method in a Promise?**
  - [ ] To immediately execute the callback function.
  - [ ] To handle the eventual result (fulfillment or rejection) of a Promise.
  - [ ] To pause the execution until the Promise is fulfilled.

#### Question 4:
- **What does the `catch` method do in a Promise chain?**
  - [ ] It logs errors to the console automatically.
  - [ ] It handles the rejection of a Promise.
  - [ ] It retries the failed Promise.

#### Question 5:
- **In a Promise chain, what happens when an error is thrown inside a `then` method?**
  - [ ] The error is ignored.
  - [ ] The error is caught by the nearest `catch` method.
  - [ ] The entire chain stops executing.

#### Question 6:
- **What is the output of the following code?**
  ```javascript
  const promise = new Promise((resolve, reject) => {
      resolve("Success!");
  });

  promise.then(result => {
      console.log(result);
      return "Another success!";
  }).then(newResult => {
      console.log(newResult);
  });
  ```
  - [ ] "Success!"
  - [ ] "Success!", "Another success!"
  - [ ] "Another success!"

#### Question 7:
- **What is the difference between `Promise.all` and `Promise.race`?**
  - [ ] `Promise.all` waits for all Promises to settle, while `Promise.race` resolves or rejects as soon as the first Promise settles.
  - [ ] `Promise.all` resolves as soon as the first Promise resolves, while `Promise.race` waits for all Promises to settle.
  - [ ] They both do the same thing, but `Promise.race` is faster.

#### Question 8:
- **How does `Promise.any` differ from `Promise.all`?**
  - [ ] `Promise.any` resolves as soon as any one of the Promises resolves, while `Promise.all` resolves only when all Promises resolve.
  - [ ] `Promise.any` rejects as soon as any one of the Promises rejects.
  - [ ] `Promise.any` and `Promise.all` have the same behavior.

#### Question 9:
- **In the context of promises, what does the `finally` method do?**
  - [ ] It executes a cleanup operation after the Promise is either fulfilled or rejected.
  - [ ] It retries a rejected Promise.
  - [ ] It only runs if the Promise is fulfilled.

#### Question 10:
- **What is the output of the following code?**
  ```javascript
  function test() {
      return new Promise(resolve => {
          setTimeout(() => {
              console.log("done first");
              resolve();
          }, 0);
      });
  }

  test().then(() => {
      console.log("done third");
  });
  console.log("done second");
  ```
  - [ ] "done first", "done second", "done third"
  - [ ] "done second", "done first", "done third"
  - [ ] "done third", "done first", "done second"

---

### **Answers**
1. [ ] Pending, Fulfilled, Rejected
2. [ ] Using the `new Promise()` constructor, which requires an executor function with `resolve` and `reject` parameters.
3. [ ] To handle the eventual result (fulfillment or rejection) of a Promise.
4. [ ] It handles the rejection of a Promise.
5. [ ] The error is caught by the nearest `catch` method.
6. [ ] "Success!", "Another success!"
7. [ ] `Promise.all` waits for all Promises to settle, while `Promise.race` resolves or rejects as soon as the first Promise settles.
8. [ ] `Promise.any` resolves as soon as any one of the Promises resolves, while `Promise.all` resolves only when all Promises resolve.
9. [ ] It executes a cleanup operation after the Promise is either fulfilled or rejected.
10. [ ] "done second", "done first", "done third"