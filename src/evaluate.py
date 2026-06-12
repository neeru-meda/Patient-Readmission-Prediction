import joblib
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve
)

# Load test data

x_test = joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\x_test_processed.pkl")
y_test = joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\y_test.pkl")

print("x_test shape:", x_test.shape)
print("y_test shape:", y_test.shape)

# recover feature names
preprocessor = joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\preprocessor.pkl")
feature_names = preprocessor.get_feature_names_out()
x_test_df = pd.DataFrame(x_test, columns=feature_names)

#load models
models = {
    "Logistic Regression": joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\trained\\logistic_regression_model.pkl"),
    "Decision Tree": joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\trained\\decision_tree_model.pkl"),
    "Random Forest": joblib.load("d:\\Codes\\Patient_Readmission_Prediction\\models\\trained\\random_forest_model.pkl")
}

# Evaluate models
results = []

best_auc = -1
best_model = None
best_model_name = ""

for name, model in models.items():
    print(f"\n{'=*50'}")
    print(f"Evaluating {name}...")
    print(f"{'=*50'}\n")

    y_pred = model.predict(x_test)
    y_proba = model.predict_proba(x_test)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print(classification_report(y_test, y_pred))

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "AUC": auc
    })

    fpr, tpr, _ = roc_curve(y_test, y_proba)

    plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})")

    if auc > best_auc:
        best_auc = auc
        best_model = model
        best_model_name = name

# Show ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend()
plt.tight_layout()
plt.savefig("d:\\Codes\\Patient_Readmission_Prediction\\reports\\figures\\roc_curve_comparison.png")
plt.close()
print("ROC Curve Saved!")

#model comparison table
results_df = pd.DataFrame(results)
print("\nModel Comparison:")
print(results_df)

results_df.set_index("Model").plot(kind='bar', figsize=(10, 6))
plt.title("Model Comparison")
plt.ylabel("Score")
plt.xlabel("Model")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("d:\\Codes\\Patient_Readmission_Prediction\\reports\\figures\\model_comparison.png")
plt.close()
print("Model Comparison Bar Chart Saved!")

#best model
print(f"\nBest Model: {best_model_name}")

# confusion matrix
y_pred_best = best_model.predict(x_test)
cm = confusion_matrix(y_test, y_pred_best)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap = "Greens")
plt.title(f"{best_model_name} - Confusion Matrix")
plt.tight_layout()
plt.savefig(f"d:\\Codes\\Patient_Readmission_Prediction\\reports\\figures\\confusion_matrix.png")
plt.close()
print("Confusion Matrix Saved!")

#SHAP Analysis
print("\nGenerating SHAP Analysis...")
x_sample = x_test_df.sample(n=100, random_state=42)
explainer = shap.TreeExplainer(best_model)
try:
    shap_values = explainer(x_sample)
    plt.figure(figsize=(12, 8))
    shap.summary_plot(
        shap_values,
        x_sample,
        max_display=20,
        show=False
    )
except :
    shap_values = explainer.shap_values(x_sample)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    plt.figure(figsize=(12, 8))
    shap.summary_plot(
        shap_values,
        x_sample,
        max_display=20,
        show=False
    )
    plt.tight_layout()
    plt.savefig(f"d:\\Codes\\Patient_Readmission_Prediction\\reports\\figures\\shap_summary.png",bbox_inches='tight')
    plt.close()
    print("SHAP Summary Plot Saved!")

#SHAP Top 15 features
x_sample = x_test_df.iloc[:50]

explainer = shap.TreeExplainer(best_model)

shap_values = explainer(x_sample)

print("SHAP Shape:", shap_values.values.shape)

plt.figure(figsize=(14,10))

shap.summary_plot(
    shap_values.values[:, :, 1],   # IMPORTANT
    x_sample,
    feature_names=x_sample.columns,
    max_display=20,
    show=False
)

plt.title(
    "SHAP Summary Plot (Top 20 Features)",
    fontsize=14
)

plt.tight_layout()

plt.savefig(
    "d:\\Codes\\Patient_Readmission_Prediction\\reports\\figures\\shap_top20.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("SHAP Summary Plot Saved!")

#waterfall plot
# Find highest-risk patient

risk_scores = best_model.predict_proba(x_sample.values)[:, 1]

high_risk_idx = np.argmax(risk_scores)

print("Highest Risk Patient Index:", high_risk_idx)
print("Predicted Risk:", risk_scores[high_risk_idx])

try:

    risk_scores = best_model.predict_proba(x_sample.values)[:, 1]

    high_risk_idx = np.argmax(risk_scores)

    patient_row = x_sample.iloc[[high_risk_idx]]

    patient_shap = explainer(patient_row)

    plt.figure(figsize=(12, 8))

    shap.plots.waterfall(
        patient_shap[0, :, 1],   # <- Class 1
        max_display=15,
        show=False
    )

    plt.savefig(
        "d:\\Codes\\Patient_Readmission_Prediction\\reports\\figures\\high_risk_waterfall.png",
        bbox_inches="tight"
    )

    plt.close()
    print("High Risk Waterfall Plot Saved")

except Exception as e:
    print("Error generating SHAP waterfall plot:",e)

print("\nEvaluation Completed!")