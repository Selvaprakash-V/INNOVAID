from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

# MongoDB Connection URI (change if using MongoDB Atlas)
app.config["MONGO_URI"] = "mongodb://localhost:27017/supermarket"

mongo = PyMongo(app)  # Connect Flask to MongoDB
CORS(app)  # Enable CORS

@app.route("/")
def home():
    return {"message": "Supermarket API is connected to MongoDB!"}

if __name__ == "__main__":
    app.run(debug=True)
