export interface Transaction {
  id: number;
  user_id: number;
  amount: number;
  description: string;
  transaction_date: string;
  created_at: string;
}

export interface User {
  id: number;
  username: string;
}

export interface AuthResponse {
  success: boolean;
  error?: string;
}

export interface TransactionFormData {
  amount: number;
  description: string;
  transaction_date: string;
} 