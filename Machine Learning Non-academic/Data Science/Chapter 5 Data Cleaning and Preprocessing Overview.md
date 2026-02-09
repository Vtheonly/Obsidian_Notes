# Chapter 05: Data Cleaning and Preprocessing

## Data Cleaning and Preprocessing Steps

1.  **Handle Missing Values**
    *   Drop rows/columns or impute (mean, median, mode)
    *   Advanced: KNN imputation, predictive models
2.  **Ensuring Consistent Data Types**
3.  **Handle Duplicates**
    *   Remove duplicate rows to avoid bias
4.  **Outlier Detection and Treatment**
    *   Boxplot, Histogram
    *   Methods: Z-score, IQR
    *   Options: remove, cap (winsorization), transform
5.  **Textual Data Processing (if applicable)**
6.  **Feature Scaling / Normalization**
    *   Methods: Min-Max, Standardization (Z-score), Robust, L1/L2
    *   Decide based on algorithm and presence of outliers

## 1. Missing data

One of the most common problems in raw datasets is missing data.
These gaps may occur for various reasons, such as data :

*   data entry mistakes,
*   sensor failures,
*   unanswered survey questions, or corrupted files.

**Understanding the cause of the missing data is crucial to determine the best way to handle it.**

### 1.1. Types of Missing Data

There are three main types of missing data, depending on why the data is missing.

*   **Missing Completely at Random (MCAR)** The missing values have no relationship with any variable.
    Example: A survey sheet was lost in the mail — it could belong to anyone.
*   **Missing at Random (MAR)** The missing data depends on other observed variables, but not on the missing one itself.
    Example: Younger people are more likely to skip income questions, but it's not related to how much they earn.
*   **Missing Not at Random (MNAR)** The missing data depends on the value of the missing variable itself.
    Example: People with very high incomes choose not to reveal their income.

### 1.2. Detecting Missing Values

| Method | Description | Example |
| :--- | :--- | :--- |
| `df.isnull()` | Returns a True/False mask for missing values | Identify missing entries |
| `df.isnull().sum()` | Counts missing values per column | Find which columns have missing data |
| `df.info()` | Shows number of non-null values | Quick structural overview |
| `sns.heatmap(df.isnull())` | Visualizes missing patterns | Detect where data is missing |
| `df[df.isnull().any(axis=1)]` | Filters rows with missing values | Inspect affected rows |

```python
In [1]: import seaborn as sns
        import matplotlib.pyplot as plt
        import pandas as pd

        # Load Titanic dataset (already contains missing data)
        df = sns.load_dataset('titanic')
        # 1 mask for missing values
        df.isnull()
```

```text
Out[1]:
      survived  pclass    sex    age  sibsp  parch   fare  embarked  class    who  adult_male   deck  emb
0        False   False  False  False  False  False  False     False  False  False       False   True
1        False   False  False  False  False  False  False     False  False  False       False  False
2        False   False  False  False  False  False  False     False  False  False       False   True
3        False   False  False  False  False  False  False     False  False  False       False  False
4        False   False  False  False  False  False  False     False  False  False       False   True
...        ...     ...    ...    ...    ...    ...    ...       ...    ...    ...         ...    ...
886      False   False  False  False  False  False  False     False  False  False       False   True
887      False   False  False  False  False  False  False     False  False  False       False  False
888      False   False  False   True  False  False  False     False  False  False       False   True
889      False   False  False  False  False  False  False     False  False  False       False  False
890      False   False  False  False  False  False  False     False  False  False       False   True

891 rows × 15 columns
```

```python
In [2]: # 2. Count missing values per column
        print(df.isnull().sum())
```

```text
survived         0
pclass           0
sex              0
age            177
sibsp            0
parch            0
fare             0
embarked         2
class            0
who              0
adult_male       0
deck           688
embark_town      2
alive            0
alone            0
dtype: int64
```

```python
In [3]: # 2. Check if the DataFrame has any missing value
        print(df.isnull().values.any())
```

```text
True
```

```python
In [4]: # 3. Percentage of missing values
        print((df.isnull().sum() / len(df)) * 100)
```

```text
survived        0.000000
pclass          0.000000
sex             0.000000
age            19.865320
sibsp           0.000000
parch           0.000000
fare            0.000000
embarked        0.224467
class           0.000000
who             0.000000
adult_male      0.000000
deck           77.216611
embark_town     0.224467
alive           0.000000
alone           0.000000
dtype: float64
```

```python
In [5]: # 4. Visualize missing data
        plt.figure(figsize=(8,4))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title("Missing Data Visualization", fontsize=14)
        plt.show()
```

*[Missing Data Visualization Heatmap]*

```python
In [6]: # 5. Inspect rows and columns with missing data
        print("\nRows with missing data:")
        display(df[df.isnull().any(axis=1)]) # Shows all rows that have at Least one NaN

        print("\nColumns with missing data:")
        missing_columns = df.columns[df.isnull().any()].tolist()
        print(missing_columns)
```

Rows with missing data:

| | survived | pclass | sex | age | sibsp | parch | fare | embarked | class | who | adult_male | deck | ... |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 0 | 3 | male | 22.0 | 1 | 0 | 7.2500 | S | Third | man | True | NaN | ... |
| **2** | 1 | 3 | female | 26.0 | 0 | 0 | 7.9250 | S | Third | woman | False | NaN | ... |
| **4** | 0 | 3 | male | 35.0 | 0 | 0 | 8.0500 | S | Third | man | True | NaN | ... |
| **5** | 0 | 3 | male | NaN | 0 | 0 | 8.4583 | Q | Third | man | True | NaN | ... |
| **7** | 0 | 3 | male | 2.0 | 3 | 1 | 21.0750 | S | Third | child | False | NaN | ... |
| **...** | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **884** | 0 | 3 | male | 25.0 | 0 | 0 | 7.0500 | S | Third | man | True | NaN | ... |
| **885** | 0 | 3 | female | 39.0 | 0 | 5 | 29.1250 | Q | Third | woman | False | NaN | ... |
| **886** | 0 | 2 | male | 27.0 | 0 | 0 | 13.0000 | S | Second | man | True | NaN | ... |
| **888** | 0 | 3 | female | NaN | 1 | 2 | 23.4500 | S | Third | woman | False | NaN | ... |
| **890** | 0 | 3 | male | 32.0 | 0 | 0 | 7.7500 | Q | Third | man | True | NaN | ... |

709 rows × 15 columns

Columns with missing data:
`['age', 'embarked', 'deck', 'embark_town']`

### 1.3. Strategies for Handling Missing Data

After identifying missing data, we can **handle** it depending on the situation and data importance.

There are 4 main strategies:

1.  **Remove (drop)** rows or columns with missing data
2.  **Fill (impute)** missing values using a constant, mean, median, or mode
3.  **Forward / backward fill** based on neighboring values
4.  **Model-based imputation** using prediction (advanced)

```python
In [7]: # 1. Setup example DataFrame with missing values
        import pandas as pd
        import numpy as np

        data = {
            'Name': ['Amel', 'Rami', 'Sara', 'Yacine', 'Lina', 'Salma', 'Ilyes', 'Ali'],
            'Age': [25, np.nan, 30, 22, 35, 40, np.nan, 28],
            'Income': [50000, 60000, np.nan, 45000, 70000, np.nan, 52000, 61000],
            'Experience': [2, 3, 5, 1, 6, 8, 2, 4],
            'City': ['Algiers', 'Oran', None, 'Constantine', 'Tlemcen', 'Constantine', 'Tlemcen', None]
        }
        df = pd.DataFrame(data)
        print("Original dataset with missing values:")
        display(df)
```

Original dataset with missing values:

| | Name | Age | Income | Experience | City |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | Amel | 25.0 | 50000.0 | 2 | Algiers |
| **1** | Rami | NaN | 60000.0 | 3 | Oran |
| **2** | Sara | 30.0 | NaN | 5 | None |
| **3** | Yacine | 22.0 | 45000.0 | 1 | Constantine |
| **4** | Lina | 35.0 | 70000.0 | 6 | Tlemcen |
| **5** | Salma | 40.0 | NaN | 8 | Constantine |
| **6** | Ilyes | NaN | 52000.0 | 2 | Tlemcen |
| **7** | Ali | 28.0 | 61000.0 | 4 | None |

```python
In [8]: # 2. Removing Missing Data
        # Drop rows that contain any missing value
        df_drop_rows = df.dropna()
        print("After dropping rows with missing data:")
        display(df_drop_rows)
```

After dropping rows with missing data:

| | Name | Age | Income | Experience | City |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | Amel | 25.0 | 50000.0 | 2 | Algiers |
| **3** | Yacine | 22.0 | 45000.0 | 1 | Constantine |
| **4** | Lina | 35.0 | 70000.0 | 6 | Tlemcen |

```python
In [9]: # Drop columns that contain any missing value
        df_drop_cols = df.dropna(axis=1)
        print("After dropping columns with missing data:")
        display(df_drop_cols)
```

After dropping columns with missing data:

| | Name | Experience |
|:---:|:---:|:---:|
| **0** | Amel | 2 |
| **1** | Rami | 3 |
| **2** | Sara | 5 |
| **3** | Yacine | 1 |
| **4** | Lina | 6 |
| **5** | Salma | 8 |
| **6** | Ilyes | 2 |
| **7** | Ali | 4 |

```python
In [10]: # 3. Filling Missing Data (Simple Imputation)
```

```python
In [11]: # Fill all missing values with a fixed value
         df_fill_constant = df.fillna("Unknown")
         print("Fill with constant value:")
         display(df_fill_constant)
```

Fill with constant value:

| | Name | Age | Income | Experience | City |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | Amel | 25.0 | 50000.0 | 2 | Algiers |
| **1** | Rami | Unknown | 60000.0 | 3 | Oran |
| **2** | Sara | 30.0 | Unknown | 5 | Unknown |
| **3** | Yacine | 22.0 | 45000.0 | 1 | Constantine |
| **4** | Lina | 35.0 | 70000.0 | 6 | Tlemcen |
| **5** | Salma | 40.0 | Unknown | 8 | Constantine |
| **6** | Ilyes | Unknown | 52000.0 | 2 | Tlemcen |
| **7** | Ali | 28.0 | 61000.0 | 4 | Unknown |

```python
In [12]: # Fill numeric columns with mean
         df_fill_mean = df.copy()
         df_fill_mean['Age'] = df_fill_mean['Age'].fillna(df['Age'].mean())
         df_fill_mean['Income'] = df_fill_mean['Income'].fillna(df['Income'].mean())
         print("Fill numeric columns with mean value:")
         print(df_fill_mean)
```

Fill numeric columns with mean value:
```text
   Name   Age        Income  Experience         City
0  Amel  25.0  50000.000000           2      Algiers
1  Rami  30.0  60000.000000           3         Oran
2  Sara  30.0  56333.333333           5         None
3 Yacine 22.0  45000.000000           1  Constantine
4  Lina  35.0  70000.000000           6      Tlemcen
5 Salma  40.0  56333.333333           8  Constantine
6 Ilyes  30.0  52000.000000           2      Tlemcen
7   Ali  28.0  61000.000000           4         None
```

```python
In [13]: # Fill categorical columns with mode (most frequent value)
         df_fill_mode = df.copy()
         df_fill_mode['City']=df_fill_mode['City'].fillna(df['City'].mode()[0])
         print("Fill categorical column with mode:")
         display(df_fill_mode)
```

Fill categorical column with mode:

| | Name | Age | Income | Experience | City |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | Amel | 25.0 | 50000.0 | 2 | Algiers |
| **1** | Rami | NaN | 60000.0 | 3 | Oran |
| **2** | Sara | 30.0 | NaN | 5 | Constantine |
| **3** | Yacine | 22.0 | 45000.0 | 1 | Constantine |
| **4** | Lina | 35.0 | 70000.0 | 6 | Tlemcen |
| **5** | Salma | 40.0 | NaN | 8 | Constantine |
| **6** | Ilyes | NaN | 52000.0 | 2 | Tlemcen |
| **7** | Ali | 28.0 | 61000.0 | 4 | Constantine |

```python
In [14]: # 4. Forward Fill / Backward Fill
         display(df)
         # Forward fill: replaces missing values with the previous non-missing value
         df_ffill = df.ffill()
         print("\nForward fill:")
         display(df_ffill)
```

*Original DataFrame Displayed*

Forward fill:

| | Name | Age | Income | Experience | City |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | Amel | 25.0 | 50000.0 | 2 | Algiers |
| **1** | Rami | 25.0 | 60000.0 | 3 | Oran |
| **2** | Sara | 30.0 | 60000.0 | 5 | Oran |
| **3** | Yacine | 22.0 | 45000.0 | 1 | Constantine |
| **4** | Lina | 35.0 | 70000.0 | 6 | Tlemcen |
| **5** | Salma | 40.0 | 70000.0 | 8 | Constantine |
| **6** | Ilyes | 40.0 | 52000.0 | 2 | Tlemcen |
| **7** | Ali | 28.0 | 61000.0 | 4 | Tlemcen |

```python
In [15]: # Backward fill: replaces missing values with the next non-missing value
         df_bfill = df.bfill()
         print("\nBackward fill:")
         display(df_bfill)
```

Backward fill:

| | Name | Age | Income | Experience | City |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | Amel | 25.0 | 50000.0 | 2 | Algiers |
| **1** | Rami | 30.0 | 60000.0 | 3 | Oran |
| **2** | Sara | 30.0 | 45000.0 | 5 | Constantine |
| **3** | Yacine | 22.0 | 45000.0 | 1 | Constantine |
| **4** | Lina | 35.0 | 70000.0 | 6 | Tlemcen |
| **5** | Salma | 40.0 | 52000.0 | 8 | Constantine |
| **6** | Ilyes | 28.0 | 52000.0 | 2 | Tlemcen |
| **7** | Ali | 28.0 | 61000.0 | 4 | None |

```python
In [16]: from sklearn.impute import KNNImputer
         # Select only the two numeric columns
         num_cols = ['Age', 'Income']

         # Apply KNN Imputer
         imputer = KNNImputer(n_neighbors=2)
         df[num_cols] = imputer.fit_transform(df[num_cols])

         # Check the results
         print("After KNN Imputation on the two numeric columns:")
         display(df[num_cols])
```

After KNN Imputation on the two numeric columns:

| | Age | Income |
|:---:|:---:|:---:|
| **0** | 25.0 | 50000.0 |
| **1** | 26.5 | 60000.0 |
| **2** | 30.0 | 55500.0 |
| **3** | 22.0 | 45000.0 |
| **4** | 35.0 | 70000.0 |
| **5** | 40.0 | 65500.0 |
| **6** | 23.5 | 52000.0 |
| **7** | 28.0 | 61000.0 |

## 2. Ensuring Consistent Data Types

### Why It Matters

Inconsistent data types can cause:

*   Incorrect mathematical operations (e.g., "500" + "200" → "500200" instead of 700).
*   Errors during transformations or model training.
*   Unexpected sorting or filtering behavior.
*   Memory inefficiency.

For example, a column with numeric values stored as text (`object` type in pandas) may not behave correctly during analysis.

### 2.1. Steps to Ensure Consistent Data Types

1.  **Inspect** current data types using `df.dtypes` or `df.info()`.
2.  **Convert** columns to appropriate types:
    *   Strings → numeric (`pd.to_numeric()`)
    *   Strings → datetime (`pd.to_datetime()`)
    *   Numeric → category (`astype('category')`)
3.  **Validate** conversion and handle errors.

```python
In [17]: # Step 1: Create a dataset with inconsistent data types
         import pandas as pd
         data = {
             'CustomerID': ['101', '102', '103', '104'],
             'JoinDate': ['2024-01-10', '2024-03-15', '2024/04/01', 'April 25, 2024'],
             'Revenue': ['5000', '6000', 'SevenThousand', '8000'],
             'Membership': ['Gold', 'Silver', 'Gold', 'Bronze']
         }
         df = pd.DataFrame(data)
         display(df)

         print("Current Data Types:")
         print(df.dtypes)
```

| | CustomerID | JoinDate | Revenue | Membership |
|:---:|:---:|:---:|:---:|:---:|
| **0** | 101 | 2024-01-10 | 5000 | Gold |
| **1** | 102 | 2024-03-15 | 6000 | Silver |
| **2** | 103 | 2024/04/01 | SevenThousand | Gold |
| **3** | 104 | April 25, 2024 | 8000 | Bronze |

Current Data Types:
CustomerID object
JoinDate object
Revenue object
Membership object
dtype: object

```python
In [18]: # Step 2: Convert Data Types (coerce:invalid->NAN, raise:error, default:keep original)
         # Convert strings to datetime
         df['JoinDate'] = pd.to_datetime(df['JoinDate'], errors='coerce')

         # Convert Revenue to numeric (coerce errors to NaN)
         df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

         # Convert CustomerID to integer
         df['CustomerID'] = df['CustomerID'].astype(int)

         # Convert Membership to categorical
         df['Membership'] = df['Membership'].astype('category')

         print(" After Conversion:")
         display(df)

         print(" Data Types After Conversion:")
         print(df.dtypes)
```

After Conversion:

| | CustomerID | JoinDate | Revenue | Membership |
|:---:|:---:|:---:|:---:|:---:|
| **0** | 101 | 2024-01-10 | 5000.0 | Gold |
| **1** | 102 | 2024-03-15 | 6000.0 | Silver |
| **2** | 103 | NaT | NaN | Gold |
| **3** | 104 | NaT | 8000.0 | Bronze |

Data Types After Conversion:
CustomerID int64
JoinDate datetime64[ns]
Revenue float64
Membership category
dtype: object

```python
In [19]: # Step 3: Validate and Detect Remaining Issues
         # Check if any conversion failed (NaN after coercion)
         missing_after_conversion = df[df.isnull().any(axis=1)]

         print(" Rows with failed type conversion:")
         display(missing_after_conversion)
```

Rows with failed type conversion:

| | CustomerID | JoinDate | Revenue | Membership |
|:---:|:---:|:---:|:---:|:---:|
| **2** | 103 | NaT | NaN | Gold |
| **3** | 104 | NaT | 8000.0 | Bronze |

## 3. Detecting and Removing Duplicate Records

### Why Duplicates Are a Problem

Duplicate records can :

*   **distort statistical analysis**,
*   **inflate sample sizes**, or
*   **bias model training**.

They often appear due to:

*   Data merging from multiple sources
*   Repeated manual entries
*   API or system logging errors

### Common Scenarios

1.  Duplicate entire rows → exact same data repeated.
2.  Duplicate entries based on a **subset of columns** (e.g., same `CustomerID` or `Email` but different info elsewhere).
3.  Near-duplicates — same entities with minor typos or case variations (requires fuzzy matching or string normalization).

```python
In [20]: # Step 1: Create a sample dataset with duplicates
         import pandas as pd
         data = {
             'CustomerID': [101, 102, 103, 101, 104, 105, 103],
             'Name': ['Amel', 'Rami', 'Sara', 'Amel', 'Yacine', 'Hassan', 'Sara'],
             'Email': [
                 'amel@example.com',
                 'rami@example.com',
                 'sara@example.com',
                 'amel@example.com',
                 'yacine@example.com',
                 'hassan@example.com',
                 'sara@example.com'
             ],
             'Purchase': [250, 300, 150, 250, 400, 500, 250]
         }
         df = pd.DataFrame(data)
         print(" Original Dataset:")
         display(df)
```

Original Dataset:

| | CustomerID | Name | Email | Purchase |
|:---:|:---:|:---:|:---:|:---:|
| **0** | 101 | Amel | amel@example.com | 250 |
| **1** | 102 | Rami | rami@example.com | 300 |
| **2** | 103 | Sara | sara@example.com | 150 |
| **3** | 101 | Amel | amel@example.com | 250 |
| **4** | 104 | Yacine | yacine@example.com | 400 |
| **5** | 105 | Hassan | hassan@example.com | 500 |
| **6** | 103 | Sara | sara@example.com | 250 |

```python
In [21]: #Detect duplicate rows
         duplicate_rows = df[df.duplicated()]
         # Drop duplicates (keep the first occurrence by default)
         df_no_duplicates = df.drop_duplicates()
         df_no_duplicates
```

| | CustomerID | Name | Email | Purchase |
|:---:|:---:|:---:|:---:|:---:|
| **0** | 101 | Amel | amel@example.com | 250 |
| **1** | 102 | Rami | rami@example.com | 300 |
| **2** | 103 | Sara | sara@example.com | 150 |
| **4** | 104 | Yacine | yacine@example.com | 400 |
| **5** | 105 | Hassan | hassan@example.com | 500 |
| **6** | 103 | Sara | sara@example.com | 250 |

```python
In [22]: #Detect duplicates based on specific columns
         # Sometimes we only care about duplicates based on CustomerID or Email
         duplicates_on_email = df[df.duplicated(subset=['Email'])]
         print(duplicates_on_email)
         # Remove duplicates by Email only (keep first occurrence)
         df_unique_email = df.drop_duplicates(subset=['Email'], keep='first')
         print(df_unique_email)
```

```text
   CustomerID  Name               Email  Purchase
3         101  Amel    amel@example.com       250
6         103  Sara    sara@example.com       250
   CustomerID    Name               Email  Purchase
0         101    Amel    amel@example.com       250
1         102    Rami    rami@example.com       300
2         103    Sara    sara@example.com       150
4         104  Yacine  yacine@example.com       400
5         105  Hassan  hassan@example.com       500
```

## 4. Handling Outliers in Data

**Outliers are extreme values that differ significantly from other data points.**

*   They can distort statistical summaries,
*   cause bias in models, and
*   lead to wrong conclusions.

### 4.1. Identifying Outliers

| Method | Description | Works Best For | Example |
| :--- | :--- | :--- | :--- |
| **Boxplot** | Visual tool showing spread and whiskers | Any numeric data | Points outside whiskers |
| **Histogram** | Shows distribution and frequency | Any numeric data | Long tail or isolated bars |
| **Z-Score** | Values far from mean (>3 or <-3 std) | Normally distributed data | Salary much higher than average |
| **IQR** | Uses quartiles and range (Q1, Q3) | Non-normal data | Detects extreme income values |

### 4.1.1 Identifying using boxplot and histogram

```python
In [23]: # Example 1
         import pandas as pd
         import numpy as np
         import matplotlib.pyplot as plt
         from scipy.stats import zscore
         np.random.seed(42)
         df = pd.DataFrame({
             "AnnualIncome": np.concatenate([np.random.normal(50000, 8000, 100), [150000, 200000]])
         })
         print("Original Data Summary:")
         display(df.describe())
```

Original Data Summary:

| | AnnualIncome |
|:---:|:---:|
| **count** | 102.000000 |
| **mean** | 51636.497903 |
| **std** | 19274.358766 |
| **min** | 29042.039167 |
| **25%** | 45271.592802 |
| **50%** | 49249.366384 |
| **75%** | 54073.032905 |
| **max** | 200000.000000 |

```python
In [24]: # 2. Visualize Outliers (Boxplot and Histogram)
         plt.figure(figsize=(10, 4))
         plt.subplot(1, 2, 1)
         df.boxplot(column='AnnualIncome')
         plt.title("Boxplot - Detect Outliers")
         plt.subplot(1, 2, 2)
         df['AnnualIncome'].hist(bins=30)
         plt.title("Histogram - Income Distribution")
         plt.show()
```

*[Boxplot and Histogram Displayed]*

```python
In [25]: # Example 2
         import pandas as pd
         import numpy as np
         import matplotlib.pyplot as plt
         import seaborn as sns

         # Charger le dataset tips
         tips = sns.load_dataset('tips')
         display(tips.head())
         display(tips.describe())
```

| | total_bill | tip | sex | smoker | day | time | size |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 16.99 | 1.01 | Female | No | Sun | Dinner | 2 |
| **1** | 10.34 | 1.66 | Male | No | Sun | Dinner | 3 |
| **2** | 21.01 | 3.50 | Male | No | Sun | Dinner | 3 |
| **3** | 23.68 | 3.31 | Male | No | Sun | Dinner | 2 |
| **4** | 24.59 | 3.61 | Female | No | Sun | Dinner | 4 |

| | total_bill | tip | size |
|:---:|:---:|:---:|:---:|
| **count** | 244.000000 | 244.000000 | 244.000000 |
| **mean** | 19.785943 | 2.998279 | 2.569672 |
| **std** | 8.902412 | 1.383638 | 0.951100 |
| **min** | 3.070000 | 1.000000 | 1.000000 |
| **25%** | 13.347500 | 2.000000 | 2.000000 |
| **50%** | 17.795000 | 2.900000 | 2.000000 |
| **75%** | 24.127500 | 3.562500 | 3.000000 |
| **max** | 50.810000 | 10.000000 | 6.000000 |

```python
In [26]: sns.boxplot(y=tips['total_bill'],showmeans=True, color='lightgreen')
         plt.title("Boxplot of Total Bill")
         plt.show()
```

*[Boxplot of Total Bill Displayed]*

### 4.1.2. Detecting Outliers using Z-Score

**Z-Score and Outlier Detection**

The **z-score** measures **how many standard deviations** a value is **above or below the mean**.

**Formula:**

$$z = \frac{x - \mu}{\sigma}$$

where:

*   $x$ = observed value
*   $\mu$ = mean of the column
*   $\sigma$ = standard deviation of the column

**Why use 3 as a threshold?**

*   In a **normal distribution**, about **99.7% of values** lie within **±3 standard deviations** from the mean (empirical rule).
*   **Values with $z > 3$ or $z < -3$ are **rare** and are considered **outliers**.**

```python
In [27]: # Values > 3 or < -3 are considered outliers.
         df['Zscore'] = zscore(df['AnnualIncome'])
         outliers_z = df[(df['Zscore'] > 3) | (df['Zscore'] < -3)]
         print("\nOutliers detected using Z-Score:")
         display(outliers_z)
```

Outliers detected using Z-Score:

| | AnnualIncome | Zscore |
|:---:|:---:|:---:|
| **100** | 150000.0 | 5.128536 |
| **101** | 200000.0 | 7.735467 |

```python
In [28]: #P=(n-1)*q+1
         import pandas as pd
         df = pd.DataFrame({'Valeurs': [3, 5, 7, 5, 12, 14, 21, 13]})
         print(df)
         q1 = df['Valeurs'].quantile(0.25)
         q2 = df['Valeurs'].quantile(0.50)
         q3 = df['Valeurs'].quantile(0.75)
         print(q1)
```

```text
   Valeurs
0        3
1        5
2        7
3        5
4       12
5       14
6       21
7       13
5.0
```

### 4.1.3. Detecting Outliers using IQR Method (Interquartile Range)

The **Interquartile Range (IQR)** measures the **spread of the middle 50%** of the data. It is a robust measure of variability that is **less sensitive to extreme values** (outliers) than the standard deviation.

**Formula:**

$$IQR = Q_3 - Q_1$$

where:

*   $Q_1$ = first quartile (25th percentile)
*   $Q_3$ = third quartile (75th percentile)

**Why $Q_3 - Q_1$?**

*   $Q_1$ represents the value below which **25% of the data** falls.
*   $Q_3$ represents the value below which **75% of the data** falls.
*   The difference $Q_3 - Q_1$ captures the **range of the middle 50% of the data**, ignoring extreme low or high values.
*   This makes IQR useful for detecting outliers:
*   **Any value below $Q_1 - 1.5 \times IQR$ or above $Q_3 + 1.5 \times IQR$ is often considered an outlier.**

*[Image: Boxplot]*

```python
In [29]: import pandas as pd
         import numpy as np
         import matplotlib.pyplot as plt
         import seaborn as sns

         # Load the tips dataset
         tips = sns.load_dataset('tips')
         display(tips.head())

         # Calculate IQR for total_bill
         Q1 = tips['total_bill'].quantile(0.25)
         Q3 = tips['total_bill'].quantile(0.75)
         IQR = Q3 - Q1
         lower_bound = Q1 - 1.5 * IQR
         upper_bound = Q3 + 1.5 * IQR

         # Create the figure
         plt.figure(figsize=(12,6))

         # Histogram + KDE
         sns.histplot(tips['total_bill'], bins=20, kde=True, color='skyblue', edgecolor='black')

         # Add IQR bounds
         plt.axvline(lower_bound, color='red', linestyle='--', label='Lower Bound (IQR)')
         plt.axvline(upper_bound, color='red', linestyle='--', label='Upper Bound (IQR)')

         # Add Q1 and Q3
         plt.axvline(Q1, color='green', linestyle='-.', label='Q1 (25th percentile)')
         plt.axvline(Q3, color='green', linestyle='-.', label='Q3 (75th percentile)')

         plt.title("Histogram + KDE of Total Bill with IQR and Quartiles")
         plt.xlabel("Total Bill")
         plt.ylabel("Frequency")
         plt.legend()
         plt.tight_layout()
         plt.show()
```

| | total_bill | tip | sex | smoker | day | time | size |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 16.99 | 1.01 | Female | No | Sun | Dinner | 2 |
| **1** | 10.34 | 1.66 | Male | No | Sun | Dinner | 3 |
| **2** | 21.01 | 3.50 | Male | No | Sun | Dinner | 3 |
| **3** | 23.68 | 3.31 | Male | No | Sun | Dinner | 2 |
| **4** | 24.59 | 3.61 | Female | No | Sun | Dinner | 4 |

*[Histogram + KDE of Total Bill with IQR and Quartiles Displayed]*

## 4.2. Handling Outliers

*   Once outliers are detected, we must decide how to handle them.
*   The strategy depends on whether outliers are due to errors, rare events, or true extreme values.
*   Options include removing, capping, transforming, or imputing them are:

```python
In [30]: import pandas as pd
         import numpy as np
         import matplotlib.pyplot as plt
         from scipy.stats import zscore
         np.random.seed(42)
         df = pd.DataFrame({
             "AnnualIncome": np.concatenate([np.random.normal(50000, 8000, 100), [150000, 200000]])
         })
         Q1 = df['AnnualIncome'].quantile(0.25)
         Q3 = df['AnnualIncome'].quantile(0.75)
         IQR = Q3 - Q1
         lower_bound = Q1 - 1.5 * IQR
         upper_bound = Q3 + 1.5 * IQR
```

```python
In [31]: # Option 1: Remove Outliers
         df_cleaned = df.copy()
         df_cleaned = df[(df['AnnualIncome'] >= lower_bound) & (df['AnnualIncome'] <= upper_bound)]
         display(df_cleaned)
```

| | AnnualIncome |
|:---:|:---:|
| **0** | 53973.713224 |
| **1** | 48893.885591 |
| **2** | 55181.508305 |
| **3** | 62184.238851 |
| **4** | 48126.773002 |
| **...** | ... |
| **95** | 38291.880415 |
| **96** | 52368.962217 |
| **97** | 52088.442177 |
| **98** | 50040.907653 |
| **99** | 48123.302933 |

99 rows × 1 columns

```python
In [32]: # Option 2: Cap Outliers (Winsorization)
         df_capped = df.copy()
         df_capped['AnnualIncome'] = np.where(df['AnnualIncome'] > upper_bound, upper_bound,
                                              np.where(df['AnnualIncome'] < lower_bound, lower_bound,
```

```python
In [33]: # Visualize Cleaned Data
         plt.figure(figsize=(10, 4))
         plt.subplot(1, 2, 1)
         df_cleaned.boxplot(column='AnnualIncome')
         plt.title("After Removing Outliers")

         plt.subplot(1, 2, 2)
         df_capped.boxplot(column='AnnualIncome')
         plt.title("After Capping Outliers")
         plt.show()
```

*[Boxplots: After Removing Outliers vs After Capping Outliers]*

```python
In [34]: # Option 3: Transform Outliers (e.g., Log Transform)
         df_transformed = df.copy()
         df_transformed['Log_Income'] = np.log(df_transformed['AnnualIncome'])
         display(df_transformed[['AnnualIncome', 'Log_Income']].head())
```

| | AnnualIncome | Log_Income |
|:---:|:---:|:---:|
| **0** | 53973.713224 | 10.896252 |
| **1** | 48893.885591 | 10.797408 |
| **2** | 55181.508305 | 10.918383 |
| **3** | 62184.238851 | 11.037857 |
| **4** | 48126.773002 | 10.781594 |

```python
In [35]: # Option 4: Impute Outliers (Replace with mean or median)
         df_imputed = df.copy()
         median_income = df['AnnualIncome'].mean()
         df_imputed.loc[(df['AnnualIncome'] > upper_bound) | (df['AnnualIncome'] < lower_bound), 'AnnualIncome']
         display(df_imputed.describe())
         print(median_income)
```

| | AnnualIncome |
|:---:|:---:|
| **count** | 102.000000 |
| **mean** | 49439.120006 |
| **std** | 6916.382278 |
| **min** | 34099.448683 |
| **25%** | 45537.509376 |
| **50%** | 49568.655357 |
| **75%** | 52977.460160 |
| **max** | 64818.225476 |

51636.49790279142

```python
In [36]: # Visualize the Effect
         plt.figure(figsize=(12, 6))
         plt.subplot(2, 2, 1)
         df.boxplot(column='AnnualIncome')
         plt.title("Original Data")

         plt.subplot(2, 2, 2)
         df_cleaned.boxplot(column='AnnualIncome')
         plt.title("After Removing Outliers")

         plt.subplot(2, 2, 3)
         df_capped.boxplot(column='AnnualIncome')
         plt.title("After Capping Outliers")

         plt.subplot(2, 2, 4)
         df_imputed.boxplot(column='AnnualIncome')
         plt.title("After Imputation (Median)")

         plt.tight_layout()
         plt.show()
```

*[Boxplots Displayed: Original Data, After Removing Outliers, After Capping Outliers, After Imputation (Median)]*

## 5. Cleaning and Normalizing Text Data

*   Text data (e.g., names, addresses, comments) often contains inconsistencies:
*   Mixed casing ("Paris", "paris", "PARIS")
*   Extra spaces (" New York ")
*   Special characters ("#London!", "São Paulo*")
*   Non-standard encodings ("München" vs "Munchen")
*   Cleaning and normalizing ensures text consistency and reliability for analysis.

```python
In [37]: import pandas as pd
         # Create Sample Data with Inconsistencies
         data = {
             'City': [
                 ' New York ', 'paris', 'LONDON!', 'São Paulo', 'münchen',
                 'new york', 'Paris ', ' london ', 'Sao Paulo ', 'MUNICH']
         }
         df = pd.DataFrame(data)
         print("Original Data:")
         display(df)
```

Original Data:

| | City |
|:---:|:---:|
| **0** | New York |
| **1** | paris |
| **2** | LONDON! |
| **3** | São Paulo |
| **4** | münchen |
| **5** | new york |
| **6** | Paris |
| **7** | london |
| **8** | Sao Paulo |
| **9** | MUNICH |

```python
In [38]: from unidecode import unidecode
         # Standard Cleaning Techniques
         # a. Convert to lowercase (for uniform comparison)
         df['City_cleaned'] = df['City'].str.lower()

         # b. Strip leading/trailing whitespaces
         df['City_cleaned'] = df['City_cleaned'].str.strip()

         # c. Remove special characters using regex
         df['City_cleaned'] = df['City_cleaned'].str.replace(r'[^a-z\s]', '', regex=True)

         # Remove accented characters (é -> e, ü -> u, ñ -> n, ã -> a, ...)
         df['City_cleaned'] = df['City_cleaned'].astype(str).apply(lambda x: unidecode(x))
```

```python
In [39]: # d. Standardize known variations (custom mapping)
         df['City_cleaned'] = df['City_cleaned'].replace({
             'sao paulo': 'sao paulo',
             'munich': 'munich',
             'muenchen': 'munich'
         })
         print("\n Cleaned Data:")
         display(df)
```

Cleaned Data:

| | City | City_cleaned |
|:---:|:---:|:---:|
| **0** | New York | new york |
| **1** | paris | paris |
| **2** | LONDON! | london |
| **3** | São Paulo | so paulo |
| **4** | münchen | mnchen |
| **5** | new york | new york |
| **6** | Paris | paris |
| **7** | london | london |
| **8** | Sao Paulo | sao paulo |
| **9** | MUNICH | munich |

```python
In [40]: # Verify Unique Values Before/After Cleaning
         print("Unique city names BEFORE cleaning:")
         print(df['City'].unique())

         print("\nUnique city names AFTER cleaning:")
         print(df['City_cleaned'].unique())
```

```text
Unique city names BEFORE cleaning:
[' New York ' 'paris' 'LONDON!' 'São Paulo' 'münchen' 'new york' 'Paris '
 ' london ' 'Sao Paulo ' 'MUNICH']

Unique city names AFTER cleaning:
['new york' 'paris' 'london' 'so paulo' 'mnchen' 'sao paulo' 'munich']
```

### 5.1. Encoding Categorical Variables

*   Many Machine Learning algorithms require numerical input.
*   Categorical features (text labels like "Male", "Female", "Other") must be converted into numbers.
*   Encoding transforms text categories into numerical representations.

### a. Label Encoding (for ordinal or binary categories)

*   Converts each category into an integer label.
*   Works best when categories have an *intrinsic order* (e.g., low < medium < high).
*   Can also be used for binary features (e.g., Male/Female).

```python
In [41]: import pandas as pd
         from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
         import numpy as np
         # Create a Sample Dataset
         df = pd.DataFrame({
             'Gender': ['Male', 'Female', 'Female', 'Male', 'Other'],
             'EducationLevel': ['High School', 'Bachelor', 'Master', 'PhD', 'Bachelor'],
             'Region': ['North', 'South', 'East', 'West', 'North']
         })
         print("Original Data:")
         display(df)
```

Original Data:

| | Gender | EducationLevel | Region |
|:---:|:---:|:---:|:---:|
| **0** | Male | High School | North |
| **1** | Female | Bachelor | South |
| **2** | Female | Master | East |
| **3** | Male | PhD | West |
| **4** | Other | Bachelor | North |

```python
In [42]: le = LabelEncoder()
         df['Gender_Label'] = le.fit_transform(df['Gender'])
         print(df)
```

```text
   Gender EducationLevel Region  Gender_Label
0    Male    High School  North             1
1  Female       Bachelor  South             0
2  Female         Master   East             0
3    Male            PhD   West             1
4   Other       Bachelor  North             2
```

### b. Ordinal Encoding (when order matters)

```python
In [43]: # Example: Education level has a natural order.
         education_order = [['High School', 'Bachelor', 'Master', 'PhD']]
         oe = OrdinalEncoder(categories=education_order)
         df['Education_Ordinal'] = oe.fit_transform(df[['EducationLevel']])
         print(df)
```

```text
   Gender EducationLevel Region  Gender_Label  Education_Ordinal
0    Male    High School  North             1                0.0
1  Female       Bachelor  South             0                1.0
2  Female         Master   East             0                2.0
3    Male            PhD   West             1                3.0
4   Other       Bachelor  North             2                1.0
```

### c. One-Hot Encoding (for nominal variables — no order)

*   Creates a new binary column for each category.
*   Prevents introducing false ordinal relationships.
*   Typically used for region, color, country, etc.

```python
In [44]: df_onehot = pd.get_dummies(df, columns=['Region'], dtype=int)
         print(df_onehot)
```

```text
   Gender EducationLevel  Gender_Label  Education_Ordinal  Region_East  \
0    Male    High School             1                0.0            0
1  Female       Bachelor             0                1.0            0
2  Female         Master             0                2.0            1
3    Male            PhD             1                3.0            0
4   Other       Bachelor             2                1.0            0

   Region_North  Region_South  Region_West
0             1             0            0
1             0             1            0
2             0             0            0
3             0             0            1
4             1             0            0
```

### d. Frequency / Count Encoding (advanced, scalable)

*   Replaces each category with its frequency count.
*   Useful for high-cardinality columns (e.g., thousands of cities, product IDs).

```python
In [45]: df['Region_Freq'] = df['Region'].map(df['Region'].value_counts())
         print(df[['Region', 'Region_Freq']])
```

```text
   Region  Region_Freq
0   North            2
1   South            1
2    East            1
3    West            1
4   North            2
```

## 6. Feature Scaling and Normalization

Many machine learning algorithms are sensitive to the **scale of input features**.
Algorithms such as **K-Nearest Neighbors (KNN), Support Vector Machines (SVM), and Gradient Descent-based models** can behave unpredictably if one feature dominates due to its magnitude.

**Feature scaling and normalization** ensure that **all features contribute equally** to the model and improve **convergence and performance**.

### Common Strategies for Numerical Features

| Scaling Method | Description | Formula | Typical Use |
| :--- | :--- | :--- | :--- |
| **Min-Max Scaling** | Rescales values to a fixed range, usually [0,1] | $$x' = \frac{x-x_{min}}{x_{max}-x_{min}}$$ | Neural networks, KNN, SVM |
| **Standardization (Z-score)** | Centers data to mean=0, std=1 | $$x' = \frac{x-\mu}{\sigma}$$ | Algorithms assuming normality (Linear/Logistic Regression, PCA) |
| **Robust Scaling** | Uses median and IQR instead of mean/std | $$x' = \frac{x-\text{median}(x)}{IQR(x)}$$ | Data with outliers |
| **Normalization (L1)** | Scales vector so that sum of absolute values = 1 | $$x' = \frac{x}{\|x\|_1}$$ | Less sensitive to outliers; useful for sparse data |
| **Normalization (L2)** | Scales vector so that Euclidean norm = 1 | $$x' = \frac{x}{\|x\|_2}$$ | Distance- or similarity-based models (KNN, cosine similarity) |

```python
In [46]: import pandas as pd
         
         df = pd.DataFrame({
             'Age': [18, 22, 35, 45, 50],
             'Income': [2000, 3000, 4000, 5000, 6000]
         })
         df
```

| | Age | Income |
|:---:|:---:|:---:|
| **0** | 18 | 2000 |
| **1** | 22 | 3000 |
| **2** | 35 | 4000 |
| **3** | 45 | 5000 |
| **4** | 50 | 6000 |

```python
In [47]: df.describe()
```

| | Age | Income |
|:---:|:---:|:---:|
| **count** | 5.000000 | 5.000000 |
| **mean** | 34.000000 | 4000.000000 |
| **std** | 13.946326 | 1581.13883 |
| **min** | 18.000000 | 2000.00000 |
| **25%** | 22.000000 | 3000.00000 |
| **50%** | 35.000000 | 4000.00000 |
| **75%** | 45.000000 | 5000.00000 |
| **max** | 50.000000 | 6000.00000 |

```python
In [48]: # a. Min-Max Scaling: Rescales values to a fixed range, usually [0,1]
         from sklearn.preprocessing import MinMaxScaler
         scaler = MinMaxScaler()
         df_minmax = df.copy()
         df_minmax[['Age', 'Income']] = scaler.fit_transform(df_minmax[['Age', 'Income']])
         df_minmax
```

| | Age | Income |
|:---:|:---:|:---:|
| **0** | 0.000000 | 0.00 |
| **1** | 0.125000 | 0.25 |
| **2** | 0.531250 | 0.50 |
| **3** | 0.843750 | 0.75 |
| **4** | 1.000000 | 1.00 |

```python
In [49]: df_minmax.describe()
```

| | Age | Income |
|:---:|:---:|:---:|
| **count** | 5.000000 | 5.000000 |
| **mean** | 0.500000 | 0.500000 |
| **std** | 0.435823 | 0.395285 |
| **min** | 0.000000 | 0.000000 |
| **25%** | 0.125000 | 0.250000 |
| **50%** | 0.531250 | 0.500000 |
| **75%** | 0.843750 | 0.750000 |
| **max** | 1.000000 | 1.000000 |

```python
In [50]: # b. Standardization : Centers data to mean=0, std=1
         from sklearn.preprocessing import StandardScaler
         scaler = StandardScaler()
         df_std = df.copy()
         df_std[['Age','Income']] = scaler.fit_transform(df_std[['Age','Income']])
         df_std
```

| | Age | Income |
|:---:|:---:|:---:|
| **0** | -1.282671 | -1.414214 |
| **1** | -0.962003 | -0.707107 |
| **2** | 0.080167 | 0.000000 |
| **3** | 0.881836 | 0.707107 |
| **4** | 1.282671 | 1.414214 |

```python
In [51]: df_std.describe().round(2)
```

| | Age | Income |
|:---:|:---:|:---:|
| **count** | 5.00 | 5.00 |
| **mean** | 0.00 | 0.00 |
| **std** | 1.12 | 1.12 |
| **min** | -1.28 | -1.41 |
| **25%** | -0.96 | -0.71 |
| **50%** | 0.08 | 0.00 |
| **75%** | 0.88 | 0.71 |
| **max** | 1.28 | 1.41 |

### c. Robust Scaling

**Purpose:**
Robust scaling is used to **rescale numerical features** while **reducing the influence of outliers**.
It uses **median** and **interquartile range (IQR)** instead of mean and standard deviation. **Formula:**

$$x' = \frac{x - \text{median}(x)}{\text{IQR}(x)}$$

Where:

*   $\text{median}(x)$ = median of the feature
*   $\text{IQR}(x) = Q_3 - Q_1$ = interquartile range
    *   $Q_1$ = 25th percentile
    *   $Q_3$ = 75th percentile

```python
In [52]: #Robuste scaling
         from sklearn.preprocessing import RobustScaler
         scaler = RobustScaler()
         df_robust = df.copy()
         df_robust[['Age', 'Income']] = scaler.fit_transform(df_robust[['Age', 'Income']])
         df_robust
```

| | Age | Income |
|:---:|:---:|:---:|
| **0** | -0.739130 | -1.0 |
| **1** | -0.565217 | -0.5 |
| **2** | 0.000000 | 0.0 |
| **3** | 0.434783 | 0.5 |
| **4** | 0.652174 | 1.0 |

```python
In [53]: print(df_robust.describe().round(2))
         print(df_robust.median())
```

```text
        Age  Income
count  5.00    5.00
mean  -0.04    0.00
std    0.61    0.79
min   -0.74   -1.00
25%   -0.57   -0.50
50%    0.00    0.00
75%    0.43    0.50
max    0.65    1.00
Age       0.0
Income    0.0
dtype: float64
```

### d. Normalization (L2 / Unit Vector)

**Purpose:**

*   Normalization rescales **feature vectors** so that each row has a **unit norm** (length 1).
*   It is especially useful for **distance-based models** like KNN, cosine similarity, and clustering algorithms.
*   **Formula (L2 Norm):**

For a feature vector $\mathbf{x} = [x_1, x_2, \ldots, x_n]$:

$$\mathbf{x}' = \frac{\mathbf{x}}{\|\mathbf{x}\|_2} = \frac{\mathbf{x}}{\sqrt{x_1^2 + x_2^2 + \ldots + x_n^2}}$$

Where:

*   $\|\mathbf{x}\|_2$ is the **L2 norm** (Euclidean length) of the vector.

**Steps:**

1.  Compute the **L2 norm** of the row: $\|\mathbf{x}\|_2 = \sqrt{\sum_i x_i^2}$
2.  Divide each element of the row by the L2 norm.

```python
In [54]: # Normalization (L2 / Unit Vector)
         from sklearn.preprocessing import Normalizer
         scaler = Normalizer(norm='l2')
         df_norm = df.copy()
         df_norm[['Age', 'Income']] = scaler.fit_transform(df_norm[['Age', 'Income']])
         df_norm
```

| | Age | Income |
|:---:|:---:|:---:|
| **0** | 0.009000 | 0.999960 |
| **1** | 0.007333 | 0.999973 |
| **2** | 0.008750 | 0.999962 |
| **3** | 0.009000 | 0.999960 |
| **4** | 0.008333 | 0.999965 |

```python
In [55]: import pandas as pd
         import matplotlib.pyplot as plt
         from sklearn.preprocessing import Normalizer

         # Sample texts
         texts = [
             "I love advanced python for data science",
             "Machine learning is fun",
             "I enjoy coding"
         ]
         df = pd.DataFrame({"text": texts})

         # Clean text
         df['text_clean'] = df['text'].str.lower().str.strip()

         # Split text into individual words (as lists)
         df['words'] = df['text_clean'].str.split()

         # One-Hot Encoding using get_dummies
         # Flatten words and then pivot back to one row per text
         df_expanded = df['words'].apply(pd.Series).stack().reset_index(level=1, drop=True)
         df_onehot = pd.get_dummies(df_expanded).groupby(level=0).sum()

         # L2 Normalization
         normalizer = Normalizer(norm='l2')
         X_norm = normalizer.fit_transform(df_onehot.values)

         # Scatter plot
         plt.figure(figsize=(10,6))
         for i, row in enumerate(X_norm):
             plt.scatter(range(len(row)), row, s=100, label=f'Text {i+1}')

         plt.xticks(range(len(df_onehot.columns)), df_onehot.columns, rotation=45)
         plt.ylabel("L2-normalized values")
         plt.title("Scatter plot of L2-normalized One-Hot vectors (using get_dummies)")
         plt.legend()
         plt.grid(True)
         plt.tight_layout()
         plt.show()

         # Print DataFrame for reference
         print("=== Original Texts ===")
         print(df['text'])
         print("\n=== L2-normalized One-Hot Vectors ===")
         print(pd.DataFrame(X_norm, columns=df_onehot.columns))
```

*[Scatter plot of L2-normalized One-Hot vectors (using get_dummies) Displayed]*

```text
=== Original Texts ===
0    I love advanced python for data science
1                    Machine learning is fun
2                             I enjoy coding
Name: text, dtype: object

=== L2-normalized One-Hot Vectors ===
   advanced    coding      data     enjoy       for       fun         i        is  \
0  0.377964  0.000000  0.377964  0.000000  0.377964  0.000000  0.377964  0.000000
1  0.000000  0.000000  0.000000  0.000000  0.000000  0.500000  0.000000  0.500000
2  0.000000  0.577350  0.000000  0.577350  0.000000  0.000000  0.577350  0.000000

   learning      love   machine    python   science
0  0.000000  0.377964  0.000000  0.377964  0.377964
1  0.500000  0.000000  0.500000  0.000000  0.000000
2  0.000000  0.000000  0.000000  0.000000  0.000000
```

## L1 vs L2 Normalization

### L1 Normalization (Manhattan norm)

*   **Definition:** Scales a vector so that the **sum of the absolute values** of its components equals 1.
    $$v_{L1} = \frac{v}{\|v\|_1} = \frac{v}{|v_1|+|v_2|+\ldots+|v_n|}$$
*   **Properties:**
    *   Emphasizes sparsity
    *   Less sensitive to large values
    *   Common in **text data** (Bag-of-Words, TF-IDF)

### L2 Normalization (Euclidean norm)

*   **Definition:** Scales a vector so that its **Euclidean length (magnitude)** equals 1.
    $$v_{L2} = \frac{v}{\|v\|_2} = \frac{v}{\sqrt{v_1^2+v_2^2+\ldots+v_n^2}}$$
*   **Properties:**
    *   Preserves the **direction** of the vector
    *   Sensitive to large values
    *   Common in **cosine similarity, SVM, k-NN, PCA**

### Intuition

*   **L1:** "unit sum" → values represent proportions of total
*   **L2:** "unit length" → vector lies on a unit circle/sphere in Euclidean space