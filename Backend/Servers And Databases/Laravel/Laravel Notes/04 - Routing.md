# Routing

In Laravel, routing is the process of defining how your application responds to a client request for a specific URI. Routes are typically defined in the `routes/web.php` and `routes/api.php` files.

**Example:**

```php
use App\Http\Controllers\UserController;

// routes/web.php
Route::get('/users', [UserController::class, 'index']);
```

This route tells Laravel that when a user visits `/users`, it should execute the `index` method in the `UserController`.

## Route Parameters

You can also define route parameters to capture segments of the URI.

```php
Route::get('/users/{id}', function ($id) {
    return 'User '.$id;
});
```

## Route Verbs

Laravel supports all the standard HTTP verbs:

*   `Route::get($uri, $callback);`
*   `Route::post($uri, $callback);`
*   `Route::put($uri, $callback);`
*   `Route::patch($uri, $callback);`
*   `Route::delete($uri, $callback);`
*   `Route::options($uri, $callback);`
