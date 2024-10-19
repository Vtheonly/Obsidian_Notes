## Useful JavaScript Syntax Tricks

### 1. Destructuring Assignment with Default Values
```javascript
let { prop1, prop2 = "default" } = someObject;
```
You can use default values in destructuring assignments, which is handy when extracting properties from objects.

### 2. Using the Logical OR (`||`) for Default Values
```javascript
let username = userInput || "Guest";
```
The logical OR (`||`) can be used to provide a default value if the left operand is falsy.

### 3. Using `Object.assign` for Object Merging
```javascript
let mergedObject = Object.assign({}, obj1, obj2);
```
`Object.assign` is useful for merging objects. The first argument is the target object, and subsequent arguments are the source objects.

### 4. Array Spreading
```javascript
let arr1 = [1, 2, 3];
let arr2 = [...arr1, 4, 5];
```
The spread operator (`...`) is useful for spreading elements from one array (or object) into another.

### 5. Immediately Invoked Function Expressions (IIFE)
```javascript
(function() {
  // Your code here
})();
```
IIFE is a function expression that is executed immediately after being created, creating a private scope.

### 6. Using `Array.from` for Array-Like Objects
```javascript
let arrayLike = document.querySelectorAll(".some-class");
let realArray = Array.from(arrayLike);
```
`Array.from` can convert array-like objects (such as the result of `querySelectorAll`) into real arrays.

### 7. Optional Chaining (?.)
```javascript
let city = user?.address?.city;
```
Optional chaining (`?.`) allows you to safely access nested properties without explicitly checking each level for existence.

### 8. Nullish Coalescing Operator (`??`)
```javascript
let value = somePossiblyUndefinedValue ?? "default";
```
The nullish coalescing operator (`??`) provides a default value only if the left operand is `null` or `undefined`, not for falsy values.

### 9. Using the Comma Operator to Combine Statements
```javascript
let a = 1, b = 2, c = 3;
```
The comma operator allows you to combine multiple statements into a single line. The value of the entire expression is the value of the last expression.

### 10. Using Tilde (~) for Bitwise NOT and Index Conversion
```javascript
let num = 5;
let bitwiseNot = ~num; // Bitwise NOT of 5 is -6
```
The tilde (~) operator performs bitwise NOT, but it's also used to convert an index to its negative counterpart in some scenarios.

### 11. Double Exclamation Mark (!!)
```javascript
let someValue = "Hello";
let isTruthy = !!someValue; // Converts any value to a boolean
```
The double exclamation mark (!! or "not not") is a quick way to convert any value to its boolean equivalent.

### 12. Void Operator (void)
```javascript
void 0; // Evaluates to undefined
```
The `void` operator is often used to obtain the `undefined` value in a concise manner.

### 13. Using Template Literals for Multi-line Strings
```javascript
let multiLineString = `
This is a
multi-line
string.
`;
```
Template literals allow you to create multi-line strings without explicitly using newline characters.

### 14. Short-Circuit Evaluation
```javascript
let result = someCondition && "This value is returned if someCondition is true";
```
Using the logical AND (`&&`) operator for short-circuit evaluation can be a concise way to provide default values or execute code conditionally.

### Additional Formatting Example
```javascript
let x = ${0|2};
```
This syntax is used in code templates or snippets to provide multiple choices for a variable value, often seen in code editors or IDEs with snippet functionality.