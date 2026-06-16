---
sources:
  - "[[5.1. Handling Missing Data]]"
  - "[[5.2. Data Consistency and Outlier Treatment]]"
  - "[[5.3. Text Cleaning and Categorical Encoding]]"
  - "[[5.4. Feature Scaling and Normalization]]"
  - "[[5.5. Tutorial 5. Medical Dataset Preprocessing Walkthrough]]"
  - "[[5.6. Tutorial 5 Project. Titanic Data Pipeline and Modeling]]"
---

> [!question] Missing data can be handled by removing rows with null values.
>> [!success]- Answer
>> True

> [!question] Mean imputation replaces missing values with the median.
>> [!success]- Answer
>> False

> [!question] One-hot encoding creates binary columns for categorical variables.
>> [!success]- Answer
>> True

> [!question] Standardization assumes data follows a normal distribution.
>> [!success]- Answer
>> False

> [!question] Outliers can negatively impact model performance.
>> [!success]- Answer
>> True

> [!question] Label encoding assigns ordinal values to categories.
>> [!success]- Answer
>> True

> [!question] Min-max scaling transforms data to a fixed range, typically [0,1].
>> [!success]- Answer
>> True

> [!question] Duplicate rows should always be removed from a dataset.
>> [!success]- Answer
>> False

> [!question] Z-score measures how many standard deviations a point is from the mean.
>> [!success]- Answer
>> True

> [!question] Text cleaning involves removing stop words and punctuation.
>> [!success]- Answer
>> True

> [!question] Which technique is used to handle missing categorical data?
> a) Mean imputation
> b) Mode imputation
> c) Standardization
> d) Scaling
>> [!success]- Answer
>> b)

> [!question] What is the IQR used for?
> a) Feature scaling
> b) Outlier detection
> c) Encoding categories
> d) Text cleaning
>> [!success]- Answer
>> b)

> [!question] Which encoding creates binary columns?
> a) Label encoding
> b) One-hot encoding
> c) Ordinal encoding
> d) Frequency encoding
>> [!success]- Answer
>> b)

> [!question] What does StandardScaler do?
> a) Scales to [0,1] range
> b) Centers to mean=0, std=1
> c) Log transforms data
> d) Removes outliers
>> [!success]- Answer
>> b)

> [!question] How to detect outliers using Z-score?
> a) Points with |z| > 3
> b) Points with z = 0
> c) Points with z < 0
> d) Points with any z-score
>> [!success]- Answer
>> a)

> [!question] What is data imputation?
> a) Removing missing data
> b) Replacing missing data with estimated values
> c) Scaling features
> d) Encoding categories
>> [!success]- Answer
>> b)

> [!question] MinMaxScaler transforms features to which range?
> a) [-1, 1]
> b) [0, 1]
> c) [0, 100]
> d) No fixed range
>> [!success]- Answer
>> b)

> [!question] What is label encoding?
> a) Creating binary columns
> b) Assigning integers to categories
> c) Scaling numerical features
> d) Removing duplicates
>> [!success]- Answer
>> b)

> [!question] Which of the following is NOT a type of missing data?
> a) MCAR
> b) MAR
> c) MNAR
> d) MCR
>> [!success]- Answer
>> d)

> [!question] What is the purpose of feature scaling?
> a) Remove outliers
> b) Bring features to similar scale
> c) Reduce dimensionality
> d) Handle missing values
>> [!success]- Answer
>> b)

> [!question] Match the items.
>> [!example] Group A
>> a) Mean Imputation
>> b) Median Imputation
>> c) Mode Imputation
>
>> [!example] Group B
>> n) Used for categorical data
>> o) Used for numerical data with outliers
>> p) Used for numerical data without outliers
>
>> [!success]- Answer
>> a) -> c)
>> b) -> b)
>> c) -> a)

> [!question] Match the items.
>> [!example] Group A
>> a) Z-score
>> b) IQR Method
>> c) Isolation Forest
>
>> [!example] Group B
>> n) Detects outliers using quartiles
>> o) Machine learning outlier detection
>> p) Detects outliers using standard deviations
>
>> [!success]- Answer
>> a) -> c)
>> b) -> a)
>> c) -> b)

> [!question] Match the items.
>> [!example] Group A
>> a) One-hot Encoding
>> b) Label Encoding
>> c) Target Encoding
>
>> [!example] Group B
>> n) Assigns integers to categories
>> o) Creates binary columns per category
>> p) Replaces category with mean target value
>
>> [!success]- Answer
>> a) -> b)
>> b) -> a)
>> c) -> c)

> [!question] Match the items.
>> [!example] Group A
>> a) StandardScaler
>> b) MinMaxScaler
>> c) RobustScaler
>
>> [!example] Group B
>> n) Scales using median and IQR
>> o) Scales to fixed range [0,1]
>> p) Centers to mean=0, std=1
>
>> [!success]- Answer
>> a) -> c)
>> b) -> a)
>> c) -> b)

> [!question] Match the items.
>> [!example] Group A
>> a) MCAR
>> b) MAR
>> c) MNAR
>
>> [!example] Group B
>> n) Missing depends on other observed data
>> o) Missing not at random (systematic)
>> p) Missing completely at random
>
>> [!success]- Answer
>> a) -> c)
>> b) -> a)
>> c) -> b)
