"""
House Price Prediction with XGBoost on AWS SageMaker
Simple and AWS-focused approach
"""
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import os

# AWS imports - will handle gracefully if not available
try:
    import boto3
    import sagemaker
    from sagemaker.xgboost import XGBoost
    from sagemaker import get_execution_role
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False
    print("⚠️ AWS libraries not available. Running in local mode only.")

class HousePricePredictor:
    """AWS SageMaker ile XGBoost House Price Prediction"""
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_names = None
        
        # AWS setup
        if AWS_AVAILABLE:
            try:
                self.sagemaker_session = sagemaker.Session()
                self.role = None  # Will be set later
                self.bucket = 'house-price-prediction-bucket'  # S3 bucket
                print("✅ AWS SageMaker available")
            except Exception as e:
                print(f"⚠️ AWS SageMaker session failed: {e}")
                self.sagemaker_session = None
        else:
            self.sagemaker_session = None
    
    def setup_aws_credentials(self):
        """AWS credentials setup"""
        print("🔑 AWS Credentials Setup")
        print("=" * 40)
        
        if not AWS_AVAILABLE:
            print("❌ AWS libraries not installed.")
            print("Install with: pip install boto3 sagemaker")
            return False
        
        # Check if AWS credentials exist
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            
            if credentials is None:
                print("❌ AWS credentials not found.")
                print("\nSetup options:")
                print("1. AWS CLI: aws configure")
                print("2. Environment variables:")
                print("   export AWS_ACCESS_KEY_ID=your_access_key")
                print("   export AWS_SECRET_ACCESS_KEY=your_secret_key")
                print("   export AWS_DEFAULT_REGION=us-east-1")
                print("3. IAM role (if running on EC2/SageMaker)")
                return False
            else:
                print(f"✅ AWS credentials found")
                print(f"Region: {session.region_name}")
                
                # Check SageMaker permissions
                try:
                    sagemaker_client = boto3.client('sagemaker')
                    sagemaker_client.list_training_jobs(MaxResults=1)
                    print("✅ SageMaker permissions OK")
                except Exception as e:
                    print(f"⚠️ SageMaker permissions issue: {e}")
                
                return True
                
        except Exception as e:
            print(f"❌ AWS setup error: {e}")
            return False
    
    def create_s3_bucket(self):
        """S3 bucket oluştur"""
        if not AWS_AVAILABLE:
            return False
            
        try:
            s3_client = boto3.client('s3')
            session = boto3.Session()
            region = session.region_name
            
            # Check if bucket exists
            try:
                s3_client.head_bucket(Bucket=self.bucket)
                print(f"✅ S3 bucket '{self.bucket}' already exists")
                return True
            except:
                # Create bucket
                if region == 'us-east-1':
                    # us-east-1 doesn't need location constraint
                    s3_client.create_bucket(Bucket=self.bucket)
                else:
                    # Other regions need location constraint
                    s3_client.create_bucket(
                        Bucket=self.bucket,
                        CreateBucketConfiguration={
                            'LocationConstraint': region
                        }
                    )
                print(f"✅ S3 bucket '{self.bucket}' created in {region}")
                return True
                
        except Exception as e:
            print(f"❌ S3 bucket creation failed: {e}")
            # Try different bucket name
            try:
                import random
                new_bucket = f"{self.bucket}-{random.randint(1000, 9999)}"
                print(f"🔄 Trying with bucket name: {new_bucket}")
                
                if region == 'us-east-1':
                    s3_client.create_bucket(Bucket=new_bucket)
                else:
                    s3_client.create_bucket(
                        Bucket=new_bucket,
                        CreateBucketConfiguration={
                            'LocationConstraint': region
                        }
                    )
                
                self.bucket = new_bucket
                print(f"✅ S3 bucket '{new_bucket}' created")
                return True
            except Exception as e2:
                print(f"❌ Failed to create bucket with new name: {e2}")
                return False
        
    def load_and_prepare_data(self, data_path='data/Housing-1.csv'):
        """Veriyi yükle ve hazırla"""
        print("📊 Loading and preparing data...")
        
        # Veriyi yükle
        df = pd.read_csv(data_path)
        print(f"Data shape: {df.shape}")
        
        # Target ve features ayır
        target = 'price'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Kategorik değişkenleri encode et
        categorical_columns = X.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.encoders[col] = le
            print(f"Encoded {col}: {le.classes_}")
        
        self.feature_names = X.columns.tolist()
        print(f"Features: {self.feature_names}")
        
        return X, y
    
    def train_local_model(self, X, y, test_size=0.2):
        """Local XGBoost modelini eğit"""
        print("🚀 Training local XGBoost model...")
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # XGBoost model
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        # Eğitim
        self.model.fit(X_train, y_train)
        
        # Değerlendirme
        y_pred = self.model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        print(f"📈 Model Performance:")
        print(f"  RMSE: {rmse:,.2f}")
        print(f"  R² Score: {r2:.3f}")
        print(f"  Mean Actual Price: {y_test.mean():,.2f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\n🔍 Top 5 Important Features:")
        print(feature_importance.head())
        
        return X_train, X_test, y_train, y_test, y_pred
    
    def prepare_for_sagemaker(self, X, y):
        """SageMaker için veriyi hazırla"""
        print("☁️ Preparing data for SageMaker...")
        
        # SageMaker XGBoost format: target + features
        train_data = pd.concat([y, X], axis=1)
        
        # CSV olarak kaydet
        os.makedirs('sagemaker_data', exist_ok=True)
        train_data.to_csv('sagemaker_data/train.csv', header=False, index=False)
        
        print("Data saved for SageMaker training")
        return train_data
    
    def get_sagemaker_role(self):
        """SageMaker execution role al"""
        if not AWS_AVAILABLE:
            return None
        
        # Direkt olarak oluşturduğumuz role'ü kullan
        role_arn = "arn:aws:iam::257394496046:role/SageMakerExecutionRole-HousePrice"
        
        try:
            # Role'ün var olup olmadığını kontrol et
            iam = boto3.client('iam')
            iam.get_role(RoleName='SageMakerExecutionRole-HousePrice')
            print(f"✅ Using SageMaker role: {role_arn}")
            return role_arn
        except Exception as e:
            print(f"❌ SageMaker role not found: {e}")
            return None
    
    def train_sagemaker_model(self, train_data_path='sagemaker_data/train.csv'):
        """SageMaker'da XGBoost modelini eğit"""
        print("🚀 Training model on SageMaker...")
        
        if not AWS_AVAILABLE or not self.sagemaker_session:
            print("❌ AWS SageMaker not available")
            return None
        
        # Get role
        self.role = self.get_sagemaker_role()
        if not self.role:
            print("❌ Cannot proceed without SageMaker role")
            return None
        
        # S3 bucket check
        if not self.create_s3_bucket():
            print("❌ Cannot proceed without S3 bucket")
            return None
        
        try:
            # S3'e veri yükle
            s3_input_train = self.sagemaker_session.upload_data(
                path=train_data_path,
                bucket=self.bucket,
                key_prefix='xgboost-train'
            )
            print(f"✅ Data uploaded to: {s3_input_train}")
            
            # XGBoost estimator
            xgb_estimator = XGBoost(
                entry_point='train.py',  # Training script
                role=self.role,
                instance_type='ml.m4.xlarge',
                instance_count=1,
                framework_version='1.5-1',
                py_version='py3',
                hyperparameters={
                    'objective': 'reg:squarederror',
                    'num_round': 100,
                    'max_depth': 6,
                    'eta': 0.1,
                    'subsample': 0.8,
                    'colsample_bytree': 0.8
                }
            )
            
            # Training job başlat
            print("🚀 Starting SageMaker training job...")
            xgb_estimator.fit({'train': s3_input_train})
            
            print("✅ SageMaker training completed!")
            return xgb_estimator
            
        except Exception as e:
            print(f"❌ SageMaker training failed: {e}")
            return None
    
    def create_sagemaker_training_script(self):
        """SageMaker training script oluştur"""
        training_script = '''
import argparse
import os
import pandas as pd
import xgboost as xgb
import joblib

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_round', type=int, default=100)
    parser.add_argument('--max_depth', type=int, default=6)
    parser.add_argument('--eta', type=float, default=0.1)
    parser.add_argument('--subsample', type=float, default=0.8)
    parser.add_argument('--colsample_bytree', type=float, default=0.8)
    parser.add_argument('--objective', type=str, default='reg:squarederror')
    
    parser.add_argument('--model_dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Veriyi yükle
    train_data = pd.read_csv(os.path.join(args.train, 'train.csv'), header=None)
    
    # Target ve features
    y = train_data.iloc[:, 0]
    X = train_data.iloc[:, 1:]
    
    # XGBoost training
    dtrain = xgb.DMatrix(X, label=y)
    
    params = {
        'objective': args.objective,
        'max_depth': args.max_depth,
        'eta': args.eta,
        'subsample': args.subsample,
        'colsample_bytree': args.colsample_bytree
    }
    
    model = xgb.train(params, dtrain, num_boost_round=args.num_round)
    
    # Model kaydet
    model.save_model(os.path.join(args.model_dir, 'xgboost-model'))

if __name__ == '__main__':
    main()
'''
        
        with open('train.py', 'w') as f:
            f.write(training_script)
        
        print("✅ SageMaker training script created: train.py")
    
    def predict(self, house_features):
        """Ev fiyatı tahmin et"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Features'ı DataFrame'e çevir
        if isinstance(house_features, dict):
            df = pd.DataFrame([house_features])
        else:
            df = pd.DataFrame(house_features)
        
        # Kategorik değişkenleri encode et
        for col, encoder in self.encoders.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col])
        
        # Tahmin
        price_prediction = self.model.predict(df)
        
        return price_prediction[0] if len(price_prediction) == 1 else price_prediction
    
    def save_model(self, path='model'):
        """Modeli kaydet"""
        os.makedirs(path, exist_ok=True)
        
        # XGBoost model
        joblib.dump(self.model, f'{path}/xgboost_model.pkl')
        
        # Encoders
        joblib.dump(self.encoders, f'{path}/encoders.pkl')
        
        # Feature names
        with open(f'{path}/feature_names.json', 'w') as f:
            json.dump(self.feature_names, f)
        
        print(f"✅ Model saved to {path}/")
    
    def load_model(self, path='model'):
        """Modeli yükle"""
        self.model = joblib.load(f'{path}/xgboost_model.pkl')
        self.encoders = joblib.load(f'{path}/encoders.pkl')
        
        with open(f'{path}/feature_names.json', 'r') as f:
            self.feature_names = json.load(f)
        
        print(f"✅ Model loaded from {path}/")


def main():
    """Ana fonksiyon"""
    print("🏠 House Price Prediction with XGBoost + AWS SageMaker")
    print("=" * 60)
    
    # Model oluştur
    predictor = HousePricePredictor()
    
    # AWS setup kontrol et
    aws_ready = predictor.setup_aws_credentials()
    

    
    # SageMaker için hazırla
    train_data = predictor.prepare_for_sagemaker(X, y)
    
    # SageMaker training script oluştur
    predictor.create_sagemaker_training_script()
    
    # AWS üzerinde eğit (eğer hazırsa)
    if aws_ready:
        print("\n" + "="*50)
        print("🚀 AWS SAGEMAKER TRAINING")
        print("="*50)
        
        user_input = input("SageMaker'da eğitim yapmak istiyor musunuz? (y/n): ")
        if user_input.lower() == 'y':
            sagemaker_estimator = predictor.train_sagemaker_model()
        else:
            print("⏭️ SageMaker training skipped")
    
    # Modeli kaydet
    predictor.save_model()
    
    # Örnek tahmin
    print("\n🔮 Example Prediction:")
    sample_house = {
        'area': 7420,
        'bedrooms': 4,
        'bathrooms': 2,
        'stories': 3,
        'mainroad': 'yes',
        'guestroom': 'no',
        'basement': 'no',
        'hotwaterheating': 'no',
        'airconditioning': 'yes',
        'parking': 2,
        'prefarea': 'yes',
        'furnishingstatus': 'furnished'
    }
    
    predicted_price = predictor.predict(sample_house)
    print(f"Predicted price: ₹{predicted_price:,.2f}")
    
    print("\n✅ Model ready!")
    print("\nNext steps for AWS deployment:")
    print("1. ✅ Model trained and saved")
    print("2. ✅ SageMaker training script created")
    print("3. 🔄 Deploy to SageMaker endpoint")
    print("4. 🔄 Create API Gateway + Lambda for serving")


if __name__ == "__main__":
    main() 