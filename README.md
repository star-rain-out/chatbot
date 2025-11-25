# 🇨🇳 China Travel AI Chatbot

A comprehensive AI-powered travel assistant for China with multiple features including weather forecasting, translation, ticket recognition, and more. Built with React (frontend) and FastAPI (backend).

## ✨ Features

### Core Features
- 🌤️ **Weather Forecast** - Real-time weather information for any city
- 🌐 **Language Translator** - English ↔ Chinese translation with audio pronunciation
- 💱 **Currency Converter** - Real-time exchange rates
- ✈️ **Travel Assistant** - AI-powered travel advice and recommendations
- 📸 **Landmark Recognition** - Identify landmarks from photos
- ✨ **Social Media Caption Generator** - Generate engaging captions from images
- 🌍 **Time Zone Converter** - Convert times between different time zones

### China Travel Features
- 🎫 **Attraction Tickets** - Query ticket prices and booking information
- 🏨 **Hotel Recommendations** - Get hotel suggestions for Chinese cities
- 🛣️ **Transport Planning** - Plan routes between cities
- 🍜 **China Experience** - Discover Chinese food, culture, and festivals
- 🛂 **Visa Information** - Get visa requirements and application guidelines
- 🛡️ **Travel Insurance** - Travel insurance recommendations
- 💰 **Budget Estimator** - Estimate travel costs

### New Features
- 🎫 **Ticket Recognition** - Extract information from PDF itinerary tickets
- 👤 **User Profile Management** - Avatar upload, profile editing
- 📱 **Phone Number Registration** - Optional phone number field

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 14.x or higher
- **npm**: 6.x or higher

### Dependencies
All dependencies are listed in:
- Backend: `backend/requirements.txt`
- Frontend: `frontend/package.json`

## 🚀 Quick Start

### Method 1: Using Startup Scripts (Windows)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd chatbot
```

2. **Start Backend**
```bash
start-backend.bat
```

3. **Start Frontend** (in a new terminal)
```bash
start-frontend.bat
```

4. **Access the application**
- Frontend: http://103.189.140.199:3000
- Backend API: http://103.189.140.199:8000
- API Docs: http://103.189.140.199:8000/docs

### Method 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
```

3. **Activate virtual environment**
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Start the backend server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://103.189.140.199:8000`

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```

The frontend will automatically open at `http://103.189.140.199:3000`

## 📁 Project Structure

```
chatbot/
├── backend/                      # FastAPI Backend
│   ├── main.py                  # Main application entry
│   ├── requirements.txt         # Python dependencies
│   ├── users.json              # User data storage (auto-created)
│   ├── static/                 # Static files (avatars, etc.)
│   └── routers/                # API route modules
│       ├── auth.py             # User authentication
│       ├── chat_general.py     # General chat
│       ├── tools_weather.py    # Weather API
│       ├── tools_translate.py  # Translation API
│       ├── tools_currency.py   # Currency converter
│       ├── tools_landmark.py   # Landmark recognition
│       ├── tools_social_media.py # Caption generator
│       ├── tools_timezone.py   # Time zone converter
│       ├── tools_attraction_tickets.py
│       ├── tools_hotel_booking.py
│       ├── tools_transport_route.py
│       ├── tools_china_experience.py
│       ├── tools_visa_info.py
│       ├── tools_travel_insurance.py
│       ├── tools_budget_estimator.py
│       └── tools_ticket_recognition.py  # PDF ticket extraction
├── frontend/                    # React Frontend
│   ├── package.json            # Node.js dependencies
│   ├── public/                 # Static resources
│   │   └── index.html         # HTML template
│   └── src/                   # Source code
│       ├── App.js             # Main app component
│       ├── index.js           # Entry point
│       ├── index.css          # Global styles (Tailwind CSS)
│       └── pages/             # Page components
│           ├── AuthPage.jsx   # Login/Register page
│           ├── Dashboard.jsx  # Main dashboard
│           └── ChatPage.jsx   # Chat interface
├── start-backend.bat          # Backend startup script
├── start-frontend.bat         # Frontend startup script
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## 🔧 Configuration

### Backend Configuration

The backend runs on port 8000 by default. To change:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port YOUR_PORT
```

### Frontend Configuration

If you change the backend port, update the API endpoints in:
- `frontend/src/pages/AuthPage.jsx`
- `frontend/src/pages/ChatPage.jsx`
- `frontend/src/pages/Dashboard.jsx`

Look for `http://103.189.140.199:8000` and replace with your backend URL.

## 👥 User Guide

### First Time Setup

1. **Register an Account**
   - Open the application
   - Click "Don't have an account? Sign Up"
   - Enter your name, email, password, and optionally phone number
   - Click "Sign Up"

2. **Login**
   - Enter your email and password
   - Click "Login"

3. **Upload Avatar (Optional)**
   - Click on your avatar in the top right
   - Select "Edit Profile"
   - Click on the avatar placeholder to upload an image

### Using Features

1. **Select a Feature**
   - Click on any feature card on the dashboard
   - Each feature opens a dedicated chat interface

2. **Chat Interface**
   - Type your question or request in the input box
   - For features requiring images (Landmark, Social Media), click the 📷 button
   - For PDF tickets (Ticket Recognition), click the 📄 button
   - Press Enter or click Send

3. **Ticket Recognition Usage**
   - Navigate to "Ticket Recognition" feature
   - Upload your PDF itinerary ticket
   - View extracted information:
     - Passenger name
     - Flight/Airline information
     - Origin and destination
     - Departure and arrival times
     - Confirmation and booking numbers

## 🔐 Security Features

- **Password Hashing**: Passwords are encrypted using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **Token Expiration**: 30-minute session timeout
- **CORS Protection**: Configured for 103.189.140.199 development

## 📡 API Documentation

After starting the backend, visit:
- **Swagger UI**: http://103.189.140.199:8000/docs
- **ReDoc**: http://103.189.140.199:8000/redoc

### Main API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/me` - Update user profile
- `POST /api/auth/upload_avatar` - Upload avatar

#### Features
- `POST /api/weather/query` - Weather information
- `POST /api/translate/do` - Translation
- `POST /api/currency/convert` - Currency conversion
- `POST /api/landmark/recognize` - Landmark recognition
- `POST /api/social_media/generate` - Caption generation
- `POST /api/timezone/convert` - Time zone conversion
- `POST /api/ticket_recognition/upload` - PDF ticket extraction
- And more... (see API docs for complete list)

## 🐛 Troubleshooting

### Backend won't start
- **Issue**: Port 8000 already in use
- **Solution**: Kill the process using port 8000 or use a different port

### Frontend won't start
- **Issue**: Port 3000 already in use
- **Solution**: Kill the process or the app will prompt to use a different port

### Import errors
- **Issue**: Missing Python packages
- **Solution**: Make sure you installed all requirements
```bash
pip install -r backend/requirements.txt
```

### Module not found errors (Frontend)
- **Issue**: Missing Node modules
- **Solution**: Install dependencies
```bash
cd frontend
npm install
```

### Login not working
- **Issue**: Backend not running or CORS error
- **Solution**: Ensure backend is running at http://103.189.140.199:8000

## 📦 Deployment

### For Production

1. **Backend Deployment**
   - Use a production ASGI server like Gunicorn
   - Set up proper environment variables
   - Use a real database instead of JSON file
   - Configure HTTPS

2. **Frontend Deployment**
   - Build the production version:
   ```bash
   npm run build
   ```
   - Serve the `build` folder using a web server (Nginx, Apache, etc.)
   - Update API endpoints to point to your production backend

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is available for use under standard open source practices.

## 🆘 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review this README
- Check the console for error messages

## 🎯 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Real-time notifications
- [ ] Multi-language support beyond English/Chinese
- [ ] Mobile app version
- [ ] Advanced ticket parsing with AI
- [ ] Group chat functionality
- [ ] Booking integration with real travel APIs

---

**Enjoy your China Travel AI Chatbot! 🚀✈️🇨🇳**