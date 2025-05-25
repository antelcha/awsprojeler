import boto3
import os

# Credentials set et


sagemaker = boto3.client('sagemaker')

try:
    response = sagemaker.describe_endpoint(EndpointName='house-price-endpoint')
    print(f"🔍 Endpoint Status: {response['EndpointStatus']}")
    print(f"📅 Creation Time: {response['CreationTime']}")
    
    if response['EndpointStatus'] == 'InService':
        print("✅ Endpoint is READY! You can now use sagemaker_api.py")
    elif response['EndpointStatus'] == 'Creating':
        print("⏳ Endpoint is still creating... Please wait.")
    else:
        print(f"⚠️ Endpoint status: {response['EndpointStatus']}")
        
except Exception as e:
    print(f"❌ Error: {e}") 