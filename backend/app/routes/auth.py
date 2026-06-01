# This file handles register and login - two endpoints that let users create an account and sign in



# Blueprint - a way to group related routes together(all auth routes in one file)
# request - lets me read the data the frontend sends me
# jsonify - converts Python dictionaries to JSON to send back to the frontend
# create_access_token - generate a JWT login token
# mongo - the database connection
# bcrypt - a library that hashes passwords (truns them into unreadable scrambled text so you never store raw passwords)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import mongo
import bcrypt

# Creates a Blueprint called "auth". 
# Like a mini Flask app that only handles auth routes
auth_bp = Blueprint("auth", __name__)

# Creates the endpoint `/api/v1/auth/register`
# It only accepts POST requests because the frontend is sending data(email + password)
@auth_bp.route("/register", methods=["POST"])
def register():
    # Reads the JSON the frontend sent.
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Checks MongoDB - does this email already exist?
    # 409 means "conflict" in HTTP status codes
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 409
    
    # Takes the raw password and scrambles it
    # Never store the real psw, only this hash
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # Saves the new user to MongoDB with their email and hashed password
    mongo.db.users.insert_one({"email": email, "password": hashed})

    # 201 means "created" in HTTP status codes
    return jsonify({"message": "User created successfully"}), 201

# Same as register, but for login this time.
@auth_bp.route("/login", methods=["POST"])

def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})
    # 401 means unauthorized
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # If everything checks out, generate a JWT token tied to this user's email and send it back.
    # The frontend will store this token and send it with every future request to prove the user is loggin in
    token = create_access_token(identity=email)
    return jsonify({"token": token}), 200