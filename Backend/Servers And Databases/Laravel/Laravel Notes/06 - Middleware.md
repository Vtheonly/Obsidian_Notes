# Middleware

Middleware provides a convenient mechanism for filtering HTTP requests entering your application. For example, Laravel includes a middleware that verifies the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen.

**Forgotten Concept Refresher: Middleware**

Think of middleware as layers of an onion. Each request to your application passes through these layers, and each layer can perform some action on the request before it reaches the controller.

## Creating Middleware

You can create a new middleware using the following Artisan command:

```bash
php artisan make:middleware CheckAge
```

This will create a new `CheckAge` middleware in the `app/Http/Middleware` directory.

## Registering Middleware

You can register a middleware in the `$routeMiddleware` property of your `app/Http/Kernel.php` file.

```php
protected $routeMiddleware = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
    'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
    'can' => \Illuminate\Auth\Middleware\Authorize::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    'age' => \App\Http\Middleware\CheckAge::class,
];
```
