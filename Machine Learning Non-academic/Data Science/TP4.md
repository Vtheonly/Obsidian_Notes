

## Exercise 01: Temperature Analysis with NumPy

### Problem Statement

We have the following table of daily temperatures (°C) measured over **7 days** in **3 cities**:

| Day | Alger | Annaba | Oran |
| :-- | :---- | :----- | :--- |
| 1   | 22    | 25     | 20   |
| 2   | 24    | 27     | 21   |
| 3   | 19    | 20     | 22   |
| 4   | 25    | 29     | 28   |
| 5   | 26    | 30     | 27   |
| 6   | 21    | 21     | 23   |
| 7   | 20    | 26     | 25   |

### Tasks

1.  Create a NumPy array `T` with the data above.
2.  Compute and display:
    *   the maximum temperature for each city,
    *   the maximum temperature for each day,
    *   the overall maximum temperature in the table.
3.  Find the **day and city** where the overall maximum temperature occurred.
4.  Create a new array showing, for each day, the **higher temperature between Alger and City Oran** (use `np.maximum`).
5.  Add a **new row** representing the average temperature of each city over the 7 days.
6.  Determine the **days where Annaba was the hottest city** (i.e., City Annaba's temperature exceeded both Alger and Oran).

## Exercise 02: Student Grades Analysis with NumPy

### Problem Statement

You are given the grades of **100 students** in **5 modules**:

**Modules**: `THL`, `DSS`, `DB`, `SE`, `RE`

Grades are integers between **0 and 20**. Your task is to perform statistical analysis and visualization using only **NumPy** and **Matplotlib**.
You will compute averages, variances, and standard deviations, apply boolean masks to filter grades, and visualize module comparisons using plots.

### Tasks

#### Data Initialization

1.  Generate the grades of **100 students × 5 modules** using `np.random.randint`.
2.  Fix the random seed with `np.random.seed(101)` to ensure reproducibility.
3.  Store the grades in a NumPy array called `grades_of_students`.
4.  Define the list of modules: `['THL', 'DSS', 'DB', 'SE', 'RE']`.
5.  Display a preview of the grades (first 5 students).

#### Basic Statistics

1.  Compute the **mean grade per student**.
2.  Compute the **mean grade per module**.
3.  Compute the **median grade per module**.
4.  Compute the **variance** and **standard deviation** for each module.
5.  Find the **overall minimum and maximum grade** in the dataset.
6.  Compute the 25th, 50th, and 75th percentiles for the module THL.

#### Boolean Mask and Filtering

1.  Create a **boolean mask** indicating grades between **10 and 15**.
2.  Count how many grades fall within this range.
3.  Extract all grades between 10 and 15 using the mask.

#### Visualization (Comparison Between Modules)

1.  Use a **bar plot** to compare the **average grades per module**.
2.  Plot a **box plot** (or multiple histograms) to show the distribution of grades per module.
3.  Customize titles, labels, and colors for clarity.

#### Extra practice

1.  Identify students who have **all grades above 15**.
2.  Compute the **top 5 students** with the highest average grades.
3.  Find the module with the **highest average grade**.

## Exercice 03: Hospital Data (Alger, Annaba, Oran) using Pandas

### Tasks

1.  Create a DataFrame with the following columns:
    *   `City`, `Department`, `Age`, `DaysAdmitted`, `DailyCost`, `Satisfaction`, `Readmitted`

| City   | Department  | Age | DaysAdmitted | DailyCost | Satisfaction | Readmitted |
| :----- | :---------- | :-: | :----------: | :-------: | :----------: | :--------: |
| Alger  | Cardiology  | 45  |      5       |    200    |     4.5      |     0      |
| Annaba | Neurology   | 60  |      8       |    300    |     3.8      |     1      |
| Oran   | Orthopedics | 30  |      3       |    150    |     4.2      |     0      |
| Alger  | Cardiology  | 50  |      7       |    220    |     4.0      |     0      |
| Oran   | Neurology   | 40  |      4       |    280    |     4.1      |     1      |
| Annaba | Orthopedics | 70  |      6       |    160    |     3.5      |     1      |
| Alger  | Cardiology  | 35  |      2       |    210    |     4.7      |     0      |
| Oran   | Neurology   | 55  |      9       |    290    |     3.9      |     1      |

2.  **Add columns:**
    *   `TotalCost` = `DaysAdmitted` \* `DailyCost`
    *   `AgeGroup`:
        *   "Young" if Age < 30
        *   "Middle" if 30 ≤ Age ≤ 50
        *   "Senior" if Age > 50

3.  **Add, Rename, and Delete Columns:**
    *   Add a column for a 10% **Bonus** based on the daily cost
    *   Rename the column `DailyCost` → `DailyFee`
    *   Delete the column `Bonus`

4.  **Data Transformation:**
    *   Create a column `HighCost` showing **"Yes"** if total cost exceeds 60,000, otherwise **"No"**
    *   Create a column `SatisfactionLevel`:
        *   "Excellent" if Satisfaction ≥ 8
        *   "Average" if 5 ≤ Satisfaction < 8
        *   "Poor" if Satisfaction < 5

5.  **Ranking and Sorting:**
    *   Add a column ranking patients by **TotalCost** (highest rank = 1)
    *   Sort the dataset by **RiskScore** in descending order

6.  **City Summary:**
    For each city, calculate:
    *   Average total cost
    *   Average satisfaction
    *   Readmission rate (percentage of patients readmitted)

7.  **Risk Score Calculation:**
    Use the formula:
    `RiskScore = (DaysAdmitted \times 0.4) + (Age \times 0.3) + (100 - Satisfaction \times 10) \times 0.3`
    Then classify into a new column `RiskCategory`:
    *   "High" if RiskScore > 60
    *   "Medium" if 40 ≤ RiskScore ≤ 60
    *   "Low" otherwise

8.  Find the city with the **highest average RiskScore**.

9.  **Apply Data Cleaning and Mapping**
    *   Replace missing or invalid `Satisfaction` values with the mean of the column
    *   Map city names (`Alger`, `Annaba`, `Oran`) to region codes (e.g., DZ-16, DZ-23, DZ-31)
    *   Replace binary values in `Readmitted` column: 0 → "No", 1 → "Yes"

10. **Pivot Analysis**
    *   Create a pivot table showing average `TotalCost` and `Satisfaction` for each city and department
    *   Compare the result with a grouped summary to discuss the difference between both methods

11. **Export Results**
    *   Export the main dataset to `hospital_risk.csv`
    *   Export the city summary to `city_summary.csv`

## Exercise 04: Hospital Data Visualization — Matplotlib vs Seaborn

### Matplotlib

#### 1. Total Cost per City

*   Use a **bar chart** to show total cost per city.
*   Add axis labels, a title, and numerical annotations above each bar.
*   Change the bar color manually (e.g., 'orange' or 'skyblue').

#### 2. Satisfaction Distribution

*   Use a **histogram** (`ax.hist`) to visualize satisfaction scores.
*   Add mean and median lines with annotations.
*   Adjust the number of bins to explore visual differences.

#### 3. Cost vs Satisfaction Scatter Plot

*   Plot `TotalCost` vs `Satisfaction`.
*   Use `ax.scatter` with custom markers and colors.
*   Highlight patients with `HighCost == "Yes"` in a different color.
*   Discuss the readability of the figure.

#### 4. Subplots by City

*   Use `plt.subplots(1, 3)` to plot average satisfaction per department for each city (`Alger`, `Annaba`, `Oran`).
*   Ensure consistent y-axis limits for comparison.
*   Add individual titles and one global figure title.

### Seaborn

#### 1. Compare City Performances

*   Create a Seaborn **barplot** showing average `TotalCost` and `Satisfaction` by `City`.
*   Use `sns.barplot()` with `hue='Department'` for multi-dimensional insight.
*   Discuss which city performs best economically and in satisfaction.

#### 2. Risk Distribution

*   Use `sns.boxplot()` to show the distribution of `RiskScore` across cities.
*   Use `sns.violinplot()` to add richer visual detail.
*   Compare both visuals and discuss what each reveals.

#### 3. Correlations

*   Use `sns.heatmap()` to visualize correlations between numeric variables.
*   Comment on which factors are most related to `RiskScore` and `Readmission`.

#### 4. Pair Relationships

*   Use `sns.pairplot()` with selected variables: `Age`, `DaysAdmitted`, `TotalCost`, `RiskScore`.
*   Use `hue='City'` to identify differences across cities.
*   Discuss one key insight revealed by this visualization.

#### 5. Combined dashboard

Use Seaborn to build a **combined dashboard**:

*   Subplot 1: Barplot of average satisfaction per city.
*   Subplot 2: Boxplot of `RiskScore` by `RiskCategory`.
*   Subplot 3: Heatmap of correlations.
*   Subplot 4: Countplot of readmissions (`Yes` / `No`) per city.

Add a shared title:
**"Hospital Risk and Satisfaction Overview"**

***




## Monthly Sales Analysis (NumPy + Pandas + Matplotlib + Seaborn)

### Objective

The goal is to **generate, analyze, and visualize monthly sales data** for four products over one year, and extract key business insights using **NumPy, Pandas, Matplotlib, and Seaborn.**

### Project Structure

```
project_sales/
├── notebook.ipynb         # Main notebook with all analysis and visualizations
├── utils.py               # Functions for data generation
└── data/
    ├── initial.csv        # Raw generated dataset
    ├── final.csv          # DataFrame with calculated metrics
    └── output.csv         # Final results including pivot tables
```

### Instructions

#### 1. Data Generation

*   Generate a series of monthly dates for one year (e.g., from '2025-01-01' to '2025-12-01').
*   Define in `utils.py` a function `generate_random_sales(min_val, max_val, size)` that returns a random NumPy array of integers between `min_val` and `max_val` for the given size.
*   Use this function to generate random monthly sales (integers) for 12 months for four products:
    *   Product A: 50-100 units
    *   Product B: 30-80 units
    *   Product C: 20-60 units
    *   Product D: 10-50 units
*   Create a DataFrame with columns: `Date`, `Product_A`, `Product_B`, `Product_C`, `Product_D`.
*   Save this initial dataset as `initial.csv`.

#### 2. Build DataFrame

*   Create a Pandas DataFrame with columns: `Month`, `Product_A`, `Product_B`, `Product_C`, `Product_D`.
*   Compute monthly metrics:
    *   `Total_Sales`: sum of all products per month
    *   `Average_Sales`: mean sales per month
    *   `Month_over_Month_Growth`: percent change of `Total_Sales` vs previous month
*   Assign each month to a quarter:
    *   Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec
*   Add additional columns:
    *   `Max_Sales_Product`: product with the highest sales each month
    *   `Min_Sales_Product`: product with the lowest sales each month
*   Save this updated DataFrame as `final.csv`.

#### 3. Pivot Tables & Summaries

*   Compute average sales per quarter for each product and total sales using a pivot table.
*   Compute total sales per quarter.
*   Save the final output including pivot tables as `output.csv`.

#### 4. Key Insights

*   Identify the **best month** (highest total sales)
*   Identify the **best product** (highest cumulative annual sales)
*   Identify the **best quarter** (highest total sales)

#### 5. Visualizations

*   Line chart for each product across months
*   Stacked bar chart of total monthly sales by product (annotate best month)
*   Seaborn heatmap: monthly sales of each product
*   Seaborn boxplot: distribution of sales per product

#### 6. Conclusion Questions

*   Which **product** contributes the most to overall sales throughout the year?
*   Which **quarter** performs best and why might that be?
*   How could this information be used to **improve sales strategy** for the next year?

---






## Part 2: Solution for the Monthly Sales Analysis Project

This solution will guide you through completing the **Monthly Sales Analysis** project step-by-step.

### Project Setup

First, create the project structure as specified. Your folder should look like this:

```
project_sales/
├── notebook.ipynb
├── utils.py
└── data/
```

### 1. Data Generation

#### File: `utils.py`

This file will contain the function to generate random sales data.

```python
# utils.py

import numpy as np

def generate_random_sales(min_val, max_val, size=12):
    """
    Generates a NumPy array of random integers within a specified range.

    Args:
        min_val (int): The minimum value for the random sales (inclusive).
        max_val (int): The maximum value for the random sales (exclusive).
        size (int): The number of random sales figures to generate (default is 12).

    Returns:
        np.ndarray: A NumPy array containing the random sales data.
    """
    # Use numpy's random integer generator. We add 1 to max_val to make it inclusive.
    return np.random.randint(min_val, max_val + 1, size)

```

**Tip:** Using `np.random.randint` is efficient for generating integer arrays. Defining this in a separate `utils.py` file promotes code reusability and organization, a key practice in larger projects.

#### File: `notebook.ipynb`

This is the main notebook where we will perform all the analysis. The following code blocks should be run in separate cells.

```python
# Cell 1: Import Libraries and the custom function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import generate_random_sales # Import our function

# Set a random seed for reproducibility
np.random.seed(42)
```

**How it works:** We import all the necessary libraries. `from utils import generate_random_sales` makes our custom function available in the notebook. Setting a `seed` ensures that our "random" data is the same every time we run the notebook, which is crucial for getting reproducible results.

```python
# Cell 2: Generate Dates and Sales Data
# Generate a series of 12 monthly dates for the year 2025
dates = pd.date_range(start='2025-01-01', periods=12, freq='MS')

# Define product sales ranges
sales_ranges = {
    'Product_A': (50, 100),
    'Product_B': (30, 80),
    'Product_C': (20, 60),
    'Product_D': (10, 50)
}

# Generate sales data for each product using our function
sales_data = {
    product: generate_random_sales(min_val, max_val)
    for product, (min_val, max_val) in sales_ranges.items()
}

# Create the initial DataFrame
initial_df = pd.DataFrame(sales_data)
initial_df.insert(0, 'Date', dates) # Insert Date as the first column

# Display the DataFrame
print("Initial Generated Data:")
print(initial_df)
```

**How it works:**
*   `pd.date_range` is a powerful Pandas function to create a sequence of dates. `freq='MS'` means 'Month Start'.
*   We use a dictionary comprehension to efficiently generate data for all products by calling our `generate_random_sales` function for each item in the `sales_ranges` dictionary.
*   Finally, we assemble the data into a Pandas DataFrame.

```python
# Cell 3: Save the initial dataset
# Create the data directory if it doesn't exist
import os
if not os.path.exists('data'):
    os.makedirs('data')

# Save the DataFrame to a CSV file
initial_df.to_csv('data/initial.csv', index=False)
print("\nInitial data saved to data/initial.csv")
```

**Tip:** `index=False` is important when saving to CSV to prevent Pandas from writing the DataFrame index as an unnamed column in the file.

### 2. Build DataFrame (Analysis)

Now we will read the raw data and compute the required metrics.

```python
# Cell 4: Load data and compute metrics
df = pd.read_csv('data/initial.csv', parse_dates=['Date'])

# Create a 'Month' column for easier labeling (e.g., 'Jan', 'Feb')
df['Month'] = df['Date'].dt.strftime('%b')

# Set Month as the index for easier plotting and calculations
df.set_index('Month', inplace=True)

# Select only product columns for calculations
product_cols = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
df_products = df[product_cols]

# Compute Total_Sales and Average_Sales
df['Total_Sales'] = df_products.sum(axis=1)
df['Average_Sales'] = df_products.mean(axis=1)

# Compute Month-over-Month Growth in Total Sales
# .pct_change() calculates the percentage change. We multiply by 100 and round.
df['Month_over_Month_Growth'] = df['Total_Sales'].pct_change().fillna(0) * 100

# Display the DataFrame with new metrics
print("DataFrame with Monthly Metrics:")
df[['Total_Sales', 'Average_Sales', 'Month_over_Month_Growth']].round(2)
```

**How it works:**
*   `axis=1` tells Pandas to perform the sum and mean operations row-wise (across columns).
*   `.pct_change()` is a convenient way to calculate the growth rate. We use `.fillna(0)` because the first month has no previous month to compare against, resulting in a `NaN` (Not a Number) value.

```python
# Cell 5: Assign Quarters and find Max/Min Sales Product
# Assign each month to a quarter
month_to_quarter = df['Date'].dt.quarter
df['Quarter'] = 'Q' + month_to_quarter.astype(str)

# Find the product with the highest and lowest sales each month
df['Max_Sales_Product'] = df_products.idxmax(axis=1)
df['Min_Sales_Product'] = df_products.idxmin(axis=1)

# Display the final DataFrame
print("Final DataFrame with all metrics:")
print(df)
```

**How it works:**
*   `.dt.quarter` directly extracts the quarter (1, 2, 3, or 4) from the date column.
*   `idxmax()` and `idxmin()` are incredibly useful functions that return the *index label* (in this case, the column name) of the maximum or minimum value in each row.

```python
# Cell 6: Save the final DataFrame
df.to_csv('data/final.csv')
print("\nFinal data saved to data/final.csv")
```

### 3. Pivot Tables & Summaries

We use pivot tables to summarize data, which is excellent for reporting.

```python
# Cell 7: Create pivot table for average sales per quarter
quarterly_pivot = pd.pivot_table(
    df,
    index='Quarter',
    values=product_cols,
    aggfunc='mean' # We want the average sales
).round(2)

print("Pivot Table: Average Sales per Product per Quarter")
print(quarterly_pivot)

# Cell 8: Compute total sales per quarter
quarterly_total_sales = df.groupby('Quarter')['Total_Sales'].sum().to_frame()
print("\nTotal Sales per Quarter:")
print(quarterly_total_sales)
```

**How it works:**
*   `pd.pivot_table` reshapes the data based on the `index`, `values`, and an aggregation function (`aggfunc`). It's perfect for this kind of summary.
*   `df.groupby('Quarter')` is another powerful way to summarize data. Here, we group by quarter and then calculate the sum of `Total_Sales` for each group.

```python
# Cell 9: Save the pivot tables to output.csv
with open('data/output.csv', 'w') as f:
    f.write("Pivot Table: Average Sales per Product per Quarter\n")
    quarterly_pivot.to_csv(f)
    f.write("\nTotal Sales per Quarter\n")
    quarterly_total_sales.to_csv(f)

print("\nPivot tables saved to data/output.csv")
```

**Tip:** Writing multiple summaries to one file can be done by opening the file in write mode (`'w'`) and writing each piece sequentially. Adding titles makes the output CSV more readable.

### 4. Key Insights

Let's programmatically find the answers to our business questions.

```python
# Cell 10: Identify Key Insights
# Best Month (highest total sales)
best_month = df['Total_Sales'].idxmax()
best_month_sales = df['Total_Sales'].max()

# Best Product (highest cumulative annual sales)
best_product = df[product_cols].sum().idxmax()
best_product_sales = df[product_cols].sum().max()

# Best Quarter (highest total sales)
best_quarter = quarterly_total_sales['Total_Sales'].idxmax()
best_quarter_sales = quarterly_total_sales['Total_Sales'].max()

print("--- Key Business Insights ---")
print(f"Best Month: {best_month} (Total Sales: {best_month_sales})")
print(f"Best Product: {best_product} (Total Annual Sales: {best_product_sales})")
print(f"Best Quarter: {best_quarter} (Total Sales: {best_quarter_sales})")
```

### 5. Visualizations

Visualizations help us understand trends and patterns more intuitively.

```python
# Cell 11: Line Chart for each product across months
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 6))

df[product_cols].plot(kind='line', ax=ax, marker='o')

ax.set_title('Monthly Sales per Product', fontsize=16)
ax.set_ylabel('Units Sold')
ax.set_xlabel('Month')
ax.legend(title='Products')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

**How it works:** A line chart is ideal for showing trends over time. Plotting all products on the same axes allows for easy comparison.

```python
# Cell 12: Stacked Bar Chart of total monthly sales by product
fig, ax = plt.subplots(figsize=(12, 7))
df[product_cols].plot(kind='bar', stacked=True, ax=ax, colormap='viridis')

ax.set_title('Total Monthly Sales by Product', fontsize=16)
ax.set_ylabel('Total Units Sold')
ax.set_xlabel('Month')
ax.legend(title='Products')
plt.xticks(rotation=45)

# Annotate the best month
ax.annotate(f'Best Month\n({best_month_sales} units)',
            xy=(df.index.get_loc(best_month), best_month_sales),
            xytext=(df.index.get_loc(best_month), best_month_sales + 10),
            ha='center',
            arrowprops=dict(facecolor='black', shrink=0.05))

plt.tight_layout()
plt.show()
```

**How it works:** A stacked bar chart shows both the total sales per month and the contribution of each product to that total. Annotation helps highlight key findings directly on the chart.

```python
# Cell 13: Seaborn Heatmap of monthly sales
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(df[product_cols].T, annot=True, fmt='d', cmap='YlGnBu', linewidths=.5, ax=ax)
# .T transposes the DataFrame to have products on the y-axis and months on the x-axis

ax.set_title('Heatmap of Monthly Sales per Product', fontsize=16)
ax.set_ylabel('Product')
ax.set_xlabel('Month')
plt.show()
```

**How it works:** A heatmap uses color intensity to represent values. It's excellent for quickly identifying high-performing (darker color) and low-performing (lighter color) periods for each product. `annot=True` displays the actual sales numbers on the cells.

```python
# Cell 14: Seaborn Boxplot for distribution of sales
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df[product_cols], ax=ax)

ax.set_title('Distribution of Sales per Product', fontsize=16)
ax.set_ylabel('Units Sold')
ax.set_xlabel('Product')
plt.show()
```

**How it works:** A boxplot provides a summary of the distribution of sales for each product over the year. It shows the median (the line in the box), the interquartile range (the box), and potential outliers (dots). This helps compare not just the average sales, but also the consistency and range of sales for each product.

### 6. Conclusion Questions

Based on the analysis and visualizations from the data generated with `seed=42`.

```python
# Cell 15: Answering Conclusion Questions

print("--- Conclusion Questions & Answers ---")
print(f"\n1. Which product contributes the most to overall sales throughout the year?")
print(f"-> {best_product} is the best-performing product with a total of {best_product_sales} units sold over the year. This is determined by summing the sales for each product across all months.")

print(f"\n2. Which quarter performs best and why might that be?")
print(f"-> {best_quarter} was the best-performing quarter with {best_quarter_sales} total units sold. Based on the line chart and heatmap, sales for most products, especially the top-seller {best_product}, tend to peak during the months within this quarter. This could be due to seasonal demand, successful marketing campaigns, or other external factors.")

print(f"\n3. How could this information be used to improve sales strategy for the next year?")
print("-> This information provides several actionable insights for the next year's strategy:")
print("   - Focus on the Best Product: Since " + best_product + " is the top contributor, marketing efforts and inventory management should prioritize it, especially during its peak season in " + best_quarter + ".")
print("   - Learn from Success: Analyze what caused the sales spike in the best month (" + best_month + "). Was it a promotion, a holiday, or a specific event? Replicate successful strategies in other months or for other products.")
print("   - Address Underperformance: Investigate why sales for the lowest-selling products are lagging. Strategies could include targeted promotions, product bundling with " + best_product + ", or market research to understand customer needs better.")
print("   - Seasonal Planning: Plan inventory and marketing campaigns around the identified quarterly trends. For instance, ramp up stock and advertising for all products leading into the best-performing quarter.")

```