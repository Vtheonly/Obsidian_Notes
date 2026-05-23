---
sources:
  - "[[03.1. Object-Relational Mapping Principles]]"
  - "[[03.2. Django Model Fields and Attribute Mappings]]"
  - "[[03.3. Database Schema Field Options]]"
  - "[[03.4. Django Database Configuration Settings]]"
  - "[[03.5. Model Relationships One-to-Many Relationships]]"
  - "[[03.6. Model Relationships Many-to-Many Relationships]]"
  - "[[03.7. Model Relationships One-to-One Relationships]]"
  - "[[03.8. Database Migration Lifecycle Commands]]"
  - "[[03.9. Django ORM CRUD Operations API]]"
---
> [!question] The Object-Relational Impedance Mismatch refers to the disconnect between object-oriented code and relational databases.
>> [!success]- Answer
>> True

> [!question] Instantiating a model object in Python (e.g., `p = Patient(name="Alice")`) immediately writes the record to the database.
>> [!success]- Answer
>> False

> [!question] Django's ORM uses the Active Record Pattern where each model class represents a database table.
>> [!success]- Answer
>> True

> [!question] The `DecimalField` is the correct choice for storing currency and financial values because it uses exact decimal arithmetic.
>> [!success]- Answer
>> True

> [!question] Setting `blank=True` on a field means the database column allows NULL values.
>> [!success]- Answer
>> False

> [!question] The `on_delete=models.CASCADE` option deletes all related child records when a parent record is deleted.
>> [!success]- Answer
>> True

> [!question] In a Many-to-Many relationship, Django automatically creates and manages an intermediate join table.
>> [!success]- Answer
>> True

> [!question] The `OneToOneField` returns a QuerySet when queried in reverse, just like a ForeignKey.
>> [!success]- Answer
>> False

> [!question] The `sqlmigrate` command displays the raw SQL statements that Django will run for a specific migration.
>> [!success]- Answer
>> True

> [!question] The `.get()` method in Django ORM always returns a QuerySet, even if only one record matches.
>> [!success]- Answer
>> False

> [!question] Which of the following best describes the purpose of an Object-Relational Mapper (ORM)?
> a) It replaces the need for a database entirely
> b) It translates object-oriented operations into SQL queries
> c) It converts SQL databases into NoSQL databases
> d) It manages only database migrations
>> [!success]- Answer
>> b) It translates object-oriented operations into SQL queries

> [!question] Which Django field type should be used for storing high-precision financial amounts?
> a) FloatField
> b) IntegerField
> c) DecimalField
> d) CharField
>> [!success]- Answer
>> c) DecimalField

> [!question] What is the difference between `null` and `blank` in Django model fields?
> a) They are synonyms and can be used interchangeably
> b) `null` is database-level; `blank` is application-level form validation
> c) `null` is for strings; `blank` is for numbers
> d) `null` is used only for primary keys
>> [!success]- Answer
>> b) `null` is database-level; `blank` is application-level form validation

> [!question] Which database driver is required to connect Django to PostgreSQL?
> a) mysqlclient
> b) psycopg2-binary
> c) sqlite3
> d) pymongo
>> [!success]- Answer
>> b) psycopg2-binary

> [!question] In a One-to-Many relationship, where is the ForeignKey field placed?
> a) On the "one" side of the relationship
> b) On the "many" side of the relationship
> c) On both sides of the relationship
> d) In a separate intermediate table
>> [!success]- Answer
>> b) On the "many" side of the relationship

> [!question] What does the `through` parameter do in a ManyToManyField?
> a) It specifies a custom intermediate model for storing relationship metadata
> b) It creates a direct connection between two tables
> c) It adds a foreign key column to both tables
> d) It enables caching of the relationship data
>> [!success]- Answer
>> a) It specifies a custom intermediate model for storing relationship metadata

> [!question] What exception does a reverse `OneToOneField` lookup raise if no related object exists?
> a) ObjectDoesNotExist
> b) DoesNotExist
> c) RelatedObjectNotFound
> d) NoReverseMatch
>> [!success]- Answer
>> b) DoesNotExist

> [!question] Which migration command lists all migrations and shows which ones have been applied?
> a) python manage.py makemigrations
> b) python manage.py migrate
> c) python manage.py showmigrations
> d) python manage.py sqlmigrate
>> [!success]- Answer
>> c) python manage.py showmigrations

> [!question] What happens when you call `Patient.objects.create(nom="Alice")`?
> a) It only instantiates the object in memory
> b) It instantiates and saves the record in one step
> c) It only validates the data without saving
> d) It creates the database table
>> [!success]- Answer
>> b) It instantiates and saves the record in one step

> [!question] Which method should you use to check if a record exists without loading it into memory?
> a) .get()
> b) .all()
> c) .exists()
> d) .count()
>> [!success]- Answer
>> c) .exists()

> [!question] Match the OOP concept with its corresponding database concept.
>> [!example] Group A
>> a) Model Class
>> b) Object Instance
>> c) Class Attribute
>
>> [!example] Group B
>> n) Database Row
>> o) Database Table
>> p) Database Column
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django field type with its PostgreSQL data type.
>> [!example] Group A
>> a) CharField
>> b) BooleanField
>> c) DateTimeField
>
>> [!example] Group B
>> n) TIMESTAMP WITH TZ
>> o) VARCHAR
>> p) BOOLEAN
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the field option with its correct description.
>> [!example] Group A
>> a) default
>> b) unique
>> c) choices
>
>> [!example] Group B
>> n) Restricts inputs to a pre-defined set of key-value pairs
>> o) Defines a fallback value if none is provided
>> p) Enforces a unique constraint at the database level
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the `on_delete` option with its behavior.
>> [!example] Group A
>> a) CASCADE
>> b) PROTECT
>> c) SET_NULL
>
>> [!example] Group B
>> n) Prevents deletion by raising ProtectedError
>> o) Deletes all related child objects
>> p) Sets the foreign key to NULL
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the relationship type with its Django field.
>> [!example] Group A
>> a) One-to-Many
>> b) Many-to-Many
>> c) One-to-One
>
>> [!example] Group B
>> n) ForeignKey
>> o) OneToOneField
>> p) ManyToManyField
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the migration command with its action.
>> [!example] Group A
>> a) makemigrations
>> b) migrate
>> c) sqlmigrate
>
>> [!example] Group B
>> n) Displays raw SQL statements
>> o) Executes pending migrations against the database
>> p) Generates new migration files from model changes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the CRUD operation with its Django ORM method.
>> [!example] Group A
>> a) Create
>> b) Read (single record)
>> c) Delete (batch)
>
>> [!example] Group B
>> n) .filter().delete()
>> o) .create() or .save()
>> p) .get()
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the ORM problem with its solution.
>> [!example] Group A
>> a) N+1 Query Problem
>> b) SQL Injection
>> c) Lazy Evaluation
>
>> [!example] Group B
>> n) Parameterized queries by Django ORM
>> o) select_related and prefetch_related
>> p) QuerySet only hits DB when evaluated
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the `auto_now` option with its behavior.
>> [!example] Group A
>> a) auto_now
>> b) auto_now_add
>> c) editable=False
>
>> [!example] Group B
>> n) Set automatically when both options are used
>> o) Updates to current time on every save
>> p) Sets to current time only on first creation
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the database engine with its Django backend string.
>> [!example] Group A
>> a) SQLite
>> b) PostgreSQL
>> c) MySQL
>
>> [!example] Group B
>> n) django.db.backends.postgresql
>> o) django.db.backends.mysql
>> p) django.db.backends.sqlite3
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)