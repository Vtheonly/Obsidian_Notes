# Eloquent ORM (Object-Relational Mapping)

Eloquent is Laravel's built-in ORM. It provides a beautiful, simple ActiveRecord implementation for working with your database. Each database table has a corresponding "Model" which is used to interact with that table.

**Forgotten Concept Refresher: ORM**

An ORM is a technique that lets you query and manipulate data from a database using an object-oriented paradigm. Instead of writing raw SQL queries, you interact with objects that map to your database tables.

**Example:**

Instead of writing this SQL query:

```sql
SELECT * FROM users WHERE email = 'test@example.com';
```

You can use Eloquent like this:

```php
$user = App\Models\User::where('email', 'test@example.com')->first();
```

## Relationships

Eloquent also makes it easy to define relationships between your models.

### One-to-One

```php
// app/Models/User.php
public function phone()
{
    return $this->hasOne(Phone::class);
}
```

### One-to-Many

```php
// app/Models/Post.php
public function comments()
{
    return $this->hasMany(Comment::class);
}
```

### Many-to-Many

```php
// app/Models/User.php
public function roles()
{
    return $this->belongsToMany(Role::class);
}
```
