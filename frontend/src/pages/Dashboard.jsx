import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [userAvatar, setUserAvatar] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
    phone_number: '',
    password: '',
    avatar_url: ''
  });

  useEffect(() => {
    // Get username from localStorage or verify token
    const token = localStorage.getItem('token');
    const savedUserName = localStorage.getItem('user_name');

    if (token) {
      if (savedUserName) {
        setUserName(savedUserName);
        // Attempt to fetch full user info even if name is saved, to get email/avatar
        fetchUserInfo();
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
      setUserEmail(response.data.email);
      setUserAvatar(response.data.avatar_url);
      setProfileData({
        name: response.data.name,
        email: response.data.email,
        phone_number: response.data.phone_number || '',
        password: '',
        avatar_url: response.data.avatar_url || ''
      });
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

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const updateData = {
        name: profileData.name,
        phone_number: profileData.phone_number
      };

      if (profileData.password) {
        updateData.password = profileData.password;
      }

      const response = await axios.put('http://localhost:8000/api/auth/me', updateData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setUserName(response.data.user.name);
      setUserEmail(response.data.user.email);
      setUserAvatar(response.data.user.avatar_url);
      setProfileData(prev => ({ ...prev, password: '', name: response.data.user.name, avatar_url: response.data.user.avatar_url }));
      localStorage.setItem('user_name', response.data.user.name);
      alert('Profile updated successfully!');
      setShowProfileModal(false);
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile.');
    }
  };

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8000/api/auth/upload_avatar', formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setUserAvatar(response.data.avatar_url);
      setProfileData(prev => ({ ...prev, avatar_url: response.data.avatar_url }));
    } catch (error) {
      console.error('Failed to upload avatar:', error);
      alert('Failed to upload avatar.');
    }
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
    },
    {
      id: 'ticket_recognition',
      name: '🎫 Ticket Recognition',
      desc: 'Extract info from PDF tickets',
      color: 'from-orange-500 to-red-600'
    },
    {
      id: 'image_search',
      name: '🖼️ Image Search',
      desc: 'Find beautiful images of any place',
      color: 'from-cyan-400 to-blue-600'
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
              China Travel Assistant
            </h1>
            <p className="text-gray-600 text-sm mt-1">Hello, {userName}! Choose a feature to start your China journey</p>
          </div>

          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2 focus:outline-none"
            >
              {userAvatar ? (
                <img src={userAvatar} alt="Avatar" className="w-10 h-10 rounded-full object-cover border-2 border-white shadow-sm" />
              ) : (
                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-sm">
                  {userName.charAt(0).toUpperCase()}
                </div>
              )}
            </button>

            {/* Dropdown Menu */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl py-2 z-20 border border-gray-100">
                <div className="px-4 py-2 border-b border-gray-100">
                  <p className="font-semibold text-gray-800 truncate">{userName}</p>
                  <p className="text-xs text-gray-500 truncate">{userEmail}</p>
                </div>
                <button
                  onClick={() => {
                    setShowUserMenu(false);
                    setShowProfileModal(true);
                  }}
                  className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors flex items-center gap-2"
                >
                  <span>✏️</span> Edit Profile
                </button>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2"
                >
                  <span>🚪</span> Sign Out
                </button>
              </div>
            )}
          </div>
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

      {/* Profile Modal */}
      {showProfileModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-6 text-white flex justify-between items-center">
              <h3 className="text-xl font-bold">Edit Profile</h3>
              <button onClick={() => setShowProfileModal(false)} className="text-white/80 hover:text-white text-2xl">&times;</button>
            </div>

            <div className="p-6 max-h-[80vh] overflow-y-auto">
              <div className="flex flex-col items-center mb-6">
                <div className="relative group cursor-pointer">
                  {profileData.avatar_url ? (
                    <img src={profileData.avatar_url} alt="Avatar" className="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg" />
                  ) : (
                    <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center text-gray-400 text-3xl border-4 border-white shadow-lg">
                      📷
                    </div>
                  )}
                  <div className="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <span className="text-white text-sm font-semibold">Change</span>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarUpload}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-2">Click to upload new avatar</p>
              </div>

              <form onSubmit={handleUpdateProfile} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    value={profileData.name}
                    onChange={e => setProfileData({ ...profileData, name: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={profileData.email}
                    disabled
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 bg-gray-50 text-gray-500 cursor-not-allowed"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    type="tel"
                    value={profileData.phone_number}
                    onChange={e => setProfileData({ ...profileData, phone_number: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="Optional"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
                  <input
                    type="password"
                    value={profileData.password}
                    onChange={e => setProfileData({ ...profileData, password: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    placeholder="Leave blank to keep current"
                  />
                </div>

                <div className="pt-4 flex gap-3">
                  <button
                    type="button"
                    onClick={() => setShowProfileModal(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
                  >
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;