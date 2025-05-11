require('dotenv').config();
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const { KinesisClient, PutRecordCommand } = require('@aws-sdk/client-kinesis');
const { DynamoDBClient, UpdateItemCommand, ScanCommand, GetItemCommand, PutItemCommand, DeleteItemCommand } = require('@aws-sdk/client-dynamodb');

const app = express();
app.use(cors());
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3002",
    methods: ["GET", "POST"]
  }
});

// AWS clients
const kinesisClient = new KinesisClient({ region: process.env.AWS_REGION });
const dynamoClient = new DynamoDBClient({ region: process.env.AWS_REGION });

// Önceden tanımlanmış kategoriler ve etiketler
const CATEGORIES = {
  'teknoloji': ['yapay zeka', 'blockchain', 'metaverse', 'siber güvenlik', 'bulut bilişim', 'robotik', 'veri bilimi', '5g', 'nesnelerin interneti', 'kripto para'],
  'kültür_sanat': ['tiyatro', 'sergi', 'müze', 'resim', 'heykel', 'opera', 'bale', 'konser', 'festival', 'sinema'],
  'spor': ['futbol', 'basketbol', 'voleybol', 'tenis', 'yüzme', 'atletizm', 'formula', 'boks', 'fitness', 'yoga'],
  'bilim': ['astronomi', 'fizik', 'kimya', 'biyoloji', 'genetik', 'ekoloji', 'kuantum', 'evrim', 'uzay', 'iklim'],
  'sağlık': ['beslenme', 'egzersiz', 'meditasyon', 'psikoloji', 'vitamin', 'bağışıklık', 'uyku', 'stres', 'diyet', 'wellness'],
  'eğitim': ['öğrenim', 'sınav', 'kurs', 'akademi', 'burs', 'yüksek lisans', 'doktora', 'seminer', 'workshop', 'sertifika'],
  'ekonomi': ['borsa', 'döviz', 'yatırım', 'enflasyon', 'faiz', 'ekonomik büyüme', 'ihracat', 'ithalat', 'girişimcilik', 'fintech'],
  'seyahat': ['turizm', 'gezi', 'tatil', 'otel', 'uçuş', 'vize', 'backpacking', 'kamp', 'doğa', 'macera'],
  'yemek': ['gastronomi', 'restoran', 'tarif', 'şef', 'mutfak', 'kahve', 'şarap', 'vejetaryen', 'organik', 'sokak lezzetleri'],
  'yaşam_stili': ['moda', 'dekorasyon', 'alışveriş', 'sürdürülebilirlik', 'minimalizm', 'hobi', 'bahçe', 'ev', 'tasarım', 'vintage']
};

// Reklam içerikleri
const AD_CONTENTS = {
  'teknoloji': {
    title: 'Teknoloji ürünlerinde %80\'e varan indirim!',
    description: 'En yeni teknoloji ürünlerini kaçırmayın',
    backgroundColor: '#007bff',
    link: '/tech-deals'
  },
  'kültür_sanat': {
    title: 'Kültür-Sanat etkinliklerinde %50 indirim!',
    description: 'Tiyatro, sergi ve konser biletlerinde özel fırsatlar',
    backgroundColor: '#6f42c1',
    link: '/art-events'
  },
  'spor': {
    title: 'Spor ekipmanlarında süper fırsatlar!',
    description: 'Fitness ve spor malzemelerinde sezon indirimi',
    backgroundColor: '#28a745',
    link: '/sports-deals'
  },
  'bilim': {
    title: 'Bilim kitaplarında büyük indirim!',
    description: 'Popüler bilim kitaplarında özel fırsatlar',
    backgroundColor: '#17a2b8',
    link: '/science-books'
  },
  'sağlık': {
    title: 'Sağlık ürünlerinde kampanya!',
    description: 'Vitamin ve takviye gıdalarda indirim fırsatı',
    backgroundColor: '#dc3545',
    link: '/health-products'
  },
  'eğitim': {
    title: 'Online kurslarda %60 indirim!',
    description: 'Sertifikalı eğitimler için son fırsat',
    backgroundColor: '#fd7e14',
    link: '/education-deals'
  },
  'ekonomi': {
    title: 'Yatırım araçlarında sıfır komisyon!',
    description: 'Ekonomi ve finans araçlarında özel teklifler',
    backgroundColor: '#20c997',
    link: '/finance-offers'
  },
  'seyahat': {
    title: 'Tatil paketlerinde erken rezervasyon!',
    description: 'Yaz tatili için erken rezervasyon fırsatları',
    backgroundColor: '#e83e8c',
    link: '/travel-deals'
  },
  'yemek': {
    title: 'Restoranlarda %40 indirim!',
    description: 'Seçili restoranlarda özel menü fırsatları',
    backgroundColor: '#ffc107',
    link: '/food-deals'
  },
  'yaşam_stili': {
    title: 'Moda ve dekorasyonda sezon indirimi!',
    description: 'Yaşam ürünlerinde özel kampanyalar',
    backgroundColor: '#6c757d',
    link: '/lifestyle-deals'
  }
};

// Mesajdaki etiketleri kontrol et
function checkForTags(message) {
  const words = message.toLowerCase().split(/\s+/);
  const foundTags = {};
  
  for (const [category, tags] of Object.entries(CATEGORIES)) {
    for (const tag of tags) {
      if (words.includes(tag.toLowerCase())) {
        if (!foundTags[category]) {
          foundTags[category] = [];
        }
        foundTags[category].push(tag);
      }
    }
  }
  
  return foundTags;
}

// Kullanıcı profilini güncelle
async function updateUserProfile(username, foundTags) {
  try {
    // Önce kullanıcının var olup olmadığını kontrol et
    const getParams = {
      TableName: process.env.DYNAMODB_TABLE,
      Key: {
        username: { S: username }
      }
    };

    let userExists = true;
    try {
      await dynamoClient.send(new GetItemCommand(getParams));
    } catch (error) {
      userExists = false;
      // Kullanıcı yoksa, yeni kullanıcı oluştur
      const putParams = {
        TableName: process.env.DYNAMODB_TABLE,
        Item: {
          username: { S: username },
          tags: { M: {} },
          categories: { M: {} }
        }
      };
      await dynamoClient.send(new PutItemCommand(putParams));
    }

    // Mevcut profili al
    const { Item } = await dynamoClient.send(new GetItemCommand(getParams));
    const currentTags = Item?.tags?.M || {};
    const currentCategories = Item?.categories?.M || {};

    // Yeni değerleri hazırla
    for (const [category, tags] of Object.entries(foundTags)) {
      // Kategori sayacını güncelle
      currentCategories[category] = { 
        N: ((parseInt(currentCategories[category]?.N || '0')) + 1).toString() 
      };

      // Etiket sayaçlarını güncelle
      for (const tag of tags) {
        currentTags[tag] = { 
          N: ((parseInt(currentTags[tag]?.N || '0')) + 1).toString() 
        };
      }
    }

    // Güncelleme işlemini tek seferde yap
    const updateParams = {
      TableName: process.env.DYNAMODB_TABLE,
      Key: {
        username: { S: username }
      },
      UpdateExpression: 'SET #tags = :tags, #categories = :categories',
      ExpressionAttributeNames: {
        '#tags': 'tags',
        '#categories': 'categories'
      },
      ExpressionAttributeValues: {
        ':tags': { M: currentTags },
        ':categories': { M: currentCategories }
      }
    };

    await dynamoClient.send(new UpdateItemCommand(updateParams));
  } catch (error) {
    console.error('Error updating user profile:', error);
  }
}

// Socket.IO bağlantı yönetimi
io.on('connection', (socket) => {
  const { roomId, username } = socket.handshake.query;
  
  console.log(`User ${username} trying to join room ${roomId}`);
  
  socket.join(roomId);
  console.log(`User ${username} joined room ${roomId}`);

  socket.on('message', async (data) => {
    console.log(`Received message from ${data.username} in room ${data.roomId}:`, data.text);
    
    const messageId = Date.now().toString();
    const message = {
      id: messageId,
      ...data
    };

    // Mesajı odadaki herkese gönder
    console.log(`Broadcasting message to room ${data.roomId}`);
    io.to(roomId).emit('message', message);

    // Mesajdaki etiketleri kontrol et
    const foundTags = checkForTags(data.text);
    console.log('Found tags:', foundTags);
    
    if (Object.keys(foundTags).length > 0) {
      try {
        // Kullanıcı profilini güncelle
        console.log(`Updating user profile for ${data.username}`);
        await updateUserProfile(data.username, foundTags);

        // Mesajı Kinesis'e gönder
        console.log('Sending message to Kinesis');
        const kinesisParams = {
          Data: Buffer.from(JSON.stringify({
            messageId,
            username: data.username,
            text: data.text,
            tags: foundTags,
            timestamp: data.timestamp
          })),
          PartitionKey: messageId,
          StreamName: process.env.KINESIS_STREAM
        };

        await kinesisClient.send(new PutRecordCommand(kinesisParams));
        console.log('Message sent to Kinesis successfully');
      } catch (error) {
        console.error('Error processing message:', error);
      }
    }
  });

  socket.on('disconnect', () => {
    console.log(`User ${username} left room ${roomId}`);
    socket.leave(roomId);
  });
});

// Admin API endpoint'i
app.get('/api/admin/profiles', async (req, res) => {
  try {
    const params = {
      TableName: process.env.DYNAMODB_TABLE,
      Select: 'ALL_ATTRIBUTES'
    };

    const { Items } = await dynamoClient.send(new ScanCommand(params));
    
    if (!Items || Items.length === 0) {
      return res.json([]);
    }

    const profiles = Items.map(item => ({
      username: item.username.S,
      tags: Object.fromEntries(
        Object.entries(item.tags?.M || {}).map(([key, value]) => [key, parseInt(value.N)])
      ),
      categories: Object.fromEntries(
        Object.entries(item.categories?.M || {}).map(([key, value]) => [key, parseInt(value.N)])
      )
    }));

    res.json(profiles);
  } catch (error) {
    console.error('Error fetching profiles:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Tüm verileri silmek için yeni endpoint
app.delete('/api/admin/clear-data', async (req, res) => {
  try {
    // Önce tüm kullanıcıları al
    const scanParams = {
      TableName: process.env.DYNAMODB_TABLE,
      Select: 'ALL_ATTRIBUTES'
    };

    const { Items } = await dynamoClient.send(new ScanCommand(scanParams));
    
    if (!Items || Items.length === 0) {
      return res.json({ message: 'No data to clear' });
    }

    // Her bir kullanıcıyı sil
    const deletePromises = Items.map(item => {
      const deleteParams = {
        TableName: process.env.DYNAMODB_TABLE,
        Key: {
          username: { S: item.username.S }
        }
      };
      return dynamoClient.send(new DeleteItemCommand(deleteParams));
    });

    await Promise.all(deletePromises);
    
    res.json({ message: 'All data cleared successfully' });
  } catch (error) {
    console.error('Error clearing data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Kullanıcının en çok kullandığı kategoriyi ve reklam içeriğini getir
app.get('/api/user/top-category/:username', async (req, res) => {
  try {
    const { username } = req.params;
    
    const params = {
      TableName: process.env.DYNAMODB_TABLE,
      Key: {
        username: { S: username }
      }
    };

    const result = await dynamoClient.send(new GetItemCommand(params));
    
    if (!result.Item) {
      return res.json({ hasProfile: false });
    }

    const categories = result.Item.categories?.M || {};
    let topCategory = null;
    let maxCount = 0;

    // En yüksek sayıya sahip kategoriyi bul
    Object.entries(categories).forEach(([category, value]) => {
      const count = parseInt(value.N);
      if (count > maxCount) {
        maxCount = count;
        topCategory = category;
      }
    });

    if (!topCategory) {
      return res.json({ hasProfile: false });
    }

    res.json({
      hasProfile: true,
      topCategory,
      adContent: AD_CONTENTS[topCategory]
    });

  } catch (error) {
    console.error('Error fetching user top category:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 