import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const ChatPage = () => {
  const { featureId } = useParams(); // 获取当前是哪个功能
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState('general');
  const [selectedTone, setSelectedTone] = useState('friendly');
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 根据 featureId 映射到不同的后端 API URL
  const getApiEndpoint = () => {
    switch (featureId) {
      case 'weather': return 'http://localhost:8000/api/weather/query';
      case 'translate': return 'http://localhost:8000/api/translate/do';
      case 'currency': return 'http://localhost:8000/api/currency/convert';
      case 'travel': return 'http://localhost:8000/api/travel/ask';
      case 'landmark': return null; // Special case - uses file upload
      case 'social_media': return null; // Special case - uses file upload
      case 'timezone': return 'http://localhost:8000/api/timezone/convert';
      // 新增的中国旅游功能
      case 'attraction_tickets': return 'http://localhost:8000/api/attraction_tickets/query';
      case 'hotel_booking': return 'http://localhost:8000/api/hotel_recommendations/recommend';
      case 'transport_route': return 'http://localhost:8000/api/transport_route/plan';
      case 'china_experience': return 'http://localhost:8000/api/china_experience/explore';
      case 'visa_info': return 'http://localhost:8000/api/visa_info/query';
      case 'travel_insurance': return 'http://localhost:8000/api/travel_insurance/recommend';
      case 'budget_estimator': return 'http://localhost:8000/api/budget_estimator/estimate';
      case 'ticket_recognition': return 'http://localhost:8000/api/ticket_recognition/upload';
      default: return null;
    }
  };

  // Get feature information
  const getFeatureInfo = () => {
    switch (featureId) {
      case 'weather':
        return {
          title: '🌤️ Weather Assistant',
          placeholder: 'e.g., What is the weather like in London?',
          welcomeMessage: 'I can help you check real-time weather information for any city, including temperature, weather conditions, air quality, and more. Which city weather would you like to know about?'
        };
      case 'translate':
        return {
          title: '🌐 Language Translator',
          placeholder: 'Enter text to translate (English or Chinese)',
          welcomeMessage: 'I can help you translate between English and Chinese. Please enter the text you want to translate, and I will automatically detect the language and translate it for you.'
        };
      case 'currency':
        return {
          title: '💱 Currency Converter',
          placeholder: 'e.g., How much is 100 USD in CNY?',
          welcomeMessage: 'I can help you convert between different currencies with real-time exchange rates. Please tell me which currencies and amount you want to convert, for example "How much is 100 USD in CNY?".'
        };
      case 'travel':
        return {
          title: '✈️ Travel Assistant',
          placeholder: 'Ask anything about travel destinations, tips, or planning...',
          welcomeMessage: 'Hello! I\'m your AI travel assistant. I can help you with destination recommendations, travel planning, local customs, transportation options, accommodation suggestions, and any other travel-related questions. What would you like to know about your travel plans?'
        };
      case 'landmark':
        return {
          title: '📸 Landmark Recognition',
          placeholder: 'Upload an image or describe a landmark...',
          welcomeMessage: 'Welcome to Landmark Recognition! Upload a photo of a landmark, and I\'ll identify it for you along with interesting facts, location information, and travel tips. You can also describe a landmark in text if you prefer.',
          isLandmarkMode: true
        };
      case 'social_media':
        return {
          title: '✨ Social Media Caption Generator',
          placeholder: 'Upload an image to generate captions...',
          welcomeMessage: 'Welcome to Social Media Caption Generator! Upload a photo, and I\'ll create engaging captions perfect for your social media posts. Choose your preferred platform and tone to get personalized content with relevant hashtags.',
          isSocialMediaMode: true
        };
      case 'timezone':
        return {
          title: '🌍 Time Zone Converter',
          placeholder: 'e.g., Vancouver time to Beijing time',
          welcomeMessage: 'Welcome to Time Zone Converter! Convert times between different time zones worldwide. Perfect for scheduling international meetings, planning travel, or coordinating with global teams.'
        };
      // 新增的中国旅游功能配置
      case 'attraction_tickets':
        return {
          title: '🎫 Attraction Tickets',
          placeholder: 'Enter attraction name to query ticket information...',
          welcomeMessage: 'Welcome to Attraction Tickets Query Assistant! I can provide you with detailed information about ticket prices, booking details, opening hours for major attractions in China. Which attraction would you like to know about?'
        };
      case 'hotel_booking':
        return {
          title: '🏨 Hotel Recommendations',
          placeholder: 'Enter city name to get hotel recommendations...',
          welcomeMessage: 'Welcome to Hotel Recommendations Assistant! I can recommend quality hotels in various Chinese cities, providing detailed information about amenities, locations, and suitability for different types of travelers. Which city would you like hotel recommendations for?'
        };
      case 'transport_route':
        return {
          title: '🛣️ Transport Planning',
          placeholder: 'Enter departure and destination cities...',
          welcomeMessage: 'Welcome to Transport Planning Assistant! I can provide you with transportation route suggestions within China, including comparisons of flights, high-speed trains, buses, and other travel methods. What are your departure and destination cities?'
        };
      case 'china_experience':
        return {
          title: '🍜🏮🎊 China Experience',
          placeholder: 'Ask about food, culture, or festivals...',
          welcomeMessage: 'Welcome to China Experience Explorer! I can guide you through authentic Chinese cuisine, rich cultural traditions, and vibrant festivals. Whether you want to know about regional specialties, traditional customs, or festival celebrations, I\'m here to help! What aspect of Chinese culture interests you most?'
        };
      case 'visa_info':
        return {
          title: '🛂 Visa Information',
          placeholder: 'Enter your nationality to query visa requirements...',
          welcomeMessage: 'Welcome to China Visa Information Assistant! I can provide you with the latest China visa policies and application guidelines, including document checklists, application processes, fees, and time requirements. What is your nationality?'
        };
      case 'travel_insurance':
        return {
          title: '🛡️ Travel Insurance',
          placeholder: 'Enter travel type and requirements...',
          welcomeMessage: 'Welcome to Travel Insurance Guide! I can provide professional travel insurance recommendations, including product comparisons, cost analysis, risk assessment, and claims guidance. Let your China journey be more secure and worry-free!'
        };
      case 'budget_estimator':
        return {
          title: '💰 Travel Budget Estimator',
          placeholder: 'Enter destination, duration, and travel style...',
          welcomeMessage: 'Welcome to Travel Budget Estimator! I can help you estimate comprehensive travel costs for China, including accommodation, food, transportation, activities, and more. Just tell me your destination, duration, travel style, group size, and I\'ll provide a detailed budget breakdown!'
        };
      case 'ticket_recognition':
        return {
          title: '🎫 Ticket Recognition',
          placeholder: 'Upload a PDF ticket to extract information...',
          welcomeMessage: 'Welcome to Ticket Recognition! Please upload a PDF file of your itinerary ticket, and I will extract the key information for you.'
        };
      default:
        return {
          title: '🇨🇳 China Travel Assistant',
          placeholder: 'Please enter your question...',
          welcomeMessage: `You have entered the [${featureId}] feature. I am your China travel assistant, how can I help you?`
        };
    }
  };

  const featureInfo = getFeatureInfo();

  // 初始化欢迎语
  useEffect(() => {
    setMessages([{
      sender: 'bot',
      text: featureInfo.welcomeMessage
    }]);
  }, [featureId]);

  const sendMessage = async () => {
    // Handle landmark mode separately
    if (featureId === 'landmark') {
      if (selectedFile) {
        await uploadAndRecognizeLandmark();
      } else if (input.trim()) {
        await describeLandmarkText();
      }
      return;
    }

    // Handle social media mode separately
    if (featureId === 'social_media') {
      if (selectedFile) {
        await generateSocialMediaCaption();
      }
      return;
    }

    // Handle ticket recognition mode separately
    if (featureId === 'ticket_recognition') {
      if (selectedFile) {
        // Handle PDF upload for ticket recognition
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
          // Show typing status
          setMessages(prev => [...prev, { sender: 'bot', text: 'Processing ticket...', isTyping: true }]);

          const res = await axios.post('http://localhost:8000/api/ticket_recognition/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });

          setMessages(prev => prev.filter(msg => !msg.isTyping));

          const extractedInfo = res.data;
          const responseText = `
**Ticket Information Extracted:**
- **Origin:** ${extractedInfo.origin}
- **Destination:** ${extractedInfo.destination}
- **Date:** ${extractedInfo.date}
- **Ticket Number:** ${extractedInfo.ticket_number}

**Raw Text:**
${extractedInfo.raw_text.substring(0, 200)}...
                `;

          const botMsg = {
            sender: 'bot',
            text: responseText
          };
          setMessages(prev => [...prev, botMsg]);
        } catch (error) {
          console.error('Error uploading ticket:', error);
          setMessages(prev => prev.filter(msg => !msg.isTyping));
          setMessages(prev => [...prev, {
            sender: 'bot',
            text: 'Sorry, I failed to process the ticket. Please try again.'
          }]);
        }
        setSelectedFile(null);
      }
      return;
    }

    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    const currentInput = input;
    setInput('');

    const apiUrl = getApiEndpoint();
    if (!apiUrl) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'This feature is not yet connected.' }]);
      return;
    }

    try {
      // Show typing status
      setMessages(prev => [...prev, { sender: 'bot', text: 'Processing your request...', isTyping: true }]);

      // Send request to independent API
      let requestBody = {};
      switch (featureId) {
        case 'weather':
          requestBody = { user_input: currentInput };
          break;
        case 'translate':
          requestBody = { text: currentInput };
          break;
        case 'currency':
          requestBody = { query: currentInput };
          break;
        case 'attraction_tickets':
          requestBody = { attraction_name: currentInput };
          break;
        case 'hotel_booking':
          requestBody = { city: currentInput };
          break;
        case 'transport_route':
          const separators = [' to ', ' To ', ' TO ', '到'];
          let fromCity = currentInput;
          let toCity = '';
          for (const sep of separators) {
            if (currentInput.includes(sep)) {
              [fromCity, toCity] = currentInput.split(sep);
              break;
            }
          }
          requestBody = { from_city: fromCity.trim(), to_city: toCity.trim() };
          break;
        case 'china_experience':
          requestBody = { query_type: currentInput };
          break;
        case 'visa_info':
          requestBody = { nationality: currentInput };
          break;
        case 'travel_insurance':
          requestBody = { travel_type: currentInput };
          break;
        case 'budget_estimator':
          requestBody = {
            destination: currentInput.split(',')[0] || 'Beijing',
            duration_days: parseInt(currentInput.split(',')[1]) || 7,
            travel_style: 'mid_range',
            group_size: 1
          };
          break;
        case 'timezone':
          requestBody = { query: currentInput };
          break;
        case 'travel':
          requestBody = { question: currentInput };
          break;
        default:
          requestBody = { user_input: currentInput, text: currentInput };
      }

      const res = await axios.post(apiUrl, requestBody);

      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const botMsg = {
        sender: 'bot',
        text: res.data.bot_response || res.data.response || res.data.result || 'Processing complete',
        audio: res.data.audio_base64
      };
      setMessages(prev => [...prev, botMsg]);

    } catch (error) {
      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      let errorMessage = 'Service error, please try again later.';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          // Handle Pydantic validation errors
          errorMessage = detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('\n');
        } else {
          errorMessage = detail;
        }
      }
      setMessages(prev => [...prev, { sender: 'bot', text: errorMessage }]);
    }
  };

  // Landmark recognition functions
  const uploadAndRecognizeLandmark = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('image', selectedFile);

    // Add user message with file info
    const userMsg = {
      sender: 'user',
      text: `📷 Uploaded image: ${selectedFile.name}`,
      isImage: true,
      imageName: selectedFile.name
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      setUploading(true);
      // Show typing status
      setMessages(prev => [...prev, { sender: 'bot', text: 'Analyzing the image...', isTyping: true }]);

      const res = await axios.post('http://localhost:8000/api/landmark/recognize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const botMsg = {
        sender: 'bot',
        text: res.data.result || res.data.response || 'Landmark recognition complete'
      };
      setMessages(prev => [...prev, botMsg]);

    } catch (error) {
      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      let errorMessage = 'Landmark recognition failed, please try again.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      setMessages(prev => [...prev, { sender: 'bot', text: errorMessage }]);
    } finally {
      setUploading(false);
      setSelectedFile(null);
    }
  };

  const describeLandmarkText = async () => {
    const currentInput = input.trim();
    if (!currentInput) return;

    const userMsg = { sender: 'user', text: currentInput };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
      // Show typing status
      setMessages(prev => [...prev, { sender: 'bot', text: 'Analyzing your description...', isTyping: true }]);

      const res = await axios.post('http://localhost:8000/api/landmark/describe', {
        description: currentInput
      });

      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const botMsg = {
        sender: 'bot',
        text: res.data.result || res.data.response || 'Analysis complete'
      };
      setMessages(prev => [...prev, botMsg]);

    } catch (error) {
      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      let errorMessage = 'Analysis failed, please try again.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      setMessages(prev => [...prev, { sender: 'bot', text: errorMessage }]);
    }
  };

  // Social Media Caption Generation
  const generateSocialMediaCaption = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('platform', selectedPlatform);
    formData.append('tone', selectedTone);
    formData.append('hashtags_count', '5');

    // Add user message with file info
    const userMsg = {
      sender: 'user',
      text: `📷 Uploaded image for ${selectedPlatform} (${selectedTone} tone): ${selectedFile.name}`,
      isImage: true,
      imageName: selectedFile.name
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      setUploading(true);
      // Show typing status
      setMessages(prev => [...prev, { sender: 'bot', text: 'Generating social media caption...', isTyping: true }]);

      const res = await axios.post('http://localhost:8000/api/social_media/generate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      const botMsg = {
        sender: 'bot',
        text: res.data.bot_response || 'Social media caption generation complete'
      };
      setMessages(prev => [...prev, botMsg]);

    } catch (error) {
      // Remove typing message
      setMessages(prev => prev.filter(msg => !msg.isTyping));

      let errorMessage = 'Caption generation failed, please try again.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      setMessages(prev => [...prev, { sender: 'bot', text: errorMessage }]);
    } finally {
      setUploading(false);
      setSelectedFile(null);
    }
  };



  // File input handler
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (featureId === 'ticket_recognition') {
      if (file && file.type === 'application/pdf') {
        setSelectedFile(file);
        // Auto send for ticket recognition
        // Note: We can't call sendMessage directly here because state update is async
        // We'll rely on the user clicking send or we could use useEffect to watch selectedFile
      } else {
        alert('Please select a valid PDF file.');
      }
    } else if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
    } else {
      alert('Please select a valid image file.');
    }
  };

  const renderMessageText = (text) => {
    if (!text) return '';
    const strText = String(text);

    let processedText = strText;

    // 1. Handle Code Blocks (extract them first to avoid messing up content inside)
    const codeBlocks = [];
    processedText = processedText.replace(/```([\s\S]*?)```/g, (match, codeContent) => {
      codeBlocks.push(codeContent);
      return `__CODE_BLOCK_${codeBlocks.length - 1}__`;
    });

    // 2. Handle Inline Code
    processedText = processedText.replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-1 rounded text-xs">$1</code>');

    // 3. Handle Headers (## and ###)
    processedText = processedText.replace(/(^|\n)###\s+(.+)/g, '$1<h3 class="text-lg font-bold mt-2 mb-1">$2</h3>');
    processedText = processedText.replace(/(^|\n)##\s+(.+)/g, '$1<h2 class="text-xl font-bold mt-3 mb-2">$2</h2>');

    // 4. Handle Bold (**text**)
    processedText = processedText.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // 5. Handle Italic (*text*)
    processedText = processedText.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // 6. Handle Bullet Points
    processedText = processedText.replace(/(^|\n)-\s+(.+)/g, '$1<li class="ml-4">$2</li>');

    // 7. Restore Code Blocks
    processedText = processedText.replace(/__CODE_BLOCK_(\d+)__/g, (match, index) => {
      const codeContent = codeBlocks[index].trim();
      return `<pre class="bg-gray-100 p-2 rounded text-xs font-mono overflow-x-auto whitespace-pre my-2">${codeContent}</pre>`;
    });

    // 8. Convert remaining newlines to <br>
    processedText = processedText.replace(/\n/g, '<br>');

    // Cleanup <br> after headers and list items to avoid extra spacing
    processedText = processedText.replace(/<\/h2><br>/g, '</h2>');
    processedText = processedText.replace(/<\/h3><br>/g, '</h3>');
    processedText = processedText.replace(/<\/pre><br>/g, '</pre>');
    processedText = processedText.replace(/<\/li><br>/g, '</li>');

    return processedText;
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-blue-50 to-purple-50">
      {/* 顶部导航栏 */}
      <div className="bg-white/80 backdrop-blur-sm shadow-sm p-4 flex items-center">
        <button
          onClick={() => navigate('/dashboard')}
          className="mr-4 text-gray-600 hover:text-black transition-colors flex items-center gap-2"
        >
          ← Back to Features
        </button>
        <h1 className="font-bold text-xl text-gray-800 flex items-center gap-2">
          {featureInfo.title}
        </h1>
      </div>

      {/* 聊天内容区 */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} items-end gap-2`}
            >
              {msg.sender === 'bot' && (
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-sm">🤖</span>
                </div>
              )}
              <div
                className={`max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl ${msg.sender === 'user'
                  ? 'bg-blue-500 text-white rounded-br-sm'
                  : msg.isTyping
                    ? 'bg-gray-100 text-gray-500 rounded-bl-sm animate-pulse'
                    : 'bg-white text-gray-800 shadow-md rounded-bl-sm'
                  }`}
              >
                <div
                  className="text-sm leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: renderMessageText(msg.text) }}
                />
                {msg.audio && (
                  <div className="mt-3 pt-2 border-t border-gray-100">
                    <p className="text-xs text-gray-500 mb-1">🔊 Pronunciation:</p>
                    <audio controls src={`data:audio/mp3;base64,${msg.audio}`} className="w-full h-8" />
                  </div>
                )}
              </div>
              {msg.sender === 'user' && (
                <div className="w-8 h-8 bg-gray-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-sm">👤</span>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* 输入框 */}
      <div className="p-4 bg-white/80 backdrop-blur-sm border-t border-gray-200">
        <div className="max-w-3xl mx-auto">
          {featureId === 'social_media' ? (
            // Social Media mode special UI
            <div className="space-y-3">
              {/* Platform and Tone Selection */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Platform</label>
                  <select
                    value={selectedPlatform}
                    onChange={(e) => setSelectedPlatform(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                  >
                    <option value="general">General Format</option>
                    <option value="wechat">WeChat Moments</option>
                    <option value="weibo">Weibo</option>
                    <option value="instagram">Instagram</option>
                    <option value="twitter">Twitter</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tone</label>
                  <select
                    value={selectedTone}
                    onChange={(e) => setSelectedTone(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                  >
                    <option value="friendly">Friendly</option>
                    <option value="casual">Casual</option>
                    <option value="professional">Professional</option>
                    <option value="humorous">Humorous</option>
                  </select>
                </div>
              </div>

              {/* File upload area */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="social-media-image-upload"
                />
                <label htmlFor="social-media-image-upload" className="cursor-pointer">
                  <div className="space-y-2">
                    <div className="text-4xl">📸</div>
                    <p className="text-sm text-gray-600">
                      {selectedFile ? `Selected: ${selectedFile.name}` : 'Click to upload an image for caption generation'}
                    </p>
                    <p className="text-xs text-gray-400">PNG, JPG, GIF up to 10MB</p>
                  </div>
                </label>
              </div>

              {/* Generate button */}
              <div className="flex gap-3 items-center">
                <button
                  onClick={generateSocialMediaCaption}
                  className="flex-1 bg-indigo-500 hover:bg-indigo-600 disabled:bg-gray-300 text-white px-6 py-3 rounded-full transition-colors flex items-center justify-center gap-2"
                  disabled={uploading || !selectedFile}
                >
                  <span>{uploading ? 'Generating...' : 'Generate Caption'}</span>
                  <span>{uploading ? '⏳' : '✨'}</span>
                </button>
              </div>
            </div>
          ) : featureId === 'landmark' ? (
            // Landmark mode special UI
            <div className="space-y-3">
              {/* File upload area */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="image-upload"
                />
                <label htmlFor="image-upload" className="cursor-pointer">
                  <div className="space-y-2">
                    <div className="text-4xl">📷</div>
                    <p className="text-sm text-gray-600">
                      {selectedFile ? `Selected: ${selectedFile.name}` : 'Click to upload an image or drag and drop'}
                    </p>
                    <p className="text-xs text-gray-400">PNG, JPG, GIF up to 10MB</p>
                  </div>
                </label>
              </div>

              {/* OR separator */}
              <div className="flex items-center gap-4">
                <div className="flex-1 h-px bg-gray-300"></div>
                <span className="text-sm text-gray-500">OR</span>
                <div className="flex-1 h-px bg-gray-300"></div>
              </div>

              {/* Text description input */}
              <div className="flex gap-3 items-center">
                <div className="flex-1 relative">
                  <input
                    className="w-full border border-gray-300 rounded-full px-4 py-3 pr-12 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyPress={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                    placeholder="Describe a landmark in text..."
                  />
                  <div className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400">
                    <span className="text-xl">✏️</span>
                  </div>
                </div>
                <button
                  onClick={selectedFile ? uploadAndRecognizeLandmark : sendMessage}
                  className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-6 py-3 rounded-full transition-colors flex items-center gap-2"
                  disabled={uploading || (!selectedFile && !input.trim())}
                >
                  <span>{uploading ? 'Processing...' : (selectedFile ? 'Analyze Image' : 'Send')}</span>
                  <span>{uploading ? '⏳' : '→'}</span>
                </button>
              </div>
            </div>

          ) : featureId === 'ticket_recognition' ? (
            // Ticket Recognition mode special UI
            <div className="space-y-3">
              {/* File upload area */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="ticket-upload"
                />
                <label htmlFor="ticket-upload" className="cursor-pointer">
                  <div className="space-y-2">
                    <div className="text-4xl">📄</div>
                    <p className="text-sm text-gray-600">
                      {selectedFile ? `Selected: ${selectedFile.name}` : 'Click to upload a PDF ticket'}
                    </p>
                    <p className="text-xs text-gray-400">PDF files only</p>
                  </div>
                </label>
              </div>

              {/* Send button */}
              <div className="flex gap-3 items-center">
                <button
                  onClick={sendMessage}
                  className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-6 py-3 rounded-full transition-colors flex items-center justify-center gap-2"
                  disabled={!selectedFile}
                >
                  <span>Process Ticket</span>
                  <span>→</span>
                </button>
              </div>
            </div>
          ) : (
            // Regular input for other features
            <div className="flex gap-3 items-center">
              <div className="flex-1 relative">
                <input
                  className="w-full border border-gray-300 rounded-full px-4 py-3 pr-12 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyPress={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                  placeholder={featureInfo.placeholder}
                />
                <div className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400">
                  <span className="text-xl">💬</span>
                </div>
              </div>
              <button
                onClick={sendMessage}
                className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-6 py-3 rounded-full transition-colors flex items-center gap-2"
                disabled={!input.trim()}
              >
                <span>Send</span>
                <span>→</span>
              </button>
            </div>
          )}
          <div className="text-center text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
