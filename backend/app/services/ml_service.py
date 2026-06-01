#This file loads my trained ML model and uses it to predict the credit risk tier for a given user's financial data.

# joblib - loads your saved model from the `.pkl` file
# pandas = converts the incoming data into a DataFrame so the model can read it

import joblib
import pandas as pd

# Loads the trained model from disk once when the server starts up
# We don't want to reload the model on every request, that would be very slow 
model = joblib.load("ml/model.pkl")

# The ML model outputs numbers - 0,1, or 2. This dictionary translates those numbers into human-readable labels
# 0 -> "Low" risk
# 1 -> "Medium" risk
# 2 -> "High" risk 
RISK_TIERS = {0: "Low", 1: "Medium", 2: "High"}

# Defines the function with type hints
def run_prediction(data: dict) -> dict:
    # Converts the incoming data dictionary into a pandas DataFrame
    # The XGBoost model was trained on DataFrames, so it expects a DataFrame as input, not a raw dictionary
    df = pd.DataFrame([data])
    # Returns the probability for each risk tier, then takes the highest probability, converts it from a numpy number to a plain Python float so it can be JSON serialized
    # This is the confidence score - how sure the model is about its prediction
    score = float(model.predict_proba(df)[0].max())
    # `predict` returns the predicted class(like 2), then converts it from numpy integer to plain Python integer
    label = int(model.predict(df)[0])
    return {
        "risk_tier": RISK_TIERS[label],
        "confidence": round(score, 3),
    }
