

## Exercise 1: Clean Lines Function
File to create: utils/helpers.py

**Task:**

Write a function called clean_lines() that:
*   Takes a list of strings
*   Removes empty lines and trims extra spaces
*   Returns the cleaned list

**Example Input:**
```
lines = ["Laptop,1000,3", " ", "Phone,500,5", "\n", "Tablet,700,2"]
```
**Expected Output:**
```
["Laptop,1000,3", "Phone,500,5", "Tablet,700,2"]
```

---

## Exercise 2: Parse Products Function
File: utils/helpers.py (add below previous function)

**Task:**

Write a function parse_products(lines) that:
*   Converts each line into a tuple (name, price, quantity)
*   Converts price to float and quantity to int
*   Ignores malformed lines

**Example Input:**
```
lines = ["Laptop,1000,3", "Phone,500,5", "Tablet,700,2"]
```
**Expected Output:**
```
[("Laptop", 1000.0, 3), ("Phone", 500.0, 5), ("Tablet", 700.0, 2)]
```

---

## Exercise 3: Product Class
File to create: utils/product.py

**Task:**

Create a class Product with:
*   Attributes: name, price, quantity
*   Method: total_value() that returns price * quantity

**Example Usage:**
```
p = Product("Laptop", 1000, 3) 
print(p.total_value()) # Output: 3000
```

---

## Exercise 4: Create Products from File
File: scripts/create_products.py

**Task:**

Read a text file data/raw/data.txt containing product info (name,price,quantity)
*   Clean the lines using clean_lines()
*   Parse the products using parse_products()
*   Create Product objects
*   Print each product's total value and overall total sales

**Example Input File (data/raw/data.txt):**
```
Laptop,1000,3
Phone,500,5
Tablet,700,2
Monitor,300,4
Camera,400,1
```

*   **Expected Output:**
```
Laptop: 3000.0
Phone: 2500.0
Tablet: 1400.0
Monitor: 1200.0
Camera: 400.0

Total Sales: 8500.0
```

---

## Exercise 5: Notebook for Visualization
File: notebooks/analysis.ipynb

**Task:**
*   Read data/raw/data.txt
*   Create Product objects
*   Plot a bar chart of total sales per product

**Plot:** X-axis: product names Y-axis: total sales

---

✅ **Folder Structure for Exercises**
```
Sales_project/
|
├── data/
│   ├── raw/
│   │   └── data.txt
│   └── processed/          # optional for cleaned files
│
├── scripts/
│   └── create_products.py
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   ├── product.py
│
└── notebooks/
    └── analysis.ipynb
```

---

## Exercise 6:
Give solution for one millon products.

***

### **Part 2: Lab Solutions with Code and Explanations**

Here are the complete solutions for each exercise, including code and explanations.

### **Project Setup**

First, create the folder structure as specified. Create empty files for `__init__.py`, `helpers.py`, `product.py`, `create_products.py`, and `analysis.ipynb`.

Create the input data file:

**File: `data/raw/data.txt`**
```
Laptop,1000,3
Phone,500,5
Tablet,700,2
Monitor,300,4
Camera,400,1
 
malformed_line
Another,bad,line,extra
 
value_error,abc,3
```
*I've added some malformed lines to test the robustness of our parsing function.*

---

### **Exercise 1 & 2: Helper Functions**

These two functions belong in the same file.

**File: `utils/helpers.py`**
```python
def clean_lines(lines):
    """
    Removes empty lines and trims leading/trailing whitespace from a list of strings.

    Args:
        lines (list): A list of strings.

    Returns:
        list: A new list with cleaned strings.
    """
    cleaned_list = []
    for line in lines:
        stripped_line = line.strip()  # Remove whitespace from both ends
        if stripped_line:  # Check if the line is not empty after stripping
            cleaned_list.append(stripped_line)
    return cleaned_list

def parse_products(lines):
    """
    Parses a list of product strings into a list of tuples.

    Args:
        lines (list): A list of cleaned strings, each in "name,price,quantity" format.

    Returns:
        list: A list of tuples, where each tuple is (name, price, quantity).
              Malformed lines are ignored.
    """
    products_list = []
    for line in lines:
        try:
            parts = line.split(',')
            # Ensure the line has exactly 3 parts
            if len(parts) != 3:
                continue  # Ignore malformed lines

            name = parts[0]
            price = float(parts[1])
            quantity = int(parts[2])

            products_list.append((name, price, quantity))
        except (ValueError, IndexError):
            # ValueError occurs if price/quantity can't be converted.
            # IndexError occurs if split doesn't produce enough parts.
            # We simply ignore these lines by continuing to the next iteration.
            continue
    return products_list
```

**How It Works:**
*   **`clean_lines(lines)`**:
    *   It iterates through the input `lines`.
    *   `line.strip()` removes all leading and trailing whitespace, including spaces, tabs, and newline characters (`\n`).
    *   The `if stripped_line:` check is a concise way to see if the string is not empty. An empty string (`""`) evaluates to `False` in a boolean context.
    *   Only non-empty lines are added to the `cleaned_list`.

*   **`parse_products(lines)`**:
    *   It iterates through the cleaned lines.
    *   A `try...except` block is used to gracefully handle errors. If any code inside the `try` block fails, the program jumps to the `except` block instead of crashing.
    *   `line.split(',')` breaks the string into a list of parts using the comma as a delimiter.
    *   We explicitly check `if len(parts) != 3` to ensure the data has the correct structure.
    *   `float()` and `int()` are used to convert the string representations of price and quantity into their correct numerical types. If this conversion fails (e.g., trying to convert `"abc"` to a float), a `ValueError` is raised.
    *   The `continue` statement skips the rest of the current loop iteration and moves to the next line, effectively ignoring any malformed lines.

---

### **Exercise 3: Product Class**

This class will represent a single product.

**File: `utils/product.py`**
```python
class Product:
    """
    Represents a product with a name, price, and quantity.
    """
    def __init__(self, name, price, quantity):
        """
        Initializes a Product object.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            quantity (int): The available quantity of the product.
        """
        self.name = name
        self.price = price
        self.quantity = quantity

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
**How It Works:**
*   **`class Product:`**: Defines a new class blueprint for creating product objects.
*   **`__init__(self, ...)`**: This is the constructor method. It runs automatically when you create a new `Product` object (e.g., `p = Product(...)`). It takes the provided arguments and assigns them to instance attributes (`self.name`, `self.price`, etc.). `self` refers to the instance of the object being created.
*   **`total_value(self)`**: This is an instance method. It can access the object's own data (like `self.price` and `self.quantity`) to perform calculations.
*   **`__repr__(self)`**: (Optional but good practice) This "representation" method provides a clear string output when you print an object, which is useful for debugging.

---

### **Exercise 4: Script to Create Products**

This script ties everything together to read the file and produce the final report.

**File: `scripts/create_products.py`**
```python
# Import the functions and class from our utils modules
from utils.helpers import clean_lines, parse_products
from utils.product import Product
import os

def main():
    """
    Main function to read, process, and display product data.
    """
    # Construct the path to the data file relative to this script's location
    # This makes the script runnable from any directory
    script_dir = os.path.dirname(__file__)  # Gets the directory where the script is
    file_path = os.path.join(script_dir, '../data/raw/data.txt')

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return

    # 1. Clean the lines from the file
    cleaned = clean_lines(lines)

    # 2. Parse the cleaned lines into structured data
    parsed_data = parse_products(cleaned)

    # 3. Create Product objects from the parsed data
    # We use a list comprehension for a concise way to build the list
    products = [Product(name, price, qty) for name, price, qty in parsed_data]
    # The line above is equivalent to:
    # products = []
    # for name, price, qty in parsed_data:
    #     products.append(Product(name, price, qty))

    # 4. Print each product's total value and calculate overall total sales
    total_sales = 0.0
    for p in products:
        value = p.total_value()
        print(f"{p.name}: {value}")
        total_sales += value

    print("\n" + "="*20)
    print(f"Total Sales: {total_sales}")
    print("="*20)


if __name__ == "__main__":
    main()

```
**How It Works:**
1.  **Imports**: We import our custom-built `clean_lines`, `parse_products`, and `Product` modules. `os` is used to build a reliable file path.
2.  **File Path**: `os.path.dirname(__file__)` gets the directory of the current script (`scripts/`). `os.path.join` then correctly combines it with `'../data/raw/data.txt'` to find the data file. This prevents "file not found" errors when you run the script from different locations in your terminal.
3.  **Reading File**: `with open(...) as f:` is the standard, safe way to handle files. It automatically closes the file even if errors occur. `f.readlines()` reads the entire file into a list of strings.
4.  **Processing Pipeline**: The script follows the exact steps outlined in the task: call `clean_lines`, then `parse_products`.
5.  **Object Creation**: A list comprehension `[Product(...) for ...]` is a Pythonic and efficient way to create the list of `Product` objects from the parsed data.
6.  **Calculation and Output**: The script iterates through the list of `Product` objects, calls the `.total_value()` method for each, prints the result, and accumulates the sum in `total_sales`.
7.  **`if __name__ == "__main__":`**: This is a standard Python construct. The code inside this block only runs when the script is executed directly (not when it's imported as a module by another script).

---

### **Exercise 5: Jupyter Notebook for Visualization**

This code would go into the cells of `notebooks/analysis.ipynb`.

**Prerequisites**: You need to install `matplotlib` and `pandas`.
```bash
pip install matplotlib pandas
```

**File: `notebooks/analysis.ipynb`**

**Cell 1: Imports and Data Loading**
```python
# Import necessary libraries
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

# Add the project's root directory to the Python path
# This allows us to import our 'utils' modules
# Assumes the notebook is in 'Sales_project/notebooks/'
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.helpers import clean_lines, parse_products
from utils.product import Product

# --- Data Loading and Processing ---
# This part is similar to the script in Exercise 4
file_path = '../data/raw/data.txt'

with open(file_path, 'r') as f:
    lines = f.readlines()

cleaned = clean_lines(lines)
parsed_data = parse_products(cleaned)
products = [Product(p[0], p[1], p[2]) for p in parsed_data]

print("Products loaded successfully:")
for p in products:
    print(p)
```

**Cell 2: Prepare Data for Plotting**
```python
# Extract the data needed for the plot
product_names = [p.name for p in products]
total_values = [p.total_value() for p in products]

# It's also common to put this data into a Pandas DataFrame for easier manipulation
df = pd.DataFrame({
    'Product': product_names,
    'TotalSales': total_values
})

print("\nData prepared for plotting:")
print(df)
```

**Cell 3: Generate the Bar Chart**
```python
# Create the plot
plt.figure(figsize=(10, 6)) # Set the figure size for better readability

plt.bar(df['Product'], df['TotalSales'], color='skyblue')

# Add labels and title
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.title("Total Sales per Product")
plt.xticks(rotation=45) # Rotate product names if they overlap
plt.tight_layout() # Adjust layout to make room for labels

# Display the plot
plt.show()
```

**How It Works:**
*   **Cell 1**: We first adjust the system path to ensure our `utils` module can be imported from the notebook. The rest of the cell reuses the logic from Exercise 4 to load and process the data into `Product` objects.
*   **Cell 2**: We prepare the data specifically for plotting. Two lists, `product_names` and `total_values`, are created. Using a Pandas DataFrame is a best practice as it organizes the data neatly and integrates well with many plotting libraries.
*   **Cell 3**:
    *   `plt.figure(figsize=(10, 6))` creates a canvas for our plot, making it a good size.
    *   `plt.bar(x, y)` is the core function from Matplotlib to create a bar chart. We pass the product names for the x-axis and their total sales for the y-axis.
    *   The `xlabel`, `ylabel`, and `title` functions add descriptive labels.
    *   `plt.show()` renders and displays the final chart.

---

### **Exercise 6: Solution for One Million Products**

Reading a file with one million lines into memory with `readlines()` is highly inefficient and may cause a crash due to high memory consumption. The solution is to **process the file as a stream**, reading and handling it line-by-line.

We can achieve this by creating **generator functions**. A generator yields one item at a time, using very little memory.

**1. Refactor `utils/helpers.py` to use generators:**

```python
# utils/helpers.py (Generator Version)

def clean_lines_generator(file_stream):
    """
    A generator that yields cleaned lines from a file stream one by one.
    """
    for line in file_stream:
        stripped_line = line.strip()
        if stripped_line:
            yield stripped_line

def parse_products_generator(cleaned_lines_stream):
    """
    A generator that yields parsed product tuples from a stream of cleaned lines.
    """
    for line in cleaned_lines_stream:
        try:
            parts = line.split(',')
            if len(parts) == 3:
                name = parts[0]
                price = float(parts[1])
                quantity = int(parts[2])
                yield (name, price, quantity)
        except (ValueError, IndexError):
            continue
```

**2. Refactor `scripts/create_products.py` to use the generators:**

```python
# scripts/create_products_large_scale.py

from utils.helpers_generators import clean_lines_generator, parse_products_generator # Assume new file
from utils.product import Product
import os

def main_large_scale():
    """
    Processes a large product file efficiently using generators.
    """
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../data/raw/large_data.txt') # Assumes a large file
    
    total_sales = 0.0
    product_count = 0

    try:
        with open(file_path, 'r') as f:
            # Create a processing pipeline of generators
            cleaned_lines = clean_lines_generator(f)
            parsed_products_data = parse_products_generator(cleaned_lines)
            
            # Pull data through the pipeline one item at a time
            for name, price, qty in parsed_products_data:
                product = Product(name, price, qty)
                total_sales += product.total_value()
                product_count += 1
                
                # Optional: Print progress for very large files
                if product_count % 100000 == 0:
                    print(f"Processed {product_count} products...")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return

    print("\n" + "="*20)
    print(f"Processed a total of {product_count} products.")
    print(f"Total Sales: {total_sales}")
    print("="*20)

if __name__ == "__main__":
    main_large_scale()
```

**How the Large-Scale Solution Works:**
1.  **No `readlines()`**: The core change is that we never call `f.readlines()`. Instead, we pass the file object `f` directly to our first generator. Iterating over a file object (`for line in f`) naturally reads it line-by-line.
2.  **Generator Chaining**: We create a "pipeline". `clean_lines_generator` takes the file stream and `yield`s one clean line. `parse_products_generator` takes that stream of clean lines and `yield`s one parsed tuple.
3.  **Lazy Evaluation**: No work is actually done when we define `cleaned_lines` or `parsed_products_data`. The code only executes when the `for` loop at the end asks for the *next* item.
4.  **Minimal Memory**: At any given time, only **one line** of the file is being held in memory for processing. After its total value is added to `total_sales`, the line and the `Product` object are discarded, and the memory is freed. This approach can process files of virtually any size with constant, low memory usage.