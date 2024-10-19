Importing and exporting modules is a fundamental concept in modern JavaScript that helps manage and structure code effectively. Here's a detailed guide on how to use them:

### Modules in JavaScript

Modules allow you to break your code into reusable pieces, each with its own context, which makes it easier to maintain and understand. ES6 introduced a native module system to JavaScript.

### Exporting Modules

There are two main ways to export modules: named exports and default exports.

#### Named Exports

Named exports allow you to export multiple values from a module. Each value is exported with its own name.

**Example:**
```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
```

You can also export values as you define them:
```javascript
export const PI = 3.14;
export function multiply(a, b) {
  return a * b;
}
```

#### Default Exports

Default exports are used to export a single value from a module. Each module can have only one default export.

**Example:**
```javascript
// calculator.js
export default function(a, b) {
  return a + b;
}
```

You can also export a class or an object as the default export:
```javascript
// person.js
export default class Person {
  constructor(name) {
    this.name = name;
  }
}
```

### Importing Modules

To use exported values in another module, you import them.

#### Importing Named Exports

You can import named exports using the `import` statement and curly braces to specify the names.

**Example:**
```javascript
// app.js
import { add, subtract } from './math.js';

console.log(add(2, 3)); // 5
console.log(subtract(5, 3)); // 2
```

If you want to import all named exports from a module, you can use the `*` syntax:
```javascript
import * as math from './math.js';

console.log(math.add(2, 3)); // 5
console.log(math.subtract(5, 3)); // 2
```

#### Importing Default Exports

Default exports are imported without curly braces, and you can give them any name.

**Example:**
```javascript
// main.js
import add from './calculator.js';

console.log(add(2, 3)); // 5
```

You can import both default and named exports from the same module:
```javascript
// index.js
import defaultFunc, { namedFunc1, namedFunc2 } from './module.js';

defaultFunc();
namedFunc1();
namedFunc2();
```

### Combining Export Types

You can combine default and named exports in a single module.

**Example:**
```javascript
// utils.js
export default function greet(name) {
  return `Hello, ${name}!`;
}

export const PI = 3.14;
export function square(x) {
  return x * x;
}
```

**Importing:**
```javascript
// main.js
import greet, { PI, square } from './utils.js';

console.log(greet('World')); // Hello, World!
console.log(PI); // 3.14
console.log(square(2)); // 4
```

### Resources and Further Reading

For more in-depth information and examples, you can explore these resources:

- [MDN Web Docs - Export](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export)
- [MDN Web Docs - Import](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/import)
- [JavaScript.info - Modules](https://javascript.info/modules)

These resources provide comprehensive explanations and additional examples to help you master the concept of modules in JavaScript.

### Named vs Default Exports and Import All

In JavaScript, the ES6 module system provides two main types of exports: named exports and default exports. Understanding these concepts is crucial for effectively structuring and maintaining your code. Here’s a detailed explanation of each:

### Named Exports

Named exports allow you to export multiple values from a module. Each value is exported with its own name, which must be used when importing.

**Example:**
```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
```

To import named exports, you need to use the same names in curly braces:

**Importing Named Exports:**
```javascript
// app.js
import { add, subtract } from './math.js';

console.log(add(2, 3)); // 5
console.log(subtract(5, 3)); // 2
```

You can also rename the imported values using the `as` keyword:

**Renaming Imports:**
```javascript
import { add as addition, subtract as subtraction } from './math.js';

console.log(addition(2, 3)); // 5
console.log(subtraction(5, 3)); // 2
```

### Default Exports

Default exports are used to export a single value from a module. Each module can have only one default export.

**Example:**
```javascript
// calculator.js
export default function(a, b) {
  return a + b;
}
```

To import a default export, you don’t use curly braces and you can give it any name you like:

**Importing Default Exports:**
```javascript
// main.js
import add from './calculator.js';

console.log(add(2, 3)); // 5
```

### Combining Named and Default Exports

A module can have both named exports and a default export:

**Example:**
```javascript
// utils.js
export default function greet(name) {
  return `Hello, ${name}!`;
}

export const PI = 3.14;
export function square(x) {
  return x * x;
}
```

**Importing Both:**
```javascript
// main.js
import greet, { PI, square } from './utils.js';

console.log(greet('World')); // Hello, World!
console.log(PI); // 3.14
console.log(square(2)); // 4
```

### Import All

You can import all named exports from a module using the `*` syntax and give them a namespace:

**Example:**
```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
export const multiply = (a, b) => a * b;
```

**Importing All:**
```javascript
// app.js
import * as math from './math.js';

console.log(math.add(2, 3)); // 5
console.log(math.subtract(5, 3)); // 2
console.log(math.multiply(2, 3)); // 6
```

### Key Differences and Best Practices

1. **Use Cases**:
   - **Named Exports**: Best when you need to export multiple values from a module. They provide clarity and explicitness.
   - **Default Exports**: Best for exporting a single main value or function from a module.

2. **Readability**:
   - Named exports improve readability by being explicit about what is imported.
   - Default exports can sometimes make the module usage less clear, especially in large codebases.

3. **Consistency**:
   - Consistently use named exports if your module exports multiple items.
   - Use default exports for modules that export a single primary function or class.

### Resources and Further Reading

For more detailed information and examples, refer to the following resources:

- [MDN Web Docs - Export](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export)
- [MDN Web Docs - Import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import)
- [JavaScript.info - Modules](https://javascript.info/modules)

These resources provide comprehensive explanations and additional examples to help you master the concept of modules in JavaScript.