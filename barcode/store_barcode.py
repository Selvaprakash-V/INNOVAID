from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change if using a remote server
db = client["barcode_db"]  # Database Name
collection = db["products"]  # Collection Name

# Product details
product_data = {
    "barcode": "1234567890123",
    "product": "Bourbon",
    "brand": "Britannia",
    "expiry_date": "2025-06-10"
}

# Insert data into MongoDB
collection.insert_one(product_data)

print("Data stored successfully in MongoDB!")
