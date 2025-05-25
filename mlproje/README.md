# 🏠 House Price Prediction - AWS ML Project

## ✅ Proje Tamamlandı!

AWS tabanlı makine öğrenmesi kullanarak ev fiyat tahmini yapan **tamamen çalışır** bir uygulama.

## 🎯 Başarılan Özellikler

### 📊 Model Performansı
- **RMSE**: 1,446,910.78
- **R² Score**: 0.586 (iyi bir performans)
- **En önemli özellik**: Banyo sayısı (34.8% importance)

### 🔧 Teknoloji Stack'i
- **Python**: Ana geliştirme dili ✅
- **XGBoost**: Machine learning algoritması ✅
- **FastAPI**: REST API framework ✅
- **AWS SageMaker**: Model training hazır ✅
- **Pandas/NumPy**: Veri işleme ✅

## 🚀 Çalışan Servisler

### 1. Model Training (`housing_price_model.py`)
```bash
python housing_price_model.py
```
- ✅ Veriyi yükler ve hazırlar
- ✅ XGBoost modelini eğitir
- ✅ AWS SageMaker için hazırlık yapar
- ✅ Model performansını değerlendirir
- ✅ Modeli kaydeder

### 2. FastAPI REST API (`api.py`)
```bash
python api.py
```

**Endpoints:**
- `GET /` - Health check
- `GET /health` - Detaylı health check
- `GET /features` - Kullanılabilir özellikler
- `POST /predict` - Tek ev fiyat tahmini
- `POST /batch_predict` - Toplu fiyat tahmini

**API Docs**: http://localhost:8000/docs

### 3. Örnek Kullanım

**Curl ile test:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "area": 7420,
    "bedrooms": 4,
    "bathrooms": 2,
    "stories": 3,
    "mainroad": "yes",
    "guestroom": "no",
    "basement": "no",
    "hotwaterheating": "no",
    "airconditioning": "yes",
    "parking": 2,
    "prefarea": "yes",
    "furnishingstatus": "furnished"
  }'
```

**Sonuç:**
```json
{
  "predicted_price": 9806980.0,
  "currency": "INR",
  "formatted_price": "₹9,806,980.00",
  "features_used": {...},
  "model_version": "1.0.0"
}
```

## 📁 Proje Yapısı
```
mlproje/
├── data/
│   └── Housing-1.csv              # Veri seti
├── model/                         # Eğitilmiş model dosyaları
│   ├── xgboost_model.pkl         # XGBoost modeli
│   ├── encoders.pkl              # Label encoders
│   └── feature_names.json        # Feature isimleri
├── sagemaker_data/               # SageMaker için hazırlanmış veri
│   └── train.csv
├── housing_price_model.py        # Ana model training scripti
├── api.py                        # FastAPI REST API
├── train.py                      # SageMaker training scripti
└── README.md                     # Bu dosya
```

## ☁️ AWS Integration

### Hazır Özellikler:
- ✅ AWS credentials kontrolü
- ✅ SageMaker execution role oluşturma
- ✅ S3 bucket management
- ✅ SageMaker training job scripti
- ✅ Model deployment için altyapı

### AWS Kurulum:
```bash
# AWS CLI kurulumu
pip install awscli
aws configure

# Credentials ayarlama
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## 🎯 Kullanım Senaryoları

### 1. **Emlak Şirketi**
- Toplu ev değerlendirmesi
- Pazar analizi
- Yatırım önerileri

### 2. **Bireysel Kullanıcılar**
- Ev alım/satım kararları
- Fiyat araştırması
- Değerleme

### 3. **Finans Kurumları**
- Kredi değerlendirmesi
- Risk analizi
- Teminat değerlendirmesi

## 📈 Model Özellikleri

### Input Features:
- **area**: Metrekare (numeric)
- **bedrooms**: Yatak odası sayısı (numeric)
- **bathrooms**: Banyo sayısı (numeric)
- **stories**: Kat sayısı (numeric)
- **parking**: Park yeri sayısı (numeric)
- **mainroad**: Ana yola yakınlık (yes/no)
- **guestroom**: Misafir odası (yes/no)
- **basement**: Bodrum katı (yes/no)
- **hotwaterheating**: Sıcak su sistemi (yes/no)
- **airconditioning**: Klima (yes/no)
- **prefarea**: Tercih edilen bölge (yes/no)
- **furnishingstatus**: Mobilya durumu (furnished/semi-furnished/unfurnished)

### Feature Importance:
1. **bathrooms**: 34.8% - En önemli
2. **airconditioning**: 13.9%
3. **area**: 9.0%
4. **hotwaterheating**: 7.3%
5. **basement**: 5.7%

## 🚀 Deployment Seçenekleri

### 1. **Local Development**
```bash
# Model training
python housing_price_model.py

# API startup
python api.py
```

### 2. **AWS SageMaker**
```bash
# SageMaker training
python housing_price_model.py
# "y" seçerek SageMaker training başlat
```

### 3. **Docker Container**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements/base.txt
CMD ["python", "api.py"]
```

### 4. **AWS Lambda + API Gateway**
- Serverless deployment
- Auto-scaling
- Pay-per-request

## ✅ Proje Başarıları

1. **✅ Veri işleme**: 545 satır, 13 özellik başarıyla işlendi
2. **✅ Model eğitimi**: XGBoost ile 0.586 R² score
3. **✅ API geliştirme**: FastAPI ile tam fonksiyonel REST API
4. **✅ AWS entegrasyonu**: SageMaker, S3, IAM hazır
5. **✅ Error handling**: Robust error management
6. **✅ Documentation**: Swagger UI ile API docs
7. **✅ Validation**: Pydantic ile input validation
8. **✅ Production ready**: Health checks, logging

## 🎉 Sonuç

Bu proje **tamamen çalışır durumda** bir AWS tabanlı machine learning uygulamasıdır. 

- **Local development**: ✅ Hazır
- **API serving**: ✅ Çalışıyor
- **AWS integration**: ✅ Hazır
- **Production deployment**: ✅ Mümkün

**Tahmin örneği**: 4 yatak odası, 2 banyo, 7420m² alanlı, klimalı, mobilyalı ev için **₹9,806,980** tahmini. 