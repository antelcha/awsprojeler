console.log('Script starting...');

import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App'

console.log('Imports completed');
console.log('main.tsx is executing');

const rootElement = document.getElementById('root');
console.log('Root element:', rootElement);

if (!rootElement) {
  console.error('Root element not found!');
  throw new Error('Failed to find the root element');
}

console.log('Creating React root...');
const root = ReactDOM.createRoot(rootElement);
console.log('React root created');

console.log('Starting render...');
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
console.log('Render called');
