#!/usr/bin/env python3
"""
AWS IoT Core Bağlantı Test Scripti
Bu script AWS IoT Core bağlantısını test eder.
"""

import ssl
import time
import paho.mqtt.client as mqtt

# AWS IoT Core ayarları
ENDPOINT = "a2kses0rnftuku-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "ConnectionTest_" + str(int(time.time()))
TOPIC = "weight/measurements"
CERT_PATH = "certs/certificate.pem.crt"
PRIVATE_KEY_PATH = "certs/private.pem.key"
ROOT_CA_PATH = "certs/root-ca.pem"

def on_connect(client, userdata, flags, rc, properties=None):
    """MQTT bağlantı callback"""
    if rc == 0:
        print("✅ AWS IoT Core'a başarıyla bağlandı!")
        print(f"📋 Client ID: {CLIENT_ID}")
        print(f"📡 Endpoint: {ENDPOINT}")
        client.subscribe(TOPIC)
        print(f"📥 Topic'e abone olundu: {TOPIC}")
    else:
        print(f"❌ Bağlantı hatası: {rc}")

def on_message(client, userdata, msg):
    """MQTT mesaj alma callback"""
    print(f"📨 Mesaj alındı: {msg.topic} -> {msg.payload.decode()}")

def on_disconnect(client, userdata, flags, rc, properties=None):
    """MQTT bağlantı kesme callback"""
    print(f"🔌 Bağlantı kesildi (RC: {rc})")

def main():
    print("🔍 AWS IoT Core Bağlantı Testi")
    print("=" * 40)
    
    # MQTT istemcisi oluştur
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    
    # Callback fonksiyonları
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # SSL/TLS yapılandırması
    try:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(ROOT_CA_PATH)
        context.load_cert_chain(CERT_PATH, PRIVATE_KEY_PATH)
        
        client.tls_set_context(context)
        print("✅ SSL sertifikaları yüklendi")
        
    except Exception as e:
        print(f"❌ SSL yapılandırma hatası: {e}")
        return
    
    try:
        print(f"🔗 {ENDPOINT}:8883 adresine bağlanılıyor...")
        client.connect(ENDPOINT, 8883, 60)
        
        print("⏳ 30 saniye boyunca bağlantı test ediliyor...")
        client.loop_start()
        
        # 30 saniye bekle
        for i in range(30):
            time.sleep(1)
            if i % 5 == 0:
                print(f"⏱️  {30-i} saniye kaldı...")
        
        client.loop_stop()
        client.disconnect()
        print("✅ Test tamamlandı!")
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")

if __name__ == "__main__":
    main() 