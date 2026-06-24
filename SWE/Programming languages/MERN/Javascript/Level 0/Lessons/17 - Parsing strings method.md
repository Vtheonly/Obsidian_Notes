I'll cover parsing texts and numbers, conversion methods, and the differences between summing text and summing numbers. I'll also touch on the effect of using the `+` operator before text that contains a number and converting text to numbers and booleans.

### Parsing Texts and Numbers:

#### Parsing Numbers from Text:

```javascript
const textNumber = "123";
const number = parseInt(textNumber, 10); // 123
```

Here, `parseInt` is used to parse the integer from the text. The second argument, `10`, specifies the radix (base) of the numeral system.

#### Parsing Floats from Text:

```javascript
const textFloat = "123.45";
const floatNumber = parseFloat(textFloat); // 123.45
```

The `parseFloat` function is used to parse a floating-point number from the text.

### Conversion Methods:

#### String to Number:

```javascript
const text = "42";
const number = Number(text); // 42
```

The `Number` constructor or coercion can be used to convert a string to a number.

#### Number to String:

```javascript
const number = 42;
const text = number.toString(); // "42"
```

The `toString` method converts a number to its string representation.

### Summing Text and Numbers:

#### Summing Text:

```javascript
const textA = "10";
const textB = "20";
const result = textA + textB; // "1020"
```

When you use the `+` operator with strings, it concatenates them rather than adding their numerical values.

#### Summing Numbers:

```javascript
const numberA = 10;
const numberB = 20;
const sum = numberA + numberB; // 30
```

When you use the `+` operator with numbers, it performs addition.

### Effect of `+` Before Text with Numbers:

```javascript
const text = "42";
const number = +text; // 42
```

The `+` operator before a string containing a number is a unary plus operator, which converts the string to a number.

### Returning Numbers and Booleans from Texts:

#### Converting Text to Numbers:

```javascript
const text = "42";
const number = Number(text); // 42
```

#### Converting Text to Booleans:

```javascript
const text = "true";
const booleanValue = Boolean(text); // true
```

The `Boolean` constructor or coercion can be used to convert a string to a boolean. In this case, any non-empty string is truthy.

Keep in mind that converting from text to number or boolean may result in unexpected behavior if the text is not a valid representation of a number or boolean. It's crucial to handle such cases appropriately in your code.

---
String manipulation is a common task in JavaScript, and there are several string methods that are frequently used. Some of these methods are similar to array methods, as strings can be treated as arrays of characters. Here are some commonly used string methods:

### 1. Concatenation:

- **`concat()`**: Concatenates two or more strings.

  ```javascript
  const str1 = "Hello";
  const str2 = "World";
  const result = str1.concat(" ", str2); // "Hello World"
  ```


### 2. Substring:

- **`substring(startIndex, endIndex)`**: Returns the part of the string between the specified `startIndex` and `endIndex` (excluding `endIndex`).

  ```javascript
  const str = "JavaScript";
  const substr = str.substring(0, 4); // "Java"
  ```

- Important points about `substring()`:
  1. If `startIndex` is greater than `endIndex`, they are swapped automatically.
  2. Negative values are treated as 0.
  3. If `endIndex` is omitted, it extracts characters to the end of the string.

Examples:
```javascript
const str = "JavaScript";
console.log(str.substring(4, 10));  // "Script"
console.log(str.substring(10, 4));  // "Script" (same as above due to swapping)
console.log(str.substring(-3, 4));  // "Java" (negative treated as 0)
console.log(str.substring(4));      // "Script" (to the end of string)
```

The `substring()` method doesn't actually use negative values to count from the end of the string. Any negative value is simply converted to 0. If you need to use negative indices, you might want to look at the `slice()` method instead, which does support negative indices.


### 3. String Length:

- **`length`**: Property that returns the length of a string.

  ```javascript
  const str = "Hello";
  const len = str.length; // 5
  ```

### 4. Accessing Characters:

- **`charAt(index)`**: Returns the character at the specified index.

  ```javascript
  const str = "JavaScript";
  const char = str.charAt(0); // "J"
  ```

### 5. Case Conversion:

- **`toUpperCase()`** and **`toLowerCase()`**: Converts a string to uppercase or lowercase.

  ```javascript
  const str = "JavaScript";
  const upper = str.toUpperCase(); // "JAVASCRIPT"
  const lower = str.toLowerCase(); // "javascript"
  ```

### 6. Searching:

- **`indexOf(substring)`** and **`lastIndexOf(substring)`**: Returns the index of the first/last occurrence of a substring. Returns -1 if not found.

  ```javascript
  const str = "Hello World";
  const index = str.indexOf("o"); // 4
  const lastIndex = str.lastIndexOf("o"); // 7
  ```

### 7. Splitting and Joining:

- **`split(separator)`**: Splits a string into an array of substrings based on a specified separator.

  ```javascript
  const str = "apple,orange,banana";
  const fruitsArray = str.split(","); // ["apple", "orange", "banana"]
  ```

- **`join(separator)`**: Joins the elements of an array into a string, using a specified separator.

  ```javascript
  const fruits = ["apple", "orange", "banana"];
  const fruitsString = fruits.join(","); // "apple,orange,banana"
  ```

### 8. Trim:

- **`trim()`**: Removes whitespace from both ends of a string.

  ```javascript
  const str = "   Hello   ";
  const trimmed = str.trim(); // "Hello"
  ```

### 9. Replace:

- **`replace(searchValue, replaceValue)`**: Replaces occurrences of a specified substring with another string.

  ```javascript
  const str = "Hello World";
  const replaced = str.replace("World", "Universe"); // "Hello Universe"
  ```

### 10. `charAt` vs. Array Access:

String characters can be accessed using array notation, similar to arrays.

```javascript
const str = "JavaScript";
const char = str[0]; // "J"
```

Keep in mind that while array notation works for accessing characters, strings are immutable in JavaScript, so you cannot modify individual characters using array notation.

These are some of the most commonly used string methods in JavaScript. Depending on your specific use case, you might find other string methods to be useful as well.

### 11. `substr()` Method:

The `substr()` method extracts a part of a string, beginning at a specified position and extending for a given number of characters.

Syntax: `string.substr(start, length)`

Key features:
1. `start`: The index at which to begin extraction. If negative, it's treated as `strLength + start` where `strLength` is the length of the string.
2. `length`: (Optional) The number of characters to extract. If omitted, it extracts to the end of the string.

Important notes:
- This method does not modify the original string.
- `substr()` is considered legacy and it's recommended to use `substring()` or `slice()` instead in modern JavaScript.

Examples:
```javascript
const str = "JavaScript";
console.log(str.substr(4, 6));     // "Script"
console.log(str.substr(0, 4));     // "Java"
console.log(str.substr(4));        // "Script" (to the end of string)
console.log(str.substr(-4));       // "ript" (starts 4 from the end)
console.log(str.substr(-4, 2));    // "ri"
console.log(str.substr(1, -1));    // "" (empty string, negative length)
```

The main difference between `substr()` and `substring()` is that `substr()` takes a start index and a length, while `substring()` takes a start index and an end index.


### 12. `includes()` Method:

The `includes()` method determines whether a string contains a specified substring. It returns `true` if the substring is found, and `false` otherwise.

#### Syntax:
```javascript
string.includes(searchString, position)
```

- `searchString`: The substring to search for.
- `position` (optional): The position in the string at which to begin searching. The default is `0`.

#### Examples:
```javascript
const str = "Hello, World!";
console.log(str.includes("World")); // true
console.log(str.includes("world")); // false (case-sensitive)
console.log(str.includes("Hello", 1)); // false (starts searching from position 1)
```

The `includes()` method is case-sensitive and does not modify the original string. It is useful for checking the presence of a substring within a string.



### 13. `splice()` Method:

The `splice()` method changes the contents of an array by removing or replacing existing elements and/or adding new elements in place. 

#### Syntax:
```javascript
array.splice(start, deleteCount, item1, item2, ...)
```

- `start`: The index at which to start changing the array. If negative, it will begin that many elements from the end.
- `deleteCount` (optional): The number of elements to remove. If set to `0`, no elements are removed.
- `item1, item2, ...` (optional): The elements to add to the array, starting from the `start` index. If no elements are specified, `splice()` will only remove elements.

#### Examples:

1. **Removing elements:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   myFriends.splice(2, 1); // Removes 1 element at index 2
   console.log(myFriends); // ["Ahmed", "Sayed", "Osama", "Gamal", "Ameer"]
   ```

2. **Adding elements:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   myFriends.splice(2, 0, "Khaled", "Hassan"); // Adds elements at index 2
   console.log(myFriends); // ["Ahmed", "Sayed", "Khaled", "Hassan", "Ali", "Osama", "Gamal", "Ameer"]
   ```

3. **Replacing elements:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   myFriends.splice(2, 2, "Khaled", "Hassan"); // Replaces 2 elements starting at index 2
   console.log(myFriends); // ["Ahmed", "Sayed", "Khaled", "Hassan", "Gamal", "Ameer"]
   ```

4. **Using negative start index:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   myFriends.splice(-2, 1); // Removes 1 element starting from the second-to-last element
   console.log(myFriends); // ["Ahmed", "Sayed", "Ali", "Osama", "Ameer"]
   ```

The `splice()` method is powerful for modifying arrays in various ways, including removing, adding, or replacing elements.


### 14. `slice()` Method:

The `slice()` method returns a shallow copy of a portion of an array into a new array object selected from `start` to `end` (end not included). The original array will not be modified.

#### Syntax:
```javascript
array.slice(start, end)
```

- `start` (optional): The beginning index of the specified portion of the array. If `undefined`, slicing starts from the beginning (`0`).
- `end` (optional): The end index (exclusive) of the specified portion of the array. If `undefined`, slicing goes until the end of the array (`array.length`).

#### Key Points:
- If `start` is undefined, it defaults to `0`.
- If `end` is undefined, it defaults to the array's length.
- Negative indices can be used, which count from the end of the array.

#### Examples:

1. **Basic usage:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   let newArray = myFriends.slice(1, 3);
   console.log(newArray); // ["Sayed", "Ali"]
   console.log(myFriends); // ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"]
   ```

2. **Omitting `end`:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   let newArray = myFriends.slice(2);
   console.log(newArray); // ["Ali", "Osama", "Gamal", "Ameer"]
   ```

3. **Negative indices:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   let newArray = myFriends.slice(-3, -1);
   console.log(newArray); // ["Osama", "Gamal"]
   ```

4. **Copying the entire array:**
   ```javascript
   let myFriends = ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"];
   let newArray = myFriends.slice();
   console.log(newArray); // ["Ahmed", "Sayed", "Ali", "Osama", "Gamal", "Ameer"]
   ```

The `slice()` method is useful for creating new arrays based on parts of existing arrays without modifying the original arrays.