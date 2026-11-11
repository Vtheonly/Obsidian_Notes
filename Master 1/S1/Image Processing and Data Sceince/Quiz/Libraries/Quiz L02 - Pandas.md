---
sources:
  - "[[06. Pandas Structural Primitives - Series and DataFrame Architecture]]"
  - "[[07. Pandas Data Ingestion, Inspection, and Type Coercion]]"
  - "[[08. Pandas Indexing, Slicing, and Query Mechanics (loc, iloc, query, at)]]"
  - "[[09. Pandas Data Cleansing - Handling Nulls, Deduplication, and String Normalization]]"
  - "[[11. Pandas Grouping, Split-Apply-Combine, and Statistical Aggregations]]"
  - "[[12. Pandas Relational Operations - Joins, Merging, and Concatenation]]"
  - "[[13. Pandas Data Reshaping - Pivoting, Unpivoting, Stacking, and Melting]]"
  - "[[14. Pandas Temporal Mechanics - Time Series and Datetime Calculations]]"
---
> [!question] A `pd.Series` can be created with custom labels for its rows by passing the `index` argument, e.g. `pd.Series([25, 28, 22], index=["Amel", "Sami", "Rania"])`.
>> [!success]- Answer
>> True

> [!question] Internally, the `BlockManager` stores a whole `pd.DataFrame` inside a single 2D NumPy array, even when columns have different data types.
>> [!success]- Answer
>> False

> [!question] When exporting with `df.to_csv("cleaned_data.csv", index=False)`, the row index is not persisted to the output file.
>> [!success]- Answer
>> True

> [!question] `pd.to_numeric(series, errors="coerce")` converts a string series into numbers and safely replaces invalid values with `NaN`.
>> [!success]- Answer
>> True

> [!question] With `.loc[]`, a slice such as `df.loc["row_a":"row_c"]` excludes the stop label `"row_c"` from the returned rows.
>> [!success]- Answer
>> False

> [!question] Unlike boolean filtering, which drops non-matching rows, `.where()` preserves the DataFrame's original dimensions and replaces values in non-matching rows with `NaN`.
>> [!success]- Answer
>> True

> [!question] `df.duplicated()` returns a new DataFrame containing only the duplicated rows.
>> [!success]- Answer
>> False

> [!question] The vectorized `.str` accessor transforms an entire text column, e.g. with `.str.upper()` or `.str.strip()`, without writing manual loops.
>> [!success]- Answer
>> True

> [!question] `df.groupby("Department")["Salary"].transform("mean")` returns a single summary row per department, reducing the DataFrame's dimensions.
>> [!success]- Answer
>> False

> [!question] In `pd.concat()`, setting `axis=1` stacks the rows of the input DataFrames on top of each other.
>> [!success]- Answer
>> False

> [!question] What does `df.reset_index(drop=False)` do?
> a) Permanently deletes the old row labels without preserving them
> b) Converts the index labels into an explicit column and assigns a default integer index
> c) Replaces all column names with sequential integers
> d) Sorts the rows alphabetically by their index labels
>> [!success]- Answer
>> b) Converts the index labels into an explicit column and assigns a default integer index

> [!question] Which `pd.read_csv()` parameters load only the `PatientID` and `Age` columns and set `PatientID` as the row index during ingestion?
> a) `columns=` and `index_key=`
> b) `subset=` and `key=`
> c) `usecols=` and `index_col=`
> d) `take=` and `row_index=`
>> [!success]- Answer
>> c) `usecols=` and `index_col=`

> [!question] When filtering DataFrame rows with multiple conditions, which operators must be used to combine the conditions, with each individual condition enclosed in parentheses?
> a) `and`, `or`, `not`
> b) `&`, `|`, `~`
> c) `&&`, `||`, `!`
> d) `+`, `*`, `-`
>> [!success]- Answer
>> b) `&`, `|`, `~`

> [!question] Which call removes duplicate patient records based on the `PatientID` key while keeping the last occurrence of each patient?
> a) `df.drop_duplicates(subset=["PatientID"], keep="last")`
> b) `df.drop_duplicates(subset=["PatientID"], keep="first")`
> c) `df.duplicated(subset=["PatientID"], keep="last")`
> d) `df.dropna(subset=["PatientID"])`
>> [!success]- Answer
>> a) `df.drop_duplicates(subset=["PatientID"], keep="last")`

> [!question] What does `pd.get_dummies(df, columns=["Gender"], drop_first=False)` add to the DataFrame?
> a) A single column of integer class codes replacing the Gender column
> b) A long-format table with one row per patient and gender
> c) A normalized text column with whitespace stripped from each entry
> d) Binary indicator columns such as `Gender_F` and `Gender_M` holding 0/1 values
>> [!success]- Answer
>> d) Binary indicator columns such as `Gender_F` and `Gender_M` holding 0/1 values

> [!question] What does the `.agg()` method enable in grouped operations?
> a) It broadcasts group statistics back across the original rows
> b) It computes different statistical metrics across multiple columns in a single operation
> c) It sorts the groups by their aggregated values
> d) It stacks the group results on top of each other with `pd.concat()`
>> [!success]- Answer
>> b) It computes different statistical metrics across multiple columns in a single operation

> [!question] In `pd.merge(patients, departments, on="City", how="left")`, what does the `on` parameter specify?
> a) The common key column whose matching values link the two DataFrames
> b) The column by which the merged output is sorted
> c) The name of a new column to create in the result
> d) The axis along which the two tables are concatenated
>> [!success]- Answer
>> a) The common key column whose matching values link the two DataFrames

> [!question] In a `df.melt()` call, what does the `id_vars` parameter specify?
> a) The measurement columns to unpivot into the new value column
> b) The new column name for the measurement labels
> c) The identifier columns that are kept fixed while other columns are unpivoted
> d) The new column name for the measured values
>> [!success]- Answer
>> c) The identifier columns that are kept fixed while other columns are unpivoted

> [!question] Which expression computes a 3-month moving average of the `Sales` column?
> a) `df["Sales"].rolling(window=3).mean()`
> b) `df["Sales"].resample("Q").mean()`
> c) `df["Sales"].shift(3).mean()`
> d) `df["Sales"].rolling(window=3).sum()`
>> [!success]- Answer
>> a) `df["Sales"].rolling(window=3).mean()`

> [!question] What does `pd.to_datetime()` do with a list of date strings such as `["2026-01-01", "2026-02-01"]`?
> a) It formats the entries back into locale-specific strings
> b) It generates a continuous monthly sequence of periods
> c) It rounds each timestamp to the start of its month
> d) It converts the string representations into `datetime64[ns]` objects
>> [!success]- Answer
>> d) It converts the string representations into `datetime64[ns]` objects

> [!question] Match the DataFrame inspection call with what it reports.
>> [!example] Group A
>> a) `df.shape`
>> b) `df.info()`
>> c) `df.dtypes`
>> d) `df.describe()`
>> e) `df.isnull().sum()`
>
>> [!example] Group B
>> n) Provides a structural and memory audit of the dataset.
>> o) Returns the dimensions as a (rows, columns) tuple.
>> p) Reports the data type of every column.
>> q) Counts the missing entries in each column.
>> r) Computes descriptive statistics for the numerical features.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> r)
>> e) -> q)

> [!question] Match the Pandas selection tool with its behavior.
>> [!example] Group A
>> a) `.loc[]`
>> b) `.iloc[]`
>> c) `.at[]`
>> d) `.iat[]`
>> e) `.query()`
>
>> [!example] Group B
>> n) Retrieves a single scalar quickly via an exact row label and column label.
>> o) Selects rows and columns using their label strings.
>> p) Filters rows using a readable, string-based expression.
>> q) The fastest scalar retrieval, using exact integer coordinates.
>> r) Selects rows and columns using zero-based integer positions.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> r)
>> c) -> n)
>> d) -> q)
>> e) -> p)

> [!question] Match the missing-value mechanism with its behavior.
>> [!example] Group A
>> a) `np.nan`
>> b) `df.dropna()`
>> c) `df.dropna(subset=["Age"])`
>> d) `df["Age"].fillna(df["Age"].median())`
>> e) `df["City"].fillna("Unknown")`
>
>> [!example] Group B
>> n) Discards any row containing at least one null entry.
>> o) The sentinel value representing missing data, with `pd.NA` as an alternative.
>> p) Replaces missing entries with a fixed constant label.
>> q) Imputes missing numeric entries with the column's middle value.
>> r) Discards a row only when the specified column is null.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> r)
>> d) -> q)
>> e) -> p)

> [!question] Match the grouping concept with its role.
>> [!example] Group A
>> a) Split
>> b) Apply
>> c) Combine
>> d) `pd.crosstab()`
>
>> [!example] Group B
>> n) Computes statistics or transformations independently within each group.
>> o) Assembles the per-group results into a single output DataFrame.
>> p) Partitions the rows into groups based on unique values of the key columns.
>> q) Builds the frequency table (contingency matrix) between two categorical columns.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the `pd.merge()` join mode with its row-retention behavior.
>> [!example] Group A
>> a) `how="inner"`
>> b) `how="left"`
>> c) `how="right"`
>> d) `how="outer"`
>
>> [!example] Group B
>> n) Retains only the rows whose keys match in both DataFrames.
>> o) Retains all rows from both DataFrames, filling unmatched values with `NaN`.
>> p) Retains every row of the first DataFrame, filling unmatched values from the second with `NaN`.
>> q) Retains every row of the second DataFrame, filling unmatched values from the first with `NaN`.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> q)
>> d) -> o)

> [!question] Match the reshaping concept with its behavior.
>> [!example] Group A
>> a) `df.pivot()`
>> b) `df.pivot_table()`
>> c) `df.melt()`
>> d) Wide Format
>> e) Long Format
>
>> [!example] Group B
>> n) Data is spread across multiple columns, e.g. one column per year or category.
>> o) Reshapes unique index-column combinations into a wide table and raises `ValueError` on duplicate entries.
>> p) Handles duplicate entries gracefully by aggregating them with a function such as `mean` or `sum`.
>> q) Converts a wide table into a long format by unpivoting measurement columns.
>> r) Data is stacked into key-value pairs (variable, value), making filtering, grouping, and Seaborn visualization easier.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)
>> e) -> r)

> [!question] Match the time-series operation with its behavior.
>> [!example] Group A
>> a) `.dt`
>> b) `resample("Q")`
>> c) `shift(1)`
>> d) `pd.date_range()`
>
>> [!example] Group B
>> n) Generates a continuous monthly sequence of periods from a starting point.
>> o) Provides access to temporal components of a date series, such as year and day.
>> p) Aggregates monthly metrics into quarterly totals.
>> q) Lags each value by one period so the previous month's figure aligns with the current row.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the Pandas structure or attribute with its description.
>> [!example] Group A
>> a) `pd.Series`
>> b) `pd.DataFrame`
>> c) `.values`
>> d) `.index`
>
>> [!example] Group B
>> n) A two-dimensional table with labeled axes for both rows and columns.
>> o) Exposes the underlying NumPy array holding the data.
>> p) Holds the labels that identify each row.
>> q) A one-dimensional labeled array built on a contiguous NumPy array.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the ingestion or export call with its behavior.
>> [!example] Group A
>> a) `pd.read_csv()`
>> b) `to_excel()`
>> c) `to_json()`
>> d) `to_pickle()`
>
>> [!example] Group B
>> n) Serializes the data with a configurable indentation level.
>> o) Ingests delimited text files with a configurable separator and encoding.
>> p) Persists the table in a high-speed binary format.
>> q) Exports to a spreadsheet file and requires the openpyxl library.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the utility call with its effect.
>> [!example] Group A
>> a) `df.select_dtypes(include="number")`
>> b) `df.rename(columns=...)`
>> c) `df.drop(columns=["Bonus"])`
>> d) `pd.concat([df1, df2], ignore_index=True)`
>
>> [!example] Group B
>> n) Assigns new names to existing features, optionally in place.
>> o) Resets the row labels of the stacked result cleanly.
>> p) Keeps only the columns matching a chosen data category, such as numeric ones.
>> q) Deletes unwanted features from the table.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)
