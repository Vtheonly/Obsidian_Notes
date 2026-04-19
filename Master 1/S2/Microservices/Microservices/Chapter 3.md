
## Chapter 3: URLs Views and Templates

### 1. URL Dispatcher and Routing
The URL dispatcher in `urls.py` captures incoming HTTP requests and maps them to the appropriate View. 

**Static URLs:** Fix paths.
```python
path('contact/', views.contact, name='contact')
```

**Dynamic URLs (Path Converters):** Capturing data from the URL to pass to the view.
*   `path('article/<int:id>/', views.voir_article)` $\rightarrow$ Passes `id` as an integer.
*   `path('blog/<slug:titre>/', views.detail_blog)` $\rightarrow$ A slug is a URL-friendly string (e.g., `my-first-post`). Great for SEO.
*   `path('files/<path:chemin>/', views.download)` $\rightarrow$ Captures a full path, including forward slashes `/`.

**Regex URLs:** For complex matching.
```python
re_path(r'^archive/(?P<annee>[0-9]{4})/$', views.archive)
```

> **Tip:** The `name='contact'` parameter is crucial. It allows you to reverse-resolve URLs in your templates (e.g., `{% url 'contact' %}`) instead of hardcoding `/contact/`. If you change the URL structure later, your templates won't break.

---

### 2. Views Function vs Class Based
The View is the business logic center. It takes an `HttpRequest` and returns an `HttpResponse`.

**Function-Based Views (FBV):** Simple and direct.
```python
def ma_vue(request):
    context = {'nom': 'Utilisateur'}
    return render(request, 'template.html', context)
```

**Class-Based Views (CBV):** Structured, reusable, relies on OOP inheritance.
```python
from django.views import View

class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')
        
    def post(self, request):
        # Process form data
        return render(request, 'dashboard.html')
```

**The Magic of `dispatch()`:**
In a CBV, when a request arrives, it hits the `dispatch()` method first. `dispatch()` analyzes the HTTP method (GET, POST, PUT, etc.) and routes the request to the corresponding method in your class (`self.get()`, `self.post()`). This is also where decorators like `@method_decorator(login_required)` are applied.

---

### 3. Template Engine and Inheritance
Django templates merge HTML presentation with Python data.

**Syntax:**
*   **Variables:** `{{ nom_variable }}`
*   **Logic (Tags):** `{% if condition %}`, `{% for item in list %}`

**Template Inheritance:**
This is the most powerful feature. It prevents code duplication (DRY principle).
1.  **Base Template (`base.html`):** Contains the skeletal HTML (doctype, head, navbar, footer). It defines blocks using `{% block content %}{% endblock %}`.
2.  **Child Template (`home.html`):** Declares `{% extends "base.html" %}` at the very top. It then injects specific HTML into the parent's blocks.

**Inclusions (`{% include %}`):**
Used to separate partial UI components (like a navbar or footer) into distinct files to keep `base.html` clean.
```html
{% include 'includes/navbar.html' %}
```

---

### 4. Managing Static Files
Static files are CSS, JavaScript, and images that do not change dynamically.

**Configuration (`settings.py`):**
*   `STATIC_URL = '/static/'`: The URL prefix the browser uses.
*   `STATICFILES_DIRS`: Where Django looks for static files during development.
*   `STATIC_ROOT`: The absolute folder path where Django will collect all static files for deployment.

**Usage in Templates:**
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

**Deployment Command:** `python manage.py collectstatic` gathers all static files from all apps into the `STATIC_ROOT` folder so a web server (like Nginx) can serve them rapidly.

---

## Chapter 3.1: URL Regular Expressions, Dispatcher, and HTML5 Templates

### 1. Advanced URL Routing and Regex
While `<int:id>` is modern and clean, older Django code or highly specific routing requires Regular Expressions using `re_path`.
*   **Syntax:** `re_path(r'^archive/(?P<annee>[0-9]{4})/$', views.archive)`
    *   `r'^...'`: The `r` denotes a raw string. `^` means "start of string" and `$` means "end of string".
    *   `(?P<annee>...)`: This is a named capturing group in Python regex. It captures the value and passes it to the view as a keyword argument named `annee`.
    *   `[0-9]{4}`: Ensures the captured value is exactly 4 digits long.
*   **Slug Concept:** A slug (`<slug:titre>`) is specifically used for **SEO (Search Engine Optimization)** to make URLs human-readable (e.g., `/blog/my-post/` instead of `/blog/12/`).

### 2. The Mechanics of the dispatch Method
In Class-Based Views (CBVs), the `dispatch()` method is the absolute gatekeeper.
*   **Role:** It is the principal entry point of the `View` class.
*   **Function:** It receives the HTTP request, identifies the HTTP verb (`GET`, `POST`, `PUT`), and mathematically routes it to the corresponding python method (e.g., `def get()`, `def post()`).
*   **Decorators:** Because `dispatch` handles *all* incoming requests for that class, if you want to protect the entire view (e.g., requiring a user to be logged in), you apply decorators to `dispatch` using `@method_decorator(@login_required)`.

### 3. HTML5 Standard Boilerplate in Django
The slides mandate a strict HTML5 document structure inside `base.html` for best practices:
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Titre de la page{% endblock %}</title>
</head>
<body>
    <header>
        <!-- En-tete du site -->
    </header>
    <nav>
        <!-- Liens de navigation -->
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <!-- Pied de page -->
    </footer>
</body>
</html>
```

### 4. settings.py Template and Static Directories
Understanding the exact settings variables for templates:
*   `BASE_DIR`: Defined using `pathlib.Path(__file__).resolve().parent.parent`. It points to the root of your project.
*   `TEMPLATES` -> `BACKEND`: Uses `django.template.backends.django.DjangoTemplates`.
*   `TEMPLATES` -> `DIRS`: `[os.path.join(BASE_DIR, 'templates')]`. This tells Django to look for a folder named `templates` at the root of the project, not just inside apps.
*   `TEMPLATES` -> `APP_DIRS`: `True`. This tells Django to automatically look inside every installed app for a folder named `templates/`.

---
