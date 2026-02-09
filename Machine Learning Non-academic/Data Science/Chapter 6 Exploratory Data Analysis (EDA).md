

**Exploratory Data Analysis (EDA)** is the initial step in which a dataset is examined in depth before performing any formal modeling or statistical testing.
The main purpose is to :

*   Understand the structure of the data,
*   Identify key characteristics, and
*   Reveal insights that will guide the next stages of data preparation and modeling.

## EDA Checklist

### 1. Understand the Dataset

*   Load dataset & check shape (`df.shape`)
*   Preview data (`df.head()`, `df.tail()`)
*   Check data types (`df.dtypes`)
*   Check duplicates (`df.duplicated().sum()`)
*   Understand columns (data dictionary)

### 2. Summary Statistics

*   Describe numerical features (`df.describe()`)
*   Summarize categorical features (`df['col'].value_counts()`)
*   Check missing values (`df.isnull().sum()`)
*   Check unique values (`df['col'].nunique()`)

### 3. Data Cleaning

*   Handle missing values (drop, impute, interpolate)
*   Handle duplicates
*   Correct data types (e.g., `object` → `datetime`)
*   Standardize units if needed

### 4. Univariate Analysis

*   Visualize numerical features (histogram, boxplot, etc.)
*   Check skewness & kurtosis
*   Visualize categorical features (countplot, pie chart)

*   Identify outliers

### 5. Bivariate Analysis

*   Numerical vs Numerical (scatter plot, correlation matrix, pairplot)
*   Numerical vs Categorical (boxplot, violin plot, bar chart)
*   Categorical vs Categorical (cross-tab, stacked bar, heatmap)

### 6. Multivariate Analysis

*   Correlation heatmap (Pearson/Spearman)
*   Pairplots or scatter matrix
*   Grouped analysis (mean, median by category)
*   Pivot tables for aggregation

## 3. Steps of Exploratory Data Analysis (EDA)

### 3.0. Preparing the Environment

*   We use popular Python libraries
*   We set visualization styles for consistency

```python
In [1]: import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set(style="whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
```

### 3.1. Understand the Dataset

```python
In [2]: df = sns.load_dataset('iris')
```
![No description has been provided for this image]

```python
In [3]: df.shape # (rows, columns)
```

```
Out[3]: (150, 5)
```

```python
In [4]: df.columns # column names
        df.info() # data types and non-null counts
        df.head() # preview first few rows
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 150 entries, 0 to 149
Data columns (total 5 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   sepal_length  150 non-null    float64
 1   sepal_width   150 non-null    float64
 2   petal_length  150 non-null    float64
 3   petal_width   150 non-null    float64
 4   species       150 non-null    object 
dtypes: float64(4), object(1)
memory usage: 6.0+ KB
```

`Out[4]:`

| | sepal_length | sepal_width | petal_length | petal_width | species |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | 5.1 | 3.5 | 1.4 | 0.2 | setosa |
| **1** | 4.9 | 3.0 | 1.4 | 0.2 | setosa |
| **2** | 4.7 | 3.2 | 1.3 | 0.2 | setosa |
| **3** | 4.6 | 3.1 | 1.5 | 0.2 | setosa |
| **4** | 5.0 | 3.6 | 1.4 | 0.2 | setosa |

### 3.2. Summary Statistics

```python
In [5]: df.describe()
```

`Out[5]:`

| | sepal_length | sepal_width | petal_length | petal_width |
| :--- | :--- | :--- | :--- | :--- |
| **count** | 150.000000 | 150.000000 | 150.000000 | 150.000000 |
| **mean** | 5.843333 | 3.057333 | 3.758000 | 1.199333 |
| **std** | 0.828066 | 0.435866 | 1.765298 | 0.762238 |
| **min** | 4.300000 | 2.000000 | 1.000000 | 0.100000 |
| **25%** | 5.100000 | 2.800000 | 1.600000 | 0.300000 |
| **50%** | 5.800000 | 3.000000 | 4.350000 | 1.300000 |
| **75%** | 6.400000 | 3.300000 | 5.100000 | 1.800000 |
| **max** | 7.900000 | 4.400000 | 6.900000 | 2.500000 |

```python
In [6]: df['species'].value_counts()
```

```
Out[6]: species
        setosa        50
        versicolor    50
        virginica     50
        Name: count, dtype: int64
```

```python
In [7]: df.isnull().sum()
```

```
Out[7]: sepal_length    0
        sepal_width     0
        petal_length    0
        petal_width     0
        species         0
        dtype: int64
```

```python
In [8]: df['species'].nunique()
```

```
Out[8]: 3
```

```python
In [9]: duplicates = df.duplicated()
        print("Number of duplicate rows:", duplicates.sum())
```

```
Number of duplicate rows: 1
```

```python
In [10]: print(df[duplicates])
```

```
     sepal_length  sepal_width  petal_length  petal_width    species
142           5.8          2.7           5.1          1.9  virginica
```

```python
In [11]: df_clean = df.drop_duplicates()
         print("Shape before:", df.shape)
```

```
Shape before: (150, 5)
```

```python
In [12]: df.dtypes.value_counts()
```

```
Out[12]: float64    4
         object     1
         Name: count, dtype: int64
```

### Check and Validate Data Types

*   Identify numerical, categorical, datetime, and text variables.
*   Convert incorrect types.
*   Ensure consistency and correct formatting.

### Identify Missing Values

*   Count missing values per feature.
*   Visualize missingness if needed.
*   Decide on treatment: removal, imputation, or leaving missing values.

```python
In [13]: # missingno is a Python library for visualizing missing data,
         #often used with seaborn for quick and informative EDA plots.
         #!pip install missingno seaborn
```

## 3.4. Univariate Analysis

*   a- Visualize numerical features (histogram, boxplot, density plot)
*   b- Check skewness & kurtosis
*   c- Visualize categorical features (countplot, pie chart)
*   d- Identify outliers

### a. Numerical Variables

*   **histograms** used to understand data distribution and skewness.
*   **boxplots** used to quickly detect outliers and spread.

```python
In [14]: import seaborn as sns
         import matplotlib.pyplot as plt

         iris = sns.load_dataset('iris')
         sns.histplot(iris['sepal_length'], kde=True)
         plt.title("Sepal Length Distribution")
```

```
Out[14]: Text(0.5, 1.0, 'Sepal Length Distribution')
```

*(Histogram Chart: Sepal Length Distribution)*

Boxplots help identify outliers and spread

```python
In [15]: sns.boxplot(x=iris['sepal_length'])
         plt.title("Sepal Length Boxplot")
         plt.show()
```

*(Boxplot Chart: Sepal Length Boxplot)*

### - b- Check skewness & kurtosis

### Definitions

Skewness: measures the asymmetry of the distribution.

*   skew > 0 : right-skewed (long tail on the right)
*   skew < 0 : left-skewed (long tail on the left)
*   skew ≈ 0 : symmetric distribution

Kurtosis: measures the "tailedness" of the distribution.

*   kurt > 0 : heavy tails (more outliers than normal)
*   kurt < 0 : light tails (fewer outliers than normal)
*   kurt ≈ 0 : similar to normal distribution

```python
In [16]: from scipy.stats import skew, kurtosis

         # Calculation on numerical features
         num_cols = df.select_dtypes(include=['float64']).columns
         for col in num_cols:
             s = skew(df[col])
             k = kurtosis(df[col]) # Fisher's definition: 0 for normal dist
             print(f"{col} -> Skewness: {s:.2f}, Kurtosis: {k:.2f}")
```

```
sepal_length -> Skewness: 0.31, Kurtosis: -0.57
sepal_width -> Skewness: 0.32, Kurtosis: 0.18
petal_length -> Skewness: -0.27, Kurtosis: -1.40
petal_width -> Skewness: -0.10, Kurtosis: -1.34
```

### Skewness and Kurtosis: Recommended Actions

| Measure | Value | Description | Recommended Action |
| :--- | :--- | :--- | :--- |
| **Skewness** | ≈ 0 | Symmetric distribution | No action needed; parametric methods are fine |
| **Skewness** | > 0 | Right-skewed (long tail on the right) | Transform variable: log, sqrt, etc. |
| **Skewness** | < 0 | Left-skewed (long tail on the left) | Transform variable: inverse, square, etc. |
| **Kurtosis** | ≈ 0 | Mesokurtic (like normal) | No action needed |
| **Kurtosis** | > 0 | Leptokurtic (sharp peak, heavy tails) | Check for outliers; remove or transform if necessary |
| **Kurtosis** | < 0 | Platykurtic (flat, light tails) | Usually okay; watch for very dispersed data |

### c. Analyzing Categorical Features

For categorical variables, frequency counts and bar charts are informative

```python
In [17]: iris['species'].value_counts().plot(kind='bar')
         plt.title('Number of Records by Species')
         plt.xlabel('Species')
         plt.ylabel('Count')
         plt.show()
```

*(Bar Chart: Number of Records by Species)*

## 3.5. Bivariate Analysis

Bivariate analysis explores the relationship between two variables. It helps reveal associations, trends, and potential predictive relationships.

*   a-Numerical vs Numerical (scatter plot, correlation matrix, pairplot)
*   b-Numerical vs Categorical (boxplot, violin plot, bar chart)
*   c-Categorical vs Categorical (cross-tab, stacked bar, heatmap)

### b.1.- Numerical vs. Numerical : Scatter Plot

```python
In [18]: sns.scatterplot(x='sepal_length', y='sepal_width', hue='species', data=iris)
         plt.title("Sepal Length vs Sepal Width")
         plt.show()
```

*(Scatter Plot: Sepal Length vs Sepal Width)*

### b.1.- Numerical vs. Numerical : Correlation

Correlation measures the **linear relationship** between two numerical variables. It tells us how much one variable changes when the other changes.

**Pearson Correlation (default in pandas `corr()` ):**

$r_{XY} = \frac{Cov(X,Y)}{\sigma_X \sigma_Y}$

Where:

*   $r_{XY}$ = correlation coefficient between X and Y
*   $Cov(X, Y)$ = covariance of X and Y
*   $\sigma_X, \sigma_Y$ = standard deviations of X and Y

**Interpretation of r:**

*   r = 1 → perfect positive correlation
*   r = -1 → perfect negative correlation
*   r = 0 → no linear correlation

## Types of Correlation

| Correlation | Description | Use Case |
| :--- | :--- | :--- |
| **Pearson** | Measures the **linear relationship** between two continuous variables. Values range from -1 to 1. | Use when both variables are continuous and relationship is linear. |
| **Spearman** | Measures the **monotonic relationship** (based on ranks) between two variables. | Use when relationship is non-linear but monotone, or for ordinal data. |
| **Kendall** | Measures the **ordinal association** between two variables using concordant and discordant pairs. | Use for small datasets or when you want a robust rank correlation. |

### b.2- Categorical vs. Numerical

**Boxplots** and **violin** plots help visualize how numerical features vary across species (the categorical variable):

```python
In [19]: sns.boxplot(x='species', y='sepal_length', data=iris)
         plt.title("Sepal Length by Species — Boxplot")
         plt.show()

         sns.violinplot(x='species', y='petal_length', data=iris)
         plt.title("Petal Length by Species — Violin Plot")
         plt.show()
```

*(Boxplot Chart: Sepal Length by Species — Boxplot)*

*(Violin Plot Chart: Petal Length by Species — Violin Plot)*

### b.3. Categorical vs. Categorical

*   Use **cross-tabulations** or **heatmaps** to analyze interactions between categorical variables.
*   We convert a numerical variable into categories, cross-tabulate it with another categorical variable, and visualize the counts using a stacked bar chart to explore relationships between the two categorical features.

```python
In [20]: import pandas as pd

         # Create bins for sepal_length
         iris['sepal_length_bin'] = pd.cut(iris['sepal_length'], bins=3, labels=['Short', 'Medium', 'Long'])

         ct = pd.crosstab(iris['species'], iris['sepal_length_bin'])
         ct.plot(kind='bar', stacked=True)
         plt.title("Species vs. Sepal Length Category — Stacked Bar Chart")
         plt.xlabel("Species")
         plt.ylabel("Count")
         plt.show()
```

*(Stacked Bar Chart: Species vs. Sepal Length Category)*

```python
In [21]: # Heatmap for categorical interaction
         sns.heatmap(ct, cmap='Blues', annot=True)
         plt.title("Heatmap — Species vs. Sepal Length Category")
         plt.xlabel("Sepal Length Category")
         plt.ylabel("Species")
         plt.show()
```

*(Heatmap Chart: Heatmap — Species vs. Sepal Length Category)*

## 3.6. Multivariate Analysis

Multivariate visualizations help uncover complex interactions between three or more variables

### c1. Pair Plots

*   Pair plots allow for the simultaneous visualization of relationships between multiple numerical variables.
*   Each cell in the pair plot shows a scatter plot (or histogram on the diagonal) for a pair of variables, helping identify correlations, linearity, and potential groupings.

```python
In [22]: sns.pairplot(df, hue='species', diag_kind='kde', height=2.5)
         plt.suptitle("Scatter plots et distributions des variables d'Iris", y=1.02)
         plt.show()
```

*(Pair Plot Matrix)*

### c.2 Facet Grids

*   Faceting allows us to see how relationships between numerical variables change across different species.
*   sns.FacetGrid creates a grid of plots based on a categorical variable (species).
*   map_dataframe(sns.scatterplot, ...) draws the scatter plot in each facet.
*   This helps detect patterns or correlations that may differ for each species, e.g., some species may have a tighter relationship between sepal length and width than others.

```python
In [23]: # FacetGrid: separate plots by species
         g = sns.FacetGrid(iris, col='species') # One column per species
         g.map_dataframe(sns.scatterplot, x='sepal_length', y='sepal_width')

         # Add title
         g.set_axis_labels("Sepal Length", "Sepal Width")
         g.fig.suptitle("Sepal Length vs. Sepal Width by Species", y=1.05)
         plt.show()
```

*(Facet Grid Charts: Sepal Length vs. Sepal Width by Species)*

### c.3. Grouped Aggregations

*   Grouping data by one or more categorical variables and then analyzing numerical trends helps in understanding how different segments behave.
*   We can also visualize such groupings using grouped bar plots or facet grids.

```python
In [24]: grouped = iris.groupby('species')['sepal_length'].mean()
         print(grouped)

         # Bar plot
         grouped.plot(kind='bar', color=['skyblue', 'lightgreen', 'salmon'])
         plt.ylabel('Mean Sepal Length')
         plt.title('Average Sepal Length by Species')
         plt.show()
```

```
species
setosa        5.006
versicolor    5.936
virginica     6.588
Name: sepal_length, dtype: float64
```

*(Bar Chart: Average Sepal Length by Species)*