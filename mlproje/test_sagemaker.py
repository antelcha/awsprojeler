#!/usr/bin/env python3
"""
SageMaker training test scripti
"""
from housing_price_model import HousePricePredictor

def test_sagemaker():
    """SageMaker training'i test et"""
    print("🧪 Testing SageMaker training...")
    
    # Model oluştur
    predictor = HousePricePredictor()
    
    # Veriyi hazırla
    X, y = predictor.load_and_prepare_data()
    train_data = predictor.prepare_for_sagemaker(X, y)
    predictor.create_sagemaker_training_script()
    
    # SageMaker training test et
    print("\n🚀 Testing SageMaker training...")
    sagemaker_estimator = predictor.train_sagemaker_model()
    
    if sagemaker_estimator:
        print("✅ SageMaker training started successfully!")
        return True
    else:
        print("❌ SageMaker training failed")
        return False

if __name__ == "__main__":
    test_sagemaker() 