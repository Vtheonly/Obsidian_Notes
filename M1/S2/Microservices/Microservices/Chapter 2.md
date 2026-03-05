
## Chapter 2: The ORM and Models

### 1. Object Relational Mapping Concept
**Definition:** ORM (Object-Relational Mapping) is a technique that lets you query and manipulate data from a database using an object-oriented paradigm.

**Why use an ORM?**
Instead of writing raw SQL queries (`SELECT * FROM users WHERE age > 20`), you write Python code (`User.objects.filter(age__gt=20)`). 
*   **Abstraction:** You don't need to be a SQL expert.
*   **Portability:** You can switch from SQLite to PostgreSQL by just changing a few lines in `settings.py`; the ORM translates your Python code into the correct SQL dialect automatically.
*   **Security:** Automatically protects against SQL injection attacks.

**Mapping Logic:**
*   Python **Class** $\rightarrow$ Database **Table**
*   Class **Attributes** $\rightarrow$ Table **Columns**
*   Class **Instances (Objects)** $\rightarrow$ Table **Rows**

---

### 2. Model Creation and Field Types
Models are defined in `models.py` by subclassing `django.db.models.Model`.

**Common Field Types:**
*   *Text/Numbers:* `CharField` (short text, requires `max_length`), `TextField` (long text), `IntegerField`, `FloatField`.
*   *Dates:* `DateField`, `DateTimeField`.
*   *Specific:* `EmailField` (validates email format), `BooleanField`, `URLField`, `FileField`, `ImageField`.

**Field Options (Parameters):**
*   `max_length=n`: Maximum character length.
*   `null=True`: Allows storing `NULL` in the database. (Default is False).
*   `blank=True`: Allows the field to be left empty in HTML forms. (Default is False).
*   `default=value`: Sets a default value if none is provided.
*   `unique=True`: Ensures no two rows have the same value for this column.
*   `auto_now_add=True`: Automatically sets the field to the current date/time when the object is *created*.

> **Important Reminder:** `null=True` affects the database schema. `blank=True` affects form validation. If you have a `CharField` that is optional, you should generally use `blank=True, null=True` (though Django specifically recommends empty strings `""` for text fields, meaning often just `blank=True` is used for strings).

---

### 3. Database Relationships
Django simplifies complex SQL `JOIN` operations using relation fields.

**1. One-to-Many (1-n) $\rightarrow$ `ForeignKey`**
*   *Concept:* One doctor can have many consultations. Each consultation belongs to exactly one doctor.
*   *Code:* `medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)`

**2. Many-to-Many (n-n) $\rightarrow$ `ManyToManyField`**
*   *Concept:* A patient can be prescribed many medications, and a medication can be prescribed to many patients.
*   *SQL equivalence:* Creates a hidden intermediate "junction" table automatically.
*   *Code:* `medicaments = models.ManyToManyField(Medicament)`

**3. One-to-One (1-1) $\rightarrow$ `OneToOneField`**
*   *Concept:* One patient has exactly one medical dossier.
*   *Code:* `patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)`

**What is `on_delete`?**
When the referenced object is deleted, what happens to the objects pointing to it?
*   `models.CASCADE`: If a Doctor is deleted, all their Consultations are deleted too.
*   `models.PROTECT`: Prevents deletion of the Doctor if they still have Consultations.
*   `models.SET_NULL`: The consultation remains, but the doctor field is set to NULL (requires `null=True`).

---

### 4. CRUD Operations
CRUD stands for Create, Read, Update, Delete. We do this via the model's `objects` manager.

*   **Create:**
    ```python
    p = Patient.objects.create(nom="Alice", email="alice@email.com")
    # OR
    p = Patient(nom="Alice")
    p.save()
    ```
*   **Read:**
    *   `Patient.objects.all()`: Returns a QuerySet of all records.
    *   `Patient.objects.filter(nom="Alice")`: Returns a QuerySet of records matching the condition.
    *   `Patient.objects.get(id=1)`: Returns exactly ONE object.
    > **Tip:** `get()` will crash (throw a `DoesNotExist` error) if the object isn't found, or `MultipleObjectsReturned` if more than one is found. `filter()` safely returns an empty list `[]` if nothing is found.
*   **Update:**
    Fetch the object, modify attributes, and call `save()`.
    ```python
    p = Patient.objects.get(id=1)
    p.nom = "Bob"
    p.save() # This triggers the SQL UPDATE
    ```
*   **Delete:**
    ```python
    p = Patient.objects.get(id=1)
    p.delete()
    ```

---

### 5. Database Configuration and Migrations
**Configuration:**
Inside `settings.py`, the `DATABASES` dictionary configures the connection. You define the `ENGINE` (e.g., `django.db.backends.postgresql` or `sqlite3`), `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT`.

**Migrations Lifecycle:**
Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model) into your database schema.

1.  **Define Models:** Write your classes in `models.py`.
2.  **Generate Migration:** `python manage.py makemigrations`
    *   This writes a Python script representing the schema change.
3.  **Apply Migration:** `python manage.py migrate`
    *   This translates the Python script into SQL and executes it against your configured database.



## Chapter 2.1: Advanced ORM Configurations, Limits, and SQL Mappings

### 1. Strict MVC vs MVT Comparison
To perfectly clarify the MVC vs MVT theoretical distinction mentioned in the slides:
*"MVT is very close to MVC, the main difference is that the controller is managed by the framework itself."*

| Component Role | MVC Architecture | MVT / MCT (Django) Architecture |
| :--- | :--- | :--- |
| **Data (Données)** | Model | Model |
| **Control Logic (Logique de contrôle)** | Controller | View (Django) |
| **Presentation (Présentation)** | View | Template |

### 2. Comprehensive Model Fields and Code Comments
The slides provide specific comments and parameters that dictate exact database behavior:
*   `choices=LISTE`: Restricts the field to a predefined list of authorized values (creates a dropdown in forms).
*   **Specific code comments from the slides:**
    *   `null=False`: Translates to `# Pas NULL en BD` (The database column gets a `NOT NULL` constraint).
    *   `blank=False`: Translates to `# Champ requis` (The HTML form will require this field; it cannot be left empty).
    *   `auto_now_add=True`: Translates to `# Auto la creation` (Django handles the timestamp automatically upon `INSERT`).

### 3. Database Relationship SQL Mappings
How does Django translate its relationship fields into actual SQL?
1.  **ForeignKey (1 to n):** Creates a standard **Clé étrangère** (Foreign Key) column in the SQL table.
2.  **ManyToManyField (n to n):** Automatically creates a **Table de liaison** (Junction Table / Join Table) in the database to manage the pairs of IDs.
3.  **OneToOneField (1 to 1):** Creates a **Clé étrangère + Unique constraint**. (Translates to: `# Chaque patient a UN SEUL dossier`).

### 4. ORM Theoretical Advantages and Limits
**Advantages:**
*   Abstraction of SQL leading to a massive gain in productivity.
*   **Portability:** You can switch RDBMS (Relational Database Management Systems) without rewriting queries.
*   Coherence between the object model and the database.
*   Automatic management of complex relational joins.

**Limits (Crucial for Exams):**
*   **Performance Overhead:** Surcharge de performance on highly complex queries. The ORM generates SQL that might not be 100% optimized for a very specific edge case.
*   **Less Fine-Grained Control:** Less control over fine SQL optimizations (like specific index hinting).
*   **Learning Curve:** Mastering migrations and object-mapping concepts takes time.

### 5. Database settings.py Nuances
When configuring `settings.py`, the `DATABASES` dictionary requires specific parameters:
*   `ENGINE`: Determines the database backend. Options specifically mentioned are `sqlite3`, `postgresql`, and `mysql`. The string looks like `django.db.backends.postgresql`.
*   `PORT`: The slides explicitly mention `5432` as the default port for PostgreSQL. (MySQL typically uses 3306).

---
