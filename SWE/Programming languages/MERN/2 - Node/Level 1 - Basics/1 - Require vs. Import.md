In JavaScript, particularly in the context of Node.js and ES6 (ECMAScript 2015), there are two primary ways to load and export modules: using `require` with `module.exports` and using `import` with `export`. Here are the key differences between them:

### 1. **Require vs. Import**

#### **`require`**
- **Syntax**: `const module = require('module-name');`
- **Usage Context**: Primarily used in Node.js.
- **Loading Mechanism**: `require` is synchronous and can be used anywhere in the code. It loads modules dynamically at runtime.
- **Module Type**: It is based on CommonJS, a module system used in Node.js.
- **Dynamic Imports**: Since it’s a function, it can be used conditionally or at runtime.

  ```javascript
  if (condition) {
    const myModule = require('./myModule');
  }
  ```

#### **`import`**
- **Syntax**: `import moduleName from 'module-name';`
- **Usage Context**: Used in ES6+ JavaScript, which is also supported in modern front-end development and newer versions of Node.js (with the `.mjs` file extension or by setting `"type": "module"` in `package.json`).
- **Loading Mechanism**: `import` is static and is hoisted to the top of the file. It happens before the code is executed, so you cannot use it conditionally at runtime.
- **Module Type**: Based on ES6 modules (also known as ECMAScript modules or ESM).
- **Static Imports**: Must be at the top of the file and cannot be dynamically imported in the same way as `require`.

  ```javascript
  import myModule from './myModule';
  ```

### 2. **module.exports vs. export**

#### **`module.exports`**
- **Context**: Used with `require` in CommonJS (Node.js).
- **Usage**: You assign anything to `module.exports`, such as an object, a function, a class, etc. This is what will be returned when the module is `require`d.
  
  ```javascript
  // In myModule.js
  module.exports = function() {
    console.log('This is a CommonJS module!');
  };

  // In another file
  const myModule = require('./myModule');
  myModule(); // Outputs: This is a CommonJS module!
  ```

- **Default Export**: Since you directly assign to `module.exports`, there's only one export per module (though you can attach multiple properties to an object and export that).

#### **`export` and `export default`**
- **Context**: Used with `import` in ES6 modules.
- **Named Export**: You can export multiple items (functions, variables, classes) from a module by prefixing them with `export`.

  ```javascript
  // In myModule.js
  export function myFunction() {
    console.log('This is an ES6 module function!');
  }

  export const myVariable = 42;
  ```

- **Default Export**: You can export a single default item from a module. This is useful when a module only exports one main thing.

  ```javascript
  // In myModule.js
  export default function() {
    console.log('This is the default export!');
  }

  // In another file
  import myModule from './myModule';
  myModule(); // Outputs: This is the default export!
  ```

- **Flexibility**: ES6 modules allow both named and default exports in the same module.

  ```javascript
  // In myModule.js
  export function myFunction() { /* ... */ }
  export default class MyClass { /* ... */ }
  ```

### **Summary**
- **`require` and `module.exports`** are used in CommonJS (Node.js).
- **`import` and `export`** are used in ES6 modules, which are more standard in modern JavaScript, especially for front-end development.
- **`require`** is synchronous and can be used conditionally at runtime, while **`import`** is static and hoisted.
- **`module.exports`** allows exporting a single entity from a module, whereas **`export`** supports both named and default exports, providing more flexibility.

Here’s a table summarizing the differences between `require` and `import`, as well as between `module.exports` and `export`:

| Feature                  | `require`                        | `import`                          |
|--------------------------|----------------------------------|-----------------------------------|
| **Usage Context**        | Node.js (CommonJS modules)       | ES6+ (ECMAScript modules)         |
| **Syntax**               | `const module = require('module');` | `import module from 'module';`    |
| **Loading Mechanism**    | Synchronous, can be used anywhere | Static, hoisted to the top of the file |
| **Dynamic Import**       | Yes, can be used conditionally or at runtime | No, must be used at the top of the file |
| **Module Type**          | CommonJS                         | ES6 modules (ESM)                 |

| Feature                  | `module.exports`                 | `export`                          |
|--------------------------|----------------------------------|-----------------------------------|
| **Usage Context**        | Node.js (CommonJS modules)       | ES6+ (ECMAScript modules)         |
| **Default Export**       | Yes, exports a single value      | Yes, using `export default`       |
| **Named Export**         | No                               | Yes, using `export`               |
| **Syntax**               | `module.exports = value;`        | `export const value = ...;`       |
| **Flexibility**          | Exports one entity               | Can export multiple named entities and a default export | 
