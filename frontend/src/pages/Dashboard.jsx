import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get username from localStorage or verify token
    const token = localStorage.getItem('token');
    const savedUserName = localStorage.getItem('user_name');

    if (token) {
      if (savedUserName) {
        setUserName(savedUserName);
        setLoading(false);
      } else {
        // If no saved username, fetch from API
        fetchUserInfo();
      }
    } else {
      navigate('/auth');
    }
  }, [navigate]);

  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setUserName(response.data.name);
      localStorage.setItem('user_name', response.data.name);
    } catch (error) {
      console.error('Failed to fetch user info:', error);
      // Token might have expired, redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user_name');
      navigate('/auth');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_name');
    navigate('/auth');
  };

  // Define all features with ID (for routing) and display names
  const features = [
    {
      id: 'weather',
      name: '🌤️ Weather Forecast',
      desc: 'Check real-time weather for any city',
      color: 'from-blue-400 to-blue-600'
    },
    {
      id: 'translate',
      name: '🌐 Language Translator',
      desc: 'Translate between English and Chinese',
      color: 'from-green-400 to-green-600'
    },
    {
      id: 'currency',
      name: '💱 Currency Converter',
      desc: 'Real-time currency exchange rates',
      color: 'from-yellow-400 to-yellow-600'
    },
    {
      id: 'travel',
      name: '✈️ Travel Assistant',
      desc: 'AI-powered travel advice and recommendations',
      color: 'from-purple-400 to-purple-600'
    },
    {
      id: 'landmark',
      name: '📸 Landmark Recognition',
      desc: 'Identify landmarks from your photos',
      color: 'from-pink-400 to-pink-600'
    },
    {
      id: 'social_media',
      name: '✨ Social Media Caption',
      desc: 'Generate engaging captions from photos',
      color: 'from-indigo-400 to-indigo-600'
    },
    {
      id: 'timezone',
      name: '🌍 Time Zone Converter',
      desc: 'Convert times between time zones',
      color: 'from-teal-400 to-teal-600'
    },
    {
      id: 'attraction_tickets',
      name: '🎫 Attraction Tickets',
      desc: 'Query attraction ticket prices and booking info',
      color: 'from-red-400 to-red-600'
    },
    {
      id: 'hotel_booking',
      name: '🏨 Hotel Recommendations',
      desc: 'Get hotel recommendations for Chinese cities',
      color: 'from-blue-500 to-blue-700'
    },
    {
      id: 'budget_estimator',
      name: '💰 Budget Estimator',
      desc: 'Estimate travel costs for China trips',
      color: 'from-green-500 to-green-700'
    },
    {
      id: 'transport_route',
      name: '🛣️ Transport Planning',
      desc: 'Plan transportation routes between cities',
      color: 'from-green-500 to-green-700'
    },
    {
      id: 'china_experience',
      name: '🍜🏮🎊 China Experience',
      desc: 'Discover food, culture, and festivals',
      color: 'from-purple-500 to-orange-600'
    },
    {
      id: 'visa_info',
      name: '🛂 Visa Information',
      desc: 'Get visa information for traveling to China',
      color: 'from-indigo-500 to-indigo-700'
    },
    {
      id: 'travel_insurance',
      name: '🛡️ Travel Insurance',
      desc: 'Get travel insurance recommendations',
      color: 'from-teal-500 to-teal-700'
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Top navigation bar */}
      <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <span className="text-3xl">🇨🇳</span>
              China Travel Assistant
            </h1>
            <p className="text-gray-600 text-sm mt-1">Hello, {userName}! Choose a feature to start your China journey</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Sign Out
          </button>
        </div>
      </header>

      {/* Main content area */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Welcome message card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-start gap-4">
            <div className="text-4xl">👋</div>
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Welcome to China Travel Assistant</h2>
              <p className="text-gray-600">
                I am your exclusive China travel assistant, providing comprehensive travel services.
                Choose the features you need to start planning your China journey:
              </p>
            </div>
          </div>
        </div>

        {/* Feature cards grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-8">
          {features.map((f) => (
            <div
              key={f.id}
              onClick={() => navigate(`/feature/${f.id}`)}
              className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:scale-105"
            >
              {/* Gradient background */}
              <div className={`absolute inset-0 bg-gradient-to-br ${f.color} opacity-90`}></div>

              {/* Content */}
              <div className="relative p-6 text-white">
                <div className="text-3xl mb-3">{f.name.split(' ')[0]}</div>
                <div className="text-lg font-bold mb-2">{f.name.split(' ').slice(1).join(' ')}</div>
                <div className="text-white/80 text-sm">{f.desc}</div>

                {/* Hover tooltip */}
                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="bg-white text-gray-800 px-4 py-2 rounded-lg font-semibold">
                    Start Chat →
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Tips */}
        <div className="text-center text-gray-500 text-sm">
          <p>💡 Click on any feature card to start a conversation and plan your China journey</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;