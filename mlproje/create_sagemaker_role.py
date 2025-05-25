"""
SageMaker için IAM Role oluşturma scripti
"""
import boto3
import json
import time

def create_sagemaker_role():
    """SageMaker execution role oluştur"""
    
    iam = boto3.client('iam')
    
    # Role adı
    role_name = 'SageMakerExecutionRole-HousePrice'
    
    # Trust policy - SageMaker'ın bu role'ü kullanmasına izin ver
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "sagemaker.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        print(f"🔄 Creating IAM role: {role_name}")
        
        # Role oluştur
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='SageMaker execution role for house price prediction',
            Path='/',
        )
        
        role_arn = response['Role']['Arn']
        print(f"✅ Role created: {role_arn}")
        
        # Managed policies ekle
        managed_policies = [
            'arn:aws:iam::aws:policy/AmazonSageMakerFullAccess',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess',
            'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly'
        ]
        
        for policy_arn in managed_policies:
            try:
                iam.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
                print(f"✅ Attached policy: {policy_arn}")
            except Exception as e:
                print(f"⚠️ Failed to attach {policy_arn}: {e}")
        
        # Biraz bekle role'ün propagate olması için
        print("⏳ Waiting for role propagation...")
        time.sleep(10)
        
        return role_arn
        
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"ℹ️ Role {role_name} already exists")
        
        # Mevcut role'ün ARN'ini al
        try:
            response = iam.get_role(RoleName=role_name)
            role_arn = response['Role']['Arn']
            print(f"✅ Using existing role: {role_arn}")
            return role_arn
        except Exception as e:
            print(f"❌ Failed to get existing role: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to create role: {e}")
        return None

def create_s3_bucket_policy():
    """S3 bucket için custom policy oluştur"""
    
    iam = boto3.client('iam')
    
    # Account ID al
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    
    policy_name = 'SageMakerS3Policy-HousePrice'
    
    # S3 policy
    s3_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::house-price-prediction-bucket",
                    "arn:aws:s3:::house-price-prediction-bucket/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:CreateBucket",
                    "s3:ListBucket"
                ],
                "Resource": "*"
            }
        ]
    }
    
    try:
        print(f"🔄 Creating S3 policy: {policy_name}")
        
        response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(s3_policy),
            Description='S3 access policy for SageMaker house price prediction'
        )
        
        policy_arn = response['Policy']['Arn']
        print(f"✅ S3 policy created: {policy_arn}")
        return policy_arn
        
    except iam.exceptions.EntityAlreadyExistsException:
        # Policy zaten var
        policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
        print(f"ℹ️ Policy {policy_name} already exists: {policy_arn}")
        return policy_arn
        
    except Exception as e:
        print(f"⚠️ Failed to create S3 policy: {e}")
        return None

def setup_sagemaker_permissions():
    """Tam SageMaker setup"""
    
    print("🚀 Setting up SageMaker IAM permissions...")
    print("=" * 60)
    
    # Account info
    try:
        sts = boto3.client('sts')
        caller_info = sts.get_caller_identity()
        print(f"Account ID: {caller_info['Account']}")
        print(f"User ARN: {caller_info['Arn']}")
        print()
    except Exception as e:
        print(f"⚠️ Could not get caller identity: {e}")
    
    # S3 policy oluştur
    s3_policy_arn = create_s3_bucket_policy()
    
    # SageMaker role oluştur
    role_arn = create_sagemaker_role()
    
    if role_arn:
        # S3 policy'yi role'e ekle
        if s3_policy_arn:
            try:
                iam = boto3.client('iam')
                iam.attach_role_policy(
                    RoleName='SageMakerExecutionRole-HousePrice',
                    PolicyArn=s3_policy_arn
                )
                print(f"✅ Attached S3 policy to role")
            except Exception as e:
                print(f"⚠️ Failed to attach S3 policy: {e}")
        
        print("\n" + "=" * 60)
        print("✅ SageMaker IAM setup completed!")
        print(f"📋 Role ARN: {role_arn}")
        print(f"📋 Copy this ARN to your housing_price_model.py")
        print("=" * 60)
        
        return role_arn
    else:
        print("❌ Failed to setup SageMaker role")
        return None

if __name__ == "__main__":
    setup_sagemaker_permissions() 