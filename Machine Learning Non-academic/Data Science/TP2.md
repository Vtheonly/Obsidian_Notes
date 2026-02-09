

## Exercise 1: Hospital Patient Data Analysis

**Goal:** Create a mini-project to manipulate patient data and visualize basic statistics.

### Step 1: Create the project directory

Create a project folder named HospitalDataAnalysis.

### Step 2: Create a virtual environment with a specific Python version

If you have multiple Python versions installed (e.g., Python 3.10, 3.11), specify the one you need.

### Step 3: Activate it and install the required libraries

like: numpy pandas

### Step 4: Create project structure

Organize your project into a clean structure by creating the following folders and files:

```
HospitalDataAnalysis/
├── env/              # Virtual environment folder (ignored by Git)
├── data/             # Folder to store CSV files
│   └── patients.csv
├── notebooks/        # Jupyter notebooks
│   └── patients_analysis.ipynb
├── scripts/          # Optional Python scripts
├── .gitignore
└── README.md
```

### Step 5: Load and explore the data

*   Create a small CSV file patients.csv in the data/ folder with columns: PatientID, Age, Sex, BloodPressure, Cholesterol, Diagnosis
*   Insert some values



### Load it in the notebook using:

```python
import pandas as pd

df = pd.read_csv("../data/patients.csv")
df.head()
```

```python
In [ ]: # Run basic descriptive statistics using:

df.describe()

df['Sex'].value_counts()

df['Diagnosis'].value_counts()
```

```python
In [ ]: # Visualize the data : Create a Simple Plot using matplotlib

import matplotlib.pyplot as plt

plt.plot(df["Age"], df["Cholesterol"], marker="o")
plt.xlabel("Age")
plt.ylabel("Cholesterol")
plt.title("Cholesterol vs Age")
plt.show()
```

### Step 6: Initialize Git and create README

*   Create a GitHub account (if you don't already have one).
*   Go to https://github.com and sign up.
*   Create a new repository on GitHub called **HospitalDataAnalysis**.
    ✍️ Do not initialize it with a README, .gitignore, or license (we'll add them from local).
*   Link your local project with the GitHub repository:
*   Create a .gitignore file in your local project with the following content:

```
env/

__pycache__/

*.pyc
```
*   Commit and push again:

### Step 7: Share the project

*   How can you export all the installed libraries in your virtual environment to a file so that someone else can recreate the same environment?
*   Test recreating the environment on a different machine:


# Part 2: Lab Solution with Code and Explanations



### Step 1: Create the project directory

First, open your terminal or command prompt and run the following commands to create the main project folder and navigate into it.

```bash
# Create the directory
mkdir HospitalDataAnalysis

# Change into the new directory
cd HospitalDataAnalysis
```
**Explanation:**
*   `mkdir` is a standard command to "make a directory".
*   `cd` stands for "change directory" and moves your terminal's focus into the specified folder. All subsequent commands will be run from inside `HospitalDataAnalysis/`.

---

### Step 2: Create a virtual environment

Now, create an isolated Python environment for this project. This prevents conflicts with other projects' dependencies.

```bash
# Using Python 3's built-in venv module
# Replace 'python3' with 'python' if that's your command for Python 3
python3 -m venv env
```
**Explanation:**
*   `python3 -m venv` tells Python to run the `venv` module.
*   `env` is the name we are giving to our virtual environment folder. This is a common convention.

---

### Step 3: Activate it and install the required libraries

You must "activate" the environment before you can use it. The activation command differs based on your operating system.

**On macOS / Linux:**
```bash
source env/bin/activate
```

**On Windows (Command Prompt):**
```bash
.\env\Scripts\activate
```

Once activated, your terminal prompt will usually change to show `(env)`. Now, install the necessary libraries. We'll add `matplotlib` and `jupyterlab` as they are needed for the analysis notebook.

```bash
# Install pandas, numpy, matplotlib, and jupyterlab
pip install pandas numpy matplotlib jupyterlab
```
**Explanation:**
*   `pip` is Python's package installer. The `install` command downloads and installs the specified packages (`pandas` for data manipulation, `numpy` for numerical operations, `matplotlib` for plotting, and `jupyterlab` to run the notebook) into the active virtual environment (`env`).

---

### Step 4: Create project structure

Create the folders and empty files as specified in the tutorial.

```bash
# Create the data, notebooks, and scripts directories
mkdir data notebooks scripts

# Create the empty files
touch data/patients.csv notebooks/patients_analysis.ipynb .gitignore README.md
```
**Note:** The `touch` command creates empty files on macOS/Linux. On Windows PowerShell, you can use `New-Item -ItemType File data/patients.csv` for each file, or simply create them manually in your code editor.

Your project structure should now look like this:

```
HospitalDataAnalysis/
├── env/
├── data/
│   └── patients.csv
├── notebooks/
│   └── patients_analysis.ipynb
├── scripts/
├── .gitignore
└── README.md
```

---

### Step 5: Load and explore the data

#### 1. Create the CSV file
Open the `data/patients.csv` file and add the following content. This is our sample dataset.

**File: `data/patients.csv`**
```csv
PatientID,Age,Sex,BloodPressure,Cholesterol,Diagnosis
101,45,Male,120/80,210,Hypertension
102,60,Female,140/90,230,Hypertension
103,35,Female,110/70,180,Normal
104,52,Male,130/85,250,High Cholesterol
105,28,Male,115/75,190,Normal
106,65,Female,150/95,260,Hypertension
107,48,Male,125/82,220,Normal
108,70,Female,160/100,280,High Cholesterol
109,33,Female,105/65,170,Normal
110,55,Male,135/88,240,High Cholesterol
```

#### 2. Write the Jupyter Notebook
Start JupyterLab from your terminal (make sure your virtual environment is still active):

```bash
jupyter-lab
```

This will open a new tab in your browser. Navigate to `notebooks/` and open `patients_analysis.ipynb`. Add the following code into the notebook cells.

**File: `notebooks/patients_analysis.ipynb`**

**Cell 1: Import library and load data**
```python
import pandas as pd

# Load the dataset
# The path is relative to the notebook's location
df = pd.read_csv('../data/patients.csv')

# Display the first 5 rows to verify it loaded correctly
df.head()
```

**Cell 2: Run basic descriptive statistics**
```python
# Get a statistical summary of the numerical columns
print("--- Descriptive Statistics ---")
print(df.describe())

# Count the occurrences of each value in the 'Sex' column
print("\n--- Sex Distribution ---")
print(df['Sex'].value_counts())

# Count the occurrences of each diagnosis
print("\n--- Diagnosis Distribution ---")
print(df['Diagnosis'].value_counts())
```

**Cell 3: Visualize the data**
```python
import matplotlib.pyplot as plt

# Create a scatter plot of Age vs. Cholesterol
plt.figure(figsize=(8, 6)) # Optional: makes the plot bigger
plt.scatter(df["Age"], df["Cholesterol"]) # Using scatter is better for this data

# Add labels and a title for clarity
plt.xlabel("Age")
plt.ylabel("Cholesterol")
plt.title("Cholesterol vs Age")
plt.grid(True) # Optional: adds a grid for easier reading
plt.show()
```

---

### Step 4 (Part 2): Initialize Git and create README

#### 1. Initialize Git Repository
First, initialize a Git repository in the project's root directory.

```bash
git init
```

#### 2. Create `.gitignore` and `README.md`
**File: `.gitignore`**
This file tells Git which files or folders to ignore.

```
# Virtual environment folder
env/

# Python cache
__pycache__/
*.pyc
```

**File: `README.md`**
A good README explains what the project is about.

```markdown
# Hospital Patient Data Analysis

This is a mini-project for Tutorial 02 of IA2 - AP_DS.

## Project Goal

The goal is to create a small project to manipulate patient data and visualize basic statistics using Python, Pandas, and Matplotlib.

## How to Run

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies: `pip install -r requirements.txt`
4. Launch JupyterLab: `jupyter-lab`
5. Open and run the `notebooks/patients_analysis.ipynb` notebook.
```

#### 3. Create GitHub Repo and Push
1.  Go to [GitHub](https://github.com/) and create a new repository named `HospitalDataAnalysis`. **Do not** initialize it with a README or .gitignore.
2.  Copy the repository URL (e.g., `https://github.com/your-username/HospitalDataAnalysis.git`).
3.  Link your local repository to the remote one and push your code.

```bash
# Add all files to the staging area
git add .

# Create your first commit
git commit -m "Initial project setup with data and analysis notebook"

# Rename the default branch to 'main' (modern convention)
git branch -M main

# Add the remote repository URL
git remote add origin https://github.com/your-username/HospitalDataAnalysis.git

# Push your code to GitHub
git push -u origin main
```

---

### Step 5 (Part 2): Share the project

To allow others to easily recreate your environment, you should create a `requirements.txt` file.

#### 1. Export Installed Libraries
Run this command in your activated virtual environment:

```bash
pip freeze > requirements.txt
```
**Explanation:**
*   `pip freeze` lists all installed packages and their exact versions in the current environment.
*   The `>` symbol redirects this output and saves it into a file named `requirements.txt`.

Now, add this new file to Git and push it.

```bash
git add requirements.txt
git commit -m "Add requirements.txt for easy setup"
git push
```

#### 2. How to Recreate the Environment
Someone else can now set up the project by following these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/HospitalDataAnalysis.git
    cd HospitalDataAnalysis
    ```
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv env
    ```
3.  **Activate it:**
    ```bash
    source env/bin/activate  # Or .\env\Scripts\activate on Windows
    ```
4.  **Install all dependencies from the file:**
    ```bash
    pip install -r requirements.txt
    ```

This ensures that they will have the exact same versions of all the libraries you used, making the project fully reproducible.