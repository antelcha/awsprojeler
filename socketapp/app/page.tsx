'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [roomNumber, setRoomNumber] = useState('');
  const [username, setUsername] = useState('');
  const router = useRouter();

  const handleJoinRoom = (e: React.FormEvent) => {
    e.preventDefault();
    if (roomNumber && username) {
      router.push(`/chat/${roomNumber}?username=${username}`);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-8">
        <h1 className="text-3xl font-bold text-black text-center mb-8">
          Chat Odası
        </h1>
        <form onSubmit={handleJoinRoom} className="space-y-6">
          <div>
            <label htmlFor="roomNumber" className="block text-sm font-medium text-black mb-2">
              Oda Numarası
            </label>
            <input
              type="text"
              id="roomNumber"
              value={roomNumber}
              onChange={(e) => setRoomNumber(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              placeholder="Örn: 12345"
              required
            />
          </div>
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-black mb-2">
              Kullanıcı Adı
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              placeholder="Örn: mustafa"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-black text-white py-3 px-4 rounded-lg hover:bg-gray-900 focus:ring-4 focus:ring-black/50 font-medium transition-all"
          >
            Odaya Katıl
          </button>
        </form>
        <button
          onClick={() => router.push('/admin')}
          className="w-full mt-4 bg-gray-900 text-white py-3 px-4 rounded-lg hover:bg-black focus:ring-4 focus:ring-black/50 font-medium transition-all"
        >
          Admin Girişi
        </button>
      </div>
    </div>
  );
}
