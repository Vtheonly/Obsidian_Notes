
# Getting Started with Debugging in VS Code (Official Beginner Guide Summary)

**Tags:** #vscode #debugging #javascript #nodejs #csharp #dotnet #react #webdev #launchjson #devtools

## Introduction

Debugging is a crucial skill for developers. VS Code offers extensive debugging capabilities. This note summarizes key features and workflows for debugging various application types in VS Code, based on the official beginner guide.

---

## 1. Basic Debugging: JavaScript & Node.js (Out-of-the-Box)

VS Code provides excellent out-of-the-box debugging for simple JavaScript and Node.js files.

### Setting Up & Starting
1.  **Add a Breakpoint:**
    *   Go to the desired line number (e.g., line 6).
    *   Click in the gutter to the left of the line number. A red dot will appear, indicating a breakpoint.
2.  **Start Debugging:**
    *   Click the "Run and Debug" icon in the Activity Bar (left-hand side).
    *   Click the "Run and Debug" button.
    *   **First-time setup:** If prompted, choose `Node.js` from the dropdown.
    *   The debugger will start and pause execution at the breakpoint.

### Debug Panes (Left Sidebar)
When a breakpoint is hit, several panes provide debugging information:

*   **Variables:**
    *   Displays variables in the current debugging scope.
    *   Shows their types and current values.
    *   Includes local variables.
*   **Watch:**
    *   Allows tracking specific expressions or variables throughout the debugging session.
    *   Add expressions by clicking the `+` icon.
    *   Useful for variables not in the immediate local scope or for evaluating expressions.
*   **Call Stack:**
    *   Shows the hierarchy of function calls at the current moment.
    *   Indicates the path the program took to reach the current breakpoint.
    *   The most recent call is at the top.
*   **Loaded Scripts:**
    *   Lists all scripts loaded in the current debugging session.
    *   Useful for navigating different parts of your code or libraries.

### [[Debug Toolbar ]](Top of Screen)
A floating toolbar appears with control buttons:

*   **Continue (Play icon):** Resumes execution until the next breakpoint or the end of the program.
*   **Step Over (Curved arrow over dot):** Executes the current line. If it's a function call, it executes the entire function without stepping into its details.
*   **Step Into (Downward arrow):** If the current line is a function call, it navigates into the function's code.
*   **Step Out (Upward arrow):** If inside a function, it executes the rest of the function and returns to the line where the function was called.
*   **Restart (Curved arrow):** Restarts the entire debugging process.
*   **Stop (Red square):** Terminates the debugging session.

---

## 2. Debugging Other Project Types (e.g., C#)

For languages/projects not supported by default, VS Code extensions are necessary.

### C# Project Example (Polymorphism Demo)
*   **Objective:** Determine worker salary based on employee/contractor status.
*   **Prerequisites (Extensions):**
    *   **C# Dev Kit:** Helps manage C# code.
    *   **C# Extension:** Core C# language support.
    *   **.NET Install Tool:** Sets up the .NET runtime.
    *   *(Referenced video for detailed setup instructions)*

### Debugging Workflow (C#):
1.  Set a breakpoint (e.g., line 48 in the `Main` method).
2.  Start "Run and Debug".
3.  **Using Debug Toolbar:**
    *   **Step Over:** Demonstrated stepping over a method call.
    *   **Step Into:** Stepped into `DetermineWeeklySalary` method for a `Contractor`.
4.  **Using Debug Panes:**
    *   **Variables (Locals):** Observed `wage` and `weeklyHours`.
    *   **Watch:**
        *   Added `person` (initially "does not exist in current context").
        *   Added `salary` (initially 0, updated to 3850 after stepping).
        *   After stepping out of `DetermineWeeklySalary`, `person` became available in the `Watch` pane, showing it's a `Contractor`.
    *   **Call Stack:**
        *   Inside `DetermineWeeklySalary`: `DetermineWeeklySalary` (top), `Main` program (below).
        *   After stepping out: Only `Main` program listed.
5.  **Debug Console:**
    *   Can be used to quickly check values.
    *   Example: typing `wage` showed `70`; typing `person` showed the object type (`Contractor`).
6.  **Restart & Stop:** Demonstrated restarting the session and stopping it.
7.  **Breakpoints View:** At the bottom of the debug sidebar, a view lists all active breakpoints.

---

## 3. Debugging Web Apps (React CRUD Example)

### Project Overview
*   React CRUD application for employee management (Create, Read, Update, Delete).
*   Runs on a specific port (e.g., `Port 3000`).

### `launch.json` Configuration
Crucial for web app debugging. It tells VS Code how to launch and attach to the application.
*   Access/create it via the "Run and Debug" view (gear icon or "create a launch.json file").
*   **Key Properties for a browser launch:**
    *   `"type"`: Specifies the debugger type. For Chrome: `pwa-chrome`. For Edge: `msedge`.
    *   `"request"`: Typically `"launch"` to launch a new browser instance.
    *   `"name"`: A user-friendly name for this debug configuration (e.g., "Launch Chrome against localhost").
    *   `"url"`: The URL to open, including the port (e.g., `http://localhost:3000`).
    *   `"webRoot"`: The root of your web server files, often `"${workspaceFolder}"`.
    *   *(Speaker suggests asking Chat AI to define these if unsure).*

```json
// Example launch.json for Chrome
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "pwa-chrome", // or "msedge" for Edge
      "request": "launch",
      "name": "Launch Chrome against localhost",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}"
    }
  ]
}
```

### Advanced Debugging Techniques (React App):

1.  **Manipulating Variables During Debugging:**
    *   Set a breakpoint (e.g., in an edit/update function).
    *   Trigger the breakpoint (e.g., by editing an employee's name like "George Blue" to "George Strong" and clicking update).
    *   In the **Variables** or **Watch** pane, find the variable (e.g., the new name "Strong").
    *   Right-click the variable -> **Set Value**.
    *   Change the value (e.g., from "Strong" to "Stronger").
    *   Continue execution. The application will use the modified value.

2.  **Conditional Breakpoints:**
    *   Set a normal breakpoint.
    *   Right-click the red dot -> **Edit Breakpoint...**.
    *   Choose "Expression" from the dropdown.
    *   Enter a condition (e.g., `firstName === "Adrien"`).
    *   The breakpoint will now only pause execution if the condition is true when that line is hit.
    *   Example: Updating "Raynal" didn't hit the breakpoint. Updating "Adrien" did.

3.  **Console Logging & Debug Console Interaction:**
    *   Use `console.log()`, `console.info()`, etc., in your code (e.g., `console.info("We are in edit mode", selectedEmployeeObject)`).
    *   Output appears in the **Debug Console** tab in VS Code's panel.
    *   The Debug Console is interactive:
        *   Access global objects like `window`.
        *   Inspect DOM elements (e.g., `document.body`).
        *   Modify styles dynamically (e.g., `document.body.style.backgroundColor = 'green'`).

---

## 4. Edge Developer Tools Integration

VS Code can integrate Microsoft Edge Developer Tools directly within the editor for a richer debugging experience.

### Setup:
1.  **`launch.json` for Edge:**
    *   Ensure your `launch.json` configuration has `"type": "msedge"`.
    *   Point to the correct URL and port.
2.  **Extension:**
    *   Install the **"Microsoft Edge Tools for VS Code"** extension.

### Usage:
1.  Start debugging using the Edge configuration.
2.  A new icon will appear on the debug toolbar (often looks like the Edge logo or a tools icon).
3.  Click this icon to open the Edge Developer Tools panel *inside* VS Code.
4.  **Features:**
    *   **Elements Tab:** Inspect and modify the DOM structure and CSS.
    *   **Styles Pane:** Change CSS properties (e.g., text color, background color) and see live updates.
    *   Provides the convenience of browser dev tools without leaving VS Code.

---

## Conclusion & Further Learning

*   VS Code offers powerful and flexible debugging tools.
*   Mastering these tools can significantly improve development efficiency.
*   **Shoutout:** Safdar Jamil for the React app referenced (GitHub link provided by speaker).
*   **Official Docs:** For more in-depth information, refer to the VS Code debugging documentation: [VS Code Debugging Docs](https://code.visualstudio.com/docs/editor/debugging) (actual link might vary, speaker pointed to one).
*   **Community Request:** Speaker mentioned making a "Part 2" video on topics like `launch.json` configuration if there's interest (50 comments).

---
