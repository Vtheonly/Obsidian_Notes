# PHP Variables and Data Types - Comprehensive Guide

## Variable Declaration and Scoping

```php
// Variable declaration
$variable = "value"; // Global scope

function test() {
    $localVar = "local"; // Local scope
    global $variable; // Access global variable
    static $staticVar = 0; // Static variable
}

// Variable variables
$varName = "message";
$$varName = "Hello"; // Creates $message
```

## Data Types

### Scalar Types
```php
$string = "Hello"; // String
$int = 42; // Integer
$float = 3.14; // Float
$bool = true; // Boolean
```

### Compound Types
```php
$array = [1, 2, 3]; // Array
$object = new stdClass(); // Object
$callable = function() { return "Hello"; }; // Callable
```

### Special Types
```php
$null = null; // Null
$resource = fopen("file.txt", "r"); // Resource
```

## Type Juggling and Casting
```php
// Automatic type conversion
$result = "5" + 2; // 7 (string to int)

// Explicit casting
$int = (int) "42";
$string = (string) 42;
$array = (array) $object;
```

## Type Checking
```php
is_int($var); // Check if integer
is_string($var); // Check if string
is_array($var); // Check if array
is_object($var); // Check if object
```

## Variable References
```php
$a = 1;
$b = &$a; // $b is reference to $a
$a = 2; // $b is now 2
```

## Constants
```php
define("CONSTANT", "value");
const CONSTANT = "value"; // Class constants
```

## Predefined Variables
```php
$_GET; // GET request data
$_POST; // POST request data
$_SERVER; // Server info
$_SESSION; // Session data
$_COOKIE; // Cookie data
$_FILES; // Uploaded files
$_REQUEST; // GET, POST, COOKIE data
$_ENV; // Environment variables