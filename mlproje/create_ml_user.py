"""
ML projesi için yeni IAM user oluşturma scripti
"""
import boto3
import json
import time

def create_ml_user():
    """ML projesi için IAM user oluştur"""
    
    iam = boto3.client('iam')
    
    # User adı
    username = 'ml-house-price-user'
    
    try:
        print(f"🔄 Creating IAM user: {username}")
        
        # User oluştur
        response = iam.create_user(
            UserName=username,
            Path='/',
        )
        
        user_arn = response['User']['Arn']
        print(f"✅ User created: {user_arn}")
        
        # Managed policies ekle
        managed_policies = [
            'arn:aws:iam::aws:policy/AmazonSageMakerFullAccess',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess',
            'arn:aws:iam::aws:policy/IAMReadOnlyAccess'
        ]
        
        for policy_arn in managed_policies:
            try:
                iam.attach_user_policy(
                    UserName=username,
                    PolicyArn=policy_arn
                )
                print(f"✅ Attached policy: {policy_arn}")
            except Exception as e:
                print(f"⚠️ Failed to attach {policy_arn}: {e}")
        
        # Access key oluştur
        print("🔑 Creating access key...")
        
        access_key_response = iam.create_access_key(UserName=username)
        access_key = access_key_response['AccessKey']
        
        print("\n" + "=" * 60)
        print("✅ ML User setup completed!")
        print(f"📋 Username: {username}")
        print(f"📋 User ARN: {user_arn}")
        print(f"📋 Access Key ID: {access_key['AccessKeyId']}")
        print(f"📋 Secret Access Key: {access_key['SecretAccessKey']}")
        print("=" * 60)
        print("\n🔧 Setup Commands:")
        print(f"export AWS_ACCESS_KEY_ID={access_key['AccessKeyId']}")
        print(f"export AWS_SECRET_ACCESS_KEY={access_key['SecretAccessKey']}")
        print("export AWS_DEFAULT_REGION=us-east-1")
        print("\n⚠️ IMPORTANT: Save these credentials safely!")
        print("=" * 60)
        
        return {
            'username': username,
            'user_arn': user_arn,
            'access_key_id': access_key['AccessKeyId'],
            'secret_access_key': access_key['SecretAccessKey']
        }
        
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"ℹ️ User {username} already exists")
        
        # Mevcut user'ın ARN'ini al
        try:
            response = iam.get_user(UserName=username)
            user_arn = response['User']['Arn']
            print(f"✅ Using existing user: {user_arn}")
            
            # Access key listele
            keys = iam.list_access_keys(UserName=username)
            if keys['AccessKeyMetadata']:
                print(f"ℹ️ User already has access keys")
                return {
                    'username': username,
                    'user_arn': user_arn,
                    'access_key_id': keys['AccessKeyMetadata'][0]['AccessKeyId'],
                    'secret_access_key': 'EXISTING_KEY'
                }
            else:
                # Yeni access key oluştur
                access_key_response = iam.create_access_key(UserName=username)
                access_key = access_key_response['AccessKey']
                print(f"✅ Created new access key for existing user")
                return {
                    'username': username,
                    'user_arn': user_arn,
                    'access_key_id': access_key['AccessKeyId'],
                    'secret_access_key': access_key['SecretAccessKey']
                }
                
        except Exception as e:
            print(f"❌ Failed to get existing user: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        return None

def add_s3_permissions_to_current_user():
    """Mevcut user'a S3 permissions ekle"""
    
    iam = boto3.client('iam')
    sts = boto3.client('sts')
    
    try:
        # Mevcut user'ı al
        caller_info = sts.get_caller_identity()
        current_arn = caller_info['Arn']
        
        # User name'i ARN'den çıkar
        username = current_arn.split('/')[-1]
        
        print(f"🔄 Adding S3 permissions to current user: {username}")
        
        # S3 policy ekle
        iam.attach_user_policy(
            UserName=username,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
        )
        
        print(f"✅ Added S3FullAccess to {username}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add S3 permissions: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("🚀 ML Project IAM Setup")
    print("=" * 60)
    
    print("Seçenekler:")
    print("1. Yeni ML user oluştur (önerilen)")
    print("2. Mevcut user'a S3 permissions ekle")
    
    choice = input("Seçiminiz (1 veya 2): ").strip()
    
    if choice == "1":
        user_info = create_ml_user()
        if user_info:
            print("\n🎉 Yeni user oluşturuldu!")
            print("Bu credentials ile AWS'ye bağlanabilirsiniz.")
    
    elif choice == "2":
        success = add_s3_permissions_to_current_user()
        if success:
            print("\n🎉 Mevcut user'a S3 permissions eklendi!")
            print("Şimdi SageMaker çalışabilir.")
    
    else:
        print("❌ Geçersiz seçim")

if __name__ == "__main__":
    main() 