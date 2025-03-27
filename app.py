from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from auth import auth_bp  # Import auth routes

app = Flask(__name__)

# 🔥 MongoDB Connection (Change DB Name if needed)
app.config["MONGO_URI"] = "mongodb://localhost:27017/supermarket"
mongo = PyMongo(app)
CORS(app)  # Enable CORS for frontend requests

# 🔥 Collections
users_collection = mongo.db.users  # Store both admins & customers

# 🔥 Register Authentication Routes
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)

