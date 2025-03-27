import streamlit as st
import pandas as pd
import datetime
import torch
import torchvision.transforms as transforms
from PIL import Image

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("supermarket_data_full_1000_entries_final.csv")
    print("Columns in CSV:", df.columns.tolist())  # Debugging: check actual columns
    return df

data = load_data()

def get_status_color(expiry_date):
    today = datetime.date.today()
    try:
        expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid Date Format", "⚠️"

    days_left = (expiry_date - today).days
    
    if days_left < 0:
        return "Expired", "🔴 Red"
    elif days_left <= 30:
        return "Expires Soon", "🟡 Yellow"
    else:
        return "Valid", "🟢 Green"

# PyTorch Model for Barcode Detection (Placeholder Model)
class BarcodeDetector(torch.nn.Module):
    def __init__(self):
        super(BarcodeDetector, self).__init__()
        self.model = torch.nn.Identity()  # Replace with actual trained model

    def forward(self, x):
        return self.model(x)

model = BarcodeDetector()

def decode_barcode_pytorch(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)  # Add batch dimension
    output = model(image)  # Placeholder inference
    return None  # Replace with actual barcode extraction logic

# Streamlit UI
st.title("📦 Expiry Date Scanner & Predictor (PyTorch)")

uploaded_image = st.file_uploader("Upload Barcode Image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    barcode = decode_barcode_pytorch(image)
    
    if barcode:
        st.success(f"Scanned Barcode: {barcode}")
        product_info = data[data["Barcode"].astype(str) == str(barcode)]
        
        if not product_info.empty:
            product = product_info.iloc[0]
            status, color = get_status_color(str(product["Expiry Date"]))
            
            st.write(f"**Product:** {product['Product']}")
            st.write(f"**Brand:** {product['Brand']}")
            st.write(f"**Deploy Date:** {product['Deploy Date']}")
            st.write(f"**Expiry Date:** {product['Expiry Date']}")
            st.write(f"**Status:** {status} {color}")
        else:
            st.error("Product not found in database!")
    else:
        st.error("No barcode detected! Try a clearer image.")
