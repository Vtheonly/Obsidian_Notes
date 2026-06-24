Here's a concise explanation of JavaScript's typeof operator:

```javascript
typeof("string"); // "string"
typeof(566); // "number"
typeof(5.66); // "number"
typeof(true); // "boolean"
typeof([1,3,6]); // "object"
typeof({som:'1',sio:2,is:true}); // "object"
typeof(undefined); // "undefined"
typeof(null); // "object"
```

The `typeof` operator recognizes primitive types like strings, numbers, and booleans. Arrays and objects both return "object". Undefined is its own type. Notably, null returns "object", which is a known quirk in JavaScript.