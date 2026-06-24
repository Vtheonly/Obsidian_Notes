Nested functions, also known as inner functions, are functions defined inside other functions. They serve several purposes and have specific use cases. Let's explore why we might need them and some scenarios where they're particularly useful:

Why use nested functions:

1. Encapsulation: They help in encapsulating functionality within a local scope.
2. Data privacy: Inner functions have access to the outer function's variables, creating a closure.
3. Code organization: They can make code more readable by grouping related functionality.
4. Avoiding global namespace pollution: Inner functions aren't accessible globally.

Best scenarios to use nested functions:

1. Helper Functions:
   When you need a utility function that's only relevant within another function.

   ```javascript
   function calculateTotalPrice(items) {
     function calculateTax(price) {
       return price * 0.1; // 10% tax
     }
     
     let total = 0;
     for (let item of items) {
       total += item.price + calculateTax(item.price);
     }
     return total;
   }
   ```


2. Closures for Data Privacy:
   When you want to create private variables or methods.

   ```javascript
   function createCounter() {
     let count = 0;
     return function() {
       return ++count;
     };
   }
   
   const counter = createCounter();
   console.log(counter()); // 1
   console.log(counter()); // 2
   ```

3. Callback Functions:
   When defining callbacks that need access to the outer function's scope.

   ```javascript
   function fetchData(url) {
     return new Promise((resolve, reject) => {
       function handleResponse(response) {
         if (response.ok) {
           resolve(response.json());
         } else {
           reject(new Error('HTTP error ' + response.status));
         }
       }
       
       fetch(url).then(handleResponse);
     });
   }
   ```

4. Event Handlers:
   When you need to create event handlers with access to local variables.

   ```javascript
   function setupButton(label) {
     const button = document.createElement('button');
     button.textContent = label;
     
     function handleClick() {
       console.log(`Button "${label}" was clicked`);
     }
     
     button.addEventListener('click', handleClick);
     return button;
   }
   ```

5. Immediate Invocation:
   When you need to execute code immediately but keep it encapsulated.

   ```javascript
   function initializeApp() {
     let config = {};
     
     (function setupConfig() {
       config.apiKey = 'abc123';
       config.environment = 'production';
     })();
     
     return config;
   }
   ```

These scenarios showcase how nested functions can enhance code organization, maintain data privacy, and provide elegant solutions to specific programming challenges. They're particularly useful when you need localized functionality that doesn't need to be exposed to the global scope.