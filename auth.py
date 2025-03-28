from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from app import mongo

SECRET_KEY = "supersecretkey"  # Change this in production

auth_bp = Blueprint("auth", __name__)

# Administrator Signup
@auth_bp.route("/signup/admin", methods=["POST"])
def signup_admin():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    shop_name = data.get("shop_name")

    if not email or not password or not shop_name:
        return jsonify({"error": "Missing fields!"}), 400

    # Check if admin already exists
    if mongo.db.administrators.find_one({"email": email}):
        return jsonify({"error": "Admin already exists!"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Store admin in MongoDB
    mongo.db.administrators.insert_one({
        "email": email,
        "password": hashed_password,
        "shop_name": shop_name,
        "created_at": datetime.datetime.utcnow()
    })

    return jsonify({"message": "Administrator registered successfully!"}), 201


# Customer Signup
@auth_bp.route("/signup/customer", methods=["POST"])
def signup_customer():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "Missing fields!"}), 400

    # Check if customer already exists
    if mongo.db.customers.find_one({"email": email}):
        return jsonify({"error": "Customer already exists!"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Store customer in MongoDB
    mongo.db.customers.insert_one({
        "email": email,
        "password": hashed_password,
        "name": name,
        "created_at": datetime.datetime.utcnow()
    })

    return jsonify({"message": "Customer registered successfully!"}), 201


# Login API (Works for both Admin & Customer)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    # Check in administrators collection
    user = mongo.db.administrators.find_one({"email": email})
    role = "admin"

    # If not found, check in customers collection
    if not user:
        user = mongo.db.customers.find_one({"email": email})
        role = "customer"

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode({
        "email": email,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Token expires in 2 hours
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login successful!", "token": token, "role": role}), 200
