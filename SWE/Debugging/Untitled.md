
### 1. Continue (▶️)

*   **What it does:** This button tells your program to run until it reaches the next breakpoint, or until the program finishes if there are no more breakpoints. Think of it as saying, "Okay, keep going until I tell you to stop again."

*   **When to use it:** You use this when you've reached a point you want to inspect, you've looked at what you need, and you want the program to proceed to the next point of interest.

*   **Example Scenario:**

    Imagine you have a loop that adds numbers together, and you want to see the final sum. You might set a breakpoint *after* the loop finishes. When you hit "Continue," the loop will run to completion, and then the debugger will pause *after* the loop, allowing you to inspect the final sum.

    ```javascript
    let sum = 0;
    for (let i = 1; i <= 5; i++) {
      sum = sum + i;
    }
    // Set a breakpoint here
    console.log("The final sum is:", sum);
    ```

    When you press "Continue" from a breakpoint *inside* the loop, the debugger will run the rest of the loop's iterations and stop at the `console.log` line.

---

### 2. Step Over (🦧)

*   **What it does:** This button executes the current line of code and then pauses on the *next* line. Crucially, if the current line calls a function, "Step Over" will run that entire function to completion and then pause on the line *after* the function call. It *doesn't* go inside the function.

*   **When to use it:** This is your go-to when you're confident the function call on the current line is working correctly, and you just want to move to the next step in your current block of code without diving into the function's internal logic.

*   **Example Scenario:**

    Suppose you have a function `calculateArea` that you've already tested and know works. You want to see what happens *after* you call `calculateArea` in your main code.

    ```javascript
    function calculateArea(width, height) {
      return width * height;
    }

    let rectangleWidth = 10;
    let rectangleHeight = 5;
    let area = calculateArea(rectangleWidth, rectangleHeight); // Set a breakpoint on this line
    console.log("Area calculated.");
    ```

    If you are paused on the `let area = calculateArea(...)` line and press "Step Over," the `calculateArea` function will execute in the background, the `area` variable will get its value (50), and the debugger will then pause on the `console.log("Area calculated.");` line. You won't see the debugger step *inside* the `calculateArea` function.

---

### 3. Step Into (🚶‍♂️)

*   **What it does:** This button executes the current line of code. If the current line contains a function call, "Step Into" will take you *inside* that function and pause on its *first* line. If the current line is not a function call, it behaves like "Step Over" – it just moves to the next line.

*   **When to use it:** This is essential when you suspect a problem might be *within* a function you've called, and you need to examine its execution step-by-step.

*   **Example Scenario:**

    Let's use the same `calculateArea` example, but this time you suspect `calculateArea` might be doing something wrong.

    ```javascript
    function calculateArea(width, height) {
      // Set a breakpoint on this line inside the function
      let result = width * height;
      return result;
    }

    let rectangleWidth = 10;
    let rectangleHeight = 5;
    let area = calculateArea(rectangleWidth, rectangleHeight); // Set a breakpoint on this line
    console.log("Area calculated.");
    ```

    If you are paused on the `let area = calculateArea(...)` line and press "Step Into," the debugger will jump into the `calculateArea` function and pause on the `let result = width * height;` line. From there, you can use "Step Into" again to see the multiplication happen, and then "Step Out" to return to where it was called.

---

### 4. Step Out (🚀)

*   **What it does:** This button allows you to finish executing the *rest of the current function* that you are currently inside. Once the function finishes, the debugger will pause on the line *after* where the function was originally called.

*   **When to use it:** You use this when you've stepped into a function (using "Step Into") and you've seen enough. You want to quickly get back to the calling code without manually stepping through every remaining line of the function.

*   **Example Scenario:**

    Continuing the `calculateArea` example, let's say you've used "Step Into" to get inside `calculateArea` and you've checked that `result` is calculated correctly. Now you want to return to the main part of your script.

    ```javascript
    function calculateArea(width, height) {
      let result = width * height; // You've stepped into here
      return result;               // Now you press "Step Out" on this line
    }

    let rectangleWidth = 10;
    let rectangleHeight = 5;
    let area = calculateArea(rectangleWidth, rectangleHeight); // Debugger will pause HERE after Step Out
    console.log("Area calculated.");
    ```

    If you are paused on the `return result;` line *inside* `calculateArea` and press "Step Out," the `calculateArea` function will complete its execution, its return value will be assigned to `area`, and the debugger will resume and pause on the `console.log("Area calculated.");` line in the original scope.

---

### 5. Restart (↩️)

*   **What it does:** This button stops the current debugging session and immediately starts a new one, running your program from the very beginning.

*   **When to use it:** When you've made changes to your breakpoints, or you want to re-examine the entire execution flow from the start. It's like hitting the "reset" button.

*   **Example Scenario:**

    You're debugging a program that reads a configuration file, processes some data, and then saves it. You set a breakpoint early on, but then you realize you forgot to set another breakpoint later in the data processing stage. Instead of manually stopping the current session and starting a new one, you can just press "Restart" to run the whole thing again from the top with your new breakpoints in place.

    ```javascript
    console.log("Starting program...");
    // Lots of code here...
    let data = fetchData(); // Maybe set a breakpoint here
    processData(data);     // Maybe set another breakpoint here
    saveResults(data);
    console.log("Program finished.");
    ```

    If you are paused somewhere in `processData` and realize you missed setting a breakpoint on `fetchData()`, pressing "Restart" will immediately stop the current execution and start the program again, pausing at `console.log("Starting program...");` (or wherever your first breakpoint is).

---

### 6. Stop (⏹️)

*   **What it does:** This button completely terminates the current debugging session. Your program will stop running, and the debugger will detach.

*   **When to use it:** When you're done debugging, or you need to exit the debugging process entirely for any reason.

*   **Example Scenario:**

    You've found the bug you were looking for, or you've decided to stop debugging for now. You press the "Stop" button. The program execution immediately halts, and the debugger panel disappears or becomes inactive.

    ```javascript
    console.log("Debugging started...");
    // Some code that is now behaving correctly or you want to stop
    // Press the Stop button here
    console.log("Debugging session ended.");
    ```

    Pressing "Stop" will immediately end the program's execution. The line `console.log("Debugging session ended.");` will not be reached.

---

**Key Concepts to Remember:**

*   **Breakpoints:** These are the red dots you set on specific lines of code. The debugger will pause execution *before* running the line with a breakpoint.
*   **Call Stack:** This shows you the sequence of function calls that led to the current paused state. It helps you understand *how* you arrived at the current line of code.
*   **Variables:** In the debugger panel, you can see the current values of all variables that are in scope at the paused line. This is where you inspect the "state" of your program.

By mastering these buttons, you can effectively navigate your code, understand its behavior, and pinpoint the source of errors.