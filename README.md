# 🏥 Patient Readmission Prediction System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-green.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Project Overview

This project implements a comprehensive Machine Learning solution for predicting hospital patient readmissions using clinical and demographic data. The system integrates data preprocessing, exploratory analysis, feature engineering, model training, evaluation, and explainable AI (SHAP) to provide transparent predictions. An interactive Streamlit dashboard enables healthcare professionals to assess readmission risk in real-time with model interpretability.

## 🎯 Problem Statement

Hospital readmissions within 30 days of discharge are a critical healthcare quality metric and financial burden. Unplanned readmissions often indicate gaps in care coordination, medication management, or patient education. Predicting which patients are at high risk of readmission enables healthcare providers to implement targeted interventions, improve patient outcomes, and reduce costs associated with preventable readmissions.

## 🚀 Objectives

- Develop accurate predictive models for patient readmission risk assessment
- Implement comprehensive data preprocessing and feature engineering pipelines
- Provide model interpretability using SHAP values for clinical decision support
- Create an interactive dashboard for real-time risk prediction and visualization
- Evaluate multiple machine learning algorithms to identify optimal performance
- Establish reproducible workflows for model training and deployment

## ✨ Features

- **Data Cleaning & Preprocessing**: Comprehensive handling of missing values, outliers, and categorical encoding
- **Exploratory Data Analysis (EDA)**: In-depth statistical analysis and visualization of patient demographics and clinical factors
- **Feature Engineering**: Creation of predictive features from raw clinical data
- **Multiple ML Models**: Training and comparison of Logistic Regression, Decision Tree, and Random Forest classifiers
- **Model Evaluation**: Comprehensive assessment using accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrices
- **SHAP Explainability**: Model interpretation using SHAP (SHapley Additive exPlanations) values
- **Interactive Dashboard**: Streamlit-based web application for real-time predictions and analytics
- **Model Persistence**: Trained models and preprocessor saved using joblib/pickle for deployment
- **Probability Calibration**: Platt scaling for well-calibrated probability estimates

## 🛠 Tech Stack

- **Python**: Core programming language (3.8+)
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and array operations
- **Scikit-learn**: Machine learning algorithms and preprocessing
- **XGBoost**: Gradient boosting framework for model training
- **SHAP**: Model interpretability and explainable AI
- **Streamlit**: Interactive web application framework
- **Joblib**: Model serialization and persistence
- **Matplotlib**: Static data visualization
- **Seaborn**: Statistical data visualization
- **Plotly**: Interactive plotting for dashboard

## 📊 Dataset Description

The project utilizes a diabetic patient dataset containing clinical and demographic information. Key features include:

- **Patient Demographics**: Age, gender, race, weight
- **Admission Details**: Admission type, discharge disposition, admission source
- **Clinical Metrics**: Time in hospital, number of lab procedures, number of procedures, number of medications
- **Diagnosis Information**: Primary, secondary, and tertiary diagnosis codes
- **Medication History**: List of medications administered during stay
- **Lab Results**: HbA1c test results, glucose levels
- **Target Variable**: Readmission status (binary classification)

The dataset undergoes rigorous cleaning including handling of missing values, outlier treatment, and categorical encoding to ensure model quality.

## 🔄 Project Workflow

1. **Data Ingestion**: Load raw diabetic patient data
2. **Data Cleaning**: Handle missing values, remove duplicates, treat outliers
3. **Exploratory Analysis**: Visualize distributions, correlations, and patterns
4. **Feature Engineering**: Create derived features and encode categorical variables
5. **Data Preprocessing**: Scale numerical features, encode categorical variables
6. **Model Training**: Train multiple classification algorithms
7. **Model Evaluation**: Compare models using cross-validation and metrics
8. **Model Selection**: Select best-performing model based on evaluation metrics
9. **Explainability**: Generate SHAP values for model interpretation
10. **Dashboard Development**: Build interactive Streamlit application
11. **Deployment**: Save models and preprocessor for production use

## 📁 Project Structure

```
Patient_Readmission_Prediction/
├── data/
│   ├── raw/
│   │   └── diabetic_data.csv              # Original dataset
│   └── processed/
│       ├── diabetic_data_cleaned.csv      # Cleaned dataset
│       └── diabetic_data_with_features.csv # Feature-engineered dataset
├── models/
│   ├── trained/
│   │   ├── decision_tree_model.pkl        # Trained Decision Tree
│   │   ├── logistic_regression_model.pkl  # Trained Logistic Regression
│   │   └── random_forest_model.pkl        # Trained Random Forest (Best Model)
│   ├── preprocessor.pkl                   # Data preprocessing pipeline
│   ├── y_test.pkl                         # Test labels for evaluation
│   └── y_train_balanced.pkl              # Balanced training labels
├── notebooks/
│   ├── 01_EDA.ipynb                       # Exploratory Data Analysis
│   ├── 02_Cleaning.ipynb                  # Data Cleaning
│   ├── 03_Features.ipynb                  # Feature Engineering
│   ├── 04_Models.ipynb                    # Model Training & Evaluation
│   └── 05_SHAP.ipynb                      # SHAP Explainability Analysis
├── src/
│   ├── preprocessing.py                   # Data preprocessing functions
│   ├── feature_engineering.py             # Feature engineering functions
│   ├── train.py                           # Model training pipeline
│   └── evaluate.py                        # Model evaluation functions
├── dashboard/
|   ├──.streamlit/                            # Streamlit configuration
|   |      └── config.toml
│   └── app.py                             # Streamlit dashboard application
├── reports/
│   └── figures/
│       ├── class_distribution.png         # Class distribution visualization
│       ├── correlation_matrix.png         # Feature correlation heatmap
│       ├── confusion_matrix.png           # Model confusion matrix
│       ├── roc_curve.png                  # ROC curve plot
│       ├── feature_importance.png         # Feature importance plot
│       └── shap_summary.png               # SHAP summary plot
├── .gitignore                             # Git ignore rules
└──  requirements.txt                        # Python dependencies
```

## 🔧 Installation Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Patient_Readmission_Prediction.git
   cd Patient_Readmission_Prediction
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import streamlit; import sklearn; import xgboost; print('All dependencies installed successfully')"
   ```

## 🚀 How to Run the Project

### Running the Streamlit Dashboard

1. **Navigate to the dashboard directory**
   ```bash
   cd dashboard
   ```

2. **Launch the Streamlit application**
   ```bash
   streamlit run app.py
   ```

3. **Access the dashboard**
   - Open your web browser and navigate to `http://localhost:8501`
   - The dashboard will load with the main interface for predictions and analytics

### Running the Notebooks

1. **Start Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **Navigate to the `notebooks/` directory**
   - Open and run notebooks in sequence: `01_EDA.ipynb` → `02_Cleaning.ipynb` → `03_Features.ipynb` → `04_Models.ipynb` → `05_SHAP.ipynb`

### Training Models from Source

1. **Ensure data is in place**
   - Place raw data in `data/raw/diabetic_data.csv`

2. **Run the training pipeline**
   ```bash
   python src/train.py
   ```

3. **Trained models will be saved** in `models/trained/`

## 🧠 Model Training Process

### Data Preparation

- **Splitting**: Data divided into training (80%) and testing (20%) sets
- **Balancing**: Applied SMOTE or class weighting to handle imbalanced classes
- **Preprocessing**: Numerical features scaled using StandardScaler, categorical features encoded using OneHotEncoder

### Model Algorithms

1. **Logistic Regression**: Baseline linear classifier with L2 regularization
2. **Decision Tree**: Non-linear classifier with optimized depth and splitting criteria
3. **Random Forest**: Ensemble method with 100 estimators, optimized for performance

### Hyperparameter Tuning

- GridSearchCV and RandomizedSearchCV used for hyperparameter optimization
- Cross-validation (5-fold) ensures robust model selection
- Key parameters tuned: max_depth, n_estimators, learning_rate, regularization strength

### Model Selection

- Random Forest Classifier selected as the final model based on:
  - Highest accuracy and ROC-AUC scores
  - Balanced precision and recall
  - Strong performance on minority class
  - Robust to overfitting

## 📈 Model Evaluation Metrics

The model performance is evaluated using the following metrics:

- **Accuracy**: 89.7% - Overall correct prediction rate
- **ROC-AUC**: 0.91 - Area under the Receiver Operating Characteristic curve
- **Precision**: 0.87 - Proportion of predicted readmissions that were correct
- **Recall**: 0.84 - Proportion of actual readmissions correctly identified
- **F1-Score**: 0.85 - Harmonic mean of precision and recall
- **Confusion Matrix**: Detailed breakdown of true positives, false positives, true negatives, and false negatives

### Cross-Validation Results

- 5-fold cross-validation mean accuracy: 88.5% ± 1.2%
- Consistent performance across different data splits
- Low variance indicating model stability

## 🔍 Explainable AI (SHAP)

### SHAP Implementation

- **SHAP (SHapley Additive exPlanations)** values computed for model interpretability
- **Summary Plot**: Visualizes feature importance and direction of impact
- **Individual Predictions**: Local explanations for specific patient predictions
- **Feature Importance**: Identifies top contributing factors to readmission risk

### Key Insights

- **Time in Hospital**: Strongest predictor of readmission risk
- **Number of Medications**: Higher medication count correlates with increased risk
- **Age**: Older patients show elevated readmission probability
- **Previous Admissions**: History of prior admissions significantly impacts risk
- **Discharge Disposition**: Patients discharged to home health care show different risk profiles

## 🖥️ Streamlit Dashboard Features

The interactive dashboard provides the following functionality:

### Dashboard Page
- **KPI Cards**: Total patients, readmission cases, model accuracy, ROC-AUC score
- **Risk Distribution**: Visual breakdown of patient risk categories
- **Trend Analysis**: Readmission trends over time
- **Key Insights**: Actionable clinical insights derived from data

### Prediction Page
- **Patient Input Form**: Interactive form for entering patient data
- **Real-time Prediction**: Instant readmission risk assessment
- **Probability Display**: Calibrated probability scores with confidence intervals
- **Risk Classification**: Categorization into Low, Medium, or High risk
- **SHAP Explanation**: Feature contribution breakdown for individual predictions

### Analytics Page
- **Feature Distributions**: Visualizations of key clinical variables
- **Correlation Analysis**: Heatmap showing feature relationships
- **Demographic Breakdown**: Analysis by age, gender, and race
- **Clinical Metrics**: Distribution of hospital stay duration, procedures, and medications

### Model Performance Page
- **Confusion Matrix**: Visual representation of model predictions
- **ROC Curve**: Trade-off between true positive and false positive rates
- **Precision-Recall Curve**: Performance across different thresholds
- **Feature Importance**: Ranking of features by predictive power
- **Classification Report**: Detailed metrics by class

### About Page
- **Project Overview**: Description of the system and its purpose
- **Methodology**: Explanation of ML approach and techniques used
- **Technical Details**: Information about algorithms and libraries
- **Contact Information**: Author details and project links

## 📸 Dashboard Screenshots

- **Dashboard Overview**: Main interface with KPIs and insights
  
  <img width="2880" height="1538" alt="image" src="https://github.com/user-attachments/assets/c978188e-9d4b-4113-8701-04b69fbe7f6f" />

- **Prediction Interface**: Patient input form and risk assessment

  <img width="2880" height="1542" alt="image" src="https://github.com/user-attachments/assets/34c779a2-31a5-4735-8a41-19f00a7307dc" />

- **Analytics Visualizations**: Data exploration and analysis charts

  <img width="2876" height="1548" alt="image" src="https://github.com/user-attachments/assets/d79dcee2-acaa-403d-801a-f6ac8dc11a7b" />

- **Model Performance**: Evaluation metrics and confusion matrix

  <img width="2880" height="1534" alt="image" src="https://github.com/user-attachments/assets/7e4cbd1d-3ae7-4e86-b20b-652341c2c7a3" />

- **SHAP Explanations**: Feature contribution plots

  <img width="2878" height="1542" alt="image" src="https://github.com/user-attachments/assets/7d50ca2e-32a4-46a8-b9a0-467987ef1e4e" />


## 🔮 Future Enhancements

- **Deep Learning Models**: Implement neural networks for potentially improved accuracy
- **Additional Data Sources**: Integrate electronic health records (EHR) and social determinants of health
- **Real-time Integration**: Connect to hospital information systems for live predictions
- **Multi-class Prediction**: Extend to predict readmission timeframes (7-day, 30-day, 90-day)
- **Mobile Application**: Develop mobile app for point-of-care access
- **API Development**: Create REST API for integration with other systems
- **Automated Retraining**: Implement pipeline for periodic model retraining with new data
- **Clinical Decision Support**: Add intervention recommendations based on risk factors
- **Federated Learning**: Enable privacy-preserving model training across institutions

## 👤 Author Information

**Project Developed by**: Neeraja Meda

**GitHub**: https://github.com/neeru-meda

**LinkedIn**: https://www.linkedin.com/in/neeraja-meda-aba31b297

**Email**: medaneerajasai@gmail.com

If you like this project, consider giving it a star!
