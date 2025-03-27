from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app import mongo, app

auth_bp = Blueprint("auth", __name__)

# Secret Key for JWT (Use .env for security in production)
SECRET_KEY = "supersecretkey"

# 🔥 Signup Route
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # "admin" or "customer"

    if not email or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Create user document
    user_data = {
        "email": email,
        "password": hashed_password,
        "role": role
    }

    # If admin, add shop_name
    if role == "admin":
        shop_name = data.get("shop_name", "")
        user_data["shop_name"] = shop_name

    # Insert into MongoDB
    mongo.db.users.insert_one(user_data)

    return jsonify({"message": f"{role.capitalize()} registered successfully!"}), 201


# 🔥 Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    # Check if user exists
    user = mongo.db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode({
        "email": email,
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # 2-hour expiry
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login successful!", "token": token, "role": user["role"]}), 200
