'use client';

import { useEffect, useState } from 'react';

interface UserProfile {
  username: string;
  tags: {
    [key: string]: number;
  };
  categories: {
    [key: string]: number;
  };
}

export default function AdminPanel() {
  const [profiles, setProfiles] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfiles = async () => {
      try {
        const response = await fetch('http://localhost:3001/api/admin/profiles');
        if (!response.ok) {
          throw new Error('Profil verileri alınamadı');
        }
        const data = await response.json();
        setProfiles(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Bir hata oluştu');
      } finally {
        setLoading(false);
      }
    };

    fetchProfiles();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-xl font-semibold">Yükleniyor...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-xl font-semibold text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-black mb-8">Admin Paneli</h1>
        
        <div className="grid grid-cols-1 gap-6">
          {profiles.map((profile) => (
            <div key={profile.username} className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-black mb-4">{profile.username}</h2>
              
              <div className="grid grid-cols-2 gap-8">
                <div>
                  <h3 className="text-lg font-medium text-black mb-3">Etiket İstatistikleri</h3>
                  <div className="space-y-2">
                    {Object.entries(profile.tags).map(([tag, count]) => (
                      <div key={tag} className="flex justify-between items-center">
                        <span className="text-black">{tag}</span>
                        <span className="bg-black text-white px-2 py-1 rounded">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-medium text-black mb-3">Kategori İstatistikleri</h3>
                  <div className="space-y-2">
                    {Object.entries(profile.categories).map(([category, count]) => (
                      <div key={category} className="flex justify-between items-center">
                        <span className="text-black">{category}</span>
                        <span className="bg-black text-white px-2 py-1 rounded">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 