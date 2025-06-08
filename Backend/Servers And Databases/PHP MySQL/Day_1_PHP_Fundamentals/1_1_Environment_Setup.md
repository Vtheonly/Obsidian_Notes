# PHP Environment Setup - Comprehensive Guide

## Detailed Installation Instructions

### Windows Installation
1. Download PHP from [php.net/downloads](https://www.php.net/downloads)
   - Choose Thread Safe version for Apache
   - Choose Non-Thread Safe for Nginx/FastCGI
2. Add PHP to PATH:
   - Edit System Environment Variables
   - Add path to PHP directory (e.g., C:\php)
3. Configure php.ini:
   - Rename php.ini-development to php.ini
   - Enable extensions: 
     ```ini
     extension=mysqli
     extension=openssl
     ```

### macOS Installation
```bash
# Using Homebrew
brew install php

# Common issues:
# If you get permission errors:
sudo chown -R $(whoami) /usr/local/*
```

### Linux Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install php php-cli php-fpm php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath

# Verify installed modules:
php -m
```

## Web Server Configuration

### Apache Setup
```apache
# In httpd.conf
LoadModule php_module "c:/php/php8apache2_4.dll"
AddHandler application/x-httpd-php .php
PHPIniDir "C:/php"
```

### Nginx Setup
```nginx
location ~ \.php$ {
    fastcgi_pass   127.0.0.1:9000;
    fastcgi_index  index.php;
    include        fastcgi_params;
    fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

## Troubleshooting
1. PHP not working in browser:
   - Check php.ini `display_errors = On`
   - Restart web server
2. Extensions not loading:
   - Verify extension_dir path in php.ini
   - Check file permissions

## Development Tools
1. Xdebug setup:
   ```ini
   zend_extension=xdebug.so
   xdebug.mode=debug
   xdebug.start_with_request=yes
   ```
2. Composer installation:
   ```bash
   php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
   php composer-setup.php
   php -r "unlink('composer-setup.php');"