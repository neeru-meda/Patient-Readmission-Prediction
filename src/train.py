import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Load preprocessed data
x_train = joblib.load('d:\\Codes\\Patient_Readmission_Prediction\\models\\x_train_balanced.pkl')
y_train = joblib.load('d:\\Codes\\Patient_Readmission_Prediction\\models\\y_train_balanced.pkl')

print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)

#logistic regression
lr = LogisticRegression(
    C = 1.0,
    class_weight = 'balanced',
    max_iter = 3000,
    random_state = 42
)

lr.fit(x_train, y_train)

# Save the trained model
joblib.dump(lr, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\trained\\logistic_regression_model.pkl')
print("Logistic Regression model saved!")

#decision tree
dt = DecisionTreeClassifier(
    max_depth = 5,
    class_weight = 'balanced',
    random_state = 42
)

dt.fit(x_train, y_train)

# Save the trained model
joblib.dump(dt, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\trained\\decision_tree_model.pkl')
print("Decision Tree model saved!")

#random forest
rf = RandomForestClassifier(
    n_estimators = 100,
    max_depth = 10,
    class_weight = 'balanced',
    random_state = 42,
    n_jobs = -1
)

rf.fit(x_train, y_train)

# Save the trained model
joblib.dump(rf, 'd:\\Codes\\Patient_Readmission_Prediction\\models\\trained\\random_forest_model.pkl')
print("Random Forest model saved!")

print("\nAll models trained and saved successfully!")



import joblib
import pandas as pd

x_test = joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\x_test_processed.pkl")
y_test = joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\y_test.pkl")

preprocessor = joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\preprocessor.pkl")

feature_names = preprocessor.get_feature_names_out()

x_test_df = pd.DataFrame(
    x_test,
    columns=feature_names
)

print("x_test_df shape:", x_test_df.shape)
print("x_test_df head():\n", x_test_df.head())