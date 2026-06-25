
##  What is an ORM?

>  **Definition**  
**ORM** stands for **Object-Relational Mapping**.  
It’s a programming technique used to interact with a **relational database** (like SQLite, MySQL, or PostgreSQL) using **Python classes and objects instead of raw SQL**.

In simple terms, an ORM lets you:
- Represent tables as Python classes
- Represent rows as Python objects
- Perform SQL operations using method calls and attributes

---

##  Why Use an ORM?

>  Without ORM (raw SQL):
```python
import sqlite3
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE age > ?", (25,))
rows = cursor.fetchall()
````

>  With ORM (SQLAlchemy):

```python
users = db.session.query(User).filter(User.age > 25).all()
```

>  **Benefits**:

- Avoids repetitive SQL syntax
    
- Automatically converts data types (e.g., `DATE` to `datetime`)
    
- Enforces structure via Python classes
    
- Easier to update/change database schema
    
- Prevents SQL injection when done right
    

>  **Drawbacks**:

- Slightly slower than raw SQL for heavy queries
    
- Learning curve for complex joins or optimizations
    
- Abstracts away the SQL — can be dangerous if misunderstood
    

---

##  Common ORMs Used with Flask

|ORM Tool|Description|
|---|---|
|**SQLAlchemy**|Full-featured ORM, very popular in Flask|
|Flask-SQLAlchemy|Flask extension that integrates SQLAlchemy easily|
|Peewee|Lightweight ORM for smaller projects|
|PonyORM|Declarative, uses Python syntax for queries|
|Django ORM|Built-in ORM (only for Django, not Flask)|

---

##  SQLAlchemy Model Example

Here’s how you'd define a table called `User` with Flask-SQLAlchemy:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
```

>  This defines a `User` table with:

- `id`: Primary key (auto-increment)
    
- `username`: Required and unique
    
- `email`: Required and unique
    

###  Create & Query

```python
new_user = User(username="marshal", email="marshal@example.com")
db.session.add(new_user)
db.session.commit()

users = User.query.filter_by(username="marshal").all()
```

---

##  Relationships in ORM

ORMs support **relationships** like foreign keys and joins:

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='posts')
```

Now `Post.user` gives you the author object, and `User.posts` gives you all posts by that user.

---

##  Summary

 ORM = A tool that maps Python classes to database tables.  
 Makes code cleaner, more maintainable, and more Pythonic.  
 SQLAlchemy is the go-to ORM for Flask.

---

##  Tips

>  Use ORM for:

- Apps that grow over time
    
- Complex queries that can be abstracted
    
- Cleaner code structure
    

>  Learn SQL too!

- ORM doesn't eliminate the need for understanding SQL.
    
- Knowing JOINs, indexing, transactions, etc., is still vital.
    

##  Does the class (e.g. `User`) need to exist in the database?

###  No — the class in your code **defines** the table.

You don't _write the table manually_ in the database. The ORM **creates it for you** based on your Python class.

>  You define the table **structure** in Python.  
>  SQLAlchemy then creates or updates the corresponding SQL table using this class.  
>  The class doesn’t have to exist in the database before — the ORM makes it real in the DB.

---

##  Example

###  Python Model:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
```

This defines what the **`users`** table _should_ look like in the DB.

Now to make it real:

###  You run:

```python
db.create_all()
```

This tells SQLAlchemy:

> “Look at all the models I defined, and create their tables in the database if they don’t exist.”

---

##  What If a Table Already Exists?

- If you already have a table in the database with the same name, SQLAlchemy **will not overwrite or modify it** automatically — `create_all()` only creates tables if they don’t exist.
    
- The class **must match** the table's structure _if_ the table already exists, or things will break (e.g., querying rows will fail or give incorrect data).
    

>  SQLAlchemy doesn’t auto-sync changes like column renames or type changes. That’s why we use tools like **Alembic** for migrations.

---

##  Summary

|Question|Answer|
|---|---|
|Does the table need to exist before?| No — the class _creates_ the table.|
|Do the class and DB table need to match?| Yes — otherwise queries break.|
|What if the table exists and doesn't match the model?| Errors or unexpected behavior.|
|Does `create_all()` update existing tables?| No — it only creates new ones.|

---

##  Tip: Use Migrations for Real Projects

Once your app evolves (and the schema changes), use:

```bash
flask db init
flask db migrate -m "add age field to User"
flask db upgrade
```

This handles updates safely.

---

Let me know if you want a walkthrough on setting up Flask + SQLAlchemy + Alembic in a clean way — or if you'd like a diagram of how models translate to tables.