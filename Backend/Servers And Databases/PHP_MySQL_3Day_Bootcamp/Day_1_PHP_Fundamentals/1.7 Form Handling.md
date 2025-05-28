# PHP Form Handling - Comprehensive Guide

## Form Submission

### HTML Form
```html
<form method="POST" action="process.php">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <input type="submit" value="Submit">
</form>
```

### Processing Form Data
```php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
}
```

## Form Validation

### Server-Side Validation
```php
$errors = [];

if (empty($_POST['username'])) {
    $errors[] = "Username is required";
}

if (strlen($_POST['password']) < 8) {
    $errors[] = "Password must be at least 8 characters";
}
```

### Client-Side Validation
```html
<input type="email" name="email" required>
```

## Security

### Input Sanitization
```php
$username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
$email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
```

### CSRF Protection
```php
session_start();
$_SESSION['token'] = bin2hex(random_bytes(32));
```

```html
<input type="hidden" name="token" value="<?php echo $_SESSION['token']; ?>">
```

## File Uploads

### Handling File Uploads
```php
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["file"]["name"]);
move_uploaded_file($_FILES["file"]["tmp_name"], $target_file);
```

### File Validation
```php
$allowed = ['jpg', 'png', 'gif'];
$ext = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

if (!in_array($ext, $allowed)) {
    $errors[] = "Invalid file type";
}
```

## Form Best Practices
1. Always validate server-side
2. Sanitize all input
3. Use HTTPS for sensitive data
4. Implement CSRF protection
5. Limit file upload size
6. Store files outside web root
7. Use prepared statements for database
8. Hash passwords
9. Implement rate limiting
10. Log form submissions