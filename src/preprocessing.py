import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder, 
    StandardScaler,
)
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

#load dataset
Data_PATH = 'd:\\Codes\\Patient_Readmission_Prediction\\data\\processed\\diabetic_data_with_features.csv'
df = pd.read_csv(Data_PATH)
print("Dataset shape:", df.shape)

#target variable
Target = 'target'
x  = df.drop(columns=[Target])
y = df[Target]

# Numerical features
numerical_features = [
    'time_in_hospital',
    'num_lab_procedures',
    'num_procedures',
    'num_medications',
    'number_outpatient',
    'number_emergency',
    'number_inpatient',
    'number_diagnoses',
    'age_numeric',
    'total_prior_visits',
    'treatment_changed',
    'lab_intensity',
    'med_intensity'
]

#categorical features
categorical_features = [
    'race',
    'gender',
    'admission_type_id',
    'discharge_disposition_id',
    'admission_source_id',
    'diag_1',
    'diag_2',
    'diag_3',
    'max_glu_serum',
    'A1Cresult',

    'metformin',
    'repaglinide',
    'nateglinide',
    'chlorpropamide',
    'glimepiride',
    'acetohexamide',
    'glipizide',
    'glyburide',
    'tolbutamide',
    'pioglitazone',
    'rosiglitazone',
    'acarbose',
    'miglitol',
    'troglitazone',
    'tolazamide',
    'examide',
    'citoglipton',
    'insulin',

    'glyburide-metformin',
    'glipizide-metformin',
    'glimepiride-pioglitazone',
    'metformin-rosiglitazone',
    'metformin-pioglitazone',

    'change',
    'diabetesMed',
    'diag1_category'
]

# print(set(numerical_features) - set(x.columns))
# print(set(categorical_features) - set(x.columns))

    
#train test split
x_train, x_test, y_train, y_test = train_test_split(
    x, 
    y, 
    test_size=0.2, 
    random_state=42,
    stratify = y
)

print("Training set shape:", x_train.shape)
print("Test set shape:", x_test.shape)

#preprocessing pipeline
numerical_transformer = Pipeline([('scaler',StandardScaler())])
categorical_transformer = Pipeline([('onehot',
                                    OneHotEncoder(handle_unknown ='ignore', sparse_output = False))])
preprocessor = ColumnTransformer(
    transformers = [
        ('num',numerical_transformer, numerical_features),
        ('cat',categorical_transformer, categorical_features)
    ]
)

#transform the data
x_train_processed = preprocessor.fit_transform(x_train)
x_test_processed = preprocessor.transform(x_test)

print("Processed training set shape:", x_train_processed.shape)
print("Processed test set shape:", x_test_processed.shape)

smote = SMOTE(random_state = 42)

x_train_balanced, y_train_balanced = smote.fit_resample(x_train_processed, y_train)

print("\nAfter SMOTE")
print("x_train_balanced shape:", x_train_balanced.shape)
print("y_train_balanced :", y_train_balanced.value_counts())

# Save the preprocessed data
import joblib

joblib.dump(preprocessor, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\preprocessor.pkl')
print("\nPreprocessor saved!")

joblib.dump(x_train_processed, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\x_train_processed.pkl')
joblib.dump(x_test_processed, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\x_test_processed.pkl')
joblib.dump(x_train_balanced, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\x_train_balanced.pkl')
joblib.dump(y_train_balanced, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\y_train_balanced.pkl')
joblib.dump(y_test, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\y_test.pkl')
print("Preprocessed data saved!")