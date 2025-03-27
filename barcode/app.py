from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this for security
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Local MongoDB connection
db = client["user_db"]
users = db["users"]

# 📌 API to Register a User
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully!"}), 201

# 📌 API to Login a User
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username})

    if user and bcrypt.check_password_hash(user["password"], password):
        access_token = create_access_token(identity=username)
        return jsonify({"message": "Login successful!", "token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# 📌 Protected Route (Requires Authentication)
@app.route('/profile', methods=['GET'])
def profile():
    return jsonify({"message": "Welcome to your profile!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
