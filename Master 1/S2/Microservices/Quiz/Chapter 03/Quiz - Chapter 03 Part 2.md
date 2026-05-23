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
> [!question] Django's ORM parameterizes queries automatically, neutralizing the risk of SQL Injection attacks.
>> [!success]- Answer
>> True

> [!question] The `FloatField` is safer than `DecimalField` for financial calculations because it is faster.
>> [!success]- Answer
>> False

> [!question] Setting `null=False, blank=True` on a CharField saves empty submissions as empty strings rather than NULL.
>> [!success]- Answer
>> True

> [!question] When using `auto_now_add` on a DateTimeField, it updates the timestamp every time the model is saved.
>> [!success]- Answer
>> False

> [!question] The `related_name` parameter in a ForeignKey overrides the default reverse relation name of `modelname_set`.
>> [!success]- Answer
>> True

> [!question] When using an explicit `through` model with ManyToManyField, you can still use the `.add()` method directly.
>> [!success]- Answer
>> False

> [!question] A `OneToOneField` is conceptually a ForeignKey with a unique constraint enforced on the foreign key column.
>> [!success]- Answer
>> True

> [!question] Django tracks which migrations have been applied using a table named `django_migrations` in the database.
>> [!success]- Answer
>> True

> [!question] The `.save()` method on a model instance triggers an SQL UPDATE statement only for existing records.
>> [!success]- Answer
>> True

> [!question] The `.get()` method in Django ORM can return multiple records without raising an error.
>> [!success]- Answer
>> False

> [!question] What is the N+1 Query Problem in Django ORM?
> a) A problem where you get N+1 results instead of N results
> b) A problem where retrieving parent items and their children causes one plus N additional queries
> c) A problem with database connection limits
> d) A problem with migration version numbering
>> [!success]- Answer
>> b) A problem where retrieving parent items and their children causes one plus N additional queries

> [!question] Which Django field type automatically validates email syntax when saved?
> a) CharField
> b) TextField
> c) EmailField
> d) URLField
>> [!success]- Answer
>> c) EmailField

> [!question] What happens when you omit `max_digits` on a DecimalField?
> a) It defaults to 10
> b) It raises a configuration error
> c) It becomes a FloatField
> d) It defaults to infinity
>> [!success]- Answer
>> b) It raises a configuration error

> [!question] Which configuration key in settings.py allows multiple database connections?
> a) CONNECTIONS
> b) DATABASES
> c) DATABASE_URL
> d) DB_CONFIG
>> [!success]- Answer
>> b) DATABASES

> [!question] How does Django handle reverse queries for a ForeignKey by default?
> a) It raises an error
> b) It provides a related manager using modelname_set
> c) It creates a separate join table
> d) It caches all related objects
>> [!success]- Answer
>> b) It provides a related manager using modelname_set

> [!question] Which method resolves migration conflicts when multiple developers make database changes on different branches?
> a) python manage.py migrate --force
> b) python manage.py makemigrations --merge
> c) python manage.py sqlmigrate --merge
> d) python manage.py showmigrations --fix
>> [!success]- Answer
>> b) python manage.py makemigrations --merge

> [!question] What is the SQL equivalent of `Patient.objects.filter(nom="Bob")`?
> a) INSERT INTO app_patient (nom) VALUES ('Bob')
> b) SELECT * FROM app_patient WHERE nom = 'Bob'
> c) UPDATE app_patient SET nom = 'Bob'
> d) DELETE FROM app_patient WHERE nom = 'Bob'
>> [!success]- Answer
>> b) SELECT * FROM app_patient WHERE nom = 'Bob'

> [!question] Which optimization method should you use to solve the N+1 Query Problem for ForeignKey relationships?
> a) .exists()
> b) .select_related()
> c) .only()
> d) .defer()
>> [!success]- Answer
>> b) .select_related()

> [!question] If a Patient does not have a DossierMedical, what is the safest way to check before accessing it?
> a) patient.dossier
> b) hasattr(patient, 'dossier')
> c) patient.dossier_set.all()
> d) Patient.dossier.exists()
>> [!success]- Answer
>> b) hasattr(patient, 'dossier')

> [!question] What does the `primary_key=True` parameter do in a OneToOneField?
> a) It makes the foreign key the primary key of the related table
> b) It creates a composite primary key
> c) It disables the foreign key constraint
> d) It makes the field nullable
>> [!success]- Answer
>> a) It makes the foreign key the primary key of the related table

> [!question] Match the ORM advantage with its description.
>> [!example] Group A
>> a) Database Portability
>> b) SQL Injection Prevention
>> c) Rapid Development
>
>> [!example] Group B
>> n) No need to write repetitive SQL for standard CRUD
>> o) Parameterized queries neutralize SQLi attacks
>> p) Switch database engines without rewriting code
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Django field with its validation purpose.
>> [!example] Group A
>> a) EmailField
>> b) UUIDField
>> c) DecimalField
>
>> [!example] Group B
>> n) Universally unique identifier for primary keys
>> o) Validates email syntax on save
>> p) Fixed-point numbers for currency and precision
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the configuration with its correct setting behavior.
>> [!example] Group A
>> a) null=False, blank=False
>> b) null=True, blank=True
>> c) null=False, blank=True
>
>> [!example] Group B
>> n) Allows NULL, field is optional
>> o) NOT NULL, field is required
>> p) NOT NULL, field is optional (strings save as "")
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the on_delete option with its use case example.
>> [!example] Group A
>> a) CASCADE
>> b) PROTECT
>> c) SET_NULL
>
>> [!example] Group B
>> n) Doctor leaves, consultations remain with NULL doctor
>> o) Cannot delete a doctor with scheduled consultations
>> p) Deleting a doctor deletes all their consultations
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the relationship pattern with its query behavior.
>> [!example] Group A
>> a) ForeignKey reverse
>> b) OneToOneField reverse
>> c) ManyToManyField
>
>> [!example] Group B
>> n) Returns a single model instance
>> o) Creates an implicit join table automatically
>> p) Returns a QuerySet manager
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the migration command with its SQL equivalent inspection.
>> [!example] Group A
>> a) makemigrations myapp
>> b) sqlmigrate myapp 0001
>> c) showmigrations
>
>> [!example] Group B
>> n) Shows [X] for applied, [ ] for pending
>> o) Generates migration for a specific app
>> p) Displays raw SQL for a specific migration
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the CRUD operation with its correct Python code.
>> [!example] Group A
>> a) Reading all records
>> b) Updating a single instance
>> c) Batch updating records
>
>> [!example] Group B
>> n) Patient.objects.filter(nom="A").update(nom="B")
>> o) patient = Patient.objects.get(id=1); patient.nom = "B"; patient.save()
>> p) Patient.objects.all()
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the model relationship concept with its description.
>> [!example] Group A
>> a) Join Table
>> b) Foreign Key
>> c) Reverse Relationship
>
>> [!example] Group B
>> n) Column referencing another table's primary key
>> o) Querying from the parent to access child records
>> p) Intermediate table for M2M relationships
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the database configuration component with its purpose.
>> [!example] Group A
>> a) ENGINE
>> b) NAME
>> c) HOST
>
>> [!example] Group B
>> n) The server address for the database
>> o) The database backend driver class path
>> p) The name of the specific database to connect to
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the QuerySet evaluation concept with its example.
>> [!example] Group A
>> a) Lazy Evaluation
>> b) QuerySet Caching
>> c) QuerySet Slicing
>
>> [!example] Group B
>> n) Results are cached when the QuerySet is first evaluated
>> o) The database query is delayed until the data is actually needed
>> p) Limits the result set and triggers a database hit
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)