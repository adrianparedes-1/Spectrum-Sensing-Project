import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import joblib

# Load real training data
training_data_file = 'sample_name.csv'  # Path to your CSV file
historical_data = pd.read_csv(training_data_file)

historical_data['ComplexNumber'] = historical_data['Magnitude'].apply(lambda x: complex(x))

# Step 3: Extract features (Magnitude, Phase, Real, Imaginary)
historical_data['Magnitude'] = historical_data['ComplexNumber'].apply(np.abs)  # Magnitude of the complex number

split_index = int(len(historical_data)*0.8)

train_data = historical_data[:split_index]
test_data = historical_data[split_index:]

# Prepare training data
X_train = train_data[['Magnitude']].values
y_train = train_data['Label'].values
X_test = test_data[['Magnitude']].values
y_test = test_data['Label'].values

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

svm = SVC(kernel='rbf', random_state=42)
svm.fit(X_train, y_train)

y_pred = svm.predict(X_test)

# Calculate False Positive Rate (FPR)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
fpr = fp / (fp + tn)

print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test,y_pred))
print("False Positive Rate (FPR):", fpr)

# Save the trained model and scaler
joblib.dump(svm, 'svm_model_3.joblib')
joblib.dump(scaler, 'scaler_3.joblib')