# Chapter 04: Essential Python Libraries for Data Science: Part 01

The power of Python in Data Science lies in:
* its rich ecosystem of specialized libraries.
* These libraries reduce the time and effort required for tasks such as data cleaning, numerical computation, visualization, and machine learning.

The goal of this chapter is to introduce and explore the fundamental Python libraries that every data scientist should master to work efficiently and effectively.

## 1. NumPy — *Numerical Python*

### 1.1. Definition
NumPy (short for Numerical Python) is the foundation of scientific computing in Python. It provides high-performance N-dimensional array objects, efficient vectorized operations, and broadcasting capabilities for fast mathematical and statistical computations.

### 1.2. Why NumPy?
* Fast numerical computations
* Handling multidimensional arrays (ndarray)
* Performing vectorized operations without loops
* foundation of scientific libraries like Pandas, Scikit-learn, and Matplotlib.

```
In [1]: import numpy as np

# Create an array and perform vectorized computation
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])
result1 = a + b
print(F"result1={result1}")
result2=a*b
print(F"result2={result2}")

result1=[ 6 8 10 12]
result2=[ 5 12 21 32]
```

### 1.3. Installation and Import
```
pip install numpy
```
```
import numpy as np
```

### 1.4. NumPy — Array Creation

---
*Essential Python Libraries for Data Science – Amel Boustil*
---

| Function | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `np.array()` | Create an array from a Python list or tuple | `np.array([1, 2, 3])` | `[1 2 3]` |
| `np.zeros(shape)` | Create an array filled with **zeros** | `np.zeros((2, 3))` | `[[0. 0. 0.] [0. 0. 0.]]` |
| `np.ones(shape)` | Create an array filled with **ones** | `np.ones((3, 2))` | `[[1. 1.] [1. 1.] [1. 1.]]` |
| `np.full(shape, value)` | Create an array filled with a **specific value** | `np.full((2, 2), 7)` | `[[7 7] [7 7]]` |
| `np.eye(n)` | Create an **identity matrix** | `np.eye(3)` | `[[1. 0. 0.] [0. 1. 0.] [0. 0. 1.]]` |
| `np.arange(start, stop, step)` | Create a range of evenly spaced **integers** | `np.arange(0, 10, 2)` | `[0 2 4 6 8]` |
| `np.linspace(start, stop, num)` | Create evenly spaced **floats** between two values | `np.linspace(0, 1, 5)` | `[0. 0.25 0.5 0.75 1.]` |
| `np.random.rand(d0, d1, ...)` | Random floats from **uniform [0, 1)** distribution | `np.random.rand(2, 2)` | e.g. `[[0.42 0.93] [0.18 0.61]]` |
| `np.random.randn(d0, d1, ...)` | Random floats from **normal (Gaussian)** distribution | `np.random.randn(2, 2)` | e.g. `[[-0.54 1.02] [0.33 -1.27]]` |
| `np.random.randint(low, high, size)` | Random **integers** within a range | `np.random.randint(0, 10, (2, 3))` | e.g. `[[2 9 5] [1 7 0]]` |
| `np.empty(shape)` | Create an **uninitialized array** (random memory values) | `np.empty((2, 3))` | e.g. `[[1.3e-312 2.5e-312 0.0e+000] [0.0e+000 0.0e+000 0.0e+000]]` |
| `np.identity(n)` | Create an **n x n identity matrix** | `np.identity(4)` | `[[1. 0. 0. 0.] [0. 1. 0. 0.] [0. 0. 1. 0.] [0. 0. 0. 1.]]` |
| `np.fromfunction(func, shape)` | Build array from a **function of indices** | `np.fromfunction(lambda i, j: i + j, (3, 3))` | `[[0. 1. 2.] [1. 2. 3.] [2. 3. 4.]]` |
| `np.fromiter(iterable, dtype)` | Create array from an **iterable object** | `np.fromiter(range(5), dtype=int)` | `[0 1 2 3 4]` |

```
In [2]: import numpy as np
a = np.empty((2,3))
print(a)

[[6.23042070e-307 4.67296746e-307 1.69121096e-306]
 [6.23054293e-307 2.22526399e-307 2.05837348e-312]]
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---

```
In [3]: import numpy as np
a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])
```
```
In [4]: np.eye(2,4)
Out[4]: array([[1., 0., 0., 0.],
             [0., 1., 0., 0.]])
```
```
In [5]: np.identity(2,dtype=int)
Out[5]: array([[1, 0],
             [0, 1]])
```
```
In [6]: np.fromfunction(lambda i, j: i * j, (3, 3))
Out[6]: array([[0., 0., 0.],
             [0., 1., 2.],
             [0., 2., 4.]])
```

### 1.5. Array Attributes & Inspection
Functions to understand array structure.

| Function / Property | Description | Example | Result |
|---|---|---|---|
| `ndim` | Number of dimensions | `a.ndim` | 2 |
| `shape` | Shape (rows, columns) | `a.shape` | `(3, 4)` |
| `size` | Total number of elements | `a.size` | 12 |
| `dtype` | Data type of elements | `a.dtype` | `int64` |
| `itemsize` | Bytes per element | `a.itemsize` | 8 |
| `nbytes` | Total bytes of array | `a.nbytes` | 96 |

```
In [7]: a = np.array([[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 11, 12]])
print(a.ndim, a.shape, a.size, a.dtype, a.itemsize, a.nbytes)

2 (3, 4) 12 int64 8 96
```

### 1.6. Indexing and Slicing

| Operation | Description | Example | Result |
|---|---|---|---|
| `a[i]` | Select row `i` | `a[1]` | `[5 6 7 8]` |
| `a[i, j]` | Select element at row `i`, column `j` | `a[1, 2]` | `7` |
| `a[i:j]` | Slice rows | `a[1:3]` | `[[5 6 7 8] [9 10 11 12]]` |
| `a[:, i]` | Select column `i` | `a[:, 0]` | `[1 5 9]` |
| `a[::2]` | Step slicing (every 2nd row) | `a[::2]` | `[[1 2 3 4] [9 10 11 12]]` |

---
*Essential Python Libraries for Data Science – Amel Boustil*
---

| Operation | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `a[a > 6]` | Boolean indexing (filter values) | `a[a > 6]` | `[7 8 9 10 11 12]` |
| `np.where(a > 6)` | Indices where condition is True | `np.where(a > 6)` | `(array([1, 1, 2, 2, 2, 2]), array([2, 3, 0, 1, 2, 3]))` |
| `a[np.where(a > 6)]` | Elements satisfying condition | `a[np.where(a > 6)]` | `[7 8 9 10 11 12]` |
| `np.argmax(a)` | Index (flattened) of max element | `np.argmax(a)` | `11` |
| `np.argmax(a, axis=0)` | Index of max in each column | `np.argmax(a, axis=0)` | `[2 2 2 2]` |
| `np.argmax(a, axis=1)` | Index of max in each row | `np.argmax(a, axis=1)` | `[3 3 3]` |
| `np.argmin(a)` | Index (flattened) of min element | `np.argmin(a)` | `0` |
| `np.argmin(a, axis=0)` | Index of min in each column | `np.argmin(a, axis=0)` | `[0 0 0 0]` |
| `np.argmin(a, axis=1)` | Index of min in each row | `np.argmin(a, axis=1)` | `[0 0 0]` |
| `np.where(a == np.min(a))` | Coordinates of minimum element | `np.where(a == np.min(a))` | `(array([0]), array([0]))` |

```
In [8]: (a>6) # creation of is a mask
Out[8]: array([[False, False, False, False],
               [False, False,  True,  True],
               [ True,  True,  True,  True]])
```
```
In [9]: a[a > 6]
Out[9]: array([ 7, 8, 9, 10, 11, 12])
```
```
In [10]: a[np.where(a > 6)]
Out[10]: array([ 7, 8, 9, 10, 11, 12])
```
```
In [11]: np.where(a > 6)
Out[11]: (array([1, 1, 2, 2, 2, 2]), array([2, 3, 0, 1, 2, 3]))
```
### 1.7. Array Operations (Vectorization)
Functions to perform arithmetic efficiently

| Operation | Description | Example | Result |
|---|---|---|---|
| `a + b` | Element-wise addition | `[1,2,3] + [4,5,6]` | `[5,7,9]` |
| `a * b` | Element-wise multiplication | `[1,2,3] * [4,5,6]` | `[4,10,18]` |
| `a * 2` | Element-wise scalar multiplication | `[1,2,3] * 2` | `[2,4,6]` |
| `a ** 2` | Power | `[2,3,4]**2` | `[4,9,16]` |

---
*Essential Python Libraries for Data Science – Amel Boustil*
---

| Operation | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `np.maximum(a, b)` | Element-wise maximum | `np.maximum([1,5,3], [4,2,6])` | `[4,5,6]` |
| Broadcasting | Auto expand shapes | `a + 10` | Adds 10 to all elements |

### 1.8. Universal Functions (ufuncs)
Functions to apply math operations element-wise.

| Function | Description | Example | Result |
|---|---|---|---|
| `np.sqrt(a)` | Square root | `np.sqrt([1,4,9])` | `[1.,2.,3.]` |
| `np.exp(a)` | Exponential | `np.exp([0,1])` | `[1.,2.718]` |
| `np.log(a)` | Logarithm | `np.log([1, np.e])` | `[0.,1.]` |
| `np.sin(a)` | Sine | `np.sin(np.pi/2)` | `1.0` |

### 1.9. Aggregate Functions
Functions to summarize data.

| Function | Description | Example | Result |
|---|---|---|---|
| `np.sum(a)` | Sum | `np.sum([1,2,3])` | 6 |
| `np.mean(a)` | Average | `np.mean([1,2,3])` | 2.0 |
| `np.min(a)` | Minimum | `np.min([4,2,8])` | 2 |
| `np.max(a)` | Maximum | `np.max([4,2,8])` | 8 |
| `np.std(a)` | Standard deviation | `np.std([1,2,3])` | 0.816 |

```
In [12]: a = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]
         ])
         b = np.array([
            [13, 14, 15, 16],
            [17, 18, 19, 20],
            [21, 22, 23, 24]
         ])
```

### 1.10. Reshaping & Stacking
Functions to change array shapes and combine arrays.

| Function | Description | Example | Result |
|---|---|---|---|
| `reshape` | Change shape | `a.reshape(4,3)` | `[[1 2 3] [4 5 6] [7 8 9] [10 11 12]]` |
| `ravel` | Flatten array | `a.ravel()` | `[1 2 3 4 5 6 7 8 9 10 11 12]` |

---
*Essential Python Libraries for Data Science – Amel Boustil*
---

| Function | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `hstack` | Horizontal stack (same rows) | `np.hstack((a,b))` | `[[1 2 3 4 13 14 15 16] [5 6 7 8 17 18 19 20] [9 10 11 12 21 22 23 24]]` |
| `vstack` | Vertical stack (same columns) | `np.vstack((a,b))` | `[[1 2 3 4] [5 6 7 8] [9 10 11 12] [13 14 15 16] [17 18 19 20] [21 22 23 24]]` |
| `concatenate` | Stack arrays along axis | `np.concatenate((a,b), axis=0)` | Same as vstack |
| `np.unravel_index` | Convert flat index to coordinates | `np.unravel_index(np.argmax(a), a.shape)` | `(2, 3)` (position of 12 in a) |

```
In [13]: a = np.linspace(0, 1, 6).reshape(3,2)
         print(a)
[[0. 0.2]
 [0.4 0.6]
 [0.8 1. ]]
```
```
In [14]: a.ravel()
Out[14]: array([0. , 0.2, 0.4, 0.6, 0.8, 1. ])
```
```
In [15]: b=np.array([1,2])
         np.vstack((a,b))
Out[15]: array([[0., 0.2],
               [0.4, 0.6],
               [0.8, 1. ],
               [1., 2. ]])
```
```
In [16]: np.hstack((b,a.ravel()))
Out[16]: array([1. , 2. , 0. , 0.2, 0.4, 0.6, 0.8, 1. ])
```
```
In [17]: np.unravel_index(np.argmax(a), a.shape)
Out[17]: (np.int64(2), np.int64(1))
```
```
In [18]: np.unravel_index(4, a.shape)
Out[18]: (np.int64(2), np.int64(0))
```

### 1.11. Random Module
Functions to generate random data.

| Function | Description | Example | Result |
|---|---|---|---|
| `np.random.rand(n)` | Uniform [0,1) | `np.random.rand(3)` | `[0.45, 0.12, 0.88]` |
| `np.random.randint(a,b)` | Random integers | `np.random.randint(1,10,3)` | `[3,8,1]` |
| `np.random.randn(n)` | Normal distribution | `np.random.randn(3)` | `[0.3, -0.1, 1.2]` |

---
*Essential Python Libraries for Data Science – Amel Boustil*
---

| Function | Description | Example | Result |
| :--- | :--- | :--- | :--- |
| `np.random.choice(list)` | Random sample | `np.random.choice([1,2,3])` | `2` |

### 1.12. NumPy Linear Algebra
NumPy provides a powerful set of functions for performing linear algebra operations such as matrix multiplication, solving equations, computing determinants, and eigenvalues.
These tools are essential for numerical analysis, machine learning, and scientific computing.

**Function of Linear Algebra**

| Function | Description | Example |
| :--- | :--- | :--- |
| `np.dot(A, B)` or `A @ B` | Matrix or vector multiplication | `np.dot(A, B)` |
| `A.T` | Transpose of a matrix | `A.T` |
| `np.linalg.det(A)` | Determinant of matrix A | `np.linalg.det(A)` |
| `np.linalg.inv(A)` | Inverse of matrix A | `np.linalg.inv(A)` |
| `np.linalg.solve(A, b)` | Solves linear system Ax = b | `np.linalg.solve(A, b)` |
| `np.linalg.eig(A)` | Returns eigenvalues and eigenvectors | `np.linalg.eig(A)` |
| `np.linalg.norm(x)` | Computes vector or matrix norm (magnitude) | `np.linalg.norm(x)` |
| `np.trace(A)` | Sum of diagonal elements | `np.trace(A)` |
| `np.linalg.matrix_rank(A)` | Rank of a matrix | `np.linalg.matrix_rank(A)` |

**Tip:**
All advanced linear algebra operations are available in the `np.linalg` module, which stands for *NumPy Linear Algebra*.

## 2. Pandas — *Python Data Analysis Library*
### 2.1. Definition
Pandas is a high-level library built on top of NumPy designed for data manipulation and analysis.
It introduces two powerful data structures
* **Series** (1D) and
* **DataFrame** (2D)
which make working with structured and tabular data intuitive, fast, and flexible.

### 2.2. Why Pandas?
* **Easy Data Handling:** Load, clean, transform, and analyze data efficiently
* **Rich I/O Tools:** Import and export data from CSV, Excel, SQL, and JSON formats
* **Powerful Indexing:** Label-based selection and alignment
* **Integrated with NumPy:** Enables seamless numerical computation
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
* **Ideal for DataFrames:** Makes statistical analysis, grouping, and pivoting effortless

### 2.3. Core Data Structures
| Structure | Description | Example |
| :--- | :--- | :--- |
| `Series` | 1D labeled array | `pd.Series([10, 20, 30], index=['A','B','C'])` |
| `DataFrame` | 2D labeled data table | `pd.DataFrame({'Name':['Amel', 'Sami'], 'Age':[25,28]})` |

### 2.4. Common Pandas Functions

| Category | Key Functions | Description |
| :--- | :--- | :--- |
| **Data Import/Export** | `read_csv()`, `read_excel()`, `read_json()`, `to_csv()`, `to_excel()` | Load and save datasets from/to various formats |
| **Exploration** | `head()`, `tail()`, `info()`, `describe()`, `shape`, `dtypes`, `value_counts()`, `unique()`, `nunique()` | View summary, structure, and quick statistics of data |
| **Selection** | `loc[]`, `iloc[]`, `at[]`, `iat[]`, `query()` | Access rows and columns by labels, indices, or conditions |
| **Copy & Views** | `copy(deep=True)` | Create a deep copy of a DataFrame or Series to avoid modifying the original |
| **Cleaning** | `dropna()`, `fillna()`, `replace()`, `duplicated()`, `drop_duplicates()`, `isna()`, `notna()` | Handle missing and duplicate values |
| **Transformation**| `apply()`, `map()`, `applymap()`, `astype()`, `rename()`, `replace()` | Transform or convert columns and elements |
| **Computation** | `sum()`, `mean()`, `median()`, `min()`, `max()`, `rank()`, `std()` | Perform mathematical and statistical calculations |
| **Aggregation** | `groupby()`, `count()`, `agg()`, `transform()` | Aggregate or summarize data by groups |
| **Merging & Joining** | `merge()`, `concat()`, `join()`, `combine_first()` | Combine multiple DataFrames |
| **Sorting** | `sort_values()`, `sort_index()` | Sort data by one or more columns or by index |
| **Pivot & Reshaping**| `pivot()`, `pivot_table()`, `melt()`, `stack()`, `unstack()` | Reshape or reorganize data for analysis |
| **Time Series** | `to_datetime()`, `resample()`, `shift()`, `rolling()`, `dt` accessor | Handle, convert, and analyze time-based data |

```
In [19]: ### Example 1
         import pandas as pd
         # Create a Series
         ages = pd.Series([25, 28, 22], name="Age")
         print(ages)
         print("----")
         print(type(ages))
```

---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
0    25
1    28
2    22
Name: Age, dtype: int64
----
<class 'pandas.core.series.Series'>
```
```
In [20]: ### Example 2
         import numpy as np
         age=np.array([25,28,22])
         print(age)
[25 28 22]
```
```
In [21]: import pandas as pd
         ages=pd.Series(age)
         print(ages)
0    25
1    28
2    22
dtype: int64
```
```
In [22]: # Create a DataFrame
         data = {'Name': ['Amel', 'Sami', 'Rania'], 'Age': [25, 28, 22]}
         df = pd.DataFrame(data, index=['A','B', 'C'])

         print(df)
         print("----")
         print(type(df))

           Name  Age
        A   Amel   25
        B   Sami   28
        C  Rania   22
        ----
        <class 'pandas.core.frame.DataFrame'>
```
```
In [23]: df.index.values
Out[23]: array(['A', 'B', 'C'], dtype=object)
```
```
In [24]: df=df.reset_index()
         df
Out[24]:
  index   Name  Age
0     A   Amel   25
1     B   Sami   28
2     C  Rania   22
```
```
In [25]: df=df.drop(columns="index")
         df
Out[25]:
    Name  Age
0   Amel   25
1   Sami   28
2  Rania   22
```
```
In [26]: df.columns
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
Out[26]: Index(['Name', 'Age'], dtype='object')
```
```
In [27]: df.index.values
Out[27]: array([0, 1, 2])
```

### 2.5. Inspecting Data
Inspecting data is the first step in data analysis. It helps to:
* Get a quick overview of the data (first/last rows, column names, types).
* Detect missing values, inconsistent types, or unexpected formats.
* Understand summary statistics (mean, median, count, etc.) for numerical columns.
* Verify data dimensions and ensure DataFrame matches expectations.

```
In [28]: import pandas as pd
         import numpy as np
         # Create a DataFrame from a dictionary
         data = {
             'Name': ['Amel', 'Sami', 'Rania', 'Yacine', 'Nour'],
             'Age': [25, 28, np.nan, 35, 22],
             'City': ['Algiers', 'Oran', 'Constantine', 'Algiers', 'Blida'],
             'Salary': [50000, 54000, 58000, 22450, 48000],
             'JoinDate': ['2020-05-10', '2019-03-15', '2021-07-22', None, '2022-01-11']
         }
         df = pd.DataFrame(data)
         df.describe()
Out[28]:
              Age        Salary
count    4.000000      5.000000
mean    27.500000  46490.000000
std      5.567764  13976.784323
min     22.000000  22450.000000
25%     24.250000  48000.000000
50%     26.500000  50000.000000
75%     29.750000  54000.000000
max     35.000000  58000.000000
```
```
In [29]: df.shape # (rows, columns)
Out[29]: (5, 5)
```
```
In [30]: df.info() # Overview of columns and data types
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 5 columns):
 #   Column    Non-Null Count  Dtype
---  ------    --------------  -----
 0   Name      5 non-null      object
 1   Age       4 non-null      float64
 2   City      5 non-null      object
 3   Salary    5 non-null      int64
 4   JoinDate  4 non-null      object
dtypes: float64(1), int64(1), object(3)
memory usage: 332.0+ bytes
```
```
In [31]: df.dtypes # Data types
Out[31]: Name         object
         Age         float64
         City         object
         Salary        int64
         JoinDate     object
         dtype: object
```
```
In [32]: df.head(3) # First 3 rows
Out[32]:
    Name   Age         City  Salary    JoinDate
0   Amel  25.0      Algiers   50000  2020-05-10
1   Sami  28.0         Oran   54000  2019-03-15
2  Rania   NaN  Constantine   58000  2021-07-22
```
```
In [33]: df.tail(2) # Last 2 rows
Out[33]:
      Name   Age     City  Salary    JoinDate
3   Yacine  35.0  Algiers   22450        None
4     Nour  22.0    Blida   48000  2022-01-11
```
```
In [34]: df.isnull().sum() # Count missing values in each column
Out[34]: Name        0
         Age         1
         City        0
         Salary      0
         JoinDate    1
         dtype: int64
```
```
In [35]: df['City'].unique()
Out[35]: array(['Algiers', 'Oran', 'Constantine', 'Blida'], dtype=object)
```

### 2.6. Selecting & Indexing
Pandas offers several ways to select data from a DataFrame.
* Syntax: `DataFrame.loc[row_indexer, column_indexer]`
* Use `.loc` → when working with labels and multiple values/slices.
* Use `.iloc`→ when working with integer positions and multiple values/slices.
* Use `.at` → when accessing a single value by label (fast).
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
* Use `.iat` → when accessing a single value by integer position (fastest).

```
In [36]: print(df[['Name', 'City']]) # Select multiple columns
      Name         City
0     Amel      Algiers
1     Sami         Oran
2    Rania  Constantine
3   Yacine      Algiers
4     Nour        Blida
```
```
In [37]: print(df.loc[1,:]) # Select a row
Name                 Sami
Age                  28.0
City                 Oran
Salary              54000
JoinDate       2019-03-15
Name: 1, dtype: object
```
```
In [38]: print(df.loc[:, "Age"]) # Select a column
0    25.0
1    28.0
2     NaN
3    35.0
4    22.0
Name: Age, dtype: float64
```
```
In [39]: print(df.iloc[:, 1]) # Select a row
0    25.0
1    28.0
2     NaN
3    35.0
4    22.0
Name: Age, dtype: float64
```
```
In [40]: print(df.loc[0:2, ['Name', 'Age']]) # By Labels
    Name   Age
0   Amel  25.0
1   Sami  28.0
2  Rania   NaN
```
```
In [41]: print(df.iloc[0:2, 0:3]) # By integer positions
   Name   Age     City
0  Amel  25.0  Algiers
1  Sami  28.0     Oran
```
```
In [42]: print(df.at[1, 'Age']) # Fast scalar access
28.0
```
```
In [43]: print(df.iat[1, 2]) # Fast Position-based, single scalar
Oran
```
### 2.7. Filtering Rows
Pandas allows to filter rows based on conditions.
* Use `&` for AND, `|` for OR in multiple conditions.
* Parentheses `()` are required around each condition when using `&` or `|`.
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
* `.query()` allows a string-based syntax that can be easier to read for complex filters.
* `.where()` keeps the same shape as the original DataFrame, replacing non-matching values with `NaN` instead of dropping rows.
```
In [44]: # Filter rows where Age > 25
         print(df['Age']>25)
0    False
1     True
2    False
3     True
4    False
Name: Age, dtype: bool
```
```
In [45]: print(df[df['Age'] > 25])
      Name   Age     City  Salary    JoinDate
1     Sami  28.0     Oran   54000  2019-03-15
3   Yacine  35.0  Algiers   22450        None
```
```
In [46]: # Filter rows with multiple conditions (Age > 25 AND City == 'Algiers')
         df[(df['Age'] > 25) & (df['City'] == 'Algiers')]
Out[46]:
      Name   Age     City  Salary JoinDate
3   Yacine  35.0  Algiers   22450     None
```
```
In [47]: # Using query syntax for readability
         df.query('Salary > 50000 and City == "Oran"')
Out[47]:
   Name   Age  City  Salary    JoinDate
1  Sami  28.0  Oran   54000  2019-03-15
```
```
In [48]: # Using where()
         df_where = df.where(df["Age"] > 30) # Non-matching rows become NaN
         print(df_where)
       Name   Age     City   Salary JoinDate
0       NaN   NaN      NaN      NaN      NaN
1       NaN   NaN      NaN      NaN      NaN
2       NaN   NaN      NaN      NaN      NaN
3    Yacine  35.0  Algiers  22450.0     None
4       NaN   NaN      NaN      NaN      NaN
```
```
In [49]: df_where.dropna(subset=["Age"], inplace=True) # Optionally remove NaN
         print(df_where)
       Name   Age     City   Salary JoinDate
3    Yacine  35.0  Algiers  22450.0     None
```

### 2.8. Adding, Renaming & Deleting Columns
Pandas allows to easily add, rename, and delete columns in a DataFrame.
* After these operations, use `df.head()` to quickly verify changes.
* Use `inplace=True` to apply changes directly to the DataFrame.
```
In [50]: # Adding, Renaming & Deleting Columns
         df['Bonus'] = df['Salary'] * 0.10 # New column
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
         df.rename(columns={'Salary': 'MonthlySalary'}, inplace=True)
         df.drop(columns='Bonus', inplace=True) # Remove column
```
```
In [51]: df.head()
Out[51]:
    Name   Age         City  MonthlySalary    JoinDate
0   Amel  25.0      Algiers          50000  2020-05-10
1   Sami  28.0         Oran          54000  2019-03-15
2  Rania   NaN  Constantine          58000  2021-07-22
3 Yacine  35.0      Algiers          22450        None
4   Nour  22.0        Blida          48000  2022-01-11
```
### 2.9. Data transformation
Data transformation is an essential step to prepare, clean, and manipulate data before analysis.
* Transformation should be done after inspection (checking for missing values, data types, outliers).
* Chain transformations carefully to maintain clean and readable code.
```
In [52]: # create a new copy of a df
         df1 = df.copy()
         # drop missing values
         df.dropna(inplace=True)
```
```
In [53]: print(df)
         print("----------")
         print(df1)
    Name   Age     City  MonthlySalary    JoinDate
0   Amel  25.0  Algiers          50000  2020-05-10
1   Sami  28.0     Oran          54000  2019-03-15
4   Nour  22.0    Blida          48000  2022-01-11
----------
    Name   Age         City  MonthlySalary    JoinDate
0   Amel  25.0      Algiers          50000  2020-05-10
1   Sami  28.0         Oran          54000  2019-03-15
2  Rania   NaN  Constantine          58000  2021-07-22
3 Yacine  35.0      Algiers          22450        None
4   Nour  22.0        Blida          48000  2022-01-11
```
```
In [54]: # --- String Transformation ---
         # Convert all names to uppercase
         df['Name'] = df['Name'].str.upper()
         print(df)
   Name   Age     City  MonthlySalary    JoinDate
0  AMEL  25.0  Algiers          50000  2020-05-10
1  SAMI  28.0     Oran          54000  2019-03-15
4  NOUR  22.0    Blida          48000  2022-01-11
```
```
In [55]: # --- Replacing Values ---
         # Replace 'Blida' with 'Blida City' in the 'City' column
         df['City'] = df['City'].replace('Blida', 'Blida City')
         print(df)
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
   Name   Age        City  MonthlySalary    JoinDate
0  AMEL  25.0     Algiers          50000  2020-05-10
1  SAMI  28.0        Oran          54000  2019-03-15
4  NOUR  22.0  Blida City          48000  2022-01-11
```
```
In [56]: # --- Transforming Values in a Column ---
         # Convert all names in the 'Name' column to lowercase using the map() function.
         # map() applies the given function (lambda x: x.lower()) to each element of the Series.
         df['Name'] = df['Name'].map(lambda x: x.lower())
         print(df)
   Name   Age        City  MonthlySalary    JoinDate
0  amel  25.0     Algiers          50000  2020-05-10
1  sami  28.0        Oran          54000  2019-03-15
4  nour  22.0  Blida City          48000  2022-01-11
```
```
In [57]: # --- Applying Functions ---
         # Create a new column 'AgeGroup' using apply() + lambda
         # (apply() is more flexible and can use multiple columns if needed)
         df['AgeGroup'] = df['Age'].apply(lambda x: 'Young' if x < 30 else 'Senior')
         print(df)
   Name   Age        City  MonthlySalary    JoinDate AgeGroup
0  amel  25.0     Algiers          50000  2020-05-10    Young
1  sami  28.0        Oran          54000  2019-03-15    Young
4  nour  22.0  Blida City          48000  2022-01-11    Young
```
```
In [58]: # --- Changing Data Types ---
         # Convert MonthlySalary from float to int
         df['MonthlySalary'] = df['MonthlySalary'].astype(int)
         print(df)
   Name   Age        City  MonthlySalary    JoinDate AgeGroup
0  amel  25.0     Algiers          50000  2020-05-10    Young
1  sami  28.0        Oran          54000  2019-03-15    Young
4  nour  22.0  Blida City          48000  2022-01-11    Young
```
```
In [59]: # Define a custom function
         def simplify(x):
             if x == "Young":
                 return "Y"
             elif x == "Senior":
                 return "S"
             else:
                 return x
         # Apply the function to the 'Age' column
         df["Age_Short"] = df["Age"].apply(simplify)
         df
Out[59]:
   Name   Age        City  MonthlySalary    JoinDate AgeGroup  Age_Short
0  amel  25.0     Algiers          50000  2020-05-10    Young       25.0
1  sami  28.0        Oran          54000  2019-03-15    Young       28.0
4  nour  22.0  Blida City          48000  2022-01-11    Young       22.0
```
### 2.10. Sorting & Ranking
* `sort_values()`: Reorders the rows in the DataFrame based on a column's values.
* `rank()`: Assigns a ranking number to each value but keeps the original row order.
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
In [60]: df = pd.DataFrame({
            'Name': ['Amel', 'Sami', 'Rania', 'Yacine', 'Nour'],
            'Age': [25, 28, 28, 35, 22],
            'City': ['Algiers', 'Oran', 'Constantine', 'Algiers', 'Blida'],
            'Salary': [50000, 54000, 58000, 22450, 48000],
            'JoinDate': ['2020-05-10', '2019-03-15', '2021-07-22', '2022-01-11', '2022-01-11']
         })
         df
Out[60]:
     Name  Age         City  Salary    JoinDate
0    Amel   25      Algiers   50000  2020-05-10
1    Sami   28         Oran   54000  2019-03-15
2   Rania   28  Constantine   58000  2021-07-22
3  Yacine   35      Algiers   22450  2022-01-11
4    Nour   22        Blida   48000  2022-01-11
```
```
In [61]: df.sort_values(by='Salary', ascending=True, inplace=True)
         df
Out[61]:
     Name  Age         City  Salary    JoinDate
3  Yacine   35      Algiers   22450  2022-01-11
4    Nour   22        Blida   48000  2022-01-11
0    Amel   25      Algiers   50000  2020-05-10
1    Sami   28         Oran   54000  2019-03-15
2   Rania   28  Constantine   58000  2021-07-22
```
```
In [62]: df['DateRank'] = df['JoinDate'].rank(ascending=True)
         df
Out[62]:
     Name  Age         City  Salary    JoinDate  DateRank
3  Yacine   35      Algiers   22450  2022-01-11       4.5
4    Nour   22        Blida   48000  2022-01-11       4.5
0    Amel   25      Algiers   50000  2020-05-10       2.0
1    Sami   28         Oran   54000  2019-03-15       1.0
2   Rania   28  Constantine   58000  2021-07-22       3.0
```
### 2.11. Grouping & Aggregation
allow to split data into groups based on specific columns and apply summary functions (like mean, sum, or count) to each group.
```
In [63]: grouped = df.groupby('Age').sum()
         grouped
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
Out[63]:
        Name          City   Salary       JoinDate  DateRank
Age
22      Nour         Blida    48000     2022-01-11       4.5
25      Amel       Algiers    50000     2020-05-10       2.0
28  SamiRania  OranConstantine  112000  2019-03-152021-07-22       4.0
35    Yacine       Algiers    22450     2022-01-11       4.5
```
```
In [64]: grouped = df.groupby('City').agg({
             'Salary': ['mean', 'max', 'min'],
             'Age': 'mean'
         })
         grouped
Out[64]:
                     Salary           Age
                       mean    max    min  mean
City
Algiers           36225.0  50000  22450  30.0
Blida             48000.0  48000  48000  22.0
Constantine       58000.0  58000  58000  28.0
Oran              54000.0  54000  54000  28.0
```
### 2.12. Merging & Concatenation
* `pd.merge()` is used to combine two DataFrames based on a column
* `pd.concatenate()` is used to concatenate horizontaly/vertically | Operation | Purpose | Joins By | Example | | --- | --- | --- | --- | --- | `merge()` | Combine DataFrames by common column(s) | Column values | `pd.merge(df, dept, on='City')` | `concat()` | Combine DataFrames by rows or columns | Index position | `pd.concat([df, df2])` |
```
In [65]: # Second DataFrame
         dept = pd.DataFrame({
             'City': ['Algiers', 'Oran', 'Constantine', 'Blida City'],
             'Department': ['HR', 'IT', 'Finance', 'Marketing']
         })
         # Merge on common column
         merged = pd.merge(df, dept, on='City', how='left') # how: left, inner, right, outer
         merged
Out[65]:
     Name  Age         City  Salary    JoinDate  DateRank Department
0  Yacine   35      Algiers   22450  2022-01-11       4.5         HR
1    Nour   22        Blida   48000  2022-01-11       4.5        NaN
2    Amel   25      Algiers   50000  2020-05-10       2.0         HR
3    Sami   28         Oran   54000  2019-03-15       1.0         IT
4   Rania   28  Constantine   58000  2021-07-22       3.0    Finance
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
In [66]: #Concatenate vertically (one below another)
         df2 = pd.DataFrame({
             'Name': ['Hana'],
             'City': ['Setif'],
             'Salary': [4800]
         })
         # Stack rows (same columns)
         concatenated = pd.concat([df, df2], ignore_index=True)
         print("\n---- CONCATENATED (Vertical) ----")
         print(concatenated)

---- CONCATENATED (Vertical) ----
     Name   Age         City   Salary    JoinDate  DateRank
0  Yacine  35.0      Algiers  22450.0  2022-01-11       4.5
1    Nour  22.0        Blida  48000.0  2022-01-11       4.5
2    Amel  25.0      Algiers  50000.0  2020-05-10       2.0
3    Sami  28.0         Oran  54000.0  2019-03-15       1.0
4   Rania  28.0  Constantine  58000.0  2021-07-22       3.0
5    Hana   NaN        Setif   4800.0         NaN       NaN
```
```
In [67]: # Combine DataFrames column-wise (axis=1), Horizontaly
         concat_side = pd.concat([df, df2], axis=1)
         print("\n---- CONCATENATED (Horizontal) ----")
         print(concat_side)

---- CONCATENATED (Horizontal) ----
     Name   Age         City   Salary    JoinDate  DateRank  Name   City   Salary
3  Yacine  35.0      Algiers  22450.0  2022-01-11       4.5   NaN    NaN      NaN
4    Nour  22.0        Blida  48000.0  2022-01-11       4.5   NaN    NaN      NaN
0    Amel  25.0      Algiers  50000.0  2020-05-10       2.0  Hana  Setif   4800.0
1    Sami  28.0         Oran  54000.0  2019-03-15       1.0   NaN    NaN      NaN
2   Rania  28.0  Constantine  58000.0  2021-07-22       3.0   NaN    NaN      NaN
```
### 2.13. Pivot Tables & Reshaping

| Function | Category | Purpose | Key Parameters | What It Does | When to Use |
|---|---|---|---|---|---|
| **pivot()** | Reshaping | Reorganize data (wide format) | `index`, `columns`, `values` | Creates a new table by turning unique combinations of `index` and `columns` into cells. | When your data has **unique index/column pairs** and you just want to reshape (no aggregation). |
| **pivot_table()** | Summarization | Aggregate and reshape data | `index`, `columns`, `values`, `aggfunc` | Works like `pivot()`, but handles **duplicates** by applying an **aggregation** (default = mean). | When your data has **duplicates** or you need to **summarize** numeric data. |
| **melt()** | Reshaping | Unpivot data (long format) | `id_vars`, `value_vars`, `var_name`, `value_name` | Converts columns into rows, creating a long and tidy structure. | When you need to **prepare data for plotting, modeling, or normalization.** |

```
In [68]: df = pd.read_csv('sample_10_rows.csv')
         print(df)
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
    Name   Age         City  Salary    JoinDate
0   Amel  25.0      Algiers   50000  2020-05-10
1   Sami  28.0         Oran   54000  2019-03-15
2  Rania   NaN  Constantine   58000  2021-07-22
3 Yacine  35.0      Algiers   22450         NaN
4   Nour  22.0        Blida   48000  2022-01-11
5  Farid  40.0        Setif   60000  2018-09-03
6   Lina  27.0         Oran   52000  2020-11-25
7  Karim  30.0        Blida   45000  2021-02-14
8  Sofia   NaN      Algiers   47000         NaN
9  Walid  33.0  Constantine   53000  2019-12-30
```
#### a) `pivot()` — Reshaping Data in Pandas
`pivot()` creates a new DataFrame where one column becomes the **index**, another defines the **columns**, and a third provides the cell **values**.

**Note:** Each combination of `index` / `columns` must be **unique** — otherwise, use `pivot_table()`.

**General Syntax**
`new_df = df.pivot(index='col1', columns='col2', values='col3')`
* `col1` → becomes the row index of the new table
* `col2` → becomes the new columns
* `col3` → fills the cell values
```
In [69]: df1 = df.drop_duplicates(subset="City", keep="first")
         print(df1)
    Name   Age         City  Salary    JoinDate
0   Amel  25.0      Algiers   50000  2020-05-10
1   Sami  28.0         Oran   54000  2019-03-15
2  Rania   NaN  Constantine   58000  2021-07-22
4   Nour  22.0        Blida   48000  2022-01-11
5  Farid  40.0        Setif   60000  2018-09-03
```
```
In [70]: pivot_df = df1.pivot(index='City', columns='JoinDate', values='Salary')
         print("\nPivot result:")
         print(pivot_df)

Pivot result:
JoinDate     2018-09-03  2019-03-15  2020-05-10  2021-07-22  2022-01-11
City
Algiers             NaN         NaN     50000.0         NaN         NaN
Blida               NaN         NaN         NaN         NaN     48000.0
Constantine         NaN         NaN         NaN     58000.0         NaN
Oran                NaN     54000.0         NaN         NaN         NaN
Setif           60000.0         NaN         NaN         NaN         NaN
```
#### b) `pivot_table()` — Creating Summarized Tables in Pandas
`pivot_table()` works like `pivot()`, but it allows **duplicate combinations** of index/columns by applying an **aggregation function** (like `mean`, `sum`, etc.).

**Note:** It's more flexible than `pivot()` because it can handle repeated values.

**General Syntax**
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
new_df = df.pivot_table(
    index='col1',
    columns='col2',
    values='col3',
    aggfunc='mean'  # default aggregation is 'mean'
)
```
```
In [71]: pivot_table = df.pivot_table(
             index='City', # become the index
             values='Age', # column to summarize
             aggfunc='mean' # aggregate duplicates using mean
         )
         print(pivot_table)
                   Age
City
Algiers      30.0
Blida        26.0
Constantine  33.0
Oran         27.5
Setif        40.0
```
#### c) `melt()` — Unpivoting (Reshaping) Data in Pandas
`melt()` performs the **opposite** of `pivot()`:
it **turns columns into rows**, making the data **longer** instead of wider.
It's useful for **normalizing** or **preparing data for analysis and visualization**.

**General Syntax**
```
new_df = df.melt(
    id_vars=['col1'],       # columns to keep as identifiers
    value_vars=['col2', 'col3'], # columns to unpivot
    var_name='variable',    # name for the new column holding former column names
    value_name='value'      # name for the new column holding values
)
```
```
In [72]: # unpivot df
         df_melted = df.melt(
             id_vars=["Name", "City"],      # columns to keep fixed
             value_vars=["Age", "Salary"], # columns to unpivot
             var_name="Attribute",          # name of the new column for former column names
             value_name="Value"            # name of the new column for the data
         )
         print(df_melted)
```
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
```
      Name         City Attribute      Value
0     Amel      Algiers       Age       25.0
1     Sami         Oran       Age       28.0
2    Rania  Constantine       Age        NaN
3   Yacine      Algiers       Age       35.0
4     Nour        Blida       Age       22.0
5    Farid        Setif       Age       40.0
6     Lina         Oran       Age       27.0
7    Karim        Blida       Age       30.0
8    Sofia      Algiers       Age        NaN
9    Walid  Constantine       Age       33.0
10    Amel      Algiers    Salary    50000.0
11    Sami         Oran    Salary    54000.0
12   Rania  Constantine    Salary    58000.0
13  Yacine      Algiers    Salary    22450.0
14    Nour        Blida    Salary    48000.0
15   Farid        Setif    Salary    60000.0
16    Lina         Oran    Salary    52000.0
17   Karim        Blida    Salary    45000.0
18   Sofia      Algiers    Salary    47000.0
19   Walid  Constantine    Salary    53000.0
```
```
In [73]: import seaborn as sns
         import matplotlib.pyplot as plt

         sns.barplot(
             data=df_melted,
             x="Name",
             y="Value",
             hue="Attribute" # différencie Age et Salary
         )
         plt.title("Comparison of Age and Salary by Person")
         plt.show()
```
![A bar plot showing side-by-side bars for Age and Salary for each person. The Age bars are not visible because their scale is much smaller than the Salary bars.](comparison_age_salary.png)
*Age doesn't appear in the bar plot, why?*
---
*Essential Python Libraries for Data Science – Amel Boustil*
---
### 2.14. Time Series in Pandas
A time series is a sequence of data points indexed by time (daily, monthly, yearly...).
Pandas provides powerful tools for analyzing and transforming time-based data.
```
In [74]: data = {
             "Name": ["nour", "amel", "sami"],
             "JoinDate": ["2022-01-11", "2020-05-10", "2019-03-15"],
         }
         df = pd.DataFrame(data)
         print(df.dtypes)
         
         df["JoinDate"] = pd.to_datetime(df["JoinDate"])
         print("-----")
         print(df)
         print("-----")
         # Vérifier le type
         print(df.dtypes)

Name        object
JoinDate    object
dtype: object
-----
   Name   JoinDate
0  nour 2022-01-11
1  amel 2020-05-10
2  sami 2019-03-15
-----
Name                object
JoinDate    datetime64[ns]
dtype: object
```
### 2.15. Exporting Data
Pandas provides simple functions to save DataFrames into different file formats such as CSV, Excel, JSON, or SQL.

#### Common Export Functions

| Function | Description | Example |
|---|---|---|
| `df.to_csv('file.csv', index=False)` | Export to CSV (comma-separated values) | Saves the DataFrame as a CSV file |
| `df.to_excel('file.xlsx', index=False)` | Export to Excel | Requires the `openpyxl` package |
| `df.to_json('file.json')` | Export to JSON format | Good for web data exchange |
| `df.to_html('file.html')` | Export to HTML table | Can be displayed in a browser |
| `df.to_sql('table_name', conn)` | Write to a SQL database | Needs a valid database connection |
| `df.to_pickle('file.pkl')` | Save in binary format (fast read/write) | For internal Python use only |

---
*Essential Python Libraries for Data Science – Amel Boustil*
---
#### Common Parameters
* `index=False` → do not include the index column in the output
* `sep=';'` → change the separator for CSV files
* `header=False` → skip column names
* `encoding='utf-8'` → set text encoding
```
In [75]: # Exporting Data
         merged.to_csv('employees_cleaned.csv', index=False)
```
### Takeaway:
Pandas is a Swiss-army knife for data analysis
* from loading data to cleaning, transforming, aggregating, and visualizing it
* all in just a few lines of code.

---
*Essential Python Libraries for Data Science – Amel Boustil*
---

# Chapter 04: Essential Python Libraries for Data Science: Part 02
## Matplotlib — Essential Library for Data Visualization
### Definition
**Matplotlib** is the core Python library for data visualization.
It allows to create **static**, **animated**, and **interactive** plots easily.
Built on NumPy, it turns raw data into clear and insightful graphics

### Why Learn Matplotlib?
* Foundation of most Python plotting libraries (e.g. Seaborn, Pandas plot)
* Full control over colors, labels, styles, and figure layouts
* upports dozens of plot types (line, bar, scatter, histogram, etc.)
* Export plots in many formats (PNG, PDF, SVG...)

## 3.1 Matplotlib: Functional vs Object-Oriented Interface
### 3.1.1. Functional (Pyplot) style in Matplotlib
means using functions from the **matplotlib.pyplot** module directly to create and modify plots — similar to MATLAB.

```python
In [1]: import matplotlib.pyplot as plt
        import numpy as np
        x = [1, 2, 3, 4]
        y = [2, 4, 6, 8]

        plt.figure(figsize=(5,3))
        plt.plot(x, y, 'o-', label="y = 2x")
        plt.title("Functional Style Example")
        plt.xlabel("X axis")
        plt.ylabel("Y axis")
        plt.legend()
        plt.show()
```

![Functional Style Example plot showing a line y=2x with circular markers.](functional_style_example.png)

### 2. Object-Oriented (OO) Style
Object-Oriented (OO) style in Matplotlib means creating and controlling figure and axes objects explicitly, then calling their methods to build the plot.

```python
In [2]: import matplotlib.pyplot as plt
        import numpy as np
        fig, ax = plt.subplots(figsize=(5,3))
        ax.plot(x, y, 's--', color='orange', label="y = 2x")
        ax.set_title("Object-Oriented Style Example")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.legend()
        plt.show()
```

![Object-Oriented Style Example plot showing a dashed orange line y=2x with square markers.](object_oriented_style_example.png)

### 3.2. General Syntax of matplotlib.pyplot.plot()
The basic syntax is:
`plt.plot(x, y, format_string, **kwargs)`

### where:
*   **x**: sequence of x-values
*   **y**: sequence of y-values
*   **format_string** : optional shorthand for **color, marker,** and **line style**
*   **\*\*kwargs** : additional keyword arguments (like label, linewidth, etc.)
*   **\*\*** : is used to unpack a dictionary into keyword arguments.
*   **color**: r, b, g, '#1f77b4', etc.
*   **marker**: -, --, :, -., etc.
*   **line style**: o, s, +, x, *, ^, etc.

```python
In [3]: import matplotlib.pyplot as plt
        import numpy as np
        # 2. Example Data
        x = np.linspace(0, 10, 50)
        y = np.sin(x)

        # Using Format String
        # Format string: 'color marker linestyle'
        # Example: 'r--o' means red dashed line with circle markers

        plt.figure(figsize=(6,4))
        plt.plot(x, y, 'r--o', label='sin(x)')
        plt.title("Using Format String")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.show()
```
![A plot of sin(x) from 0 to 10. The line is red, dashed, and has circle markers.](using_format_string.png)

```python
In [4]: # Common Keyword Arguments (**kwargs)
        plt.plot(
            x, y,
            color='green',        # Line color
            linestyle='--',       # '-', '--', '-.', ':'
            linewidth=2,          # line thickness
            marker='s',           # marker style: 'o', 's', '^', 'x', etc.
            markersize=6,         # marker size
            label='sin(x)',       # Label for Legend
            alpha=0.7             # transparency (0-1)
        )
        plt.title("Using Keyword Arguments")
        plt.xlabel("X axis")
        plt.ylabel("Y axis")
        plt.legend()
        plt.show()
```

![A plot of sin(x) from 0 to 10. The line is green, dashed, with square markers, and a line width of 2.](using_keyword_arguments.png)

```python
In [5]: # Plotting Multiple Lines
        plt.figure(figsize=(5,3))

        plt.figure(figsize=(8,5))
        style2 = {'color': 'blue', 'marker': 's', 'linestyle': '-.', 'linewidth': 2, 'label': 'blue s
        style3 = {'color': 'green', 'marker': '^', 'linestyle': ':', 'linewidth': 2, 'label': 'green

        plt.plot(x, np.sin(x), **style2)
        plt.plot(x, np.cos(x), **style3)
        plt.title("Multiple Lines in One Plot")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.show()
<Figure size 500x300 with 0 Axes>
```

![A plot showing both sin(x) and cos(x). Sin(x) is a blue dash-dot line with square markers. Cos(x) is a green dotted line with triangle markers.](multiple_lines_plot.png)

### 3.3. The Lifecycle of a Matplotlib Figure (Object Oriented Approach)
*   **Create a Figure** : A figure is the overall window or page that everything is drawn on.
*   **Add Axes (Subplots)** : Axes are the actual plotting areas inside the figure.
    `fig, ax = plt.subplots(figsize=(x,y))`
*   **Plot Data**: Use plot commands to add lines, markers, or other graphical elements.
    Example:
    ```python
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y, label='sin(x)', color='blue')
    ```
*   **Customize the Plot**: Add labels, titles, legends, and grid lines.
    Example:
    ```python
    ax.set_title("Sine Wave")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()
    ax.grid(True)
    ```
*   **Render (Display) the Figure**
    `plt.show()`
*   **Save the Figure**
    `plt.savefig("filename.png")`
*   **Close the Figure (optional)**
    `plt.close(fig)`

### 3.4. Choosing the Right Chart Type

| Chart Type | When to Use It | Description / Best For | Example Code |
| :--- | :--- | :--- | :--- |
| **Line Chart** (`plt.plot()`) | Use when data changes **over time** (months, years, days). | Great for showing **trends or progression** — e.g., sales growth, temperature change. | `plt.plot(months, sales, marker='o')plt.title("Sales Over Time")` |
| **Bar Chart** (`plt.bar()`) | Use when comparing **categories** or **groups**. | Best for **discrete data** — e.g., sales by product, students per class. | `plt.bar(products, sales) plt.title("Sales by Product")` |
| **Scatter Plot** (`plt.scatter()`) | Use to show **relationship or correlation** between two numeric variables. | Helps detect **patterns or clusters** — e.g., age vs income, height vs weight. | `plt.scatter(age, income) plt.title("Age vs Income")` |
| **Histogram** (`plt.hist()`) | Use to show the **distribution** of a single numeric variable. | Great for visualizing **frequency or spread** - e.g., exam scores, ages, salaries. | `plt.hist(ages, bins=10) plt.title("Age Distribution")` |
| **Pie Chart** (`plt.pie()`) | Use to show **proportions or percentages** of a whole (for a single variable). | Best for showing **composition** — e.g., market share, budget allocation. | `plt.pie(sizes, labels=categories, autopct='%1.1f%%') plt.title("Market Share")` |

```python
In [5]: import pandas as pd
        import matplotlib.pyplot as plt
        data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Sales": [1200, 1500, 1700, 1600, 2800, 2000],
            "Profit": [200, 300, 250, 280, 350, 400],
            "Category": ["A", "B", "C", "A", "B", "C"]
        }
        df = pd.DataFrame(data)
        df
Out[5]:
  Month  Sales  Profit Category
0   Jan   1200     200        A
1   Feb   1500     300        B
2   Mar   1700     250        C
3   Apr   1600     280        A
4   May   2800     350        B
5   Jun   2000     400        C
```
```python
In [6]: # Line Chart - Show Trend Over Time
        plt.plot(df["Month"], df["Sales"], marker='o', color='teal')
        plt.title("Sales Over Time")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.show()
```

![Line chart showing sales trend over months from Jan to Jun.](sales_over_time.png)

```python
In [9]: # Bar Chart - Compare Categories
        plt.bar(df["Month"], df["Sales"], color='teal')
        plt.title("Sales by Month")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.show()
```

![Bar chart showing sales for each month. May has the highest sales.](sales_by_month.png)

```python
In [10]: # Scatter Plot - Relationship Between Sales and Profit
         plt.scatter(df["Sales"], df["Profit"], color='teal')
         plt.title("Sales vs Profit")
         plt.xlabel("Sales")
         plt.ylabel("Profit")
         plt.show()
```

![Scatter plot of Sales vs Profit, showing a positive but not strongly linear relationship.](sales_vs_profit.png)

```python
In [11]: # Histogram - distribution of a variable
         plt.hist(df["Sales"], bins=5, color='teal', edgecolor='black')
         plt.title("Sales Distribution")
         plt.xlabel("Sales")
         plt.ylabel("Frequency")
         plt.show()
```

![Histogram showing the frequency distribution of sales data.](sales_distribution.png)

```python
In [13]: # Pie Chart - proportions of a whole
         plt.pie(df["Sales"], labels=df["Month"], autopct='%1.2f%%')
         plt.title("Sales Share by Month")
         plt.show()
```

![Pie chart showing the percentage share of sales for each month.](sales_share_by_month.png)

### 3.5. Subplot / Subplots
#### a- The `subplot()` function in Matplotlib allows displaying multiple plots within a single figure.
The figure is divided into a grid (rows × columns) and draw a different chart in each section.

**Basic Syntax**
`plt.subplot(nrows, ncols, index)`
Where:
*   `nrows`: Number of rows in the subplot grid
*   `ncols`: Number of columns in the subplot grid
*   `index`: Position of the current plot (starts at 1)
```python
In [24]: import matplotlib.pyplot as plt
         # Figure with 2 rows and 1 column
         plt.figure(figsize=(15,5))
         # 1st subplot
         plt.subplot(1, 2, 1) # colomn 1
         plt.plot([1, 2, 3], [4, 5, 6])
         plt.title("Subplot 1")
         # 2nd subplot
         plt.subplot(1, 2, 2) # colomn 2
         plt.plot([1, 2, 3], [6, 5, 4])
         plt.title("Subplot 2")
         plt.tight_layout() # adjust spacing
         plt.show()
```

![Two subplots side-by-side. Subplot 1 is an upward sloping line. Subplot 2 is a downward sloping line.](subplots_1.png)

#### b.The `subplots()` function in Matplotlib allows creating multiple plots in one figure using the object-oriented (OO) approach.
It returns a figure object and an array of axes objects, which can be used to plot individually on each subplot.

**Basic Syntax**
`fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))`
```python
In [25]: fig, axes = plt.subplots(1, 2, figsize=(8, 4))
         axes[0].plot([1, 2, 3], [2, 4, 6])
         axes[0].set_title("Line Chart")

         axes[1].bar(["A", "B", "C"], [5, 3, 7])
         axes[1].set_title("Bar Chart")

         plt.tight_layout()
         plt.show()
```
![Two subplots: a Line Chart on the left and a Bar Chart on the right.](subplots_2.png)
```
<Figure size 640x480 with 0 Axes>
```
### 3.6. Functions to Learn: `plt.text()` vs `plt.annotate()`

| Function | Description | Example Code |
| :--- | :--- | :--- |
| `plt.text(x, y, "Text")` | Adds simple text at coordinates (x, y) — no arrow or pointer. Used for labels or comments directly on the plot. | `plt.text(2, 50, "High Value", color="blue", fontsize=12)` |
| `plt.annotate("Label", xy=(x, y), xytext=(x2, y2), arrowprops=...)` | Adds an annotation with a pointer. `xy` marks the point, `xytext` sets where the text is placed, and `arrowprops` defines arrow style. | `plt.annotate("Peak", xy=(5, 80), xytext=(3, 90), arrowprops=dict(facecolor='red', arrowstyle='->'))` |

## 4. Seaborn: Statistical Data Visualization
Seaborn is a **high-level data visualization library** built on top of Matplotlib.
It provides **beautiful, easy-to-use** functions for **statistical plots**, especially when working with **Pandas DataFrames**.

### 4.1. Key Features
* Simplifies complex visualizations.
* Automatically integrates with Pandas.
* Adds colors, themes, and statistical elements (confidence intervals, regression lines, etc.).

```python
In [13]: ### Import and Setup
         import matplotlib.pyplot as plt
         import seaborn as sns
         import pandas as pd
         import numpy as np

         # Example dataset
         tips = sns.load_dataset("tips") # built-in dataset
         tips.head()

Out[13]:
   total_bill   tip     sex smoker  day   time  size
0       16.99  1.01  Female     No  Sun  Dinner     2
1       10.34  1.66    Male     No  Sun  Dinner     3
2       21.01  3.50    Male     No  Sun  Dinner     3
3       23.68  3.31    Male     No  Sun  Dinner     2
4       24.59  3.61  Female     No  Sun  Dinner     4
```
```python
In [14]: # Simple scatter plot: total bill vs tip
         sns.scatterplot(x="total_bill", y="tip", data=tips)

         # Show the plot
         plt.show()
```
![A scatter plot showing the relationship between total bill and tip amount.](seaborn_scatterplot.png)

### 4.2. Seaborn: General Syntax of Plotting Functions
Seaborn plotting functions generally follow a **consistent structure**, which makes it easy to create a wide variety of statistical plots.

**General Syntax**
```python
sns.<plot_function>(
    data=None,      # pandas DataFrame or array-like data
    x=None,         # column name or array for x-axis
    y=None,         # column name or array for y-axis
    hue=None,       # variable name for color encoding
    style=None,     # variable name for marker style (scatter plots)
    size=None,      # variable name for marker size
    palette=None,   # color palette (e.g., "Set1", "coolwarm")
    kind=None,      # type of plot (used in functions like sns.catplot)
    **kwargs        # other options like markers, linewidth, alpha, etc.
)
```

### 4.3. Seaborn Workflow: From Data to Plots
Seaborn provides a **structured workflow** to create statistical visualizations. The cycle typically has **four main steps**:

#### a- Prepare the Data
*   Use a **pandas DataFrame** or array-like structure.
*   Make sure the data is **clean and structured** (one column per variable).

```python
In [33]: import pandas as pd
         import numpy as np
         data = pd.DataFrame({
             'x': np.arange(1, 21),
             'y': np.random.normal(0, 5, 20),
             'category': ['A','B']*10
         })
```

#### b- Set Figure Aesthetics
*   Choose themes, styles, and context for consistent and attractive plots.
*   Functions:
    *   `sns.set_theme()`: Sets the overall visual theme,
    *   `sns.set_style()`: Adjusts only the background style and grid,
    *   `sns.set_context()`: Modifies text sizes and elements

```python
In [16]: import seaborn as sns
         sns.set_theme(style="whitegrid", palette="pastel")
         sns.set_context("talk") # sns.set_style("darkgrid")

         sns.set_style("whitegrid") # sns.set_context("talk")
```

#### c- Plot with Seaborn
Select a plot type depending on the data:
*   **Relational plots**: `sns.scatterplot()`, `sns.lineplot()`
*   **Distribution plots**: `sns.histplot()`, `sns.kdeplot()`
*   **Categorical plots**: `sns.boxplot()`, `sns.violinplot()`
*   **Matrix plots**: `sns.heatmap()`

#### d- Further Customization
Refine plots with:
*   **Titles**: `plt.title()`
*   **Labels**: `plt.xlabel()`, `plt.ylabel()`
*   **Legends**: `plt.legend()`
*   **Axis limits and ticks**:
    *   `plt.xlim()`: Set limits for x-axis (example: `plt.xlim(0,5)`)
    *   `plt.ylim()`: Set limits for y-axis(example : `plt.ylim(0,40)`)
    *   `plt.xticks(rotation=45)`: Rotate or customize x-axis tick labels (example: `plt.xticks(rotation=45)`)

```python
In [34]: # Seaborn Workflow Example with Tips Dataset
         import seaborn as sns
         import matplotlib.pyplot as plt

         # Prepare the Data
         tips = sns.load_dataset("tips")

         # Set Figure Aesthetics
         sns.set_theme(style="whitegrid", palette="pastel")
         sns.set_context("talk") # Bigger fonts for presentations
         #sns.set_style("darkgrid") # Grille foncée

         # Plot with Seaborn
         plt.figure(figsize=(8,5))
         scatter = sns.scatterplot(
             data=tips,
             x='total_bill',
             y='tip',
             hue='sex',
             s=120
         )

         # Further Customization
         plt.title("Tips Dataset: Total Bill vs Tip")
         plt.xlabel("Total Bill ($)")
         plt.ylabel("Tip ($)")
         plt.xticks(rotation=0)
         plt.legend(title="sex")
         plt.show()
```

![A scatter plot of Total Bill vs Tip, with points colored by sex (Male/Female).](tips_dataset_plot.png)

```python
In [18]: # Examples of other plots on tips
         # Distribution plot
         plt.figure(figsize=(6,4))
         sns.histplot(tips['tip'], bins=10, color='skyblue')
         plt.title("Distribution of Tips")
         plt.show()
```

![A histogram showing the distribution of tip amounts, which is right-skewed.](distribution_of_tips.png)

```python
In [19]: # Boxplot
         # Create a boxplot to show the distribution of tips by day
         # hue='sex' separates the boxes by gender, palette='Set2' sets the colors
         plt.figure(figsize=(6,4))
         sns.boxplot(x='day', y='tip', data=tips, hue='sex', palette='Set2')
         plt.title("Boxplot of Tips by Day")
         plt.show()
```

![Side-by-side boxplots for each day of the week, further split by sex, showing the distribution of tips.](boxplot_tips_by_day.png)

```python
In [20]: # Heatmap example (correlation)
         corr = tips[['total_bill', 'tip', 'size']].corr()
         plt.figure(figsize=(4,3))
         sns.heatmap(corr, annot=True, cmap="coolwarm")
         plt.title("Correlation Heatmap")
         plt.show()
```

![A heatmap showing the correlation matrix for total_bill, tip, and size.](correlation_heatmap.png)

```python
In [21]: ### Tip: Always start the visualization with a **theme** and **palette** for consistent style
         sns.set_style("whitegrid") # or: darkgrid, white, ticks
         sns.set_palette("pastel")    # or: deep, muted, bright, etc.
```

### 5. Introduction to Plotly in Python
**Plotly** is a Python library for creating **interactive and dynamic plots**.
Unlike Matplotlib or Seaborn (static), Plotly allows to:
*   Zoom, pan, and hover over data points
*   Create 3D plots and interactive maps
*   Integrate easily in notebooks and dashboards

```
In [22]: ## Installation
         !pip install plotly

Requirement already satisfied: plotly in c:\users\pc\anaconda3\lib\site-packages (5.24.1)
Requirement already satisfied: tenacity>=6.2.0 in c:\users\pc\anaconda3\lib\site-packages (from plotly) (9.0.0)
Requirement already satisfied: packaging in c:\users\pc\anaconda3\lib\site-packages (from plotly) (24.2)
```
```python
In [23]: ## importing: plotly.express (alias px) is the simplest module to create interactive
         ## plots with just a few lines of code.
         import plotly.express as px
         import pandas as pd
```
```python
In [24]: df = pd.DataFrame({
             'Fruit': ['Apples', 'Bananas', 'Cherries', 'Oranges'],
             'Quantity': [10, 15, 7, 12]
         })
```
```python
In [25]: fig = px.bar(df, x='Fruit', y='Quantity', title='Fruit Quantity')
         fig.show()
```

![An interactive bar chart from Plotly showing the quantity of different fruits.](plotly_fruit_quantity.png)
*   **Hover**: shows exact values
*   **Zoom/Pan**: zoom in on specific parts
*   **Download**: button to export the figure

```python
In [26]: import pandas as pd
         import plotly.express as px

         df = pd.DataFrame({
             'x': [1,2,3,4],
             'y': [10,15,13,17],
             'category': ['A','B','A','B']
         })
         fig = px.scatter(df, x='x', y='y', color='category', size='y',
                         title='Scatter Plot Example')
         fig.show()
```

![An interactive scatter plot from Plotly where points are colored by category and sized by the y-value.](plotly_scatter_example.png)

```python
In [27]: fig = px.scatter(tips, x='total_bill', y='tip', color='sex',
                          size='size', hover_data=['day', 'time'],
                          title='Tip vs Total Bill by Sex and Table Size')
         fig.show()
```

![An interactive scatter plot of the tips dataset. Hovering over points reveals additional data like day and time.](plotly_tips_scatter.png)

```python
In [28]: # Compute average tip by party size
         avg_tip = tips.groupby('size', as_index=False)['tip'].mean()
         avg_tip.rename(columns={'tip': 'Average Tip'}, inplace=True)

         # Compute count of observations per size
         counts = tips.groupby('size')['tip'].count().reset_index()
         counts.rename(columns={'tip':'Count'}, inplace=True)

         # Merge avg_tip and counts
         avg_tip = avg_tip.merge(counts, on='size')

         # Plot line chart with hover info
         fig = px.line(avg_tip, x='size', y='Average Tip', markers=True,
                       title='Average Tip by Party Size',
                       hover_data={'size':True, 'Average Tip':':.2f', 'Count':True})
         fig.show()
```

![An interactive line chart showing how the average tip changes with party size. Hovering shows the count of observations.](plotly_avg_tip_by_party_size.png)

```python
In [29]: # px.line explores how tip amount changes with the size of the party.
```

### 6. Introduction to Basemap
*   **Basemap** is a toolkit for **Matplotlib** that allows to create **2D maps** and visualize geospatial data.
*   It is useful for plotting **coastlines, countries, rivers**, and **overlaying points-lines** using geographic coordinates.
*   Note: Basemap is **deprecated** in favor of **Cartopy**, which is more modern and maintained. But Basemap is still used in legacy projects.

```
In [30]: ## Installation
         !pip install basemap
```
```
Requirement already satisfied: basemap in c:\users\pc\anaconda3\lib\site-packages (2.0.0)
Requirement already satisfied: basemap_data<3.0,>=2.0 in c:\users\pc\anaconda3\lib\site-packages (from basemap) (2.0.0)
Requirement already satisfied: packaging<26.0,>=20.5 in c:\users\pc\anaconda3\lib\site-packages (from basemap) (24.2)
Requirement already satisfied: numpy<2.4,>=2.0 in c:\users\pc\anaconda3\lib\site-packages (from basemap) (2.1.3)
Requirement already satisfied: matplotlib<3.11,>=3.4 in c:\users\pc\anaconda3\lib\site-packages (from basemap) (3.10.0)
Requirement already satisfied: pyproj<3.8,>=3.0 in c:\users\pc\anaconda3\lib\site-packages (from basemap) (3.7.2)
Requirement already satisfied: pyshp<2.4,>=2.0 in c:\users\pc\anaconda3\lib\site-packages (from basemap) (2.3.1)
Requirement already satisfied: contourpy>=1.0.1 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (1.3.1)
Requirement already satisfied: cycler>=0.10 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (0.11.0)
Requirement already satisfied: fonttools>=4.22.0 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (4.55.3)
Requirement already satisfied: kiwisolver>=1.3.1 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (1.4.8)
Requirement already satisfied: pillow>=8 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (11.1.0)
Requirement already satisfied: pyparsing>=2.3.1 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (3.2.0)
Requirement already satisfied: python-dateutil>=2.7 in c:\users\pc\anaconda3\lib\site-packages (from matplotlib<3.11,>=3.4->basemap) (2.9.0.post0)
Requirement already satisfied: certifi in c:\users\pc\anaconda3\lib\site-packages (from pyproj<3.8,>=3.0->basemap) (2025.4.26)
Requirement already satisfied: six>=1.5 in c:\users\pc\anaconda3\lib\site-packages (from python-dateutil>=2.7->matplotlib<3.11,>=3.4->basemap) (1.17.0)
```

```python
In [31]: # Creating a Basic Map
         from mpl_toolkits.basemap import Basemap
         import matplotlib.pyplot as plt

         plt.figure(figsize=(10,6))

         m = Basemap(projection='merc',
                     llcrnrlat=-60, urcrnrlat=80,
                     llcrnrlon=-180, urcrnrlon=180,
                     resolution='c')
         m.drawcoastlines()
         m.drawcountries()
         m.fillcontinents(color='lightgray', lake_color='lightblue')
         m.drawmapboundary(fill_color='lightblue')

         plt.title("World Map using Basemap")
         plt.show()
```
![A world map created using Basemap, with continents in light gray and oceans in light blue.](basemap_world_map.png)

```python
In [32]: # Import necessary libraries
         from mpl_toolkits.basemap import Basemap
         import matplotlib.pyplot as plt
         # ------------------------------------
         # Create a figure
         # ------------------------------------
         plt.figure(figsize=(12,6)) # width=12 inches, height=6 inches
         # ------------------------------------
         # Define the map projection and boundaries
         # ------------------------------------
         m = Basemap(
             projection='merc',      # Mercator projection
             llcrnrlat=-20,          # Lower-left latitude
             urcrnrlat=60,           # upper-right latitude
             llcrnrlon=-20,          # Lower-left longitude
             urcrnrlon=60,           # upper-right longitude
             resolution='i'          # intermediate resolution for coastlines
         )
         # ------------------------------------
         # Draw basic map features
         # ------------------------------------
         m.drawcoastlines()              # draw coastlines
         m.drawcountries()               # draw country borders
         m.fillcontinents(
             color='lightgray',           # color for continents
             lake_color='lightblue'      # color for Lakes
         )
         m.drawmapboundary(fill_color='lightblue') # fill ocean/background
         # ------------------------------------
         # Define cities with their coordinates (Longitude, Latitude)
         # ------------------------------------
         cities = {
             'Alger': (3.0588, 36.7538),  # Algiers
             'Paris': (2.3522, 48.8566),  # Paris
             'Riyadh': (46.6753, 24.7136) # Riyadh
         }
         # ------------------------------------
         # Plot cities on the map
         # ------------------------------------
         for city, (lon, lat) in cities.items():
             # Convert Lat/Lon to map projection coordinates
             x, y = m(lon, lat)
             
             # Plot the city as a red circle
             m.scatter(x, y, marker='o', color='red', s=100, zorder=5)

             # Add the city name near the point
             plt.text(
                 x + 0.5e5, # shift text slightly right
                 y + 0.5e5, # shift text slightly up
                 city,
                 fontsize=12,
                 fontweight='bold',
                 color='blue'
             )
         # ------------------------------------
         # Add a title
         # ------------------------------------
         plt.title("Map: Algiers, Paris, and Riyadh", fontsize=16)
         # ------------------------------------
         # Display the map
         # ------------------------------------
         plt.show()
```
![A map showing parts of Europe, Africa, and the Middle East, with red markers and blue labels for the cities of Paris, Algiers, and Riyadh.](map_algiers_paris_riyadh.png)