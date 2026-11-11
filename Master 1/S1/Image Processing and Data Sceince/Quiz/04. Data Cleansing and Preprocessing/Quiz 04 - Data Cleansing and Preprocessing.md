---
sources:
  - "[[04.1. Missing Data Mechanisms and Statistical Imputation]]"
  - "[[04.2. Statistical Outlier Detection and Consistency Rectification]]"
  - "[[04.3. Categorical Feature Encoding and Text Normalization]]"
  - "[[04.4. Feature Scaling, Standardization, and Normalization Theory]]"
  - "[[04.5. Tutorial 05 - End-to-End Medical Cohort Preprocessing Pipeline]]"
  - "[[04.6. Tutorial 05 - Titanic Predictive Modeling Pipeline and Classifier Evaluation]]"
---
> [!question] A survey form dropped in the rain produces missing data that follows the Missing Completely at Random (MCAR) mechanism.
>> [!success]- Answer
>> True

> [!question] When high earners refuse to report their salary, the missingness follows the Missing at Random (MAR) mechanism because it depends only on observed features.
>> [!success]- Answer
>> False

> [!question] Row deletion is a safe strategy for handling missing values under MAR or MNAR as long as the percentage of missing values is small.
>> [!success]- Answer
>> False

> [!question] The Z-score outlier detection method makes no assumptions about the underlying distribution, so it works equally well on heavily skewed data.
>> [!success]- Answer
>> False

> [!question] In the Titanic predictive pipeline, missing age values were filled with the mean age.
>> [!success]- Answer
>> False

> [!question] Applying one-hot encoding to a naturally ordered feature such as education level discards the rank information between its categories.
>> [!success]- Answer
>> True

> [!question] Min-max normalization is highly robust to outliers because it rescales features using the mean and the standard deviation.
>> [!success]- Answer
>> False

> [!question] Computing the scaling parameters on the full dataset before splitting it into train and test sets is a safe practice that does not cause data leakage.
>> [!success]- Answer
>> False

> [!question] In the medical cohort preprocessing pipeline, text standardization of the categorical columns was completed before mode imputation filled their missing values.
>> [!success]- Answer
>> True

> [!question] In the medical cohort preprocessing pipeline, feature standardization was the final step, applied after the categorical columns had been one-hot encoded.
>> [!success]- Answer
>> True

> [!question] Missing depression reports depend on the observed gender feature but not on the missing value itself, which is the Missing at Random (MAR) mechanism. Which handling approach does the theory recommend for MAR data?
> a) Row deletion, because the missingness is completely random
> b) Multi-variable imputation such as KNN imputation
> c) Domain-specific modeling of the missingness process
> d) Mean imputation of the depression column
>> [!success]- Answer
>> b) Multi-variable imputation such as KNN imputation

> [!question] A continuous clinical feature is strongly right-skewed and contains extreme outliers. Which univariate imputation strategy is most appropriate for its missing values?
> a) Mean imputation
> b) Mode imputation
> c) Row deletion of all records with a missing value
> d) Median imputation
>> [!success]- Answer
>> d) Median imputation

> [!question] Which formula corresponds to min-max normalization?
> a) $x' = \frac{x - x_{min}}{x_{max} - x_{min}}$
> b) $x' = \frac{x - \mu}{\sigma}$
> c) $x' = \frac{x - \text{median}}{\text{IQR}}$
> d) $x' = \frac{x}{\sqrt{\sum x_i^2}}$
>> [!success]- Answer
>> a) $x' = \frac{x - x_{min}}{x_{max} - x_{min}}$

> [!question] According to the Z-score method, when is a data point typically flagged as an outlier?
> a) When its Z-score falls between -3 and +3
> b) When its absolute Z-score exceeds 1.5
> c) When its absolute Z-score exceeds 3
> d) When its Z-score equals exactly 0
>> [!success]- Answer
>> c) When its absolute Z-score exceeds 3

> [!question] A numeric feature is heavily skewed and does not follow a normal distribution. Which outlier detection method is more appropriate for it?
> a) The IQR method, because it is non-parametric and makes no distributional assumptions
> b) The Z-score method, because it works on any distribution
> c) The Z-score method, because it is robust to extreme values
> d) The IQR method, because it assumes the data is Gaussian
>> [!success]- Answer
>> a) The IQR method, because it is non-parametric and makes no distributional assumptions

> [!question] In `pd.get_dummies()`, which problem does setting `drop_first=True` prevent?
> a) The loss of ordinal rank information between categories
> b) Perfect multicollinearity between indicator columns, known as the dummy variable trap
> c) The overrepresentation of majority classes
> d) The underestimation of feature variance
>> [!success]- Answer
>> b) Perfect multicollinearity between indicator columns, known as the dummy variable trap

> [!question] In the Titanic pipeline, what happened to the `adult_male` and `alone` columns during the categorical encoding step?
> a) They were one-hot encoded with `drop_first=True`
> b) They were dropped as redundant columns
> c) They were cast to integer type with `astype(int)`
> d) They were filled with the most frequent value
>> [!success]- Answer
>> c) They were cast to integer type with `astype(int)`

> [!question] Why do distance-based algorithms such as KNN and SVM require feature scaling before training?
> a) Without scaling, features with large numeric ranges dominate the distance computations
> b) Scaling automatically removes outliers from the feature space
> c) Scaling converts categorical labels into numeric codes
> d) Scaling forces every feature to follow a normal distribution
>> [!success]- Answer
>> a) Without scaling, features with large numeric ranges dominate the distance computations

> [!question] In the end-to-end medical cohort preprocessing pipeline, which stage was executed immediately after the numerical columns were imputed with their medians?
> a) One-hot encoding of the Gender and Diagnosis columns
> b) Standardization of the numeric columns with StandardScaler
> c) Mode imputation of the categorical columns
> d) Outlier capping at the IQR fences
>> [!success]- Answer
>> d) Outlier capping at the IQR fences

> [!question] Which evaluation tools were used to assess the Titanic classifiers after prediction?
> a) Mean squared error and R-squared
> b) Accuracy score, classification report, and confusion matrix
> c) ROC AUC and log loss
> d) Mean absolute error and residual plots
>> [!success]- Answer
>> b) Accuracy score, classification report, and confusion matrix

> [!question] Match each missing data mechanism with its definition.
>> [!example] Group A
>> a) Missing Completely at Random (MCAR)
>> b) Missing at Random (MAR)
>> c) Missing Not at Random (MNAR)
>
>> [!example] Group B
>> n) The probability of an observation being missing depends directly on the unobserved value itself.
>> o) The probability of an observation being missing is independent of both observed and unobserved features.
>> p) The probability of an observation being missing depends on observed features but not on the unobserved missing value itself.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each imputation strategy with its advantages and disadvantages.
>> [!example] Group A
>> a) Row deletion
>> b) Mean imputation
>> c) Median imputation
>> d) Mode imputation
>> e) KNN imputation
>
>> [!example] Group B
>> n) Simple to compute and maintains sample size, but underestimates variance and distorts correlations.
>> o) Applies to non-numeric features, but overrepresents the majority classes.
>> p) Simple and keeps the untouched values exactly as they were, but discards records that still hold valid values in other columns.
>> q) Preserves relationships across variables, but runs at $O(n^2)$ cost and is sensitive to feature scale.
>> r) Not swayed by extreme values, but distorts covariance and correlation structures.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> r)
>> d) -> o)
>> e) -> q)

> [!question] Match each outlier handling technique with the situation where it fits best.
>> [!example] Group A
>> a) Trimming
>> b) Winsorization
>> c) Log transformation
>
>> [!example] Group B
>> n) The extreme values should be pulled back to the boundary limits while keeping every row.
>> o) The distribution is right-skewed and the extremes exert too much leverage.
>> p) The flagged values are unambiguous data entry errors, so the whole records can be removed.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match each outlier detection quantity with its formula.
>> [!example] Group A
>> a) Z-score
>> b) Interquartile range
>> c) Lower fence
>> d) Upper fence
>
>> [!example] Group B
>> n) The spread $Q_3 - Q_1$ covered by the middle half of the data.
>> o) The limit $Q_1 - 1.5 \times (Q_3 - Q_1)$, below which values are flagged as outliers.
>> p) The quantity $z = \frac{x - \mu}{\sigma}$, which measures distance from the mean in standard deviations.
>> q) The limit $Q_3 + 1.5 \times (Q_3 - Q_1)$, above which values are flagged as outliers.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match each categorical encoding scheme or concept with its description.
>> [!example] Group A
>> a) One-hot encoding
>> b) Ordinal encoding
>> c) Frequency encoding
>> d) Dummy variable trap
>
>> [!example] Group B
>> n) Creates a binary indicator column for each category of a nominal, unordered feature.
>> o) The perfect multicollinearity that appears when every category receives its own indicator column.
>> p) Replaces each category with its overall proportion in the dataset to avoid high-dimensional feature expansion.
>> q) Maps ordered categories to integer codes that preserve their natural rank.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> p)
>> d) -> o)

> [!question] Match each text normalization operation with its purpose.
>> [!example] Group A
>> a) Lowercasing
>> b) Whitespace stripping
>> c) Null token replacement
>
>> [!example] Group B
>> n) Removes leading and trailing spaces that would otherwise split identical labels apart.
>> o) Merges inconsistent labels such as MALE, Male, and male into a single category.
>> p) Converts placeholder strings like "none" into true missing values.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match each feature scaling transformation with its core characteristics.
>> [!example] Group A
>> a) Standardization
>> b) Min-max normalization
>> c) Robust scaling
>> d) L2 vector normalization
>
>> [!example] Group B
>> n) Rescales each feature to the fixed interval $[0, 1]$ and is sensitive to outliers.
>> o) Rescales each row so that its Euclidean length equals 1.
>> p) Centers each feature at the median and divides by the interquartile range, handling extreme anomalies well.
>> q) Rescales each feature to $\mu = 0$ and $\sigma = 1$ and leaves the values unbounded.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> p)
>> d) -> o)

> [!question] Match each stage of the medical cohort preprocessing pipeline with what it did.
>> [!example] Group A
>> a) Text standardization
>> b) Mode imputation
>> c) Median imputation
>> d) IQR outlier capping
>> e) One-hot encoding
>> f) Feature standardization
>
>> [!example] Group B
>> n) Filled missing Gender and Diagnosis entries with each column's most frequent value.
>> o) Expanded the categorical columns into binary indicator columns, dropping the first category.
>> p) Made the raw Gender and Diagnosis strings uniform by removing casing and whitespace inconsistencies.
>> q) Rescaled the numeric columns so they had mean 0 and standard deviation 1.
>> r) Clipped extreme values in the numeric columns to the quartile-based boundary limits.
>> s) Filled missing Age, BloodPressure, and Cholesterol entries with each column's middle value.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> s)
>> d) -> r)
>> e) -> o)
>> f) -> q)

> [!question] Match each Titanic pipeline column with its role or fate.
>> [!example] Group A
>> a) FamilySize
>> b) IsAlone
>> c) deck
>> d) alive
>
>> [!example] Group B
>> n) Dropped because of its high proportion of missing values.
>> o) Engineered feature computed as the sum of the siblings/spouses and parents/children columns plus one.
>> p) Dropped because it was an alias duplicating the survival target.
>> q) Engineered binary feature that flags passengers traveling without any relatives on board.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match each Titanic modeling step with its effect on the data.
>> [!example] Group A
>> a) `SimpleImputer(strategy='median')`
>> b) `pd.get_dummies(drop_first=True)`
>> c) `stratify=y`
>> d) `scaler.transform(X_test)`
>
>> [!example] Group B
>> n) Applied the parameters learned from the training partition to the held-out rows without refitting.
>> o) Partitioned the data so that the target's class balance stayed the same in both partitions.
>> p) Filled the missing age values with the middle value of the observed ages.
>> q) Expanded the sex and embarked columns into binary indicator columns while avoiding perfect multicollinearity.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)
