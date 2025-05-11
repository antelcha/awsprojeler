import express from 'express';
import cors from 'cors';
import session from 'express-session';
import pgSession from 'connect-pg-simple';
import { pool } from './db';
import authRoutes from './routes/auth';
import transactionRoutes from './routes/transactions';

const app = express();
const PORT = process.env.PORT || 3000;

// Log environment variables (excluding sensitive data)
console.log('Environment:', {
  NODE_ENV: process.env.NODE_ENV,
  PORT: process.env.PORT,
  HAS_DATABASE_URL: !!process.env.DATABASE_URL,
  HAS_SESSION_SECRET: !!process.env.SESSION_SECRET
});

const allowedOrigins = [
  'http://localhost:5173',
  'http://localhost:5174',
  'https://main.d1d1z3k019disz.amplifyapp.com',
  'https://db234zv43oe6l.cloudfront.net'
];

// Add trust proxy for CloudFront
app.set('trust proxy', 1);

app.use(cors({
  origin: function(origin, callback) {
    // Allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    
    if (process.env.NODE_ENV === 'development') {
      // In development, allow localhost with any port
      if (origin.startsWith('http://localhost:')) {
        return callback(null, origin);
      }
    }
    
    // In production, check against allowed origins
    if (allowedOrigins.includes(origin)) {
      return callback(null, origin);
    }
    
    callback(new Error('Not allowed by CORS'));
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: [
    'Content-Type', 
    'Authorization', 
    'Origin', 
    'X-Requested-With', 
    'Accept',
    'Access-Control-Allow-Origin',
    'Access-Control-Allow-Methods',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Credentials'
  ],
  exposedHeaders: ['Set-Cookie']
}));

// Add security headers middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Credentials', 'true');
  next();
});

app.use(express.json());

// Test database connection
pool.connect()
  .then(() => console.log('Database connected successfully'))
  .catch(err => console.error('Database connection error:', err));

const PostgresStore = pgSession(session);

// Configure session cookie settings based on environment
const cookieSettings = process.env.NODE_ENV === 'production' 
  ? {
      secure: true,
      httpOnly: true,
      sameSite: 'none' as const,
      maxAge: 24 * 60 * 60 * 1000,
      path: '/',
      domain: '.cloudfront.net'
    }
  : {
      secure: false,
      httpOnly: true,
      sameSite: 'lax' as const,
      maxAge: 24 * 60 * 60 * 1000,
      path: '/'
    };

app.use(session({
  store: new PostgresStore({
    pool,
    tableName: 'sessions'
  }),
  secret: process.env.SESSION_SECRET || 'your_session_secret',
  resave: false,
  saveUninitialized: false,
  proxy: process.env.NODE_ENV === 'production',
  cookie: cookieSettings
}));

// Add session debug middleware
app.use((req, res, next) => {
  console.log('Session:', req.session);
  console.log('Cookies:', req.cookies);
  console.log('Headers:', req.headers);
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    env: process.env.NODE_ENV
  });
});

app.use('/api/auth', authRoutes);
app.use('/api/transactions', transactionRoutes);

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal Server Error', message: err.message });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('Environment:', process.env.NODE_ENV);
  console.log('Allowed origins:', allowedOrigins);
}); 