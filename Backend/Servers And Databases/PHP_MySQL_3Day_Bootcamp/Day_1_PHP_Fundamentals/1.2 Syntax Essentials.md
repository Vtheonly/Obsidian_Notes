# PHP Syntax Essentials - In-Depth Guide

## Comprehensive Syntax Rules

### PHP Tags and Modes
```php
<?php // Standard opening tag
// Code goes here
?>  // Closing tag optional for pure PHP files

<?= $variable ?> // Short echo tag (always available since PHP 5.4)

// PHP can be embedded in HTML:
<html>
<body>
    <?php echo date('Y-m-d'); ?>
</body>
</html>
```

### Detailed Output Methods
```php
echo "Hello", " ", "World"; // Can take multiple parameters
print "Hello World";        // Returns 1, can only take one argument

// Output buffering
ob_start();
echo "Content";
$output = ob_get_clean();

// Heredoc syntax
echo <<<EOT
    Multi-line
    string content
    with variables: $variable
EOT;
```

### Advanced Comment Usage
```php
/**
 * PHPDoc comments for documentation
 * @param string $name The user's name
 * @return string Greeting message
 */
function greet($name) {
    return "Hello $name";
}

// Comment best practices:
// - Use // for single-line comments
// - Use /* */ for multi-line or temporary code blocks
// - Use /** */ for documentation
```

### Strict Typing
```php
declare(strict_types=1); // Enables strict type checking

function add(int $a, int $b): int {
    return $a + $b;
}

// Type declarations:
// - bool, int, float, string, array, object
// - self, parent, iterable, mixed
```

### Error Control Operator
```php
$file = @file('non_existent_file'); // @ suppresses errors
if ($file === false) {
    // Handle error
}
```

### Execution Operator
```php
$output = `ls -la`; // Executes shell command
```

### Detailed Case Sensitivity Rules
- Variables: $Var ≠ $var ≠ $VAR
- Constants: define() are case-sensitive by default
- Functions/methods: case-insensitive
- Classes: case-insensitive (but best practice to match declaration)

### Alternative Syntax for Control Structures
```php
<?php if ($condition): ?>
    HTML content here
<?php endif; ?>

<?php foreach ($items as $item): ?>
    <li><?= $item ?></li>
<?php endforeach; ?>