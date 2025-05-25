import boto3
import json
import os
import time

def setup_aws_iot():
    """AWS IoT Core kaynaklarını otomatik olarak kurar"""
    
    # AWS IoT istemcisini oluştur
    iot_client = boto3.client('iot')
    
    # Thing adı
    thing_name = "WeightScaleDevice"
    policy_name = "WeightScalePolicy"
    
    try:
        print("1. Thing oluşturuluyor...")
        # Thing oluştur
        try:
            iot_client.create_thing(thingName=thing_name)
            print(f"✓ Thing '{thing_name}' oluşturuldu")
        except iot_client.exceptions.ResourceAlreadyExistsException:
            print(f"✓ Thing '{thing_name}' zaten mevcut")
        
        print("\n2. Sertifika oluşturuluyor...")
        # Sertifika ve anahtar çifti oluştur
        cert_response = iot_client.create_keys_and_certificate(setAsActive=True)
        
        certificate_arn = cert_response['certificateArn']
        certificate_id = cert_response['certificateId']
        certificate_pem = cert_response['certificatePem']
        private_key = cert_response['keyPair']['PrivateKey']
        
        print(f"✓ Sertifika oluşturuldu: {certificate_id}")
        
        print("\n3. Sertifika dosyaları kaydediliyor...")
        # Sertifika dosyalarını kaydet
        os.makedirs('certs', exist_ok=True)
        
        with open('certs/certificate.pem.crt', 'w') as f:
            f.write(certificate_pem)
        
        with open('certs/private.pem.key', 'w') as f:
            f.write(private_key)
        
        # Root CA sertifikasını indir
        import urllib.request
        root_ca_url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
        urllib.request.urlretrieve(root_ca_url, 'certs/root-ca.pem')
        
        print("✓ Sertifika dosyaları kaydedildi")
        
        print("\n4. IoT Policy oluşturuluyor...")
        # IoT Policy oluştur
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "iot:Connect",
                        "iot:Publish",
                        "iot:Subscribe",
                        "iot:Receive"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        try:
            iot_client.create_policy(
                policyName=policy_name,
                policyDocument=json.dumps(policy_document)
            )
            print(f"✓ Policy '{policy_name}' oluşturuldu")
        except iot_client.exceptions.ResourceAlreadyExistsException:
            print(f"✓ Policy '{policy_name}' zaten mevcut")
        
        print("\n5. Policy sertifikaya ekleniyor...")
        # Policy'yi sertifikaya ekle
        iot_client.attach_policy(
            policyName=policy_name,
            target=certificate_arn
        )
        print("✓ Policy sertifikaya eklendi")
        
        print("\n6. Sertifika Thing'e ekleniyor...")
        # Sertifikayı Thing'e ekle
        iot_client.attach_thing_principal(
            thingName=thing_name,
            principal=certificate_arn
        )
        print("✓ Sertifika Thing'e eklendi")
        
        print("\n7. IoT Endpoint alınıyor...")
        # IoT Endpoint'i al
        endpoint_response = iot_client.describe_endpoint(endpointType='iot:Data-ATS')
        endpoint = endpoint_response['endpointAddress']
        
        print(f"✓ IoT Endpoint: {endpoint}")
        
        # Endpoint'i weight_simulator.py dosyasında güncelle
        print("\n8. weight_simulator.py dosyası güncelleniyor...")
        with open('src/weight_simulator.py', 'r') as f:
            content = f.read()
        
        content = content.replace('YOUR_AWS_IOT_ENDPOINT', endpoint)
        
        with open('src/weight_simulator.py', 'w') as f:
            f.write(content)
        
        print("✓ weight_simulator.py dosyası güncellendi")
        
        print("\n🎉 AWS IoT Core kurulumu tamamlandı!")
        print(f"📋 Thing Name: {thing_name}")
        print(f"📋 Certificate ID: {certificate_id}")
        print(f"📋 Endpoint: {endpoint}")
        print(f"📋 Topic: weight/measurements")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return False

if __name__ == "__main__":
    print("AWS IoT Core Kurulum Scripti")
    print("=" * 40)
    
    # AWS kimlik bilgilerini kontrol et
    try:
        boto3.Session().get_credentials()
        print("✓ AWS kimlik bilgileri bulundu")
    except:
        print("❌ AWS kimlik bilgileri bulunamadı!")
        print("Lütfen 'aws configure' komutunu çalıştırın")
        exit(1)
    
    setup_aws_iot() 