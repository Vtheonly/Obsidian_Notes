---
sources:
  - "[[Final/Chapter 1]]"
---
> [!question] Virtual environments in Python prevent dependency version conflicts between projects.
>> [!success]- Answer
>> True

> [!question] The command python manage.py startproject creates a new Django project folder structure.
>> [!success]- Answer
>> False

> [!question] The null=True argument in a Django model field allows the field to be left blank in input forms.
>> [!success]- Answer
>> False

> [!question] A ForeignKey field in Django creates a One-to-Many relationship between models.
>> [!success]- Answer
>> True

> [!question] The makemigrations command directly updates the database schema in Django.
>> [!success]- Answer
>> False

> [!question] The ORM method Patient.objects.get(id=1) returns a single object instance.
>> [!success]- Answer
>> True

> [!question] The filter() method in Django ORM returns a collection called a QuerySet.
>> [!success]- Answer
>> True

> [!question] The on_delete=models.CASCADE option in a ForeignKey will delete child records when the parent is deleted.
>> [!success]- Answer
>> True

> [!question] A ManyToManyField in Django generates a new database column on the parent table.
>> [!success]- Answer
>> False

> [!question] The Django template engine uses {{ var }} syntax to display variables.
>> [!success]- Answer
>> True

> [!question] Which command is used to activate a Python virtual environment on Linux or macOS?
> a) venv\Scripts\Activate.ps1
> b) source venv/bin/activate
> c) python3 activate venv
> d) venv activate
>> [!success]- Answer
>> b) source venv/bin/activate

> [!question] What does the Django field argument auto_now_add=True do?
> a) Updates the field to the current time on every save
> b) Sets the field to the current timestamp only when the record is created
> c) Adds the field to the admin panel automatically
> d) Automatically generates a default value based on other fields
>> [!success]- Answer
>> b) Sets the field to the current timestamp only when the record is created

> [!question] Which database engine configuration in Django uses SQLite by default?
> a) django.db.backends.postgresql
> b) django.db.backends.mysql
> c) django.db.backends.sqlite3
> d) django.db.backends.oracle
>> [!success]- Answer
>> c) django.db.backends.sqlite3

> [!question] What does the on_delete=models.PROTECT option do in a Django ForeignKey?
> a) Deletes all child records when the parent is deleted
> b) Blocks deletion of the parent if child records exist
> c) Sets the foreign key to NULL when the parent is deleted
> d) Automatically creates a backup of the parent before deletion
>> [!success]- Answer
>> b) Blocks deletion of the parent if child records exist

> [!question] What is the correct method to save an updated record back to the database in Django ORM?
> a) model.commit()
> b) model.update()
> c) model.save()
> d) model.flush()
>> [!success]- Answer
>> c) model.save()

> [!question] Which file contains the DATABASES dictionary for database configuration in Django?
> a) models.py
> b) settings.py
> c) database.py
> d) config.py
>> [!success]- Answer
>> b) settings.py

> [!question] What does the Django ORM method Patient.objects.create() do?
> a) Creates a database table
> b) Creates and saves a new model instance in a single step
> c) Generates a migration file
> d) Creates a database index
>> [!success]- Answer
>> b) Creates and saves a new model instance in a single step

> [!question] Which command is used to install Django framework?
> a) django install
> b) pip install django
> c) python django setup
> d) npm install django
>> [!success]- Answer
>> b) pip install django

> [!question] What does the blank=True argument in a Django model field allow?
> a) Allows NULL values in the database column
> b) Allows the field to be left empty in input forms
> c) Creates a blank default value
> d) Removes the field from database migration
>> [!success]- Answer
>> b) Allows the field to be left empty in input forms

> [!question] In a Django view, what does the render() function return?
> a) A JSON response
> b) An HTML template rendered with context data
> c) A redirect response
> d) A plain text response
>> [!success]- Answer
>> b) An HTML template rendered with context data

> [!question] Match the virtual environment command with its action.
>> [!example] Group A
>> a) python3 -m venv venv
>> b) source venv/bin/activate
>> c) pip freeze > requirements.txt
>
>> [!example] Group B
>> n) Saves current packages to file
>> o) Creates the environment directory
>> p) Activates the virtual environment
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Django field argument with its purpose.
>> [!example] Group A
>> a) null=True
>> b) unique=True
>> c) max_length=n
>
>> [!example] Group B
>> n) Restricts string length in CharField
>> o) Allows NULL values in the database
>> p) Restricts values to unique entries across the column
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the migration lifecycle step with its command.
>> [!example] Group A
>> a) Create migration files
>> b) Apply migrations to database
>> c) Edit model class
>
>> [!example] Group B
>> n) python manage.py makemigrations
>> o) python manage.py migrate
>> p) Modify models.py file
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the on_delete behavior with its description.
>> [!example] Group A
>> a) models.CASCADE
>> b) models.PROTECT
>> c) models.SET_NULL
>
>> [!example] Group B
>> n) Retains child records with NULL foreign key
>> o) Blocks deletion of parent while children exist
>> p) Deletes all associated child records automatically
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the relationship type with its Django field.
>> [!example] Group A
>> a) One-to-Many
>> b) Many-to-Many
>> c) One-to-One
>
>> [!example] Group B
>> n) OneToOneField
>> o) ForeignKey
>> p) ManyToManyField
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the CRUD operation with its Django ORM method.
>> [!example] Group A
>> a) Create
>> b) Read
>> c) Update
>
>> [!example] Group B
>> n) Model.objects.get()
>> o) Model.objects.create()
>> p) obj.save() after modifying attributes
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django file with its code element.
>> [!example] Group A
>> a) models.py
>> b) urls.py
>> c) views.py
>
>> [!example] Group B
>> n) path('', views.liste_articles, name='home')
>> o) return render(request, 'template.html', context)
>> p) class Patient(models.Model)
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the model field type with its database column type.
>> [!example] Group A
>> a) CharField
>> b) IntegerField
>> c) BooleanField
>
>> [!example] Group B
>> n) Database integer column
>> o) Database boolean column
>> p) Database VARCHAR column
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Django template tag with its purpose.
>> [!example] Group A
>> a) {{ var }}
>> b) {% for item in items %}
>> c) {% block name %}
>
>> [!example] Group B
>> n) Defines a placeholder in parent template
>> o) Displays a variable value
>> p) Loops through a collection
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the SGBD option with its Django engine string.
>> [!example] Group A
>> a) PostgreSQL
>> b) MySQL
>> c) SQLite
>
>> [!example] Group B
>> n) django.db.backends.mysql
>> o) django.db.backends.sqlite3
>> p) django.db.backends.postgresql
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)