import os

class Config:
    MONGO_URI = "mongodb://localhost:27017/supermarket_db"  # Local MongoDB database
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
