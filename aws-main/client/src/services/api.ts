import axios, { InternalAxiosRequestConfig, AxiosHeaders } from 'axios';
import { Transaction, AuthResponse, TransactionFormData } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Access-Control-Allow-Credentials': 'true'
  },
  validateStatus: function (status) {
    return status >= 200 && status < 500;
  }
});

// Add request interceptor
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (!config.headers) {
    config.headers = new AxiosHeaders();
  }
  config.headers['Access-Control-Allow-Credentials'] = 'true';
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.log('Unauthorized - redirecting to login');
    }
    return Promise.reject(error);
  }
);

export const auth = {
  register: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', { username, password });
    return response.data;
  },

  login: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },

  logout: async (): Promise<AuthResponse> => {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  checkStatus: async (): Promise<{ isAuthenticated: boolean }> => {
    const response = await api.get('/auth/status');
    return response.data;
  }
};

export const transactions = {
  getLast7Days: async (): Promise<Transaction[]> => {
    const response = await api.get('/transactions/last-7-days');
    return response.data;
  },

  getLast30Days: async (): Promise<Transaction[]> => {
    const response = await api.get('/transactions/last-30-days');
    return response.data;
  },

  create: async (data: TransactionFormData): Promise<Transaction> => {
    const response = await api.post('/transactions', data);
    return response.data;
  },

  update: async (id: number, data: TransactionFormData): Promise<Transaction> => {
    const response = await api.put(`/transactions/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/transactions/${id}`);
  }
}; 