# PHP Control Structures - Comprehensive Guide

## Conditional Statements

### If/Else
```php
if ($condition) {
    // code
} elseif ($otherCondition) {
    // code
} else {
    // code
}
```

### Ternary Operator
```php
$result = $condition ? 'true' : 'false';
```

### Null Coalescing
```php
$result = $value ?? 'default';
```

## Switch Statement
```php
switch ($variable) {
    case 'value1':
        // code
        break;
    case 'value2':
        // code
        break;
    default:
        // code
}
```

## Loops

### For Loop
```php
for ($i = 0; $1 < 10; $i++) {
    // code
}
```

### While Loop
```php
while ($condition) {
    // code
}
```

### Do-While Loop
```php
do {
    // code
} while ($condition);
```

### Foreach Loop
```php
foreach ($array as $key => $value) {
    // code
}
```

## Loop Control
```php
break;    // Exit loop
continue; // Skip to next iteration
```

## Alternative Syntax
```php
if ($condition):
    // code
else:
    // code
endif;
```

## Error Control
```php
try {
    // code
} catch (Exception $e) {
    // handle error
} finally {
    // cleanup
}