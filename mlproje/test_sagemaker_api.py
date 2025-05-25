"""
SageMaker API Test Script
"""
import requests
import json

def test_sagemaker_api():
    """SageMaker API'yi test et"""
    
    base_url = "http://localhost:8001"
    
    # Test data
    test_house = {
        "area": 7420,
        "bedrooms": 4,
        "bathrooms": 1,
        "stories": 3,
        "mainroad": "yes",
        "guestroom": "no",
        "basement": "no",
        "hotwaterheating": "no",
        "airconditioning": "yes",
        "parking": 2,
        "prefarea": "yes",
        "furnishingstatus": "furnished"
    }
    
    # Luxury house test
    luxury_house = {
        "area": 9000,
        "bedrooms": 5,
        "bathrooms": 3,
        "stories": 4,
        "mainroad": "yes",
        "guestroom": "yes",
        "basement": "yes",
        "hotwaterheating": "yes",
        "airconditioning": "yes",
        "parking": 3,
        "prefarea": "yes",
        "furnishingstatus": "furnished"
    }
    
    print("🧪 Testing SageMaker API...")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Health check: FAILED")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    print("\n" + "-" * 50)
    
    # Test 2: Standard house prediction
    try:
        response = requests.post(f"{base_url}/predict", json=test_house)
        if response.status_code == 200:
            result = response.json()
            print("✅ Standard House Prediction: PASSED")
            print(f"   Predicted Price: {result['formatted_price']}")
            print(f"   Model Type: {result['model_type']}")
        else:
            print(f"❌ Standard house prediction failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Standard house prediction failed: {e}")
        return False
    
    print("\n" + "-" * 50)
    
    # Test 3: Luxury house prediction
    try:
        response = requests.post(f"{base_url}/predict", json=luxury_house)
        if response.status_code == 200:
            result = response.json()
            print("✅ Luxury House Prediction: PASSED")
            print(f"   Predicted Price: {result['formatted_price']}")
            print(f"   Model Type: {result['model_type']}")
        else:
            print(f"❌ Luxury house prediction failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Luxury house prediction failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All SageMaker API tests PASSED!")
    print("🚀 SageMaker endpoint is working correctly!")
    return True

if __name__ == "__main__":
    test_sagemaker_api() 