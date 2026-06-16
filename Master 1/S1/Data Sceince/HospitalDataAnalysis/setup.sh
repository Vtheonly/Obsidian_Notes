#!/bin/bash
# Hospital Data Analysis - Environment Setup Script
# Run: bash setup.sh

set -e

echo "=== Step 1: Creating virtual environment ==="
python3 -m venv env
source env/bin/activate

echo "=== Step 2: Upgrading pip ==="
pip install --upgrade pip

echo "=== Step 3: Installing dependencies ==="
pip install numpy pandas matplotlib jupyter

echo "=== Step 4: Registering Jupyter kernel ==="
python3 -m ipykernel install --user --name=hospital_env --display-name="Python (Hospital Analysis)"

echo "=== Step 5: Updating notebook kernel spec ==="
cat > notebooks/patients_analysis.ipynb << 'NOTEBOOK_EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Hospital Patient Data Analysis\n",
    "\n",
    "This notebook performs descriptive statistics and visualization on the hospital patient dataset."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Load dataset using a relative file path\n",
    "df = pd.read_csv(\"../data/patients.csv\")\n",
    "\n",
    "# Print the shape of the DataFrame (rows, columns)\n",
    "print(f\"Dataset Dimensions: {df.shape}\")\n",
    "\n",
    "# Preview the top 5 records\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Compute descriptive statistics for numerical columns\n",
    "print(\"--- Numerical Column Statistics ---\")\n",
    "print(df.describe())\n",
    "\n",
    "# Compute class distributions for categorical columns\n",
    "print(\"\\n--- Sex Categorical Distribution ---\")\n",
    "print(df['Sex'].value_counts())\n",
    "\n",
    "print(\"\\n--- Diagnosis Categorical Distribution ---\")\n",
    "print(df['Diagnosis'].value_counts())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set the plot style and figure size\n",
    "plt.figure(figsize=(8, 5))\n",
    "\n",
    "# Generate scatter plot: Age vs Cholesterol, color-coded\n",
    "plt.scatter(df['Age'], df['Cholesterol'], color='darkred', marker='o', s=80, alpha=0.8, edgecolor='black', label='Patients')\n",
    "\n",
    "# Apply labels, title, grid, and legend\n",
    "plt.xlabel(\"Age (Years)\", fontsize=12)\n",
    "plt.ylabel(\"Cholesterol Level (mg/dL)\", fontsize=12)\n",
    "plt.title(\"Patient Cholesterol Levels vs. Patient Age\", fontsize=14, fontweight='bold')\n",
    "plt.grid(True, linestyle='--', alpha=0.6)\n",
    "plt.legend()\n",
    "\n",
    "# Render plot cleanly in output window\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (Hospital Analysis)",
   "language": "python",
   "name": "hospital_env"
  },
  "language_info": {
   "name": "python",
   "version": "3.0.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
NOTEBOOK_EOF

echo "=== Step 6: Exporting requirements ==="
pip freeze > requirements.txt

echo ""
echo "============================================="
echo "Setup complete!"
echo "============================================="
echo ""
echo "Activate environment: source env/bin/activate"
echo "Launch notebook:      jupyter notebook notebooks/patients_analysis.ipynb"
echo ""