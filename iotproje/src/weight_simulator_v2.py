import json
import time
import random
import ssl
from datetime import datetime
import paho.mqtt.client as mqtt

# AWS IoT Core endpoint
ENDPOINT = "a2kses0rnftuku-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "WeightScaleSimulator"
TOPIC = "weight/measurements"
CERT_PATH = "certs/certificate.pem.crt"
PRIVATE_KEY_PATH = "certs/private.pem.key"
ROOT_CA_PATH = "certs/root-ca.pem"

# Veri sayacı
data_count = 0
MAX_DATA_COUNT = 300

def on_connect(client, userdata, flags, rc, properties=None):
    """MQTT bağlantı callback fonksiyonu"""
    if rc == 0:
        print("✓ AWS IoT Core'a başarıyla bağlandı!")
    else:
        print(f"❌ Bağlantı hatası: {rc}")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """MQTT publish callback fonksiyonu"""
    print(f"✓ Mesaj gönderildi (Message ID: {mid})")

def on_disconnect(client, userdata, flags, rc, properties=None):
    """MQTT bağlantı kesme callback fonksiyonu"""
    print("🔌 AWS IoT Core bağlantısı kesildi")

def create_mqtt_client():
    """MQTT istemcisini oluşturur ve yapılandırır"""
    # Yeni API versiyonu kullan
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    
    # Callback fonksiyonlarını ayarla
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    # MQTT ayarları - bağlantı kararlılığı için
    client.reconnect_delay_set(min_delay=1, max_delay=120)
    client.max_inflight_messages_set(20)
    client.max_queued_messages_set(0)
    
    # SSL/TLS yapılandırması
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(ROOT_CA_PATH)
    context.load_cert_chain(CERT_PATH, PRIVATE_KEY_PATH)
    
    client.tls_set_context(context)
    
    return client

def generate_weight_data():
    """Rastgele ağırlık verisi üretir (1-1000 kg arası)"""
    return round(random.uniform(1, 1000), 2)

def main():
    global data_count
    
    print("🚀 IoT Ağırlık Ölçer Simülatörü Başlatılıyor...")
    print("=" * 50)
    
    # MQTT istemcisini oluştur
    mqtt_client = create_mqtt_client()
    
    try:
        print("🔗 AWS IoT Core'a bağlanılıyor...")
        mqtt_client.connect(ENDPOINT, 8883, 60)
        
        # Bağlantı döngüsünü başlat
        mqtt_client.loop_start()
        
        # Bağlantının kurulmasını bekle
        time.sleep(3)
        
        print(f"📡 Topic: {TOPIC}")
        print(f"🆔 Client ID: {CLIENT_ID}")
        print("📊 Veri gönderimi başlıyor...\n")
        
        while True:
            # Veri sayacını kontrol et
            if data_count >= MAX_DATA_COUNT:
                print(f"\n🔄 {MAX_DATA_COUNT} veri gönderildi. Sayaç sıfırlanıyor...")
                data_count = 0
                
            # Veri oluştur
            weight = generate_weight_data()
            timestamp = datetime.now().isoformat()
            
            message = {
                "device_id": CLIENT_ID,
                "weight_kg": weight,
                "timestamp": timestamp,
                "data_count": data_count + 1,
                "location": "Warehouse-A",
                "unit": "kg"
            }
            
            # Veriyi JSON formatında gönder
            try:
                result = mqtt_client.publish(TOPIC, json.dumps(message), qos=1)
                
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"📦 Ağırlık: {weight} kg | Sayaç: {data_count + 1} | Zaman: {timestamp}")
                else:
                    print(f"❌ Veri gönderme hatası: {result.rc}")
                    
            except Exception as e:
                print(f"❌ Publish hatası: {e}")
                # Yeniden bağlanmayı dene
                try:
                    mqtt_client.reconnect()
                    time.sleep(2)
                except:
                    print("🔄 Yeniden bağlanma başarısız, devam ediliyor...")
            
            # Sayacı artır
            data_count += 1
            
            # 5 saniye bekle
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Program sonlandırılıyor...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("👋 Bağlantı kapatıldı. Güle güle!")
        
    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        
if __name__ == "__main__":
    main() 