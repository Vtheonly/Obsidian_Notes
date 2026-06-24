### Syntax of Arrow Functions

1. **Basic Syntax**:

   Without parameters:
   ```javascript
   let func = () => expression;
   ```

   With one parameter:
   ```javascript
   let func = param => expression;
   ```

   With multiple parameters:
   ```javascript
   let func = (param1, param2, ...) => expression;
   ```

   For a multi-line function body, use curly braces and `return`:
   ```javascript
   let func = (param1, param2, ...) => {
     // multiple lines of code
     return expression;
   };
   ```

2. **Examples**:

   Without parameters:
   ```javascript
   let greet = () => "Hello, World!";
   console.log(greet()); // Outputs: Hello, World!
   ```

   With one parameter:
   ```javascript
   let square = x => x * x;
   console.log(square(5)); // Outputs: 25
   ```

   With multiple parameters:
   ```javascript
   let add = (a, b) => a + b;
   console.log(add(2, 3)); // Outputs: 5
   ```

   Multi-line function body:
   ```javascript
   let multiply = (a, b) => {
     let result = a * b;
     return result;
   };
   console.log(multiply(2, 3)); // Outputs: 6
   ```

### When and Why to Use Arrow Functions

1. **Lexical `this` Binding**:
   Arrow functions do not have their own `this` context; they inherit `this` from the parent scope at the time they are defined. This makes them particularly useful for maintaining the correct `this` context within callbacks.

   ```javascript
   function Person() {
     this.age = 0;

     setInterval(() => {
       this.age++; // `this` refers to the Person object
       console.log(this.age);
     }, 1000);
   }

   let person = new Person();
   ```

2. **Concise Syntax**:
   Arrow functions provide a shorter syntax for writing functions, which can make your code more readable and concise, especially for simple one-liner functions.

3. **No `arguments` Object**:
   Arrow functions do not have their own `arguments` object. This can be beneficial when you want to use the `arguments` object of a parent function.

   ```javascript
   function myFunc() {
     console.log(arguments);
     let arrowFunc = () => {
       console.log(arguments); // refers to myFunc's arguments
     };
     arrowFunc();
   }

   myFunc(1, 2, 3); // Outputs: [1, 2, 3]
   ```

4. **No Duplicate Named Parameters**:
   Unlike regular functions, arrow functions cannot have duplicate named parameters, which can help avoid errors in your code.

### When Not to Use Arrow Functions

1. **Methods in Object Literals**:
   Arrow functions should not be used as methods in object literals because they do not have their own `this`.

   ```javascript
   const obj = {
     value: 10,
     method: () => {
       console.log(this.value); // `this` is not the object
     }
   };

   obj.method(); // Outputs: undefined
   ```

2. **Functions with Dynamic Contexts**:
   If a function needs to dynamically set `this` (e.g., in event handlers that need to refer to the element that triggered the event), regular functions are more appropriate.

   ```javascript
   const button = document.querySelector('button');
   button.addEventListener('click', function() {
     console.log(this); // `this` refers to the button
   });
   ```

Arrow functions are a powerful feature in JavaScript, providing a concise syntax and a more predictable behavior for `this`. However, they are not suitable for all use cases, so it's essential to understand when to use them and when to stick with regular functions.