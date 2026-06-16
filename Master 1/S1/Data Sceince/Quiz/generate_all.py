#!/usr/bin/env python3
"""Generate all quiz files for all 6 chapters - 2 files per chapter, 30 questions each."""
import os

TF_TPL = "> [!question] {q}\n>> [!success]- Answer\n>> {a}"

def make_tf(q, a):
    return TF_TPL.format(q=q, a=a)

def make_mc(q, opts, ans):
    lines = [f"> [!question] {q}"]
    for o in opts:
        lines.append(f"> {o}")
    lines.append(">> [!success]- Answer")
    lines.append(f">> {ans}")
    return "\n".join(lines)

def make_match(a_group, b_group, answer_key):
    lines = ["> [!question] Match the items."]
    lines.append(">> [!example] Group A")
    for i, item in enumerate(a_group):
        lines.append(f">> {chr(97+i)}) {item}")
    lines.append(">")
    lines.append(">> [!example] Group B")
    for i, item in enumerate(b_group):
        lines.append(f">> {chr(110+i)}) {item}")
    lines.append(">")
    lines.append(">> [!success]- Answer")
    for line in answer_key.split("\n"):
        lines.append(f">> {line}")
    return "\n".join(lines)

def write_quiz(chapter_dir, filename, sources, tf_data, mc_data, match_data):
    lines = ["---", "sources:"]
    for s in sources:
        lines.append(f'  - "{s}"')
    lines.append("---")
    lines.append("")
    
    for q, a in tf_data:
        lines.append(make_tf(q, a))
        lines.append("")
    
    for q, opts, ans in mc_data:
        lines.append(make_mc(q, opts, ans))
        lines.append("")
    
    for a_group, b_group, ak in match_data:
        lines.append(make_match(a_group, b_group, ak))
        lines.append("")
    
    content = "\n".join(lines)
    filepath = os.path.join(chapter_dir, filename)
    os.makedirs(chapter_dir, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {filepath}")

# ===================== CHAPTER 01 =====================
ch01_sources = [
    "[[1.1. Data Science Fundamentals and Workflows]]",
    "[[1.2. Exercise 1. Identify Applications]]",
    "[[1.3. Exercise 2. Project Roles and Critical Thinking]]",
]
ch01_tf_a = [
    ("Data science is only about building machine learning models.", "False"),
    ("The CRISP-DM framework is a standard process model for data science projects.", "True"),
    ("Data science workflows are always linear and never iterative.", "False"),
    ("Unstructured data like images and text can be analyzed in data science.", "True"),
    ("Descriptive analytics focuses on predicting future outcomes.", "False"),
    ("A hypothesis in data science must always be testable.", "True"),
    ("Data scientists primarily communicate results through raw data alone.", "False"),
    ("Cross-industry standard processes help structure data science projects.", "True"),
    ("Regression analysis is used exclusively for categorical outcomes.", "False"),
    ("Exploratory data analysis is performed after model deployment.", "False"),
]
ch01_tf_b = [
    ("Data mining and data science are synonymous terms.", "False"),
    ("The data science lifecycle typically begins with data collection.", "True"),
    ("Python is one of the most popular programming languages for data science.", "True"),
    ("Data science projects always require big data infrastructure.", "False"),
    ("Feature engineering is a step performed before model training.", "True"),
    ("Data visualization is only useful for final presentations.", "False"),
    ("Machine learning models always require labeled data.", "False"),
    ("Domain expertise is valuable in data science.", "True"),
    ("SQL is a language used for querying relational databases.", "True"),
    ("A data science project ends after model deployment.", "False"),
]
ch01_mc_a = [
   ("Which is NOT a step in the data science workflow?",
    ["a) Data collection", "b) Model deployment", "c) Algorithm patenting", "d) Communication of results"], "c)"),
   ("What type of analytics answers 'What happened'?",
    ["a) Descriptive analytics", "b) Predictive analytics", "c) Prescriptive analytics", "d) Diagnostic analytics"], "a)"),
   ("Which technique groups similar data points without labels?",
    ["a) Linear regression", "b) Clustering", "c) Classification", "d) Hypothesis testing"], "b)"),
   ("Primary purpose of data preprocessing?",
    ["a) Visualize raw data", "b) Clean and transform raw data", "c) Deploy models", "d) Write papers"], "b)"),
   ("Example of structured data?",
    ["a) Text document", "b) Relational database table", "c) Social media post", "d) Video file"], "b)"),
   ("Three V's of Big Data?",
    ["a) Volume, Variety, Velocity", "b) Value, Verification, Version", "c) Volume, Vector, Velocity", "d) Variety, Validity, Volume"], "a)"),
   ("Which role builds and deploys ML models?",
    ["a) Data Engineer", "b) Data Analyst", "c) ML Engineer", "d) Business Analyst"], "c)"),
   ("Common tool for version control?",
    ["a) Jupyter Notebook", "b) Git", "c) Excel", "d) Tableau"], "b)"),
   ("Best describes supervised learning?",
    ["a) Learning without labels", "b) Learning from labeled data", "c) Trial and error", "d) Clustering"], "b)"),
   ("Main goal of data visualization?",
    ["a) Make data attractive", "b) Communicate insights", "c) Store data", "d) Replace statistics"], "b)"),
]
ch01_mc_b = [
   ("What is a data warehouse?",
    ["a) Physical storage for servers", "b) Central repository for integrated data", "c) A database index", "d) A visualization tool"], "b)"),
   ("Which Python library is used for numerical computing?",
    ["a) Django", "b) NumPy", "c) Flask", "d) BeautifulSoup"], "b)"),
   ("What does ETL stand for?",
    ["a) Extract, Transform, Load", "b) Evaluate, Test, Launch", "c) Execute, Trace, Log", "d) Extract, Train, Learn"], "a)"),
   ("Which is a classification algorithm?",
    ["a) K-Means", "b) Linear Regression", "c) Decision Tree", "d) PCA"], "c)"),
   ("What is overfitting?",
    ["a) Poor training performance", "b) Memorizes training data, fails on new data", "c) Trains too quickly", "d) Uses too many features"], "b)"),
   ("Metric for regression evaluation?",
    ["a) Accuracy", "b) Precision", "c) Mean Squared Error", "d) F1 Score"], "c)"),
   ("What is a confusion matrix?",
    ["a) Matrix for data storage", "b) Table for classification evaluation", "c) Regression model", "d) Cleaning technique"], "b)"),
   ("Purpose of train-test split?",
    ["a) Speed up training", "b) Evaluate model on unseen data", "c) Reduce dataset size", "d) Visualize data"], "b)"),
   ("What is cross-validation?",
    ["a) Training on multiple datasets", "b) Assess model generalizability", "c) Combining multiple models", "d) Validating data types"], "b)"),
   ("Unsupervised learning algorithm?",
    ["a) Logistic Regression", "b) SVM", "c) K-Means", "d) Random Forest"], "c)"),
]
ch01_ma = [
   (["Descriptive Analytics", "Predictive Analytics", "Prescriptive Analytics"],
    ["Recommends actions based on data", "Summarizes historical data", "Forecasts future trends"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Data Collection", "Data Cleaning", "Model Evaluation"],
    ["Assessing model performance using metrics", "Gathering raw data from various sources", "Removing inconsistencies"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Categorical Data", "Numerical Data", "Ordinal Data"],
    ["Data with ordered categories", "Data representing groups or labels", "Data representing measurable quantities"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Mean", "Median", "Standard Deviation"],
    ["Middle value of sorted dataset", "Average of all data points", "Measure of data spread"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["Classification", "Regression", "Clustering"],
    ["Predicting continuous numerical value", "Grouping similar data points", "Predicting categorical label"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["Accuracy", "Precision", "Recall"],
    ["Proportion of positives correctly predicted", "Proportion of correct predictions", "Proportion of actual positives identified"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Jupyter Notebook", "GitHub", "Tableau"],
    ["Version control platform", "Interactive computing environment", "Data visualization and BI tool"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["Training Data", "Test Data", "Validation Data"],
    ["Used to tune model hyperparameters", "Used to train the model", "Used to evaluate final performance"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Underfitting", "Overfitting", "Good Fit"],
    ["Model too complex, memorizes noise", "Captures pattern well", "Model too simple, misses patterns"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["CRISP-DM", "SEMMA", "KDD"],
    ["Knowledge Discovery in Databases process", "Cross-Industry Standard Process for DM", "Sample, Explore, Modify, Model, Assess"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
]

# ===================== CHAPTER 02 =====================
ch02_sources = [
    "[[2.1. Managing Python Environments and Package Managers]]",
    "[[2.2. Exercise 1. Hospital Patient Data Analysis Setup]]",
]
ch02_tf_a = [
    ("Virtual environments isolate Python project dependencies.", "True"),
    ("Conda is exclusively a package manager and cannot manage environments.", "False"),
    ("The requirements.txt file lists all project dependencies.", "True"),
    ("Pip installs packages globally by default without an active virtual environment.", "True"),
    ("Conda environments cannot be exported to YAML files.", "False"),
    ("Jupyter Notebooks require a separate Python environment from system Python.", "False"),
    ("The 'pip freeze' command outputs installed packages in requirements format.", "True"),
    ("Anaconda distribution includes pre-installed data science packages.", "True"),
    ("Virtual environments are not recommended for collaborative projects.", "False"),
    ("Python virtual environments can be created using the 'venv' module.", "True"),
]
ch02_tf_b = [
    ("Pip is only available on Linux operating systems.", "False"),
    ("The 'conda update' command updates Conda itself.", "True"),
    ("Virtual environments consume significantly more disk space than global installs.", "False"),
    ("A requirements.txt file can specify exact package versions using the == operator.", "True"),
    ("Conda environments can use different Python versions.", "True"),
    ("The pipenv tool combines pip and virtualenv functionality.", "True"),
    ("Python packages can only be installed from PyPI.", "False"),
    ("Activating a virtual environment changes the PATH variable.", "True"),
    ("The --user flag installs packages for all users on the system.", "False"),
    ("Environment variables set in a virtual environment persist after deactivation.", "False"),
]
ch02_mc_a = [
   ("Which command creates a virtual environment named 'myenv'?",
    ["a) python -m venv myenv", "b) virtualenv create myenv", "c) env new myenv", "d) python create myenv"], "a)"),
   ("What file format does Conda use to export environments?",
    ["a) requirements.txt", "b) environment.yml", "c) config.json", "d) env.yaml"], "b)"),
   ("Which command activates a virtual environment on Linux?",
    ["a) activate myenv", "b) source myenv/bin/activate", "c) start myenv", "d) run myenv"], "b)"),
   ("Purpose of a package manager in Python?",
    ["a) Manage Python versions", "b) Install and manage third-party libraries", "c) Compile Python code", "d) Create GUIs"], "b)"),
   ("Which package manager is included with Python by default?",
    ["a) Conda", "b) Pip", "c) npm", "d) Homebrew"], "b)"),
   ("What does 'pip install -r requirements.txt' do?",
    ["a) Installs requests library", "b) Installs all packages listed", "c) Removes listed packages", "d) Updates all packages"], "b)"),
   ("Benefit of virtual environments?",
    ["a) Faster execution", "b) Dependency isolation", "c) Auto code formatting", "d) Built-in version control"], "b)"),
   ("How to deactivate a virtual environment?",
    ["a) exit", "b) deactivate", "c) stop", "d) close"], "b)"),
   ("Conda command to create env with Python 3.9?",
    ["a) conda new -n myenv python=3.9", "b) conda create -n myenv python=3.9", "c) conda init -n myenv python=3.9", "d) conda build -n myenv python=3.9"], "b)"),
   ("Conda env specification file extension?",
    ["a) .txt", "b) .yml", "c) .env", "d) .cfg"], "b)"),
]
ch02_mc_b = [
   ("Which command lists all installed packages in the current environment?",
    ["a) pip list", "b) pip show", "c) pip display", "d) pip packages"], "a)"),
   ("What does 'conda update --all' do?",
    ["a) Updates Conda only", "b) Updates all packages in environment", "c) Removes all packages", "d) Updates Python version"], "b)"),
   ("Which file is used by pipenv for dependency management?",
    ["a) Pipfile", "b) Pipenv.txt", "c) requirements.pip", "d) env.json"], "a)"),
   ("Purpose of anaconda-navigator?",
    ["a) GUI for managing Conda environments", "b) Python code editor", "c) Version control system", "d) Data visualization tool"], "a)"),
   ("What does 'pip show numpy' display?",
    ["a) Removes numpy", "b) Shows numpy package details", "c) Installs latest numpy", "d) Updates numpy"], "b)"),
   ("Where are global Python packages stored on Linux?",
    ["a) ~/packages/", "b) /usr/lib/python3/dist-packages/", "c) /opt/python/", "d) /etc/python/"], "b)"),
   ("Which tool combines pip and virtualenv?",
    ["a) Conda", "b) Pipenv", "c) Poetry", "d) Venv"], "b)"),
   ("What does 'conda info --envs' do?",
    ["a) Shows current env details", "b) Lists all Conda environments", "c) Creates a new environment", "d) Deletes an environment"], "b)"),
   ("Purpose of a .gitignore file in data science projects?",
    ["a) Track dependencies", "b) Exclude files from version control", "c) Configure Python path", "d) Set environment variables"], "b)"),
   ("How to install a specific package version with pip?",
    ["a) pip install numpy==1.21.0", "b) pip install numpy@1.21.0", "c) pip install numpy-1.21.0", "d) pip install numpy[1.21.0]"], "a)"),
]
ch02_ma = [
   (["pip install numpy", "pip freeze", "pip uninstall pandas"],
    ["Removes the pandas package", "Installs the numpy package", "Lists all installed packages"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["conda create", "conda activate", "conda list"],
    ["Shows installed packages", "Creates a new Conda environment", "Activates a Conda environment"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["requirements.txt", "environment.yml", "Pipfile"],
    ["Pipenv dependency file", "Conda environment file", "Pip requirements file"],
    "a) -> c)\nb) -> b)\nc) -> a)"),
   (["Virtual Environment", "Global Installation", "Conda Environment"],
    ["System-wide package installs", "Cross-platform env manager", "Isolated project dependencies"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["pip install", "pip uninstall", "pip freeze"],
    ["Outputs installed package list", "Installs a Python package", "Removes a Python package"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["venv", "virtualenv", "pipenv"],
    ["Python 3 built-in env module", "Third-party env tool", "Package and env manager"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["Anaconda", "Miniconda", "Miniforge"],
    ["Minimal Conda installer", "Full distribution with many packages", "Community-maintained Conda distribution"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["--user flag", "--no-deps flag", "--quiet flag"],
    ["Suppresses output messages", "Installs for current user only", "Skips installing dependencies"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["__init__.py", "setup.py", "setup.cfg"],
    ["Package distribution config file", "Marks directory as Python package", "Package metadata file"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["import module", "from module import", "import module as"],
    ["Imports specific attributes", "Imports with an alias", "Imports entire module"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
]

# ===================== CHAPTER 03 =====================
ch03_sources = [
    "[[3.1. Python Essentials and Data Structures]]",
    "[[3.2. Object Oriented Programming in Python]]",
    "[[3.3. Advanced Control Flow, Iterators, and Exception Handling]]",
    "[[3.4. Code Modularity and Packaging]]",
    "[[3.5. Tutorial 3. Step by Step Exercise Implementations]]",
    "[[3.6. Exercise 6. Processing One Million Records without Memory Explosion]]",
]
ch03_tf_a = [
    ("Python lists are mutable data structures.", "True"),
    ("Tuples can be modified after creation.", "False"),
    ("A dictionary stores key-value pairs.", "True"),
    ("Inheritance allows a class to use methods from another class.", "True"),
    ("A try block must always be followed by a finally block.", "False"),
    ("Generators use the 'yield' keyword.", "True"),
    ("Python sets maintain insertion order.", "False"),
    ("A decorator is a function that modifies another function.", "True"),
    ("Lambda functions can contain multiple statements.", "False"),
    ("List comprehensions provide a concise way to create lists.", "True"),
]
ch03_tf_b = [
    ("Python strings are immutable.", "True"),
    ("The 'pass' statement is used as a placeholder.", "True"),
    ("Global variables can be modified inside a function without the global keyword.", "False"),
    ("A static method can access class instance variables.", "False"),
    ("The __str__ method returns a string representation of an object.", "True"),
    ("Exception handling allows graceful error recovery.", "True"),
    ("The 'zip' function pairs elements from multiple iterables.", "True"),
    ("Recursion always requires a base case to terminate.", "True"),
    ("Python uses indentation to define code blocks.", "True"),
    ("The 'else' clause in a loop executes only if the loop completes without break.", "True"),
]
ch03_mc_a = [
   ("Which data structure is immutable in Python?",
    ["a) List", "b) Dictionary", "c) Tuple", "d) Set"], "c)"),
   ("Keyword to define a class?",
    ["a) struct", "b) class", "c) object", "d) define"], "b)"),
   ("Exception handling construct in Python?",
    ["a) try-except", "b) catch-throw", "c) handle-error", "d) try-catch"], "a)"),
   ("Output of 'len([1,2,[3,4]])'?",
    ["a) 3", "b) 4", "c) 5", "d) 2"], "a)"),
   ("Method called when an object is created?",
    ["a) __init__", "b) __new__", "c) __create__", "d) __start__"], "a)"),
   ("What does 'self' represent in a class?",
    ["a) The class itself", "b) Current instance of class", "c) Static reference", "d) The parent class"], "b)"),
   ("Python iterator protocol methods?",
    ["a) __iter__", "b) __loop__", "c) __next__", "d) Both __iter__ and __next__"], "d)"),
   ("Purpose of 'with' statement?",
    ["a) Import modules", "b) Resource management via context managers", "c) Define conditionals", "d) Create loops"], "b)"),
   ("Exit a loop prematurely?",
    ["a) exit", "b) stop", "c) break", "d) return"], "c)"),
   ("What does map() return in Python 3?",
    ["a) A list", "b) A tuple", "c) An iterator", "d) A dictionary"], "c)"),
]
ch03_mc_b = [
   ("What is a Python generator?",
    ["a) A function that returns a list", "b) An iterator using yield", "c) A type of exception", "d) A class method"], "b)"),
   ("What does the 'is' operator compare?",
    ["a) Values", "b) Object identity", "c) Types", "d) Lengths"], "b)"),
   ("How to open a file for reading?",
    ["a) open('file.txt', 'r')", "b) open('file.txt', 'w')", "c) open('file.txt', 'a')", "d) open('file.txt', 'x')"], "a)"),
   ("What is a decorator syntax?",
    ["a) @decorator", "b) #decorator", "c) $decorator", "d) &decorator"], "a)"),
   ("What does super() do?",
    ["a) Calls parent class method", "b) Creates a super object", "c) Overrides a method", "d) Deletes an attribute"], "a)"),
   ("Which loop is used with iterators?",
    ["a) for loop", "b) while loop", "c) do-while", "d) repeat loop"], "a)"),
   ("What is pickling in Python?",
    ["a) Sorting data", "b) Serializing objects", "c) Encrypting data", "d) Compressing files"], "b)"),
   ("What does *args represent?",
    ["a) Keyword arguments", "b) Variable positional arguments", "c) Default arguments", "d) Required arguments"], "b)"),
   ("What does **kwargs represent?",
    ["a) Positional arguments", "b) Variable keyword arguments", "c) Default keyword args", "d) Required keyword args"], "b)"),
   ("Which module provides random number functions?",
    ["a) math", "b) random", "c) statistics", "d) sys"], "b)"),
]
ch03_ma = [
   (["list", "tuple", "set"],
    ["Immutable ordered collection", "Mutable unordered unique elements", "Mutable ordered collection"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["__init__", "__str__", "__len__"],
    ["Returns object length", "Initializes object instance", "Returns string representation"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Inheritance", "Polymorphism", "Encapsulation"],
    ["Restricts direct data access", "Allows using methods from another class", "Treats objects of different classes as common superclass"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["try", "except", "finally"],
    ["Executes regardless of exceptions", "Defines block to test for errors", "Handles exception if occurs"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["List Comprehension", "Dictionary Comprehension", "Generator Expression"],
    ["Creates generator object lazily", "Creates list concisely", "Creates dictionary concisely"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["@staticmethod", "@classmethod", "@property"],
    ["Method receiving cls instead of self", "Method that does not receive self or cls", "Makes method accessible like an attribute"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["append()", "extend()", "insert()"],
    ["Adds element at specific index", "Adds element to end of list", "Adds all elements from iterable"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["keys()", "values()", "items()"],
    ["Returns all dictionary keys", "Returns all dictionary key-value pairs", "Returns all dictionary values"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["raise", "assert", "import"],
    ["Includes module in current namespace", "Raises an exception intentionally", "Checks condition and raises AssertionError"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["open()", "read()", "write()"],
    ["Reads content from file", "Writes content to file", "Opens a file and returns file object"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
]

# ===================== CHAPTER 04 =====================
ch04_sources = [
    "[[4.1. NumPy Deep Dive]]",
    "[[4.2. Pandas Data Manipulation Framework]]",
    "[[4.3. Data Visualization Frameworks]]",
    "[[4.4. Tutorial 4. NumPy Temperature and Student Grades Solutions]]",
    "[[4.5. Tutorial 4. Hospital Pandas and Visualization Solutions]]",
    "[[4.6. Tutorial 4 Project. Monthly Sales Analysis Solution]]",
]
ch04_tf_a = [
    ("NumPy arrays are homogeneous in data type.", "True"),
    ("Pandas Series can hold multiple data types in a single column.", "False"),
    ("Matplotlib is a data visualization library for Python.", "True"),
    ("A DataFrame in Pandas is immutable after creation.", "False"),
    ("NumPy broadcasting allows operations on arrays of different shapes.", "True"),
    ("The loc accessor in Pandas uses integer-based indexing.", "False"),
    ("Seaborn is built on top of Matplotlib.", "True"),
    ("Missing values in Pandas are represented as NaN.", "True"),
    ("NumPy supports native GPU acceleration.", "False"),
    ("The groupby operation in Pandas follows a split-apply-combine pattern.", "True"),
]
ch04_tf_b = [
    ("Pandas can read CSV files directly.", "True"),
    ("The iloc accessor uses label-based indexing.", "False"),
    ("Vectorization in NumPy is faster than Python loops.", "True"),
    ("A Pandas DataFrame is a 1-dimensional labeled array.", "False"),
    ("Histograms are used for visualizing the distribution of numerical data.", "True"),
    ("The apply() function in Pandas applies a function along an axis.", "True"),
    ("NumPy arrays have a fixed size upon creation.", "True"),
    ("Seaborn automatically handles statistical transformations.", "True"),
    ("A box plot shows the distribution of data based on quartiles.", "True"),
    ("Pandas merge() performs SQL-like joins on DataFrames.", "True"),
]
ch04_mc_a = [
   ("How to create a NumPy array from a list?",
    ["a) np.array(list)", "b) np.from_list(list)", "c) np.create(list)", "d) np.make(list)"], "a)"),
   ("Which Pandas function reads a CSV file?",
    ["a) pd.read_csv()", "b) pd.load_csv()", "c) pd.import_csv()", "d) pd.open_csv()"], "a)"),
   ("Attribute of NumPy array for shape?",
    ["a) .size", "b) .shape", "c) .dims", "d) .len"], "b)"),
   ("What does df.head() return?",
    ["a) Last 5 rows", "b) First 5 rows", "c) Random 5 rows", "d) First 5 columns"], "b)"),
   ("Which library is used for statistical data visualization?",
    ["a) NumPy", "b) Seaborn", "c) Pandas", "d) SciPy"], "b)"),
   ("Pandas function to check for missing values?",
    ["a) df.missing()", "b) df.isna()", "c) df.null()", "d) df.empty()"], "b)"),
   ("What is the default NumPy data type for integers?",
    ["a) int32", "b) int64", "c) int16", "d) int8"], "b)"),
   ("Which plot type displays data as rectangular bars?",
    ["a) Scatter plot", "b) Bar plot", "c) Line plot", "d) Histogram"], "b)"),
   ("What does df.describe() provide?",
    ["a) Data types", "b) Statistical summary", "c) Missing values count", "d) Column names"], "b)"),
   ("NumPy function for linear space between values?",
    ["a) np.arange()", "b) np.linspace()", "c) np.logspace()", "d) np.space()"], "b)"),
]
ch04_mc_b = [
   ("What is the purpose of plt.figure()?",
    ["a) Save a figure", "b) Create a new figure", "c) Close a figure", "d) Show a figure"], "b)"),
   ("How to select a single column in Pandas?",
    ["a) df['col']", "b) df.col", "c) Both a and b", "d) df[0]"], "c)"),
   ("Which NumPy function creates an array of zeros?",
    ["a) np.zeros()", "b) np.empty()", "c) np.ones()", "d) np.null()"], "a)"),
   ("What does df.dropna() do?",
    ["a) Fills missing values", "b) Drops rows with missing values", "c) Drops duplicate rows", "d) Drops specified columns"], "b)"),
   ("Which matplotlib function creates a scatter plot?",
    ["a) plt.plot()", "b) plt.scatter()", "c) plt.bar()", "d) plt.hist()"], "b)"),
   ("Pandas function to concatenate DataFrames?",
    ["a) pd.concat()", "b) pd.join()", "c) pd.merge()", "d) pd.append()"], "a)"),
   ("NumPy attribute for data type of array?",
    ["a) .dtype", "b) .type", "c) .datatype", "d) .kind"], "a)"),
   ("What does df.groupby('col').mean() compute?",
    ["a) Global mean", "b) Group-wise means", "c) Running mean", "d) Weighted mean"], "b)"),
   ("Which method creates a pivot table in Pandas?",
    ["a) df.pivot_table()", "b) df.pivot()", "c) df.crosstab()", "d) df.table()"], "a)"),
   ("Purpose of plt.tight_layout()?",
    ["a) Adjust subplot parameters", "b) Auto-adjust padding between subplots", "c) Set figure size", "d) Save figure"], "b)"),
]
ch04_ma = [
   (["np.array()", "np.zeros()", "np.ones()"],
    ["Creates array of all ones", "Creates array from list", "Creates array of all zeros"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["df.head()", "df.info()", "df.describe()"],
    ["Statistical summary of data", "Returns first few rows", "Data types and memory usage"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Matplotlib", "Seaborn", "Plotly"],
    ["Interactive web-based visualizations", "Publication-quality static plots", "Statistical data visualization"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["loc", "iloc", "ix"],
    ["Integer position-based indexing", "Mixed label/position indexing (deprecated)", "Label-based indexing"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["mean()", "median()", "std()"],
    ["Standard deviation", "Average of values", "Middle value of sorted data"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Line Plot", "Bar Plot", "Scatter Plot"],
    ["Relationship between two variables", "Trend over continuous interval", "Comparing categories"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["merge()", "join()", "concat()"],
    ["Index-based joining", "Column-based SQL-like joining", "Stacks DataFrames along axis"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["fillna()", "dropna()", "interpolate()"],
    ["Removes rows with missing values", "Fills missing values", "Estimates missing values"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["ndim", "size", "itemsize"],
    ["Total number of elements", "Number of dimensions", "Byte size of each element"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["plt.title()", "plt.xlabel()", "plt.legend()"],
    ["Sets label for x-axis", "Sets plot title", "Shows legend on plot"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
]

# ===================== CHAPTER 05 =====================
ch05_sources = [
    "[[5.1. Handling Missing Data]]",
    "[[5.2. Data Consistency and Outlier Treatment]]",
    "[[5.3. Text Cleaning and Categorical Encoding]]",
    "[[5.4. Feature Scaling and Normalization]]",
    "[[5.5. Tutorial 5. Medical Dataset Preprocessing Walkthrough]]",
    "[[5.6. Tutorial 5 Project. Titanic Data Pipeline and Modeling]]",
]
ch05_tf_a = [
    ("Missing data can be handled by removing rows with null values.", "True"),
    ("Mean imputation replaces missing values with the median.", "False"),
    ("One-hot encoding creates binary columns for categorical variables.", "True"),
    ("Standardization assumes data follows a normal distribution.", "False"),
    ("Outliers can negatively impact model performance.", "True"),
    ("Label encoding assigns ordinal values to categories.", "True"),
    ("Min-max scaling transforms data to a fixed range, typically [0,1].", "True"),
    ("Duplicate rows should always be removed from a dataset.", "False"),
    ("Z-score measures how many standard deviations a point is from the mean.", "True"),
    ("Text cleaning involves removing stop words and punctuation.", "True"),
]
ch05_tf_b = [
    ("Feature scaling is unnecessary for tree-based models.", "True"),
    ("Imputation always improves model accuracy.", "False"),
    ("Outliers can be detected using IQR (Interquartile Range).", "True"),
    ("Ordinal encoding preserves the order of categories.", "True"),
    ("Regex can be used to clean text data.", "True"),
    ("Standardization centers data around zero with unit variance.", "True"),
    ("Categorical variables with high cardinality can cause dimensionality issues.", "True"),
    ("Data leakage occurs when information from the test set influences training.", "True"),
    ("Stemming reduces words to their root form.", "True"),
    ("Missing Completely at Random (MCAR) means missingness depends on other variables.", "False"),
]
ch05_mc_a = [
   ("Which technique is used to handle missing categorical data?",
    ["a) Mean imputation", "b) Mode imputation", "c) Standardization", "d) Scaling"], "b)"),
   ("What is the IQR used for?",
    ["a) Feature scaling", "b) Outlier detection", "c) Encoding categories", "d) Text cleaning"], "b)"),
   ("Which encoding creates binary columns?",
    ["a) Label encoding", "b) One-hot encoding", "c) Ordinal encoding", "d) Frequency encoding"], "b)"),
   ("What does StandardScaler do?",
    ["a) Scales to [0,1] range", "b) Centers to mean=0, std=1", "c) Log transforms data", "d) Removes outliers"], "b)"),
   ("How to detect outliers using Z-score?",
    ["a) Points with |z| > 3", "b) Points with z = 0", "c) Points with z < 0", "d) Points with any z-score"], "a)"),
   ("What is data imputation?",
    ["a) Removing missing data", "b) Replacing missing data with estimated values", "c) Scaling features", "d) Encoding categories"], "b)"),
   ("MinMaxScaler transforms features to which range?",
    ["a) [-1, 1]", "b) [0, 1]", "c) [0, 100]", "d) No fixed range"], "b)"),
   ("What is label encoding?",
    ["a) Creating binary columns", "b) Assigning integers to categories", "c) Scaling numerical features", "d) Removing duplicates"], "b)"),
   ("Which of the following is NOT a type of missing data?",
    ["a) MCAR", "b) MAR", "c) MNAR", "d) MCR"], "d)"),
   ("What is the purpose of feature scaling?",
    ["a) Remove outliers", "b) Bring features to similar scale", "c) Reduce dimensionality", "d) Handle missing values"], "b)"),
]
ch05_mc_b = [
   ("Which method is robust to outliers for scaling?",
    ["a) StandardScaler", "b) RobustScaler", "c) MinMaxScaler", "d) Normalizer"], "b)"),
   ("What does tokenization do in text preprocessing?",
    ["a) Removes punctuation", "b) Splits text into tokens", "c) Converts to lowercase", "d) Stems words"], "b)"),
   ("Which technique handles high cardinality categorical features?",
    ["a) One-hot encoding", "b) Target encoding", "c) Label encoding", "d) Ordinal encoding"], "b)"),
   ("What is the purpose of data validation?",
    ["a) Ensure data quality and consistency", "b) Scale features", "c) Train models", "d) Visualize data"], "a)"),
   ("Which is a univariate outlier detection method?",
    ["a) Isolation Forest", "b) Z-score method", "c) LOF", "d) DBSCAN"], "b)"),
   ("What does lemmatization do?",
    ["a) Removes suffixes to get root word", "b) Converts words to their dictionary form", "c) Removes stop words", "d) Tokenizes text"], "b)"),
   ("Pandas function to check for duplicates?",
    ["a) df.duplicated()", "b) df.repeated()", "c) df.double()", "d) df.unique()"], "a)"),
   ("What is the difference between fit and transform?",
    ["a) No difference", "b) fit learns parameters, transform applies them", "c) transform learns, fit applies", "d) Both do the same"], "b)"),
   ("What does RobustScaler use for scaling?",
    ["a) Mean and std", "b) Median and IQR", "c) Min and max", "d) Mode and range"], "b)"),
   ("Which encoding is suitable for ordinal data?",
    ["a) One-hot encoding", "b) Ordinal encoding", "c) Binary encoding", "d) Hash encoding"], "b)"),
]
ch05_ma = [
   (["Mean Imputation", "Median Imputation", "Mode Imputation"],
    ["Used for categorical data", "Used for numerical data with outliers", "Used for numerical data without outliers"],
    "a) -> c)\nb) -> b)\nc) -> a)"),
   (["Z-score", "IQR Method", "Isolation Forest"],
    ["Detects outliers using quartiles", "Machine learning outlier detection", "Detects outliers using standard deviations"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["One-hot Encoding", "Label Encoding", "Target Encoding"],
    ["Assigns integers to categories", "Creates binary columns per category", "Replaces category with mean target value"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["StandardScaler", "MinMaxScaler", "RobustScaler"],
    ["Scales using median and IQR", "Scales to fixed range [0,1]", "Centers to mean=0, std=1"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["MCAR", "MAR", "MNAR"],
    ["Missing depends on other observed data", "Missing not at random (systematic)", "Missing completely at random"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["Stemming", "Lemmatization", "Tokenization"],
    ["Reduces to dictionary base word", "Splits text into units", "Reduces to root by chopping suffixes"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["dropna()", "fillna()", "interpolate()"],
    ["Estimates and fills missing values", "Removes rows with NaN", "Fills NaN with specified value"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["fit()", "transform()", "fit_transform()"],
    ["Applies learned parameters to data", "Learns parameters from data", "Both learns and applies in one step"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["Upper case", "Lower case", "Sentence case"],
    ["Standard for text normalization", "Used for proper nouns", "Used for emphasis"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["Regex", "Stop word removal", "Punctuation removal"],
    ["Removes common unimportant words", "Uses patterns to find and replace text", "Removes characters like . , ! ?"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
]

# ===================== CHAPTER 06 =====================
ch06_sources = [
    "[[6.1. Exploratory Data Analysis Principles]]",
]
ch06_tf_a = [
    ("EDA is performed before formal modeling.", "True"),
    ("A histogram shows the relationship between two variables.", "False"),
    ("Correlation measures the strength of a linear relationship.", "True"),
    ("A box plot visualizes data distribution using quartiles.", "True"),
    ("Skewness measures the asymmetry of a distribution.", "True"),
    ("A scatter plot is useful for visualizing bivariate relationships.", "True"),
    ("Kurtosis describes the tailedness of a probability distribution.", "True"),
    ("A bar chart is suitable for categorical data.", "True"),
    ("Correlation implies causation.", "False"),
    ("Missing values should always be ignored during EDA.", "False"),
]
ch06_tf_b = [
    ("A pair plot shows pairwise relationships in a dataset.", "True"),
    ("Outliers can be easily identified in a box plot.", "True"),
    ("The correlation coefficient ranges between -1 and 1.", "True"),
    ("A heatmap is useful for visualizing correlation matrices.", "True"),
    ("Univariate analysis examines one variable at a time.", "True"),
    ("A count plot is used for numerical continuous data.", "False"),
    ("PCA is a dimensionality reduction technique used in EDA.", "True"),
    ("Data can have both positive and negative skewness.", "True"),
    ("A violin plot combines box plot and KDE.", "True"),
    ("EDA should be conducted without any prior hypotheses.", "True"),
]
ch06_mc_a = [
   ("Which plot shows the distribution of a single numerical variable?",
    ["a) Scatter plot", "b) Histogram", "c) Bar chart", "d) Heatmap"], "b)"),
   ("What does a correlation coefficient of 0 indicate?",
    ["a) Strong positive correlation", "b) No linear correlation", "c) Strong negative correlation", "d) Perfect correlation"], "b)"),
   ("Which plot is best for comparing categories?",
    ["a) Histogram", "b) Bar chart", "c) Line chart", "d) Box plot"], "b)"),
   ("What does a box plot whisker represent?",
    ["a) Minimum and maximum", "b) Typically 1.5 * IQR from quartiles", "c) Standard deviations", "d) Mean values"], "b)"),
   ("What is the purpose of a Q-Q plot?",
    ["a) Check normality", "b) Check correlation", "c) Check missing values", "d) Check outliers"], "a)"),
   ("Which measure describes the spread of data?",
    ["a) Mean", "b) Standard deviation", "c) Mode", "d) Median"], "b)"),
   ("What does a high kurtosis value indicate?",
    ["a) Normal distribution", "b) Heavy tails with outliers", "c) Uniform distribution", "d) Symmetric distribution"], "b)"),
   ("Which plot is best for time series data?",
    ["a) Bar chart", "b) Line plot", "c) Scatter plot", "d) Pie chart"], "b)"),
   ("What does a heatmap display?",
    ["a) Data distribution", "b) Matrix values as colors", "c) Time trends", "d) Category counts"], "b)"),
   ("Which EDA technique reduces dimensionality?",
    ["a) PCA", "b) K-Means", "c) Linear Regression", "d) Decision Tree"], "a)"),
]
ch06_mc_b = [
   ("What does a violin plot show?",
    ["a) Only box plot statistics", "b) Distribution + box plot combined", "c) Only density estimation", "d) Only outliers"], "b)"),
   ("Which value indicates perfect positive correlation?",
    ["a) -1", "b) 0", "c) 1", "d) 0.5"], "c)"),
   ("What is the purpose of univariate analysis?",
    ["a) Analyze relationships between variables", "b) Analyze single variable distribution", "c) Group similar data points", "d) Predict outcomes"], "b)"),
   ("What does a pair plot create?",
    ["a) Single plot", "b) Grid of scatter plots for all variable pairs", "c) Time series plot", "d) 3D plot"], "b)"),
   ("Which plot is suitable for checking outliers?",
    ["a) Histogram", "b) Box plot", "c) Line chart", "d) Heatmap"], "b)"),
   ("What does skewness measure?",
    ["a) Spread of data", "b) Asymmetry of distribution", "c) Central tendency", "d) Correlation"], "b)"),
   ("Which library is commonly used for EDA visualization?",
    ["a) NumPy", "b) Seaborn", "c) Pandas", "d) Scikit-learn"], "b)"),
   ("What does a count plot show?",
    ["a) Count of numerical values", "b) Count of categorical observations", "c) Correlation counts", "d) Missing value counts"], "b)"),
   ("What is the purpose of a joint plot?",
    ["a) Single variable distribution", "b) Bivariate + univariate distributions", "c) Multivariate relationships", "d) Time series analysis"], "b)"),
   ("Which plot is best for showing the distribution of categorical data?",
    ["a) Histogram", "b) Pie chart", "c) Scatter plot", "d) Line chart"], "b)"),
]
ch06_ma = [
   (["Histogram", "Box Plot", "Scatter Plot"],
    ["Shows bivariate relationship", "Shows distribution using quartiles", "Shows univariate distribution"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["Mean", "Median", "Mode"],
    ["Most frequent value", "Average of values", "Middle value of sorted data"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Positive Skew", "Negative Skew", "No Skew"],
    ["Tail extends to the left", "Tail extends to the right", "Symmetric distribution"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["Pearson Correlation", "Spearman Correlation", "Kendall Correlation"],
    ["Non-parametric rank correlation", "Measures monotonic relationship", "Measures linear relationship"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["Variance", "Standard Deviation", "Range"],
    ["Square root of variance", "Difference between max and min", "Average squared deviation from mean"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["KDE Plot", "Violin Plot", "Rug Plot"],
    ["Box plot + KDE combined", "Marks individual data points", "Smooth density estimation"],
    "a) -> c)\nb) -> a)\nc) -> b)"),
   (["Heatmap", "Pair Plot", "Joint Plot"],
    ["Grid of scatter plots", "Matrix values as colors", "Bivariate + marginal distributions"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
   (["plt.hist()", "plt.boxplot()", "plt.scatter()"],
    ["Creates a scatter plot", "Creates a histogram", "Creates a box plot"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["Categorical", "Numerical", "Ordinal"],
    ["Data with order (rankings)", "Data representing labels or groups", "Measurable quantities"],
    "a) -> b)\nb) -> c)\nc) -> a)"),
   (["df.corr()", "df.cov()", "df.describe()"],
    ["Computes covariance matrix", "Computes correlation matrix", "Statistical summary of data"],
    "a) -> b)\nb) -> a)\nc) -> c)"),
]

# ===================== GENERATE ALL FILES =====================
BASE = "Quiz"

chapters_config = [
    ("Chapter 01", ch01_sources, ch01_tf_a, ch01_tf_b, ch01_mc_a, ch01_mc_b, ch01_ma, ch01_ma),
    ("Chapter 02", ch02_sources, ch02_tf_a, ch02_tf_b, ch02_mc_a, ch02_mc_b, ch02_ma, ch02_ma),
    ("Chapter 03", ch03_sources, ch03_tf_a, ch03_tf_b, ch03_mc_a, ch03_mc_b, ch03_ma, ch03_ma),
    ("Chapter 04", ch04_sources, ch04_tf_a, ch04_tf_b, ch04_mc_a, ch04_mc_b, ch04_ma, ch04_ma),
    ("Chapter 05", ch05_sources, ch05_tf_a, ch05_tf_b, ch05_mc_a, ch05_mc_b, ch05_ma, ch05_ma),
    ("Chapter 06", ch06_sources, ch06_tf_a, ch06_tf_b, ch06_mc_a, ch06_mc_b, ch06_ma, ch06_ma),
]

for label, srcs, tf_a, tf_b, mc_a, mc_b, ma_all, _ in chapters_config:
    ch_dir = os.path.join(BASE, label)
    print(f"Generating {label}...")
    # For both Quiz_A and Quiz_B use the same matching data (10 items each, split 5+5 can work but we use full 10)
    # We split: Quiz_A gets first 5 matching, Quiz_B gets last 5 matching
    write_quiz(ch_dir, "Quiz_A.md", srcs, tf_a, mc_a, ma_all[:5])
    write_quiz(ch_dir, "Quiz_B.md", srcs, tf_b, mc_b, ma_all[5:])

print("\n=== All quiz files generated successfully! ===")