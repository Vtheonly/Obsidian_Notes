---
sources:
  - "[[03.1. Contextual Data Science Computing with NumPy and Pandas]]"
  - "[[03.2. Tutorial 04 - Multi-City Temperature Array Analysis with NumPy]]"
  - "[[03.3. Tutorial 04 - Academic Performance Statistical Analysis with NumPy and Matplotlib]]"
  - "[[03.4. Tutorial 04 - Hospital Department Patient Analytics with Pandas]]"
  - "[[03.5. Tutorial 04 - Longitudinal Sales Forecasting Project]]"
---
> [!question] Pandas DataFrames build upon NumPy arrays, allowing tabular datasets to be processed with vectorized calculations.
>> [!success]- Answer
>> True

> [!question] In a 7 by 3 temperature matrix with days as rows and cities as columns, `T.max(axis=1)` returns the highest temperature recorded in each city over the week.
>> [!success]- Answer
>> False

> [!question] The temperature workflow locates the day and city of the overall peak by converting the flat index from `T.argmax()` with `np.unravel_index(flat_max_index, T.shape)`.
>> [!success]- Answer
>> True

> [!question] In the 7-day, 3-city temperature analysis, Annaba was the hottest city on every single day.
>> [!success]- Answer
>> False

> [!question] In the grades workflow, the Boolean mask covering grades from 10 to 15 inclusive picks out the students whose overall average falls in that range.
>> [!success]- Answer
>> False

> [!question] In the grades workflow, `np.percentile(thl_grades, [25, 50, 75])` computes the 25th, 50th, and 75th percentiles of the THL module's grades.
>> [!success]- Answer
>> True

> [!question] In the hospital cohort indexed 'A' through 'H', `df.loc['C':'F']` returns the records labeled C, D, E, and F, with the end label included.
>> [!success]- Answer
>> True

> [!question] Under the hospital RiskScore formula, a patient with higher satisfaction receives a higher risk score.
>> [!success]- Answer
>> False

> [!question] In the sales project, `pd.date_range(start='2025-01-01', end='2025-12-01', freq='MS')` yields 12 monthly timestamps, one for the first day of each month of 2025.
>> [!success]- Answer
>> True

> [!question] In the sales project, `data/initial.csv` stores the final cleaned dataset with all computed metrics such as Total_Sales and Quarter.
>> [!success]- Answer
>> False

> [!question] How do the Tutorial 04 projects position Pandas relative to NumPy for tabular data work?
> a) Pandas DataFrames are built on top of NumPy arrays, and business logic is mapped into vectorized transformations.
> b) Pandas bypasses NumPy entirely and relies on its own compiled routines for every operation.
> c) NumPy arrays wrap Pandas DataFrames to add labeled columns and a row index.
> d) The two libraries are strictly separated, with NumPy for storage and Pandas for plotting.
>> [!success]- Answer
>> a) Pandas DataFrames are built on top of NumPy arrays, and business logic is mapped into vectorized transformations.

> [!question] Before appending the city averages as an eighth row, the temperature workflow calls `T.mean(axis=0).reshape(1, 3)`. Why reshape to `(1, 3)` before `np.vstack`?
> a) To round each average to at most three decimal places
> b) To transpose the averages onto the day axis
> c) To keep the averages as a single-row 2D array that stacks as one new row
> d) To convert the averages into a column vector aligned with each city
>> [!success]- Answer
>> c) To keep the averages as a single-row 2D array that stacks as one new row

> [!question] In the temperature workflow, what does `np.maximum(T[:, 0], T[:, 2])` compute?
> a) A single scalar holding the hotter city's overall maximum
> b) An element-wise, per-day higher temperature between Alger and Oran
> c) A Boolean array marking the days when Alger exceeded Oran
> d) The average gap between the two cities for each day
>> [!success]- Answer
>> b) An element-wise, per-day higher temperature between Alger and Oran

> [!question] How does the grades workflow rank the top 5 students by overall average?
> a) `np.sort(mean_per_student)[:5]`
> b) `np.argsort(mean_per_student)[:5]`
> c) `grades_of_students.mean(axis=0)[:5]`
> d) `np.argsort(mean_per_student)[::-1][:5]`
>> [!success]- Answer
>> d) `np.argsort(mean_per_student)[::-1][:5]`

> [!question] The grades figure pairs a bar chart with a boxplot. What does the boxplot panel add beyond the bar chart?
> a) It shows each module's full grade distribution, including median, spread, and outliers, rather than one average per module.
> b) It plots every student's overall average as a connected line over the five modules.
> c) It counts how many individual grades fall between 10 and 15.
> d) It replaces the five module columns with their variance and standard deviation.
>> [!success]- Answer
>> a) It shows each module's full grade distribution, including median, spread, and outliers, rather than one average per module.

> [!question] On the module-average bar chart, what does the red dashed horizontal line at 10.0 represent?
> a) The cohort's overall mean grade
> b) The passing threshold of 10 out of 20
> c) The median grade of the THL module
> d) The 25th percentile of all grades
>> [!success]- Answer
>> b) The passing threshold of 10 out of 20

> [!question] After filtering neurology patients and keeping four columns, how is the hospital subset finally indexed and ordered?
> a) Indexed by 'City' and sorted by 'DailyCost' from highest to lowest
> b) Indexed by 'DailyCost' and sorted by 'City' alphabetically
> c) Indexed by the original 'A' to 'H' labels in raw order
> d) Indexed by 'Department' and sorted by 'Age' ascending
>> [!success]- Answer
>> a) Indexed by 'City' and sorted by 'DailyCost' from highest to lowest

> [!question] In the per-city hospital summary, `ReadmissionRate=('Readmitted', 'mean')` is computed from a 0/1 column. What does the resulting value mean?
> a) The total number of readmitted patients in that city
> b) The average days admitted among readmitted patients only
> c) The share of that city's patients flagged as readmitted
> d) The proportion of patients whose satisfaction is below 4.0
>> [!success]- Answer
>> c) The share of that city's patients flagged as readmitted

> [!question] What summary shape does the hospital call `pivot_table(index='City', columns='Department', values=['TotalCost', 'Satisfaction'], aggfunc='mean')` produce?
> a) A single row of cohort-wide means for each metric
> b) One row per patient with city and department appended as columns
> c) One row per department and one column per city of readmission counts
> d) One row per city and one column per department, with mean TotalCost and mean Satisfaction per city-department combination
>> [!success]- Answer
>> d) One row per city and one column per department, with mean TotalCost and mean Satisfaction per city-department combination

> [!question] The sales pipeline computes `df_final['Total_Sales'] = df_final[product_cols].sum(axis=1)`. What does `axis=1` do here?
> a) It sums down each product column across the 12 months
> b) It sums across the four product columns for each month
> c) It sums the Date column together with each product column
> d) It totals the quarterly pivot cells across all quarters
>> [!success]- Answer
>> b) It sums across the four product columns for each month

> [!question] Match each Tutorial 04 exercise with its analytical focus.
>> [!example] Group A
>> a) Multi-city temperature analysis
>> b) Academic performance analysis
>> c) Hospital department analytics
>> d) Longitudinal sales forecasting
>
>> [!example] Group B
>> n) Axis-based array aggregations, peak coordinate lookup, and Boolean masks over a week of daily readings.
>> o) Descriptive statistics, quartiles, and distribution plots for 100 students across five modules.
>> p) DataFrame construction, label-based filtering, risk scoring, and pivot summaries on a clinical cohort.
>> q) Monthly date indexing, quarter mapping, growth metrics, and seasonal visuals for four product lines.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each NumPy element of the multi-city temperature workflow with what it yields.
>> [!example] Group A
>> a) `T.max()`
>> b) `T.max(axis=0)`
>> c) `annaba_hottest_mask`
>> d) `T.shape`
>
>> [!example] Group B
>> n) The single largest reading in the entire matrix, 30 °C.
>> o) One peak per city, taken across all of the days.
>> p) A True/False flag per day, set where the middle city strictly beats both rivals.
>> q) The tuple (7, 3): one row per day of the week, one column per city.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each finding from the 7-day, 3-city temperature analysis with its detail.
>> [!example] Group A
>> a) The week's overall peak
>> b) Alger's highest reading
>> c) Oran's highest reading
>> d) The weekly-average leader
>
>> [!example] Group B
>> n) 30 °C, logged on Day 5 in Annaba.
>> o) 28 °C, posted on Day 4.
>> p) 26 °C, reached on Day 5.
>> q) Annaba, topping both rival cities across the seven days.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
>> d) -> q)

> [!question] Match each call from the grades workflow with its role.
>> [!example] Group A
>> a) `np.random.seed(101)`
>> b) `np.median(grades_of_students, axis=0)`
>> c) `high_achievers`
>> d) `plt.subplots(1, 2, figsize=(14, 5))`
>
>> [!example] Group B
>> n) Makes the synthetic class scores reproducible on every rerun.
>> o) The middle value of each module's scores, robust against extreme outliers.
>> p) Learners with at least fifteen in every one of the five modules.
>> q) Builds the figure with two side-by-side panels for the bar chart and the boxplot.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each metric computed in the grades workflow with what it captures.
>> [!example] Group A
>> a) `mean_per_student`
>> b) `mean_per_module`
>> c) `var_per_module`
>> d) `std_per_module`
>
>> [!example] Group B
>> n) Each learner's overall average across the five subjects.
>> o) The average score of each subject over its 100 learners.
>> p) The average of squared deviations from each subject's mean.
>> q) The spread of scores around each subject's mean, expressed in the original grade units.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each tool with how the hospital workflow uses it.
>> [!example] Group A
>> a) `iloc`
>> b) `apply`
>> c) `fillna`
>> d) `map`
>> e) `np.where`
>
>> [!example] Group B
>> n) Selects patients by integer position, such as positions 1 through 3, rather than by label.
>> o) Runs the age-banding function on each record to tag Young, Middle, or Senior.
>> p) Replaces missing satisfaction entries with the column's average value.
>> q) Looks up each city's regional code, such as DZ-16.
>> r) A vectorized Yes/No flag for total costs above 1200.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match each engineered hospital column with how it is derived.
>> [!example] Group A
>> a) `TotalCost`
>> b) `RiskCategory`
>> c) `SatisfactionLevel`
>> d) `CostRank`
>> e) `Bonus`
>
>> [!example] Group B
>> n) Days admitted multiplied by the daily fee.
>> o) High above 60, Medium from 40 to 60, otherwise Low.
>> p) Excellent at 4.5 or more, Average from 3.5 up to 4.5, Poor below 3.5.
>> q) Each record's position when expenses are ordered from highest to lowest.
>> r) Ten percent of the daily fee, created and then dropped from the frame.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match each step of the sales pipeline with what it does.
>> [!example] Group A
>> a) `pct_change() * 100`
>> b) `dt.strftime("%b")`
>> c) `apply(assign_quarter)`
>> d) `high=max_val + 1`
>> e) `np.random.seed(42)`
>
>> [!example] Group B
>> n) The relative shift of the monthly combined figure versus the prior month, in percent.
>> o) Short month labels such as Jan and Feb for the table and charts.
>> p) Tags each timestamp Q1, Q2, Q3, or Q4 according to its month number.
>> q) Ensures the largest allowed sales value can actually be drawn.
>> r) Locks the generator so the synthetic demand reproduces identically on every run.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match each panel of the four-part sales dashboard with what it displays.
>> [!example] Group A
>> a) Line chart
>> b) Stacked bar chart
>> c) Annotated heatmap
>> d) Boxplot panel
>
>> [!example] Group B
>> n) One connected, marked series per product tracing monthly units across the year.
>> o) Vertical columns where each month's total splits into colored product layers.
>> p) A color-intensity grid of month against product with the unit counts printed inside the cells.
>> q) Per product, a summary of how monthly units spread around the median.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each computation from the sales project with the insight it delivers.
>> [!example] Group A
>> a) `df_final["Total_Sales"].idxmax()`
>> b) `df_final[product_cols].idxmax(axis=1)`
>> c) `df_final[product_cols].sum().idxmax()`
>> d) `df_final.groupby("Quarter")["Total_Sales"].sum().idxmax()`
>> e) `pivot_table(index="Quarter", values=product_cols + ["Total_Sales"], aggfunc="mean")`
>
>> [!example] Group B
>> n) Points to the single month with the largest combined volume.
>> o) Names the strongest line for each individual month.
>> p) Crowns the line with the biggest annual volume.
>> q) Flags the three-month block with the largest combined volume.
>> r) Holds, per three-month block, the average monthly volume of each line and of the combined figure.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)
