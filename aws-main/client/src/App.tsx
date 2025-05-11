import { useState, useEffect } from 'react';
import { auth } from './services/api';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

export default function App() {
  console.log('App is rendering!');
  
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    console.log('API URL:', import.meta.env.VITE_API_URL);
    console.log('Checking auth status...');
    auth.checkStatus()
      .then(response => {
        console.log('Auth status response:', response);
        setIsAuthenticated(response.isAuthenticated);
      })
      .catch(error => {
        console.error('Auth check error:', error);
        setIsAuthenticated(false);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f9fafb',
      }}>
        <div style={{
          width: '2rem',
          height: '2rem',
          borderRadius: '50%',
          borderTop: '2px solid #3b82f6',
          borderBottom: '2px solid #3b82f6',
          animation: 'spin 1s linear infinite',
        }} />
      </div>
    );
  }

  return isAuthenticated ? (
    <Dashboard setIsAuthenticated={setIsAuthenticated} />
  ) : (
    <Login setIsAuthenticated={setIsAuthenticated} />
  );
}
  