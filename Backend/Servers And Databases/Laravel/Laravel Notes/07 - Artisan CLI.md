# Artisan CLI

Artisan is the command-line interface included with Laravel. It provides a number of helpful commands that can assist you while you build your application.

**Common Artisan Commands:**

*   `php artisan make:model`
*   `php artisan make:controller`
*   `php artisan make:migration`
*   `php artisan serve`
*   `php artisan test`
*   `php artisan migrate`
*   `php artisan db:seed`
*   `php artisan route:list`
*   `php artisan view:clear`

## Creating Custom Commands

You can create your own custom commands using the following Artisan command:

```bash
php artisan make:command SendEmails
```

This will create a new `SendEmails` command in the `app/Console/Commands` directory. You can then define the logic for your command in the `handle` method of the command class.
