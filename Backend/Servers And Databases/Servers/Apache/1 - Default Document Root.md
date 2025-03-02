You're on the right track! Changing the default Document Root and creating other entry points is a fundamental part of configuring Apache to serve websites the way you want.  Let's break down the primary way to do this: **using Virtual Hosts**.

**Virtual Hosts: The Key to Multiple Entry Points and Custom Document Roots**

Virtual Hosts are the *standard and recommended* way to manage different websites or different entry points on a single Apache server.  They allow you to:

* **Host multiple websites on one server:** Each website can have its own domain name (or subdomain) and its own set of configurations, including its own Document Root.
* **Create different entry points for a single website:**  You can set up different URLs or subdomains to point to different directories within your server, effectively creating different "entry points."
* **Customize configurations per website/entry point:**  You can have different settings for each virtual host, such as log files, security settings, SSL certificates, and more.

**How to Change the Document Root and Create Entry Points with Virtual Hosts**

Here's a step-by-step guide, building on the example from the previous response:

**1. Understand Virtual Host Configuration Files**

* **Configuration Files Location:** Virtual host configurations are typically stored in files within the `/etc/apache2/sites-available/` directory.
* **Enabling/Disabling Sites:**  To activate a virtual host, you create a symbolic link from its configuration file in `sites-available` to the `/etc/apache2/sites-enabled/` directory.  Apache only reads configurations from `sites-enabled`.
* **Tools for Managing Sites:** Apache provides command-line tools:
    * `a2ensite <sitename>`:  Enables a site by creating the symbolic link in `sites-enabled`.
    * `a2dissite <sitename>`: Disables a site by removing the symbolic link from `sites-enabled`.

**2. Create a New Virtual Host Configuration File**

Let's say you want to:

* Change the Document Root for your main website (let's call it `mywebsite.com`) to `/var/www/mywebsite`.
* Create another entry point, maybe a subdomain like `blog.mywebsite.com`, with its own Document Root at `/var/www/mywebsite-blog`.

**Steps:**

1. **Create configuration files in `/etc/apache2/sites-available/`:**

   ```bash
   sudo nano /etc/apache2/sites-available/mywebsite.com.conf
   sudo nano /etc/apache2/sites-available/blog.mywebsite.com.conf
   ```

2. **Edit `mywebsite.com.conf` (for your main website):**

   ```apache
   <VirtualHost *:80>
       ServerName mywebsite.com
       ServerAlias www.mywebsite.com  # Optional alias for www subdomain
       DocumentRoot /var/www/mywebsite  # **New Document Root**

       <Directory /var/www/mywebsite>  # Configure directory access
           AllowOverride All
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/mywebsite_error.log
       CustomLog ${APACHE_LOG_DIR}/mywebsite_access.log combined
   </VirtualHost>
   ```

3. **Edit `blog.mywebsite.com.conf` (for the subdomain/new entry point):**

   ```apache
   <VirtualHost *:80>
       ServerName blog.mywebsite.com  # **Different ServerName**
       DocumentRoot /var/www/mywebsite-blog # **Different Document Root**

       <Directory /var/www/mywebsite-blog> # Configure directory access
           AllowOverride All
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/blog_error.log
       CustomLog ${APACHE_LOG_DIR}/blog_access.log combined
   </VirtualHost>
   ```

   **Key Differences:**
   * **`ServerName`:**  Crucially different for each virtual host. This is how Apache knows which configuration to use based on the domain name requested by the browser.
   * **`DocumentRoot`:**  Set to the desired directory for each virtual host.

4. **Create the Document Root Directories:**

   ```bash
   sudo mkdir /var/www/mywebsite
   sudo mkdir /var/www/mywebsite-blog
   ```

5. **Enable the Virtual Hosts:**

   ```bash
   sudo a2ensite mywebsite.com.conf
   sudo a2ensite blog.mywebsite.com.conf
   ```

6. **Disable the Default Site (if you don't want it or if it conflicts):**

   ```bash
   sudo a2dissite 000-default.conf  # Disable the default site
   ```

7. **Restart Apache:**

   ```bash
   sudo systemctl restart apache2
   ```

8. **Update DNS (if using domain names):**

   * For `mywebsite.com` and `www.mywebsite.com`, make sure your DNS records (A records or CNAME for `www`) point to the public IP address of your server.
   * For `blog.mywebsite.com`, create a new DNS record (usually an A record) that also points `blog.mywebsite.com` to the same public IP address.

**Explanation of What Happens:**

* **When a request comes in for `mywebsite.com` or `www.mywebsite.com`:** Apache looks at the `Host` header in the HTTP request. It matches it to the `ServerName` (or `ServerAlias`) in the `mywebsite.com.conf` virtual host. It then serves files from the `/var/www/mywebsite` directory.
* **When a request comes in for `blog.mywebsite.com`:** Apache matches the `Host` header to the `ServerName` in `blog.mywebsite.com.conf`. It serves files from `/var/www/mywebsite-blog`.

**Other Ways to Create "Entry Points" (Less Common for Major Changes)**

While Virtual Hosts are the primary and best method, here are a couple of other approaches, though they are typically less flexible for changing Document Roots and more for specific URL path manipulations:

* **Subdirectories within a Document Root:** As we discussed before, you can simply place website files in subdirectories within a single Document Root.  For example, if your Document Root is `/var/www/html`, you could have:
    * `/var/www/html/website1/`
    * `/var/www/html/website2/`
    You would access them as `http://yourdomain.com/website1/` and `http://yourdomain.com/website2/`. This is simple but doesn't provide separate configurations or truly distinct entry points in the same way as Virtual Hosts.

* **`Alias` Directive (within Virtual Host or main config):**  The `Alias` directive lets you map a URL path to a *different* directory location, potentially outside of the Document Root.  For example, inside your `mywebsite.com.conf` virtual host, you could add:

   ```apache
   Alias /blog /var/www/mywebsite-blog-content
   ```

   Now, when someone accesses `http://mywebsite.com/blog`, Apache will serve files from `/var/www/mywebsite-blog-content`, even though the main Document Root is still `/var/www/mywebsite`.  This is useful for creating specific "sections" of a website that reside in different locations, but it's still within the context of the main virtual host.

* **`Redirect` Directive (within Virtual Host or main config):** The `Redirect` directive is for URL redirection. You can redirect one URL path to another URL. It doesn't really change the Document Root, but it can be used to create different URL entry points that point to other places (even external websites). For example:

   ```apache
   Redirect /old-blog http://blog.example.com
   ```

   Accessing `http://yourdomain.com/old-blog` would redirect the user to `http://blog.example.com`.

**Recommendation:**

For most scenarios where you want to change the Document Root or create distinct entry points for different websites or sections, **Virtual Hosts are the most flexible, organized, and recommended approach.**  They provide clear separation and configuration control for each entry point.

Let me know if you'd like to explore any of these methods in more detail, or if you have a specific setup you're trying to achieve!