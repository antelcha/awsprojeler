import { useState } from 'react';
import { auth } from '../services/api';

interface LoginProps {
  setIsAuthenticated: (value: boolean) => void;
}

export default function Login({ setIsAuthenticated }: LoginProps) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = isRegister
        ? await auth.register(username, password)
        : await auth.login(username, password);

      if (response.success) {
        setIsAuthenticated(true);
      } else {
        setError(response.error || 'Authentication failed');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
    }
  };

  const containerStyle = {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'center',
    padding: '2rem',
    backgroundColor: '#f9fafb',
  };

  const formContainerStyle = {
    maxWidth: '400px',
    margin: '0 auto',
    backgroundColor: 'white',
    padding: '2rem',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  };

  const titleStyle = {
    marginBottom: '2rem',
    fontSize: '1.875rem',
    fontWeight: '600',
    textAlign: 'center' as const,
    color: '#111827',
  };

  const inputStyle = {
    width: '100%',
    padding: '0.5rem 0.75rem',
    marginBottom: '1rem',
    borderRadius: '0.375rem',
    border: '1px solid #d1d5db',
    fontSize: '0.875rem',
  };

  const buttonStyle = {
    width: '100%',
    padding: '0.5rem 1rem',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
  };

  const toggleStyle = {
    marginTop: '1rem',
    textAlign: 'center' as const,
    fontSize: '0.875rem',
    color: '#3b82f6',
    cursor: 'pointer',
    background: 'none',
    border: 'none',
    width: '100%',
  };

  const errorStyle = {
    color: '#dc2626',
    fontSize: '0.875rem',
    marginBottom: '1rem',
    textAlign: 'center' as const,
  };

  return (
    <div style={containerStyle}>
      <div style={formContainerStyle}>
        <h2 style={titleStyle}>
          {isRegister ? 'Create Account' : 'Sign In'}
        </h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={inputStyle}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputStyle}
            required
          />
          {error && <div style={errorStyle}>{error}</div>}
          <button type="submit" style={buttonStyle}>
            {isRegister ? 'Register' : 'Sign In'}
          </button>
          <button
            type="button"
            onClick={() => setIsRegister(!isRegister)}
            style={toggleStyle}
          >
            {isRegister ? 'Already have an account? Sign in' : "Don't have an account? Register"}
          </button>
        </form>
      </div>
    </div>
  );
} 