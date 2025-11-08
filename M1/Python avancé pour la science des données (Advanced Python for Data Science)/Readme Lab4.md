# Tutorial 04: Essential Python Libraries - Solutions

This repository contains the complete solutions for the exercises in Tutorial 04, focusing on NumPy, Pandas, Matplotlib, and Seaborn.

## How to Run

1.  **Install Dependencies:** Make sure you have Python installed. Then, install the required libraries using pip.
    ```bash
    pip install numpy pandas matplotlib seaborn jupyter
    ```
2.  **Run the Python Script:** Execute the complete solution script from your terminal.
    ```bash
    python solution.py
    ```
3.  **Use the Jupyter Notebook:** For an interactive experience, run Jupyter Notebook.
    ```bash
    jupyter notebook
    ```
    Then, open the `solution.ipynb` file in your browser.

---

## Exercise 01: Temperature Analysis with NumPy

This exercise involves using NumPy to analyze a dataset of temperatures from three cities over seven days.

### Task 1: Create a NumPy array `T`

**Problem:** Store the given temperature data in a NumPy array.

**Solution:**
```python
import numpy as np

temperatures = [
    [22, 25, 20], [24, 27, 21], [19, 20, 22],
    [25, 29, 28], [26, 30, 27], [21, 21, 23],
    [20, 26, 25]
]
T = np.array(temperatures)
```
-   **`import numpy as np`**: Imports the NumPy library.
-   **`T = np.array(...)`**: Converts the Python list of lists into a 2D NumPy array (a matrix) for efficient numerical operations.

### Task 2: Compute Max Temperatures

**Problem:** Find the maximum temperature for each city, each day, and overall.

**Solution:**
```python
max_temp_city = T.max(axis=0)
max_temp_day = T.max(axis=1)
overall_max_temp = T.max()
```
-   **`T.max(axis=0)`**: Computes the maximum value along `axis=0` (down the columns). Since each column represents a city, this gives the max temperature for each city.
-   **`T.max(axis=1)`**: Computes the maximum value along `axis=1` (across the rows). Each row represents a day, so this gives the max temperature for each day.
-   **`T.max()`**: Computes the maximum value in the entire array.

### Task 3: Find Day and City of Overall Max

**Problem:** Identify the specific day and city where the highest temperature was recorded.

**Solution:**
```python
max_index = np.unravel_index(np.argmax(T), T.shape)
day_of_max = max_index[0] + 1
city_of_max = cities[max_index[1]]
```
-   **`np.argmax(T)`**: Finds the linear index of the maximum value in the flattened array.
-   **`np.unravel_index(..., T.shape)`**: Converts the linear index into a tuple of array coordinates `(row, column)`.
-   **`max_index[0] + 1`**: The row index (`0` to `6`) corresponds to the day (`1` to `7`).
-   **`cities[max_index[1]]`**: The column index is used to get the city name from our `cities` list.

### Task 4: Higher Temperature between Alger and Oran

**Problem:** Create an array showing the higher temperature of the day between Alger and Oran.

**Solution:**
```python
alger_temps = T[:, 0]  # Selects all rows from column 0 (Alger)
oran_temps = T[:, 2]   # Selects all rows from column 2 (Oran)
higher_temps = np.maximum(alger_temps, oran_temps)
```
-   **`T[:, 0]`**: NumPy slicing to get all elements from the first column.
-   **`np.maximum(arr1, arr2)`**: A universal function that performs an element-wise comparison and returns an array containing the greater value from each pair.

### Task 5: Add Average Temperature Row

**Problem:** Calculate the average temperature for each city and add it as a new row to the array.

**Solution:**
```python
avg_temp_per_city = T.mean(axis=0)
T_with_avg = np.vstack([T, avg_temp_per_city])
```
-   **`T.mean(axis=0)`**: Calculates the mean for each column (city).
-   **`np.vstack([...])`**: Stacks arrays vertically. Here, it adds the new `avg_temp_per_city` array as the last row of `T`.

### Task 6: Days Annaba was Hottest

**Problem:** Find the days when Annaba's temperature was higher than both Alger's and Oran's.

**Solution:**
```python
annaba_temps = T[:, 1]
is_annaba_hottest = (annaba_temps > T[:, 0]) & (annaba_temps > T[:, 2])
hottest_days = days[is_annaba_hottest]
```
-   **`(annaba_temps > T[:, 0]) & (annaba_temps > T[:, 2])`**: Creates a boolean array. An element is `True` only if Annaba's temperature is greater than both others for that day.
-   **`days[is_annaba_hottest]`**: This is called boolean indexing. It selects elements from the `days` array where the corresponding value in `is_annaba_hottest` is `True`.

---

## Exercise 02: Student Grades Analysis with NumPy

This exercise uses NumPy and Matplotlib to perform statistical analysis and visualization on randomly generated student grades.

### Data Initialization

**Problem:** Generate a `100x5` array of random integer grades between 0 and 20.

**Solution:**
```python
np.random.seed(101)
grades_of_students = np.random.randint(0, 21, size=(100, 5))
```
-   **`np.random.seed(101)`**: Sets the seed for the random number generator. This ensures that the "random" numbers are the same every time the code runs, making the results reproducible.
-   **`np.random.randint(0, 21, ...)`**: Generates random integers. The range is `[0, 21)`, meaning integers from 0 up to (but not including) 21. `size=(100, 5)` specifies the shape of the output array.

### Basic Statistics & Visualization

**Problem:** Compute various statistics (mean, median, etc.) and visualize the grade distributions.

**Solution (Statistics):**
```python
mean_per_module = grades_of_students.mean(axis=0)
median_per_module = np.median(grades_of_students, axis=0)
thl_percentiles = np.percentile(grades_of_students[:, 0], [25, 50, 75])
```
-   **`.mean(axis=0)`**, **`.median(axis=0)`**: As in Exercise 1, `axis=0` performs the calculation down the columns (per module).
-   **`np.percentile(array, [q1, q2, ...])`**: Calculates the q-th percentiles of the data. Here, we find the 25th, 50th (median), and 75th percentiles for the first module (THL).

**Solution (Visualization):**
```python
# Bar Plot
plt.bar(modules, mean_per_module)
plt.title('Average Grade per Module')
plt.show()

# Box Plot
plt.boxplot(grades_of_students, labels=modules)
plt.title('Distribution of Grades per Module')
plt.show()
```
-   **`plt.bar()`**: Creates a bar chart, ideal for comparing a single metric (like the mean) across different categories.
-   **`plt.boxplot()`**: Creates a box plot for each module. This is excellent for visualizing the distribution of data, showing the median, quartiles, and outliers.

---

## Exercise 03: Hospital Data using Pandas

This exercise introduces Pandas for data manipulation using a hospital dataset.

### Task 1: Create a DataFrame

**Problem:** Create a Pandas DataFrame from the provided hospital data.

**Solution:**
```python
import pandas as pd
data = { ... } # Dictionary of lists
df = pd.DataFrame(data)
```
-   **`pd.DataFrame()`**: The primary constructor for creating a DataFrame. A dictionary where keys become column names and values (lists) become the column data is a common way to create one.

### Task 2 & 4: Add and Transform Columns

**Problem:** Create new columns based on existing data (`TotalCost`, `AgeGroup`, `RiskScore`, etc.).

**Solution:**
```python
# Direct calculation
df['TotalCost'] = df['DaysAdmitted'] * df['DailyFee']

# Categorization using pd.cut
age_bins = [0, 29, 50, float('inf')]
age_labels = ['Young', 'Middle', 'Senior']
df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
```
-   **`df['NewColumn'] = ...`**: The standard way to create or update a column.
-   **`pd.cut(...)`**: A powerful function for segmenting and sorting data into bins. It's perfect for creating categorical variables from continuous ones, like creating `AgeGroup` from `Age`.

### Task 6: City Summary

**Problem:** Calculate aggregate statistics (average cost, satisfaction, etc.) for each city.

**Solution:**
```python
city_summary = df.groupby('City').agg(
    AverageTotalCost=('TotalCost', 'mean'),
    ReadmissionRate=('Readmitted', 'mean')
).reset_index()
```
-   **`df.groupby('City')`**: Groups the DataFrame by unique values in the 'City' column. All subsequent operations are performed on these groups.
-   **`.agg(...)`**: The aggregate function allows you to apply multiple calculations to different columns simultaneously in a clean and readable way.
-   **`.reset_index()`**: Converts the grouped output (where 'City' is the index) back into a standard DataFrame.

### Task 9: Data Cleaning and Mapping

**Problem:** Handle missing values and map categorical data to new values.

**Solution:**
```python
# Filling missing values
df['Satisfaction'].fillna(df['Satisfaction'].mean(), inplace=True)

# Mapping values
df['Readmitted'] = df['Readmitted'].map({0: 'No', 1: 'Yes'})
```
-   **`.fillna(value, inplace=True)`**: Fills `NaN` (Not a Number) values with a specified value. Using the mean is a common imputation strategy. `inplace=True` modifies the DataFrame directly.
-   **`.map(dictionary)`**: Transforms a Series by substituting each value with the one provided in the dictionary.

---

## Exercise 04: Hospital Data Visualization

This exercise focuses on creating insightful visualizations from the hospital DataFrame using Matplotlib and Seaborn.

### Matplotlib: Total Cost per City (Bar Chart)

**Problem:** Visualize the total cost aggregated by city.

**Solution:**
```python
total_cost_per_city = df.groupby('City')['TotalCost'].sum()
plt.bar(total_cost_per_city.index, total_cost_per_city.values)
# Code to add labels and title
plt.show()
```
- This follows a common pattern: first, **aggregate the data** using Pandas (`.groupby().sum()`), then **plot the result** using Matplotlib.

### Seaborn: Correlation Heatmap

**Problem:** Visualize the correlation between all numeric variables.

**Solution:**
```python
import seaborn as sns
numeric_df = df.select_dtypes(include=np.number)
corr_matrix = numeric_df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
```
-   **`df.select_dtypes(...)`**: Selects only the numeric columns to calculate correlations.
-   **`.corr()`**: Computes the pairwise correlation of columns, returning a correlation matrix.
-   **`sns.heatmap(...)`**: Creates a color-coded matrix plot. `annot=True` writes the data value in each cell, and `cmap` sets the color map.

### Seaborn: Pair Relationships

**Problem:** Explore relationships between multiple variables at once, segmented by city.

**Solution:**
```python
sns.pairplot(df, vars=['Age', 'DaysAdmitted', 'TotalCost'], hue='City')
```
-   **`sns.pairplot()`**: Creates a grid of axes such that each numeric variable in `data` will be shared across the y-axes across a single row and the x-axes across a single column. The diagonal plots are histograms, and the off-diagonals are scatter plots.
-   **`hue='City'`**: A powerful parameter that colors the data points based on the 'City' column, allowing for easy comparison between categories.

### Seaborn: Combined Dashboard

**Problem:** Create a single figure with multiple different plots (subplots) to provide a comprehensive overview.

**Solution:**
```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1 on axes[0, 0]
sns.barplot(ax=axes[0, 0], data=df, x='City', y='Satisfaction')

# Plot 2 on axes[0, 1]
sns.boxplot(ax=axes[0, 1], data=df, x='RiskCategory', y='RiskScore')

# ... and so on for other plots
plt.tight_layout()
plt.show()
```
-   **`plt.subplots(rows, cols, ...)`**: Creates a figure and a grid of subplots (axes). It returns the figure and an array of `axes` objects.
-   **`ax=axes[r, c]`**: The key to creating dashboards. Most Seaborn (and Matplotlib) plotting functions accept an `ax` argument, which tells them exactly which subplot to draw on.
-   **`plt.tight_layout()`**: Automatically adjusts subplot params so that the subplots fit into the figure area nicely.