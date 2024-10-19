Here are 15 quiz questions based on the provided text about `EventEmitter` in JavaScript:

---

## Comprehensive Quiz: EventEmitter in JavaScript

1. **What is `EventEmitter` in Node.js?**
   - [ ] A built-in function to handle HTTP requests.
   - [ ] A core module that allows you to create, manage, and respond to custom events.
   - [ ] A method for managing asynchronous code.
   - [ ] A class specifically for handling DOM events.

2. **Which pattern does `EventEmitter` implement?**
   - [ ] Singleton
   - [ ] Factory
   - [ ] Observer
   - [ ] Prototype

3. **What is the primary difference between `EventEmitter` and `onClick`?**
   - [ ] `EventEmitter` is for DOM events, while `onClick` is for custom events.
   - [ ] `onClick` handles browser DOM events, while `EventEmitter` handles custom events in Node.js.
   - [ ] `onClick` can emit custom events, while `EventEmitter` cannot.
   - [ ] There is no significant difference.

4. **Which of the following correctly sets up a listener for an event named `greet`?**
   - [ ] `myEmitter.listen('greet', callback);`
   - [ ] `myEmitter.on('greet', callback);`
   - [ ] `myEmitter.emit('greet', callback);`
   - [ ] `myEmitter.addListener('greet', callback);`

5. **How do you emit an event named `greet` with a parameter `name`?**
   - [ ] `emit('greet', name);`
   - [ ] `myEmitter.call('greet', name);`
   - [ ] `myEmitter.emit('greet', name);`
   - [ ] `myEmitter.trigger('greet', name);`

6. **True or False: In Node.js, `EventEmitter` handles events asynchronously by default.**
   - [ ] True
   - [ ] False

7. **Which method adds a listener to an event in `EventEmitter`?**
   - [ ] `emit()`
   - [ ] `on()`
   - [ ] `addListener()`
   - [ ] Both `on()` and `addListener()`

8. **What will the following code output?**
   ```javascript
   const EventEmitter = require('events');
   const myEmitter = new EventEmitter();
   
   myEmitter.on('test', () => console.log('First'));
   myEmitter.on('test', () => console.log('Second'));
   myEmitter.emit('test');
   ```
   - [ ] First Second
   - [ ] Second First
   - [ ] First
   - [ ] Nothing, because events are asynchronous

9. **How can you create a custom class that inherits from `EventEmitter`?**
   - [ ] `class MyEmitter extends EventEmitter {}`
   - [ ] `class MyEmitter inherits EventEmitter {}`
   - [ ] `class MyEmitter extends events {}`
   - [ ] `class MyEmitter requires EventEmitter {}`
  
10. **What is the purpose of calling `super()` in a class that extends `EventEmitter`?**
    - [ ] To import the `EventEmitter` module.
    - [ ] To allow the custom class to use `EventEmitter` methods.
    - [ ] To register custom events.
    - [ ] To create synchronous event listeners.

11. **How does `EventEmitter` handle multiple listeners for the same event?**
    - [ ] It executes them asynchronously.
    - [ ] It executes them in reverse order.
    - [ ] It executes them in the order they were registered.
    - [ ] It ignores all but the first listener.

12. **True or False: The `emit()` method can be used to pass multiple arguments to event listeners.**
    - [ ] True
    - [ ] False

13. **Which method can be used to remove a specific listener from an event in `EventEmitter`?**
    - [ ] `removeListener()`
    - [ ] `off()`
    - [ ] `deleteListener()`
    - [ ] `removeEventListener()`

14. **What will be the output of the following code?**
    ```javascript
    const EventEmitter = require('events');
    class MyEmitter extends EventEmitter {}
    
    const myEmitter = new MyEmitter();
    
    myEmitter.on('greet', (name) => console.log(`Hello, ${name}!`));
    myEmitter.emit('greet', 'Alice');
    ```
    - [ ] Hello, Alice!
    - [ ] Nothing, because `MyEmitter` does not have a `greet` method.
    - [ ] An error, because `EventEmitter` is not imported.
    - [ ] `undefined`

15. **What is a key advantage of creating a class that inherits from `EventEmitter`?**
    - [ ] It can manage multiple asynchronous tasks.
    - [ ] It enables adding custom methods and properties while still using event-driven features.
    - [ ] It simplifies the process of handling browser events.
    - [ ] It ensures all events are handled asynchronously.

---

### Answers

Here are the correct answers to the quiz:

1. **What is `EventEmitter` in Node.js?**
   - [x] A core module that allows you to create, manage, and respond to custom events.

2. **Which pattern does `EventEmitter` implement?**
   - [x] Observer

3. **What is the primary difference between `EventEmitter` and `onClick`?**
   - [x] `onClick` handles browser DOM events, while `EventEmitter` handles custom events in Node.js.

4. **Which of the following correctly sets up a listener for an event named `greet`?**
   - [x] `myEmitter.on('greet', callback);`

5. **How do you emit an event named `greet` with a parameter `name`?**
   - [x] `myEmitter.emit('greet', name);`

6. **True or False: In Node.js, `EventEmitter` handles events asynchronously by default.**
   - [ ] False

7. **Which method adds a listener to an event in `EventEmitter`?**
   - [x] Both `on()` and `addListener()`

8. **What will the following code output?**
   - [x] First Second

9. **How can you create a custom class that inherits from `EventEmitter`?**
   - [x] `class MyEmitter extends EventEmitter {}`

10. **What is the purpose of calling `super()` in a class that extends `EventEmitter`?**
    - [x] To allow the custom class to use `EventEmitter` methods.

11. **How does `EventEmitter` handle multiple listeners for the same event?**
    - [x] It executes them in the order they were registered.

12. **True or False: The `emit()` method can be used to pass multiple arguments to event listeners.**
    - [x] True

13. **Which method can be used to remove a specific listener from an event in `EventEmitter`?**
    - [x] `removeListener()`

14. **What will be the output of the following code?**
    - [x] Hello, Alice!

15. **What is a key advantage of creating a class that inherits from `EventEmitter`?**
    - [x] It enables adding custom methods and properties while still using event-driven features.

---

These answers should help solidify your understanding of the `EventEmitter` in JavaScript and how to use it effectively.