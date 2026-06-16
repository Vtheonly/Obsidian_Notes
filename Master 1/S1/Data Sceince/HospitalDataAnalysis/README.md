# Hospital Patient Data Analysis

## Project Overview
A clean data science project setup for analyzing hospital patient data. This project demonstrates environment isolation, data ingestion, descriptive statistics, and data visualization using Python's data science stack.

## Project Structure
```
HospitalDataAnalysis/
├── env/                          # Virtual environment folder (ignored by Git)
├── data/
│   └── patients.csv              # Raw patient dataset
├── notebooks/
│   └── patients_analysis.ipynb    # Jupyter Notebook with analysis
├── scripts/                      # Utility Python scripts
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

## Dataset
The dataset (`data/patients.csv`) contains 10 patient records with the following attributes:
- **PatientID**: Unique identifier
- **Age**: Patient age in years
- **Sex**: Male/Female
- **BloodPressure**: Systolic blood pressure (mmHg)
- **Cholesterol**: Cholesterol level (mg/dL)
- **Diagnosis**: Medical diagnosis (Diabetes, Healthy, Hypertension)

## Setup Instructions

### 1. Create and Activate Virtual Environment
```bash
python -m venv env
source env/bin/activate    # macOS/Linux
# .\env\Scripts\activate   # Windows
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install numpy pandas matplotlib jupyter
```

### 3. Launch Jupyter Notebook
```bash
jupyter notebook notebooks/patients_analysis.ipynb
```

### 4. Export Environment (for reproducibility)
```bash
pip freeze > requirements.txt
```

## Notebook Cells
1. **Data Ingestion**: Loads CSV data and displays shape + first 5 rows
2. **Descriptive Statistics**: Computes numerical stats and categorical distributions
3. **Data Visualization**: Scatter plot of Age vs Cholesterol