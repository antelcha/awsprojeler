# Mesajlaşma Uygulaması Üzerinden Reklam Profili Analizi Demosu

Mustafa Girgin 
21290649

Bu projede, WebSocket teknolojisi kullanarak gerçek zamanlı bir mesajlaşma uygulaması geliştirdim ve bu uygulama üzerinden akan mesajları AWS Kinesis servisi aracılığıyla analiz etmeyi amaçladım. Projenin temel amacı, kullanıcıların sohbet ederken paylaştıkları mesajların içeriklerini inceleyerek, kişiselleştirilmiş reklamlar için veri toplamaktı.

Projeye başlarken ilk olarak basit bir mesajlaşma uygulaması geliştirmeye odaklandım. Node.js ve Socket.io teknolojilerini seçtim çünkü gerçek zamanlı iletişim için en kolay ve hızlı çözümü bu ikili sunuyordu. Express.js kullanarak bir web server oluşturdum ve üzerine Socket.io'yu entegre ettim.

Mesajlaşma kısmını geliştirirken özellikle şu noktalara dikkat ettim:
- Kullanıcılar sayfaya girdiğinde otomatik olarak bir socket bağlantısı oluşturulması
- Mesajların anlık olarak tüm bağlı kullanıcılara iletilmesi
- Bağlantı kopması durumunda kullanıcının tekrar bağlanabilmesi

Frontend tarafını mümkün olduğunca basit tuttum. HTML ve temel CSS kullanarak bir mesajlaşma arayüzü tasarladım. Kullanıcılar bir metin kutusuna mesajlarını yazıp gönderebiliyor ve diğer kullanıcıların mesajlarını anlık olarak görebiliyorlar.

AWS tarafında ise ilk olarak bir Kinesis Data Stream oluşturdum. AWS Console üzerinden IAM servisini kullanarak gerekli izinleri aldım ve bir access key oluşturdum. Bu anahtarları güvenli bir şekilde .env dosyasında sakladım.

Mesajlaşma uygulaması ile AWS Kinesis'i birleştirirken, her gelen mesajı Kinesis stream'e göndermeye çalıştım. Bu kısımda AWS SDK'yı kullanarak Kinesis'e bağlandım. Her mesaj geldiğinde, içeriği JSON formatına çevirip stream'e gönderiyorum. Bu sayede mesajların içeriğini daha sonra analiz edebilmek için kaydediyorum.

Projeyi geliştirirken bazı zorluklarla karşılaştım:
- AWS servislerinin konfigürasyonu başlangıçta biraz karmaşık geldi
- Socket.io ve Kinesis'in birlikte çalışmasını sağlamak için biraz uğraşmam gerekti
- Mesajların Kinesis'e gönderilirken bazen yaşanan gecikmeler

Şu an için uygulama temel seviyede çalışıyor:
1. Kullanıcılar web sayfasını açıp mesajlaşabiliyor
2. Gönderilen her mesaj Kinesis stream'e aktarılıyor
3. AWS Console üzerinden mesaj akışını görebiliyorum

İleride projeyi geliştirmek için bazı planlarım var:
- Mesaj içeriklerinin daha detaylı analizi
- Kullanıcı bazlı istatistikler çıkarma
- Toplanan verilere göre basit bir reklam önerme sistemi

Bu proje sayesinde özellikle WebSocket teknolojisi ve AWS servislerinin nasıl çalıştığını öğrenme fırsatı buldum. Her ne kadar şu an için basit bir demo olsa da, gerçek zamanlı veri akışı ve analizi konusunda güzel bir deneyim oldu. Socket.io'nun ne kadar kullanışlı bir teknoloji olduğunu ve AWS Kinesis'in veri akışı konusunda nasıl yardımcı olabileceğini görmüş oldum.
