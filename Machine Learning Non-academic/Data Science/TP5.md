
## Exercise 01 — Data Cleaning, Preprocessing & Visualization (Medical Dataset)

### Objective
We have a messy medical dataset containing patient information, vital signs, and diagnoses. The goal is to clean it, prepare it for modeling, and visualize relationships in the data using Seaborn.

### Dataset
We have the following dataset:

| PatientID | Age | BloodPressure | Cholesterol | Gender | Diagnosis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P001 | 25 | 120 | 200 | Female | Diabetes |
| P002 | NaN | 130 | 180 | male | Healthy |
| P003 | 65 | NaN | 250 | Male | Diabetes |
| P004 | 50 | 110 | 190 | female | Healthy |
| P005 | 80 | 200 | 300 | MALE | Hypertension |
| P006 | 120 | 95 | 180 | None | Healthy |
| P007 | 45 | 125 | NaN | Female | Diabetes |
| P008 | 38 | 118 | 210 | female | Healthy |
| P009 | NaN | 122 | 220 | FEMALE | None |
| P010 | 55 | 210 | 350 | Male | Hypertension |

### Tasks
We have to perform the following steps:

1.  **Clean the Dataset**
    *   Make all text in `Gender` and `Diagnosis` consistent (lowercase, remove extra spaces).
    *   Fill missing categorical values with a suitable representative value.
    *   Fill missing numeric values (`Age`, `BloodPressure`, `Cholesterol` ) with a suitable measure of central tendency.
    *   Remove extreme values (outliers) in numeric columns using an appropriate method.
    *   Encode categorical variables ( `Gender`, `Diagnosis` ) into numeric format.
    *   Scale numeric columns so they are comparable.
2.  **Visualize the Data**
    *   Show the relationship between `Age` and `BloodPressure`, distinguishing genders visually.
    *   Compare the distribution of `Cholesterol` by `Diagnosis`.
    *   Combine `Age`, `BloodPressure`, and `Cholesterol` into a format suitable for a single comparative plot by `Diagnosis`.
    *   Summarize average `BloodPressure` by `Diagnosis` and `Gender`, and present it visually using a pivot table or heatmap.

## Project 02: Titanic Data Preprocessing & Modeling

### Objective:
Build a full **data preprocessing and modeling pipeline** on the Titanic dataset.

### Instructions

#### Initial Exploration
*   Load the dataset: `sns.load_dataset('titanic')`.
*   Perform **exploratory data analysis (EDA)**: `.head()`, `.info()`, `.describe()`.
*   Check for missing values, data types, and outliers.
*   Visualize distributions of numerical and categorical features.
*   Explore correlation between features and the target (`survived`).

#### Data Cleaning
*   Handle **missing values** (choose your method): median, mean, mode, interpolation, etc.
*   Remove **duplicates** if necessary.
*   Decide which irrelevant or redundant columns to drop (e.g., `deck`, `embark_town`, `alive`, `who`).

#### Feature Engineering
*   Create new features such as:
    *   `FamilySize = sibsp + parch + 1`
    *   `IsAlone` (boolean if `FamilySize == 1`)
    *   Extract **titles** from `name` (Mr, Mrs, Miss, etc.)
*   Transform or combine other columns if useful.
*   Decide which features to keep or drop before modeling.

#### Categorical Encoding
*   Choose an encoding method for each categorical column:
    *   Label Encoding
    *   One-Hot Encoding
    *   Ordinal Encoding
*   Ensure all features are **numeric** before training.

#### Outlier Handling
*   Detect and handle outliers (choose a method):
    *   Z-score, IQR etc.
*   Consider transforming skewed features (log, sqrt, Box-Cox).

#### Scaling / Normalization
*   Decide if certain features need scaling:
    *   StandardScaler, MinMaxScaler, RobustScaler, Normalizer
*   Optional: compare the effect of scaling on model performance.

#### Train/Test Split
*   Split the dataset: 80% train / 20% test (consider stratified split).

#### Modeling
*   Train at least two models:
    *   Logistic Regression (`max_iter=500`)
    *   K-Nearest Neighbors (`n_neighbors=5`)

#### Evaluation
*   Evaluate performance on the **test set**:
    *   Accuracy
    *   Confusion Matrix
    *   Classification Report (precision, recall, F1-score)
*   Compare models and justify your final choice.

***

# Part 2: Lab Solution with Code and Explanations

This section provides a complete Python solution for both exercises using the `pandas`, `seaborn`, `matplotlib`, and `scikit-learn` libraries.

## Exercise 01: Medical Dataset Solution

### Setup and Data Creation
First, we'll import the necessary libraries and create the DataFrame from the provided data.

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# Create the initial DataFrame
data = {
    'PatientID': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010'],
    'Age': [25, np.nan, 65, 50, 80, 120, 45, 38, np.nan, 55],
    'BloodPressure': [120, 130, np.nan, 110, 200, 95, 125, 118, 122, 210],
    'Cholesterol': [200, 180, 250, 190, 300, 180, np.nan, 210, 220, 350],
    'Gender': ['Female', 'male', 'Male', 'female', 'MALE', 'None', 'Female', 'female', 'FEMALE', 'Male'],
    'Diagnosis': ['Diabetes', 'Healthy', 'Diabetes', 'Healthy', 'Hypertension', 'Healthy', 'Diabetes', 'Healthy', 'None', 'Hypertension']
}
df = pd.DataFrame(data)

print("Original Dataset:")
print(df)
```

### 1. Clean the Dataset

#### Step 1.1: Make Text Consistent
We standardize the `Gender` and `Diagnosis` columns to be lowercase and free of extra spaces. This prevents treating 'Female', 'female', and 'FEMALE' as different categories.

```python
# Standardize text columns
for col in ['Gender', 'Diagnosis']:
    df[col] = df[col].str.lower().str.strip()

print("\nDataset after standardizing text:")
print(df)
```

#### Step 1.2: Fill Missing Categorical Values
We replace `None` values (which become `None` strings after lowercasing) with `NaN` to handle them uniformly. Then, we fill these missing values using the mode (the most frequent value) of each column, which is a common strategy for categorical data.

```python
# Replace 'none' string with NaN for consistent handling
df.replace('none', np.nan, inplace=True)

# Fill missing categorical values with the mode
for col in ['Gender', 'Diagnosis']:
    mode_value = df[col].mode()[0]
    df[col].fillna(mode_value, inplace=True)
    
print("\nDataset after filling missing categorical values:")
print(df)
```

#### Step 1.3: Fill Missing Numeric Values
For numeric columns, we use the median to fill missing values. The median is robust to outliers, making it a safer choice than the mean.

```python
# Fill missing numeric values with the median
for col in ['Age', 'BloodPressure', 'Cholesterol']:
    median_value = df[col].median()
    df[col].fillna(median_value, inplace=True)

print("\nDataset after filling missing numeric values:")
print(df)
```

#### Step 1.4: Remove Outliers using IQR
We identify and remove extreme values using the Interquartile Range (IQR) method. Any data point that falls below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR is considered an outlier.

```python
# Keep a copy for visualization before outlier removal
df_for_viz = df.copy()

# Remove outliers from numeric columns
numeric_cols = ['Age', 'BloodPressure', 'Cholesterol']
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter out the outliers
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

print("\nDataset after removing outliers:")
print(df.reset_index(drop=True))
```

#### Step 1.5: Encode Categorical Variables
Machine learning models require numeric input. We use One-Hot Encoding to convert `Gender` and `Diagnosis` into a numeric format without implying any order between categories.

```python
# One-Hot Encode categorical variables
df_encoded = pd.get_dummies(df, columns=['Gender', 'Diagnosis'], drop_first=True)

print("\nDataset after one-hot encoding:")
print(df_encoded)
```

#### Step 1.6: Scale Numeric Columns
We scale the numeric features to a range between 0 and 1 using `MinMaxScaler`. This ensures that all features have a similar scale, which is important for many algorithms.

```python
# Scale numeric columns
scaler = MinMaxScaler()
df_encoded[numeric_cols] = scaler.fit_transform(df_encoded[numeric_cols])

print("\nFinal Cleaned and Scaled Dataset:")
print(df_encoded)
```

### 2. Visualize the Data
For visualization, we'll use the dataset **before** outlier removal and encoding (`df_for_viz`) to see the original distributions.

#### Step 2.1: Relationship between Age and BloodPressure
A scatter plot is perfect for visualizing the relationship between two continuous variables. The `hue` parameter color-codes the points by gender.

```python
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_for_viz, x='Age', y='BloodPressure', hue='Gender', style='Gender', s=100)
plt.title('Relationship between Age and Blood Pressure by Gender')
plt.xlabel('Age')
plt.ylabel('Blood Pressure')
plt.grid(True)
plt.show()
```

#### Step 2.2: Distribution of Cholesterol by Diagnosis
A box plot is an excellent way to compare the distributions of a numeric variable across different categories.

```python
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_for_viz, x='Diagnosis', y='Cholesterol')
plt.title('Distribution of Cholesterol by Diagnosis')
plt.xlabel('Diagnosis')
plt.ylabel('Cholesterol')
plt.show()
```

#### Step 2.3: Combined Comparative Plot
To create a single plot comparing multiple variables (`Age`, `BloodPressure`, `Cholesterol`), we first need to reshape the data from a "wide" format to a "long" format using `pd.melt`. This makes it suitable for plotting with Seaborn's `hue`.

```python
# Melt the DataFrame to a long format
df_melted = df_for_viz.melt(id_vars='Diagnosis', 
                            value_vars=['Age', 'BloodPressure', 'Cholesterol'],
                            var_name='Metric', 
                            value_name='Value')

plt.figure(figsize=(12, 7))
sns.boxplot(data=df_melted, x='Diagnosis', y='Value', hue='Metric')
plt.title('Comparison of Metrics by Diagnosis')
plt.xlabel('Diagnosis')
plt.ylabel('Scaled Value (for comparison)')
plt.show()
```

#### Step 2.4: Summarize with a Heatmap
A pivot table can summarize the average blood pressure for each combination of `Diagnosis` and `Gender`. A heatmap provides a clear, color-coded visualization of this summary.

```python
# Create a pivot table
pivot_table = df_for_viz.pivot_table(values='BloodPressure', 
                                     index='Diagnosis', 
                                     columns='Gender', 
                                     aggfunc='mean')

plt.figure(figsize=(8, 5))
sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt=".1f")
plt.title('Average Blood Pressure by Diagnosis and Gender')
plt.show()
```
---
## Project 02: Titanic Data Preprocessing & Modeling Solution

This is a complete pipeline from loading data to evaluating models.

### Setup

```python
# Import all necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
```

### Initial Exploration
Load the dataset and perform basic EDA to understand its structure, missing values, and distributions.

```python
# Load dataset
titanic = sns.load_dataset('titanic')

# EDA
print("First 5 rows:")
print(titanic.head())

print("\nDataset Info:")
titanic.info()

print("\nDescriptive Statistics:")
print(titanic.describe())

print("\nMissing Values:")
print(titanic.isnull().sum())

# Visualize distributions
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
sns.histplot(titanic['age'].dropna(), kde=True, ax=axes[0, 0]).set_title('Age Distribution')
sns.countplot(x='sex', data=titanic, ax=axes[0, 1]).set_title('Gender Distribution')
sns.countplot(x='pclass', data=titanic, ax=axes[1, 0]).set_title('Passenger Class Distribution')
sns.histplot(titanic['fare'], kde=True, ax=axes[1, 1]).set_title('Fare Distribution')
plt.tight_layout()
plt.show()
```

### Data Cleaning
Handle missing values and drop irrelevant or redundant columns.

```python
# Handle missing values
# Age: Impute with the median, as it's robust to outliers.
titanic['age'].fillna(titanic['age'].median(), inplace=True)

# Embarked: Impute with the mode, as it's a categorical feature.
titanic['embarked'].fillna(titanic['embarked'].mode()[0], inplace=True)

# Drop irrelevant/redundant columns
# 'deck': Too many missing values.
# 'embark_town': Redundant with 'embarked'.
# 'alive': Redundant with 'survived'.
# 'who', 'adult_male': Can be derived from 'sex' and 'age'.
# 'class': Redundant with 'pclass'.
titanic.drop(['deck', 'embark_town', 'alive', 'who', 'adult_male', 'class'], axis=1, inplace=True)

print("\nDataset after cleaning missing values and dropping columns:")
print(titanic.isnull().sum())
```

### Feature Engineering
Create new, potentially more informative features from existing ones.

```python
# Create FamilySize
titanic['family_size'] = titanic['sibsp'] + titanic['parch'] + 1

# Create IsAlone
titanic['is_alone'] = (titanic['family_size'] == 1).astype(int)

# Extract titles from name
titanic['title'] = titanic['name'].str.extract(' ([A-Za-z]+)\.', expand=False)
# Consolidate rare titles
common_titles = ['Mr', 'Miss', 'Mrs', 'Master']
titanic['title'] = titanic['title'].apply(lambda x: x if x in common_titles else 'Other')

# Drop original columns that are now redundant
titanic.drop(['name', 'sibsp', 'parch', 'ticket', 'passengerid'], axis=1, inplace=True)

print("\nDataset after feature engineering:")
print(titanic.head())
```

### Preprocessing Pipeline (Encoding & Scaling)
We create a preprocessing pipeline to handle categorical encoding and numerical scaling cleanly. This is best practice as it prevents data leakage and simplifies applying the same transformations to the test set.

```python
# Define features and target
X = titanic.drop('survived', axis=1)
y = titanic['survived']

# Identify categorical and numerical features
categorical_features = ['sex', 'embarked', 'title', 'pclass']
numerical_features = ['age', 'fare', 'family_size']

# Create preprocessing pipelines for both numeric and categorical data
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Create a preprocessor object using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough' # Keep 'is_alone' as it is already 0/1
)
```

### Train/Test Split
Split the data into training and testing sets. Using `stratify=y` ensures that both sets have a similar proportion of survivors, which is important for imbalanced datasets.

```python
# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### Modeling
Train the two specified models: Logistic Regression and K-Nearest Neighbors. We'll embed our preprocessor into a full pipeline with the model.

```python
# --- Model 1: Logistic Regression ---
lr_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', LogisticRegression(max_iter=500, random_state=42))])
lr_pipeline.fit(X_train, y_train)

# --- Model 2: K-Nearest Neighbors ---
knn_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', KNeighborsClassifier(n_neighbors=5))])
knn_pipeline.fit(X_train, y_train)

print("\nModels trained successfully.")
```

### Evaluation
Evaluate both models on the unseen test set and compare their performance.

```python
# Make predictions
y_pred_lr = lr_pipeline.predict(X_test)
y_pred_knn = knn_pipeline.predict(X_test)

# --- Evaluation for Logistic Regression ---
print("\n--- Logistic Regression Evaluation ---")
print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))
print("\nClassification Report:\n", classification_report(y_test, y_pred_lr))

# --- Evaluation for K-Nearest Neighbors ---
print("\n--- K-Nearest Neighbors Evaluation ---")
print("Accuracy:", accuracy_score(y_test, y_pred_knn))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_knn))
print("\nClassification Report:\n", classification_report(y_test, y_pred_knn))

# --- Justification ---
print("\n--- Model Comparison and Justification ---")
lr_acc = accuracy_score(y_test, y_pred_lr)
knn_acc = accuracy_score(y_test, y_pred_knn)

if lr_acc > knn_acc:
    print(f"Final Choice: Logistic Regression (Accuracy: {lr_acc:.4f})")
    print("Justification: Logistic Regression achieved a higher overall accuracy and balanced precision/recall scores. It is also a more interpretable model, which is beneficial for understanding feature importance.")
else:
    print(f"Final Choice: K-Nearest Neighbors (Accuracy: {knn_acc:.4f})")
    print("Justification: K-Nearest Neighbors provided a higher overall accuracy. While less interpretable, its performance on this dataset was superior.")

```