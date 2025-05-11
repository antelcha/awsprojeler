import { useEffect, useState } from 'react';

interface AdContent {
  title: string;
  description: string;
  backgroundColor: string;
  link: string;
}

interface AdBannerProps {
  username: string;
}

export default function AdBanner({ username }: AdBannerProps) {
  const [adContent, setAdContent] = useState<AdContent | null>(null);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const fetchAdContent = async () => {
      try {
        const response = await fetch(`http://localhost:3001/api/user/top-category/${username}`);
        const data = await response.json();
        
        if (data.hasProfile && data.adContent) {
          setAdContent(data.adContent);
        }
      } catch (error) {
        console.error('Error fetching ad content:', error);
      }
    };

    fetchAdContent();
  }, [username]);

  if (!adContent || !isVisible) return null;

  return (
    <div 
      className="relative w-full"
      style={{ backgroundColor: adContent.backgroundColor }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div className="flex items-center justify-between">
          <a 
            href={adContent.link}
            className="flex-1 text-white hover:opacity-90 transition-opacity"
          >
            <h3 className="text-lg font-semibold">{adContent.title}</h3>
            <p className="text-sm opacity-90">{adContent.description}</p>
          </a>
          <button
            onClick={() => setIsVisible(false)}
            className="ml-4 text-white opacity-70 hover:opacity-100 transition-opacity"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
} 