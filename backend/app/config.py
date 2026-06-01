import os #Gives access to environment variables on the computer
from dotenv import load_dotenv

# Read a file called .env in the project and loads whatever's inside it as environment
# The .env file is where you'll store secrets like your database password
# stuff you never put directly in your code.
load_dotenv() 

# A python class that groups all your app settings together in one place.
# Flask will read from this class on startup
class Config:
    # Looks for a variable called `SECRET_KEY` in my `.env` file.
    # If it doesn't find one, it falls back to `dev-secret-key`.
    # Flask uses this to sign cookies and sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # The address of my MongoDB database.
    # When deployed, this will point to MongoDB Atlas in the cloud
    # For now it points to my local machine
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/creditrisk")
    
    # The secret key used to sign JWT login tokens.
    # If someone logs in, Flask uses this to generate their token
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
