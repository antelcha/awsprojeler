# Real-time Chat Application with AWS Integration

Bu proje, WebSocket tabanlı gerçek zamanlı bir sohbet uygulamasıdır. Kullanıcılar oda numarası ve kullanıcı adı ile odalara katılabilir ve mesajlaşabilirler. Mesajlar içindeki etiketler otomatik olarak analiz edilir ve kullanıcı profilleri oluşturulur.

## Özellikler

- Gerçek zamanlı mesajlaşma (WebSocket)
- Oda tabanlı sohbet sistemi
- Otomatik etiket analizi
- Kullanıcı profili oluşturma
- Admin paneli
- AWS entegrasyonu (Kinesis, DynamoDB, Lambda)

## Teknolojiler

- Frontend: Next.js, React, TailwindCSS
- Backend: Node.js, Express, Socket.IO
- AWS Servisleri: Kinesis, DynamoDB, Lambda
- Diğer: TypeScript, CORS

## Kurulum

1. Projeyi klonlayın:
```bash
git clone <repo-url>
cd <proje-dizini>
```

2. Frontend bağımlılıklarını yükleyin:
```bash
npm install
```

3. Backend bağımlılıklarını yükleyin:
```bash
cd server
npm install
```

4. AWS kaynaklarını oluşturun:
```bash
cd aws
aws cloudformation create-stack --stack-name chat-app --template-body file://template.yaml
```

5. `.env` dosyasını oluşturun:
```bash
# server/.env
AWS_REGION=us-east-1
DYNAMODB_TABLE=user_profiles
KINESIS_STREAM=chat_messages
PORT=3001
```

## Çalıştırma

1. Backend sunucusunu başlatın:
```bash
cd server
node index.js
```

2. Frontend uygulamasını başlatın:
```bash
# Ana dizinde
npm run dev
```

3. Tarayıcınızda `http://localhost:3000` adresine gidin.

## Kullanım

1. Ana sayfada bir oda numarası ve kullanıcı adı girin
2. Sohbet odasına katılın
3. Mesajlaşmaya başlayın
4. Admin paneline erişmek için ana sayfadaki "Admin Girişi" butonunu kullanın

## Etiket Sistemi

Şu anda desteklenen kategoriler ve etiketler:

- Teknoloji
  - google
  - youtube
  - amazon

- Kültür
  - kitap
  - tiyatro
  - sinema

Bu etiketlerden bahseden mesajlar otomatik olarak analiz edilir ve kullanıcı profilinde sayılır.

## AWS Mimarisi

1. WebSocket mesajları önce sunucuya gönderilir
2. Etiket içeren mesajlar AWS Kinesis'e iletilir
3. AWS Lambda fonksiyonu Kinesis'ten mesajları işler
4. Kullanıcı profilleri DynamoDB'de güncellenir
5. Admin paneli bu verileri görüntüler

## Lisans

MIT
