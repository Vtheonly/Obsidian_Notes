## 1. Linking JavaScript to HTML

JavaScript needs to connect to your HTML to work with a webpage. You’ve got two ways to do this:

**Inside `<script>` tags:** You write the JavaScript right in your HTML file, usually at the bottom of the `<body>` so the page loads first.

```html
<!DOCTYPE html>
<html>
<head>
  <title>My First Page</title>
</head>
<body>
  <p>This is my page!</p>
  <script>
    console.log("This is my first message!");
    console.log("JavaScript is running!");
  </script>
</body>
</html>
```

When you open this in a browser and check the console (right-click > Inspect > Console), you’ll see both messages printed.

**External .js file:** Keep your JavaScript in a separate file (like `mycode.js`) and link it with `<script src="...">`. Put this line at the end of `<body>` too.

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Page</title>
</head>
<body>
  <p>Look at the console!</p>
  <script src="mycode.js"></script>
</body>
</html>
```

```javascript
// mycode.js
console.log("Hello from a separate file!");
console.log("This is neater for bigger projects!");
```

This keeps your HTML clean and is great when your JavaScript gets longer.

## 2. `console.log`

This is your best friend for seeing what’s happening in your code. It prints stuff to the browser’s console.

```javascript
console.log("I’m learning JavaScript!"); // Prints that exact text
console.log(10);                        // Prints the number 10
console.log(5 + 2);                     // Calculates and prints 7
console.log("Hi", 123);                 // Prints: Hi 123 (you can list multiple things)
```

Think of it like a way to “talk” to yourself while coding to check if things work.

## 3. Variables (`var`, `let`, `const`)

Variables are like labeled boxes where you store stuff (numbers, text, etc.). Here’s more detail:

**`var`**: The old-school way. You can change its value anytime and even redeclare it (say it’s a new box with the same name).

```javascript
var name = "Alice";
console.log(name); // Prints: Alice

name = "Bob";      // Change the value
console.log(name); // Prints: Bob

var name = "Charlie"; // Redeclare it (not recommended, but allowed)
console.log(name);    // Prints: Charlie
```

**`let`**: The modern way. You can change the value, but you can’t redeclare it (no making a new box with the same name).

```javascript
let score = 100;
console.log(score); // Prints: 100

score = 150;        // Update it
console.log(score); // Prints: 150

// let score = 200; // This would cause an error!
```

**`const`**: For things that won’t change. Once you set it, it’s locked (but it’s still a box, just one you can’t refill).

```javascript
const price = 5.99;
console.log(price); // Prints: 5.99

// price = 6.99;    // Error! Can’t change a const
```

Use `const` when you know something (like a price or a setting) should stay the same.

## 4. Basic Operations

JavaScript can do math like a calculator. Here’s more on each operator:

**Addition (`+`)**: Adds numbers or sticks text together (called concatenation).

```javascript
let a = 3 + 4;          // 7
console.log(a);

let b = "Hello " + "there"; // "Hello there"
console.log(b);

let c = 5 + " apples";  // "5 apples" (mixing types!)
console.log(c);
```

**Subtraction (`-`)**: Takes one number away from another.

```javascript
let d = 10 - 6;         // 4
console.log(d);
```

**Multiplication (`*`)**: Multiplies numbers.

```javascript
let e = 3 * 4;          // 12
console.log(e);
```

**Division (`/`)**: Divides numbers.

```javascript
let f = 15 / 3;         // 5
console.log(f);

let g = 10 / 4;         // 2.5 (it keeps decimals)
console.log(g);
```

**Modulus (`%`)**: Gives the remainder after division.

```javascript
let h = 10 % 3;         // 1 (10 ÷ 3 = 3 with 1 left over)
console.log(h);

let i = 8 % 2;          // 0 (8 ÷ 2 = 4, no remainder)
console.log(i);
```

## 5. Booleans

Booleans are just `true` or `false`—like a light switch (on or off).

```javascript
let isHappy = true;
console.log(isHappy);    // Prints: true

let isCold = false;
console.log(isCold);     // Prints: false

console.log(5 > 3);      // Prints: true (comparison gives a boolean)
console.log(2 === 5);    // Prints: false (=== checks if they’re equal)
```

You’ll use these a lot with conditions.

## 6. Conditions (`if` statements)

Conditions let your code make decisions. Use `if` to check something, and `else` for what happens if it’s not true.

```javascript
let temperature = 25;

if (temperature > 20) {
  console.log("It’s warm outside!"); // This runs because 25 > 20
} else {
  console.log("It’s cold outside!");
}

let time = 14;
if (time < 12) {
  console.log("Good morning!");
} else if (time < 18) {
  console.log("Good afternoon!"); // This runs because 14 < 18
} else {
  console.log("Good evening!");
}
```

`>` (greater than), `<` (less than), `===` (equal to), `!==` (not equal to) are common checks.

## 7. Loops

Loops repeat code so you don’t have to write it over and over.

**`for` loop:** Great when you know how many times to repeat.

```javascript
for (let i = 1; i <= 3; i++) {
  console.log("Count: " + i); // Prints: Count: 1, Count: 2, Count: 3
}
// i starts at 1, goes up by 1 each time, stops when it’s not <= 3
```

**`while` loop:** Repeats as long as something is true.

```javascript
let energy = 5;
while (energy > 0) {
  console.log("Still going! Energy: " + energy);
  energy--; // Decrease energy by 1
}
// Prints:
// Still going! Energy: 5
// Still going! Energy: 4
// Still going! Energy: 3
// Still going! Energy: 2
// Still going! Energy: 1
```

## 8. Simple Functions

Functions are like little machines: you give them a job, and they do it when you “turn them on” (call them). Here’s how to make them:

**Defining a function:** Use the `function` keyword, give it a name, and add code inside `{}`.

```javascript
function sayHello() {
  console.log("Hello, everyone!");
}

sayHello(); // Call it to run it - Prints: Hello, everyone!
sayHello(); // Call it again - Prints it again!
```

**Functions with inputs:** Add parameters (like knobs on the machine) to customize it.

```javascript
function addNumbers(num1, num2) {
  let result = num1 + num2;
  console.log("The sum is: " + result);
}

addNumbers(3, 4); // Prints: The sum is: 7
addNumbers(10, 5); // Prints: The sum is: 15
```

Functions save you from repeating code—just call them whenever you need that job done!

## Putting It All Together

Here’s a tiny example using most of these basics:

```html
<!DOCTYPE html>
<html>
<body>
  <script>
    const goal = 10;
    let current = 0;

    function countUp() {
      while (current < goal) {
        current = current + 1;
        console.log("Current number: " + current);
      }
      if (current === goal) {
        console.log("Reached the goal!");
      }
    }

    countUp(); // Runs the function
  </script>
</body>
</html>
```

## More About Data Types

1.  **More About Data Types (Specifically Strings and Numbers)**

    *   **Strings in Detail:** You've used strings like `"Hello"`.  Strings are for text.  It's good to know you can do more with them:
        *   **String Length:**  Find out how many characters are in a string.
        *   **Changing Case:** Make strings uppercase or lowercase.
        *   **Getting Parts of Strings (Slicing):** Grab just a piece of a string.

        ```javascript
        let message = "Hello World";

        console.log(message.length);       // Output: 11 (counts spaces too!)
        console.log(message.toUpperCase());  // Output: HELLO WORLD
        console.log(message.toLowerCase());  // Output: hello world
        console.log(message.slice(0, 5));  // Output: Hello (from the start up to, but not including, index 5)
        console.log(message.slice(6));     // Output: World (from index 6 to the end)
        ```

    *   **Numbers - Math Objects:**  JavaScript has a built-in `Math` object for more math stuff than just `+ - * / %`.
        *   **Rounding:** Round numbers up or down.
        *   **Random Numbers:** Generate random numbers (very useful for games or simulations!).
        *   **Absolute Value:** Get the positive version of a number.

        ```javascript
        console.log(Math.round(4.7));   // Output: 5 (rounds to the nearest whole number)
        console.log(Math.ceil(4.2));    // Output: 5 (rounds up)
        console.log(Math.floor(4.9));   // Output: 4 (rounds down)
        console.log(Math.random());    // Output: A random number between 0 (inclusive) and 1 (exclusive)
        console.log(Math.abs(-5));      // Output: 5 (absolute value)
        ```

2.  **Arrays (Lists of Things)**

    *   Arrays are like ordered lists. You can store many values in one variable.
    *   **Creating Arrays:**
    *   **Accessing Elements:** Get items out of the array using their position (index).
    *   **Adding and Removing Elements:**  Put things in and take things out of arrays.

        ```javascript
        let colors = ["red", "green", "blue"]; // Array of strings

        console.log(colors[0]);     // Output: red (arrays start at index 0)
        console.log(colors[1]);     // Output: green
        console.log(colors.length);  // Output: 3 (how many items in the array)

        colors.push("yellow");       // Add "yellow" to the end
        console.log(colors);         // Output: ["red", "green", "blue", "yellow"]

        colors.pop();              // Remove the last item ("yellow")
        console.log(colors);         // Output: ["red", "green", "blue"]

        colors.unshift("purple");    // Add "purple" to the beginning
        console.log(colors);         // Output: ["purple", "red", "green", "blue"]

        colors.shift();             // Remove the first item ("purple")
        console.log(colors);         // Output: ["red", "green", "blue"]
        ```
