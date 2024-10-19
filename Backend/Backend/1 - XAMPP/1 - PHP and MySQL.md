
### Next Step: PHP and MySQL Integration Using XAMPP

In this section, we will delve into **PHP** and **MySQL**, exploring their integration, common practices, and useful features for developing dynamic web applications.

#### Part 2: PHP Overview

---

### 1. **Introduction to PHP**

**PHP (Hypertext Preprocessor)** is a popular server-side scripting language designed for web development. It is embedded within HTML and can interact with databases, making it an ideal choice for dynamic web applications. 

#### Key Features of PHP:
- **Simplicity**: Easy to learn for beginners.
- **Open Source**: Free to use and widely supported.
- **Cross-Platform**: Runs on various operating systems (Windows, Linux, macOS).
- **Database Support**: Integrates seamlessly with MySQL and other databases.

---

### 2. **Setting Up PHP in XAMPP**

After installing XAMPP, PHP is automatically included. To verify that PHP is working correctly:

1. **Create a PHP File**:
   Navigate to the `htdocs` directory where you place your web files:
   ```bash
   cd /opt/lampp/htdocs
   ```

2. **Create a Test PHP File**:
   Use a text editor to create a file named `info.php`:
   ```bash
   nano info.php
   ```
   Add the following code:
   ```php
   <?php
   phpinfo();
   ?>
   ```

3. **Access the File in a Browser**:
   Open your browser and go to `http://localhost/info.php`. This should display the PHP configuration page, confirming that PHP is operational.

---

### 3. **Basic PHP Syntax**

- **Variables**: Declared using the `$` symbol.
    ```php
    $name = "John Doe";
    ```
- **Data Types**: String, Integer, Float, Boolean, Array, Object.
- **Control Structures**: Includes `if`, `else`, `for`, `while`, etc.
    ```php
    if ($age >= 18) {
        echo "Adult";
    } else {
        echo "Minor";
    }
    ```

---

### 4. **Integrating PHP with MySQL**

#### 1. **Connecting to MySQL Database**

You can connect PHP to your MySQL database using the `mysqli` extension. Here’s how:

```php
<?php
$servername = "localhost";
$username = "root";
$password = ""; // Default password for XAMPP MySQL
$dbname = "test_db"; // Replace with your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?>
```

#### 2. **Creating a Database and Table**

To create a database and a table using PHP:

```php
<?php
$conn = new mysqli($servername, $username, $password);

// Create database
$sql = "CREATE DATABASE test_db";
if ($conn->query($sql) === TRUE) {
    echo "Database created successfully";
} else {
    echo "Error creating database: " . $conn->error;
}

// Select the database
$conn->select_db("test_db");

// Create table
$sql = "CREATE TABLE Users (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    email VARCHAR(50),
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)";

if ($conn->query($sql) === TRUE) {
    echo "Table Users created successfully";
} else {
    echo "Error creating table: " . $conn->error;
}
$conn->close();
?>
```

---

### 5. **CRUD Operations**

#### 1. **Creating (Insert) Data**

To insert data into the database:

```php
<?php
$conn = new mysqli($servername, $username, $password, $dbname);

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO Users (username, email) VALUES (?, ?)");
$stmt->bind_param("ss", $username, $email);

// Set parameters and execute
$username = "JohnDoe";
$email = "john@example.com";
$stmt->execute();

echo "New records created successfully";

$stmt->close();
$conn->close();
?>
```

#### 2. **Reading (Select) Data**

To read data from the database:

```php
<?php
$conn = new mysqli($servername, $username, $password, $dbname);

$sql = "SELECT id, username, email FROM Users";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Output data of each row
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - Name: " . $row["username"]. " - Email: " . $row["email"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>
```

#### 3. **Updating Data**

To update existing records:

```php
<?php
$conn = new mysqli($servername, $username, $password, $dbname);

$sql = "UPDATE Users SET email='john.doe@example.com' WHERE username='JohnDoe'";

if ($conn->query($sql) === TRUE) {
    echo "Record updated successfully";
} else {
    echo "Error updating record: " . $conn->error;
}
$conn->close();
?>
```

#### 4. **Deleting Data**

To delete records from the database:

```php
<?php
$conn = new mysqli($servername, $username, $password, $dbname);

$sql = "DELETE FROM Users WHERE username='JohnDoe'";

if ($conn->query($sql) === TRUE) {
    echo "Record deleted successfully";
} else {
    echo "Error deleting record: " . $conn->error;
}
$conn->close();
?>
```

---

### 6. **Handling Forms with PHP**

To handle user input from forms, use the `$_POST` or `$_GET` superglobals:

```html
<form method="post" action="submit.php">
    Username: <input type="text" name="username">
    Email: <input type="text" name="email">
    <input type="submit">
</form>
```

In `submit.php`:

```php
<?php
$username = $_POST['username'];
$email = $_POST['email'];
// Proceed with inserting the data into MySQL
?>
```

---

### 7. **Using phpMyAdmin**

phpMyAdmin provides a graphical interface to manage MySQL databases. You can create databases, tables, and perform queries without writing SQL commands. Access it at `http://localhost/phpmyadmin/`.

---

### 8. **Common Issues and Troubleshooting**

- **Connection Failed**: Ensure MySQL service is running and the credentials are correct.
- **Database Not Found**: Verify that the database name in the connection matches one created in phpMyAdmin.
- **Syntax Errors**: Double-check your PHP syntax using tools like `php -l filename.php`.

---
