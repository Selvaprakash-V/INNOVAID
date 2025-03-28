from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# ✅ MongoDB Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/supermarket_db"
mongo = PyMongo(app)

# ✅ Import auth_bp AFTER mongo is initialized
from auth_routes import auth_bp  # Import should be placed here to avoid circular import

# ✅ Register Authentication Routes
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
