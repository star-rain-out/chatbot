# Chatbot Project

A multi-functional chatbot project with React frontend and FastAPI backend, each feature has its own independent API interface.

## Project Structure

```
chatbot/
├── backend/           # FastAPI Backend
│   ├── routers/      # Independent Feature Modules
│   │   ├── auth.py   # User Authentication API
│   │   ├── chat_general.py  # General Q&A API
│   │   ├── tools_weather.py # Weather Query API
│   │   └── tools_translate.py # Translation API
│   ├── main.py       # Main Application Entry
│   └── requirements.txt
├── frontend/         # React Frontend
│   ├── pages/       # Page Components
│   │   ├── AuthPage.jsx    # Registration & Login Page
│   │   ├── Dashboard.jsx   # Main Interface
│   │   └── ChatPage.jsx    # Chat Page
│   └── src/App.js   # Main Application Component
└── README.md
```

## Features

- ✅ **User Registration and Login System** - Independent Authentication API
- ✅ **JWT Token Authentication** - Secure Session Management
- ✅ **Responsive Main Interface** - Display All Available Features
- ✅ **Independent API Design** - Each Feature Has Dedicated API Endpoint

## Implemented Features

1. **User Authentication** (`/api/auth/`)
   - User Registration - Independent Endpoint
   - User Login - Independent Endpoint
   - User Information Verification - Independent Endpoint

2. **Weather Query** (`/api/weather/`)
   - Real-time Weather Information Query - Independent Endpoint
   - Supports major cities: Beijing, Shanghai, Guangzhou, Shenzhen, etc.
   - Provides detailed information: temperature, humidity, air quality, UV index, etc.

3. **Currency Conversion** (`/api/currency/`)
   - Real-time Currency Exchange Rate Conversion - Independent Endpoint
   - Supports USD, CNY, EUR, GBP, JPY, KRW, HKD, CAD
   - Intelligent User Query Intent Recognition

4. **Translation Assistant** (`/api/translate/`)
   - Chinese-English Bidirectional Translation - Independent Endpoint
   - Supports Common Vocabulary and Phrase Translation
   - Automatic Language Detection

## Installation and Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start backend service:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Or simply run:
```bash
start-backend.bat
```

Backend will start at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start frontend development server:
```bash
npm start
```
Or simply run:
```bash
start-frontend.bat
```

Frontend will start at `http://localhost:3000`

### Project File Structure

```
chatbot/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main Application Entry
│   ├── requirements.txt       # Python Dependencies
│   ├── users.json            # User Data File (Created at Runtime)
│   └── routers/              # API Routing Modules
│       ├── auth.py           # User Authentication API
│       ├── chat_general.py   # General Q&A API
│       ├── tools_weather.py  # Weather Query API
│       └── tools_translate.py # Translation API
├── frontend/                  # React Frontend
│   ├── package.json          # Node.js Dependencies Configuration
│   ├── public/               # Static Resources
│   │   └── index.html       # HTML Template
│   └── src/                  # Source Code
│       ├── App.js           # Main Application Component
│       ├── index.js         # Application Entry
│       ├── index.css        # Global Styles (Including Tailwind)
│       └── pages/           # Page Components
│           ├── AuthPage.jsx     # Registration & Login Page
│           ├── Dashboard.jsx    # Main Function Interface
│           └── ChatPage.jsx     # Chat Function Page
├── start-frontend.bat        # Frontend Startup Script
├── start-backend.bat         # Backend Startup Script
└── README.md                # Project Documentation
```

## Usage Instructions

1. **Register New User**: Visit the application, click "Don't have an account? Sign Up"
2. **Login System**: Use your registered email and password to login
3. **Select Feature**: Click on feature cards on the main interface to enter corresponding chat mode
4. **Start Conversation**: Enter your questions on the chat page, the system will call the corresponding independent API

## API Documentation

After backend startup, you can visit the following addresses to view API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development Notes

- Each feature has an independent API endpoint, meeting your requirements
- JWT Token expiration time is 30 minutes
- User data is stored in `users.json` file (database recommended for production environment)
- Passwords are hashed using bcrypt
- CORS cross-origin requests supported

## Features That Can Be Added Next

Based on the reserved feature cards in the Dashboard, you can also add:
- Currency Converter (`/api/currency/`)
- Image Search (`/api/image/`)
- Trip Planning (`/api/itinerary/`)
- And more...

Each new feature needs to create independent API interfaces!