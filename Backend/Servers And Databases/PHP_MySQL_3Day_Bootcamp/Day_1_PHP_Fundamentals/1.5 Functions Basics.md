# PHP Functions - Comprehensive Guide

## Function Declaration

```php
function functionName($param1, $param2 = 'default') {
    // Function body
    return $result;
}
```

## Function Parameters

### Required Parameters
```php
function greet($name) {
    return "Hello, $name";
}
```

### Optional Parameters
```php
function greet($name = 'Guest') {
    return "Hello, $name";
}
```

### Variable-length Arguments
```php
function sum(...$numbers) {
    return array_sum($numbers);
}
```

## Return Values

### Returning Values
```php
function add($a, $b) {
    return $a + $b;
}
```

### Returning Multiple Values
```php
function getCoordinates() {
    return [10, 20];
}
list($x, $y) = getCoordinates();
```

## Variable Scope

### Global Variables
```php
$globalVar = 10;

function test() {
    global $globalVar;
    echo $globalVar;
}
```

### Static Variables
```php
function countCalls() {
    static $count = 0;
    return ++$count;
}
```

## Function Types

### Anonymous Functions
```php
$greet = function($name) {
    return "Hello, $name";
};
```

### Arrow Functions
```php
$add = fn($a, $b) => $a + $b;
```

### Callback Functions
```php
function process($callback) {
    return $callback();
}
```

## Built-in Functions

### String Functions
```php
strlen($string);
str_replace('old', 'new', $string);
```

### Array Functions
```php
count($array);
array_map($callback, $array);
```

## Best Practices
1. Use descriptive function names
2. Keep functions small and focused
3. Limit parameters to 3-4
4. Document functions with PHPDoc
5. Avoid global variables
6. Use type hints
7. Handle errors properly