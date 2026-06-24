
Comparison operators are used to compare values and return a boolean result (true or false).

1. **Equal (==)**:
   - Compares values for equality, performing type coercion if necessary.
   - Example: `10 == "10"` returns `true`

2. **Not Equal (!=)**:
   - Checks if values are not equal, performing type coercion if necessary.
   - Example: `10 != "11"` returns `true`

3. **Identical (===)**:
   - Compares both value and type, without type coercion.
   - Example: `10 === "10"` returns `false`

4. **Not Identical (!==)**:
   - Checks if values are not identical in both value and type.
   - Example: `10 !== "10"` returns `true`

5. **Larger Than (>)**:
   - Checks if the left value is greater than the right value.
   - Example: `15 > 10` returns `true`

6. **Larger Than Or Equal (>=)**:
   - Checks if the left value is greater than or equal to the right value.
   - Example: `15 >= 15` returns `true`

7. **Smaller Than (<)**:
   - Checks if the left value is less than the right value.
   - Example: `5 < 10` returns `true`

8. **Smaller Than Or Equal (<=)**:
   - Checks if the left value is less than or equal to the right value.
   - Example: `5 <= 5` returns `true`

Note:
- The `==` and `!=` operators perform type coercion, which can lead to unexpected results. It's generally recommended to use `===` and `!==` for more predictable comparisons.
- When comparing values of different types, JavaScript converts the values to numbers when using `<`, `<=`, `>`, or `>=`.

Examples:
```javascript
console.log(10 == "10");     // true (compares value only)
console.log(-100 == "-100"); // true (compares value only)
console.log(10 === "10");    // false (compares value and type)
console.log(10 !== "10");    // true (compares value and type)
```