import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib
import os

X, y = make_classification(
    n_samples=1000,
    n_features=5,
    n_classes=2,
    n_informative=2,
    random_state=42
)

cols = [
    "annual_income",
    "debt_to_income",
    "credit_history_months",
    "num_late_payments",
    "loan_amount"
]

X = pd.DataFrame(X, columns=cols)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

model = XGBClassifier(n_estimators=100, eval_metric="mlogloss")
model.fit(X_train, y_train)

print(f"Accuracy: {model.score(X_test, y_test):.2f}")

os.makedirs("ml", exist_ok=True)
joblib.dump(model, "ml/model.pkl")
print("Model saved to ml/model.pkl")