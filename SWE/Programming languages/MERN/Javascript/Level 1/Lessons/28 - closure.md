A closure is a fundamental concept in JavaScript that occurs when an inner function retains access to the variables and scope of its outer function, even after the outer function has finished executing. This allows the inner function to continue to access and manipulate those variables, creating a persistent state that is encapsulated within the inner function.

Here's a more detailed definition and an example to illustrate the concept:

**Definition**:
A closure is a function that captures and retains access to the variables from its enclosing lexical scope, even when the function is executed outside that scope. This allows the function to maintain a private state that can be accessed and modified through the closure.

**Example**:
```javascript
function createCounter() {
  let count = 0;
  let unusedVariable = 'I am not used';
  return function() {
    return ++count;
  };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

**Explanation**:
1. **Outer Function (`createCounter`)**:
   - Defines a variable `count` and an unused variable `unusedVariable`.
   - Returns an inner function that increments and returns the value of `count`.

2. **Inner Function (Closure)**:
   - Captures and retains access to the `count` variable from the outer function's scope.
   - The `unusedVariable` is also part of the closure, even though it is not used by the inner function.

3. **Execution**:
   - When `createCounter` is called, it returns the inner function, which is assigned to `counter`.
   - The inner function (closure) maintains access to the `count` variable, allowing it to increment and return the value each time it is called.

4. **Memory Retention**:
   - The `count` variable is retained in memory because the inner function forms a closure over it.
   - The `unusedVariable` is also retained in memory as part of the closure, although modern JavaScript engines may optimize memory usage by garbage collecting unused variables.

In summary, a closure in JavaScript is a powerful feature that allows functions to maintain private state and access variables from their enclosing scope, even after the outer function has completed execution. This enables the creation of functions with persistent and encapsulated data.