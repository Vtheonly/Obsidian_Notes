# MVC Architecture (Model-View-Controller)

The MVC pattern separates the application's logic into three interconnected components:

*   **Model:** Represents your data and interacts with your database. In Laravel, this is handled by **Eloquent**.
*   **View:** The user interface of your application. In Laravel, this is managed by the **Blade** templating engine.
*   **Controller:** Acts as an intermediary between the Model and the View, handling user requests and returning responses.

This separation of concerns makes your code more organized, easier to maintain, and scalable.

## The Request Lifecycle

1.  **Entry Point:** The request enters your application through the `public/index.php` file.
2.  **HTTP Kernel:** The request is then passed to the HTTP kernel, which is located in `app/Http/Kernel.php`.
3.  **Service Providers:** The kernel boots up the application and registers the service providers.
4.  **Router:** The request is then passed to the router, which matches the request to a specific route.
5.  **Controller:** The router then dispatches the request to the appropriate controller.
6.  **Middleware:** The request passes through any middleware that is assigned to the route.
7.  **Response:** The controller then returns a response, which is sent back to the user.
