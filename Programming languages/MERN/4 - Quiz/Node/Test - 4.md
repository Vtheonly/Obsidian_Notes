Here are 15 quiz questions based on the `EventEmitter` and `readline` module concepts in Node.js:

### EventEmitter and readline Quiz

1. - [ ] What is the primary purpose of the `EventEmitter` class in Node.js?
   - [ ] A. Handling user input events in the browser
   - [ ] B. Emitting and listening to custom events in Node.js
   - [ ] C. Managing HTTP requests
   - [ ] D. Reading files from the filesystem

2. - [ ] Which method is used to emit an event in `EventEmitter`?
   - [ ] A. `emit()`
   - [ ] B. `dispatch()`
   - [ ] C. `trigger()`
   - [ ] D. `fire()`

3. - [ ] What does the `on` method of `EventEmitter` do?
   - [ ] A. Registers an event listener
   - [ ] B. Emits an event
   - [ ] C. Removes an event listener
   - [ ] D. Pauses event emission

4. - [ ] How can you inherit from `EventEmitter` in Node.js?
   - [ ] A. By using the `inherits` module
   - [ ] B. By using the `extend` method
   - [ ] C. By using the `class` and `extends` keywords
   - [ ] D. It is not possible to inherit from `EventEmitter`

5. - [ ] Which event is automatically emitted when the `readline` interface is closed?
   - [ ] A. `end`
   - [ ] B. `close`
   - [ ] C. `finish`
   - [ ] D. `exit`

6. - [ ] What does the `readline.createInterface` method do?
   - [ ] A. Creates a new file interface
   - [ ] B. Creates an interface for reading lines from a stream
   - [ ] C. Creates a GUI interface for Node.js
   - [ ] D. Creates an interface for handling HTTP requests

7. - [ ] How do you prompt the user for input using the `readline` module?
   - [ ] A. `rl.ask()`
   - [ ] B. `rl.prompt()`
   - [ ] C. `rl.query()`
   - [ ] D. `rl.input()`

8. - [ ] What argument is required when emitting an event in `EventEmitter`?
   - [ ] A. Event name
   - [ ] B. Event listener
   - [ ] C. Callback function
   - [ ] D. Stream object

9. - [ ] What is the significance of the `line` event in the `readline` module?
   - [ ] A. It handles the closing of the interface
   - [ ] B. It is triggered whenever a line of input is received
   - [ ] C. It is used to emit an event
   - [ ] D. It indicates the end of input

10. - [ ] What does the `rl.question` method do?
    - [ ] A. Exits the readline interface
    - [ ] B. Prompts the user with a question and waits for input
    - [ ] C. Closes the readline interface
    - [ ] D. Skips to the next line of input

11. - [ ] How does `EventEmitter` handle multiple listeners for the same event?
    - [ ] A. Executes them simultaneously
    - [ ] B. Executes them one by one in the order they were registered
    - [ ] C. Executes only the first listener
    - [ ] D. Randomly selects a listener to execute

12. - [ ] What happens when the `emit` method is called on an event with no listeners?
    - [ ] A. An error is thrown
    - [ ] B. Nothing happens
    - [ ] C. The event is logged
    - [ ] D. The event is stored for future listeners

13. - [ ] How can you remove an event listener from an `EventEmitter` instance?
    - [ ] A. `off()`
    - [ ] B. `removeListener()`
    - [ ] C. `deleteListener()`
    - [ ] D. `clearListener()`

14. - [ ] Which stream is typically used as the input for `readline.createInterface`?
    - [ ] A. `fs.createReadStream()`
    - [ ] B. `process.stdout`
    - [ ] C. `process.stdin`
    - [ ] D. `http.createServer()`

15. - [ ] What is the purpose of the `process.exit(0)` statement in a `close` event listener?
    - [ ] A. To start a new process
    - [ ] B. To restart the readline interface
    - [ ] C. To exit the program gracefully
    - [ ] D. To log the exit code to the console

---


### Answers to EventEmitter and readline Quiz

1. **B. Emitting and listening to custom events in Node.js**
2. **A. `emit()`**
3. **A. Registers an event listener**
4. **C. By using the `class` and `extends` keywords**
5. **B. `close`**
6. **B. Creates an interface for reading lines from a stream**
7. **B. `rl.prompt()`**
8. **A. Event name**
9. **B. It is triggered whenever a line of input is received**
10. **B. Prompts the user with a question and waits for input**
11. **B. Executes them one by one in the order they were registered**
12. **B. Nothing happens**
13. **B. `removeListener()`**
14. **C. `process.stdin`**
15. **C. To exit the program gracefully**

These answers should give you a complete understanding of the key concepts related to the `EventEmitter` and `readline` modules in Node.js.