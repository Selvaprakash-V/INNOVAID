from flask_pymongo import PyMongo

def get_product_model(mongo):
    return mongo.db.products  # MongoDB collection for products
hh