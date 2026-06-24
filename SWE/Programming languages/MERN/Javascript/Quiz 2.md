---
sources:
  - "[[30 - object]]"
  - "[[29 - 'this' keyword]]"
  - "[[28 - closure]]"
  - "[[27 - Nested functions]]"
  - "[[26 - Arrow functions]]"
  - "[[25 - setTimeout]]"
  - "[[24 - Currying]]"
  - "[[23 - map, filter, and reduce]]"
  - "[[22 - Rest Default Params]]"
  - "[[21 - Functions]]"
  - "[[Test - 30 - object]]"
  - "[[Test - 29 - 'this' keyword]]"
  - "[[Test - 28 - closure]]"
  - "[[Test - 27 - Nested functions]]"
  - "[[Test - 26 - Arrow functions]]"
  - "[[Test - 25 - setTimeout]]"
  - "[[Test - 24 - Currying]]"
  - "[[Test - 23 - map, filter, and reduce]]"
  - "[[Test - 22 - Rest Default Params]]"
  - "[[Test - 21 - Functions]]"
---
> [!question] What is the primary purpose of REST parameters (`...`) in a JavaScript function definition?
> a) To define default values for parameters.
> b) To restrict the number of arguments a function can accept.
> c) To gather an indefinite number of arguments into an array.
> d) To refer to the `this` context within the function.
>> [!success]- Answer
>> c) To gather an indefinite number of arguments into an array.

> [!question] What is a key difference between function declarations and function expressions in JavaScript?
> a) Function expressions can accept parameters, while function declarations cannot.
> b) Function declarations are hoisted, while function expressions are not.
> c) Function expressions must always be named, while function declarations can be anonymous.
> d) Function declarations are only used for asynchronous operations.
>> [!success]- Answer
>> b) Function declarations are hoisted, while function expressions are not.

> [!question] How do arrow functions determine the value of `this`?
> a) They always bind `this` to the global object.
> b) They have their own `this` context based on how they are called.
> c) They inherit `this` from the enclosing lexical scope.
> d) They do not have access to `this` at all.
>> [!success]- Answer
>> c) They inherit `this` from the enclosing lexical scope.

> [!question] What is a closure in JavaScript?
> a) A way to close the browser window using JavaScript.
> b) A function that has no access to variables outside its own scope.
> c) An object that bundles data and functions together.
> d) An inner function that retains access to its outer function's scope and variables, even after the outer function has executed.
>> [!success]- Answer
>> d) An inner function that retains access to its outer function's scope and variables, even after the outer function has executed.

> [!question] In JavaScript running in a browser, the `window` object is the top-level object in the JavaScript hierarchy.
>> [!success]- Answer
>> True

> [!question] What is the primary function of the `window.location` property in JavaScript?
> a) To access the DOM document loaded in the window.
> b) To display an alert box with a message.
> c) To provide information about the current URL and allow redirection.
> d) To access local storage for saving data across sessions.
>> [!success]- Answer
>> c) To provide information about the current URL and allow redirection.

> [!question] What is the main difference between the `call` and `apply` methods for invoking a function?
> a) `call` requires arguments as an array, while `apply` requires individual arguments.
> b) `call` creates a bound function, while `apply` invokes the function immediately.
> c) `call` passes arguments individually, while `apply` passes arguments as an array.
> d) `call` sets the `this` value, while `apply` does not.
>> [!success]- Answer
>> c) `call` passes arguments individually, while `apply` passes arguments as an array.

> [!question] According to the text, what does `this` refer to when used in the global context (outside any function) in a browser?
> a) The `document` object
> b) The `window` object
> c) `null`
> d) `undefined`
>> [!success]- Answer
>> b) The `window` object

> [!question] In the provided example of creating an object using object literals (the 'old way'), how are methods like `getFullName` defined?
> a) Using arrow function syntax.
> b) Using the `class` keyword.
> c) Using the `function` keyword directly within the object literal.
> d) By defining them outside the object and assigning them later.
>> [!success]- Answer
>> c) Using the `function` keyword directly within the object literal.

> [!question] Which array method creates a new array with only the elements that pass a test implemented by a provided function?
> a) `map`
> b) `filter`
> c) `reduce`
> d) `forEach`
>> [!success]- Answer
>> b) `filter`

> [!question] When is bracket notation preferred over dot notation for accessing object properties in JavaScript?
> a) When the property name is a valid identifier and known beforehand.
> b) When accessing deeply nested properties.
> c) When the property name is dynamic (stored in a variable) or contains special characters.
> d) Bracket notation is never preferred over dot notation.
>> [!success]- Answer
>> c) When the property name is dynamic (stored in a variable) or contains special characters.

