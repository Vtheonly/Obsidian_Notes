### Primitive Data Types

- **Boolean**: Holds `true` or `false`. Size: 1 bit.
- **Byte**: Stores integers from `-128` to `127`. Size: 1 byte.
- **Short**: Stores integers from `-32,768` to `32,767`. Size: 2 bytes.
- **Int**: Stores integers from `-2^31` to `2^31 - 1`. Size: 4 bytes.
- **Long**: Stores integers from `-2^63` to `2^63 - 1`. Size: 8 bytes.
- **Float**: Stores fractional numbers with up to 6-7 digits of precision. Size: 4 bytes. Requires an `f` suffix when assigning values.
- **Double**: Stores fractional numbers with up to 15 digits of precision. Size: 8 bytes.
- **Char**: Stores a single character. Size: 2 bytes. Enclosed in single quotes.

### Reference Data Types

- **String**: Stores a sequence of characters, such as a word or sentence. Size varies based on content. Begins with a capital `S` because it is a reference data type.

### Differences Between Primitive and Reference Data Types

- **Primitive Data Types**:
  - Limited to a fixed number of types.
  - Store actual data values.
  - Use less memory and offer faster performance.

- **Reference Data Types**:
  - User-defined and virtually unlimited.
  - Store references (memory addresses) instead of actual data.
  - Can hold complex data structures, use more memory, and are slower.

### Variable Creation in Java

1. **Declaration**: Specify the data type and variable name.  
   Example: `int x;`
2. **Assignment**: Assign a value to the variable.  
   Example: `x = 123;`
3. **Initialization**: Combine declaration and assignment in a single step.  
   Example: `int x = 123;`

### Practical Examples

- **Integer Variable**: `int x = 123;`
- **Long Variable**: Use a capital `L` for large numbers.  
  Example: `long debt = 10000000000L;`
- **Float Variable**: Requires an `f` suffix.  
  Example: `float y = 3.14f;`
- **Boolean Variable**: Holds `true` or `false`.  
  Example: `boolean z = true;`
- **Character Variable**: Enclosed in single quotes.  
  Example: `char symbol = '@';`
- **String Variable**: Stores text and can concatenate with other strings or variables.  
  Example: `String name = "John";`

### Naming Conventions in Java

Java is case-sensitive, and by convention:
- **Primitive data types** like `int`, `char`, and `boolean` start with lowercase letters.
- **Reference data types**, which are typically classes, start with uppercase letters. This helps distinguish them from primitive types and other identifiers.

#### Example:

```java
// Primitive data type
int myNumber = 42;

// Reference data type (class)
String myString = "Hello, Java!";
```

