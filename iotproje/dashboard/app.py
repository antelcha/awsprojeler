from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json
import ssl
import threading
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'weight_monitor_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# AWS IoT Core ayarları
ENDPOINT = "a2kses0rnftuku-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "WeightDashboard_" + str(int(time.time()))
TOPIC = "weight/measurements"
CERT_PATH = "../certs/certificate.pem.crt"
PRIVATE_KEY_PATH = "../certs/private.pem.key"
ROOT_CA_PATH = "../certs/root-ca.pem"

# Veri depolama (son 100 ölçüm)
weight_data = deque(maxlen=100)
latest_data = {}
is_connected = False

def on_connect(client, userdata, flags, rc, properties=None):
    """MQTT bağlantı callback"""
    global is_connected
    if rc == 0:
        print("✓ Dashboard AWS IoT Core'a bağlandı!")
        is_connected = True
        client.subscribe(TOPIC)
        socketio.emit('connection_status', {'connected': True})
    else:
        print(f"❌ Dashboard bağlantı hatası: {rc}")
        is_connected = False
        socketio.emit('connection_status', {'connected': False})

def on_message(client, userdata, msg):
    """MQTT mesaj alma callback"""
    global latest_data
    try:
        data = json.loads(msg.payload.decode())
        
        # Zaman damgasını düzenle
        timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        data['formatted_time'] = timestamp.strftime('%H:%M:%S')
        data['formatted_date'] = timestamp.strftime('%Y-%m-%d')
        
        # Veriyi kaydet
        weight_data.append(data)
        latest_data = data
        
        print(f"📊 Yeni veri alındı: {data['weight_kg']} kg")
        
        # WebSocket ile frontend'e gönder
        socketio.emit('new_weight_data', data)
        
    except Exception as e:
        print(f"❌ Veri işleme hatası: {e}")

def on_disconnect(client, userdata, flags, rc, properties=None):
    """MQTT bağlantı kesme callback"""
    global is_connected
    is_connected = False
    print("🔌 Dashboard bağlantısı kesildi")
    socketio.emit('connection_status', {'connected': False})

def create_mqtt_client():
    """MQTT istemcisi oluştur"""
    # Yeni API versiyonu kullan
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    
    # Callback fonksiyonları
    client.on_connect = on_connect
    client.on_message = on_message
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

def start_mqtt_client():
    """MQTT istemcisini başlat"""
    mqtt_client = create_mqtt_client()
    
    try:
        print("🔗 Dashboard AWS IoT Core'a bağlanıyor...")
        mqtt_client.connect(ENDPOINT, 8883, 60)
        
        # Otomatik yeniden bağlanma ile loop
        while True:
            try:
                mqtt_client.loop(timeout=1.0)
            except Exception as e:
                print(f"⚠️ MQTT loop hatası: {e}")
                time.sleep(5)
                try:
                    mqtt_client.reconnect()
                except:
                    print("🔄 Yeniden bağlanma deneniyor...")
                    time.sleep(10)
                    
    except Exception as e:
        print(f"❌ MQTT bağlantı hatası: {e}")
        time.sleep(5)
        # Yeniden başlatmayı dene
        start_mqtt_client()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/latest')
def get_latest_data():
    """Son veriyi döndür"""
    return jsonify(latest_data)

@app.route('/api/history')
def get_history():
    """Geçmiş verileri döndür"""
    return jsonify(list(weight_data))

@app.route('/api/stats')
def get_stats():
    """İstatistikleri döndür"""
    if not weight_data:
        return jsonify({})
    
    weights = [item['weight_kg'] for item in weight_data]
    
    stats = {
        'total_measurements': len(weight_data),
        'average_weight': round(sum(weights) / len(weights), 2),
        'min_weight': min(weights),
        'max_weight': max(weights),
        'last_update': latest_data.get('formatted_time', 'N/A'),
        'connection_status': is_connected
    }
    
    return jsonify(stats)

@socketio.on('connect')
def handle_connect():
    """WebSocket bağlantısı"""
    print('👤 Kullanıcı bağlandı')
    emit('connection_status', {'connected': is_connected})
    if latest_data:
        emit('new_weight_data', latest_data)

@socketio.on('disconnect')
def handle_disconnect():
    """WebSocket bağlantı kesme"""
    print('👤 Kullanıcı ayrıldı')

if __name__ == '__main__':
    # MQTT istemcisini ayrı thread'de başlat
    mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
    mqtt_thread.start()
    
    print("🚀 Ağırlık İzleme Dashboard'u Başlatılıyor...")
    print("📱 Dashboard: http://localhost:5001")
    
    # Flask uygulamasını başlat
    socketio.run(app, host='0.0.0.0', port=5001, debug=True) 