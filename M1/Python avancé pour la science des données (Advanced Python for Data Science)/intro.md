
## 1. Python Virtual Environments (venv)

### 1.1 How does a venv work

A **virtual environment (venv)** is an isolated environment that allows you to install Python packages separately from your system-wide Python.  
When you create a venv, it:

- Makes a **copy of your Python interpreter** (not the whole Python installation, just the executable and libraries it needs).
    
- Creates a folder structure like:
    
    ```
    project/
    ├── venv/
    │   ├── bin/ (or Scripts\ on Windows)
    │   ├── lib/
    │   ├── include/
    │   └── pyvenv.cfg
    ```
    
- When you **activate** it, the `PATH` variable changes so that `python` and `pip` point to the venv’s executables instead of the system ones.
    

So all installations via `pip` go inside `venv/lib/...` instead of global directories.

---

### 1.2 How to know all the packages installed

Inside an activated venv, run:

```bash
pip list
```

Or to save them to a file:

```bash
pip freeze > requirements.txt
```

This lists every package and version currently installed in that virtual environment.

---

### 1.3 How to remove a venv

Deactivate it first (if it’s active):

```bash
deactivate
```

Then delete the folder:

```bash
rm -rf venv
```

That’s it. Virtual environments are self-contained — no external registry or system config to clean.

---

### 1.4 How to merge the content of two venvs

You can’t directly “merge” two venvs, but you can combine their package lists.

If you have two environments, say `venv1` and `venv2`:

```bash
source venv1/bin/activate
pip freeze > req1.txt
deactivate

source venv2/bin/activate
pip freeze > req2.txt
deactivate

cat req1.txt req2.txt | sort | uniq > merged.txt
python -m venv new_venv
source new_venv/bin/activate
pip install -r merged.txt
```

This creates a new venv with all packages from both environments.

---

### 1.5 How to change which venv is being used

#### In **VS Code**:

- Open the Command Palette (`Ctrl+Shift+P`)
    
- Search for **“Python: Select Interpreter”**
    
- Choose the venv path you want (e.g., `.venv/bin/python`)
    

#### In **Terminal**:

Activate the one you want manually:

```bash
source path/to/venv/bin/activate
```

Deactivate with:

```bash
deactivate
```

#### In **Jupyter Notebook**:

1. Activate your venv:
    
    ```bash
    source venv/bin/activate
    ```
    
2. Install Jupyter and add the venv to kernels:
    
    ```bash
    pip install jupyter ipykernel
    python -m ipykernel install --user --name=venv_name
    ```
    
3. Restart Jupyter, then select the kernel named `venv_name` from the top-right corner.
    

---

### 1.6 Does an entire Python interpreter get installed in the venv?

Not exactly.  
The venv **copies or links the interpreter executable** and builds a local environment around it. It doesn’t redownload Python — it uses your system Python binary but isolates dependencies and paths.

---

### 1.7 Difference between Python versions (3.7, 3.9, 3.12)

Each version adds:

- **New syntax features** (e.g., pattern matching in 3.10)
    
- **Performance improvements**
    
- **Deprecated or removed functions**
    
- **Updated standard library modules**
    

For example:

- **Python 3.7**: dataclasses introduced.
    
- **Python 3.9**: new string methods and dict union (`a | b`).
    
- **Python 3.12**: faster startup, better type annotations.
    

You should generally use the **newest stable version** unless your project depends on older libraries.

---

## 2. VS Code and Python Integration

### 2.1 What does the Python extension do in VS Code?

The official **Python extension**:

- Detects Python interpreters and virtual environments.
    
- Provides syntax highlighting, IntelliSense (autocompletion, type hints).
    
- Adds debugging tools (breakpoints, variable watch).
    
- Lets you run cells or full files.
    
- Integrates with Jupyter notebooks.
    
- Manages linting (via `flake8`, `pylint`) and formatting (e.g., `black`).
    

Without it, VS Code treats Python like plain text.

---

### 2.2 Run button differences in VS Code

At the top right of VS Code, the “run” triangle behaves differently depending on the option:

|Option|Description|
|---|---|
|**Run Code**|Runs using the **Code Runner extension**, not the Python debugger. It just executes the script quickly (like `python file.py`) without debugging or environment handling.|
|**Run Python File**|Uses the **Python extension**, runs in the terminal, respects your selected interpreter (venv), and allows debugging.|
|**Run as Task**|Runs it as a **VS Code task**, defined in `.vscode/tasks.json`. Used for automating build/test pipelines or chained commands.|

In short:

- **Run Code** = quick test, no environment awareness
    
- **Run Python File** = proper execution in your project environment
    
- **Run as Task** = part of automated workflows
    

---

## 3. Jupyter and venv

### 3.1 Difference between `.ipynb` and `.py`

|Type|Description|
|---|---|
|**.py**|A normal Python script. Plain text code executed top to bottom.|
|**.ipynb**|A Jupyter Notebook file in JSON format. It holds code cells, markdown text, and outputs (plots, tables, etc.). Interactive for data science or teaching.|

`.ipynb` = interactive and stateful.  
`.py` = linear and static.

---

### 3.2 How to load a venv in Jupyter

If you already created a venv, just add it as a kernel:

```bash
source venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=venv_name
```

Then select `venv_name` inside Jupyter from **Kernel → Change Kernel**.

---

### 3.3 How to make a venv in Jupyter

In a Jupyter cell:

```python
!python -m venv myenv
!source myenv/bin/activate
```

But normally, it’s better to make the venv outside, then install it as a kernel as shown above.

---

## 4. Requirements File

### 4.1 How to make a requirements file

Inside an activated environment:

```bash
pip freeze > requirements.txt
```

This saves all installed packages and their versions.  
To recreate the same environment later:

```bash
pip install -r requirements.txt
```

---

## 5. Machine Learning (Extra Context)

### 5.1 SVM (Support Vector Machine)

An **SVM** is a supervised learning algorithm used for **classification** and **regression**.  
It finds the optimal **hyperplane** that separates data points of different classes with the **maximum margin**.

---

### 5.2 Fitting

“Fitting” a model means **training it on data** — the process where the algorithm learns patterns and parameters from the input features.

For example:

```python
model.fit(X_train, y_train)
```

Here the model learns the relationship between X and y.

---

### 5.3 Linear Regression

**Linear regression** models the relationship between one or more independent variables and a dependent variable using a straight line:

```
y = a*x + b
```

It minimizes the **sum of squared errors** between predictions and actual values.

---

## Summary

|Concept|Core Idea|
|---|---|
|venv|Isolated Python environment|
|pip list|See installed packages|
|requirements.txt|Save/restore dependencies|
|remove venv|Just delete the folder|
|merge venvs|Combine `pip freeze` outputs|
|Python extension|Adds intelligence and debugging to VS Code|
|Run options|“Run Code” is quick; “Run Python File” uses interpreter|
|.py vs .ipynb|Script vs interactive notebook|
|Python versions|Language and performance updates|
|SVM|Classification model using hyperplanes|
|Fitting|Model training|
|Linear Regression|Line-based prediction model|

---

Would you like me to turn this into a **clean Obsidian.md note** (with structure and callouts for definitions/examples)? It’ll look more polished and ready for your notes.