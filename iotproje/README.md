# IoT Ağırlık Ölçer Simülatörü & Canlı İzleme Dashboard'u

Bu proje, AWS IoT Core kullanarak ağırlık ölçümlerini simüle eden bir IoT cihazı simülatörü ve gerçek zamanlı web dashboard'u içerir.

## 🚀 Özellikler

### Simülatör
- Rastgele ağırlık verisi üretimi (1-1000 kg)
- AWS IoT Core'a MQTT protokolü ile veri gönderimi
- Otomatik yeniden bağlanma
- Veri sayacı (300 veri sonrası sıfırlanır)
- Zaman damgası ile veri kayıt

### Dashboard
- 📊 Gerçek zamanlı ağırlık izleme
- 📈 Canlı grafik (son 20 ölçüm)
- 📋 İstatistikler (ortalama, min, max)
- 📝 Son ölçümler tablosu
- 🔄 WebSocket ile anlık güncelleme
- 📱 Responsive tasarım

## 📋 Gereksinimler

- Python 3.7+
- AWS hesabı
- AWS CLI kurulu ve yapılandırılmış

## 🛠️ Kurulum

### 1. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 2. AWS CLI'yi Yapılandır

```bash
aws configure
```

AWS Access Key ID, Secret Access Key, region ve output format bilgilerini girin.

### 3. AWS IoT Core'u Kur

```bash
python setup_aws_iot.py
```

Bu script otomatik olarak:
- IoT Thing oluşturur
- Sertifika ve private key üretir
- IoT Policy oluşturur ve ekler
- Endpoint bilgisini alır ve koda ekler

## 🎯 Kullanım

### Kolay Başlatma (Önerilen)

```bash
python start_project.py
```

Bu script size şu seçenekleri sunar:
1. Sadece Simülatör
2. Sadece Dashboard
3. Her ikisi birden

### Manuel Başlatma

#### Simülatörü Çalıştır

```bash
python src/weight_simulator_v2.py
```

#### Dashboard'u Çalıştır

```bash
cd dashboard
python app.py
```

Dashboard'a tarayıcınızdan şu adresten erişebilirsiniz: http://localhost:5001

## 📊 Dashboard Özellikleri

### Ana Ekran
- **Anlık Ağırlık**: Güncel ağırlık değeri büyük fontla gösterilir
- **Bağlantı Durumu**: AWS IoT Core bağlantı durumu
- **İstatistikler**: Ortalama, minimum, maksimum değerler ve toplam ölçüm sayısı

### Grafik
- Son 20 ölçümün canlı line chart'ı
- Otomatik güncelleme
- Responsive tasarım

### Veri Tablosu
- Son 10 ölçümün detaylı listesi
- Zaman, ağırlık, sayaç ve lokasyon bilgileri

## 📁 Proje Yapısı

```
iotproje/
├── src/
│   ├── weight_simulator.py       # Orijinal simülatör (Python 3.13 uyumsuz)
│   └── weight_simulator_v2.py    # Güncellenmiş simülatör (paho-mqtt)
├── dashboard/
│   ├── app.py                    # Flask dashboard uygulaması
│   └── templates/
│       └── index.html            # Dashboard HTML template
├── certs/                        # AWS IoT sertifikaları
│   ├── certificate.pem.crt
│   ├── private.pem.key
│   └── root-ca.pem
├── setup_aws_iot.py             # AWS IoT kurulum scripti
├── start_project.py             # Proje başlatma scripti
├── requirements.txt             # Python bağımlılıkları
└── README.md                    # Bu dosya
```

## 🔧 Konfigürasyon

### Simülatör Ayarları
`src/weight_simulator_v2.py` dosyasında:
- `MAX_DATA_COUNT`: Maksimum veri sayısı (varsayılan: 300)
- `TOPIC`: MQTT topic adı (varsayılan: "weight/measurements")
- `CLIENT_ID`: MQTT client ID (varsayılan: "WeightScaleSimulator")

### Dashboard Ayarları
`dashboard/app.py` dosyasında:
- `CLIENT_ID`: Dashboard MQTT client ID
- Port: 5000 (varsayılan)

## 📊 Veri Formatı

Gönderilen veri formatı:

```json
{
    "device_id": "WeightScaleSimulator",
    "weight_kg": 125.67,
    "timestamp": "2024-01-15T10:30:45.123456",
    "data_count": 1,
    "location": "Warehouse-A",
    "unit": "kg"
}
```

## 🌐 Dashboard API Endpoints

- `GET /`: Ana dashboard sayfası
- `GET /api/latest`: Son ölçüm verisi
- `GET /api/history`: Tüm geçmiş veriler
- `GET /api/stats`: İstatistikler
- WebSocket: Gerçek zamanlı veri akışı

## 📊 AWS IoT Core'da Veri İzleme

1. AWS Console'da IoT Core servisine gidin
2. "Test" sekmesine tıklayın
3. "MQTT test client"i açın
4. Topic: `weight/measurements` olarak ayarlayın
5. "Subscribe" butonuna tıklayın

## 🛑 Durdurma

- Simülatörü durdurmak için `Ctrl+C` tuşlarına basın
- Dashboard'u durdurmak için `Ctrl+C` tuşlarına basın
- Her ikisini birden çalıştırıyorsanız, `Ctrl+C` ile her ikisini de durdurabilirsiniz

## 🔍 Sorun Giderme

### Python 3.13 SSL Hatası
Eğer `ssl.wrap_socket` hatası alıyorsanız:
- `weight_simulator_v2.py` kullanın (paho-mqtt ile)
- Eski `AWSIoTPythonSDK` yerine modern `paho-mqtt` kullanır

### Bağlantı Hatası
- AWS kimlik bilgilerinizi kontrol edin
- Sertifika dosyalarının doğru yerde olduğundan emin olun
- Internet bağlantınızı kontrol edin

### Dashboard Bağlantı Sorunu
- Simülatörün çalıştığından emin olun
- AWS IoT Core bağlantısını kontrol edin
- Tarayıcı konsolunda hata mesajlarını kontrol edin

### Sertifika Hatası
- `setup_aws_iot.py` scriptini tekrar çalıştırın
- `certs/` klasörünü silin ve tekrar oluşturun

## 🎨 Dashboard Özellikleri

- **Modern UI**: Gradient arka plan ve card-based tasarım
- **Responsive**: Mobil ve desktop uyumlu
- **Real-time**: WebSocket ile anlık güncelleme
- **Charts**: Chart.js ile interaktif grafikler
- **Icons**: Font Awesome ikonları
- **Animations**: CSS animasyonları ve hover efektleri

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add some amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun 