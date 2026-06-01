# This folder is a python package
# Create a Flask app, load its settings, connect the database and JWT, 
# register the routes, and return it ready to use.

from flask import Flask # The core web framework
from flask_jwt_extended import JWTManager # Handles login tokens
from flask_pymongo import PyMongo # connects to MongoDB
from flask_cors import CORS

# Creating empty instances of both tools.
mongo = PyMongo()
jwt = JWTManager()

# A function that builds and returns my Flask app. 
# This pattern is called an "application factory"
# Instead of creating the app directly, we wrap it in a function
# This makes testing easier later.
def create_app():
    # Actually creates the Flask app.
    # `__name__` tells Flask the name of the current file
    # so it knows where to look for templates and static files
    app = Flask(__name__)

    # Loads all the settings from `config.py`
    app.config.from_object("app.config.Config")

    # Connects MongoDB and JWT to my app
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Impors the two route files
    from app.routes.auth import auth_bp
    from app.routes.predict import predict_bp
    # Registers the routes with my app.
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(predict_bp, url_prefix="/api/v1")

    return app 