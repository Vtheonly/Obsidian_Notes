Of course. Here is the complete Python code for each of the `.py` files in your project structures.

### Project 1: `Sales_project`

You should be in the `Sales_project` directory. Copy the code below into the corresponding empty files you created.

---

#### `utils/__init__.py`

This file can remain empty. Its presence tells Python that the `utils` directory is a package, allowing you to import from it.

```python
# This file is intentionally left empty.
# It marks the 'utils' directory as a Python package.
```

---

#### `utils/helpers.py`

This file contains the functions for cleaning and parsing data from Exercises 1 and 2.

```python
# utils/helpers.py

def clean_lines(lines):
    """
    Removes empty lines and trims extra whitespace from a list of strings.

    Args:
        lines (list): A list of strings, potentially with empty lines and spaces.

    Returns:
        list: A new list containing only the cleaned, non-empty strings.
    """
    cleaned_list = []
    for line in lines:
        # .strip() removes leading/trailing whitespace, including newline characters
        trimmed_line = line.strip()
        if trimmed_line:  # An empty string evaluates to False
            cleaned_list.append(trimmed_line)
    return cleaned_list


def parse_products(lines):
    """
    Converts a list of product strings into tuples of (name, price, quantity).
    It handles type conversion and ignores malformed lines.

    Args:
        lines (list): A list of cleaned strings, each in "name,price,quantity" format.

    Returns:
        list: A list of tuples, e.g., [("Laptop", 1000.0, 3), ...].
    """
    products_data = []
    for line in lines:
        parts = line.split(',')
        # A valid line must have exactly 3 parts
        if len(parts) == 3:
            name, price_str, quantity_str = parts
            try:
                # Attempt to convert price to float and quantity to int
                price = float(price_str)
                quantity = int(quantity_str)
                products_data.append((name, price, quantity))
            except ValueError:
                # If conversion fails, the line is malformed. We just skip it.
                print(f"Warning: Skipping malformed line -> {line}")
                pass
    return products_data

```

---

#### `utils/product.py`

This file contains the `Product` class from Exercise 3.

```python
# utils/product.py

class Product:
    """
    A simple class to represent a product with its name, price, and quantity.
    """
    def __init__(self, name, price, quantity):
        """
        Initializes a Product instance.

        Args:
            name (str): The product's name.
            price (float): The price per unit of the product.
            quantity (int): The number of units.
        """
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def total_value(self):
        """
        Calculates the total value of the product stock (price * quantity).

        Returns:
            float: The total value.
        """
        return self.price * self.quantity

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the object.
        """
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

```

---

#### `scripts/create_products.py`

This is the main script from Exercise 4 that reads the file, processes the data, and prints the sales report to the console.

```python
# scripts/create_products.py

import os
# To run this script from the project root (Sales_project),
# Python can find the 'utils' package.
from utils.helpers import clean_lines, parse_products
from utils.product import Product

DATA_FILE_PATH = "data/raw/data.txt"

def main():
    """
    Main function to execute the data processing workflow.
    """
    # 1. Read the text file
    if not os.path.exists(DATA_FILE_PATH):
        print(f"Error: The data file was not found at '{DATA_FILE_PATH}'")
        return

    with open(DATA_FILE_PATH, 'r') as file:
        raw_lines = file.readlines()

    # 2. Clean the lines using the helper function
    cleaned = clean_lines(raw_lines)

    # 3. Parse the products using the helper function
    parsed_data = parse_products(cleaned)

    # 4. Create Product objects and calculate total sales
    products = []
    total_sales = 0.0

    print("--- Product Sales Report ---")
    for name, price, quantity in parsed_data:
        product = Product(name, price, quantity)
        products.append(product)
        
        value = product.total_value()
        total_sales += value
        print(f"{product.name}: {value:.1f}")

    print("----------------------------")
    print(f"Total Sales: {total_sales:.1f}")


if __name__ == "__main__":
    main()

```

**To run this script:**
Navigate to your `Sales_project` root directory in the terminal and run:
`python scripts/create_products.py`

---

#### `notebooks/analysis.py`

This is the Python script version of Exercise 5. It will generate and display a bar chart.

```python
# notebooks/analysis.py

import os
import matplotlib.pyplot as plt
from utils.helpers import clean_lines, parse_products
from utils.product import Product

DATA_FILE_PATH = "data/raw/data.txt"

def main():
    """
    Reads product data, creates Product objects, and plots a bar chart of total sales.
    """
    # Read, clean, and parse data (same as the other script)
    if not os.path.exists(DATA_FILE_PATH):
        print(f"Error: The data file was not found at '{DATA_FILE_PATH}'")
        return
        
    with open(DATA_FILE_PATH, 'r') as file:
        raw_lines = file.readlines()
    
    cleaned = clean_lines(raw_lines)
    parsed_data = parse_products(cleaned)
    products = [Product(name, price, quantity) for name, price, quantity in parsed_data]

    if not products:
        print("No product data found to visualize.")
        return

    # Prepare data for plotting
    product_names = [p.name for p in products]
    total_values = [p.total_value() for p in products]

    # Create the bar chart
    plt.figure(figsize=(10, 6))  # Set the figure size for better readability
    plt.bar(product_names, total_values, color='teal')

    plt.title('Total Sales per Product')
    plt.xlabel('Product')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45, ha='right')  # Rotate labels for long names
    plt.tight_layout()  # Adjust plot to ensure everything fits without overlapping

    # Display the plot
    print("Generating plot... Close the plot window to exit the script.")
    plt.show()


if __name__ == "__main__":
    main()

```

**To run this script:**
Navigate to your `Sales_project` root directory and run:
`python notebooks/analysis.py`

---

### Project 2: `HospitalDataAnalysis`

Navigate to your `HospitalDataAnalysis` directory. Here is the code for the main analysis script.

---

#### `notebooks/patients_analysis.py`

This script loads the patient data with pandas, prints summary statistics, and displays a scatter plot.

```python
# notebooks/patients_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE_PATH = "data/patients.csv"

def main():
    """
    Loads, analyzes, and visualizes the hospital patient data.
    """
    # Step 1: Load and explore the data
    try:
        df = pd.read_csv(DATA_FILE_PATH)
    except FileNotFoundError:
        print(f"Error: Data file not found at '{DATA_FILE_PATH}'.")
        return

    print("--- First 5 Rows of Patient Data ---")
    print(df.head())
    print("\n" + "="*40 + "\n")

    # Step 2: Run basic descriptive statistics
    print("--- Descriptive Statistics ---")
    print(df.describe())
    print("\n" + "="*40 + "\n")

    print("--- Counts by Sex ---")
    print(df['Sex'].value_counts())
    print("\n" + "="*40 + "\n")

    print("--- Counts by Diagnosis ---")
    print(df['Diagnosis'].value_counts())
    print("\n" + "="*40 + "\n")
    
    # Step 3: Visualize the data with a simple plot
    print("Generating plot of Cholesterol vs. Age...")
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Age"], df["Cholesterol"], marker="o", color="blue", alpha=0.7)
    
    plt.title("Cholesterol vs Age")
    plt.xlabel("Age (Years)")
    plt.ylabel("Cholesterol Level")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Show the plot. The script will pause here until you close the plot window.
    plt.show()

if __name__ == "__main__":
    main()

```

**To run this script:**
Navigate to your `HospitalDataAnalysis` root directory and run:
`python notebooks/patients_analysis.py`