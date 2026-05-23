---
sources:
  - "[[02.1. Python Virtual Environments and Dependency Management]]"
  - "[[02.2. Django Architectural Philosophy and MVT Pattern]]"
  - "[[02.3. Project Directory Structure and Configurations]]"
  - "[[02.4. Django Application Lifecycle and Modularity]]"
  - "[[02.5. Best Practices for Secret Keys and Environments]]"
---
> [!question] A virtual environment isolates a project's Python dependencies from the rest of the operating system.
>> [!success]- Answer
>> True

> [!question] You should always commit your `venv` folder to Git so other developers can use it directly.
>> [!success]- Answer
>> False

> [!question] In Django's MVT pattern, the framework itself acts as the Controller.
>> [!success]- Answer
>> True

> [!question] The `settings.py` file acts as a centralized configuration hub for the Django project.
>> [!success]- Answer
>> True

> [!question] A Django Project can contain only one App.
>> [!success]- Answer
>> False

> [!question] The `SECRET_KEY` can be safely hardcoded in `settings.py` and committed to GitHub.
>> [!success]- Answer
>> False

> [!question] The Template layer in Django's MVT contains business logic that directly queries the database.
>> [!success]- Answer
>> False

> [!question] A Django App can be reused in multiple different Projects.
>> [!success]- Answer
>> True

> [!question] The `migrations/` folder contains schema version control history for database changes.
>> [!success]- Answer
>> True

> [!question] Gunicorn is a development server that can be used safely in production for handling network traffic.
>> [!success]- Answer
>> False

> [!question] Which command is used to create a new virtual environment?
> a) python3 -m venv venv
> b) pip install venv
> c) django-admin startenv
> d) python3 init venv
>> [!success]- Answer
>> a) python3 -m venv venv

> [!question] In Django's MVT pattern, what does the View correspond to in traditional MVC?
> a) Model
> b) View
> c) Controller
> d) Template
>> [!success]- Answer
>> c) Controller

> [!question] Which file in a Django project is the heart of the project containing the centralized configuration?
> a) manage.py
> b) urls.py
> c) settings.py
> d) wsgi.py
>> [!success]- Answer
>> c) settings.py

> [!question] What command creates a new Django app inside a project?
> a) django-admin startproject myapp
> b) python manage.py startapp myapp
> c) python manage.py createapp myapp
> d) django-admin startapp myapp
>> [!success]- Answer
>> b) python manage.py startapp myapp

> [!question] How should you read the SECRET_KEY in a secure production Django deployment?
> a) Hardcode it directly in settings.py
> b) Read it from environment variables
> c) Store it in the database
> d) Generate a new one every request
>> [!success]- Answer
>> b) Read it from environment variables

> [!question] What does the command `pip freeze > requirements.txt` do?
> a) Installs all packages from requirements.txt
> b) Exports a list of installed packages with versions
> c) Freezes the current Python version
> d) Creates a new virtual environment
>> [!success]- Answer
>> b) Exports a list of installed packages with versions

> [!question] Which file in a Django project serves as the global routing table?
> a) settings.py
> b) models.py
> c) urls.py
> d) views.py
>> [!success]- Answer
>> c) urls.py

> [!question] What is the purpose of the `admin.py` file in a Django app?
> a) To define database models
> b) To configure the automatically generated CMS administration panel
> c) To write business logic for HTTP requests
> d) To store environment variables
>> [!success]- Answer
>> b) To configure the automatically generated CMS administration panel

> [!question] Which methodology does the Twelve-Factor App methodology for cloud architecture recommend?
> a) Hardcoding all configuration values
> b) Injecting different Environment Variables at runtime
> c) Using the same settings for all environments
> d) Storing secrets in the Git repository
>> [!success]- Answer
>> b) Injecting different Environment Variables at runtime

> [!question] What is the role of the Model in Django's MVT pattern?
> a) It receives HTTP requests and returns responses
> b) It defines how data is presented to the user
> c) It represents the database schema as Python classes
> d) It acts as the routing dispatcher for URLs
>> [!success]- Answer
>> c) It represents the database schema as Python classes

> [!question] Match the virtual environment lifecycle step with the correct command.
>> [!example] Group A
>> a) Activation on Linux
>> b) Deactivation
>> c) Exporting dependencies
>
>> [!example] Group B
>> n) deactivate
>> o) source venv/bin/activate
>> p) pip freeze > requirements.txt
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the MVT component with its equivalent in traditional MVC.
>> [!example] Group A
>> a) Django Model
>> b) Django View
>> c) Django Template
>
>> [!example] Group B
>> n) MVC Controller
>> o) MVC Model
>> p) MVC View
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Django project file with its primary purpose.
>> [!example] Group A
>> a) manage.py
>> b) wsgi.py
>> c) settings.py
>
>> [!example] Group B
>> n) Synchronous web server entry point for production
>> o) Centralized configuration hub for the project
>> p) Command-line utility for administrative tasks
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Django app file with its purpose.
>> [!example] Group A
>> a) models.py
>> b) views.py
>> c) apps.py
>
>> [!example] Group B
>> n) App metadata and initialization code
>> o) Business logic that returns HttpResponse objects
>> p) Database schema defined as Python classes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the configuration element in settings.py with its role.
>> [!example] Group A
>> a) INSTALLED_APPS
>> b) DATABASES
>> c) MIDDLEWARE
>
>> [!example] Group B
>> n) Hooks that process requests globally
>> o) Registry of all active Django apps and plugins
>> p) Database connection strings
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the security risk with its consequence.
>> [!example] Group A
>> a) Exposed SECRET_KEY
>> b) Hardcoded credentials in settings.py
>> c) Committing .env to Git
>
>> [!example] Group B
>> n) Attacker can impersonate any user
>> o) Exposes database passwords publicly
>> p) Attacker can forge session cookies
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Django component with its MVT role.
>> [!example] Group A
>> a) Model
>> b) View
>> c) Template
>
>> [!example] Group B
>> n) Defines how data is presented to the user
>> o) Receives HTTP requests and contains business logic
>> p) Handles data validation and database interactions
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the step with its corresponding action.
>> [!example] Group A
>> a) python -m venv venv
>> b) pip install -r requirements.txt
>> c) source venv/bin/activate
>
>> [!example] Group B
>> n) Tells terminal to use isolated Python binaries
>> o) Creates an isolated directory tree
>> p) Installs dependencies from a manifest file
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Django project file with its production role.
>> [!example] Group A
>> a) wsgi.py
>> b) asgi.py
>> c) manage.py
>
>> [!example] Group B
>> n) Used only for local administrative commands
>> o) Asynchronous web server entry point
>> p) Synchronous web server entry point
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the security best practice with its description.
>> [!example] Group A
>> a) Use .env files
>> b) Add .env to .gitignore
>> c) Use os.environ.get()
>
>> [!example] Group B
>> n) Prevents secrets from being committed to version control
>> o) Safely reads variables with optional fallback values
>> p) Stores environment variables locally during development
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)