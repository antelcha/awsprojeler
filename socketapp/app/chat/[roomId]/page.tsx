'use client';

import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import io, { Socket } from 'socket.io-client';
import AdBanner from '@/app/components/AdBanner';

interface Message {
  id: string;
  username: string;
  text: string;
  timestamp: number;
}

export default function ChatRoom() {
  const params = useParams();
  const searchParams = useSearchParams();
  const roomId = params.roomId as string;
  const username = searchParams.get('username') || 'Anonymous';
  
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [connectionStatus, setConnectionStatus] = useState('Bağlanıyor...');

  useEffect(() => {
    console.log('Connecting to WebSocket...');
    const newSocket = io('http://localhost:3001', {
      query: { roomId, username },
      transports: ['websocket'],
      reconnection: true,
    });

    newSocket.on('connect', () => {
      console.log('Connected to WebSocket');
      setConnectionStatus('Bağlandı');
    });

    newSocket.on('connect_error', (error) => {
      console.error('Connection error:', error);
      setConnectionStatus('Bağlantı hatası');
    });

    newSocket.on('message', (message: Message) => {
      console.log('Received message:', message);
      setMessages(prev => [...prev, message]);
    });

    setSocket(newSocket);

    return () => {
      console.log('Disconnecting...');
      newSocket.close();
    };
  }, [roomId, username]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (socket && newMessage.trim()) {
      console.log('Sending message:', newMessage);
      const messageData = {
        text: newMessage,
        username,
        roomId,
        timestamp: Date.now()
      };
      socket.emit('message', messageData);
      setNewMessage('');
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <AdBanner username={username} />
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-black">Oda: {roomId}</h1>
              <p className="text-sm text-black">Kullanıcı: {username}</p>
            </div>
            <div className="text-sm text-black">
              {connectionStatus} • {messages.length} mesaj
            </div>
          </div>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-w-7xl mx-auto w-full">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.username === username ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`rounded-lg px-4 py-2 max-w-[70%] shadow-sm ${
                message.username === username
                  ? 'bg-black text-white'
                  : 'bg-white text-black'
              }`}
            >
              <div className={`font-medium text-sm ${
                message.username === username ? 'text-white' : 'text-black'
              }`}>
                {message.username}
              </div>
              <div className="mt-1">{message.text}</div>
              <div className={`text-xs mt-1 ${
                message.username === username ? 'text-white' : 'text-black'
              }`}>
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white border-t border-gray-200 p-4">
        <form onSubmit={sendMessage} className="max-w-7xl mx-auto">
          <div className="flex gap-4">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              className="flex-1 rounded-lg border-gray-300 shadow-sm focus:ring-2 focus:ring-black focus:border-transparent px-4 py-3 text-black placeholder-black/60"
              placeholder="Mesajınızı yazın..."
            />
            <button
              type="submit"
              className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-900 focus:ring-4 focus:ring-black/50 font-medium transition-all"
            >
              Gönder
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 