"""
SageMaker role'ünün S3 policy'sini güncelleme scripti
"""
import boto3
import json

def update_s3_policy_for_sagemaker():
    """SageMaker role'ünün S3 policy'sini güncelle"""
    
    iam = boto3.client('iam')
    
    # Role ve policy adları
    role_name = 'SageMakerExecutionRole-HousePrice'
    policy_name = 'SageMakerS3Policy-Updated'
    
    # Güncellenmiş S3 policy - wildcard ile
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
                    "arn:aws:s3:::house-price-prediction-bucket*",
                    "arn:aws:s3:::house-price-prediction-bucket*/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:CreateBucket",
                    "s3:ListBucket",
                    "s3:ListAllMyBuckets"
                ],
                "Resource": "*"
            }
        ]
    }
    
    try:
        # Account ID al
        sts = boto3.client('sts')
        account_id = sts.get_caller_identity()['Account']
        
        print(f"🔄 Creating updated S3 policy: {policy_name}")
        
        # Yeni policy oluştur
        try:
            response = iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(s3_policy),
                Description='Updated S3 access policy for SageMaker with wildcard bucket names'
            )
            policy_arn = response['Policy']['Arn']
            print(f"✅ New S3 policy created: {policy_arn}")
        except iam.exceptions.EntityAlreadyExistsException:
            policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
            print(f"ℹ️ Policy already exists: {policy_arn}")
        
        # Policy'yi role'e ekle
        try:
            iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"✅ Attached updated S3 policy to {role_name}")
        except Exception as e:
            print(f"⚠️ Policy already attached or error: {e}")
        
        # Eski policy'yi kaldır (opsiyonel)
        try:
            old_policy_arn = f"arn:aws:iam::{account_id}:policy/SageMakerS3Policy-HousePrice"
            iam.detach_role_policy(
                RoleName=role_name,
                PolicyArn=old_policy_arn
            )
            print(f"✅ Removed old S3 policy")
        except Exception as e:
            print(f"ℹ️ Old policy not found or already removed: {e}")
        
        print("\n" + "=" * 60)
        print("✅ S3 Policy update completed!")
        print(f"📋 SageMaker role now has access to all house-price buckets")
        print("📋 Try SageMaker training again")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update S3 policy: {e}")
        return False

if __name__ == "__main__":
    update_s3_policy_for_sagemaker() 