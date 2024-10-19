Section 19.2: Currying Currying is the transformation of a function of n arity or arguments into a sequence of n functions taking only one argument


**Curried Rectangle Area Function:**

```javascript
function curryRectangleArea(length) {
  return function(width) {
    return length * width;
  };
}
```

**Description:**

The `curryRectangleArea` function is a curried function designed to calculate the area of a rectangle. The purpose of currying is to transform a function with multiple parameters into a series of functions, each taking a single argument.

1. **First Function:**
   - The outer function, `curryRectangleArea`, takes a single parameter `length`.
   - It returns a new function, an inner function.

2. **Second Function:**
   - The inner function takes a single parameter `width`.
   - When both parameters `length` and `width` are provided, it calculates and returns the area of the rectangle using the formula `length * width`.

**Usage Example:**

```javascript
// Using the curried function
const areaFunction = curryRectangleArea(4);
const area1Curried = areaFunction(5); // Area with length 4 and width 5
const area2Curried = areaFunction(8); // Area with length 4 and width 8
const area3Curried = areaFunction(6); // Area with length 4 and width 6
```

**Description of Usage:**

- The `curryRectangleArea` function is partially applied with a specific `length` value (in this case, `4`), creating a new function called `areaFunction`.
- The `areaFunction` function is then invoked with different `width` values to calculate the area of rectangles with the fixed `length`.
- This allows for the creation of specialized functions for calculating the area with a constant length, avoiding the need to repeatedly pass the same length value.

**Advantages:**

- **Partial Application:** It enables the creation of partially applied functions with fixed values for certain parameters.
- **Function Composition:** It facilitates function composition, allowing for the creation of more modular and reusable functions.
- **Readability:** It enhances code readability by breaking down a function with multiple parameters into a series of smaller functions, each focused on one parameter.

In summary, the `curryRectangleArea` function showcases the concept of currying, providing a more flexible and modular way to calculate the area of rectangles in JavaScript.