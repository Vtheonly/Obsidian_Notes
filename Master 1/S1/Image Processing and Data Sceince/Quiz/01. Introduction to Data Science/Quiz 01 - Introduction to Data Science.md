---
sources:
  - "[[01.1. Data Science Foundations and CRISP-DM Workflow]]"
  - "[[01.2. The Modern Data Ecosystem and Professional Roles]]"
  - "[[01.3. Setting Up the Professional Python and Data Science Environment]]"
  - "[[01.4. Tutorial 02 - Hospital Patient Cohort Initialization and Environment Audit]]"
---
> [!question] Data Science is an interdisciplinary field that combines mathematical analysis, computational algorithms, and contextual domain expertise to discover patterns and build predictive engines.
>> [!success]- Answer
>> True

> [!question] The Cross-Industry Standard Process for Data Mining (CRISP-DM) prescribes a strictly linear sequence of stages, where each stage is completed exactly once per project.
>> [!success]- Answer
>> False

> [!question] In the CRISP-DM lifecycle, imputing null values and removing duplicate records take place during the Modeling stage.
>> [!success]- Answer
>> False

> [!question] The Evaluation stage of CRISP-DM assesses model predictions against unseen validation sets using domain-specific metrics such as AUC-ROC, F1-Score, and RMSE.
>> [!success]- Answer
>> True

> [!question] In the CRISP-DM lifecycle, when the Monitoring stage detects concept drift in a deployed model, the process loops back to Problem Definition.
>> [!success]- Answer
>> True

> [!question] In the comparative ecosystem matrix, Data Science is characterized by designing autonomous agents that exhibit cognitive reasoning.
>> [!success]- Answer
>> False

> [!question] A Data Engineer designs scalable, fault-tolerant ingestion pipelines and data warehouses, with expertise in distributed architectures, ACID transactional safety, and database partitioning.
>> [!success]- Answer
>> True

> [!question] In the hospital patient cohort tutorial, the categorical Diagnosis feature is summarized by passing it through `df.describe()` alongside Age and BloodPressure.
>> [!success]- Answer
>> False

> [!question] Python installs libraries globally by default, which is why running multiple projects on a single global installation often leads to dependency conflicts.
>> [!success]- Answer
>> True

> [!question] In the hospital patient cohort tutorial, the `env/` virtual environment folder should be committed to Git so that teammates can reuse it directly.
>> [!success]- Answer
>> False

> [!question] In the CRISP-DM lifecycle, which stage immediately follows Data Collection?
> a) Exploratory Data Analysis
> b) Data Cleaning and Preparation
> c) Problem Definition
> d) Modeling
>> [!success]- Answer
>> b) Data Cleaning and Preparation

> [!question] According to the CRISP-DM lifecycle, what happens during the Deployment stage?
> a) Live inference pipelines are audited for data drift and latency regressions
> b) Generalized predictions are assessed against unseen validation sets
> c) Model artifacts are containerized into production microservices exposed via REST endpoints
> d) Ambiguous operational challenges are translated into measurable objectives
>> [!success]- Answer
>> c) Model artifacts are containerized into production microservices exposed via REST endpoints

> [!question] Which activities characterize the Exploratory Data Analysis stage of the CRISP-DM lifecycle?
> a) Imputing null values and removing duplicate records
> b) Containerizing model artifacts with Docker
> c) Auditing live pipelines for concept drift
> d) Calculating summary statistics such as skewness and kurtosis and charting variable distributions
>> [!success]- Answer
>> d) Calculating summary statistics such as skewness and kurtosis and charting variable distributions

> [!question] In the comparative ecosystem matrix, which field is centered on descriptive and diagnostic analysis of past operations?
> a) Business Intelligence
> b) Data Science
> c) Machine Learning
> d) Big Data
>> [!success]- Answer
>> a) Business Intelligence

> [!question] Processing sensor streams from 50,000 IoT devices is classified as a Big Data Engineering problem because the workload is defined by which characteristics?
> a) ACID safety, serialization, and partitioning
> b) Skewness, kurtosis, and variance
> c) High data Volume, Velocity, and Variety
> d) Latency optimization, quantization, and drift
>> [!success]- Answer
>> c) High data Volume, Velocity, and Variety

> [!question] According to the IDE comparison, what is a key limitation of Jupyter Notebook?
> a) It cannot display inline plots
> b) Its .ipynb JSON format produces noisy diffs, and it is not suited for production APIs
> c) It requires a commercial license for the full feature set
> d) It lacks a variable explorer for inspecting arrays
>> [!success]- Answer
>> b) Its .ipynb JSON format produces noisy diffs, and it is not suited for production APIs

> [!question] What distinguishes conda from pip as a package manager?
> a) It fetches packages exclusively from the Python Package Index
> b) It requires separate tooling such as venv for environment management
> c) It installs multi-language packages and resolves system-level shared C library dependencies
> d) It falls back to a local compiler whenever pre-compiled wheels are unavailable
>> [!success]- Answer
>> c) It installs multi-language packages and resolves system-level shared C library dependencies

> [!question] Which path practice does the hospital patient cohort tutorial recommend when loading `patients.csv` to keep the notebook portable?
> a) Hardcode a machine-specific absolute path to the CSV file
> b) Use a relative path such as `../data/patients.csv` instead of machine-specific absolute paths
> c) Fetch the dataset from a remote REST API at runtime
> d) Duplicate the CSV into every directory the script runs from
>> [!success]- Answer
>> b) Use a relative path such as `../data/patients.csv` instead of machine-specific absolute paths

> [!question] The first notebook cell of the hospital patient cohort tutorial inspects the loaded DataFrame; which outputs does it produce?
> a) Cohort dimensions, the memory summary from `df.info()`, and the first 5 records
> b) A styled scatter plot of age versus cholesterol
> c) Frequency counts for the Sex and Diagnosis attributes
> d) The Git commit history and requirements.txt contents
>> [!success]- Answer
>> a) Cohort dimensions, the memory summary from `df.info()`, and the first 5 records

> [!question] In the hospital patient cohort tutorial, what were the reported average age and mean cholesterol level of the patient cohort?
> a) 25 years and 200 mg/dL
> b) 55 years and 300 mg/dL
> c) 80 years and 350 mg/dL
> d) 45.7 years and 220 mg/dL
>> [!success]- Answer
>> d) 45.7 years and 220 mg/dL

> [!question] Match the CRISP-DM stage with its primary activity.
>> [!example] Group A
>> a) Problem Definition
>> b) Data Collection
>> c) Modeling
>> d) Monitoring
>
>> [!example] Group B
>> n) Translating ambiguous operational or clinical challenges into concrete, measurable analytical objectives.
>> o) Extracting records from internal transaction databases, external REST APIs, telemetry streams, and flat file archives.
>> p) Auditing live inference pipelines for data drift, latency regressions, and software dependency failures.
>> q) Choosing and training algorithmic representations such as Logistic Regression and Neural Networks.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> q)
>> d) -> p)

> [!question] Match the data science discipline pillar with its representative topics.
>> [!example] Group A
>> a) Mathematics and Statistics
>> b) Computer Science
>> c) Domain Knowledge
>> d) Communication
>
>> [!example] Group B
>> n) Algorithms and distributed systems.
>> o) Data storytelling and technical translation.
>> p) Probability modeling and calculus.
>> q) Healthcare, financial modeling, and marketing.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the analytics level with the question it answers.
>> [!example] Group A
>> a) Descriptive
>> b) Diagnostic
>> c) Predictive
>> d) Prescriptive
>
>> [!example] Group B
>> n) Asks what will happen.
>> o) Asks what happened.
>> p) Asks what should be done.
>> q) Asks why it happened.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the professional role with its primary contribution in the data collaboration workflow.
>> [!example] Group A
>> a) Business Analyst
>> b) Data Scientist
>> c) Machine Learning Engineer
>> d) Data Analyst
>
>> [!example] Group B
>> n) Defines the requirements that analytical work must address.
>> o) Builds visual reporting layers for operational stakeholders.
>> p) Trains and validates prototype models ahead of production scaling.
>> q) Packages and scales low-latency APIs into production microservices.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> q)
>> d) -> o)

> [!question] Match the field with its primary technical stack.
>> [!example] Group A
>> a) Business Intelligence
>> b) Machine Learning
>> c) Artificial Intelligence
>> d) Big Data
>
>> [!example] Group B
>> n) Draws on Spark, Hadoop, Kafka, and Flink for distributed data at ingestion scale.
>> o) Draws on SQL, PowerBI, Tableau, and Excel for executive dashboards and KPI reports.
>> p) Draws on PyTorch, TensorFlow, and Scikit-Learn to produce serialized models.
>> q) Draws on Reinforcement Learning and Transformers to build autonomous agents.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the development environment with its key strength.
>> [!example] Group A
>> a) Jupyter Notebook
>> b) VS Code
>> c) PyCharm Professional
>> d) Spyder
>
>> [!example] Group B
>> n) A MATLAB-like interface with a variable explorer and array inspector for scientific computation.
>> o) Interactive step-by-step execution with inline plots, well suited to exploratory analysis.
>> p) Advanced refactoring, deep debugging, and built-in database tools for large-scale production applications.
>> q) An extensible ecosystem with an integrated terminal, Git integration, and remote SSH execution.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the project directory entry with its purpose.
>> [!example] Group A
>> a) `data/raw`
>> b) `data/processed`
>> c) `src`
>> d) `outputs`
>
>> [!example] Group B
>> n) Immutable original extracts that must never be modified.
>> o) Production Python modules of the project.
>> p) Cleaned and engineered datasets.
>> q) Exported figures, plots, and metrics.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
>> d) -> q)

> [!question] Match the environment command with its purpose.
>> [!example] Group A
>> a) `pip install -r requirements.txt`
>> b) `conda activate clinical_env`
>> c) `pip freeze`
>> d) `conda env export`
>
>> [!example] Group B
>> n) Records the exact current package versions into a dependency file.
>> o) Recreates the exact dependency list on a new machine.
>> p) Serializes the complete package state into a YAML definition.
>> q) Switches the current shell into a named isolated runtime.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the hospital cohort tutorial step with what it accomplishes.
>> [!example] Group A
>> a) `mkdir -p data notebooks scripts`
>> b) `python -m venv env`
>> c) `git init`
>> d) `pip install numpy pandas matplotlib jupyter`
>
>> [!example] Group B
>> n) Places the project under version control.
>> o) Installs the analysis libraries into the isolated runtime.
>> p) Creates the project directory skeleton.
>> q) Initializes the isolated runtime for the project.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the scatter plot element with the patient attribute it encodes in the hospital cohort visualization.
>> [!example] Group A
>> a) X-axis
>> b) Y-axis
>> c) Marker color
>> d) Colormap
>
>> [!example] Group B
>> n) The patient's age in years.
>> o) The serum cholesterol level.
>> p) The blood pressure reading.
>> q) The viridis palette applied to markers.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
