from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
CORS(app)  # Enable CORS for frontend requests

@app.route("/")
def home():
    return {"message": "Supermarket API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
