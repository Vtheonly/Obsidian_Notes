---
sources:
  - "[[5.1. Handling Missing Data]]"
  - "[[5.2. Data Consistency and Outlier Treatment]]"
  - "[[5.3. Text Cleaning and Categorical Encoding]]"
  - "[[5.4. Feature Scaling and Normalization]]"
  - "[[5.5. Tutorial 5. Medical Dataset Preprocessing Walkthrough]]"
  - "[[5.6. Tutorial 5 Project. Titanic Data Pipeline and Modeling]]"
---

> [!question] Feature scaling is unnecessary for tree-based models.
>> [!success]- Answer
>> True

> [!question] Imputation always improves model accuracy.
>> [!success]- Answer
>> False

> [!question] Outliers can be detected using IQR (Interquartile Range).
>> [!success]- Answer
>> True

> [!question] Ordinal encoding preserves the order of categories.
>> [!success]- Answer
>> True

> [!question] Regex can be used to clean text data.
>> [!success]- Answer
>> True

> [!question] Standardization centers data around zero with unit variance.
>> [!success]- Answer
>> True

> [!question] Categorical variables with high cardinality can cause dimensionality issues.
>> [!success]- Answer
>> True

> [!question] Data leakage occurs when information from the test set influences training.
>> [!success]- Answer
>> True

> [!question] Stemming reduces words to their root form.
>> [!success]- Answer
>> True

> [!question] Missing Completely at Random (MCAR) means missingness depends on other variables.
>> [!success]- Answer
>> False

> [!question] Which method is robust to outliers for scaling?
> a) StandardScaler
> b) RobustScaler
> c) MinMaxScaler
> d) Normalizer
>> [!success]- Answer
>> b)

> [!question] What does tokenization do in text preprocessing?
> a) Removes punctuation
> b) Splits text into tokens
> c) Converts to lowercase
> d) Stems words
>> [!success]- Answer
>> b)

> [!question] Which technique handles high cardinality categorical features?
> a) One-hot encoding
> b) Target encoding
> c) Label encoding
> d) Ordinal encoding
>> [!success]- Answer
>> b)

> [!question] What is the purpose of data validation?
> a) Ensure data quality and consistency
> b) Scale features
> c) Train models
> d) Visualize data
>> [!success]- Answer
>> a)

> [!question] Which is a univariate outlier detection method?
> a) Isolation Forest
> b) Z-score method
> c) LOF
> d) DBSCAN
>> [!success]- Answer
>> b)

> [!question] What does lemmatization do?
> a) Removes suffixes to get root word
> b) Converts words to their dictionary form
> c) Removes stop words
> d) Tokenizes text
>> [!success]- Answer
>> b)

> [!question] Pandas function to check for duplicates?
> a) df.duplicated()
> b) df.repeated()
> c) df.double()
> d) df.unique()
>> [!success]- Answer
>> a)

> [!question] What is the difference between fit and transform?
> a) No difference
> b) fit learns parameters, transform applies them
> c) transform learns, fit applies
> d) Both do the same
>> [!success]- Answer
>> b)

> [!question] What does RobustScaler use for scaling?
> a) Mean and std
> b) Median and IQR
> c) Min and max
> d) Mode and range
>> [!success]- Answer
>> b)

> [!question] Which encoding is suitable for ordinal data?
> a) One-hot encoding
> b) Ordinal encoding
> c) Binary encoding
> d) Hash encoding
>> [!success]- Answer
>> b)

> [!question] Match the items.
>> [!example] Group A
>> a) Stemming
>> b) Lemmatization
>> c) Tokenization
>
>> [!example] Group B
>> n) Reduces to dictionary base word
>> o) Splits text into units
>> p) Reduces to root by chopping suffixes
>
>> [!success]- Answer
>> a) -> c)
>> b) -> a)
>> c) -> b)

> [!question] Match the items.
>> [!example] Group A
>> a) dropna()
>> b) fillna()
>> c) interpolate()
>
>> [!example] Group B
>> n) Estimates and fills missing values
>> o) Removes rows with NaN
>> p) Fills NaN with specified value
>
>> [!success]- Answer
>> a) -> b)
>> b) -> c)
>> c) -> a)

> [!question] Match the items.
>> [!example] Group A
>> a) fit()
>> b) transform()
>> c) fit_transform()
>
>> [!example] Group B
>> n) Applies learned parameters to data
>> o) Learns parameters from data
>> p) Both learns and applies in one step
>
>> [!success]- Answer
>> a) -> b)
>> b) -> a)
>> c) -> c)

> [!question] Match the items.
>> [!example] Group A
>> a) Upper case
>> b) Lower case
>> c) Sentence case
>
>> [!example] Group B
>> n) Standard for text normalization
>> o) Used for proper nouns
>> p) Used for emphasis
>
>> [!success]- Answer
>> a) -> b)
>> b) -> a)
>> c) -> c)

> [!question] Match the items.
>> [!example] Group A
>> a) Regex
>> b) Stop word removal
>> c) Punctuation removal
>
>> [!example] Group B
>> n) Removes common unimportant words
>> o) Uses patterns to find and replace text
>> p) Removes characters like . , ! ?
>
>> [!success]- Answer
>> a) -> b)
>> b) -> a)
>> c) -> c)
