# Blade Templating Engine

Blade is Laravel's powerful templating engine. It allows you to use plain PHP code in your views while providing helpful shortcuts for common tasks like displaying data, conditional statements, and loops.

**Example:**

```blade
<!-- resources/views/users.blade.php -->

@extends('layouts.app')

@section('content')
    <h1>Users</h1>

    @if (count($users) > 0)
        <ul>
            @foreach ($users as $user)
                <li>{{ $user->name }}</li>
            @endforeach
        </ul>
    @else
        <p>No users found.</p>
    @endif
@endsection
```

## Layouts

Blade also makes it easy to create reusable layouts for your application.

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

## Directives

Blade provides a number of helpful directives for common tasks:

*   `@if`, `@elseif`, `@else`, `@endif`
*   `@unless`, `@endunless`
*   `@isset`, `@endisset`
*   `@empty`, `@endempty`
*   `@auth`, `@endauth`
*   `@guest`, `@endguest`
