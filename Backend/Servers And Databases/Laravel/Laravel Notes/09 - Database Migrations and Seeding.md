# Database Migrations and Seeding

Migrations are like version control for your database. They allow you to easily modify and share your application's database schema.

**Example:**

```php
// database/migrations/YYYY_MM_DD_HHMMSS_create_users_table.php

public function up()
{
    Schema::create('users', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->string('email')->unique();
        $table->timestamp('email_verified_at')->nullable();
        $table->string('password');
        $table->rememberToken();
        $table->timestamps();
    });
}
```

You can run your migrations using the following Artisan command:

```bash
php artisan migrate
```

**Seeding** is the process of populating your database with test data. This is useful for development and testing purposes.

## Schema Builder

The `Schema` facade provides a number of helpful methods for creating and modifying database tables.

*   `$table->string('name');`
*   `$table->integer('votes');`
*   `$table->text('description');`
*   `$table->timestamps();`

## Model Factories

Model factories allow you to easily generate fake data for your models.

```php
// database/factories/UserFactory.php

public function definition()
{
    return [
        'name' => $this->faker->name,
        'email' => $this->faker->unique()->safeEmail,
        'email_verified_at' => now(),
        'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
        'remember_token' => Str::random(10),
    ];
}
```
