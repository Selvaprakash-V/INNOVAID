from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app import mongo  # ✅ Import MongoDB instance from app.py

# ✅ Create Blueprint for Auth
auth_bp = Blueprint("auth", __name__)

# ✅ Secret Key for JWT Authentication
SECRET_KEY = "super_secret_key"

# 🚀 1️⃣ ADMIN SIGNUP (Directly Logs in & Redirects to Dashboard)
@auth_bp.route("/signup/admin", methods=["POST"])
def signup_admin():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    shop_name = data.get("shop_name")

    if not email or not password or not shop_name:
        return jsonify({"error": "All fields are required"}), 400

    # ✅ Check if admin already exists
    if mongo.db.administrators.find_one({"email": email}):
        return jsonify({"error": "Admin already registered"}), 400

    # ✅ Hash Password & Store in MongoDB
    hashed_password = generate_password_hash(password)
    mongo.db.administrators.insert_one({
        "email": email,
        "password": hashed_password,
        "shop_name": shop_name,
        "created_at": datetime.datetime.utcnow()
    })

    # ✅ Automatically Generate JWT Token (Admin Doesn't Need to Login Again)
    token = jwt.encode(
        {"email": email, "role": "admin", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY, algorithm="HS256"
    )

    return jsonify({"message": "Admin registered successfully", "token": token, "role": "admin"}), 201

# 🚀 2️⃣ CUSTOMER SIGNUP (Redirects to Sign-in Page)
@auth_bp.route("/signup/customer", methods=["POST"])
def signup_customer():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "All fields are required"}), 400

    # ✅ Check if customer already exists
    if mongo.db.customers.find_one({"email": email}):
        return jsonify({"error": "Customer already registered"}), 400

    # ✅ Hash Password & Store in MongoDB
    hashed_password = generate_password_hash(password)
    mongo.db.customers.insert_one({
        "email": email,
        "password": hashed_password,
        "name": name,
        "created_at": datetime.datetime.utcnow()
    })

    return jsonify({"message": "Customer registered successfully. Please login."}), 201

# 🚀 3️⃣ LOGIN (Admin & Customer)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    # ✅ Check if user exists in Admin Database
    user = mongo.db.administrators.find_one({"email": email})
    role = "admin"

    # ✅ If not found in Admin DB, check Customer Database
    if not user:
        user = mongo.db.customers.find_one({"email": email})
        role = "customer"

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Generate JWT Token
    token = jwt.encode(
        {"email": email, "role": role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY, algorithm="HS256"
    )

    return jsonify({"message": "Login successful", "token": token, "role": role}), 200
