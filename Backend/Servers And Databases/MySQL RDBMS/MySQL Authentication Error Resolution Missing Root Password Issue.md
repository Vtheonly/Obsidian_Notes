
## **Context and Problem**

While attempting to connect to the MySQL database server as `root` on `localhost`, the following error was encountered:

```plaintext
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

### **Possible Cause**

The issue likely occurred because no password was initially set for the MySQL `root` user, leading to difficulties during authentication. Additionally, the MySQL server enforces a password validation policy that complicates setting a simple password if the policy requirements aren't met.

---

## **Steps Taken to Investigate**

1. Checked the MySQL service status to ensure it was running:
    
    ```bash
    sudo systemctl status mysql
    ```
    
    Output confirmed the service was active and operational.
    
2. Verified the MySQL password policy settings:
    
    ```sql
    SHOW VARIABLES LIKE 'validate_password%';
    ```
    
    Results showed:
    
    - **Policy**: MEDIUM
    - **Minimum Length**: 8 characters
    - **Mixed Case**: 1 (must include upper and lowercase letters)
    - **Special Characters**: 1 (must include at least one special character)
    - **Numbers**: 1 (must include at least one number)
3. Attempted to set a new password using:
    
    ```sql
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '74532180';
    ```
    
    This failed because the password did not meet the policy requirements.
    

---

## **Resolution**

The root cause was addressed by identifying two potential solutions:

### **Option 1: Set a Password That Meets Policy Requirements**

Set a password that satisfies the `MEDIUM` policy. For example:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Str0ngP@ss!';
```

### **Option 2: Relax Password Policy**

Adjusted the password validation rules to allow simpler passwords:

1. Reduced password policy to `LOW`:
    
    ```sql
    SET GLOBAL validate_password.policy = LOW;
    SET GLOBAL validate_password.length = 4;
    SET GLOBAL validate_password.mixed_case_count = 0;
    SET GLOBAL validate_password.special_char_count = 0;
    ```
    
2. Set a simpler password:
    
    ```sql
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '74532180';
    ```
    
3. Made these changes persistent by updating the MySQL configuration file:
    
    ```bash
    sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
    ```
    
    Added:
    
    ```ini
    validate_password.policy=LOW
    validate_password.length=4
    validate_password.mixed_case_count=0
    validate_password.special_char_count=0
    ```
    
    Restarted MySQL to apply changes:
    
    ```bash
    sudo systemctl restart mysql
    ```
    

### **Option 3: Temporarily Disable Password Validation**

If necessary, the password validation plugin can be disabled temporarily:

```sql
UNINSTALL PLUGIN validate_password;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '74532180';
INSTALL PLUGIN validate_password SONAME 'validate_password.so';
```

---

## **Reflection**

This error highlights the importance of ensuring that:

1. A password is set during the MySQL installation process to avoid configuration issues later.
2. The password validation policy matches the user's requirements for simplicity or security.

---

This note can be stored in Obsidian for future reference, especially if encountering similar issues in other MySQL installations. Let me know if you need further adjustments!