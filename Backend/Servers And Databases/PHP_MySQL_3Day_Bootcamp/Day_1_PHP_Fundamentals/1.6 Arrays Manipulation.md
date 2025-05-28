# PHP Arrays - Comprehensive Guide

## Array Types

### Indexed Arrays
```php
$colors = ['red', 'green', 'blue'];
$colors = array('red', 'green', 'blue');
```

### Associative Arrays
```php
$person = [
    'name' => 'John',
    'age' => 30
];
```

### Multidimensional Arrays
```php
$matrix = [
    [1, 2, 3],
    [4, 5, 6]
];
```

## Array Creation

### Range
```php
$numbers = range(1, 10);
```

### Fill
```php
$filled = array_fill(0, 5, 'default');
```

### Combine
```php
$keys = ['a', 'b'];
$values = [1, 2];
$combined = array_combine($keys, $values);
```

## Array Operations

### Adding Elements
```php
$colors[] = 'yellow'; // Add to end
array_push($colors, 'purple'); // Add to end
array_unshift($colors, 'black'); // Add to start
```

### Removing Elements
```php
array_pop($colors); // Remove last
array_shift($colors); // Remove first
unset($colors[1]); // Remove by index
```

### Slicing
```php
$slice = array_slice($colors, 1, 2);
```

### Merging
```php
$merged = array_merge($array1, $array2);
```

## Array Functions

### Sorting
```php
sort($array); // By value
asort($array); // By value, keep keys
ksort($array); // By key
```

### Searching
```php
in_array('red', $colors); // Check existence
array_search('red', $colors); // Get key
array_key_exists('name', $person); // Check key
```

### Filtering
```php
$filtered = array_filter($array, function($item) {
    return $item > 10;
});
```

### Mapping
```php
$mapped = array_map(function($item) {
    return $item * 2;
}, $array);
```

### Reducing
```php
$sum = array_reduce($array, function($carry, $item) {
    return $carry + $item;
}, 0);
```

## Array Destructuring
```php
[$a, $b] = [1, 2];
['name' => $name, 'age' => $age] = $person;
```

## Array Best Practices
1. Use descriptive keys for associative arrays
2. Prefer array syntax [] over array()
3. Use array functions for complex operations
4. Consider performance for large arrays
5. Document array structures