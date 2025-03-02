Below are step-by-step instructions to set up PHP on Ubuntu 24.10 using Apache as your web server:

---

### **1. Update Your Package List**

Open a terminal and update your package list to ensure you have the latest repository information:

```bash
sudo apt update
```

---

### **2. Install Apache Web Server**

Install Apache with the following command:

```bash
sudo apt install apache2
```

Once installed, you can check its status:

```bash
sudo systemctl status apache2
```

If Apache isn’t running, start it with:

```bash
sudo systemctl start apache2
```

---

### **3. Install PHP**

Install PHP along with the Apache PHP module:

```bash
sudo apt install php libapache2-mod-php
```

This command installs PHP and integrates it with Apache, so PHP files can be processed.

---

### **4. Test Your PHP Setup**

1. **Create a Test PHP File:**
    
    Create a new file named `info.php` in Apache’s default document root (`/var/www/html/`):
    
    ```bash
    sudo nano /var/www/html/info.php
    ```
    
2. **Add PHP Code:**
    
    Insert the following code into the file:
    
    ```php
    <?php
    phpinfo();
    ?>
    ```
    
    Save the file (in nano, press `CTRL+O` to save and `CTRL+X` to exit).
    
3. **Restart Apache:**
    
    To ensure Apache picks up the new PHP configuration, restart the server:
    
    ```bash
    sudo systemctl restart apache2
    ```
    
4. **View the Test Page:**
    
    Open your web browser and navigate to:
    
    ```
    http://localhost/info.php
    ```
    
    You should see a page displaying detailed information about your PHP installation.
    

---

### **5. (Optional) Using PHP’s Built-in Server**

If you prefer not to install Apache and just want to test PHP scripts quickly, you can use PHP’s built-in server:

1. **Navigate to Your Project Directory:**
    
    ```bash
    cd /path/to/your/project
    ```
    
2. **Start the Built-in Server:**
    
    ```bash
    php -S localhost:8000
    ```
    
3. **Access Your Project:**
    
    Open your browser and go to `http://localhost:8000/`.
    

---

With these steps, PHP should be set up and ready to run on your Ubuntu 24.10 system. Once you're comfortable with this setup, you can start creating PHP files, learning PHP syntax, and eventually integrating PHP with SQL/MySQL for dynamic web applications.

Let me know if you need any further assistance or additional details!