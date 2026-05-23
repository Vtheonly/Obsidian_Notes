---
sources:
  - "[[02.1. Python Virtual Environments and Dependency Management]]"
  - "[[02.2. Django Architectural Philosophy and MVT Pattern]]"
  - "[[02.3. Project Directory Structure and Configurations]]"
  - "[[02.4. Django Application Lifecycle and Modularity]]"
  - "[[02.5. Best Practices for Secret Keys and Environments]]"
---
> [!question] The `pip freeze` command shows all globally installed Python packages on the operating system.
>> [!success]- Answer
>> False

> [!question] In Django's MVT pattern, the Template is equivalent to the View in traditional MVC.
>> [!success]- Answer
>> True

> [!question] The `urls.py` file uses the `include()` function to delegate routes to internal application `urls.py` files.
>> [!success]- Answer
>> True

> [!question] After creating a Django app with `startapp`, Django automatically recognizes it without any additional configuration.
>> [!success]- Answer
>> False

> [!question] If an attacker discovers your Django SECRET_KEY, they can forge session cookies and impersonate any user.
>> [!success]- Answer
>> True

> [!question] The Django Template layer contains no business logic, only presentation formatting.
>> [!success]- Answer
>> True

> [!question] The `manage.py` file is used for production web server deployment.
>> [!success]- Answer
>> False

> [!question] A Django migration script dictates exactly how to alter the SQL database schema without losing existing data.
>> [!success]- Answer
>> True

> [!question] Database credentials stored in environment variables are parsed as integers by default.
>> [!success]- Answer
>> False

> [!question] Django's philosophy is "The web framework for perfectionists with deadlines."
>> [!success]- Answer
>> True

> [!question] What is the benefit of using `pip install -r requirements.txt` on a new machine?
> a) It creates a new virtual environment
> b) It installs the exact same library versions used in the original project
> c) It upgrades all packages to their latest versions
> d) It deactivates the current virtual environment
>> [!success]- Answer
>> b) It installs the exact same library versions used in the original project

> [!question] In the MVT request flow, what does the View pass data to after querying the Model?
> a) The URL Router
> b) The Template
> c) The Database
> d) The Browser directly
>> [!success]- Answer
>> b) The Template

> [!question] What is the role of `wsgi.py` in a Django project?
> a) To define URL routing patterns
> b) To provide a standard interface for production web servers to communicate with Django
> c) To manage database schema migrations
> d) To store application environment variables
>> [!success]- Answer
>> b) To provide a standard interface for production web servers to communicate with Django

> [!question] Which command analyzes changes in `models.py` and generates migration scripts?
> a) python manage.py migrate
> b) python manage.py makemigrations
> c) python manage.py sqlmigrate
> d) python manage.py startapp
>> [!success]- Answer
>> b) python manage.py makemigrations

> [!question] Why is it critical to use environment variables in Docker containers for microservices?
> a) Docker cannot read settings.py files
> b) Containers use identical images, so env vars are the only way to configure behavior at runtime
> c) Environment variables are faster than reading files
> d) Docker automatically generates SECRET_KEY values
>> [!success]- Answer
>> b) Containers use identical images, so env vars are the only way to configure behavior at runtime

> [!question] Which Python method reads a value from environment variables with an optional fallback?
> a) os.environ.read()
> b) os.environ.fetch()
> c) os.environ.get()
> d) os.environ.load()
>> [!success]- Answer
>> c) os.environ.get()

> [!question] What is the correct way to activate a virtual environment on Windows PowerShell?
> a) source venv/bin/activate
> b) venv\Scripts\Activate.ps1
> c) venv activate
> d) python venv activate
>> [!success]- Answer
>> b) venv\Scripts\Activate.ps1

> [!question] What does the `migrate` command do in Django?
> a) Creates new migration scripts
> b) Applies migration scripts to the database
> c) Creates a new Django project
> d) Starts the development server
>> [!success]- Answer
>> b) Applies migration scripts to the database

> [!question] What is the purpose of the `__init__.py` file in a Django app directory?
> a) It defines the app's database models
> b) It marks the directory as a Python package
> c) It contains the app's URL configuration
> d) It stores the app's metadata
>> [!success]- Answer
>> b) It marks the directory as a Python package

> [!question] Which of the following is NOT a component managed by `settings.py`?
> a) INSTALLED_APPS
> b) MIDDLEWARE
> c) VIEWS
> d) DATABASES
>> [!success]- Answer
>> c) VIEWS

> [!question] Match the terminal prompt indicator with its meaning.
>> [!example] Group A
>> a) (venv) prefix in terminal
>> b) No prefix in terminal
>> c) pip freeze output
>
>> [!example] Group B
>> n) Running in the global Python environment
>> o) The virtual environment is currently activated
>> p) A list of all installed packages and versions
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django MVT component with its description from the request flow.
>> [!example] Group A
>> a) URL Router
>> b) View
>> c) Model
>
>> [!example] Group B
>> n) Receives HTTP request and queries the database
>> o) Dispatches incoming request to the correct function
>> p) Returns a QuerySet of database records
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django concept with its description.
>> [!example] Group A
>> a) Project
>> b) App
>> c) Migration
>
>> [!example] Group B
>> n) A self-contained module that does something specific
>> o) A Python script dictating how to alter the database schema
>> p) A collection of configurations and apps for a website
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the settings.py component with its configuration purpose.
>> [!example] Group A
>> a) TEMPLATES
>> b) STATIC_URL
>> c) INSTALLED_APPS
>
>> [!example] Group B
>> n) Configuration for serving CSS and JavaScript assets
>> o) Registry of all activated Django apps and plugins
>> p) Configuration for the template rendering engine
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the security vulnerability with its prevention method.
>> [!example] Group A
>> a) SECRET_KEY exposure
>> b) Database credential leak
>> c) Environment confusion
>
>> [!example] Group B
>> n) Use separate .env files for development and production
>> o) Store in environment variables, never in code
>> p) Read from environment variable with os.environ.get()
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Django app file with its Django concept.
>> [!example] Group A
>> a) models.py
>> b) views.py
>> c) admin.py
>
>> [!example] Group B
>> n) HTTP Controllers holding business logic
>> o) Automatically generated CMS administration panel
>> p) Database schema defined as Python classes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the gitignore rule with its justification.
>> [!example] Group A
>> a) Add venv/ to .gitignore
>> b) Add .env to .gitignore
>> c) Commit only requirements.txt
>
>> [!example] Group B
>> n) Allows reproduction of the exact dependency set
>> o) Contains system-specific binary files that break on other OS
>> p) Contains secret keys and database credentials
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Django tool with its use case.
>> [!example] Group A
>> a) django-admin
>> b) manage.py
>> c) pip
>
>> [!example] Group B
>> n) Python package installer for dependencies
>> o) Thin wrapper used for project-level administrative commands
>> p) Command-line tool for starting new projects
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the environment variable with its typical value type.
>> [!example] Group A
>> a) DEBUG
>> b) SECRET_KEY
>> c) DATABASE_URL
>
>> [!example] Group B
>> n) A connection string to the database
>> o) Boolean value (True/False)
>> p) A long string of random characters
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the MVT layer with its responsibility.
>> [!example] Group A
>> a) Data Access Layer
>> b) Business Logic Layer
>> c) Presentation Layer
>
>> [!example] Group B
>> n) Django Template
>> o) Django Model
>> p) Django View
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)