Here are 15 quiz questions based on the provided text about `export` and `require` syntax in JavaScript:

---

## Comprehensive Quiz: Exporting and Requiring in JavaScript

1. **Which of the following correctly exports the `pi` variable from a module?**
   - [ ] `module.exports.pi = pi;`
   - [ ] `exports pi = pi;`
   - [ ] `module.export.pi = pi;`
   - [ ] `export pi;`

2. **What is the correct way to import the `add` function from `mathUtils.js` into another file?**
   - [ ] `const { add } = require('./mathUtils');`
   - [ ] `const add = require('./mathUtils').add;`
   - [ ] `import add from './mathUtils';`
   - [ ] `const add = import('./mathUtils');`

3. **True or False: In Node.js, `module.exports` is an object used to define what a module exports.**
   - [ ] True
   - [ ] False

4. **Which of the following exports the entire `Calculator` class?**
   - [ ] `module.export = Calculator;`
   - [ ] `module.exports.Calculator = Calculator;`
   - [ ] `exports.Calculator = Calculator;`
   - [ ] `module.exports = Calculator;`

5. **Given the following code, how would you correctly import `pi`, `add`, and `Calculator` from `mathUtils.js`?**
   ```javascript
   const { pi, add, Calculator } = require('___');
   ```
   - [ ] `./mathUtils`
   - [ ] `mathUtils.js`
   - [ ] `mathUtils`
   - [ ] `./mathUtils.js`

6. **How do you export multiple items at once in Node.js?**
   - [ ] `module.exports = { item1, item2 };`
   - [ ] `module.exports(item1, item2);`
   - [ ] `export { item1, item2 };`
   - [ ] `exports = { item1, item2 };`

7. **Which method is used to load an external module or file in Node.js?**
   - [ ] `require()`
   - [ ] `import()`
   - [ ] `include()`
   - [ ] `load()`

8. **What does the following line of code do?**
   ```javascript
   const utils = require('./mathUtils');
   ```
   - [ ] It imports all exported components from `mathUtils.js` as a single object.
   - [ ] It imports only the `utils` function from `mathUtils.js`.
   - [ ] It exports all components to `mathUtils.js`.
   - [ ] It removes all functions from `mathUtils.js`.

9. **True or False: You can use `require` to import JSON files in Node.js.**
   - [ ] True
   - [ ] False

10. **What does `module.exports` refer to in Node.js?**
    - [ ] The current file's exported object.
    - [ ] A built-in Node.js module.
    - [ ] A global variable that stores all exports.
    - [ ] A function used to include external files.

11. **What would happen if you assign `module.exports` to a function instead of an object?**
    - [ ] The entire module will export only that function.
    - [ ] The function would become unusable.
    - [ ] It would cause an error.
    - [ ] It would export the function as part of an object.

12. **Which of the following correctly imports only the `multiply` method from the `Calculator` class?**
    - [ ] `const { multiply } = require('./mathUtils').Calculator;`
    - [ ] `const multiply = require('./mathUtils').Calculator.multiply;`
    - [ ] `const multiply = require('./mathUtils').multiply;`
    - [ ] `import multiply from './mathUtils';`

13. **True or False: The `export` keyword is used in ES Modules, while `module.exports` is used in CommonJS modules.**
    - [ ] True
    - [ ] False

14. **Which statement would you use to export an entire object containing multiple variables and functions?**
    - [ ] `module.exports = { var1, func1 };`
    - [ ] `module.exports(var1, func1);`
    - [ ] `exports = { var1, func1 };`
    - [ ] `export { var1, func1 };`

15. **What will be the output of the following code?**
    ```javascript
    const utils = require('./mathUtils');
    console.log(utils.pi);
    ```
    - [ ] The value of `pi` as exported from `mathUtils.js`.
    - [ ] `undefined`
    - [ ] An error, because `pi` is not imported directly.
    - [ ] `null`

---
Here are the answers to the quiz:

---

## Quiz Answers: Exporting and Requiring in JavaScript

1. **Which of the following correctly exports the `pi` variable from a module?**
   - [x] `module.exports.pi = pi;`

2. **What is the correct way to import the `add` function from `mathUtils.js` into another file?**
   - [x] `const { add } = require('./mathUtils');`

3. **True or False: In Node.js, `module.exports` is an object used to define what a module exports.**
   - [x] True

4. **Which of the following exports the entire `Calculator` class?**
   - [x] `module.exports = Calculator;`

5. **Given the following code, how would you correctly import `pi`, `add`, and `Calculator` from `mathUtils.js`?**
   - [x] `./mathUtils`

6. **How do you export multiple items at once in Node.js?**
   - [x] `module.exports = { item1, item2 };`

7. **Which method is used to load an external module or file in Node.js?**
   - [x] `require()`

8. **What does the following line of code do?**
   ```javascript
   const utils = require('./mathUtils');
   ```
   - [x] It imports all exported components from `mathUtils.js` as a single object.

9. **True or False: You can use `require` to import JSON files in Node.js.**
   - [x] True

10. **What does `module.exports` refer to in Node.js?**
    - [x] The current file's exported object.

11. **What would happen if you assign `module.exports` to a function instead of an object?**
    - [x] The entire module will export only that function.

12. **Which of the following correctly imports only the `multiply` method from the `Calculator` class?**
    - [x] `const multiply = require('./mathUtils').Calculator.multiply;`

13. **True or False: The `export` keyword is used in ES Modules, while `module.exports` is used in CommonJS modules.**
    - [x] True

14. **Which statement would you use to export an entire object containing multiple variables and functions?**
    - [x] `module.exports = { var1, func1 };`

15. **What will be the output of the following code?**
    ```javascript
    const utils = require('./mathUtils');
    console.log(utils.pi);
    ```
    - [x] The value of `pi` as exported from `mathUtils.js`.

--- 
