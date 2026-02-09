
## Exercise 1: Identify Applications

**Objective:** Identify which field (Data Science, ML, AI, Big Data, BI) applies.
**Task:** Decide which domain fits each scenario:

1. A company wants to predict customer churn using historical data.
2. An app recommends products based on user behavior.
3. Storing and processing terabytes of sensor data from IoT devices.
4. A dashboard shows last year's sales trends.
5. An AI agent plays chess and learns strategies over time.

## Exercise 2: Roles in a Data Science Project

### Scenario

A hospital wants to build a system that predicts whether a patient is at risk of **heart disease** within the next 5 years.

Several specialists will be involved in this project: Data Analyst, Data Scientist, Data Engineer, ML Engineer, and Business Analyst.

### Tasks

**1. Match the Roles**

Assign the following tasks to the correct role(s):

*   (a) Collect patient records from multiple hospital databases and prepare them for use.
*   (b) Build a predictive model using patient data to estimate heart disease risk.
*   (c) Create a dashboard to show current statistics about patient risk factors (age, weight, smoking).
*   (d) Deploy the predictive model so doctors can access it via a web application.
*   (e) Define the business question: "How can we reduce the number of undetected high-risk patients?"

**2. Critical Thinking**

*   Explain in your own words why a **Data Engineer** and a **Machine Learning Engineer** cannot simply replace each other.
*   Also explain why a Data Analyst and a Data Scientist cannot fully replace each other?

file:///C:/Users/pc/Downloads/TP1_Chapter_Introduction (1).html
1/1

***

**Part 2: Solutions and Explanations**

### Solution to Exercise 1: Identify Applications

Here are the domains that best fit each scenario, along with a brief explanation.

1.  **A company wants to predict customer churn using historical data.**
    *   **Domain:** **Machine Learning (ML)** and **Data Science**.
    *   **How it works:** This is a classic classification problem. An ML model is trained on historical customer data (features) to predict a binary outcome (churn or no churn). This entire process of using data to make predictions is a core part of Data Science.

2.  **An app recommends products based on user behavior.**
    *   **Domain:** **Machine Learning (ML)**.
    *   **How it works:** This uses a recommender system, a specific application of ML. The system learns user preferences from their behavior (e.g., clicks, purchases, ratings) to suggest items they are likely to enjoy.

3.  **Storing and processing terabytes of sensor data from IoT devices.**
    *   **Domain:** **Big Data**.
    *   **How it works:** The key terms are "terabytes" and "storing and processing." Big Data technologies (like Hadoop, Spark, or cloud data lakes) are designed to handle massive volumes of data that traditional databases cannot manage efficiently.

4.  **A dashboard shows last year's sales trends.**
    *   **Domain:** **Business Intelligence (BI)**.
    *   **How it works:** BI focuses on descriptive analytics—summarizing historical data to understand past performance. Dashboards with charts and graphs showing trends, KPIs, and metrics are the primary output of BI.

5.  **An AI agent plays chess and learns strategies over time.**
    *   **Domain:** **Artificial Intelligence (AI)**.
    *   **How it works:** This goes beyond simple prediction. The agent exhibits intelligent behavior by perceiving its environment (the chessboard), making decisions (moves), and learning from the outcomes to improve its strategy. This is a hallmark of AI, often using a technique called reinforcement learning.

***

### Solution to Exercise 2: Roles in a Data Science Project

#### 1. Match the Roles

*   **(a) Collect patient records from multiple hospital databases and prepare them for use.**
    *   **Role:** **Data Engineer**.
    *   **Tip:** The Data Engineer is the architect of the data pipeline. Their job is to build robust, automated systems (ETL/ELT processes) to extract data from various sources (databases, APIs), transform it into a clean, usable format, and load it into a central repository (like a data warehouse) where the Data Scientist and Analyst can access it.

*   **(b) Build a predictive model using patient data to estimate heart disease risk.**
    *   **Role:** **Data Scientist**.
    *   **Tip:** This is the core modeling task. The Data Scientist explores the prepared data, selects relevant features, experiments with different algorithms (e.g., Logistic Regression, Gradient Boosting), trains the model, and evaluates its performance to ensure it accurately predicts risk.

*   **(c) Create a dashboard to show current statistics about patient risk factors (age, weight, smoking).**
    *   **Role:** **Data Analyst**.
    *   **Tip:** The Data Analyst focuses on descriptive analytics. They use tools like Tableau, Power BI, or Python libraries (Matplotlib, Seaborn) to create visualizations and dashboards that help stakeholders (like hospital administrators) understand the current state of patient health and identify trends from existing data.

*   **(d) Deploy the predictive model so doctors can access it via a web application.**
    *   **Role:** **Machine Learning (ML) Engineer**.
    *   **Tip:** An ML Engineer specializes in MLOps (Machine Learning Operations). They take the model built by the Data Scientist and productionalize it. This involves wrapping it in an API, deploying it on a server (cloud or on-premise), ensuring it can handle requests efficiently (scalability), and monitoring its performance over time.

*   **(e) Define the business question: "How can we reduce the number of undetected high-risk patients?"**
    *   **Role:** **Business Analyst**.
    *   **Tip:** The Business Analyst is the translator. They work with stakeholders (doctors, hospital management) to understand their needs and translate a high-level business goal into a specific, actionable, data-driven question that the technical team can solve.

#### Example Code Snippet (Illustrating Task b - Data Scientist's role)
This is a simplified Python example of what a Data Scientist might do to build a predictive model.

```python
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Tip: This code assumes the Data Engineer has already prepared a clean CSV file.
# 1. Load the prepared patient data
data = pd.read_csv('clean_patient_data.csv')

# 2. Define features (X) and the target variable (y)
# Features might include age, cholesterol, blood_pressure, etc.
# Target is what we want to predict: has_heart_disease (1 for yes, 0 for no)
features = ['age', 'sex', 'cholesterol', 'blood_pressure', 'smoking_status']
target = 'has_heart_disease'

X = data[features]
y = data[target]

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and train a machine learning model
# A RandomForestClassifier is a good choice for this type of problem.
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Make predictions on the test set and evaluate performance
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Tip: The final 'model' object is what the Data Scientist would hand off
# to the ML Engineer for deployment.
```

#### 2. Critical Thinking

*   **Why a Data Engineer and a Machine Learning Engineer cannot simply replace each other:**

    A **Data Engineer** focuses on the **data infrastructure**. Their primary goal is to make high-quality data available, reliable, and accessible. They build and maintain the "plumbing" of the data world: databases, data warehouses, and ETL/ELT pipelines. They are experts in data modeling, SQL, and big data technologies (like Spark). Their final product is a clean, well-structured dataset.

    A **Machine Learning Engineer** focuses on the **model infrastructure**. Their primary goal is to take a completed model and deploy it into a live production environment so it can be used. They are experts in software engineering principles, cloud computing (AWS, Azure, GCP), containerization (Docker), and MLOps tools. Their final product is a scalable, reliable, and monitored ML application (e.g., an API).

    **In short:** The Data Engineer builds the roads for data to travel on; the ML Engineer builds the factory that uses that data to produce a real-world service. One cannot do the other's job effectively because the core skills (data systems architecture vs. software/systems deployment) are fundamentally different.

*   **Why a Data Analyst and a Data Scientist cannot fully replace each other:**

    A **Data Analyst** primarily looks at the **past**. They answer the questions "What happened?" and "Why?". They use descriptive statistics, SQL queries, and visualization tools to mine historical data for insights, trends, and patterns. Their output is typically a report or a dashboard that helps business users make better-informed decisions based on past events.

    A **Data Scientist** primarily looks to the **future**. They build systems that make predictions or automated decisions. They answer the questions "What will happen next?" and "What is the best possible outcome?". They use advanced statistics, machine learning algorithms, and programming to create predictive models. While they can perform the tasks of an analyst, their core competency lies in advanced modeling and experimentation.

    **In short:** There is overlap, but the focus is different. An Analyst is a storyteller who explains what the data says about the past. A Scientist is an architect who uses data to build a system that can predict the future. A company needs both: an analyst to understand its current state and a scientist to chart its future direction.