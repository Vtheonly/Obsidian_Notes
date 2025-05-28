Okay, here's the note for `04_Templates_and_Jinja2.md`. This is where your Flask app starts to generate dynamic HTML for users!

---
# 04 Templates and Jinja2

> **Context**: You've learned to define routes, create view functions, and debug your Flask application. So far, your view functions have been returning simple strings. To build real web pages, you need to generate HTML, and often this HTML needs to include dynamic data.
> **Goal**: Understand how Flask uses templates, specifically with the Jinja2 templating engine, to render dynamic HTML. Learn to pass data from Python to templates, use basic Jinja2 syntax (variables, control structures, filters), and leverage template inheritance.

---

## 1. What are Templates?

In web development, a **template** is a file (usually HTML) that contains placeholder variables and some basic logic. A **templating engine** (like Jinja2) processes this template file, replacing the placeholders with actual data and executing the logic, to produce a final HTML document that is sent to the user's browser.

**Why use templates?**
*   **Separation of Concerns**: Keeps your presentation logic (HTML structure) separate from your application logic (Python code). This makes code cleaner, easier to manage, and allows designers and developers to work more independently.
*   **Reusability**: You can reuse template structures for different pages or parts of pages.
*   **Dynamic Content**: Easily inject data from your Python backend into your HTML.
*   **Readability**: HTML mixed directly in Python strings quickly becomes unmanageable. Templates provide a much cleaner way to define HTML.

Flask is configured to use **Jinja2** as its default templating engine. Jinja2 is powerful, fast, and has a syntax similar to Python.

---

## 2. Setting Up Templates in Flask

Flask automatically looks for templates in a folder named `templates` located in your application's root directory (or next to your application package).

**Project Structure (revisiting `01_Project_Structure.md`)**:
```
my_flask_app/
├── myproject/
│   ├── __init__.py
│   └── routes.py
├── static/
│   └── style.css  # (Example static file)
├── templates/     <-- Jinja2 templates go here
│   ├── index.html
│   └── user_profile.html
└── run.py
```

If you create a file like `templates/index.html`, Flask will be able to find it.

---

## 3. Rendering Templates with `render_template()`

Flask provides the `render_template()` function to process a template file and return it as an HTTP response.

```python
# myproject/routes.py
from flask import render_template
from myproject import app

@app.route('/')
def home():
    # This will look for 'index.html' in the 'templates' folder
    # and pass the 'page_title' variable to it.
    return render_template('index.html', page_title="Welcome Home!")

@app.route('/user/<username>')
def profile(username):
    user_data = {
        'name': username,
        'email': f"{username.lower()}@example.com",
        'is_active': True,
        'hobbies': ['coding', 'reading', 'hiking']
    }
    # Passes the 'user' dictionary to the 'user_profile.html' template
    return render_template('user_profile.html', user=user_data)
```

**Explanation**:
*   `from flask import render_template`: Import the necessary function.
*   `render_template('template_name.html', ...)`:
    *   The first argument is the filename of the template (relative to the `templates` folder).
    *   Subsequent keyword arguments (`page_title="...", user=user_data`) are variables that will be made available inside the template.

---

## 4. Jinja2 Template Syntax Basics

Inside your HTML template files, you can use Jinja2's special syntax to display variables and use control structures.

### 4.1. Variables
Variables passed from your Python view function are accessed using double curly braces: `{{ variable_name }}`.

**`templates/index.html`**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title> <!-- Accesses page_title passed from Python -->
</head>
<body>
    <h1>{{ page_title }}</h1>
    <p>This is the homepage of our amazing Flask application.</p>
</body>
</html>
```

### 4.2. Accessing Dictionary Keys and Object Attributes
If you pass a dictionary or an object, you can access its items or attributes using dot notation `.` or square bracket notation `[]`.

**`templates/user_profile.html`**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Profile: {{ user.name }}</title>
</head>
<body>
    <h1>User Profile: {{ user.name }}</h1>
    <p>Email: {{ user['email'] }}</p> <!-- Alternative access for dict keys -->
    <p>Status: {% if user.is_active %}Active{% else %}Inactive{% endif %}</p>

    <h2>Hobbies:</h2>
    {% if user.hobbies %}
        <ul>
            {% for hobby in user.hobbies %}
                <li>{{ hobby }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No hobbies listed.</p>
    {% endif %}
</body>
</html>
```

### 4.3. Control Structures
Jinja2 supports common control structures using `{% ... %}` blocks.

*   **If/Else/Elif Statements**:
    ```jinja2
    {% if user.is_admin %}
        <p>Welcome, Administrator!</p>
    {% elif user.is_moderator %}
        <p>Welcome, Moderator!</p>
    {% else %}
        <p>Welcome, User!</p>
    {% endif %}
    ```

*   **For Loops**: Iterate over sequences (lists, tuples, dictionaries).
    ```jinja2
    <ul>
    {% for item in item_list %}
        <li>{{ item }}</li>
    {% else %}
        <li>No items in the list.</li> {# Optional: displayed if the list is empty #}
    {% endfor %}
    </ul>
    ```
    You can also access loop helper variables like `loop.index`, `loop.index0`, `loop.first`, `loop.last`.

### 4.4. Filters
Filters allow you to modify variables before displaying them. They are applied using the pipe `|` symbol.
`{{ variable | filter_name }}` or `{{ variable | filter_name(argument) }}`

**Common Jinja2 Filters**:
*   `capitalize`: `{{ "hello world" | capitalize }}` → `Hello world`
*   `lower`: `{{ "HELLO" | lower }}` → `hello`
*   `upper`: `{{ "hello" | upper }}` → `HELLO`
*   `title`: `{{ "hello world" | title }}` → `Hello World`
*   `trim`: `{{ "  hello  " | trim }}` → `hello`
*   `length` or `count`: `{{ my_list | length }}` → Number of items
*   `default`: `{{ user_bio | default("No bio provided.") }}` → Displays "No bio provided." if `user_bio` is undefined or false.
*   `safe`: Marks a string as safe, preventing auto-escaping (use with caution for user-generated content to avoid XSS). `{{ html_content | safe }}`
*   `join`: `{{ my_list | join(', ') }}` → `item1, item2, item3`
*   `truncate`: `{{ long_text | truncate(100, True) }}` → Truncates to 100 chars, adds ellipsis.

**Example with Filters**:
```html
<p>Username (capitalized): {{ user.name | capitalize }}</p>
<p>Number of hobbies: {{ user.hobbies | length }}</p>
```

### 4.5. Comments
Template comments are written as `{# This is a comment #}`. They are not included in the rendered HTML.

---

## 5. Template Inheritance

Template inheritance is a powerful Jinja2 feature that allows you to create a base layout template (e.g., `base.html`) with common HTML structure (like header, navigation, footer) and then have other templates "extend" this base and fill in specific blocks.

**`templates/base.html` (Base Layout)**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Flask App{% endblock %}</title> <!-- Default title -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}"> {# Link to static CSS #}
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('home') }}">Home</a> |
            <a href="{{ url_for('about_page') }}">About</a> {# Assuming you have an 'about_page' view #}
            {# More navigation links #}
        </nav>
    </header>

    <main>
        {% block content %}
            <!-- Content from child templates will go here -->
        {% endblock %}
    </main>

    <footer>
        <p>&copy; {{ now().year }} My Awesome Company</p> {# Jinja can access some globals like now() #}
    </footer>
</body>
</html>
```

**Explanation of `base.html`**:
*   `{% block block_name %}` ... `{% endblock %}`: Defines named blocks that child templates can override.
*   `url_for('static', filename='style.css')`: This is a Flask/Jinja2 function that generates the correct URL for static files (like CSS or JS). It's preferred over hardcoding paths. (`01_Static_Files.md` will cover this in more detail).
*   `url_for('home')`: Generates a URL for the view function named `home`.

**`templates/index.html` (Child Template Extending `base.html`)**:
```html
{% extends "base.html" %} {# Must be the first line #}

{% block title %}Welcome - {{ super() }}{% endblock %} {# super() includes parent block content #}

{% block content %}
    <h1>{{ page_title }}</h1>
    <p>This is the homepage content, inheriting the base layout.</p>
    <p>It's much cleaner now!</p>
{% endblock %}
```
**`templates/user_profile.html` (Another Child Template)**:
```html
{% extends "base.html" %}

{% block title %}Profile: {{ user.name }} - My Flask App{% endblock %}

{% block content %}
    <h1>User Profile: {{ user.name | upper }}</h1>
    <p>Email: {{ user.email }}</p>
    <p>Status: {% if user.is_active %}Active{% else %}Inactive{% endif %}</p>

    <h2>Hobbies:</h2>
    {% if user.hobbies %}
        <ul>
            {% for hobby in user.hobbies %}
                <li>{{ hobby | capitalize }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No hobbies listed.</p>
    {% endif %}
{% endblock %}
```
**Benefits of Inheritance**:
*   **DRY (Don't Repeat Yourself)**: Avoids duplicating common HTML across multiple pages.
*   **Maintainability**: Changes to the base layout (e.g., adding a new navigation link) automatically apply to all inheriting pages.
*   **Consistency**: Ensures a consistent look and feel across your site.

---

## 6. Linking Static Files (`url_for()`)

As seen in the `base.html` example, `url_for('static', filename='path/to/file')` is the standard way to link to CSS, JavaScript, images, etc., located in your `static` folder.

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```
Flask will correctly generate the URL path (e.g., `/static/css/main.css`).

---

## 7. Other Useful Jinja2 Features (Brief Mention)

*   **Macros**: Reusable template snippets, similar to functions.
*   **Includes**: `{% include 'partial.html' %}` to insert the content of another template. Useful for components like sidebars or forms that are used in multiple places but don't fit the full inheritance model.
*   **Tests**: Check conditions, e.g., `{% if name is defined %}` or `{% if number is odd %}`.
*   **Context Processors**: Functions that automatically inject variables into the context of all templates. Useful for global data like the current user or site name.

---

## 8. Summary & Key Takeaways

*   Templates (HTML + Jinja2 syntax) separate presentation from application logic.
*   Flask uses the `templates` folder by default.
*   `render_template('filename.html', **kwargs)` passes data to templates.
*   Jinja2 syntax:
    *   `{{ variable }}` for outputting variables.
    *   `{% control_structure %}` for loops, conditionals.
    *   `variable | filter` for modifying data.
    *   `{# comment #}` for template comments.
*   **Template inheritance** (`{% extends %}`, `{% block %}`) is crucial for DRY and maintainable layouts.
*   Use `url_for('static', filename='...')` to link static files and `url_for('view_function_name')` for internal links.

By mastering templates and Jinja2, you can now build dynamic, data-driven web pages with Flask, laying a strong foundation for more complex user interfaces.

---

## 9. Checklist

*   Understand the purpose of templates and a templating engine.
*   Know where Flask expects template files to be located.
*   Be able to use `render_template()` to render a template and pass data to it.
*   Write basic Jinja2 syntax: display variables, use `if/else`, and `for` loops.
*   Apply common Jinja2 filters to variables.
*   Implement template inheritance using `{% extends %}` and `{% block %}`.
*   Correctly link to static files using `url_for('static', ...)`.