# This file defines the rules for what data the frontend is allowed to send to your predict endpoint.
# Think of it as a bouncer at the door

# Schema - the base class you inherit from to create your own schema
# fields - defines what type each field should be (Float, Int, Stringm etc.)
# validate - adds extra 

from marshmallow import Schema, fields, validate

# A custom schema by inheriting from marshmallow's Schema.
class PredictSchema(Schema):
    annual_income = fields.Float(required=True)
    debt_to_income = fields.Float(required=True, validate=validate.Range(0,1))
    credit_history_months = fields.Int(required=True)
    num_late_payments = fields.Int(required=True)
    loan_amount = fields.Float(required=True)

# I used marshmallow to validate all incoming data before it reached the ML model, so the model always receives clean, correctly typed inputs.