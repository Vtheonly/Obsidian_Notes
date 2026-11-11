
# Lab 3: Data Cleaning, Normalization, and Encoding - Solution Guide

This guide provides a detailed walkthrough for completing the "Apprentissage Automatique" Lab 3. The objective is to take a raw, messy dataset (`students.csv`) and prepare it for a machine learning model by performing essential preprocessing steps.

### Project Structure
```
/your-project-folder
|-- venv/                  # Your Python virtual environment
|-- students.csv           # The dataset file
|-- lab3_solution.ipynb    # The Jupyter Notebook with the solution
|-- README.md              # This guide
```

### **What To Do and What Not To Do: A Step-by-Step Walkthrough**

The lab requires us to address several common data quality issues. We will tackle them in a logical order.

#### Step 1: Setup and Data Loading
- **DO:** Import necessary libraries like `pandas` and `numpy`.
- **DO:** Load the `students.csv` dataset into a pandas DataFrame.
- **DO:** Use `df.head()` to inspect the first few rows and `df.info()` to get a summary of the data types and non-null values. This initial inspection is crucial for understanding what problems exist.

#### Step 2: Data Cleaning

This is the most critical part, where we fix the "dirty" data.

**A. Handling Duplicates**
- **The Problem:** The dataset contains completely identical rows. These can bias a machine learning model, giving more weight to the duplicated samples.
- **What To Do:**
    1.  Use `df.duplicated().sum()` to count how many duplicate rows exist.
    2.  Use `df.drop_duplicates(inplace=True)` to remove them permanently from our DataFrame. The `inplace=True` argument modifies the DataFrame directly, saving us from having to reassign it (e.g., `df = df.drop_duplicates()`).
- **What Not To Do:** Don't ignore duplicates. They are a common and easy-to-fix issue that can improve model performance.

**B. Handling Irrelevant or Invalid Data (The "Negative Ages" Problem)**
- **The Problem:** The lab description mentions "irrelevant data (like negative ages)". An age cannot be negative. This is a data entry error and represents impossible, invalid data.
- **What To Do:**
    1.  First, identify these rows. A simple filter like `df[df['Age'] < 0]` will show them.
    2.  Decide on a strategy. We could:
        a. **Remove the rows:** If there are only a few, this is the safest option.
        b. **Replace the value:** We could replace the negative age with the mean or median age. However, this assumes the rest of the data in that row is valuable and the error was isolated to the age. For this lab, removal is cleaner.
    3.  We will filter the DataFrame to keep only rows where `Age` is positive: `df = df[df['Age'] >= 0]`.
- **What Not To Do:** Don't just take the absolute value (e.g., `-22` becomes `22`). We don't know if `22` is the correct age, so it's safer to discard the invalid entry.

**C. Handling Missing Values (NaN)**
- **The Problem:** Some cells in the dataset are empty (represented as `NaN`). Machine learning algorithms cannot process `NaN` values, so we must handle them.
- **What To Do:**
    1.  Use `df.isnull().sum()` to see which columns have missing values and how many.
    2.  Choose a strategy based on the column:
        *   **For the 'Score' column:** This is a numerical value. A good strategy is **imputation**. We can fill the missing values with the mean or median score of the column. Using the mean is simple and often effective: `df['Score'].fillna(df['Score'].mean(), inplace=True)`.
        *   **For other columns:** If a row has many missing values, or if a crucial piece of information (like `Name` or `Gender`) is missing, it might be better to **drop the entire row** using `df.dropna(inplace=True)`.
- **What Not To Do:** Don't drop every row that has a single missing value without thinking. You might lose a significant portion of your dataset. Always analyze the impact before dropping data.

#### Step 3: Data Normalization

- **The Problem:** Features can have vastly different scales. For example, 'Age' might range from 18-40, while 'Score' ranges from 0-100. Algorithms that rely on distance calculations (like K-NN or SVM) can be biased by the feature with the larger range.
- **What To Do:** We will use **Min-Max Scaling** on the 'Age' column as instructed. This technique rescales the data to a fixed range, usually [0, 1].
    1.  Import `MinMaxScaler` from `sklearn.preprocessing`.
    2.  Create an instance of the scaler: `scaler = MinMaxScaler()`.
    3.  Apply it to the 'Age' column: `df['Age'] = scaler.fit_transform(df[['Age']])`. Note the double square brackets `[['Age']]` which are required because the scaler expects a 2D array-like input.
- **What Not To Do:** Don't normalize categorical data that has been encoded (like 'Gender' or 'City'). Normalization is intended for numerical features.

#### Step 4: Data Encoding

- **The Problem:** Most machine learning models only understand numbers, not text categories like "Male", "Female", or "New York". We need to convert these text labels into numbers.
- **What To Do:**
    1.  **Label Encoding for 'Gender':** 'Gender' has two categories ("Male", "Female"). Label Encoding will convert them to `0` and `1`. This is acceptable for binary categories.
        - Import `LabelEncoder`.
        - Apply it: `df['Gender'] = encoder.fit_transform(df['Gender'])`.
    2.  **One-Hot Encoding for 'City':** 'City' has multiple categories (e.g., "New York", "London", "Tokyo"). If we used Label Encoding (0, 1, 2), the model might incorrectly assume an ordered relationship (i.e., Tokyo > London > New York). **One-Hot Encoding** is the correct technique here. It creates a new binary column for each city.
        - Use the simple pandas function `pd.get_dummies()`.
        - `df = pd.get_dummies(df, columns=['City'], drop_first=True)`. The `drop_first=True` is important to avoid multicollinearity, a situation where features are highly correlated, which can be an issue for some models.

### Final Result

After all these steps, our dataset will be clean, fully numeric, and scaled appropriately, making it ready to be fed into a machine learning algorithm.


### 3. The Complete Solution Code

First, you need the `students.csv` file. Since it wasn't provided, I have created a sample one that includes all the problems mentioned in the lab.

**File: `students.csv`**
```csv
Name,Age,Gender,Score,Grade,City
Alice,22,Female,85,A,New York
Bob,23,Male,90,A,London
Charlie,21,Male,78,B,Tokyo
David,-22,Male,92,A,New York
Eve,24,Female,,B,Paris
Frank,23,Male,88,A,London
Alice,22,Female,85,A,New York
Grace,25,Female,95,A,Tokyo
Heidi,,Female,82,B,Paris
Ivan,22,Male,79,B,New York
Judy,24,Female,91,A,London
Frank,23,Male,88,A,London
Mallory,21,Male,65,C,Tokyo
Nancy,23,Female,89,A,Paris
Oscar,22,Male,,B,New York
```
*Save this text into a file named `students.csv` in your project folder.*

---

**File: `lab3_solution.py` (or a Jupyter Notebook)**

This is the complete, commented Python code to execute the lab steps.

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# --- 1. Import basic libraries and Load the dataset ---
print("--- Step 1 & 2: Loading dataset and initial inspection ---")
try:
    df = pd.read_csv('students.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: students.csv not found. Make sure the file is in the same directory.")
    exit()

print("\nOriginal DataFrame head:")
print(df.head())

print("\nOriginal DataFrame info:")
df.info()

# --- 3. Check for duplicates and remove them ---
print("\n--- Step 3: Checking for and removing duplicates ---")
num_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows found: {num_duplicates}")

# Displaying the duplicate rows before removing them
print("\nDuplicate rows:")
print(df[df.duplicated()])

# Removing duplicates
df.drop_duplicates(inplace=True)
print(f"\nNumber of rows after dropping duplicates: {len(df)}")


# --- Adding a step to handle irrelevant data (negative ages) ---
# This was mentioned in the lab description but not in the code examples.
print("\n--- Bonus Step: Handling Invalid Data (e.g., Negative Age) ---")
invalid_age_rows = df[df['Age'] < 0]
print(f"Number of rows with invalid (negative) age: {len(invalid_age_rows)}")
if not invalid_age_rows.empty:
    print("Rows with negative age:")
    print(invalid_age_rows)

    # Filter out rows with negative age
    df = df[df['Age'] >= 0]
    print(f"\nNumber of rows after removing invalid ages: {len(df)}")


# --- 4. Check for missing data and process them ---
print("\n--- Step 4: Checking for and handling missing data ---")
print("Missing values before handling:")
print(df.isnull().sum())

# Strategy 1: Imputation for 'Score' (numerical column)
# We fill missing scores with the mean of the existing scores.
score_mean = df['Score'].mean()
print(f"\n'Score' column mean is: {score_mean:.2f}. Using this for imputation.")
df['Score'].fillna(score_mean, inplace=True)

# Strategy 2: Drop rows where other crucial data might be missing (like 'Age')
# The dropna() function is a simple way to remove any remaining rows with NaN.
df.dropna(inplace=True)
# Note: In our case, after handling Score, dropna() will handle the missing 'Age'.

print("\nMissing values after handling:")
print(df.isnull().sum())
print(f"\nNumber of rows after handling all missing values: {len(df)}")


# --- Data Normalization ---
print("\n--- Step 5: Data Normalization (Min-Max Scaling on 'Age') ---")
print("'Age' column before normalization:")
print(df[['Name', 'Age']].head())

# Initialize the scaler
scaler = MinMaxScaler()

# Reshape the data and apply the scaler
# We use df[['Age']] to select the column as a DataFrame (2D), which the scaler expects
df['Age'] = scaler.fit_transform(df[['Age']])

print("\n'Age' column after Min-Max Scaling:")
print(df[['Name', 'Age']].head())


# --- Data Encoding ---
print("\n--- Step 6: Data Encoding (Categorical to Numerical) ---")

# --- Label Encoding for 'Gender' ---
print("\nEncoding 'Gender' column using Label Encoding...")
print("'Gender' column before encoding:")
print(df['Gender'].head())

le = LabelEncoder()
df['Gender'] = le.fit_transform(df['Gender'])
# To see which number corresponds to which label:
# print(le.classes_) # Will show ['Female', 'Male'] -> 0 is Female, 1 is Male

print("\n'Gender' column after Label Encoding:")
print(df['Gender'].head())


# --- One-Hot Encoding for 'City' ---
print("\nEncoding 'City' column using One-Hot Encoding...")
print("DataFrame shape before One-Hot Encoding:", df.shape)
print("Original columns:", df.columns.tolist())

# Use pandas get_dummies for one-hot encoding
# drop_first=True helps prevent multicollinearity in some models
df = pd.get_dummies(df, columns=['City'], drop_first=True)

print("\nDataFrame shape after One-Hot Encoding:", df.shape)
print("New columns:", df.columns.tolist())


# --- Final Cleaned DataFrame ---
print("\n--- Final, Cleaned, Normalized, and Encoded DataFrame ---")
print(df.head())

print("\nFinal DataFrame info:")
df.info()
print("\nLab successfully completed!")
```