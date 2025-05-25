"""
SageMaker endpoint kullanan FastAPI
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
import numpy as np
from typing import Dict, Any
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from contextlib import asynccontextmanager

# SageMaker client
sagemaker_runtime = boto3.client('sagemaker-runtime')
ENDPOINT_NAME = 'house-price-endpoint'  # SageMaker endpoint adı

# Encoders'ı local'den yükle (preprocessing için)
encoders = None

def load_encoders():
    """Preprocessing için encoders'ı yükle"""
    global encoders
    try:
        encoders = joblib.load('model/encoders.pkl')
        print("✅ Encoders loaded for SageMaker preprocessing")
        return True
    except Exception as e:
        print(f"❌ Failed to load encoders: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not load_encoders():
        raise RuntimeError("Failed to load encoders")
    yield
    # Shutdown - cleanup if needed

# Initialize FastAPI
app = FastAPI(
    title="🏠 House Price Prediction API (SageMaker)",
    description="SageMaker endpoint ile house price prediction",
    version="2.0.0",
    lifespan=lifespan
)

# Request model
class HouseFeatures(BaseModel):
    area: int
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str
    guestroom: str
    basement: str
    hotwaterheating: str
    airconditioning: str
    parking: int
    prefarea: str
    furnishingstatus: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "🏠 House Price Prediction API (SageMaker)",
        "status": "healthy",
        "model_type": "sagemaker_endpoint",
        "endpoint": ENDPOINT_NAME
    }

@app.post("/predict")
async def predict_price(house: HouseFeatures):
    """SageMaker endpoint ile tahmin yap"""
    
    try:
        # Convert to DataFrame ve preprocess
        house_dict = house.model_dump()
        df = pd.DataFrame([house_dict])
        
        # Encode categorical variables
        for col, encoder in encoders.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col])
        
        # SageMaker format (CSV without header)
        csv_data = df.to_csv(header=False, index=False)
        
        # SageMaker endpoint'e inference request
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='text/csv',
            Body=csv_data
        )
        
        # Response'u parse et
        result = response['Body'].read().decode()
        prediction = float(result.strip())
        
        return {
            "predicted_price": prediction,
            "currency": "INR",
            "formatted_price": f"₹{prediction:,.2f}",
            "features_used": house_dict,
            "model_type": "sagemaker_endpoint",
            "model_version": "2.0.0"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SageMaker prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SageMaker House Price Prediction API...")
    uvicorn.run(app, host="0.0.0.0", port=8001) 