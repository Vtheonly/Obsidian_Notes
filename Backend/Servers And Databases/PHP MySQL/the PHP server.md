Excellent question. It gets to the very core of how PHP works. The short answer to your second question is **both**, and understanding this distinction is the key to understanding the different environments.

Let's break it down, starting with the two fundamental execution models of PHP.

### The Two Core Execution Models of PHP

Everything about how PHP runs falls into one of these two categories.

#### 1. The "Share-Nothing" Request/Response Model (The Classic Way)

This is the traditional and most common way PHP is used for websites.

*   **How it works:** A separate, long-running program (a web server like Apache or Nginx) is constantly listening for HTTP requests on port 80/443.
*   When a request for a `.php` file comes in (e.g., `your-site.com/index.php`), the web server recognizes it.
*   The web server starts up a **brand new PHP interpreter process**.
*   This PHP process executes your script (`index.php`) from top to bottom.
*   The script generates output (usually HTML).
*   The output is sent back to the web server, which sends it to the user's browser.
*   **Crucially, the PHP process then shuts down completely.** It forgets everything—all variables, all objects, all state.

**Analogy:** Imagine ordering a pizza. The pizza shop (the web server) is always open and listening for phone calls. When you call (the request), they hire a temporary chef (the PHP process). The chef makes your pizza (executes the script), gives it to the delivery driver (sends the response), and then immediately goes home (the process exits). For the next order, they hire a completely new chef.

> **Key takeaway:** In this model, **PHP does not keep running and listening.** The web server does the listening. PHP is just a short-lived worker that is invoked, does a job, and exits.

#### 2. The Long-Running / Application Server Model (The Modern Way)

This model is more like how applications in Node.js, Python, or Java traditionally work. It's less common for simple PHP sites but is used for high-performance applications, APIs, and asynchronous tasks.

*   **How it works:** A single PHP script is started from the command line.
*   This script uses a special library (like **Swoole**, **RoadRunner**, or **ReactPHP**) to start its own server and listen for requests on a specific port.
*   **This PHP process does not exit.** It stays running in memory, waiting for new connections.
*   When a request comes in, the application's internal code handles it without having to re-initialize the entire framework on every request.

**Analogy:** Imagine a fine-dining restaurant. The head chef (the long-running PHP process) is *always* in the kitchen. When an order comes in from a waiter (the request), the chef prepares the dish and sends it out. The chef remains in the kitchen, ready for the next order, retaining all their knowledge and having all their tools ready.

> **Key takeaway:** In this model, a PHP script **can be written to stay running and listen for requests directly**, but it requires special tools/libraries to do so.

---

### How PHP Gets Executed in Different Environments

Now let's apply these two models to your specific examples.

#### On Linux (e.g., a standard server)

This is the classic production environment for PHP. You'll typically see two setups:

*   **LAMP Stack (Linux, Apache, MySQL, PHP):** #Apache is the web server. It uses a module, historically `mod_php` (less common now) or **PHP-FPM** (FastCGI Process Manager), to execute PHP scripts. PHP-FPM is a highly efficient manager that maintains a "pool" of ready-to-go PHP worker processes. When a request comes in, Apache hands it to an available worker from the pool. This avoids the startup cost of creating a new process every time. This is an optimized version of the **Request/Response Model**.
*   **LEMP Stack (Linux, Nginx, MySQL, PHP):** Nginx is a very high-performance web server. Unlike Apache, it cannot execute PHP by itself. It *must* pass the request to an external process. This is almost always **PHP-FPM**. The flow is: Request -> Nginx -> PHP-FPM -> Nginx -> User. This is the gold standard for the **Request/Response Model** in production.

#### With XAMPP (on Windows, Linux, or macOS)

*   **What it is:** XAMPP is not a different way of executing PHP. It's a **pre-configured software bundle** that installs Apache, MariaDB (MySQL), and PHP for you and makes them work together.
*   **How it executes:** When you start Apache from the XAMPP control panel, you are starting a web server. It's configured to use the **Request/Response Model**. When you visit `http://localhost/dashboard/` in your browser, you are sending a request to the Apache server running on your machine, which then executes the PHP script.

#### On Windows (natively)

If you're not using a bundle like XAMPP, you have a few options:

*   **IIS (Internet Information Services):** This is Windows' built-in web server. You configure it with the **FastCGI** module to talk to your PHP installation. This works just like the Nginx/LEMP stack. IIS is the listener, and it passes PHP requests to the PHP-FPM process manager. This is the **Request/Response Model**.
*   **Manual Apache/Nginx Install:** You can install Apache or Nginx directly on Windows and configure them to work with PHP, just like on Linux. This would also use the **Request/Response Model**.

#### In Docker

*   **What it is:** Docker is a containerization platform. It packages an application and its entire environment (OS, libraries, configurations) into a portable "container."
*   **How it executes:** A typical modern PHP Docker setup uses multiple containers linked together (often with `docker-compose`).
    1.  An `nginx` container to act as the web server.
    2.  A `php` container that runs the **PHP-FPM** service.
    3.  A `mysql` container for the database.
*   The execution flow is identical to a LEMP stack: The request hits the Nginx container, which forwards the PHP request to the PHP-FPM container. The PHP-FPM container executes the script and returns the result. This is a containerized version of the **Request/Response Model**.

#### On localhost or directly on its own

This is where you see both execution models clearly.

*   **As a local server (localhost):** "localhost" is just a name for your own computer (`127.0.0.1`). Accessing a PHP site on localhost means you are running a web server *on your machine*. This could be XAMPP, Docker, or the simplest one:
*   **PHP's Built-in Web Server:** PHP comes with a simple, single-process development server. You can run it from your project's directory:
    ```bash
    php -S localhost:8000
    ```
    This command starts a PHP process that **listens for requests** on port 8000. It's a very basic implementation of the **Long-Running Model**, but it still re-initializes for each request and is **not for production use**. It's perfect for quick local development without setting up Apache/Nginx.

*   **Directly on its own (CLI - Command Line Interface):** This is the purest form of PHP execution. It has nothing to do with web servers or HTTP requests.
    ```bash
    php my_script.php
    ```
    This command tells the PHP interpreter to execute `my_script.php` once, print any output to the console, and then **immediately exit**. This is used for maintenance tasks, cron jobs, command-line tools (like Composer), and data processing. It is the raw "execute and exit" behavior.

### Summary Table

| Environment / Method                 | Primary Execution Model        | Who is Listening for Requests?     | Does PHP Keep Running?                                                        |
| ------------------------------------ | ------------------------------ | ---------------------------------- | ----------------------------------------------------------------------------- |
| **Linux Server (LEMP/LAMP)**         | Request/Response (via PHP-FPM) | Nginx or Apache                    | **No.** The web server and PHP-FPM service do, but each script process exits. |
| **XAMPP**                            | Request/Response               | The bundled Apache server          | **No.** The Apache server does, but each script process exits.                |
| **Windows with IIS**                 | Request/Response (via FastCGI) | The IIS web server                 | **No.** The IIS service does, but each script process exits.                  |
| **Docker (common setup)**            | Request/Response (via PHP-FPM) | The `nginx` container              | **No.** The Nginx & PHP-FPM containers do, but each script process exits.     |
| **PHP Built-in Server (`php -S`)**   | Long-Running (for development) | The PHP process itself             | **Yes,** until you stop it (Ctrl+C).                                          |
| **PHP CLI (`php script.php`)**       | Execute-and-Exit               | No one (it's not a server)         | **No,** it runs once and immediately exits.                                   |
| **Advanced PHP (Swoole/RoadRunner)** | Long-Running (for production)  | The PHP application process itself | **Yes,** it's designed to run continuously as an application server.          |