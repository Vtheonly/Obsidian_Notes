# Installation and Setup

To get started with Laravel, you'll need to have Composer installed on your machine. You can then create a new Laravel project using the following command:

```bash
composer create-project --prefer-dist laravel/laravel blog
```

This will create a new `blog` directory with a fresh Laravel installation.

## Environment Configuration

Laravel's environment configuration is stored in the `.env` file. This file contains all of the configuration options for your application, such as your database credentials, mail driver, and cache driver.

You should never commit your `.env` file to source control. Instead, you should commit the `.env.example` file, which contains a template of the configuration options that your application needs.

## Application Configuration

You can access your application's configuration options using the `config` helper function.

```php
$value = config('app.timezone');
```

You can also set configuration options at runtime using the `config` helper function.

```php
config(['app.timezone' => 'America/Chicago']);
```
