import requests

barcode = "1234567890123"
api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

response = requests.get(api_url)
data = response.json()

if "product" in data:
    product_name = data["product"]["product_name"]
    brand = data["product"]["brands"]
    expiry_date = data["product"].get("expiration_date", "Not Available")
    print(f"Product: {product_name}, Brand: {brand}, Expiry: {expiry_date}")
else:
    print("Product not found!")
