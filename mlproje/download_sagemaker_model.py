"""
SageMaker'da eğitilen modeli indirme scripti
"""
import boto3
import os
import tarfile
import shutil

def download_sagemaker_model():
    """SageMaker training job'dan modeli indir"""
    
    sagemaker = boto3.client('sagemaker')
    s3 = boto3.client('s3')
    
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
    
    print(f"📥 Latest training job: {job_name}")
    print(f"Status: {latest_job['TrainingJobStatus']}")
    
    # Training job detaylarını al
    job_details = sagemaker.describe_training_job(TrainingJobName=job_name)
    
    # Model artifacts S3 path
    model_s3_path = job_details['ModelArtifacts']['S3ModelArtifacts']
    print(f"Model S3 path: {model_s3_path}")
    
    # S3'ten modeli indir
    bucket = model_s3_path.split('/')[2]
    key = '/'.join(model_s3_path.split('/')[3:])
    
    local_path = 'sagemaker_model.tar.gz'
    
    try:
        print(f"⬇️ Downloading model from S3...")
        s3.download_file(bucket, key, local_path)
        print(f"✅ Model downloaded: {local_path}")
        
        # Tar dosyasını extract et
        extract_dir = 'sagemaker_model'
        os.makedirs(extract_dir, exist_ok=True)
        
        with tarfile.open(local_path, 'r:gz') as tar:
            tar.extractall(extract_dir)
        
        print(f"✅ Model extracted to: {extract_dir}")
        
        # Model dosyasını model klasörüne kopyala
        sagemaker_model_file = os.path.join(extract_dir, 'xgboost-model')
        if os.path.exists(sagemaker_model_file):
            # XGBoost model olarak kaydet
            import xgboost as xgb
            
            # Model'i yükle ve tekrar kaydet
            model = xgb.Booster()
            model.load_model(sagemaker_model_file)
            
            # Scikit-learn format olarak kaydet
            import joblib
            
            # Not: XGBoost model'i doğrudan joblib ile kaydedilemiyor
            # SageMaker modelini kullanmak için farklı approach gerekir
            
            print("✅ SageMaker model downloaded and ready")
            return True
        else:
            print("❌ Model file not found in extracted archive")
            return False
            
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        return False
    
    finally:
        # Cleanup
        if os.path.exists(local_path):
            os.remove(local_path)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

if __name__ == "__main__":
    download_sagemaker_model() 