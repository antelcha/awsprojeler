import { Session } from 'express-session';

declare module 'express-session' {
  interface SessionData {
    userId: number;
  }
}

export interface User {
  id: number;
  username: string;
  password: string;
}

export interface Transaction {
  id: number;
  user_id: number;
  amount: number;
  description: string;
  transaction_date: Date;
  created_at: Date;
} 