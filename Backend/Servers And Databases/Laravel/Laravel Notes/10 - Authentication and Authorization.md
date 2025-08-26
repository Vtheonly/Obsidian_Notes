# Authentication and Authorization

Laravel makes implementing authentication and authorization a breeze. You can scaffold a complete authentication system with a single command:

```bash
php artisan make:auth
```

This will create all the necessary routes, views, and controllers for user registration, login, and password reset.

## Protecting Routes

You can protect your routes from unauthenticated users using the `auth` middleware.

```php
Route::get('/profile', function () {
    // Only authenticated users may enter...
})->middleware('auth');
```

## Gates and Policies

Gates and Policies are used to authorize user actions against a given resource.

### Gates

Gates are simple, closure-based authorization callbacks.

```php
// app/Providers/AuthServiceProvider.php

public function boot()
{
    $this->registerPolicies();

    Gate::define('update-post', function ($user, $post) {
        return $user->id === $post->user_id;
    });
}
```

### Policies

Policies are classes that organize authorization logic around a particular model or resource.

```php
// app/Policies/PostPolicy.php

public function update(User $user, Post $post)
{
    return $user->id === $post->user_id;
}
```
