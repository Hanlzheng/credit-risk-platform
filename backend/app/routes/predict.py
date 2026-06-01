# This file handles the predict endpoint 
# It receives financial data from the frontend, validates it, runs it through my XGBoost model,
# and sends back a credit risk score

# jwt_required - as decorator that blocks the endpoint if the user isn't loggin in
# PredictSchema - my validation rules
# run_prediction - the function that actually runs my ML model
# validationError - the error marshmallow throws when input data is invalid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.schemas.predict_schema import PredictSchema
from app.services.ml_service import run_prediction
from marshmallow import ValidationError

# Creates the Bluepoint and one instance of my validation schema.
# We create schema once here instead of inside the function
# so Python doesn't recreate it on every request
predict_bp = Blueprint("predict", __name__)
schema = PredictSchema()

# Two decorators stacked on top of the function
@predict_bp.route("/predict", methods=["POST"]) # register this as the `/api/v1/predict` endpoint
@jwt_required() # checks the request has a valid login token before doing anything
                # If the user isn't logged in, Flask automatically returns 401 and never even reaches my code
def predict():
    try:
        data = schema.load(request.get_json()) # runs my validation rules against the incoming data
                                               # If the data is valid, it continues
    # If something is missing or wrong (like a negative income), marshmallow throws a `ValidationError` and I return `422` with a helpful errormessage instead of crashing
    except ValidationError as err: 
        return jsonify({"errors": err.messages}), 422
    
    # If validation passed, send the clean data to my ML model and return the result.
    # `result` will look like:
    #{
    #     "risk_tier": "Low",
    #     "confidence": 0.87
    #}
    result = run_prediction(data)
    return jsonify(result), 200
