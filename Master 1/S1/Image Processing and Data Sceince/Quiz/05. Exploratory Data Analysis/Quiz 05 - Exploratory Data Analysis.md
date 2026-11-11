---
sources:
  - "[[05.1. Exploratory Data Analysis Principles, Distributions, and Correlation Metrics]]"
---
> [!question] In a positively skewed distribution, the mean is typically greater than the median.
>> [!success]- Answer
>> True

> [!question] Spearman rank correlation measures the strength of linear relationships just like Pearson, but is more robust to outliers.
>> [!success]- Answer
>> False

> [!question] A leptokurtic distribution has a flatter peak and thinner tails than a normal distribution.
>> [!success]- Answer
>> False

> [!question] A contingency table is a bivariate analysis tool for examining relationships between two categorical variables.
>> [!success]- Answer
>> True

> [!question] Pearson correlation assumes the variables are normally distributed and linearly related, making it sensitive to outliers.
>> [!success]- Answer
>> True

> [!question] Which analysis level examines interactions across three or more variables simultaneously using pairplots and correlation heatmaps?
> a) Univariate analysis
> b) Bivariate analysis
> c) Multivariate analysis
> d) Meta-analytic review
>> [!success]- Answer
>> c) Multivariate analysis

> [!question] Which measure of distribution shape indicates the frequency of extreme values such as outliers?
> a) Skewness
> b) Kurtosis
> c) Variance
> d) Median absolute deviation
>> [!success]- Answer
>> b) Kurtosis

> [!question] A distribution with skewness near 0 and kurtosis near 0 is best described how?
> a) Right-tailed and leptokurtic
> b) Left-tailed and platykurtic
> c) Bimodal and heavy-tailed
> d) Symmetric and mesokurtic
>> [!success]- Answer
>> d) Symmetric and mesokurtic

> [!question] Which correlation coefficient is best suited for a small dataset with many tied ranks?
> a) Pearson correlation
> b) Spearman rank correlation
> c) Kendall's tau
> d) Cosine similarity
>> [!success]- Answer
>> c) Kendall's tau

> [!question] A right-skewed numeric feature can often be made more symmetric using which transformation?
> a) Exponential expansion
> b) Logarithmic compression
> c) Squaring
> d) Mean-centering
>> [!success]- Answer
>> b) Logarithmic compression

> [!question] Match each level of exploratory analysis with its purpose and typical tools.
>> [!example] Group A
>> a) Univariate analysis
>> b) Bivariate analysis
>> c) Multivariate analysis
>
>> [!example] Group B
>> n) Examines interactions across three or more variables using pairplots, correlation heatmaps, and dimensional facets.
>> o) Examines individual variables in isolation using histograms, KDE plots, and box plots.
>> p) Examines relationships between two features using scatter plots, grouped aggregations, and contingency tables.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each skewness situation with its defining property.
>> [!example] Group A
>> a) Positive skew
>> b) Negative skew
>> c) Symmetric distribution
>
>> [!example] Group B
>> n) Skewness value approximately equal to zero.
>> o) Right tail is longer and the mean is typically greater than the median.
>> p) Left tail is longer and the mean is typically less than the median.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each kurtosis class with its distribution shape.
>> [!example] Group A
>> a) Leptokurtic
>> b) Platykurtic
>> c) Mesokurtic
>
>> [!example] Group B
>> n) Flatter peak with thinner tails and fewer extreme outliers.
>> o) Sharp peak with heavy tails indicating a higher frequency of outliers.
>> p) Tailedness matching a normal distribution.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match each correlation coefficient with its defining characteristic.
>> [!example] Group A
>> a) Pearson correlation
>> b) Spearman rank correlation
>> c) Kendall's tau
>
>> [!example] Group B
>> n) Rank-based measure counting concordant versus discordant pairs, well suited to small datasets.
>> o) Measures the linear relationship between continuous variables and is sensitive to outliers.
>> p) Non-parametric measure of the monotonic relationship, robust to non-linearities and outliers.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each exploratory analysis tool or remedy with its role.
>> [!example] Group A
>> a) Exploratory Data Analysis
>> b) Count plot
>> c) Grouped aggregation
>> d) Square-root transformation
>
>> [!example] Group B
>> n) One of the standard remedies for reducing positive skew.
>> o) Investigates patterns, tests hypotheses, and checks statistical assumptions before formal modeling.
>> p) Bivariate technique that summarizes a numeric field for each category.
>> q) Univariate visualization for categorical features.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)
