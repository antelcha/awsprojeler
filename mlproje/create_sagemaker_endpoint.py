"""
SageMaker endpoint oluşturma scripti
"""
import boto3
import time
from datetime import datetime

def create_sagemaker_endpoint():
    """SageMaker training job'dan endpoint oluştur"""
    
    sagemaker = boto3.client('sagemaker')
    
    # En son training job'ı bul
    training_jobs = sagemaker.list_training_jobs(
        SortBy='CreationTime',
        SortOrder='Descending',
        MaxResults=1
    )
    
    if not training_jobs['TrainingJobSummaries']:
        print("❌ No training jobs found")
        return False
    
    latest_job = training_jobs['TrainingJobSummaries'][0]
    job_name = latest_job['TrainingJobName']
    
    print(f"📥 Using training job: {job_name}")
    print(f"Status: {latest_job['TrainingJobStatus']}")
    
    if latest_job['TrainingJobStatus'] != 'Completed':
        print("❌ Training job not completed yet")
        return False
    
    # Training job detaylarını al
    job_details = sagemaker.describe_training_job(TrainingJobName=job_name)
    model_s3_path = job_details['ModelArtifacts']['S3ModelArtifacts']
    
    print(f"Model S3 path: {model_s3_path}")
    
    # Unique names
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    model_name = f'house-price-model-{timestamp}'
    endpoint_config_name = f'house-price-config-{timestamp}'
    endpoint_name = 'house-price-endpoint'
    
    # IAM role (SageMaker execution role)
    role_arn = "arn:aws:iam::257394496046:role/SageMakerExecutionRole-HousePrice"
    
    try:
        # 1. Model oluştur
        print(f"🔄 Creating model: {model_name}")
        
        sagemaker.create_model(
            ModelName=model_name,
            PrimaryContainer={
                'Image': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.5-1',
                'ModelDataUrl': model_s3_path
            },
            ExecutionRoleArn=role_arn
        )
        print(f"✅ Model created: {model_name}")
        
        # 2. Endpoint configuration oluştur
        print(f"🔄 Creating endpoint configuration: {endpoint_config_name}")
        
        sagemaker.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    'VariantName': 'primary',
                    'ModelName': model_name,
                    'InitialInstanceCount': 1,
                    'InstanceType': 'ml.t2.medium',  # En ucuz instance
                    'InitialVariantWeight': 1.0
                }
            ]
        )
        print(f"✅ Endpoint configuration created: {endpoint_config_name}")
        
        # 3. Endpoint oluştur veya güncelle
        print(f"🔄 Creating/updating endpoint: {endpoint_name}")
        
        try:
            # Endpoint var mı kontrol et
            sagemaker.describe_endpoint(EndpointName=endpoint_name)
            
            # Varsa güncelle
            print(f"ℹ️ Endpoint exists, updating...")
            sagemaker.update_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=endpoint_config_name
            )
            
        except sagemaker.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                # Yoksa oluştur
                print(f"ℹ️ Endpoint doesn't exist, creating...")
                sagemaker.create_endpoint(
                    EndpointName=endpoint_name,
                    EndpointConfigName=endpoint_config_name
                )
            else:
                raise e
        
        # Endpoint'in hazır olmasını bekle
        print(f"⏳ Waiting for endpoint to be ready...")
        
        while True:
            response = sagemaker.describe_endpoint(EndpointName=endpoint_name)
            status = response['EndpointStatus']
            
            print(f"Endpoint status: {status}")
            
            if status == 'InService':
                print(f"✅ Endpoint is ready!")
                break
            elif status in ['Failed', 'OutOfService']:
                print(f"❌ Endpoint creation failed: {status}")
                return False
            
            time.sleep(30)  # 30 saniye bekle
        
        print("\n" + "=" * 60)
        print("✅ SageMaker Endpoint Setup Completed!")
        print(f"📋 Endpoint Name: {endpoint_name}")
        print(f"📋 Model Name: {model_name}")
        print(f"📋 Instance Type: ml.t2.medium")
        print(f"📋 Status: InService")
        print("=" * 60)
        print("\n🚀 Now you can use sagemaker_api.py!")
        print(f"python sagemaker_api.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create endpoint: {e}")
        return False

if __name__ == "__main__":
    create_sagemaker_endpoint() 